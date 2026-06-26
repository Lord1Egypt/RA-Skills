#!/usr/bin/env python3
"""
iMessage Sender - Send images from Mac to phone via iMessage
"""

import os
import sys
import subprocess
from pathlib import Path

CONFIG_FILE = Path.home() / ".openclaw" / "workspace" / "imessage-sender-config.json"

def load_config():
    """Load configuration"""
    if CONFIG_FILE.exists():
        import json
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration"""
    import json
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def send_imessage(recipient, image_path):
    """Send iMessage"""
    
    # Ensure absolute path
    abs_path = os.path.abspath(image_path)
    
    # Copy to dedicated folder (avoid path issues)
    send_folder = Path.home() / "Pictures" / "openclaw-send"
    send_folder.mkdir(parents=True, exist_ok=True)
    
    # Generate new filename
    filename = f"send_{Path(abs_path).name}"
    send_path = send_folder / filename
    
    # Copy file
    import shutil
    shutil.copy2(abs_path, send_path)
    
    # Phone number format: +86XXXXXXXXXX
    formatted_recipient = recipient
    if not recipient.startswith('+'):
        if len(recipient) == 11:
            formatted_recipient = '+86' + recipient
    
    # Use POSIX file path format
    script = f'''
    tell application "Messages"
        activate
        send POSIX file "{send_path}" to participant "{formatted_recipient}"
    end tell
    '''
    
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Image sent to {recipient}")
        return True
    else:
        print(f"❌ Failed to send: {result.stderr}")
        return False

def config_set(recipient):
    """Set default recipient"""
    config = load_config()
    config['default_recipient'] = recipient
    save_config(config)
    print(f"✅ Default recipient set: {recipient}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  send.py send <recipient> <image_path>  - Send image")
        print("  send.py config set <recipient>         - Set default recipient")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send":
        if len(sys.argv) < 4:
            print("Please provide recipient and image path")
            sys.exit(1)
        recipient = sys.argv[2]
        image_path = sys.argv[3]
        send_imessage(recipient, image_path)
    
    elif cmd == "config":
        if len(sys.argv) < 4 or sys.argv[2] != "set":
            print("Usage: send.py config set <recipient>")
            sys.exit(1)
        config_set(sys.argv[3])
    
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
