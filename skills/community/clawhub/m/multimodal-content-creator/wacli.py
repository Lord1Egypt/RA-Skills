#!/usr/bin/env python3
"""WhatsApp CLI client for sending and receiving messages."""

import os
import sys
import json
from datetime import datetime

class WhatsAppClient:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser("~/.wacli/config.json")
        self.load_config()
    
    def load_config(self) -> None:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {"auth_token": None, "default_number": None}
    
    def save_config(self) -> None:
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def login(self, auth_token: str) -> None:
        """Authenticate with WhatsApp CLI service"""
        self.config["auth_token"] = auth_token
        self.save_config()
        print("Login successful")
    
    def set_default_number(self, number: str) -> None:
        """Set default WhatsApp number to use for outgoing messages"""
        self.config["default_number"] = number
        self.save_config()
        print(f"Default number set to {number}")
    
    def list_messages(self, limit: int = 20) -> list[dict]:
        """List recent incoming messages"""
        if not self.config["auth_token"]:
            print("Error: Not logged in. Use `wacli login <token>` first.")
            return []
        
        # Simulate API call (replace with actual wacli command)
        mock_messages = [
            {
                "id": "msg_123",
                "from": "+1234567890",
                "timestamp": datetime.now().isoformat(),
                "type": "audio",
                "content": "/workspace/sample_data/customer_request.mp3",
                "caption": "Hi! Can you create a logo for my new coffee shop?"
            },
            {
                "id": "msg_124",
                "from": "+0987654321",
                "timestamp": datetime.now().isoformat(),
                "type": "text",
                "content": "I need a illustration of a cat riding a skateboard for my t-shirt design"
            }
        ]
        
        for msg in mock_messages[:limit]:
            print(f"[{msg['timestamp']}] {msg['from']}:")
            print(f"  Type: {msg['type']}")
            if msg['type'] == 'text':
                print(f"  Content: {msg['content']}")
            else:
                print(f"  File: {msg['content']}")
                if msg.get('caption'):
                    print(f"  Caption: {msg['caption']}")
            print()
        
        return mock_messages
    
    def send_message(self, to: str, content: str, media_path: str | None = None) -> bool:
        """Send message to WhatsApp number"""
        if not self.config["auth_token"]:
            print("Error: Not logged in. Use `wacli login <token>` first.")
            return False
        
        if media_path:
            print(f"Sending media to {to}: {media_path}")
            print(f"Caption: {content}")
        else:
            print(f"Sending message to {to}: {content}")
        
        return True

def main():
    client = WhatsAppClient()
    
    if len(sys.argv) < 2:
        print("WhatsApp CLI (wacli)")
        print("Usage:")
        print("  wacli login <auth_token> - Authenticate with service")
        print("  wacli set-default <number> - Set default outgoing number")
        print("  wacli list [limit] - List recent messages")
        print("  wacli send <to> <message> [media_path] - Send message")
        return
    
    command = sys.argv[1]
    
    if command == "login":
        if len(sys.argv) != 3:
            print("Usage: wacli login <auth_token>")
            return
        client.login(sys.argv[2])
    elif command == "set-default":
        if len(sys.argv) != 3:
            print("Usage: wacli set-default <number>")
            return
        client.set_default_number(sys.argv[2])
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) == 3 else 20
        client.list_messages(limit)
    elif command == "send":
        if len(sys.argv) < 4:
            print("Usage: wacli send <to> <message> [media_path]")
            return
        to = sys.argv[2]
        message = sys.argv[3]
        media = sys.argv[4] if len(sys.argv) > 4 else None
        client.send_message(to, message, media)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()