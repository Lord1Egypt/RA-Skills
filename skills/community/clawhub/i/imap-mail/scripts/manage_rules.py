#!/usr/bin/env python3
"""
Manage auto-rules via IMAP Mail API.

Rules are applied automatically to UNSEEN messages on every mail check,
so you only need to define them once — they stay active until you remove them.

Usage:
    # Add rules
    python manage_rules.py --inbox agent@example.com --add --from "craig@example.com"
    python manage_rules.py --inbox agent@example.com --add --from "igor@example.com"
    python manage_rules.py --inbox agent@example.com --add --subject "URGENT"

    # List active rules
    python manage_rules.py --inbox agent@example.com --list

    # Apply all rules now (flag matching UNSEEN messages)
    python manage_rules.py --inbox agent@example.com --apply

    # Disable a rule (keep it but don't apply)
    python manage_rules.py --inbox agent@example.com --disable 1

    # Re-enable a rule
    python manage_rules.py --inbox agent@example.com --enable 1

    # Remove a rule permanently
    python manage_rules.py --inbox agent@example.com --remove 1

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
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to IMAP Mail API at {API}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Manage auto-rules for incoming mail")
    p.add_argument("--inbox",   default=INBOX, help="Inbox email address")
    p.add_argument("--list",    action="store_true", help="List all rules")
    p.add_argument("--apply",   action="store_true", help="Apply all rules now to new messages")
    p.add_argument("--add",     action="store_true", help="Add a new rule")
    p.add_argument("--from",    dest="from_", metavar="EMAIL", help="Match sender (use with --add)")
    p.add_argument("--subject", metavar="TEXT",  help="Match subject keyword (use with --add)")
    p.add_argument("--to",      metavar="EMAIL", help="Match recipient (use with --add)")
    p.add_argument("--action",  default="flag", choices=["flag", "mark-seen"],
                   help="Action to apply (default: flag)")
    p.add_argument("--folder",  default="INBOX", help="Folder to watch (default: INBOX)")
    p.add_argument("--remove",  metavar="ID", type=int, help="Remove a rule by ID")
    p.add_argument("--disable", metavar="ID", type=int, help="Disable a rule (keep but skip)")
    p.add_argument("--enable",  metavar="ID", type=int, help="Re-enable a disabled rule")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc = urllib.parse.quote(args.inbox, safe="@.")

    if args.list:
        data  = api_call("GET", f"/inboxes/{enc}/rules")
        rules = data.get("rules", [])
        if not rules:
            print("No rules defined. Add one with --add --from <email>")
            return
        print(f"📋 Rules for {args.inbox}:\n")
        for r in rules:
            status = "✅" if r["enabled"] else "⏸️ "
            print(f"  {status} [{r['id']}] {r['action'].upper()} when "
                  f"{r['match_field']}={r['match_value']!r}  (folder: {r['folder']})")
        return

    if args.apply:
        result = api_call("POST", f"/inboxes/{enc}/rules/apply")
        print(f"⭐ Applied {result['rules_checked']} rule(s) → "
              f"{result['applied']} message(s) affected.")
        return

    if args.add:
        if args.from_:
            field, value = "from", args.from_
        elif args.subject:
            field, value = "subject", args.subject
        elif args.to:
            field, value = "to", args.to
        else:
            print("Error: --add requires --from, --subject, or --to", file=sys.stderr)
            sys.exit(1)
        result = api_call("POST", f"/inboxes/{enc}/rules", {
            "match_field": field,
            "match_value": value,
            "action":      args.action,
            "folder":      args.folder,
        })
        action_icon = "⭐" if args.action == "flag" else "✉️ "
        print(f"✅ Rule [{result['id']}] added: {action_icon} {args.action.upper()} "
              f"when {field}={value!r}")
        return

    if args.remove is not None:
        api_call("DELETE", f"/inboxes/{enc}/rules/{args.remove}")
        print(f"🗑️  Rule [{args.remove}] removed.")
        return

    if args.disable is not None:
        api_call("PATCH", f"/inboxes/{enc}/rules/{args.disable}", {"enabled": False})
        print(f"⏸️  Rule [{args.disable}] disabled.")
        return

    if args.enable is not None:
        api_call("PATCH", f"/inboxes/{enc}/rules/{args.enable}", {"enabled": True})
        print(f"✅ Rule [{args.enable}] enabled.")
        return

    p.print_help()


if __name__ == "__main__":
    main()
