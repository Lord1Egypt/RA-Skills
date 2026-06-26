---
name: kiro-realtime
description: Real-time chat between Kiro instances via shared JSON file with polling. Use when: (1) Two or more Kiros need to chat in real-time, (2) One Kiro sends a message and expects quick response, (3) Coordinating tasks between instances.
---

# Kiro Realtime Chat

## Overview

This skill enables near real-time communication between multiple Kiro instances using a shared JSON file with polling. Each message includes timestamp, sender, and content.

## File Location

```
memory/kiro-realtime.json
```

## JSON Structure

```json
{
  "messages": [
    {
      "id": 1,
      "from": "VPS Kiro",
      "to": "Laptop Kiro",
      "message": "Selam!",
      "timestamp": "2026-03-05T22:58:00Z",
      "read": false
    }
  ],
  "lastCheck": "2026-03-05T22:58:00Z"
}
```

## Usage

### Sending a Message

```python
import json
import os
from datetime import datetime

CHAT_FILE = "memory/kiro-realtime.json"

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
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    return msg_id
```

### Checking for New Messages

```python
def check_messages(my_name, since_timestamp=None):
    if not os.path.exists(CHAT_FILE):
        return []
    
    with open(CHAT_FILE, "r") as f:
        chat = json.load(f)
    
    # Update last check time
    chat["lastCheck"] = datetime.now().isoformat()
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    # Filter messages my_messages = []
 for me
       for msg in chat["messages"]:
        if msg["to"] == my_name and not msg["read"]:
            my_messages.append(msg)
            msg["read"] = True
    
    # Save read status
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    return my_messages
```

### Polling Loop (for near real-time)

```python
import time

def poll_messages(my_name, interval=5):
    """Poll for new messages every N seconds"""
    while True:
        msgs = check_messages(my_name)
        for msg in msgs:
            print(f"{msg['from']}: {msg['message']}")
            # Process and respond here
        time.sleep(interval)
```

## Recommended Polling Interval

- **Fast response needed:** 2-3 seconds
- **Normal:** 5-10 seconds
- **Low bandwidth:** 30-60 seconds

## Tips

- Mark messages as "read" after processing
- Use timestamps to avoid duplicate processing
- For better real-time, consider MCP server or WebSocket
- Keep messages under 1000 characters
