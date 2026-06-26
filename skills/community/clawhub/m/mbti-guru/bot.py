#!/usr/bin/env python3
"""
MBTI Guru - OpenClaw Telegram Bot Entry Point
与OpenClaw集成的Telegram bot处理程序
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.telegram_handler import (
    handle_message,
    handle_callback,
    handle_start,
    handle_resume,
    handle_history,
    handle_status,
    handle_cancel,
    VERSIONS
)

def process_update(update: dict) -> dict:
    """
    处理Telegram更新
    
    Args:
        update: Telegram webhook更新
    
    Returns:
        回复消息
    """
    # 提取chat_id和消息
    message = update.get("message", {})
    callback = update.get("callback_query", {})
    
    chat_id = None
    text = ""
    
    if message:
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
    elif callback:
        chat_id = callback.get("message", {}).get("chat", {}).get("id")
        data = callback.get("data", "")
        return handle_callback(chat_id, data)
    
    if not chat_id:
        return {"action": "send", "message": "Error: No chat_id"}
    
    return handle_message(chat_id, text)


# CLI测试模式
if __name__ == "__main__":
    print("=" * 50)
    print("MBTI Guru - CLI Test Mode")
    print("=" * 50)
    
    chat_id = 123456  # 测试用chat_id
    
    # 模拟开始
    result = handle_start(chat_id)
    print(result["message"])
    print()
    
    # 模拟选择版本
    print("--- Selecting version 2 ---")
    result = handle_message(chat_id, "2")
    print(result["message"][:200] + "...")
    print()
    
    # 模拟回答几题
    print("--- Answering questions ---")
    for i in range(5):
        answer = "A" if i % 2 == 0 else "B"
        result = handle_message(chat_id, answer)
        if result["action"] == "complete":
            print("Test completed!")
            print(result["message"])
            break
        elif result.get("feedback"):
            print(f"Q{i+1}: Answer {answer} - {result.get('feedback', '')[:50]}...")
        else:
            print(f"Q{i+1}: Answer {answer} - OK")
    
    # 测试历史
    print("\n--- Testing history ---")
    result = handle_history(chat_id)
    print(result["message"][:200] + "...")
    
    # 测试状态
    print("\n--- Testing status ---")
    result = handle_status(chat_id)
    print(result["message"])
