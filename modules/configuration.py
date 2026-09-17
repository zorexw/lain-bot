import logging
import logging.handlers
import sys
import typing
from itertools import cycle

import dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = dotenv.find_dotenv()

class Settings(BaseSettings):

    DISCORD_TOKEN: SecretStr

    LOGGING_LEVEL: typing.Literal["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"] = "INFO"

    BOT_PREFIX: str = "."
    LAIN_COLOR: int = 0x5b00c1

    ACTIVITY_NAMES: cycle = cycle([
        {
            "name": "everyone is always connected 🤍",
            "streaming_url": ""
        },
        {
            "name": "Don't talk to me like I'm a machine,I'm not that.",
            "streaming_url": ""
        }
    ])

    BOT_LOGS_CHANNEL_ID:           int = 1550215370588291072
    GUILD_ID:                      int = 1550207026947297280
    AUTOMOD_LOGS_CHANNEL_ID:       int = 1550215471922675752
    NEWS_CHANNEL_ID:               int = 1550211953308471376

    AUTOMOD_WHITELISTED_ROLES_IDS: typing.List[int] = [
        1550211047078502500,
    ]

    ADS_CHANNELS_IDS: typing.List[int] = [
        0,
    ]

    PROTECTED_CHANNELS_IDS: typing.List[int] = [
        1550212696753045595,
        1550211953308471376,
        1550207027626647574,
        1550214746706550866
    ]

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, enable_decoding="utf-8"
    )

CONFIG = Settings()

# Логирование
def setup_logging():
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(
        logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
    )

    backup_handler = logging.handlers.TimedRotatingFileHandler(
        filename='logs/tmp.log', 
        when='D', 
        interval=1, 
        backupCount=10, 
        encoding='utf-8', 
        delay=False
    )
    backup_handler.setFormatter(
        logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
    )
    
    root_logger.setLevel(CONFIG.LOGGING_LEVEL)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(backup_handler)
    
    logging.getLogger('discord').setLevel(logging.ERROR)
    logging.getLogger('discord.client').setLevel(logging.ERROR)
    logging.getLogger('discord.gateway').setLevel(logging.ERROR)
    # logging.getLogger('discord.http').setLevel(logging.ERROR)
    logging.getLogger('discord.webhook.async_').setLevel(logging.ERROR)

setup_logging()
