# GxpCode Skill — 共享日志/错误处理

import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "gxpcode_data", "logs")

def get_logger(name: str) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(
            os.path.join(LOG_DIR, f"run_{datetime.now().strftime('%Y%m%d')}.log"),
            encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

class ErrorLevel:
    FATAL = "FATAL"
    SOURCE_SKIP = "SOURCE_SKIP"
    ITEM_SKIP = "ITEM_SKIP"
    DEGRADED = "DEGRADED"
