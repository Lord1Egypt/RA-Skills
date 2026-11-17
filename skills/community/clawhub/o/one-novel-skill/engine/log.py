#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一日志框架 — 所有引擎通过此模块输出日志

基于标准库 logging，与 generator.py 共享同一日志体系。
支持: LOG_LEVEL=DEBUG|INFO|WARN|ERROR 环境变量
输出格式: [LEVEL] [engine] message
"""

import logging
import os
import sys

# 配置一次（模块级配置）
_logger = logging.getLogger("one-novel-skill")
if not _logger.handlers:
    _level_name = os.environ.get("LOG_LEVEL", "WARN").upper()
    _level = getattr(logging, _level_name, logging.WARN)
    _logger.setLevel(_level)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    _logger.addHandler(_handler)


def debug(engine, msg):
    _logger.debug("[%s] %s", engine, msg)


def info(engine, msg):
    _logger.info("[%s] %s", engine, msg)


def warn(engine, msg):
    _logger.warning("[%s] %s", engine, msg)


def error(engine, msg, exc=None):
    _logger.error("[%s] %s", engine, msg)
    if exc:
        import traceback
        traceback.print_exc()


def safe_call(engine, fn, *args, default=None, **kwargs):
    """安全调用: 捕获异常, 返回默认值"""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        error(engine, f"{getattr(fn, "__name__", repr(fn))} failed: {e}", exc=True)
        return default