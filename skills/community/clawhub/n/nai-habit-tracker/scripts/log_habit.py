#!/usr/bin/env python3
"""
log_habit.py — Mark a habit as completed for today (or a specific date).

Usage:
  python log_habit.py "Exercise"
  python log_habit.py "Exercise" --date 2024-01-15
  python log_habit.py "Exercise" --undo
  python log_habit.py --data-dir /path/to/data "Exercise"
"""

import json
import sys
import os
import argparse
from datetime import date, datetime
from pathlib import Path


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "habits"


def get_data_dir(override=None):
    if override:
        return Path(override)
    env = os.environ.get("HABIT_DATA_DIR")
    if env:
        return Path(env)
    return DEFAULT_DATA_DIR


def load_json(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def find_habit(habits_data, name):
    """Find an active habit by name (case-insensitive) or ID."""
    active = [h for h in habits_data.get("habits", []) if h.get("active", True)]
    # Exact name match first
    for h in active:
        if h["name"].lower() == name.lower():
            return h
    # ID match
    for h in active:
        if h["id"].lower() == name.lower():
            return h
    # Partial name match
    matches = [h for h in active if name.lower() in h["name"].lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(h["name"] for h in matches)
        print(f"Error: '{name}' is ambiguous. Matches: {names}", file=sys.stderr)
        sys.exit(1)
    return None


def main():
    parser = argparse.ArgumentParser(description="Log a habit completion.")
    parser.add_argument("habit", help="Habit name or ID")
    parser.add_argument("--date", dest="log_date", metavar="YYYY-MM-DD",
                        help="Date to log for (default: today)")
    parser.add_argument("--undo", action="store_true", help="Remove today's log entry")
    parser.add_argument("--data-dir", help="Override data directory")

    args = parser.parse_args()
    data_dir = get_data_dir(args.data_dir)

    # Resolve date
    if args.log_date:
        try:
            log_date = date.fromisoformat(args.log_date)
        except ValueError:
            print(f"Error: invalid date '{args.log_date}'. Use YYYY-MM-DD format.", file=sys.stderr)
            sys.exit(1)
    else:
        log_date = date.today()

    date_str = log_date.isoformat()

    # Load habits
    habits_file = data_dir / "habits.json"
    if not habits_file.exists():
        print("Error: no habits configured. Run setup_habits.py --add first.", file=sys.stderr)
        sys.exit(1)

    habits_data = load_json(habits_file, {"habits": []})
    habit = find_habit(habits_data, args.habit)

    if not habit:
        active_names = [h["name"] for h in habits_data.get("habits", []) if h.get("active", True)]
        print(f"Error: habit '{args.habit}' not found.", file=sys.stderr)
        if active_names:
            print(f"Active habits: {', '.join(active_names)}", file=sys.stderr)
        sys.exit(1)

    # Load log
    log_file = data_dir / "log.json"
    log_data = load_json(log_file, {})

    habit_id = habit["id"]
    habit_name = habit["name"]
    emoji = habit.get("emoji", "✓")

    if args.undo:
        if date_str in log_data and habit_id in log_data[date_str]:
            del log_data[date_str][habit_id]
            if not log_data[date_str]:
                del log_data[date_str]
            save_json(log_file, log_data)
            print(f"↩  Removed log for '{habit_name}' on {date_str}")
        else:
            print(f"Nothing to undo — '{habit_name}' wasn't logged on {date_str}.")
        return

    # Check for duplicate
    if date_str in log_data and habit_id in log_data[date_str]:
        logged_at = log_data[date_str][habit_id].get("logged_at", "unknown time")
        print(f"Already logged '{habit_name}' on {date_str} (at {logged_at}).")
        print("Use --undo to remove it first.")
        return

    # Log the completion
    if date_str not in log_data:
        log_data[date_str] = {}

    log_data[date_str][habit_id] = {
        "done": True,
        "logged_at": datetime.now().isoformat(timespec="seconds"),
    }

    save_json(log_file, log_data)

    suffix = "" if log_date == date.today() else f" (for {date_str})"
    print(f"{emoji} Logged '{habit_name}'{suffix}")


if __name__ == "__main__":
    main()
