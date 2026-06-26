#!/usr/bin/env python3
"""
Estimate API cost for a prompt (text or file).
Run from project root: python scripts/examples/estimate_cost.py [text_or_file] [model]
Or: python scripts/examples/estimate_cost.py input.txt gpt-4
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core import TokenCounter, estimate_cost
from scripts.exceptions import UnsupportedModelError, TokenizationError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate API cost for a prompt (text or file)"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="Your prompt text here",
        help="Text to estimate, or path to file",
    )
    parser.add_argument(
        "model",
        nargs="?",
        default="gpt-4",
        help="Model name (default: gpt-4)",
    )
    parser.add_argument(
        "-m", "--model",
        dest="model_opt",
        help="Model name (alternative to positional)",
    )
    args = parser.parse_args()

    model = args.model_opt or args.model

    if Path(args.input).is_file():
        path = Path(args.input)
        if not path.exists():
            print(f"Error: File '{path}' not found", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        print(f"Estimating cost for file: {path}")
    else:
        text = args.input
        print(f'Estimating cost for text: "{text[:50]}{"..." if len(text) > 50 else ""}"')

    try:
        tokens = TokenCounter(model).count(text)
        cost = estimate_cost(tokens, model, input_tokens=True)
        symbol = "$"
        print(f"tokens={tokens} cost={symbol}{cost:.6f}")
    except UnsupportedModelError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except TokenizationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
