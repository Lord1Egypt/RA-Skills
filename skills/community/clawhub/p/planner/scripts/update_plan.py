#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_plans, save_plans

VALID_STATUS = ["active", "paused", "done", "archived"]

def parse_pipe(value):
    if not value:
        return None
    return [v.strip() for v in value.split("|") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Update a plan")
    parser.add_argument("--id", required=True, help="Plan ID")
    parser.add_argument("--status", choices=VALID_STATUS)
    parser.add_argument("--deadline")
    parser.add_argument("--phases")
    parser.add_argument("--milestones")
    parser.add_argument("--next_steps")
    parser.add_argument("--notes")
    args = parser.parse_args()

    data = load_plans()
    plans = data.get("plans", {})

    if args.id not in plans:
        print(f"Plan not found: {args.id}")
        sys.exit(1)

    plan = plans[args.id]

    if args.status:
        plan["status"] = args.status
    if args.deadline is not None:
        plan["deadline"] = args.deadline
    if args.phases is not None:
        plan["phases"] = parse_pipe(args.phases)
    if args.milestones is not None:
        plan["milestones"] = parse_pipe(args.milestones)
    if args.next_steps is not None:
        plan["next_steps"] = parse_pipe(args.next_steps)
    if args.notes is not None:
        plan["notes"] = args.notes

    plan["updated_at"] = datetime.now().isoformat()
    save_plans(data)

    print(f"✓ Updated {args.id}")
    print(f"  Status: {plan['status']}")

if __name__ == "__main__":
    main()
