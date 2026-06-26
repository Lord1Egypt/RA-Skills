#!/usr/bin/env python3
"""
Self-Improving Agent v2 - Best Practice Logging Tool
Record discovered best practices for future reference
"""

import sys
import json
import os
from datetime import datetime

def get_base_dir():
    if "OPENCLAW_HOME" in os.environ:
        return os.path.join(os.environ["OPENCLAW_HOME"], "memory", "self-improving")
    home = os.path.expanduser("~")
    for candidate in [
        os.path.join(home, ".openclaw"),
        os.path.join(home, "AppData", "Roaming", "openclaw"),
    ]:
        if os.path.exists(os.path.join(candidate, "memory")):
            return os.path.join(candidate, "memory", "self-improving")
    return os.path.join(home, ".openclaw", "memory", "self-improving")

SELF_IMPROVING_DIR = get_base_dir()
BEST_PRACTICES_FILE = os.path.join(SELF_IMPROVING_DIR, "best_practices.jsonl")

def ensure_dir():
    os.makedirs(SELF_IMPROVING_DIR, exist_ok=True)

def log_best_practice(category, practice, reason=None, context=None):
    ensure_dir()
    entry = {
        "category": category,
        "practice": practice,
        "reason": reason or "",
        "context": context or "",
        "timestamp": datetime.now().isoformat()
    }
    with open(BEST_PRACTICES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[OK] Best practice logged: [{category}] {practice}")

if __name__ == "__main__":
    args = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, val = arg.split("=", 1)
            args[key.strip().lstrip("-")] = val.strip()
    
    if "--help" in sys.argv or not args:
        print("Usage: python log_best_practice.py --category=<type> --practice=<what> [--reason=<why>] [--context=<info>]")
        sys.exit(1)
    
    log_best_practice(
        category=args.get("category", ""),
        practice=args.get("practice", ""),
        reason=args.get("reason"),
        context=args.get("context")
    )
