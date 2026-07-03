#!/usr/bin/env python3
"""
retry_worker.py - 重试逻辑模块

由 Cron 定时任务调用，检查队列并执行重试
"""

import json
import os
import sys
import subprocess
import re
from datetime import datetime
from typing import Optional, List, Dict, Any

# 添加父目录到路径，以便导入 queue_manager
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from queue_manager import (
    load_queue, save_queue, load_config,
    get_all_pending, get_pending_for_sender,
    mark_completed, increment_retry, update_error
)

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))


def should_retry_now(msg: dict) -> bool:
    """
    判断消息是否应该现在重试
    
    比较 next_retry_at 和当前时间，早于或等于当前时间则可重试
    """
    next_retry_str = msg.get("next_retry_at", "")
    if not next_retry_str:
        return True
    
    # 兼容带 Z 时区后缀的 ISO 格式
    next_retry_str = next_retry_str.replace('Z', '+00:00')
    try:
        next_retry = datetime.fromisoformat(next_retry_str)
    except ValueError:
        return True
    
    return datetime.now() >= next_retry


def build_retry_message(msg: dict) -> str:
    """
    构建重试消息
    格式：[RETRY:id=xxx] 原始消息
    
    兼容三种字段名（历史遗留问题）：
    - originalMessage (JS plugin 新版)
    - original_message (queue_manager.py 旧版定义)
    - userMessage (早期版本)
    """
    # 兼容三种字段名
    original = (
        msg.get('originalMessage') or
        msg.get('original_message') or
        msg.get('userMessage') or
        ''
    )
    return f"[RETRY:id={msg['id']}] {original}"


def send_via_sessions_send(session_key: str, message: str) -> tuple[bool, str]:
    """
    通过 openclaw sessions_send 发送消息
    
    Returns:
        (success: bool, message: str)
    """
    try:
        cmd = [
            "openclaw", "sessions", "send",
            session_key,
            "--message", message
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "sent"
        else:
            return False, result.stderr or result.stdout
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except FileNotFoundError:
        return False, "openclaw CLI not found"
    except Exception as e:
        return False, str(e)


def process_queue() -> dict:
    """
    处理重试队列的主函数
    
    逻辑：
    1. 读取队列
    2. 遍历 pending，找出到期消息（next_retry_at <= 当前时间）
    3. 对到期消息：
       a. 如果 retry_count >= max_retry → 标记失败，移到 completed
       b. 否则 → 发送 RETRY 消息 → increment_retry → 更新状态
    4. 返回统计结果
    
    Returns:
        包含处理统计的字典
    """
    config = load_config()
    max_retry = config.get("max_retry_count", 5)
    queue_file = os.path.join(SKILL_DIR, "retry_queue.json")
    
    # 读取队列
    if not os.path.exists(queue_file):
        return {
            "processed": 0,
            "sent": 0,
            "failed": 0,
            "skipped": 0,
            "max_retry_reached": 0,
            "errors": []
        }
    
    with open(queue_file, "r", encoding="utf-8") as f:
        queue = json.load(f)
    
    pending = queue.get("pending", [])
    stats = {
        "processed": 0,
        "sent": 0,
        "failed": 0,
        "skipped": 0,
        "max_retry_reached": 0,
        "errors": []
    }
    
    for msg in pending:
        stats["processed"] += 1
        
        # 检查是否应该重试
        if not should_retry_now(msg):
            stats["skipped"] += 1
            continue
        
        msg_id = msg.get("id", "")
        session_key = msg.get("sessionKey", msg.get("session_key", ""))
        retry_count = msg.get("retry_count", 0)
        
        # 检查是否超过最大重试次数
        if retry_count >= max_retry:
            # 标记为失败
            queue = mark_completed(msg_id, "max_retry_exceeded")
            if queue is None:
                queue = load_queue()
            # 从 pending 移到 completed
            for i, m in enumerate(queue["pending"]):
                if m.get("id") == msg_id:
                    m["completed_at"] = datetime.now().isoformat()
                    m["final_status"] = "max_retry_exceeded"
                    queue["completed"].append(m)
                    queue["pending"].pop(i)
                    break
            save_queue(queue)
            stats["max_retry_reached"] += 1
            stats["failed"] += 1
            continue
        
        # 构建 RETRY 消息
        retry_msg = build_retry_message(msg)
        
        # 发送消息
        if not session_key:
            stats["errors"].append(f"msg {msg_id}: no session_key, skipping")
            continue
        
        success, result = send_via_sessions_send(session_key, retry_msg)
        
        if success:
            # 发送成功，更新状态
            increment_retry(msg_id)
            # 更新发送状态
            queue = load_queue()
            for m in queue["pending"]:
                if m.get("id") == msg_id:
                    m["last_retry_at"] = datetime.now().isoformat()
                    m["last_retry_status"] = "sent_via_sessions_send"
                    break
            save_queue(queue)
            stats["sent"] += 1
        else:
            stats["failed"] += 1
            stats["errors"].append(f"msg {msg_id}: {result}")
            # 更新错误状态
            update_error(msg_id, result)
    
    return stats


if __name__ == "__main__":
    # 供 Cron 调用，直接输出统计
    result = process_queue()
    print(json.dumps(result, ensure_ascii=False, indent=2))
