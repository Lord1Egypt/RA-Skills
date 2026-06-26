#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_plans

def score_plan(plan):
    score = 0
    if plan.get("status") != "active":
        return -9999
    if plan.get("deadline"):
        score += 20
        try:
            days_left = (datetime.fromisoformat(plan["deadline"]) - datetime.now()).days
            if days_left <= 7:
                score += 25
            elif days_left <= 30:
                score += 10
        except ValueError:
            pass
    if plan.get("next_steps"):
        score += 20
    if plan.get("milestones"):
        score += 10
    if plan.get("phases"):
        score += 10
    return score

def main():
    parser = argparse.ArgumentParser(description="Suggest current planning focus")
    parser.add_argument("--type", choices=["trip", "week", "project", "launch", "decision"])
    args = parser.parse_args()

    data = load_plans()
    plans = list(data.get("plans", {}).values())

    if args.type:
        plans = [p for p in plans if p.get("type") == args.type]

    ranked = sorted(plans, key=score_plan, reverse=True)
    ranked = [p for p in ranked if score_plan(p) > 0][:3]

    if not ranked:
        print("No strong active plan stands out right now.")
        print("Capture a new plan or add next steps to an existing one.")
        return

    labels = ["Top Plan", "Backup", "Backup"]
    for idx, plan in enumerate(ranked):
        print(f"{labels[idx]} — {plan['goal']}")
        print(f"  Type: {plan['type']}")
        if plan.get("deadline"):
            print(f"  Deadline: {plan['deadline']}")
        if plan.get("next_steps"):
            print(f"  Next step: {plan['next_steps'][0]}")
        elif plan.get("phases"):
            print(f"  Current phase candidate: {plan['phases'][0]}")
        print()

if __name__ == "__main__":
    main()
