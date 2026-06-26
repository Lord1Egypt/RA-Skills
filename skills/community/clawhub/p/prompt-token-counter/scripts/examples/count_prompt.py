#!/usr/bin/env python3
"""
Count tokens for local file(s). Default: read from local files, batch mode.
Run from project root:
  python scripts/examples/count_prompt.py file1.txt file2.txt -m gpt-4
  python scripts/examples/count_prompt.py -f input.txt -m gpt-4
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core import TokenCounter
from scripts.exceptions import UnsupportedModelError, TokenizationError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count tokens for local file(s), batch mode"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        metavar="FILE",
        help="Local file path(s) to count (default input)",
    )
    parser.add_argument(
        "-f", "--file",
        action="append",
        dest="files",
        help="Read from file (repeatable)",
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-4",
        help="Model name (default: gpt-4)",
    )
    args = parser.parse_args()

    paths = list(args.paths or [])
    if args.files:
        paths.extend(args.files)

    if not paths:
        parser.error("Provide at least one local file path")

    model = args.model
    print(f"Model: {model}")
    print("---")

    try:
        counter = TokenCounter(model)
        for p in paths:
            path = Path(p)
            if not path.exists():
                print(f"Error: File '{path}' not found", file=sys.stderr)
                sys.exit(1)
            text = path.read_text(encoding="utf-8")
            tokens = counter.count(text)
            print(f"{p}: tokens={tokens}")
    except UnsupportedModelError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except TokenizationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
