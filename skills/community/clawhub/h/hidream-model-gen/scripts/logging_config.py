#!/usr/bin/env python3
"""
统一日志配置

Usage:
    from logging_config import get_logger
    logger = get_logger(__name__)
"""
import logging
import sys
from typing import Optional


DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    level: int = logging.INFO,
    format_str: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
    handler: Optional[logging.Handler] = None
) -> None:
    """
    配置根日志记录器
    
    Args:
        level: 日志级别，默认 INFO
        format_str: 日志格式
        date_format: 日期格式
        handler: 自定义handler，默认使用StreamHandler
    """
    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
    
    formatter = logging.Formatter(format_str, date_format)
    handler.setFormatter(formatter)
    
    # 配置根记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)
    
    # 设置第三方库的日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取命名日志记录器"""
    return logging.getLogger(name)


# 默认配置（在导入时自动应用）
configure_logging()
