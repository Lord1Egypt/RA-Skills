#!/usr/bin/env python3
"""
Decision History Manager
Stores and retrieves structured decision records in JSON format.

Usage:
  python decision_history.py save --title "..." --context "..." --options '["A","B"]' --frameworks '["SWOT","10/10/10"]' --analysis "..." --choice "A" --reasoning "..."
  python decision_history.py list [--limit N]
  python decision_history.py view --id <decision_id>
  python decision_history.py update --id <decision_id> --outcome "..." --satisfaction <1-10> --reflection "..."
  python decision_history.py patterns
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".decision-advisor" / "data"
HISTORY_FILE = DATA_DIR / "decision_history.json"


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"decisions": []}


def save_history(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_id(decisions):
    return f"d{len(decisions) + 1:04d}"


def cmd_save(args):
    history = load_history()
    decision_id = generate_id(history["decisions"])
    record = {
        "id": decision_id,
        "timestamp": datetime.now().isoformat(),
        "title": args.title,
        "context": args.context,
        "options": json.loads(args.options) if args.options else [],
        "frameworks_used": json.loads(args.frameworks) if args.frameworks else [],
        "analysis_summary": args.analysis or "",
        "choice": args.choice,
        "reasoning": args.reasoning or "",
        "values_weights": json.loads(args.values_weights) if args.values_weights else {},
        "scores": json.loads(args.scores) if args.scores else {},
        "outcome": None,
        "satisfaction": None,
        "reflection": None,
        "outcome_date": None,
    }
    history["decisions"].append(record)
    save_history(history)
    print(f"Decision saved: {decision_id} - {args.title}")
    print(json.dumps(record, ensure_ascii=False, indent=2))


def cmd_list(args):
    history = load_history()
    decisions = history["decisions"]
    if not decisions:
        print("No decision records found.")
        return
    limit = args.limit or len(decisions)
    for d in decisions[-limit:]:
        outcome_status = "✅ reviewed" if d.get("outcome") else "⏳ pending review"
        print(f"[{d['id']}] {d['timestamp'][:10]} | {d['title']} | chose: {d['choice']} | {outcome_status}")


def cmd_view(args):
    history = load_history()
    for d in history["decisions"]:
        if d["id"] == args.id:
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
    print(f"Decision {args.id} not found.")


def cmd_update(args):
    history = load_history()
    for d in history["decisions"]:
        if d["id"] == args.id:
            if args.outcome:
                d["outcome"] = args.outcome
            if args.satisfaction:
                d["satisfaction"] = int(args.satisfaction)
            if args.reflection:
                d["reflection"] = args.reflection
            d["outcome_date"] = datetime.now().isoformat()
            save_history(history)
            print(f"Decision {args.id} updated with outcome.")
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
    print(f"Decision {args.id} not found.")


def cmd_patterns(args):
    history = load_history()
    decisions = history["decisions"]
    if len(decisions) < 2:
        print("Need at least 2 decisions to analyze patterns.")
        return

    # Framework usage frequency
    fw_count = {}
    for d in decisions:
        for fw in d.get("frameworks_used", []):
            fw_count[fw] = fw_count.get(fw, 0) + 1

    # Satisfaction analysis
    reviewed = [d for d in decisions if d.get("satisfaction") is not None]
    avg_satisfaction = sum(d["satisfaction"] for d in reviewed) / len(reviewed) if reviewed else None

    # Values frequency
    values_count = {}
    for d in decisions:
        for v in d.get("values_weights", {}):
            values_count[v] = values_count.get(v, 0) + 1

    report = {
        "total_decisions": len(decisions),
        "reviewed_decisions": len(reviewed),
        "avg_satisfaction": round(avg_satisfaction, 1) if avg_satisfaction else "N/A",
        "most_used_frameworks": sorted(fw_count.items(), key=lambda x: -x[1])[:5],
        "recurring_values": sorted(values_count.items(), key=lambda x: -x[1])[:5],
    }

    print("=== Decision Pattern Analysis ===")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Decision History Manager")
    sub = parser.add_subparsers(dest="command")

    p_save = sub.add_parser("save")
    p_save.add_argument("--title", required=True)
    p_save.add_argument("--context", default="")
    p_save.add_argument("--options", default="[]")
    p_save.add_argument("--frameworks", default="[]")
    p_save.add_argument("--analysis", default="")
    p_save.add_argument("--choice", required=True)
    p_save.add_argument("--reasoning", default="")
    p_save.add_argument("--values-weights", default="{}")
    p_save.add_argument("--scores", default="{}")

    p_list = sub.add_parser("list")
    p_list.add_argument("--limit", type=int, default=None)

    p_view = sub.add_parser("view")
    p_view.add_argument("--id", required=True)

    p_update = sub.add_parser("update")
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--outcome", default=None)
    p_update.add_argument("--satisfaction", default=None)
    p_update.add_argument("--reflection", default=None)

    sub.add_parser("patterns")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {"save": cmd_save, "list": cmd_list, "view": cmd_view, "update": cmd_update, "patterns": cmd_patterns}[args.command](args)


if __name__ == "__main__":
    main()
