#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_plans, save_plans

VALID_TYPES = ["trip", "week", "project", "launch", "decision"]

def parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def parse_pipe(value):
    if not value:
        return []
    return [v.strip() for v in value.split("|") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Capture a new plan")
    parser.add_argument("--goal", required=True, help="Main planning goal")
    parser.add_argument("--type", choices=VALID_TYPES, default="project")
    parser.add_argument("--deadline", help="Target date YYYY-MM-DD")
    parser.add_argument("--constraints", help="Comma-separated constraints")
    parser.add_argument("--phases", help="Pipe-separated phases")
    parser.add_argument("--milestones", help="Pipe-separated milestones")
    parser.add_argument("--next_steps", help="Pipe-separated immediate next steps")
    parser.add_argument("--notes", default="", help="Additional notes")
    args = parser.parse_args()

    prefix_map = {
        "trip": "TRP",
        "week": "WKP",
        "project": "PLN",
        "launch": "LCH",
        "decision": "DSN"
    }
    plan_id = f"{prefix_map[args.type]}-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    plan = {
        "id": plan_id,
        "goal": args.goal,
        "type": args.type,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "deadline": args.deadline,
        "constraints": parse_csv(args.constraints),
        "phases": parse_pipe(args.phases),
        "milestones": parse_pipe(args.milestones),
        "next_steps": parse_pipe(args.next_steps),
        "notes": args.notes
    }

    data = load_plans()
    data["plans"][plan_id] = plan
    save_plans(data)

    print(f"✓ Plan captured: {plan_id}")
    print(f"  Goal: {args.goal}")
    print(f"  Type: {args.type}")
    if args.deadline:
        print(f"  Deadline: {args.deadline}")

if __name__ == "__main__":
    main()
