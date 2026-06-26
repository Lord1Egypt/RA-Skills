#!/usr/bin/env python3
"""Rank analyzed podcast episodes into final recommendations."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List

from utils.tts_output import format_markdown_briefing, format_tts_briefing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank analyzed podcast episodes")
    parser.add_argument(
        "--analyses",
        type=str,
        help="Path to analyses JSON or raw JSON string",
    )
    parser.add_argument("--top", type=int, default=5, help="Return top N items")
    parser.add_argument(
        "--output",
        choices=["json", "markdown", "tts"],
        default="markdown",
        help="Output format",
    )
    return parser.parse_args()


def load_payload(value: str) -> List[Any]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        with open(value, "r") as handle:
            payload = json.load(handle)

    if isinstance(payload, list):
        return payload
    return [payload]


def main() -> None:
    args = parse_args()
    if args.analyses:
        analyses = load_payload(args.analyses)
    else:
        data = json.load(sys.stdin)
        analyses = data if isinstance(data, list) else [data]

    analyses.sort(key=lambda item: item.get("worth_your_time_score", 0.0), reverse=True)
    analyses = analyses[: args.top]

    if args.output == "json":
        print(json.dumps(analyses, indent=2))
        return
    if args.output == "tts":
        print(format_tts_briefing(analyses, args.top))
        return
    print(format_markdown_briefing(analyses, args.top))


if __name__ == "__main__":
    main()
