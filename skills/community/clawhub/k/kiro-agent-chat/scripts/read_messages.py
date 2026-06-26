#!/usr/bin/env python3
"""Read messages for a specific agent."""
import json
import os
import sys

def main():
    queue_file = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/shared/agent-chat.json")
    my_name = os.environ.get("MY_NAME", "")
    
    if not my_name:
        print("Usage: MY_NAME=agent-name read_messages.py <queue-file>")
        sys.exit(1)
    
    if not os.path.exists(queue_file):
        print("No messages yet.")
        sys.exit(0)
    
    with open(queue_file, 'r') as f:
        data = json.load(f)
    
    # Filter messages for this agent
    messages = [m for m in data.get("messages", []) 
                if m.get("receiver") == my_name or m.get("receiver") == "broadcast"]
    
    if not messages:
        print("No messages for you.")
    else:
        for m in messages:
            print(f"[{m['id']}] {m['sender']} -> {m['receiver']}: {m['message']} ({m['timestamp']})")

if __name__ == "__main__":
    main()
