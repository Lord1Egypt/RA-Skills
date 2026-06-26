#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_plans

def main():
    data = load_plans()
    plans = [p for p in data.get("plans", {}).values() if p.get("status") == "active"]

    if not plans:
        print("No active plans right now.")
        return

    print("Active planning view:")
    for plan in plans[:5]:
        print(f"- {plan['id']} | {plan['goal']} | type={plan['type']}")
        if plan.get("next_steps"):
            print(f"  next: {plan['next_steps'][0]}")
        elif plan.get("phases"):
            print(f"  phase: {plan['phases'][0]}")

if __name__ == "__main__":
    main()
