#!/usr/bin/env python3
import json
import os
from datetime import datetime

HOTEL_DIR = os.path.expanduser("~/.openclaw/workspace/memory/hotel")
TRIPS_FILE = os.path.join(HOTEL_DIR, "trips.json")
HOTELS_FILE = os.path.join(HOTEL_DIR, "hotels.json")
PREFS_FILE = os.path.join(HOTEL_DIR, "preferences.json")

def ensure_dir():
    os.makedirs(HOTEL_DIR, exist_ok=True)

def _safe_load(path, default):
    ensure_dir()
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _atomic_save(path, data):
    ensure_dir()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_trips():
    now = datetime.now().isoformat()
    return _safe_load(TRIPS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "trips": {}
    })

def save_trips(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(TRIPS_FILE, data)

def load_hotels():
    now = datetime.now().isoformat()
    return _safe_load(HOTELS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "hotels": {}
    })

def save_hotels(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(HOTELS_FILE, data)

def load_preferences():
    now = datetime.now().isoformat()
    return _safe_load(PREFS_FILE, {
        "metadata": {"version": "1.0.0", "created_at": now, "last_updated": now},
        "preferences": {}
    })

def save_preferences(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(PREFS_FILE, data)
