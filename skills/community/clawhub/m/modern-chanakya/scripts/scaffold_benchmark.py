#!/usr/bin/env python3
"""Generate a ready-to-fill Modern Chanakya benchmark markdown block."""

from __future__ import annotations

import argparse
import re
import sys


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "benchmark"


def build_markdown(title: str, situation: str, prompt: str, hidden_constraint: str) -> str:
    return f"""# {title}\n\n## Situation\n{situation}\n\n## Hidden constraint\n{hidden_constraint}\n\n## Good answer should include\n- \n- \n- \n\n## Failure modes\n- \n- \n- \n\n## User prompt\n\"{prompt}\"\n\n## Without-skill baseline summary\n- tone:\n- likely weakness:\n- missing tradeoff:\n\n## With-skill target summary\n- better diagnosis:\n- sharper recommendation:\n- clearer risk view:\n\n## Scores\n| Category | Without skill | With skill | Notes |\n|---|---:|---:|---|\n| Problem diagnosis |  |  |  |\n| Strategic depth |  |  |  |\n| Practicality |  |  |  |\n| Ethical balance |  |  |  |\n| User clarity |  |  |  |\n| Emotional intelligence |  |  |  |\n| Foresight / risk awareness |  |  |  |\n| Real-world usefulness |  |  |  |\n| **Total** |  |  |  |\n\n## Decision\n\n"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Benchmark title")
    parser.add_argument("--situation", default="<describe the situation>")
    parser.add_argument("--prompt", default="<realistic user prompt>")
    parser.add_argument(
        "--hidden-constraint",
        default="<weak leverage / timing / emotional overload / no buffer / unclear objective / reputation damage>",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of suggesting a filename",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    markdown = build_markdown(args.title, args.situation, args.prompt, args.hidden_constraint)
    if args.stdout:
        sys.stdout.write(markdown)
        return 0

    filename = f"{slugify(args.title)}.md"
    sys.stdout.write(filename + "\n\n" + markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
