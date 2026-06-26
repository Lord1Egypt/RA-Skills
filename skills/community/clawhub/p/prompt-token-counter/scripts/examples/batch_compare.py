#!/usr/bin/env python3
"""
Compare token counts across multiple models for local file(s).
Run from project root:
  python scripts/examples/batch_compare.py file1.txt file2.txt
  python scripts/examples/batch_compare.py -f input.txt -m gpt-4 claude-3-opus
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
        description="Compare token counts across models for local file(s)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        metavar="FILE",
        help="Local file path(s) to compare",
    )
    parser.add_argument(
        "-f", "--file",
        action="append",
        dest="files",
        help="Read from file (repeatable)",
    )
    parser.add_argument(
        "-m", "--models",
        nargs="*",
        default=["gpt-4", "claude-3-opus", "gemini-pro"],
        help="Model names (default: gpt-4 claude-3-opus gemini-pro)",
    )
    args = parser.parse_args()

    paths = list(args.paths or [])
    if args.files:
        paths.extend(args.files)

    if not paths:
        parser.error("Provide at least one local file path")

    models = args.models or ["gpt-4", "claude-3-opus", "gemini-pro"]

    print(f"Files: {paths}")
    print(f"Models: {models}")
    print("---")

    for path_str in paths:
        path = Path(path_str)
        if not path.exists():
            print(f"Error: File '{path}' not found", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        print(f"\n{path_str}:")
        for model in models:
            try:
                tokens = TokenCounter(model).count(text)
                print(f"  {model}: tokens={tokens}")
            except (UnsupportedModelError, TokenizationError) as e:
                print(f"  {model}: Error - {e}")


if __name__ == "__main__":
    main()
