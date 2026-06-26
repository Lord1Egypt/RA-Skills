#!/usr/bin/env python3
"""Render meeting minutes from template with provided values."""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "template.md"

def render(template: str, values: dict) -> str:
    def replacer(match):
        key = match.group(1)
        return values.get(key, match.group(0))
    return re.sub(r'\{\{(\w+)\}\}', replacer, template)

def main():
    parser = argparse.ArgumentParser(description="Render meeting minutes template")
    parser.add_argument("--values", help="JSON string or path to JSON file with template values")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    template = TEMPLATE_PATH.read_text()

    if args.values:
        p = Path(args.values) if len(args.values) < 255 else None
        if p and p.exists():
            values = json.loads(p.read_text())
        else:
            values = json.loads(args.values)
    else:
        values = {}

    # Defaults
    values.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
    values.setdefault("title", "Team Sync")
    values.setdefault("attendees", "TBD")
    values.setdefault("type", "planning")
    values.setdefault("facilitator", "TBD")
    values.setdefault("duration", "TBD")

    result = render(template, values)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Written to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
