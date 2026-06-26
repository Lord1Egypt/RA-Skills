#!/usr/bin/env python3
"""
setup_habits.py — Initialize or modify the habit list.

Usage:
  python setup_habits.py --list
  python setup_habits.py --add "Habit Name" [--frequency daily|weekday|weekly] [--emoji 🏋️]
  python setup_habits.py --remove "Habit Name"
  python setup_habits.py --data-dir /path/to/data
"""

import json
import sys
import os
import argparse
import re
from datetime import date
from pathlib import Path


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "habits"


def get_data_dir(override=None):
    if override:
        return Path(override)
    env = os.environ.get("HABIT_DATA_DIR")
    if env:
        return Path(env)
    return DEFAULT_DATA_DIR


def slugify(name):
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9\s]", "", slug)
    slug = re.sub(r"\s+", "_", slug.strip())
    return slug


def load_habits(data_dir):
    habits_file = data_dir / "habits.json"
    if not habits_file.exists():
        return {"habits": []}
    with open(habits_file) as f:
        return json.load(f)


def save_habits(data_dir, data):
    data_dir.mkdir(parents=True, exist_ok=True)
    habits_file = data_dir / "habits.json"
    with open(habits_file, "w") as f:
        json.dump(data, f, indent=2)


def ensure_log(data_dir):
    """Create log.json if it doesn't exist."""
    log_file = data_dir / "log.json"
    if not log_file.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w") as f:
            json.dump({}, f, indent=2)


def unique_id(existing_ids, slug):
    if slug not in existing_ids:
        return slug
    i = 2
    while f"{slug}_{i}" in existing_ids:
        i += 1
    return f"{slug}_{i}"


def cmd_list(data_dir):
    data = load_habits(data_dir)
    habits = data.get("habits", [])
    active = [h for h in habits if h.get("active", True)]
    inactive = [h for h in habits if not h.get("active", True)]

    if not habits:
        print("No habits configured. Use --add to create one.")
        return

    print(f"\n{'='*48}")
    print(f"  HABIT TRACKER — {len(active)} active habit(s)")
    print(f"{'='*48}")

    if active:
        print("\n  Active habits:")
        for h in active:
            emoji = h.get("emoji", "•")
            freq = h.get("frequency", "daily")
            created = h.get("created", "unknown")
            print(f"    {emoji}  {h['name']}  [{freq}]  (since {created})")

    if inactive:
        print(f"\n  Archived ({len(inactive)}):")
        for h in inactive:
            print(f"    ✗  {h['name']} (archived)")

    print()


def cmd_add(data_dir, name, frequency, emoji):
    valid_freqs = {"daily", "weekday", "weekly"}
    if frequency not in valid_freqs:
        print(f"Error: frequency must be one of {sorted(valid_freqs)}", file=sys.stderr)
        sys.exit(1)

    data = load_habits(data_dir)
    habits = data.get("habits", [])
    existing_ids = {h["id"] for h in habits}
    existing_names = {h["name"].lower() for h in habits if h.get("active", True)}

    if name.lower() in existing_names:
        print(f"Error: habit '{name}' already exists (active).", file=sys.stderr)
        sys.exit(1)

    slug = slugify(name)
    habit_id = unique_id(existing_ids, slug)

    new_habit = {
        "id": habit_id,
        "name": name,
        "frequency": frequency,
        "created": date.today().isoformat(),
        "active": True,
    }
    if emoji:
        new_habit["emoji"] = emoji

    habits.append(new_habit)
    data["habits"] = habits
    save_habits(data_dir, data)
    ensure_log(data_dir)

    freq_label = {"daily": "every day", "weekday": "weekdays only", "weekly": "once a week"}[frequency]
    print(f"✓ Added '{name}' ({freq_label})")


def cmd_remove(data_dir, name):
    data = load_habits(data_dir)
    habits = data.get("habits", [])
    matched = [h for h in habits if h["name"].lower() == name.lower() and h.get("active", True)]

    if not matched:
        print(f"Error: no active habit named '{name}'.", file=sys.stderr)
        sys.exit(1)

    for h in matched:
        h["active"] = False

    data["habits"] = habits
    save_habits(data_dir, data)
    print(f"✓ Archived '{matched[0]['name']}' (history preserved)")


def main():
    parser = argparse.ArgumentParser(description="Manage tracked habits.")
    parser.add_argument("--data-dir", help="Override data directory")
    parser.add_argument("--list", action="store_true", help="List all habits")
    parser.add_argument("--add", metavar="NAME", help="Add a new habit")
    parser.add_argument("--frequency", default="daily", choices=["daily", "weekday", "weekly"],
                        help="Habit frequency (default: daily)")
    parser.add_argument("--emoji", default="", help="Optional emoji for the habit")
    parser.add_argument("--remove", metavar="NAME", help="Archive (soft-delete) a habit")

    args = parser.parse_args()
    data_dir = get_data_dir(args.data_dir)

    if args.add:
        cmd_add(data_dir, args.add, args.frequency, args.emoji)
    elif args.remove:
        cmd_remove(data_dir, args.remove)
    elif args.list:
        cmd_list(data_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
