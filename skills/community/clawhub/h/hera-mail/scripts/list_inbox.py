#!/usr/bin/env python3
"""
HERA Mail - List Inbox

Usage: python3 list_inbox.py <agent_name>

Lists all emails in the agent's inbox with status (read/unread).
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def list_inbox(agent_name):
    """List all emails in agent's inbox."""
    
    base_dir = Path("/Users/zhaoruiwu/.openclaw/workspace/hera-agents")
    inbox_dir = base_dir / agent_name / "inbox"
    
    if not inbox_dir.exists():
        print(f"❌ Inbox not found for agent: {agent_name}")
        return
    
    # Get all mail files
    mail_files = sorted(inbox_dir.glob("*.md"))
    
    if not mail_files:
        print("📭 Inbox is empty")
        return
    
    print(f"📬 Inbox for {agent_name} ({len(mail_files)} messages)\n")
    print("-" * 60)
    
    for i, mail_file in enumerate(mail_files, 1):
        # Check if mail has been read (look for .read marker)
        read_marker = mail_file.with_suffix(".read")
        status = "✓" if read_marker.exists() else "○"
        status_text = "read" if read_marker.exists() else "unread"
        
        # Parse mail header
        try:
            content = mail_file.read_text()
            lines = content.split("\n")
            
            subject = "No Subject"
            sender = "Unknown"
            timestamp = "Unknown"
            
            for line in lines[:10]:  # Look in first 10 lines for headers
                if line.startswith("[SUBJECT:"):
                    subject = line.replace("[SUBJECT:", "").replace("]", "").strip()
                elif line.startswith("[FROM:"):
                    sender = line.replace("[FROM:", "").replace("]", "").strip()
                elif line.startswith("[TIMESTAMP:"):
                    timestamp = line.replace("[TIMESTAMP:", "").replace("]", "").strip()
            
            # Truncate long subjects
            if len(subject) > 50:
                subject = subject[:47] + "..."
            
            print(f"{i}. [{status}] {subject}")
            print(f"   From: {sender} | {timestamp}")
            print(f"   File: {mail_file.name}")
            print()
            
        except Exception as e:
            print(f"{i}. [{status}] Error reading: {mail_file.name}")
            print(f"   Error: {e}")
            print()
    
    print("-" * 60)
    print(f"Legend: [○] = unread, [✓] = read")
    print(f"\nTo read a message: python3 read_mail.py <agent_name> <mail_file_name>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 list_inbox.py <agent_name>")
        print("Example: python3 list_inbox.py group-leader")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    list_inbox(agent_name)
