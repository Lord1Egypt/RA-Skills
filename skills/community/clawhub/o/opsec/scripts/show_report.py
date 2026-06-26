#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_reports
from lib.output import print_human_report, print_json, print_summary_only

def main():
    parser = argparse.ArgumentParser(description="Show one saved clawguard report")
    parser.add_argument("--id", required=True, help="Report ID")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--summary-only", action="store_true", help="Output only a short decision-oriented summary")
    args = parser.parse_args()

    data = load_reports()
    report = data.get("reports", {}).get(args.id)

    if not report:
        print(f"Report not found: {args.id}")
        sys.exit(1)

    if args.json:
        print_json(report)
    elif args.summary_only:
        print_summary_only(report)
    else:
        print_human_report(report)

if __name__ == "__main__":
    main()
