#!/usr/bin/env python3
"""
MD Viewer Link Helper - Generate LAN-accessible link for markdown files

Usage:
    python3 md-link.py <path/to/file.md> --password PASSWORD

Example:
    python3 md-link.py /Users/name/project/README.md --password abc123
"""

import argparse
import socket
import sys
from pathlib import Path
from urllib.parse import quote

DEFAULT_PORT = 8765


def get_lan_ip():
    """Get LAN IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(description="Generate LAN link for markdown files")
    parser.add_argument("file_path", help="Path to .md file")
    parser.add_argument("--password", required=True, help="Server password (required)")
    args = parser.parse_args()
    
    file_path = Path(args.file_path).resolve()
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    
    if not file_path.suffix.lower() == '.md':
        print(f"❌ Error: Only .md files allowed: {file_path}")
        sys.exit(1)
    
    lan_ip = get_lan_ip()
    encoded_path = quote(str(file_path))
    
    link = f"http://{lan_ip}:{DEFAULT_PORT}/view?path={encoded_path}&token={quote(args.password)}"
    
    print(f"\n📄 Markdown Viewer Link:")
    print(f"   {link}")
    print()
    print(f"📁 File: {file_path.name}")
    print(f"🌐 LAN IP: {lan_ip}")
    print(f"🔐 Password protected")
    print()
    print("💡 Open from any device on the same WiFi network")


if __name__ == "__main__":
    main()