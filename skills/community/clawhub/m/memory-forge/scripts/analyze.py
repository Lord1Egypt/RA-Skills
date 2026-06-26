#!/usr/bin/env python3
"""Memory Forge Skill — Local conversation statistics.

Reads Claude Code / ChatGPT / Cursor conversation files and outputs
structured JSON statistics. No external API calls, pure local computation.

Usage:
    python3 analyze.py              # Full stats
    python3 analyze.py --days 30    # Last 30 days only
    python3 analyze.py --weekly     # Include weekly breakdown
    python3 analyze.py --project X  # Filter by project name
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def find_conversations(base_dir: Path, project_filter: str = None) -> list[dict]:
    """Scan conversation directories and parse JSONL files."""
    conversations = []

    if not base_dir.exists():
        return conversations

    for project_dir in sorted(base_dir.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith('.'):
            continue

        project_name = project_dir.name

        if project_filter and project_filter.lower() not in project_name.lower():
            continue

        for jsonl_file in project_dir.glob("*.jsonl"):
            try:
                conv = parse_conversation(jsonl_file, project_name)
                if conv:
                    conversations.append(conv)
            except Exception:
                continue

    return conversations


def parse_conversation(filepath: Path, project: str) -> dict | None:
    """Parse a single JSONL conversation file."""
    messages = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                messages.append(msg)
            except json.JSONDecodeError:
                continue

    if not messages:
        return None

    # Extract metadata
    first_ts = None
    last_ts = None
    total_tokens_in = 0
    total_tokens_out = 0
    cost = 0.0
    model = "unknown"
    human_turns = 0
    assistant_turns = 0

    for msg in messages:
        ts = msg.get("timestamp") or msg.get("createdAt") or msg.get("ts")
        if ts:
            try:
                if isinstance(ts, str):
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                elif isinstance(ts, (int, float)):
                    dt = datetime.fromtimestamp(ts / 1000 if ts > 1e12 else ts)
                else:
                    dt = None

                if dt:
                    if first_ts is None or dt < first_ts:
                        first_ts = dt
                    if last_ts is None or dt > last_ts:
                        last_ts = dt
            except (ValueError, OSError):
                pass

        role = msg.get("role", "")
        if role == "human" or role == "user":
            human_turns += 1
        elif role == "assistant":
            assistant_turns += 1

        # Token usage
        usage = msg.get("usage", {})
        if isinstance(usage, dict):
            total_tokens_in += usage.get("input_tokens", 0) or usage.get("prompt_tokens", 0)
            total_tokens_out += usage.get("output_tokens", 0) or usage.get("completion_tokens", 0)

        # Cost
        if "costUSD" in msg:
            cost += msg["costUSD"]
        elif "cost" in msg:
            cost += msg["cost"]

        # Model
        if msg.get("model"):
            model = msg["model"]

    date_str = first_ts.strftime("%Y-%m-%d") if first_ts else "unknown"

    return {
        "file": str(filepath),
        "project": project,
        "date": date_str,
        "first_ts": first_ts.isoformat() if first_ts else None,
        "last_ts": last_ts.isoformat() if last_ts else None,
        "human_turns": human_turns,
        "assistant_turns": assistant_turns,
        "total_turns": human_turns + assistant_turns,
        "tokens_in": total_tokens_in,
        "tokens_out": total_tokens_out,
        "cost": round(cost, 4),
        "model": model,
    }


def compute_stats(conversations: list[dict], include_weekly: bool = False) -> dict:
    """Compute aggregate statistics from parsed conversations."""
    if not conversations:
        return {"error": "No conversations found", "summary": {}, "projects": {}}

    total_sessions = len(conversations)
    total_turns = sum(c["total_turns"] for c in conversations)
    total_cost = sum(c["cost"] for c in conversations)
    total_tokens_in = sum(c["tokens_in"] for c in conversations)
    total_tokens_out = sum(c["tokens_out"] for c in conversations)

    # Date range
    dates = [c["date"] for c in conversations if c["date"] != "unknown"]
    dates.sort()
    active_days = len(set(dates))
    date_min = dates[0] if dates else "N/A"
    date_max = dates[-1] if dates else "N/A"

    # Per-project stats
    projects = defaultdict(lambda: {"sessions": 0, "cost": 0.0, "turns": 0})
    for c in conversations:
        p = projects[c["project"]]
        p["sessions"] += 1
        p["cost"] += c["cost"]
        p["turns"] += c["total_turns"]

    project_list = []
    for name, stats in sorted(projects.items(), key=lambda x: -x[1]["cost"]):
        project_list.append({
            "name": name,
            "sessions": stats["sessions"],
            "cost": round(stats["cost"], 2),
            "turns": stats["turns"],
            "avg_cost": round(stats["cost"] / max(stats["sessions"], 1), 3),
        })

    # Per-model stats
    models = defaultdict(lambda: {"sessions": 0, "cost": 0.0})
    for c in conversations:
        m = models[c["model"]]
        m["sessions"] += 1
        m["cost"] += c["cost"]

    model_list = [
        {"model": name, "sessions": s["sessions"], "cost": round(s["cost"], 2)}
        for name, s in sorted(models.items(), key=lambda x: -x[1]["cost"])
    ]

    result = {
        "summary": {
            "total_sessions": total_sessions,
            "total_turns": total_turns,
            "total_cost": round(total_cost, 2),
            "total_tokens_in": total_tokens_in,
            "total_tokens_out": total_tokens_out,
            "active_days": active_days,
            "daily_avg_sessions": round(total_sessions / max(active_days, 1), 1),
            "avg_cost_per_session": round(total_cost / max(total_sessions, 1), 3),
            "date_range": f"{date_min} → {date_max}",
        },
        "projects": project_list[:20],  # Top 20
        "models": model_list,
    }

    # Weekly breakdown
    if include_weekly:
        weekly = defaultdict(lambda: {"sessions": 0, "cost": 0.0, "turns": 0})
        for c in conversations:
            if c["date"] == "unknown":
                continue
            try:
                dt = datetime.strptime(c["date"], "%Y-%m-%d")
                week_start = (dt - timedelta(days=dt.weekday())).strftime("%Y-%m-%d")
                w = weekly[week_start]
                w["sessions"] += 1
                w["cost"] += c["cost"]
                w["turns"] += c["total_turns"]
            except ValueError:
                continue

        weekly_list = []
        for week, stats in sorted(weekly.items(), key=lambda x: x[0])[-8:]:
            weekly_list.append({
                "week": week,
                "sessions": stats["sessions"],
                "cost": round(stats["cost"], 2),
                "turns": stats["turns"],
            })
        result["weekly"] = weekly_list

    return result


def main():
    parser = argparse.ArgumentParser(description="Memory Forge conversation analyzer")
    parser.add_argument("--days", type=int, help="Only analyze last N days")
    parser.add_argument("--project", type=str, help="Filter by project name")
    parser.add_argument("--weekly", action="store_true", help="Include weekly breakdown")
    parser.add_argument("--base-dir", type=str, help="Override conversation directory")
    args = parser.parse_args()

    # Find conversation base directory
    base_dir = Path(args.base_dir) if args.base_dir else None
    if not base_dir:
        candidates = [
            Path.home() / ".claude" / "projects",
            Path.home() / ".config" / "claude" / "projects",
            Path.home() / ".cursor" / "projects",
        ]
        for c in candidates:
            if c.exists():
                base_dir = c
                break

    if not base_dir or not base_dir.exists():
        print(json.dumps({"error": f"No conversation directory found. Checked: ~/.claude/projects/, ~/.config/claude/projects/, ~/.cursor/projects/"}))
        sys.exit(1)

    conversations = find_conversations(base_dir, args.project)

    # Filter by days
    if args.days:
        cutoff = datetime.now() - timedelta(days=args.days)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
        conversations = [c for c in conversations if c["date"] >= cutoff_str]

    stats = compute_stats(conversations, include_weekly=args.weekly)

    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
