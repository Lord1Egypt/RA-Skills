#!/usr/bin/env python3
"""
Sort inbox messages into Personal and Forwarded folders.

- Personal  : inbox address is directly in To: or Cc:
- Forwarded : subject starts with Fwd/FW, or X-Forwarded/Resent headers present

Usage:
    # Preview what would be moved (no changes made)
    python sort_inbox.py --inbox agent@example.com --dry-run

    # Sort all messages in INBOX
    python sort_inbox.py --inbox agent@example.com

    # Sort only unread messages
    python sort_inbox.py --inbox agent@example.com --unseen

    # Use custom folder names
    python sort_inbox.py --inbox agent@example.com \\
        --personal-folder MyInbox --forwarded-folder Forwards

    # Sort a different source folder
    python sort_inbox.py --inbox agent@example.com --folder AllMail

Environment:
    IMAP_MAIL_API    (default: http://127.0.0.1:8025)
    IMAP_MAIL_INBOX  default inbox address
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API   = os.getenv("IMAP_MAIL_API",   "http://127.0.0.1:8025")
INBOX = os.getenv("IMAP_MAIL_INBOX", "")


def api_post(path, params=None):
    url = API.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=b"", method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to IMAP Mail API at {API}: {e}", file=sys.stderr)
        print("Is the API server running? Start with: python3 mail-api.py", file=sys.stderr)
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Sort inbox into Personal / Forwarded folders")
    p.add_argument("--inbox",            default=INBOX,       help="Inbox email address")
    p.add_argument("--folder",           default="INBOX",     help="Source folder (default: INBOX)")
    p.add_argument("--personal-folder",  default="Personal",  dest="personal_folder",
                   help="Destination for personal mail (default: Personal)")
    p.add_argument("--forwarded-folder", default="Forwarded", dest="forwarded_folder",
                   help="Destination for forwarded mail (default: Forwarded)")
    p.add_argument("--unseen",           action="store_true", help="Only sort unread messages")
    p.add_argument("--dry-run",          action="store_true", dest="dry_run",
                   help="Preview moves without making any changes")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc    = urllib.parse.quote(args.inbox, safe="@.")
    params = {
        "folder":           args.folder,
        "personal_folder":  args.personal_folder,
        "forwarded_folder": args.forwarded_folder,
        "unseen_only":      "true" if args.unseen else "false",
        "dry_run":          "true" if args.dry_run else "false",
    }

    result = api_post(f"/inboxes/{enc}/sort", params)

    if args.dry_run:
        print(f"🔍 Dry run — no messages were moved\n")
    else:
        print(f"✅ Sorted {result['total_moved']} message(s)\n")

    personal  = result.get("moved_personal",  [])
    forwarded = result.get("moved_forwarded", [])
    skipped   = result.get("skipped",         [])

    if personal:
        print(f"📥 → {result['personal_folder']} ({len(personal)} message(s)):")
        for uid in personal:
            print(f"   uid:{uid}")

    if forwarded:
        print(f"📨 → {result['forwarded_folder']} ({len(forwarded)} message(s)):")
        for uid in forwarded:
            print(f"   uid:{uid}")

    if skipped:
        print(f"⏭️  Skipped (kept in {result['folder']}): {len(skipped)} message(s)")

    if not personal and not forwarded and not skipped:
        print(f"📭 No messages to sort in {result['folder']}")


if __name__ == "__main__":
    main()
