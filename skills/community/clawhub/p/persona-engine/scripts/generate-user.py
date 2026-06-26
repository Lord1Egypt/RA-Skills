#!/usr/bin/env python3
"""
Generate USER.md from user context.

Usage:
    python3 generate-user.py --name "Chance" --call-names "Chance, babe" --timezone "America/New_York" --output USER.md
    echo '{"userName":"Chance",...}' | python3 generate-user.py --output USER.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.templates import render_template


def generate_user(context):
    """Generate USER.md content from user context dict."""
    return render_template("USER.md.hbs", context)


def main():
    parser = argparse.ArgumentParser(description="Generate USER.md")
    parser.add_argument("--input", "-i", help="JSON user context file")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--name", help="User's name")
    parser.add_argument("--call-names", help="What the agent should call the user")
    parser.add_argument("--pronouns", help="User's pronouns")
    parser.add_argument("--timezone", help="User's timezone", default="UTC")
    parser.add_argument("--notes", help="Additional notes")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            context = json.load(f)
    elif args.name:
        context = {}
    elif not sys.stdin.isatty():
        try:
            context = json.load(sys.stdin)
        except json.JSONDecodeError:
            context = {}
    else:
        context = {}

    # Override with CLI args
    if args.name:
        context["userName"] = args.name
    if args.call_names:
        context["callNames"] = args.call_names
    if args.pronouns:
        context["pronouns"] = args.pronouns
    if args.timezone:
        context["timezone"] = args.timezone
    if args.notes:
        context["userNotes"] = args.notes

    # Defaults
    context.setdefault("userName", "User")
    context.setdefault("callNames", context["userName"])
    context.setdefault("timezone", "UTC")

    result = generate_user(context)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Generated: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
