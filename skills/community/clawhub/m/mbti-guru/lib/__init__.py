#!/usr/bin/env python3
"""
MBTI Guru - OpenClaw Skill Interface
支持所有 OpenClaw 渠道: Telegram, Discord, 飞书, 微信等
"""

from lib.mbti_core import (
    process_message,
    process_start,
    process_resume,
    process_history,
    process_status,
    process_cancel,
    get_version_selection_text,
    get_progress_bar,
    get_history_text,
    VERSIONS
)

__all__ = [
    'process_message',
    'process_start',
    'process_resume',
    'process_history',
    'process_status',
    'process_cancel',
    'get_version_selection_text',
    'get_progress_bar',
    'get_history_text',
    'VERSIONS'
]
