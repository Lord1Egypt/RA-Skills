#!/usr/bin/env python3
"""Causal Action Logger - 动作因果记录"""

import json
import os
import sys
from datetime import datetime, timezone

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/causal")
ACTIONS_FILE = os.path.join(MEMORY_DIR, "actions.jsonl")

def ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(ACTIONS_FILE):
        open(ACTIONS_FILE, 'w').close()

def log_action(action, domain="general", outcome="pending", context="", pre_state="", post_state=""):
    """记录动作"""
    ensure_dir()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "domain": domain,
        "outcome": outcome,
        "context": context,
        "pre_state": pre_state,
        "post_state": post_state
    }
    with open(ACTIONS_FILE, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✓ 记录: {action} -> {outcome}")
    return entry

def query_actions(domain=None, outcome=None, limit=20):
    """查询动作"""
    ensure_dir()
    results = []
    with open(ACTIONS_FILE) as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            if domain and entry.get("domain") != domain:
                continue
            if outcome and entry.get("outcome") != outcome:
                continue
            results.append(entry)
    return results[-limit:]

def get_timeline(limit=10):
    """获取时间线"""
    actions = query_actions(limit=limit)
    for a in actions:
        ts = a.get('timestamp', '')[:10]
        act = a.get('action', 'unknown')[:40]
        out = a.get('outcome', 'pending')
        print(f"[{ts}] {act} -> {out}")
    return actions

def get_today():
    """获取今日记录"""
    today = datetime.now().strftime("%Y-%m-%d")
    return query_actions(limit=50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: causal.py <log|query|timeline|today> ...")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "log":
        action = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        outcome = sys.argv[3] if len(sys.argv) > 3 else "success"
        log_action(action, outcome=outcome)
    elif cmd == "query":
        for a in query_actions():
            print(json.dumps(a, ensure_ascii=False))
    elif cmd == "timeline":
        get_timeline()
    elif cmd == "today":
        for a in get_today():
            ts = a.get('timestamp', '')[:10]
            print(f"[{ts}] {a.get('action')} -> {a.get('outcome')}")
    else:
        print(f"Unknown: {cmd}")
