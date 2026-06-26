#!/usr/bin/env python3
"""
MemWeaver — Memory Collection Script

Reads long-term memory (MEMORY.md) and recent daily logs (memory/*.md)
from the workspace, merges them into structured JSON output for Agent analysis.

Usage:
    python3 collect_memory.py [--days 14] [--workspace /path/to/workspace]

Output:
    stdout: JSON-formatted memory collection result
    stderr: Progress information
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="MemWeaver Memory Collector")
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Collect logs from the last N days (default: 14)",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Workspace root directory (default: auto-detect)",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Path to existing profile file (for incremental updates)",
    )
    return parser.parse_args()


def find_workspace(script_dir):
    """Walk up from script directory to find workspace root (directory containing .codebuddy/)"""
    current = Path(script_dir).resolve()
    for _ in range(5):
        if (current / ".codebuddy").is_dir():
            return current
        current = current.parent
    return None


def read_file_safe(filepath):
    """Safely read a file, return None on failure"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"  ⚠️ Cannot read {filepath}: {e}", file=sys.stderr)
        return None


def estimate_tokens(text):
    """Rough token estimation (Chinese ~1.5 chars/token, English ~4 chars/token)"""
    if not text:
        return 0
    chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.5 + other_chars / 4)


def collect_daily_logs(memory_dir, days):
    """Collect daily log files from the last N days"""
    logs = {}
    cutoff = datetime.now() - timedelta(days=days)

    if not memory_dir.is_dir():
        print(f"  ⚠️ Log directory does not exist: {memory_dir}", file=sys.stderr)
        return logs

    for f in sorted(memory_dir.glob("*.md"), reverse=True):
        # Filename format: 2026-03-20.md
        try:
            date_str = f.stem  # "2026-03-20"
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue

        if file_date < cutoff:
            continue

        content = read_file_safe(f)
        if content and content.strip():
            logs[date_str] = content.strip()
            print(f"  ✅ {f.name} ({len(content.splitlines())} lines)", file=sys.stderr)

    return logs


def main():
    args = parse_args()

    # Locate workspace
    if args.workspace:
        workspace = Path(args.workspace)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace = find_workspace(script_dir)

    if not workspace or not (workspace / ".codebuddy").is_dir():
        print("Error: Cannot locate workspace (.codebuddy/ directory not found)", file=sys.stderr)
        sys.exit(1)

    print(f"Workspace: {workspace}", file=sys.stderr)
    print(f"Collection range: last {args.days} days", file=sys.stderr)
    print("", file=sys.stderr)

    # 1. Read long-term memory
    print("📖 Reading long-term memory...", file=sys.stderr)
    memory_file = workspace / ".codebuddy" / "MEMORY.md"
    long_term = read_file_safe(memory_file)
    if long_term:
        print(
            f"  ✅ MEMORY.md ({len(long_term.splitlines())} lines)",
            file=sys.stderr,
        )
    else:
        print("  ❌ MEMORY.md does not exist or is empty", file=sys.stderr)
        long_term = ""

    # 2. Collect daily logs
    print("📋 Collecting daily logs...", file=sys.stderr)
    memory_dir = workspace / ".codebuddy" / "memory"
    daily_logs = collect_daily_logs(memory_dir, args.days)
    print(f"  Collected {len(daily_logs)} days of logs", file=sys.stderr)

    # 3. Read existing profile (if any)
    existing_profile = None
    if args.profile and os.path.exists(args.profile):
        print(f"📄 Reading existing profile: {args.profile}", file=sys.stderr)
        existing_profile = read_file_safe(args.profile)
    else:
        # Auto-detect latest profile in output/
        # Look for memweaver/output/ relative to the skill directory
        skill_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        output_dir = skill_dir / "output"
        if output_dir.is_dir():
            profiles = sorted(output_dir.glob("profile_*.yaml"), reverse=True)
            if profiles:
                print(
                    f"📄 Found existing profile: {profiles[0].name}",
                    file=sys.stderr,
                )
                existing_profile = read_file_safe(profiles[0])

    # 4. Statistics
    all_files = []
    total_lines = 0

    if long_term:
        all_files.append("MEMORY.md")
        total_lines += len(long_term.splitlines())

    for date_str in daily_logs:
        all_files.append(f"memory/{date_str}.md")
        total_lines += len(daily_logs[date_str].splitlines())

    all_text = long_term + "\n".join(daily_logs.values())
    total_tokens = estimate_tokens(all_text)

    # 5. Output JSON
    result = {
        "workspace": str(workspace),
        "collected_at": datetime.now().isoformat(),
        "files_read": all_files,
        "total_lines": total_lines,
        "estimated_tokens": total_tokens,
        "days_covered": args.days,
        "existing_profile": existing_profile,
        "content": {
            "long_term": long_term,
            "daily_logs": daily_logs,
        },
    }

    print("", file=sys.stderr)
    print(f"📊 Summary: {len(all_files)} files, {total_lines} lines, ~{total_tokens} tokens", file=sys.stderr)

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
