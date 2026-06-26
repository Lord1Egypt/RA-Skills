#!/usr/bin/env python3
"""Hermes 通信 CLI 工具"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from communication_queue import CommunicationQueue

def send_to_hermes(content, msg_type="message", priority="normal"):
    queue = CommunicationQueue()
    msg_id = queue.send_message(sender="workbuddy", receiver="hermes",
                                 content=content, msg_type=msg_type, priority=priority)
    print(f"已发送消息到 Hermes: {msg_id}")
    return msg_id

def receive_from_hermes():
    queue = CommunicationQueue()
    messages = queue.get_messages("workbuddy", status="pending")
    if not messages:
        print("没有来自 Hermes 的新消息")
    for msg in messages:
        print(f"\n=== 来自 {msg['sender']} ===")
        print(f"类型: {msg['type']} | 优先级: {msg['priority']}")
        print(f"内容: {msg['content']}")
        queue.mark_as_processed(msg['id'], status="completed")
    return messages

def main():
    parser = argparse.ArgumentParser(description='Hermes 通信工具')
    parser.add_argument('action', choices=['send', 'receive'], help='send 或 receive')
    parser.add_argument('--content', '-c', help='消息内容（send 时用）')
    parser.add_argument('--type', '-t', default='message', help='消息类型')
    parser.add_argument('--priority', '-p', default='normal', help='优先级')
    args = parser.parse_args()

    if args.action == 'send':
        if not args.content:
            print("错误: send 需要 --content 参数")
            sys.exit(1)
        send_to_hermes(args.content, args.type, args.priority)
    else:
        receive_from_hermes()

if __name__ == "__main__":
    main()
