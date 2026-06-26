#!/usr/bin/env python3
"""
memory-stack-core — WAL + Working Buffer implementation
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
WAL_FILE = MEMORY_DIR / "wal.jsonl"
BUFFER_FILE = MEMORY_DIR / "working-buffer.md"
CONFIG_FILE = WORKSPACE / "memory-stack-config.json"

# Token estimation: rough chars/4 (actual would use tiktoken)
def estimate_tokens(text: str) -> int:
    return len(text) // 4

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except:
            pass
    return {
        "wal": {"enabled": True, "auto_capture": True, "max_entries": 10000},
        "buffer": {"enabled": True, "threshold_token_percent": 60, "max_size_mb": 10},
        "integration": {"auto_wrap_up_at_token_percent": 80, "include_buffer_in_wrap_up": True}
    }

def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)

def wal_append(category: str, content: str, context: str = ""):
    ensure_dirs()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "category": category,
        "content": content,
        "context": context[:200] if context else ""
    }
    with open(WAL_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    # Rotate if too large
    cfg = load_config()
    max_entries = cfg["wal"].get("max_entries", 10000)
    # Simple rotation: if lines exceed max, rename to .jsonl.old (keep one)
    try:
        line_count = sum(1 for _ in open(WAL_FILE))
        if line_count > max_entries:
            archive = WAL_FILE.with_suffix(".jsonl.old")
            WAL_FILE.rename(archive)
    except:
        pass

def wal_read(limit: int = 50):
    if not WAL_FILE.exists():
        return {"entries": [], "count": 0}
    entries = []
    with open(WAL_FILE) as f:
        lines = f.readlines()[-limit:]
        for line in lines:
            try:
                entries.append(json.loads(line))
            except:
                continue
    return {"entries": entries, "count": len(entries)}

def buffer_write(role: str, content: str):
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BUFFER_FILE, "a") as f:
        f.write(f"\n## {timestamp} (role: {role})\n\n{content}\n\n")
    # Size check
    cfg = load_config()
    max_bytes = cfg["buffer"].get("max_size_mb", 10) * 1024 * 1024
    try:
        if BUFFER_FILE.stat().st_size > max_bytes:
            # Rotate: keep last max_size/2
            all_text = BUFFER_FILE.read_text()
            half = max_bytes // 2
            BUFFER_FILE.write_text(all_text[-half:])
    except:
        pass

def buffer_read(tail: int = 1000):
    if not BUFFER_FILE.exists():
        return {"content": "", "size": 0}
    content = BUFFER_FILE.read_text()
    return {"content": content[-tail:], "size": len(content)}

def memory_health():
    ensure_dirs()
    size_wal = WAL_FILE.stat().st_size if WAL_FILE.exists() else 0
    size_buf = BUFFER_FILE.stat().st_size if BUFFER_FILE.exists() else 0
    daily_logs = list(MEMORY_DIR.glob("*.md")) + list(MEMORY_DIR.glob("20*.md"))
    # Estimate tokens in buffer as proxy for utilization
    tokens_buf_est = estimate_tokens(BUFFER_FILE.read_text()[-10000:]) if BUFFER_FILE.exists() else 0
    # Assume 120k context; buffer tokens / 120k = utilization
    utilization = min(100, int((tokens_buf_est / 120000) * 100))
    return {
        "wal": {"file": str(WAL_FILE), "size_bytes": size_wal, "entries": sum(1 for _ in open(WAL_FILE) if WAL_FILE.exists())},
        "buffer": {"file": str(BUFFER_FILE), "size_bytes": size_buf, "estimated_tokens": tokens_buf_est},
        "daily_logs_count": len(daily_logs),
        "context_utilization_percent": utilization,
        "status": "healthy" if utilization < 80 else "high"
    }

def auto_capture_wal_from_message(message: str):
    """Scan message for specifics and write to WAL automatically."""
    if not load_config()["wal"].get("auto_capture", True):
        return
    patterns = {
        "path": r"(/[-\w./]+|~[-\w./]+|[a-zA-Z]:\\[-\w.\]+)",
        "url": r"https?://[^\s]+",
        "decision": r"(?:decide|choose|go with|let's|we will)\s+([^\n.,;]+)",
        "preference": r"(?:prefer|like|don't like|hate|rather)\s+([^\n.,;]+)",
        "value": r"([\d]+(?:\.\d+)?)(?:\s*(?:seconds?|minutes?|hours?|days?|GB|MB|KB))?",
        "correction": r"(?:actually|correction|oops|sorry,\s*)\s*([^\n.,;]+)"
    }
    found = False
    for cat, pat in patterns.items():
        for m in re.finditer(pat, message, re.IGNORECASE):
            content = m.group(1) if cat in ("decision", "preference", "correction") else m.group(0)
            if content and len(content.strip()) > 1:
                wal_append(cat, content.strip(), message[:100])
                found = True
    return found

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [tool-call|wal-auto] [args...]")
        sys.exit(1)

    action = sys.argv[1]
    args = sys.argv[2:]

    if action == "tool-call":
        if len(args) < 2:
            print(json.dumps({"error": "tool-call requires tool_name and json_input"}))
            sys.exit(1)
        tool = args[0]
        input_json = json.loads(args[1]) if len(args) > 1 else {}

        if tool == "wal_write":
            wal_append(input_json["category"], input_json["content"], input_json.get("context", ""))
            print(json.dumps({"status": "ok", "wal_file": str(WAL_FILE)}))
        elif tool == "wal_read":
            result = wal_read(limit=input_json.get("limit", 50))
            print(json.dumps(result))
        elif tool == "buffer_write":
            buffer_write(input_json["role"], input_json["content"])
            print(json.dumps({"status": "ok", "buffer_file": str(BUFFER_FILE)}))
        elif tool == "buffer_read":
            result = buffer_read(tail=input_json.get("tail", 1000))
            print(json.dumps(result))
        elif tool == "memory_health":
            result = memory_health()
            print(json.dumps(result))
        else:
            print(json.dumps({"error": f"unknown tool: {tool}"}))
            sys.exit(1)

    elif action == "wal-auto":
        # Read message from stdin or file
        msg = sys.stdin.read() if not args else open(args[0]).read()
        captured = auto_capture_wal_from_message(msg)
        print(json.dumps({"captured": captured, "wal_file": str(WAL_FILE)}))
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()