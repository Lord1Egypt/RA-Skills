#!/usr/bin/env python3
"""
HERA Mail - Read Mail

Usage: python3 read_mail.py <agent_name> <mail_file_name>

Reads a specific email and marks it as read.
"""

import os
import sys
from pathlib import Path

def read_mail(agent_name, mail_file_name):
    """Read a specific email and mark as read."""
    
    base_dir = Path("/Users/zhaoruiwu/.openclaw/workspace/hera-agents")
    inbox_dir = base_dir / agent_name / "inbox"
    
    mail_file = inbox_dir / mail_file_name
    
    if not mail_file.exists():
        print(f"❌ Mail not found: {mail_file_name}")
        print(f"   Check inbox with: python3 list_inbox.py {agent_name}")
        return
    
    # Read and display content
    content = mail_file.read_text()
    
    print("\n" + "=" * 60)
    print("📖 MESSAGE CONTENT")
    print("=" * 60 + "\n")
    print(content)
    print("\n" + "=" * 60)
    
    # Mark as read
    read_marker = mail_file.with_suffix(".read")
    read_marker.touch()
    print(f"✓ Marked as read: {mail_file_name}")
    
    # Check for attachments
    attach_dir = inbox_dir / "attachments" / mail_file_name.replace(".md", "")
    if attach_dir.exists():
        attachments = list(attach_dir.glob("*"))
        if attachments:
            print(f"\n📎 Attachments ({len(attachments)}):")
            for att in attachments:
                print(f"   - {att.name} ({att.stat().st_size} bytes)")
                print(f"     Path: {att}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 read_mail.py <agent_name> <mail_file_name>")
        print("Example: python3 read_mail.py group-leader 2026-03-29-001.md")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    mail_file_name = sys.argv[2]
    read_mail(agent_name, mail_file_name)
