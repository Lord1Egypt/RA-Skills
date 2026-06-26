#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from lib.engine import load_rules, scan_skill
from lib.output import print_human_report, print_json, print_summary_only
from lib.storage import ensure_storage, save_report

def main():
    parser = argparse.ArgumentParser(description="Review a third-party skill for risky patterns")
    parser.add_argument("--skill-path", required=True, help="Path to the local skill directory")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable report")
    parser.add_argument("--summary-only", action="store_true", help="Output only a short decision-oriented summary")
    parser.add_argument("--note", default="", help="Attach a short human review note to the saved report")
    args = parser.parse_args()

    if not os.path.isdir(args.skill_path):
        print(f"Skill path not found: {args.skill_path}")
        sys.exit(1)

    ensure_storage()
    rules_path = os.path.join(ROOT_DIR, "rules", "skill_review.json")
    rules = load_rules(rules_path)
    report = scan_skill(args.skill_path, rules)

    if args.note:
        report["note"] = args.note

    save_report(report)

    if args.json:
        print_json(report)
    elif args.summary_only:
        print_summary_only(report)
    else:
        print_human_report(report)

if __name__ == "__main__":
    main()
