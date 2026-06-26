#!/usr/bin/env python3
"""Send message to agent chat queue."""
import json
import os
import sys
from datetime import datetime

def main():
    queue_file = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/shared/agent-chat.json")
    sender = os.environ.get("SENDER", "anonymous")
    receiver = os.environ.get("RECEIVER", "broadcast")
    message = os.environ.get("MESSAGE", "")
    
    if not message:
        print("Usage: SENDER=name RECEIVER=target MESSAGE='text' send_message.py <queue-file>")
        sys.exit(1)
    
    # Create directory if needed
    os.makedirs(os.path.dirname(queue_file), exist_ok=True)
    
    # Load or init queue
    if os.path.exists(queue_file):
        with open(queue_file, 'r') as f:
            data = json.load(f)
    else:
        data = {"messages": []}
    
    # Generate ID
    msg_id = int(datetime.now().timestamp() * 1000)
    
    # Add message
    data["messages"].append({
        "id": msg_id,
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Save
    with open(queue_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Message sent: [{sender} -> {receiver}] {message}")

if __name__ == "__main__":
    main()
