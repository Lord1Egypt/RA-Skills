#!/usr/bin/env python3
"""处理队列中的消息 - Hermes 用这个轮询"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from communication_queue import CommunicationQueue

def process_pending_messages():
    queue = CommunicationQueue()
    # 获取发给 hermes 的 pending 消息
    messages = queue.get_messages("hermes", status="pending")
    
    if not messages:
        print(f"[{datetime.now().isoformat()}] 无待处理消息")
        return
    
    for msg in messages:
        print(f"处理消息: {msg['id']} | 内容: {msg['content'][:50]}...")
        
        # Hermes 读取消息后，可以在这里回复
        # 回复写入队列
        reply = queue.send_message(
            sender="hermes",
            receiver="workbuddy",
            content=f"收到 WorkBuddy 的消息: {msg['content'][:30]}...，我来处理。",
            msg_type="response",
            priority="normal"
        )
        print(f"已回复: {reply}")
        
        # 标记原消息完成
        queue.mark_as_processed(msg['id'], status="completed")
        print(f"已标记完成: {msg['id']}")

from datetime import datetime
if __name__ == "__main__":
    process_pending_messages()
