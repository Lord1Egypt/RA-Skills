"""日志工具：写到 logs/gold-tracker.log，带轮转与备份（可审计）。

零第三方依赖，使用标准库 logging + RotatingFileHandler。
"""

import logging
import logging.handlers

from . import paths

_LOGGERS = {}


def get_logger(name="gold-tracker"):
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    paths.resolve("logs").mkdir(parents=True, exist_ok=True)
    fh = logging.handlers.RotatingFileHandler(
        paths.resolve("logs/gold-tracker.log"),
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    _LOGGERS[name] = logger
    return logger
