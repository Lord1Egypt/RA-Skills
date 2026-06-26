#!/usr/bin/env python3
"""
Contact memory (CRM) via IMAP Mail API.

Stores notes, history and context about email contacts.
Used automatically when processing flagged/important messages.

Usage:
    # Look up everything about a contact
    python manage_contacts.py --get craig@example.com

    # List all contacts
    python manage_contacts.py --list

    # Add or update a contact
    python manage_contacts.py --save craig@example.com --name "Craig Smith" --tags "client,priority"

    # Append a note (timestamped automatically)
    python manage_contacts.py --note craig@example.com "Wants proposal by Friday. Budget ~$5k."

    # Delete a contact
    python manage_contacts.py --delete craig@example.com

Environment:
    IMAP_MAIL_API    (default: http://127.0.0.1:8025)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

API = os.getenv("IMAP_MAIL_API", "http://127.0.0.1:8025")


def api_call(method, path, payload=None):
    url  = API.rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    req  = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 404:
            return None
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to IMAP Mail API at {API}: {e}", file=sys.stderr)
        sys.exit(1)


def fmt_ts(ts):
    if not ts:
        return "never"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts


def print_contact(c):
    print(f"👤 {c.get('name') or c['email']}  <{c['email']}>")
    if c.get("tags"):
        print(f"   Tags:     {c['tags']}")
    print(f"   Messages: {c.get('message_count', 0)}  |  Last seen: {fmt_ts(c.get('last_seen'))}")
    notes = (c.get("notes") or "").strip()
    if notes:
        print(f"\n   📝 Notes:")
        for line in notes.splitlines():
            print(f"      {line}")
    print()


def main():
    p = argparse.ArgumentParser(description="Manage contact memory (CRM)")
    p.add_argument("--list",   action="store_true", help="List all contacts")
    p.add_argument("--get",    metavar="EMAIL",     help="Show full contact info")
    p.add_argument("--save",   metavar="EMAIL",     help="Create or update contact")
    p.add_argument("--name",   metavar="NAME",      help="Contact display name (use with --save)")
    p.add_argument("--tags",   metavar="TAGS",      help="Comma-separated tags (use with --save)")
    p.add_argument("--notes",  metavar="TEXT",      help="Set notes text (use with --save)")
    p.add_argument("--note",   metavar="EMAIL",     help="Append a note to a contact")
    p.add_argument("--delete", metavar="EMAIL",     help="Remove contact and all notes")
    p.add_argument("text",     nargs="?",           help="Note text (use with --note)")
    args = p.parse_args()

    if args.list:
        data     = api_call("GET", "/contacts")
        contacts = data.get("contacts", [])
        if not contacts:
            print("No contacts saved yet.")
            return
        print(f"👥 Contacts ({len(contacts)}):\n")
        for c in contacts:
            tags = f"  [{c['tags']}]" if c.get("tags") else ""
            name = c.get("name") or c["email"]
            print(f"  👤 {name} <{c['email']}>{tags}  — {c.get('message_count',0)} msg(s), last: {fmt_ts(c.get('last_seen'))}")
        return

    if args.get:
        enc = urllib.parse.quote(args.get, safe="@.")
        c   = api_call("GET", f"/contacts/{enc}")
        if not c:
            print(f"No contact found for {args.get}")
            return
        print_contact(c)
        return

    if args.save:
        enc    = urllib.parse.quote(args.save, safe="@.")
        result = api_call("PUT", f"/contacts/{enc}", {
            "email": args.save,
            "name":  args.name  or "",
            "notes": args.notes or "",
            "tags":  args.tags  or "",
        })
        print(f"✅ Contact saved: {args.save}")
        return

    if args.note:
        if not args.text:
            print("Error: provide note text after --note EMAIL", file=sys.stderr)
            sys.exit(1)
        enc    = urllib.parse.quote(args.note, safe="@.")
        result = api_call("POST", f"/contacts/{enc}/notes", {"note": args.text})
        print(f"✅ Note added to {args.note}:\n   {result['note_added']}")
        return

    if args.delete:
        enc    = urllib.parse.quote(args.delete, safe="@.")
        result = api_call("DELETE", f"/contacts/{enc}")
        if result:
            print(f"🗑️  Contact {args.delete} deleted.")
        else:
            print(f"Contact {args.delete} not found.")
        return

    p.print_help()


if __name__ == "__main__":
    main()
