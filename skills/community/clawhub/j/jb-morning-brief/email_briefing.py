#!/usr/bin/env python3
"""
Email Briefing — JB's Claw
Reads Gmail via IMAP, summarizes inbox in 3 bullets.
"""
import imaplib, email as emaillib, email.message, ssl, sys, os
from datetime import datetime, timedelta, date

# Credentials from environment
EMAIL = os.environ.get("GMAIL_EMAIL", "")  # Set in ~/.openclaw/.env
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

if not APP_PASSWORD:
    print("ERROR: GMAIL_APP_PASSWORD env var not set")
    sys.exit(1)

# Connect
ctx = ssl.create_default_context()
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=ctx)
mail.login(EMAIL, APP_PASSWORD)
mail.select("INBOX")

# Search unseen emails from last 24 hours
yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
status, messages = mail.search(None, f'SINCE "{yesterday}" UNSEEN')
mail_ids = messages[0].split()
print(f"Emails found: {len(mail_ids)}")

urgent, medium, can_wait = [], [], []

for uid in mail_ids[-20:]:  # last 20
    status, msg_data = mail.fetch(uid, "(RFC822)")
    msg = emaillib.message_from_bytes(msg_data[0][1])
    subject = msg.get("Subject", "(no subject)")
    sender = msg.get("From", "")
    sender_clean = sender.split("@")[0].replace("<", "").replace(">", "") if sender else "unknown"
    try:
        name, sender_addr = email.utils.parseaddr(sender)
        sender_clean = sender_addr.split("@")[0] if sender_addr else sender_clean
    except Exception:
        pass
    date_str = msg.get("Date", "")
    
    # Simple triage: sender + subject keywords
    lower_subj = subject.lower()
    if any(k in lower_subj for k in ["urgent", "asap", "critical", "sparkchange", "urgent:", "important"]):
        urgent.append(f"• {subject} [{sender_clean}]")
    elif any(k in lower_subj for k in ["meeting", "calendar", "invite", "schedule", "request"]):
        medium.append(f"• {subject} [{sender_clean}]")
    else:
        can_wait.append(f"• {subject[:60]}")

print("\\n=== JB's Email Briefing ===")
if urgent:
    print(f"\\n🔴 Urgent ({len(urgent)}):")
    for u in urgent: print(u)
if medium:
    print(f"\\n🟡 Meetings/Requests ({len(medium)}):")
    for m in medium: print(m)
if can_wait:
    print(f"\\n🟢 Can Wait ({len(can_wait)}):")
    for c in can_wait[:5]: print(c)  # top 5
    if len(can_wait) > 5: print(f"  ...and {len(can_wait)-5} more")

mail.logout()
