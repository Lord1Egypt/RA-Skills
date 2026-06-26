#!/usr/bin/env python3
"""Manage music recommendation history.

Usage:
  python3 history.py today          — Show today's recommendations (if any)
  python3 history.py show           — Show ALL previously recommended songs
  python3 history.py save           — Save JSON from stdin as today's recommendations
  python3 history.py check <name> <artists> — Check if a song was recommended before

History files: ~/.openclaw/workspace/music-history/YYYY-MM-DD.json
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

HISTORY_DIR = os.path.expanduser("~/.openclaw/workspace/music-history")
CST = timezone(timedelta(hours=8))


def today_filename() -> str:
    now = datetime.now(CST)
    return os.path.join(HISTORY_DIR, f"{now.strftime('%Y-%m-%d')}.json")


def get_today() -> list | None:
    path = today_filename()
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def get_all_history() -> list:
    """Get all previously recommended songs."""
    all_songs = []
    if not os.path.isdir(HISTORY_DIR):
        return all_songs
    for fname in sorted(os.listdir(HISTORY_DIR)):
        if fname.endswith(".json") and fname[0].isdigit():
            path = os.path.join(HISTORY_DIR, fname)
            try:
                with open(path) as f:
                    songs = json.load(f)
                    for s in songs:
                        s["_date"] = fname.replace(".json", "")
                    all_songs.extend(songs)
            except (json.JSONDecodeError, OSError):
                pass
    return all_songs


def is_recommended(name: str, artists: str) -> bool:
    """Check if a song has been recommended before."""
    history = get_all_history()
    target = f"{name}|{artists}".lower().strip()
    for s in history:
        key = f"{s.get('name','')}|{s.get('artists','')}".lower().strip()
        if target == key:
            return True
    return False


def save_today(data: list) -> None:
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = today_filename()
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} songs to {path}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "today":
        result = get_today()
        if result is None:
            print("NO_RECOMMENDATION_TODAY")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "show":
        history = get_all_history()
        print(json.dumps(history, ensure_ascii=False, indent=2))

    elif cmd == "save":
        data = json.load(sys.stdin)
        save_today(data)
        print("OK")

    elif cmd == "check":
        if len(sys.argv) < 4:
            print("Usage: history.py check <name> <artists>", file=sys.stderr)
            sys.exit(1)
        name = sys.argv[2]
        artists = sys.argv[3]
        if is_recommended(name, artists):
            print("DUPLICATE")
        else:
            print("NEW")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
