#!/usr/bin/env python3
import json
import os
from datetime import datetime

HOTEL_DIR = os.path.expanduser("~/.openclaw/workspace/memory/hotel")
TRIPS_FILE = os.path.join(HOTEL_DIR, "trips.json")
HOTELS_FILE = os.path.join(HOTEL_DIR, "hotels.json")
PREFS_FILE = os.path.join(HOTEL_DIR, "preferences.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(HOTEL_DIR, exist_ok=True)

    now = datetime.now().isoformat()

    write_json_if_missing(TRIPS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "trips": {}
    })

    write_json_if_missing(HOTELS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "hotels": {}
    })

    write_json_if_missing(PREFS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "preferences": {}
    })

    print("✓ Hotel storage initialized")
    print(f"  {TRIPS_FILE}")
    print(f"  {HOTELS_FILE}")
    print(f"  {PREFS_FILE}")

if __name__ == "__main__":
    main()
