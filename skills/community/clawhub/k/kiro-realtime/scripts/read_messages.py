#!/usr/bin/env python3
"""Check and read messages for a specific Kiro"""

import json
import os
import sys
from datetime import datetime

CHAT_FILE = os.path.expanduser("~/.openclaw/workspace/memory/kiro-realtime.json")

def read_messages(my_name, mark_read=True):
    if not os.path.exists(CHAT_FILE):
        print("📭 No messages yet")
        return []
    
    with open(CHAT_FILE, "r") as f:
        chat = json.load(f)
    
    # Update last check time
    chat["lastCheck"] = datetime.now().isoformat()
    
    # Filter unread messages for me
    my_messages = []
    for msg in chat["messages"]:
        if msg["to"] == my_name and not msg["read"]:
            my_messages.append(msg)
            if mark_read:
                msg["read"] = True
    
    # Save read status
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    return my_messages

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_messages.py <my_name>")
        print("Example: read_messages.py 'Laptop Kiro'")
        sys.exit(1)
    
    my_name = sys.argv[1]
    messages = read_messages(my_name)
    
    if not messages:
        print("📭 No new messages")
    else:
        print(f"📬 {len(messages)} new message(s):")
        for msg in messages:
            ts = msg["timestamp"][:16].replace("T", " ")
            print(f"  [{ts}] {msg['from']}: {msg['message']}")
