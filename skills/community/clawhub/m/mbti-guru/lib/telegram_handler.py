#!/usr/bin/env python3
"""
MBTI Guru - Telegram Handler
基于 mbti_core 的 Telegram 适配器
支持所有 OpenClaw 渠道
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# 导入核心处理模块
from lib.mbti_core import (
    process_message,
    process_start,
    process_resume,
    process_history,
    process_status,
    process_cancel,
    process_answer,
    process_version_select,
    get_version_selection_text,
    get_progress_bar,
    get_history_text,
    VERSIONS
)

# 兼容旧接口
def handle_message(chat_id: int, text: str):
    """Telegram 消息处理"""
    return process_message(chat_id, text)

def handle_callback(chat_id: int, data: str):
    """Telegram 回调处理"""
    if data == "resume":
        return process_resume(chat_id)
    elif data.startswith("version_"):
        version_key = data.split("_")[1]
        return process_version_select(chat_id, version_key)
    elif data == "history":
        return process_history(chat_id)
    return {"action": "send", "message": "未知操作"}

# 导出
__all__ = [
    'handle_message',
    'handle_callback',
    'process_message',
    'process_start',
    'process_resume',
    'process_history',
    'process_status',
    'process_cancel',
    'get_version_selection_text',
    'get_progress_bar',
    'VERSIONS'
]
