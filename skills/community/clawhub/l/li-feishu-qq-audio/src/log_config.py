"""
日志配置模块
功能：统一配置日志输出到文件和控制台

使用方式：
    from log_config import get_logger
    logger = get_logger(__name__)
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# 日志目录配置
LOG_DIR = os.environ.get('LOG_DIR', '/tmp/openclaw')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    获取配置好的 logger 实例
    
    Args:
        name: logger 名称（通常为 __name__）
    
    Returns:
        配置好的 logger 实例
    """
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # 创建 formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. 控制台处理器（输出到 stderr，不干扰 stdout）
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. 文件处理器（按日期创建日志文件）
    log_file = os.path.join(LOG_DIR, f"{name.split('.')[-1]}-{datetime.now().strftime('%Y-%m-%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# 预配置的 logger 实例
default_logger = get_logger('li-feishu-audio')
