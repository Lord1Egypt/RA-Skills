#!/usr/bin/env python3
"""Send a message to another Kiro via shared JSON file"""

import json
import os
import sys
from datetime import datetime

CHAT_FILE = os.path.expanduser("~/.openclaw/workspace/memory/kiro-realtime.json")

def send_message(from_name, to_name, message):
    # Load or create chat file
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            chat = json.load(f)
    else:
        chat = {"messages": [], "lastCheck": datetime.now().isoformat()}
    
    # Add new message
    msg_id = len(chat["messages"]) + 1
    chat["messages"].append({
        "id": msg_id,
        "from": from_name,
        "to": to_name,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "read": False
    })
    
    # Save
    os.makedirs(os.path.dirname(CHAT_FILE), exist_ok=True)
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    print(f"✅ Message sent: #{msg_id} from {from_name} to {to_name}")
    return msg_id

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: send_message.py <from> <to> <message>")
        print("Example: send_message.py 'VPS Kiro' 'Laptop Kiro' 'Selam!'")
        sys.exit(1)
    
    from_name = sys.argv[1]
    to_name = sys.argv[2]
    message = " ".join(sys.argv[3:])
    
    send_message(from_name, to_name, message)
