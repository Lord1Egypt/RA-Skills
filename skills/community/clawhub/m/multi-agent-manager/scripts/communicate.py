#!/usr/bin/env python3
"""
Agent Orchestrator - Agent Communication
智能体间通信工具
"""

import json
import subprocess
import sys

def send_message(from_agent, to_agent, message):
    """发送消息给指定智能体"""
    try:
        # 使用 sessions_send 发送消息
        result = subprocess.run(
            ['openclaw', 'sessions', 'send', 
             '--agent', to_agent,
             '--message', message],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    if '--from' not in sys.argv or '--to' not in sys.argv or '--message' not in sys.argv:
        print("Usage: communicate.py --from <agent> --to <agent> --message <text>")
        sys.exit(1)
    
    from_idx = sys.argv.index('--from')
    to_idx = sys.argv.index('--to')
    msg_idx = sys.argv.index('--message')
    
    from_agent = sys.argv[from_idx + 1]
    to_agent = sys.argv[to_idx + 1]
    message = sys.argv[msg_idx + 1]
    
    print(f"Sending message from {from_agent} to {to_agent}...")
    success, output = send_message(from_agent, to_agent, message)
    
    if success:
        print("✓ Message sent successfully")
        print(output)
    else:
        print("✗ Failed to send message")
        print(output, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
