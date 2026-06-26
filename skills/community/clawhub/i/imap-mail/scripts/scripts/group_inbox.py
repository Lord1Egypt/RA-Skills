#!/usr/bin/env python3
"""
Analyze inbox and group recurring messages into dedicated sub-folders.

Groups messages by sender (3+ messages from same address) or by subject
(3+ messages with the same normalized topic). Creates sub-folders under
a parent folder (default: Groups) and adds persistent auto-rules so all
future matching messages are routed there automatically.

Usage:
    # Preview candidates (no changes)
    python group_inbox.py --inbox agent@example.com --suggest

    # Apply specific candidates by index (shown in --suggest output)
    python group_inbox.py --inbox agent@example.com --apply 0 2

    # Apply all candidates at once
    python group_inbox.py --inbox agent@example.com --apply-all

    # Enable auto-grouping (applied automatically on every mail check)
    python group_inbox.py --inbox agent@example.com --auto-enable

    # Disable auto-grouping
    python group_inbox.py --inbox agent@example.com --auto-disable

    # Check auto-grouping status
    python group_inbox.py --inbox agent@example.com --status

    # Apply auto-grouping right now (used by cron when enabled)
    python group_inbox.py --inbox agent@example.com --auto-apply

Options:
    --threshold N      Minimum messages to suggest a group (default: 3)
    --parent-folder F  Parent folder for groups (default: Groups)
    --folder F         Source folder to analyze (default: INBOX)
    --dry-run          Show what would happen without making changes

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


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def api_get(path):
    url = API.rstrip("/") + path
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url), timeout=20)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to API at {API}: {e}", file=sys.stderr)
        sys.exit(1)


def api_post(path, payload=None, params=None):
    url = API.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(payload or {}).encode()
    req  = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


# ── Output helpers ────────────────────────────────────────────────────────────

def print_candidates(candidates, parent_folder):
    if not candidates:
        print("📭 No grouping candidates found (not enough repeated senders/subjects).")
        return
    print(f"📊 Found {len(candidates)} candidate(s) for grouping:\n")
    for i, c in enumerate(candidates):
        icon   = "👤" if c["type"] == "sender" else "📌"
        folder = f"{parent_folder}/{c['suggested_folder']}"
        print(f"  [{i}] {icon} {c['key']}")
        print(f"       {c['count']} messages → folder: {folder}")
        print(f"       Auto-rule: {c['rule_field']}={c['rule_value']!r}")
        print()


def print_applied(report, dry_run):
    if dry_run:
        print(f"🔍 Dry run — no changes made\n")
    else:
        print(f"✅ Applied {len(report)} group(s)\n")
    for r in report:
        status = "would move" if dry_run else "moved"
        rule   = "" if dry_run else ("  ✅ rule added" if r["rule_added"] else "")
        print(f"  📁 {r['folder']}: {status} {r['moved']} message(s){rule}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="Group inbox messages into sub-folders by sender or subject"
    )
    p.add_argument("--inbox",         default=INBOX,    help="Inbox email address")
    p.add_argument("--folder",        default="INBOX",  help="Source folder (default: INBOX)")
    p.add_argument("--parent-folder", default="Groups", dest="parent_folder",
                   help="Parent folder for groups (default: Groups)")
    p.add_argument("--threshold",     type=int, default=3,
                   help="Min messages to suggest a group (default: 3)")
    p.add_argument("--dry-run",       action="store_true", dest="dry_run",
                   help="Preview without making changes")

    # Actions
    p.add_argument("--suggest",      action="store_true",
                   help="Analyze and show candidates")
    p.add_argument("--apply",        nargs="+", type=int, metavar="INDEX",
                   help="Apply candidates by index from --suggest output")
    p.add_argument("--apply-all",    action="store_true", dest="apply_all",
                   help="Apply all candidates")
    p.add_argument("--auto-enable",  action="store_true", dest="auto_enable",
                   help="Enable auto-grouping (runs on every mail check)")
    p.add_argument("--auto-disable", action="store_true", dest="auto_disable",
                   help="Disable auto-grouping")
    p.add_argument("--auto-apply",   action="store_true", dest="auto_apply",
                   help="Run auto-grouping now (used by cron)")
    p.add_argument("--status",       action="store_true",
                   help="Show auto-grouping status")
    args = p.parse_args()

    if not args.inbox:
        print("Error: specify --inbox or set IMAP_MAIL_INBOX", file=sys.stderr)
        sys.exit(1)

    enc = urllib.parse.quote(args.inbox, safe="@.")

    # ── Status ──
    if args.status:
        data = api_get(f"/inboxes/{enc}/autogroup/status")
        status = "✅ enabled" if data["enabled"] else "⏸️  disabled"
        print(f"Auto-grouping: {status}")
        print(f"  Threshold:     {data['threshold']} messages")
        print(f"  Parent folder: {data['parent_folder']}")
        return

    # ── Enable / Disable ──
    if args.auto_enable:
        data = api_post(f"/inboxes/{enc}/autogroup/enable", params={
            "threshold":     args.threshold,
            "parent_folder": args.parent_folder,
        })
        print(f"✅ Auto-grouping enabled  (threshold: {data['threshold']}, "
              f"parent: {data['parent_folder']})")
        return

    if args.auto_disable:
        api_post(f"/inboxes/{enc}/autogroup/disable")
        print("⏸️  Auto-grouping disabled.")
        return

    # ── Fetch candidates ──
    def get_candidates():
        params = urllib.parse.urlencode({
            "folder":    args.folder,
            "threshold": args.threshold,
        })
        return api_get(f"/inboxes/{enc}/analyze?{params}")

    # ── Suggest ──
    if args.suggest:
        data       = get_candidates()
        candidates = data.get("candidates", [])
        print(f"🔍 Scanned {data['scanned']} messages in {data['folder']}\n")
        print_candidates(candidates, args.parent_folder)
        if candidates:
            print("To apply, run:")
            indices = " ".join(str(i) for i in range(len(candidates)))
            print(f"  python group_inbox.py --inbox {args.inbox} --apply {indices}")
            print(f"  python group_inbox.py --inbox {args.inbox} --apply-all")
        return

    # ── Apply selected / all ──
    if args.apply is not None or args.apply_all:
        data       = get_candidates()
        candidates = data.get("candidates", [])

        if not candidates:
            print("📭 No candidates to apply.")
            return

        if args.apply_all:
            selected = candidates
        else:
            selected = []
            for i in args.apply:
                if 0 <= i < len(candidates):
                    selected.append(candidates[i])
                else:
                    print(f"Warning: index {i} out of range (0–{len(candidates)-1}), skipped.",
                          file=sys.stderr)
            if not selected:
                print("No valid candidates selected.", file=sys.stderr)
                sys.exit(1)

        params = {"folder": args.folder, "parent_folder": args.parent_folder}
        if args.dry_run:
            params["dry_run"] = "true"

        result = api_post(
            f"/inboxes/{enc}/analyze/apply",
            payload={"candidates": selected},
            params=params,
        )
        print_applied(result["applied"], args.dry_run)
        return

    # ── Auto-apply (called by cron when enabled) ──
    if args.auto_apply:
        status = api_get(f"/inboxes/{enc}/autogroup/status")
        if not status["enabled"]:
            return  # silently skip — auto-grouping is off

        params = urllib.parse.urlencode({
            "folder":    args.folder,
            "threshold": status["threshold"],
        })
        data       = api_get(f"/inboxes/{enc}/analyze?{params}")
        candidates = data.get("candidates", [])

        if not candidates:
            return  # nothing to do

        result = api_post(
            f"/inboxes/{enc}/analyze/apply",
            payload={"candidates": candidates},
            params={"folder": args.folder, "parent_folder": status["parent_folder"]},
        )
        total_moved = sum(r["moved"] for r in result["applied"])
        if total_moved > 0:
            print(f"🗂️  Auto-grouped: {total_moved} message(s) into "
                  f"{len(result['applied'])} folder(s).")
            for r in result["applied"]:
                if r["moved"] > 0:
                    print(f"   📁 {r['folder']}: {r['moved']} message(s)")
        return

    p.print_help()


if __name__ == "__main__":
    main()
