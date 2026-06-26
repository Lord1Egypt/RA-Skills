#!/usr/bin/env python3
"""操作日志：记录记忆系统自身的操作"""

import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_write, file_lock

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
LOG_FILE = ".operations.log.jsonl"


def log(memory_dir: Path, operation: str, details: dict | None = None, level: str = "info"):
    """记录操作日志"""
    log_path = memory_dir / LOG_FILE
    entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "level": level,
        "details": details or {},
    }
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    safe_write(log_path, line, append=True)


def get_recent_logs(memory_dir: Path, count: int = 20, level: str | None = None) -> list[dict]:
    """获取最近日志"""
    log_path = memory_dir / LOG_FILE
    if not log_path.exists():
        return []

    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    entries = []
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            if level and entry.get("level") != level:
                continue
            entries.append(entry)
            if len(entries) >= count:
                break
        except json.JSONDecodeError:
            continue
    return entries


def print_logs(entries: list[dict]):
    if not entries:
        print("📭 无操作日志")
        return

    level_icons = {"info": "ℹ️", "warn": "⚠️", "error": "❌", "success": "✅"}
    
    print("=" * 60)
    print("📋 最近操作日志")
    print("=" * 60)
    
    for entry in entries:
        ts = entry["timestamp"][:16].replace("T", " ")
        icon = level_icons.get(entry.get("level", "info"), "•")
        op = entry["operation"]
        details = entry.get("details", {})
        
        detail_str = ""
        if details:
            if isinstance(details, dict):
                parts = [f"{k}={v}" for k, v in list(details.items())[:3]]
                detail_str = " | " + " ".join(parts)
            else:
                detail_str = f" | {details}"
        
        print(f"  {ts} {icon} {op}{detail_str}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="操作日志")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--level", default=None)
    p.add_argument("--test", action="store_true", help="写入测试日志")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.test:
        log(md, "test", {"message": "操作日志测试"}, "info")
        log(md, "archive", {"date": "2026-04-11", "session": "test"}, "success")
        log(md, "warning", {"issue": "测试警告"}, "warn")
        print("✅ 测试日志已写入")

    entries = get_recent_logs(md, args.count, args.level)
    print_logs(entries)
