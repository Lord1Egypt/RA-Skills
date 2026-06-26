#!/usr/bin/env python3
"""GOG Dormant Game Sweep — find installed games not played in N days, email report, add Apple Reminders."""

import json
import subprocess
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

DEFAULT_LIBRARY = "config/gog_library.json"
DEFAULT_HIMALAYA_ACCOUNT = "personal"
DEFAULT_REMINDERS_LIST = "Gaming"
DEFAULT_DAYS = 30


def load_library(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"Error: library file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(p) as f:
        return json.load(f)


def find_dormant_games(library: dict, days: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    dormant = []
    for g in library.get("games", []):
        if not g.get("installed"):
            continue
        lp = g.get("last_played")
        if lp is None:
            # Never played and installed → dormant
            dormant.append(g)
            continue
        last = datetime.fromisoformat(lp)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        if last < cutoff:
            dormant.append(g)
    return dormant


def format_email_body(dormant: list[dict], days: int) -> str:
    lines = [
        f"GOG Dormant Game Report — games not played in {days}+ days",
        "=" * 50,
        "",
    ]
    if not dormant:
        lines.append("No dormant games found. Your library is clean!")
        return "\n".join(lines)

    for i, g in enumerate(dormant, 1):
        lp = g.get("last_played")
        played_str = lp if lp else "Never"
        lines.append(f"{i}. {g['name']}")
        lines.append(f"   Last played: {played_str}")
        lines.append(f"   Install path: {g.get('install_path', 'N/A')}")
        lines.append("")

    lines.append(f"Total: {len(dormant)} dormant game(s)")
    lines.append("Consider uninstalling games you no longer play.")
    return "\n".join(lines)


def send_email(account: str, to_addr: str, subject: str, body: str):
    """Send email via himalaya CLI."""
    cmd = [
        "himalaya", "message", "write",
        "--account", account,
        "-H", f"To:{to_addr}",
        "-H", f"Subject:{subject}",
        body,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error sending email: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Email sent to {to_addr}")


def add_reminder(game_name: str, reminders_list: str):
    """Add a reminder via remindctl."""
    title = f"Consider uninstalling: {game_name}"
    cmd = [
        "remindctl", "add",
        "--title", title,
        "--list", reminders_list,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Warning: failed to add reminder for '{game_name}': {result.stderr}", file=sys.stderr)
    else:
        print(f"Reminder added: {title}")


def main():
    parser = argparse.ArgumentParser(description="GOG Dormant Game Sweep")
    parser.add_argument("--library", default=DEFAULT_LIBRARY, help="Path to GOG library JSON")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Dormancy threshold in days")
    parser.add_argument("--email", default=None, help="Recipient email address")
    parser.add_argument("--himalaya-account", default=DEFAULT_HIMALAYA_ACCOUNT, help="Himalaya account name")
    parser.add_argument("--reminders-list", default=DEFAULT_REMINDERS_LIST, help="Apple Reminders list name")
    parser.add_argument("--no-email", action="store_true", help="Skip sending email")
    parser.add_argument("--no-reminders", action="store_true", help="Skip adding reminders")
    parser.add_argument("--dry-run", action="store_true", help="Print results without taking action")
    args = parser.parse_args()

    library = load_library(args.library)
    dormant = find_dormant_games(library, args.days)

    if not dormant:
        print("No dormant games found.")
        return

    print(f"Found {len(dormant)} dormant game(s):")
    for g in dormant:
        lp = g.get("last_played", "Never")
        print(f"  - {g['name']} (last played: {lp})")

    body = format_email_body(dormant, args.days)
    subject = f"GOG Dormant Games — {len(dormant)} game(s) to review"

    if args.dry_run:
        print("\n--- Dry run: email body ---")
        print(body)
        print("--- End dry run ---")
        return

    if not args.no_email and args.email:
        send_email(args.himalaya_account, args.email, subject, body)

    if not args.no_reminders:
        for g in dormant:
            add_reminder(g["name"], args.reminders_list)

    print("Sweep complete.")


if __name__ == "__main__":
    main()