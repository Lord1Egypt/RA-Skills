#!/usr/bin/env python3
"""
OpenCC converter CLI tool.

Usage:
    python scripts/convert.py --source s2t "汉字"
    echo "汉字" | python scripts/convert.py --source s2t
    python scripts/convert.py --source s2t --input input.txt --output output.txt
"""

import argparse
import sys
import opencc


def main():
    parser = argparse.ArgumentParser(
        description="Convert Chinese text using OpenCC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Conversion modes:
  s2t   - Simplified to Traditional (OpenCC Standard)
  t2s   - Traditional to Simplified
  s2tw  - Simplified to Taiwan Standard (正體)
  tw2s  - Taiwan to Simplified
  s2hk  - Simplified to Hong Kong variant
  hk2s  - Hong Kong to Simplified
  s2twp - Simplified to Taiwan + idioms
  tw2sp - Taiwan to Simplified + idioms
  t2tw  - Traditional to Taiwan Standard
  t2hk  - Traditional to Hong Kong
  hk2t  - Hong Kong to Traditional
  t2jp  - Traditional to Japanese Kanji
  jp2t  - Japanese to Traditional
  tw2t  - Taiwan to Traditional

Examples:
  python scripts/convert.py --source s2t "汉字转换"
  echo "简体中文" | python scripts/convert.py --source s2tw
  python scripts/convert.py --source s2t --input input.txt --output output.txt
        """,
    )

    parser.add_argument(
        "-s",
        "--source",
        required=True,
        help="Conversion mode (e.g., s2t, t2s, s2tw)",
    )
    parser.add_argument("text", nargs="?", help="Text to convert (or read from stdin)")
    parser.add_argument(
        "-i",
        "--input",
        help="Input file path (overrides stdin/text argument)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Initialize converter
    try:
        converter = opencc.OpenCC(f"{args.source}.json")
    except Exception as e:
        print(f"Error: Invalid conversion mode '{args.source}'", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

    # Get input text
    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        # Read from stdin
        text = sys.stdin.read()

    # Convert
    try:
        result = converter.convert(text)
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✓ Converted text written to: {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
