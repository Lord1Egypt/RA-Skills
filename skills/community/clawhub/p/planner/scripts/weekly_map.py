#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_plans

def main():
    data = load_plans()
    plans = list(data.get("plans", {}).values())

    if not plans:
        print("No plans captured yet.")
        return

    print("Weekly planning map:")
    grouped = {}
    for plan in plans:
        grouped.setdefault(plan["type"], []).append(plan)

    for plan_type, items in grouped.items():
        print(f"\n[{plan_type}]")
        for plan in items[:10]:
            print(f"- {plan['id']} | {plan['goal']} | status={plan['status']}")

if __name__ == "__main__":
    main()
