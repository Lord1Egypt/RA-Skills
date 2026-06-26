#!/usr/bin/env python3
import json
import os
from datetime import datetime

PLANNER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/planner")
PLANS_FILE = os.path.join(PLANNER_DIR, "plans.json")
ARCHIVE_FILE = os.path.join(PLANNER_DIR, "archive.json")

def ensure_dir():
    os.makedirs(PLANNER_DIR, exist_ok=True)

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

def load_plans():
    return _safe_load(PLANS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "plans": {}
    })

def save_plans(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(PLANS_FILE, data)

def load_archive():
    return _safe_load(ARCHIVE_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "plans": {}
    })

def save_archive(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(ARCHIVE_FILE, data)
