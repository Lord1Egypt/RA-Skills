#!/usr/bin/env python3
"""
Produce a sanitized version of risky input text. The output wraps the
original content in an UNTRUSTED_USER_CONTENT block and replaces matched
injection phrases with [[REDACTED:category]] markers, so the agent can
still read the surrounding context without executing the embedded
instructions.

Usage:
  python3 sanitize_input.py --file path/to/input.txt --output safe.txt
  python3 sanitize_input.py --text "..." --output -          # stdout
  python3 sanitize_input.py --file in.txt                    # writes <in>.safe.txt

Exit codes:
  0 = success
  3 = error
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _core import scan_text, sanitize_text

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Text to sanitize, passed inline")
    src.add_argument("--file", help="Path to a file with text to sanitize")
    parser.add_argument(
        "--output",
        default="",
        help="Output path. Use '-' for stdout. Default: '<input>.safe.txt' next to --file.",
    )
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
        default_out = "-"
    else:
        try:
            in_path = safe_path(args.file).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 3
        if not in_path.is_file():
            print(f"error: file not found: {in_path}", file=sys.stderr)
            return 3
        try:
            text = in_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = in_path.read_text(encoding="latin-1")
        default_out = str(in_path.with_suffix(in_path.suffix + ".safe.txt"))

    out_arg = args.output if args.output else default_out

    scan = scan_text(text)
    safe_body = sanitize_text(text, scan)

    if out_arg == "-":
        sys.stdout.write(safe_body)
        return 0

    try:
        out_path = safe_path(out_arg).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(safe_body, encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
