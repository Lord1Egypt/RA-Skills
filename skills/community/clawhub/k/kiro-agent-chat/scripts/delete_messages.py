#!/usr/bin/env python3
"""Delete processed messages by ID."""
import json
import os
import sys

def main():
    queue_file = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/shared/agent-chat.json")
    ids_str = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if not ids_str:
        print("Usage: delete_messages.py <queue-file> <id1,id2,...>")
        sys.exit(1)
    
    if not os.path.exists(queue_file):
        print("Queue file not found.")
        sys.exit(1)
    
    # Parse IDs
    ids_to_delete = [int(x) for x in ids_str.split(',')]
    
    with open(queue_file, 'r') as f:
        data = json.load(f)
    
    # Filter out deleted messages
    original_count = len(data.get("messages", []))
    data["messages"] = [m for m in data.get("messages", []) if m.get("id") not in ids_to_delete]
    deleted_count = original_count - len(data["messages"])
    
    with open(queue_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Deleted {deleted_count} message(s): {ids_str}")

if __name__ == "__main__":
    main()
