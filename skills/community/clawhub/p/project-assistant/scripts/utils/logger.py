#!/usr/bin/env python3
"""
统一日志模块
提供统一的日志记录功能

使用方式:
    from utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("消息")
    logger.debug("调试信息")
    logger.error("错误信息")
"""

import os
import sys
import logging
import time
from datetime import datetime
from typing import Optional
from pathlib import Path


# 日志级别映射
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

# 默认日志格式
DEFAULT_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DETAILED_FORMAT = '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'

# 全局日志配置
_log_level = logging.INFO
_log_format = DEFAULT_FORMAT
_log_file: Optional[str] = None
_loggers = {}


def configure_logging(
    level: str = 'INFO',
    log_file: Optional[str] = None,
    detailed: bool = False,
    env_prefix: str = 'CLAUDE'
) -> None:
    """配置全局日志设置

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径
        detailed: 是否使用详细格式
        env_prefix: 环境变量前缀
    """
    global _log_level, _log_format, _log_file

    # 从环境变量读取配置
    env_level = os.environ.get(f'{env_prefix}_LOG_LEVEL', '').upper()
    if env_level in LOG_LEVELS:
        level = env_level

    env_file = os.environ.get(f'{env_prefix}_LOG_FILE', '')
    if env_file:
        log_file = env_file

    _log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    _log_format = DETAILED_FORMAT if detailed else DEFAULT_FORMAT
    _log_file = log_file

    # 重新配置所有已存在的 logger
    for name, logger in _loggers.items():
        _configure_logger(logger)


def _configure_logger(logger: logging.Logger) -> None:
    """配置单个 logger"""
    logger.setLevel(_log_level)

    # 清除现有 handlers
    logger.handlers.clear()

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(_log_level)
    console_handler.setFormatter(logging.Formatter(_log_format))
    logger.addHandler(console_handler)

    # 文件 handler
    if _log_file:
        try:
            log_path = Path(_log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(_log_file, encoding='utf-8')
            file_handler.setLevel(_log_level)
            file_handler.setFormatter(logging.Formatter(_log_format))
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"无法创建日志文件: {e}")


def get_logger(name: str = None) -> logging.Logger:
    """获取 logger 实例

    Args:
        name: logger 名称，通常使用 __name__

    Returns:
        配置好的 logger 实例
    """
    if name is None:
        name = 'claude-project-assistant'

    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    _configure_logger(logger)
    _loggers[name] = logger

    return logger


class LoggerAdapter:
    """日志适配器，提供更简洁的API"""

    def __init__(self, name: str = None):
        self._logger = get_logger(name)
        self._start_time: Optional[float] = None

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self._logger.exception(msg, *args, **kwargs)

    def start_timer(self, msg: str = None) -> None:
        """开始计时"""
        self._start_time = time.time()
        if msg:
            self.debug(msg)

    def end_timer(self, msg: str = "耗时") -> float:
        """结束计时并记录"""
        if self._start_time is None:
            return 0.0

        elapsed = time.time() - self._start_time
        self.debug(f"{msg}: {elapsed:.2f}s")
        self._start_time = None
        return elapsed

    def progress(self, current: int, total: int, msg: str = "进度") -> None:
        """记录进度"""
        if total > 0:
            percent = (current / total) * 100
            self.info(f"{msg}: {current}/{total} ({percent:.1f}%)")
        else:
            self.info(f"{msg}: {current}")

    def separator(self, title: str = "", char: str = "=", width: int = 50) -> None:
        """打印分隔符"""
        if title:
            padding = (width - len(title) - 2) // 2
            line = char * padding + f" {title} " + char * padding
            if len(line) < width:
                line += char * (width - len(line))
        else:
            line = char * width
        self.info(line)


# 便捷函数
def create_logger(name: str = None) -> LoggerAdapter:
    """创建日志适配器"""
    return LoggerAdapter(name)


# 初始化默认配置
def init_from_env():
    """从环境变量初始化日志配置"""
    configure_logging()


# 自动初始化
init_from_env()


if __name__ == '__main__':
    # 测试
    logger = create_logger("test")
    logger.separator("日志测试")
    logger.info("这是一条信息")
    logger.debug("这是一条调试信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")

    logger.start_timer("开始操作...")
    time.sleep(0.1)
    logger.end_timer("操作完成")

    logger.progress(5, 10, "处理文件")
    logger.separator()