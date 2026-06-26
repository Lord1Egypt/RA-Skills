#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cli.py — Command line interface for managing the music stream database.

Usage:
  python cli.py list [genre]                — list streams (optionally filtered by genre)
  python cli.py add URL NAME GENRE [LANG]   — add a stream
  python cli.py remove URL                  — remove a stream
  python cli.py export FILE                 — export to JSON
"""

import json
import os
import sys
from datetime import datetime, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(SKILL_DIR, "state.json")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"streams": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def cmd_list(genre_filter=None):
    state = load_state()
    streams = state.get("streams", [])
    if genre_filter:
        streams = [s for s in streams if s.get("genre", "").lower() == genre_filter.lower()]

    if not streams:
        print("No streams found.")
        return

    streams.sort(key=lambda s: (not s.get("available", True), s.get("genre", ""), s.get("name", "")))

    print(f"{'Status':<6} {'Genre':<15} {'Lang':<6} {'Name'}")
    print("-" * 80)
    for s in streams:
        status = "OK" if s.get("available", True) else "--"
        genre = s.get("genre", "?")[:14]
        lang = s.get("language", "?")[:5]
        name = s.get("name", "Unknown")[:50]
        print(f"{status:<6} {genre:<15} {lang:<6} {name}")

    print(f"\nTotal: {len(streams)}")


def cmd_add(url, name, genre, language="unknown"):
    state = load_state()
    for s in state["streams"]:
        if s["url"] == url:
            print(f"Stream already exists: {name}")
            return

    state["streams"].append({
        "url": url,
        "name": name,
        "genre": genre,
        "language": language,
        "available": True,
        "source": "manual",
        "added_at": datetime.now(timezone.utc).isoformat(),
        "last_checked": None,
        "failed_checks": 0,
    })
    save_state(state)
    print(f"Added: {name} ({genre})")


def cmd_remove(url):
    state = load_state()
    before = len(state["streams"])
    state["streams"] = [s for s in state["streams"] if s["url"] != url]
    after = len(state["streams"])
    save_state(state)
    removed = before - after
    print(f"Removed: {removed}")


def cmd_export(filepath):
    state = load_state()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(state['streams'])} streams to {filepath}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0].lower()

    if cmd == "list":
        genre = args[1] if len(args) > 1 else None
        cmd_list(genre)
    elif cmd == "add" and len(args) >= 4:
        cmd_add(args[1], args[2], args[3], args[4] if len(args) > 4 else "unknown")
    elif cmd == "remove" and len(args) >= 2:
        cmd_remove(args[1])
    elif cmd == "export" and len(args) >= 2:
        cmd_export(args[1])
    else:
        print("Unknown command. Usage:")
        print(__doc__)


if __name__ == "__main__":
    main()
