#!/usr/bin/env python3
"""
Generate IDENTITY.md from identity info.

Usage:
    python3 generate-identity.py --name "Pepper" --emoji "🌶️" --creature "Executive assistant" --output IDENTITY.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.templates import render_template


def generate_identity(context):
    """Generate IDENTITY.md content from identity context dict."""
    return render_template("IDENTITY.md.hbs", context)


def main():
    parser = argparse.ArgumentParser(description="Generate IDENTITY.md")
    parser.add_argument("--input", "-i", help="JSON identity file")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--name", help="Agent name")
    parser.add_argument("--emoji", help="Agent emoji")
    parser.add_argument("--creature", help="Agent description")
    parser.add_argument("--vibe", help="Vibe summary")
    parser.add_argument("--nickname", help="Agent nickname")
    parser.add_argument("--reference-image", help="Path to reference image")
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

    if args.name:
        context["name"] = args.name
    if args.emoji:
        context["emoji"] = args.emoji
    if args.creature:
        context["creature"] = args.creature
    if args.vibe:
        context["vibe"] = args.vibe
    if args.nickname:
        context["nickname"] = args.nickname
    if args.reference_image:
        context["referenceImage"] = args.reference_image

    context.setdefault("name", "Agent")
    context.setdefault("emoji", "")
    context.setdefault("creature", "AI assistant")
    context.setdefault("vibe", "Helpful and reliable")

    result = generate_identity(context)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Generated: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
