#!/usr/bin/env python3
"""
queue_manager.py - 队列读写操作模块
"""

import json
import uuid
import os
from datetime import datetime, timedelta
from typing import Optional

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(SKILL_DIR, "retry_queue.json")
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")


def load_config() -> dict:
    """加载配置"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_queue() -> dict:
    """加载队列数据"""
    if not os.path.exists(QUEUE_FILE):
        return {"pending": [], "completed": [], "cleared": []}
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(queue: dict) -> None:
    """保存队列数据"""
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def add_to_queue(
    sender_id: str,
    channel: str,
    session_key: str,
    original_message: str,
    error_message: str
) -> str:
    """
    添加消息到待重试队列

    去重逻辑：同一渠道 + 同一用户 + 同样内容 → 丢弃

    Returns:
        生成的唯一消息ID，如果是重复消息返回None
    """
    config = load_config()
    queue = load_queue()

    # 去重检查：同一渠道 + 同一用户 + 同样内容
    is_duplicate = any(
        msg["original_message"] == original_message
        and msg["sender_id"] == sender_id
        and msg["channel"] == channel
        for msg in queue["pending"]
    )
    
    if is_duplicate:
        return None  # 丢弃重复消息

    msg_id = str(uuid.uuid4())
    now = datetime.now()
    
    # 计算首次重试时间
    wait_hours = config.get("initial_wait_hours", 1)
    next_retry = now + timedelta(hours=wait_hours)

    item = {
        "id": msg_id,
        "sender_id": sender_id,
        "channel": channel,
        "session_key": session_key,
        "original_message": original_message,
        "sent_at": now.isoformat(),
        "retry_count": 0,
        "next_retry_at": next_retry.isoformat(),
        "last_error": error_message
    }

    queue["pending"].append(item)
    save_queue(queue)

    return msg_id


def remove_from_queue(msg_id: str) -> bool:
    """
    从 pending 队列中移除指定消息

    Returns:
        是否成功移除
    """
    queue = load_queue()
    original_count = len(queue["pending"])
    queue["pending"] = [msg for msg in queue["pending"] if msg["id"] != msg_id]
    
    if len(queue["pending"]) < original_count:
        save_queue(queue)
        return True
    return False


def mark_completed(msg_id: str, response: str = "") -> None:
    """标记消息为已完成"""
    queue = load_queue()
    
    for i, msg in enumerate(queue["pending"]):
        if msg["id"] == msg_id:
            msg["completed_at"] = datetime.now().isoformat()
            msg["response"] = response
            queue["completed"].append(msg)
            queue["pending"].pop(i)
            break
    
    # 只保留最近100条 completed 记录
    if len(queue["completed"]) > 100:
        queue["completed"] = queue["completed"][-100:]
    
    save_queue(queue)


def mark_cleared(msg_id: str) -> None:
    """标记消息为已清空"""
    queue = load_queue()
    
    for i, msg in enumerate(queue["pending"]):
        if msg["id"] == msg_id:
            msg["cleared_at"] = datetime.now().isoformat()
            queue["cleared"].append(msg)
            queue["pending"].pop(i)
            break
    
    if len(queue["cleared"]) > 100:
        queue["cleared"] = queue["cleared"][-100:]
    
    save_queue(queue)


def get_pending_for_sender(sender_id: str) -> list:
    """获取指定发送者的所有待重试消息"""
    queue = load_queue()
    return [msg for msg in queue["pending"] if msg["sender_id"] == sender_id]


def get_all_pending() -> list:
    """获取所有待重试消息"""
    queue = load_queue()
    return queue["pending"]


def get_queue_status(sender_id: Optional[str] = None) -> dict:
    """
    获取队列状态

    Args:
        sender_id: 如果指定，只返回该发送者的状态
    """
    queue = load_queue()
    
    if sender_id:
        pending = get_pending_for_sender(sender_id)
    else:
        pending = queue["pending"]
    
    return {
        "pending_count": len(pending),
        "pending_messages": pending,
        "total_completed": len(queue["completed"]),
        "total_cleared": len(queue["cleared"])
    }


def increment_retry(msg_id: str) -> Optional[dict]:
    """
    增加消息的重试次数，返回更新后的消息或None

    指数退避策略：initial_wait_minutes * 2^(retry_count) 分钟
    例如 initial_wait=30min: 30 → 60 → 120 → 240 → 480

    Returns:
        更新后的消息对象，或None如果未找到
    """
    queue = load_queue()
    
    for msg in queue["pending"]:
        if msg["id"] == msg_id:
            msg["retry_count"] += 1
            
            # 从消息本身读取初始间隔（Plugin 入队时写入的）
            initial_wait = msg.get("initial_wait_minutes", 30)
            # 指数退避：wait = initial * 2^retry_count 分钟
            wait_minutes = initial_wait * (2 ** msg["retry_count"])
            next_retry = datetime.now() + timedelta(minutes=wait_minutes)
            
            msg["next_retry_at"] = next_retry.isoformat()
            msg["last_retry_at"] = datetime.now().isoformat()
            msg["last_retry_status"] = "pending"
            
            save_queue(queue)
            return msg
    
    return None


def update_error(msg_id: str, error_message: str) -> None:
    """更新消息的最后错误信息"""
    queue = load_queue()
    
    for msg in queue["pending"]:
        if msg["id"] == msg_id:
            msg["last_error"] = error_message
            break
    
    save_queue(queue)
