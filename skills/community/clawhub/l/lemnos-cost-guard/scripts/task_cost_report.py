#!/usr/bin/env python3
"""
task_cost_report.py — Per-task cost reporting for Max / Lemnos AI Operations

USAGE:
  python3 task_cost_report.py                  # Today's task breakdown
  python3 task_cost_report.py --days 7         # Last 7 days
  python3 task_cost_report.py --date 2026-03-02
  python3 task_cost_report.py --format summary # One-liner per task type
  python3 task_cost_report.py --format full    # Every individual task entry
  python3 task_cost_report.py --format brief   # Telegram-ready compact output
"""

import json
import os
import argparse
from datetime import datetime, timezone, timedelta
from collections import defaultdict

LOG_PATH = "/root/.openclaw/workspace/skills/lemnos-cost-guard/references/task-log.jsonl"

TASK_LABELS = {
    "briefing": "📋 Briefing",
    "email_send": "📤 Email Send",
    "email_draft": "✍️  Email Draft",
    "prospect_research": "🔍 Prospect Research",
    "bounce_check": "📬 Bounce Check",
    "tweet_draft": "🐦 Tweet Draft",
    "tweet_send": "🐦 Tweet Send",
    "reddit_scan": "📣 Reddit Scan",
    "reddit_draft": "📣 Reddit Draft",
    "memory_update": "🧠 Memory Update",
    "cost_report": "💰 Cost Report",
    "reply_monitor": "📥 Reply Monitor",
    "linkedin_research": "🔗 LinkedIn Research",
    "trl_intel": "💊 TRL Intel",
    "aeramed_research": "😴 AeraMed Research",
    "crypto_monitor": "₿  Crypto Monitor",
    "other": "⚙️  Other",
}


def load_entries(date_strings):
    date_set = set(date_strings)
    entries = []
    if not os.path.exists(LOG_PATH):
        return entries
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("date", obj.get("timestamp", "")[:10]) in date_set:
                    entries.append(obj)
            except json.JSONDecodeError:
                continue
    return entries


def get_date_strings(days=1, date=None):
    if date:
        return [date]
    today = datetime.now(timezone.utc)
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]


def aggregate_by_type(entries):
    agg = defaultdict(lambda: {
        "count": 0, "calls": 0, "cost": 0.0,
        "output_tokens": 0, "cache_write_tokens": 0
    })
    for e in entries:
        t = e.get("task_type", "other")
        agg[t]["count"] += 1
        agg[t]["calls"] += e.get("calls", 0)
        agg[t]["cost"] += e.get("cost_usd", 0)
        agg[t]["output_tokens"] += e.get("output_tokens", 0)
        agg[t]["cache_write_tokens"] += e.get("cache_write_tokens", 0)
    return agg


def format_brief(entries, date_label):
    """Compact Telegram-ready output."""
    if not entries:
        print(f"💰 TASK COSTS ({date_label}): No tasks logged yet.")
        return

    agg = aggregate_by_type(entries)
    total_cost = sum(v["cost"] for v in agg.values())
    total_tasks = sum(v["count"] for v in agg.values())
    total_calls = sum(v["calls"] for v in agg.values())

    print(f"💰 TASK COSTS ({date_label}) — {total_tasks} tasks | {total_calls} calls | ${total_cost:.4f} total")
    print()

    for task_type, data in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
        label = TASK_LABELS.get(task_type, f"⚙️  {task_type}")
        avg = data["cost"] / data["count"] if data["count"] else 0
        print(f"  {label:<28} {data['count']:>2}x | ${data['cost']:.4f} total | ${avg:.4f}/task")


def format_summary(entries, date_label):
    """Table-style summary by task type."""
    if not entries:
        print(f"No tasks logged for {date_label}.")
        return

    agg = aggregate_by_type(entries)
    total_cost = sum(v["cost"] for v in agg.values())

    print(f"\n{'='*65}")
    print(f"TASK COST REPORT — {date_label}")
    print(f"{'='*65}")
    print(f"{'Task Type':<26} {'Runs':>5} {'Calls':>6} {'Output':>9} {'Total$':>8} {'Avg$/task':>10}")
    print(f"{'-'*65}")

    for task_type, data in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
        label = TASK_LABELS.get(task_type, task_type)[:25]
        avg = data["cost"] / data["count"] if data["count"] else 0
        out_k = f"{data['output_tokens']//1000}K" if data["output_tokens"] >= 1000 else str(data["output_tokens"])
        print(f"{label:<26} {data['count']:>5} {data['calls']:>6} {out_k:>9} "
              f"${data['cost']:>7.4f} ${avg:>9.4f}")

    print(f"{'-'*65}")
    print(f"{'TOTAL':<26} {sum(v['count'] for v in agg.values()):>5} "
          f"{sum(v['calls'] for v in agg.values()):>6} "
          f"{'':>9} ${total_cost:>7.4f}")
    print(f"{'='*65}\n")


def format_full(entries, date_label):
    """Every individual task entry."""
    if not entries:
        print(f"No tasks logged for {date_label}.")
        return

    print(f"\n{'='*75}")
    print(f"FULL TASK LOG — {date_label} ({len(entries)} entries)")
    print(f"{'='*75}")

    for e in entries:
        ts = e.get("timestamp", "")[:16].replace("T", " ")
        task_type = e.get("task_type", "other")
        label = TASK_LABELS.get(task_type, task_type)
        desc = e.get("description", "")[:40]
        cost = e.get("cost_usd", 0)
        calls = e.get("calls", 0)
        out_tok = e.get("output_tokens", 0)
        status = "✅" if e.get("status") == "ok" else "❌"

        print(f"{status} {ts} | {label:<22} | ${cost:.4f} | {calls:>3} calls | "
              f"{out_tok:>6} out | {desc}")

    total = sum(e.get("cost_usd", 0) for e in entries)
    print(f"{'='*75}")
    print(f"TOTAL: ${total:.4f} across {len(entries)} tasks\n")


def format_daily_breakdown(entries):
    """Group by date then by task type."""
    by_date = defaultdict(list)
    for e in entries:
        date = e.get("date", e.get("timestamp", "")[:10])
        by_date[date].append(e)

    for date in sorted(by_date.keys()):
        day_entries = by_date[date]
        agg = aggregate_by_type(day_entries)
        day_cost = sum(v["cost"] for v in agg.values())
        day_tasks = sum(v["count"] for v in agg.values())
        print(f"\n📅 {date} — {day_tasks} tasks | ${day_cost:.4f}")
        for task_type, data in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
            label = TASK_LABELS.get(task_type, task_type)
            avg = data["cost"] / data["count"] if data["count"] else 0
            print(f"   {label:<26} {data['count']}x | ${data['cost']:.4f} | ${avg:.4f}/task")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Per-task cost report")
    parser.add_argument("--days", type=int, default=1, help="Last N days (default: 1 = today)")
    parser.add_argument("--date", type=str, help="Specific date YYYY-MM-DD")
    parser.add_argument("--format", choices=["brief", "summary", "full", "daily"],
                        default="summary", help="Output format")
    args = parser.parse_args()

    date_strings = get_date_strings(days=args.days, date=args.date)
    entries = load_entries(date_strings)

    if len(date_strings) == 1:
        date_label = date_strings[0]
    else:
        date_label = f"{date_strings[-1]} to {date_strings[0]}"

    if args.format == "brief":
        format_brief(entries, date_label)
    elif args.format == "full":
        format_full(entries, date_label)
    elif args.format == "daily":
        format_daily_breakdown(entries)
    else:
        format_summary(entries, date_label)
