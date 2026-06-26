#!/usr/bin/env python3
"""
Self-Improving Agent v2 - User Correction Logging Tool
Record user corrections to avoid repeating the same mistakes
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
CORRECTIONS_FILE = os.path.join(SELF_IMPROVING_DIR, "corrections.jsonl")

def ensure_dir():
    os.makedirs(SELF_IMPROVING_DIR, exist_ok=True)

def log_correction(topic, wrong, correct, context=None):
    ensure_dir()
    entry = {
        "topic": topic,
        "wrong": wrong,
        "correct": correct,
        "context": context or "",
        "timestamp": datetime.now().isoformat()
    }
    with open(CORRECTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[OK] Correction logged: [{topic}]")
    print(f"     Wrong: {wrong}")
    print(f"     Correct: {correct}")

if __name__ == "__main__":
    args = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, val = arg.split("=", 1)
            args[key.strip().lstrip("-")] = val.strip()
    
    if "--help" in sys.argv or not args:
        print("Usage: python log_correction.py --topic=<category> --wrong=<wrong> --correct=<right> [--context=<info>]")
        sys.exit(1)
    
    log_correction(
        topic=args.get("topic", ""),
        wrong=args.get("wrong", ""),
        correct=args.get("correct", ""),
        context=args.get("context")
    )
