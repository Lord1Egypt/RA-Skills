#!/usr/bin/env python3
"""
Search emails via IMAP Mail API.

Usage:
    python search.py --inbox agent@example.com --q "invoice"
    python search.py --inbox agent@example.com --from "alice@example.com"
    python search.py --inbox agent@example.com --subject "meeting" --since 2026-01-01
    python search.py --inbox agent@example.com --unseen --folder INBOX
    python search.py --inbox agent@example.com --has-attachments --since 2026-03-01
    python search.py --inbox agent@example.com --body "password reset" --limit 5
    python search.py --inbox agent@example.com --vip
    python search.py --inbox agent@example.com --has-attachments --save-attachments /tmp/mail/

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
        resp = urllib.request.urlopen(urllib.request.Request(url), timeout=15)
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
    attach = f"  📎 {len(m['attachments'])}" if m.get("attachments") else ""
    vip    = "  ⭐ VIP" if m.get("vip") else ""
    print(f"📧 uid:{m.get('uid','?')}  [{m.get('folder','INBOX')}]{attach}{vip}")
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
        return
    inbox_id = msg_data.get("inbox_id", "")
    uid      = msg_data.get("uid", "")
    folder   = urllib.parse.quote(msg_data.get("folder", "INBOX"))
    enc      = urllib.parse.quote(inbox_id, safe="@.")
    os.makedirs(save_dir, exist_ok=True)
    for i, att in enumerate(attachments):
        data     = api_get(f"/inboxes/{enc}/messages/{uid}/attachments/{i}?folder={folder}")
        filename = data.get("filename", f"attachment-{i}")
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(data["data"]))
        print(f"   💾 Saved: {filepath} ({data['size']} bytes)")


def main():
    p = argparse.ArgumentParser(description="Search emails via IMAP Mail API")
    p.add_argument("--inbox",            default=INBOX, help="Inbox email address")
    p.add_argument("--folder",           default="INBOX", help="IMAP folder to search (default: INBOX)")
    p.add_argument("--q",                default="",  help="Search subject + body (shorthand)")
    p.add_argument("--from",             dest="from_", default="", help="Filter by sender")
    p.add_argument("--to",               default="",  help="Filter by recipient")
    p.add_argument("--subject",          default="",  help="Filter by subject")
    p.add_argument("--body",             default="",  help="Filter by body text")
    p.add_argument("--since",            default="",  help="Messages since date (YYYY-MM-DD)")
    p.add_argument("--before",           default="",  help="Messages before date (YYYY-MM-DD)")
    p.add_argument("--unseen",           action="store_true", help="Unread messages only")
    p.add_argument("--seen",             action="store_true", help="Read messages only")
    p.add_argument("--has-attachments",  action="store_true", dest="has_attachments",
                   help="Only messages with attachments")
    p.add_argument("--vip",              action="store_true", help="Only messages from VIP senders")
    p.add_argument("--flagged",          action="store_true", help="Only flagged/starred messages")
    p.add_argument("--unflagged",        action="store_true", help="Only unflagged messages")
    p.add_argument("--limit",            type=int, default=10, help="Max results (default: 10)")
    p.add_argument("--save-attachments", dest="save_attachments", metavar="DIR",
                   help="Save all attachments from results to DIR")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc = urllib.parse.quote(args.inbox, safe="@.")

    params = urllib.parse.urlencode({k: v for k, v in {
        "folder":          args.folder,
        "q":               args.q,
        "from":            args.from_,
        "to":              args.to,
        "subject":         args.subject,
        "body":            args.body,
        "since":           args.since,
        "before":          args.before,
        "unseen":          "true" if args.unseen else "",
        "seen":            "true" if args.seen   else "",
        "has_attachments": "true" if args.has_attachments else "",
        "vip_only":        "true" if args.vip      else "",
        "flagged":         "true" if args.flagged  else "",
        "unflagged":       "true" if args.unflagged else "",
        "limit":           args.limit,
    }.items() if v})

    data     = api_get(f"/inboxes/{enc}/search?{params}")
    messages = data.get("messages", [])
    criteria = data.get("criteria", "")

    if not messages:
        print(f"🔍 No results  (criteria: {criteria})")
        return

    print(f"🔍 Found {len(messages)} message(s)  (criteria: {criteria})\n")
    for m in messages:
        print_msg(m)
        if args.save_attachments:
            save_attachments(m, args.save_attachments)


if __name__ == "__main__":
    main()
