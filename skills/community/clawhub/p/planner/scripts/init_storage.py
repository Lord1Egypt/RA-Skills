#!/usr/bin/env python3
import json
import os
from datetime import datetime

PLANNER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/planner")
PLANS_FILE = os.path.join(PLANNER_DIR, "plans.json")
ARCHIVE_FILE = os.path.join(PLANNER_DIR, "archive.json")

def write_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(PLANNER_DIR, exist_ok=True)

    write_if_missing(PLANS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "plans": {}
    })

    write_if_missing(ARCHIVE_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "plans": {}
    })

    print("✓ Planner storage initialized")
    print(f"  {PLANS_FILE}")
    print(f"  {ARCHIVE_FILE}")

if __name__ == "__main__":
    main()
