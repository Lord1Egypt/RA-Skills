#!/usr/bin/env python3
"""
command_parser.py - 指令解析模块
"""

import json
import os
import re
from typing import Optional, Tuple

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")


def load_config() -> dict:
    """加载配置"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_command(text: str) -> Tuple[str, Optional[str]]:
    """
    解析清空/状态指令

    Args:
        text: 用户输入的原始文本

    Returns:
        (命令类型, 消息ID或None)
        命令类型: "clear", "status", "unknown"
        消息ID: 如果是 #清空 消息ID 格式，返回消息ID
    """
    config = load_config()
    
    clear_cmd = config.get("clear_command", "#清空")
    status_cmd = config.get("status_command", "#队列状态")
    
    text = text.strip()

    # 解析状态指令
    if text == status_cmd:
        return ("status", None)
    
    # 解析清空指令（无参数）
    if text == clear_cmd:
        return ("clear", None)
    
    # 解析清空指令（带消息ID）
    # 格式: #清空 uuid-xxx
    clear_pattern = rf"^{re.escape(clear_cmd)}\s+(\S+)$"
    match = re.match(clear_pattern, text)
    if match:
        msg_id = match.group(1)
        return ("clear", msg_id)
    
    return ("unknown", None)


def is_retry_command(text: str) -> bool:
    """判断是否是重试相关的指令"""
    if text.strip().startswith("#"):
        return True
    return False
