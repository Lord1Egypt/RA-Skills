#!/usr/bin/env python3
"""
Score a single piece of text for prompt-injection risk.

Usage:
  python3 scan_input.py --text "..."
  python3 scan_input.py --file path/to/input.txt
  python3 scan_input.py --text "..." --json
  python3 scan_input.py --text "..." --caution-at 30 --block-at 70
  python3 scan_input.py --text "..." --whitelist-file allow.txt

Exit codes:
  0 = safe
  1 = caution
  2 = block
  3 = error (bad arguments / I/O)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Make sibling imports work when invoked directly
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _core import (
    full_report,
    SAFE_THRESHOLD_DEFAULT,
    BLOCK_THRESHOLD_DEFAULT,
)

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def _load_whitelist(path_str: str) -> list:
    path = safe_path(path_str).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"whitelist file not found: {path}")
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Text to scan, passed inline")
    src.add_argument("--file", help="Path to a file with the text to scan")
    parser.add_argument(
        "--caution-at", type=int, default=SAFE_THRESHOLD_DEFAULT,
        help=f"Score >= this is 'caution' (default {SAFE_THRESHOLD_DEFAULT})",
    )
    parser.add_argument(
        "--block-at", type=int, default=BLOCK_THRESHOLD_DEFAULT,
        help=f"Score >= this is 'block' (default {BLOCK_THRESHOLD_DEFAULT})",
    )
    parser.add_argument(
        "--whitelist", action="append", default=[],
        help="Allow-list phrase. May be passed multiple times. "
             "If a matched fragment is contained in any whitelist entry, "
             "it is dropped before scoring.",
    )
    parser.add_argument(
        "--whitelist-file",
        help="Path to a UTF-8 file with one whitelist phrase per line "
             "(blank lines and #-comments ignored).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    args = parser.parse_args()

    if args.caution_at < 0 or args.caution_at > 100:
        print("error: --caution-at must be in 0..100", file=sys.stderr)
        return 3
    if args.block_at <= args.caution_at or args.block_at > 100:
        print("error: --block-at must be > --caution-at and <= 100", file=sys.stderr)
        return 3

    whitelist = list(args.whitelist or [])
    if args.whitelist_file:
        try:
            whitelist.extend(_load_whitelist(args.whitelist_file))
        except (ValueError, FileNotFoundError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 3

    if args.text is not None:
        text = args.text
    else:
        try:
            path = safe_path(args.file).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 3
        if not path.is_file():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 3
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="latin-1")

    report = full_report(
        text,
        caution_at=args.caution_at,
        block_at=args.block_at,
        whitelist=whitelist or None,
    )

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"risk_score: {report['risk_score']}")
        print(f"verdict: {report['verdict']}")
        print(f"thresholds: caution>={report['thresholds']['caution_at']}, block>={report['thresholds']['block_at']}")
        if report.get("combined_signal_bonus"):
            print(
                f"combined_signal_bonus: +{report['combined_signal_bonus']} "
                f"(distinct categories: {report.get('distinct_categories', 0)})"
            )
        if report["matches"]:
            print("matches:")
            for cat, items in sorted(report["matches"].items()):
                cat_score = report["category_scores"].get(cat, 0)
                print(f"  {cat} (+{cat_score}):")
                for s in items:
                    snippet = s if len(s) <= 120 else s[:117] + "..."
                    print(f"    - {snippet}")
        else:
            print("matches: (none)")
        print(f"recommendation: {report['recommendation']}")

    if report["verdict"] == "safe":
        return 0
    if report["verdict"] == "caution":
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
