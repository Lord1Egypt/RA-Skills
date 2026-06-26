#!/usr/bin/env python3
"""
HERA Mail - Send Mail

Usage: python3 send_mail.py <from_agent> <to_agent> <subject> [attachment_paths...]

Sends an email to another agent with optional file attachments.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def send_mail(from_agent, to_agent, subject, body="", attachments=None):
    """Send an email to another agent."""
    
    base_dir = Path("/Users/zhaoruiwu/.openclaw/workspace/hera-agents")
    
    # Validate agents exist
    from_dir = base_dir / from_agent
    to_dir = base_dir / to_agent
    
    if not from_dir.exists():
        print(f"❌ Sender agent not found: {from_agent}")
        return False
    
    if not to_dir.exists():
        print(f"❌ Recipient agent not found: {to_agent}")
        return False
    
    # Create inbox if needed
    inbox_dir = to_dir / "inbox"
    inbox_dir.mkdir(exist_ok=True)
    
    # Generate mail ID
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    mail_id = f"{timestamp}-{from_agent}-{to_agent}"
    mail_file = inbox_dir / f"{mail_id}.md"
    
    # Create mail content
    mail_content = f"""[FROM: {from_agent}]
[TO: {to_agent}]
[TIMESTAMP: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
[MAIL-ID: {mail_id}]
[SUBJECT: {subject}]
[STATUS: unread]

---

{body}

---
[END]
"""
    
    # Write mail
    mail_file.write_text(mail_content)
    
    # Handle attachments
    if attachments:
        attach_dir = inbox_dir / "attachments" / mail_id
        attach_dir.mkdir(parents=True, exist_ok=True)
        
        for att_path in attachments:
            att_path = Path(att_path)
            if att_path.exists():
                dest = attach_dir / att_path.name
                shutil.copy2(att_path, dest)
                print(f"📎 Attached: {att_path.name}")
            else:
                print(f"⚠️  Attachment not found: {att_path}")
    
    # Create sent copy
    outbox_dir = from_dir / "outbox"
    outbox_dir.mkdir(exist_ok=True)
    sent_copy = outbox_dir / f"{mail_id}.md"
    sent_copy.write_text(mail_content)
    
    print(f"\n✅ Mail sent successfully!")
    print(f"   From: {from_agent}")
    print(f"   To: {to_agent}")
    print(f"   Subject: {subject}")
    print(f"   Mail ID: {mail_id}")
    print(f"   Saved to: {mail_file}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_mail.py <from_agent> <to_agent> <subject> [attachment_paths...]")
        print("Example: python3 send_mail.py group-leader rough-reader \"Analyze this paper\" paper.pdf")
        sys.exit(1)
    
    from_agent = sys.argv[1]
    to_agent = sys.argv[2]
    subject = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) > 4 else []
    
    # For body, read from stdin or use default
    import io
    body = sys.stdin.read() if not sys.stdin.isatty() else "No body content."
    
    send_mail(from_agent, to_agent, subject, body, attachments)
