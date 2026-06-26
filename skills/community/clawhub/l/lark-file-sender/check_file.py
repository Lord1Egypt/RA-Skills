#!/usr/bin/env python3
"""
Feishu File Sender Helper Script
Checks file existence, size, and provides formatted output for sending
"""

import os
import sys

def check_file(file_path):
    """Check if file exists and get info"""
    if not os.path.exists(file_path):
        return None, f"File not found: {file_path}"
    
    if not os.path.isfile(file_path):
        return None, f"Path is not a file: {file_path}"
    
    size = os.path.getsize(file_path)
    size_mb = size / (1024 * 1024)
    
    # Feishu limits (adjust based on your plan)
    if size_mb > 1000:
        return None, f"File too large ({size_mb:.1f}MB). Max: 1000MB"
    
    return {
        "path": os.path.abspath(file_path),
        "size": size,
        "size_mb": size_mb,
        "name": os.path.basename(file_path)
    }, None

def format_send_command(file_info, message=""):
    """Format the message send command"""
    cmd = f'message action=send filePath="{file_info["path"]}"'
    if message:
        cmd += f' message="{message}"'
    return cmd

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_file.py <file_path> [optional_message]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else ""
    
    info, error = check_file(file_path)
    
    if error:
        print(f"❌ Error: {error}")
        sys.exit(1)
    
    print(f"✅ File OK: {info['name']}")
    print(f"   Size: {info['size_mb']:.2f} MB")
    print(f"   Path: {info['path']}")
    print()
    print("Send command:")
    print(format_send_command(info, message))
