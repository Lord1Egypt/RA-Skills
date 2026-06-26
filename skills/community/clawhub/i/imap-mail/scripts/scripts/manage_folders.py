#!/usr/bin/env python3
"""
Manage IMAP folders via IMAP Mail API.

Usage:
    python manage_folders.py --inbox agent@example.com --list
    python manage_folders.py --inbox agent@example.com --create Archive
    python manage_folders.py --inbox agent@example.com --delete OldFolder
    python manage_folders.py --inbox agent@example.com --move 42 --to Archive
    python manage_folders.py --inbox agent@example.com --move 42 --to Archive --from-folder Junk
    python manage_folders.py --inbox agent@example.com --delete-msg 42 --from-folder INBOX
    python manage_folders.py --inbox agent@example.com --mark-seen
    python manage_folders.py --inbox agent@example.com --mark-seen --from-folder Junk
    python manage_folders.py --inbox agent@example.com --mark-seen-uid 42
    python manage_folders.py --inbox agent@example.com --flag-uid 42 55 73
    python manage_folders.py --inbox agent@example.com --flag-from "craig@example.com"
    python manage_folders.py --inbox agent@example.com --unflag-uid 42

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


def api_post(path, payload):
    url  = API.rstrip("/") + path
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def api_delete(path):
    url = API.rstrip("/") + path
    req = urllib.request.Request(url, method="DELETE")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Manage IMAP folders via local API")
    p.add_argument("--inbox",       default=INBOX, help="Inbox email address")
    p.add_argument("--list",        action="store_true", help="List all folders")
    p.add_argument("--create",      metavar="NAME",      help="Create a folder")
    p.add_argument("--delete",      metavar="NAME",      help="Delete a folder")
    p.add_argument("--move",        metavar="UID",       help="Move a message (provide UID)")
    p.add_argument("--to",          metavar="FOLDER",    help="Destination folder for --move")
    p.add_argument("--from-folder", metavar="FOLDER",    default="INBOX",
                   help="Source folder for --move or --delete-msg (default: INBOX)")
    p.add_argument("--delete-msg",    metavar="UID",       help="Delete a message by UID")
    p.add_argument("--mark-seen",     action="store_true", help="Mark all messages in folder as read")
    p.add_argument("--mark-seen-uid", metavar="UID", nargs="+", help="Mark specific message(s) as read (one or more UIDs)")
    p.add_argument("--flag-uid",      metavar="UID", nargs="+", help="Flag (star) specific message(s) as important")
    p.add_argument("--unflag-uid",    metavar="UID", nargs="+", help="Remove flag from specific message(s)")
    p.add_argument("--flag-from",     metavar="EMAIL",          help="Flag all messages from a sender address")
    p.add_argument("--unflag-from",   metavar="EMAIL",          help="Remove flag from all messages from a sender")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc = urllib.parse.quote(args.inbox, safe="@.")

    if args.list:
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

    if args.create:
        result = api_post(f"/inboxes/{enc}/folders", {"name": args.create})
        print(f"✅ Folder '{result['name']}' created.")
        return

    if args.delete:
        folder_enc = urllib.parse.quote(args.delete, safe="")
        result = api_delete(f"/inboxes/{enc}/folders/{folder_enc}")
        print(f"🗑️  Folder '{result['name']}' deleted.")
        return

    if args.move:
        if not args.to:
            print("Error: --move requires --to <destination folder>", file=sys.stderr)
            sys.exit(1)
        src_enc = urllib.parse.quote(args.from_folder)
        result  = api_post(
            f"/inboxes/{enc}/messages/{args.move}/move?folder={src_enc}",
            {"destination": args.to},
        )
        print(f"✅ Message uid:{result['uid']} moved to '{result['moved_to']}'.")
        return

    if args.delete_msg:
        src_enc = urllib.parse.quote(args.from_folder)
        result  = api_delete(
            f"/inboxes/{enc}/messages/{args.delete_msg}?folder={src_enc}"
        )
        print(f"🗑️  Message uid:{result['uid']} deleted.")
        return

    if args.mark_seen or args.mark_seen_uid:
        folder_enc = urllib.parse.quote(args.from_folder)
        uid_param  = f"&uid={','.join(args.mark_seen_uid)}" if args.mark_seen_uid else ""
        result     = api_post(
            f"/inboxes/{enc}/mark-seen?folder={folder_enc}{uid_param}", {}
        )
        print(f"✅ Marked as read: {result['marked_seen']} in '{result['folder']}'.")
        return

    if args.flag_uid or args.unflag_uid or args.flag_from or args.unflag_from:
        folder_enc = urllib.parse.quote(args.from_folder)
        unflag     = bool(args.unflag_uid or args.unflag_from)
        uids       = args.unflag_uid or args.flag_uid
        sender     = args.unflag_from or args.flag_from or ""
        uid_param  = f"&uid={','.join(uids)}" if uids else ""
        from_param = f"&sender={urllib.parse.quote(sender)}" if sender else ""
        unflag_param = "&unflag=true" if unflag else ""
        result     = api_post(
            f"/inboxes/{enc}/flag?folder={folder_enc}{uid_param}{from_param}{unflag_param}", {}
        )
        action = "Unflagged" if unflag else "Flagged ⭐"
        if "count" in result:
            print(f"✅ {action}: {result['count']} message(s) from '{sender}' in '{result['folder']}'.")
        else:
            key = "unflagged" if unflag else "flagged"
            print(f"✅ {action}: {result.get(key, '?')} in '{result['folder']}'.")
        return

    p.print_help()


if __name__ == "__main__":
    main()
