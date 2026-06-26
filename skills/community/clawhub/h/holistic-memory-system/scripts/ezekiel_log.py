#!/usr/bin/env python3
"""
Ézekiel Memory System — L3 Log Writer (FIXED)
Écrit les logs en JSONL pour la couche L3 (Traces Pures)
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path.home() / ".openclaw" / "memory-logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_interaction(intent: str, content: str, tags: list = None, agent: str = "ezekiel"):
    """Écrit une interaction dans les logs JSONL"""
    now = datetime.now(timezone.utc)
    entry = {
        "ts": now.isoformat(),
        "intent": intent,
        "content": content,
        "tags": tags or [],
        "agent": agent,
        "day": now.strftime("%Y-%m-%d")
    }
    
    log_file = LOG_DIR / f"ezekiel_{now.strftime('%Y-%m-%d')}.jsonl"
    
    with open(log_file, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    return entry

def query_logs(date: str = None, intent: str = None, limit: int = 100):
    """Requête les logs par date ou intent"""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    log_file = LOG_DIR / f"ezekiel_{date}.jsonl"
    
    if not log_file.exists():
        return []
    
    results = []
    with open(log_file, "r") as f:
        for line in f:
            entry = json.loads(line)
            if intent is None or intent in entry.get("intent", ""):
                results.append(entry)
    
    return results[:limit]

def get_recent_entries(days: int = 7, limit: int = 100):
    """Récupère les entrées récentes sur plusieurs jours"""
    results = []
    now = datetime.now(timezone.utc)
    
    for i in range(days):
        date = (now - timezone.utc).replace(day=now.day - i).strftime("%Y-%m-%d")
        day_results = query_logs(date)
        results.extend(day_results)
    
    return results[:limit]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "log" and len(sys.argv) > 3:
            intent = sys.argv[2]
            content = sys.argv[3]
            tags = sys.argv[4:] if len(sys.argv) > 4 else []
            result = log_interaction(intent, content, tags)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif sys.argv[1] == "query":
            date = sys.argv[2] if len(sys.argv) > 2 else None
            results = query_logs(date)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif sys.argv[1] == "recent":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            results = get_recent_entries(days)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print("Usage: python3 ezekiel_log.py log <intent> <content> [tags...]")
            print("       python3 ezekiel_log.py query [date]")
            print("       python3 ezekiel_log.py recent [days]")
    else:
        # Test: log current session start
        result = log_interaction("session_reinit", "Ézekiel L3 log reinitialized (fixed datetime)", ["system", "startup", "fixed"])
        print(f"Logged: {result['ts']}")