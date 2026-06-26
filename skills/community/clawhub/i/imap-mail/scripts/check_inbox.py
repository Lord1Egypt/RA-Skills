#!/usr/bin/env python3
"""
Check inbox via IMAP Mail API.

Usage:
    python check_inbox.py --inbox agent@example.com
    python check_inbox.py --inbox agent@example.com --folder Sent
    python check_inbox.py --inbox agent@example.com --unseen
    python check_inbox.py --inbox agent@example.com --message 42
    python check_inbox.py --inbox agent@example.com --message 42 --save-attachments /tmp/mail/
    python check_inbox.py --inbox agent@example.com --threads
    python check_inbox.py --inbox agent@example.com --folders
    python check_inbox.py --inbox agent@example.com --limit 20

Environment:
    IMAP_MAIL_API    (default: http://127.0.0.1:8025)
    IMAP_MAIL_INBOX  default inbox address
"""

import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime


API   = os.getenv("IMAP_MAIL_API",   "http://127.0.0.1:8025")
INBOX = os.getenv("IMAP_MAIL_INBOX", "")


def api_get(path):
    url = API.rstrip("/") + path
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url), timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to IMAP Mail API at {API}: {e}", file=sys.stderr)
        print("Is the API server running? Start with: python3 mail-api.py", file=sys.stderr)
        sys.exit(1)


def fmt_ts(ts):
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts


def print_msg(m):
    frm = m.get("from_") or []
    from_str = (frm[0].get("name") or frm[0].get("email", "Unknown")) if frm else "Unknown"
    folder = m.get("folder", "INBOX")
    attach = f"  📎 {len(m['attachments'])}" if m.get("attachments") else ""
    vip    = "  ⭐ VIP" if m.get("vip") else ""
    print(f"📧 uid:{m.get('uid','?')}  [{folder}]{attach}{vip}")
    print(f"   From:    {from_str}")
    print(f"   Subject: {m.get('subject', '(no subject)')}")
    print(f"   Time:    {fmt_ts(m.get('timestamp', ''))}")
    preview = (m.get("preview") or m.get("text") or "")[:120].replace("\n", " ")
    if preview:
        print(f"   Preview: {preview}")
    print()


def save_attachments(msg_data, save_dir):
    """Download and save all attachments for a message."""
    attachments = msg_data.get("attachments", [])
    if not attachments:
        print("   (no attachments to save)")
        return
    inbox_id = msg_data.get("inbox_id", "")
    uid      = msg_data.get("uid", "")
    folder   = urllib.parse.quote(msg_data.get("folder", "INBOX"))
    enc      = urllib.parse.quote(inbox_id, safe="@.")
    os.makedirs(save_dir, exist_ok=True)
    for i, att in enumerate(attachments):
        data = api_get(f"/inboxes/{enc}/messages/{uid}/attachments/{i}?folder={folder}")
        filename = data.get("filename", f"attachment-{i}")
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(data["data"]))
        print(f"   💾 Saved: {filepath} ({data['size']} bytes)")


def main():
    p = argparse.ArgumentParser(description="Check IMAP inbox via local API")
    p.add_argument("--inbox",            default=INBOX, help="Inbox email address")
    p.add_argument("--folder",           default="INBOX", help="IMAP folder (default: INBOX)")
    p.add_argument("--message",          help="UID of specific message to fetch")
    p.add_argument("--threads",          action="store_true", help="List threads")
    p.add_argument("--folders",          action="store_true", help="List all folders")
    p.add_argument("--unseen",           action="store_true", help="Show unread messages only")
    p.add_argument("--limit",            type=int, default=10, help="Max results (default: 10)")
    p.add_argument("--save-attachments", dest="save_attachments", metavar="DIR",
                   help="Save attachments to DIR (use with --message)")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc = urllib.parse.quote(args.inbox, safe="@.")

    if args.folders:
        data = api_get(f"/inboxes/{enc}/folders")
        folders = data.get("folders", [])
        if not folders:
            print("No folders found.")
            return
        print(f"📁 Folders ({len(folders)}):\n")
        for f in folders:
            flags = ", ".join(f.get("flags", []))
            print(f"  📁 {f['name']}" + (f"  [{flags}]" if flags else ""))
        return

    if args.message:
        m = api_get(f"/inboxes/{enc}/messages/{args.message}?folder={urllib.parse.quote(args.folder)}")
        print_msg(m)
        print("📝 Body:")
        print(m.get("text") or "(no text body)")
        if args.save_attachments:
            save_attachments(m, args.save_attachments)
        return

    if args.threads:
        data = api_get(f"/inboxes/{enc}/threads?limit={args.limit}&folder={urllib.parse.quote(args.folder)}")
        threads = data.get("threads", [])
        if not threads:
            print(f"📭 No threads in {args.folder}")
            return
        print(f"🧵 Threads in {args.folder} ({len(threads)}):\n")
        for t in threads:
            print(f"🧵 {t.get('thread_id', '')}")
            print(f"   Subject:      {t.get('subject', '(no subject)')}")
            print(f"   Participants: {', '.join(t.get('participants', []))}")
            print(f"   Messages:     {t.get('message_count', 0)}")
            print(f"   Last:         {fmt_ts(t.get('last_message_at', ''))}")
            print()
        return

    params = f"limit={args.limit}&folder={urllib.parse.quote(args.folder)}"
    if args.unseen:
        params += "&unseen=true"
    data = api_get(f"/inboxes/{enc}/messages?{params}")
    messages = data.get("messages", [])
    if not messages:
        label = "unread messages" if args.unseen else "messages"
        print(f"📭 No {label} in {args.folder}")
        return
    print(f"📧 Messages in {args.folder} ({len(messages)}):\n")
    for m in messages:
        print_msg(m)


if __name__ == "__main__":
    main()
