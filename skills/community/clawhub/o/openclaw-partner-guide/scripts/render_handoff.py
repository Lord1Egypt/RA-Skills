#!/usr/bin/env python3
"""Render a compact partner-style handoff summary."""

import argparse

parser = argparse.ArgumentParser(description="Render compact handoff summary")
parser.add_argument("--goal", required=True)
parser.add_argument("--status", required=True)
parser.add_argument("--next", required=True)
parser.add_argument("--decisions", default="")
parser.add_argument("--blockers", default="")
args = parser.parse_args()

print("Partner Handoff Summary")
print("=======================")
print(f"Goal: {args.goal}")
print(f"Status: {args.status}")
if args.decisions:
    print(f"Key decisions: {args.decisions}")
if args.blockers:
    print(f"Blockers: {args.blockers}")
print(f"Next step: {args.next}")
