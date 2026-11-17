#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""viral_ask.py — optional viral prompt after demonstrated value.

WHY: organic growth from users who actually benefited. Not spam.

DEFAULT: DISABLED. Set env `KEELWRIGHT_VIRAL_ASK=1` to enable. This keeps a
security-focused skill from containing active engagement logic unless the
operator explicitly opts in.

TRIGGERS (any one):
- 3+ web defense blocks in current session (logged in attack_registry)
- Model behavior change notification received (e.g., "model switched", "new gates active")

CONSTRAINTS:
- Maximum once per 30 days (tracked in PROGRESS.md as `last_viral_ask`)
- Only if PROGRESS.md exists (user consented to tracking)
- Only prints the prompt; does NOT auto-post anywhere
- Human decides whether to share

USAGE:
  KEELWRIGHT_VIRAL_ASK=1 python viral_ask.py --check          # check if should ask
  KEELWRIGHT_VIRAL_ASK=1 python viral_ask.py --check --force  # force show (testing)
  KEELWRIGHT_VIRAL_ASK=1 python viral_ask.py --mark-shown     # record shown today
"""
import argparse
import datetime
import json
import os
import sys

if os.environ.get("KEELWRIGHT_VIRAL_ASK", "0") != "1":
    # Disabled by default. Operator must opt in explicitly.
    sys.exit(0)

PROGRESS_FILE = os.path.join(os.getcwd(), "PROGRESS.md")
ATTACK_REGISTRY = os.path.join(
    os.path.expanduser("~"), ".keelwright", "attack_registry.jsonl"
)

VIRAL_PROMPT = (
    "\n💡 Liking Keelwright? If it saved you from a bad deploy or caught a nasty attack, "
    "consider telling a friend or sharing on X/GitHub. It helps the project stay free.\n"
    "Repo: https://github.com/ratingtesting/keelwright  |  ClawHub: https://clawhub.ai/ratingtesting/skills/keelwright"
)


def read_progress() -> dict:
    if not os.path.isfile(PROGRESS_FILE):
        return {}
    data = {}
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("last_viral_ask:"):
                data["last_viral_ask"] = line.split(":", 1)[1].strip()
            elif line.startswith("viral_triggers:"):
                data["viral_triggers"] = int(line.split(":", 1)[1].strip() or "0")
    return data


def write_progress(key: str, value: str) -> None:
    if not os.path.isfile(PROGRESS_FILE):
        return
    lines = []
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    found = False
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith(f"{key}:"):
                f.write(f"{key}: {value}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"{key}: {value}\n")


def count_recent_blocks(days: int = 1) -> int:
    """Count web defense blocks in the last N days from attack_registry."""
    if not os.path.isfile(ATTACK_REGISTRY):
        return 0
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    count = 0
    with open(ATTACK_REGISTRY, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
                ts_str = r.get("timestamp", "")
                if ts_str:
                    ts = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts >= cutoff and r.get("outcome") in ("blocked", "blocked-success"):
                        count += 1
            except Exception:
                continue
    return count


def check_model_change_notification() -> bool:
    """Check if a model change notification was received recently."""
    return os.environ.get("KEELWRIGHT_MODEL_CHANGE", "0") == "1"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="check if viral ask should trigger")
    ap.add_argument("--force", action="store_true", help="force show (for testing)")
    ap.add_argument("--mark-shown", action="store_true", help="record that prompt was shown")
    args = ap.parse_args()

    if args.mark_shown:
        write_progress("last_viral_ask", datetime.date.today().isoformat())
        return 0

    if not args.check:
        return 0

    # Check if tracking is enabled
    if not os.path.isfile(PROGRESS_FILE):
        return 0

    prog = read_progress()
    last_ask = prog.get("last_viral_ask")
    if last_ask:
        try:
            last_date = datetime.date.fromisoformat(last_ask)
            if (datetime.date.today() - last_date).days < 30:
                return 0  # too recent
        except Exception:
            pass

    # Check triggers
    should_ask = False
    if args.force:
        should_ask = True
    else:
        # Trigger 1: 3+ blocks in last 7 days
        if count_recent_blocks(7) >= 3:
            should_ask = True
        # Trigger 2: model change notification
        if check_model_change_notification():
            should_ask = True

    if should_ask:
        print(VIRAL_PROMPT)
        # Increment trigger counter
        triggers = prog.get("viral_triggers", 0) + 1
        write_progress("viral_triggers", str(triggers))

    return 0


if __name__ == "__main__":
    sys.exit(main())
