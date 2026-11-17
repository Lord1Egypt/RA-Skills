# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
统一日志配置模块

提供结构化日志能力，支持：
- 统一格式（JSON / 文本）
- 级别控制
- 模块级日志隔离
- 性能友好的懒加载

使用方式：
    from scripts.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("模块初始化完成")
    logger.debug("详细调试信息", extra={"key": "value"})
"""

from __future__ import annotations

import logging
import os
import sys
import json
import time
from typing import Any, Optional


# ============================================================================
# 日志级别映射
# ============================================================================

LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# ============================================================================
# 结构化日志格式化器
# ============================================================================


class StructuredFormatter(logging.Formatter):
    """
    结构化 JSON 日志格式化器

    输出格式：
    {
        "timestamp": "2024-01-01T00:00:00.000Z",
        "level": "INFO",
        "logger": "scripts.perception",
        "message": "模块初始化完成",
        "module": "perception",
        "function": "__init__",
        "line": 42,
        "extra_key": "extra_value"
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为 JSON 字符串"""
        log_entry = {
            "timestamp": self._format_timestamp(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 添加异常信息
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        # 添加额外字段
        for key in ["extra_data", "user_id", "session_id", "operation",
                     "duration_ms", "memory_count", "chain_type"]:
            value = getattr(record, key, None)
            if value is not None:
                log_entry[key] = value

        try:
            return json.dumps(log_entry, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            # JSON 序列化失败时降级为文本格式
            return f"[{log_entry['level']}] {log_entry['logger']}: {log_entry['message']}"

    def _format_timestamp(self, record: logging.LogRecord) -> str:
        """格式化时间戳为 ISO 8601 格式"""
        return time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.gmtime(record.created)
        ) + f".{int(record.msecs):03d}Z"


class TextFormatter(logging.Formatter):
    """
    人类可读的文本日志格式化器

    输出格式：
    2024-01-01 00:00:00 [INFO] scripts.perception: 模块初始化完成
    """

    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


# ============================================================================
# 日志配置管理
# ============================================================================

_initialized = False
_log_level: int = logging.INFO
_log_format: str = "text"  # "text" or "json"


def _get_log_level_from_env() -> int:
    """从环境变量获取日志级别"""
    level_str = os.environ.get("AGENT_MEMORY_LOG_LEVEL", "INFO").upper()
    return LOG_LEVEL_MAP.get(level_str, logging.INFO)


def _get_log_format_from_env() -> str:
    """从环境变量获取日志格式"""
    return os.environ.get("AGENT_MEMORY_LOG_FORMAT", "text").lower()


def _initialize_logging() -> None:
    """初始化日志系统（仅执行一次）"""
    global _initialized, _log_level, _log_format

    if _initialized:
        return

    _log_level = _get_log_level_from_env()
    _log_format = _get_log_format_from_env()

    # 配置根日志器
    root_logger = logging.getLogger("scripts")
    root_logger.setLevel(_log_level)

    # 清除已有的处理器
    root_logger.handlers.clear()

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(_log_level)

    # 设置格式化器
    if _log_format == "json":
        formatter = StructuredFormatter()
    else:
        formatter = TextFormatter()

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 防止日志传播到根日志器
    root_logger.propagate = False

    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """
    获取模块日志器

    Args:
        name: 日志器名称，通常传入 __name__

    Returns:
        配置好的 Logger 实例

    使用示例：
        logger = get_logger(__name__)
        logger.info("操作完成")
        logger.error("操作失败", extra={"error_code": 500})
    """
    _initialize_logging()
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """
    动态设置日志级别

    Args:
        level: 日志级别字符串（DEBUG/INFO/WARNING/ERROR/CRITICAL）
    """
    global _log_level
    _log_level = LOG_LEVEL_MAP.get(level.upper(), logging.INFO)

    root_logger = logging.getLogger("scripts")
    root_logger.setLevel(_log_level)
    for handler in root_logger.handlers:
        handler.setLevel(_log_level)


def set_log_format(fmt: str) -> None:
    """
    动态设置日志格式

    Args:
        fmt: 日志格式（text/json）
    """
    global _log_format, _initialized
    _log_format = fmt.lower()

    # 重新初始化以应用新格式
    _initialized = False
    _initialize_logging()


# ============================================================================
# 便捷日志装饰器
# ============================================================================


def log_execution(logger_name: str = ""):
    """
    函数执行日志装饰器

    自动记录函数进入、退出和执行时间。

    使用示例：
        @log_execution("scripts.perception")
        def process_data(data):
            ...
    """
    def decorator(func):
        import functools

        _logger = get_logger(logger_name or func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            _logger.debug(f"Entering {func_name}")
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                _logger.debug(
                    f"Exiting {func_name}",
                    extra={"duration_ms": round(duration_ms, 2)}
                )
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                _logger.error(
                    f"Error in {func_name}: {e}",
                    extra={"duration_ms": round(duration_ms, 2)}
                )
                raise

        return wrapper
    return decorator


# ============================================================================
# 模块初始化时输出日志系统信息
# ============================================================================

def get_log_info() -> dict:
    """获取当前日志系统配置信息"""
    return {
        "initialized": _initialized,
        "level": logging.getLevelName(_log_level),
        "format": _log_format,
        "handlers": len(logging.getLogger("scripts").handlers),
    }
