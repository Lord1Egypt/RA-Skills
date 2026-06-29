#!/usr/bin/env python3
"""Morgan Stanley Investment Deck — CLI entry point.

Usage:
    python scripts/run.py -o output/test_deck.pptx
    python scripts/run.py -o output/test_deck.pptx --lang en
    python scripts/run.py -o output/test_deck.pptx --theme classic
"""
import argparse
import os
import sys

# Ensure the scripts directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ms_investment_deck import make_deck, sample_data


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Morgan Stanley Investment Deck Generator")
    parser.add_argument("-o", "--output", default=None,
                        help="Output .pptx file path (default: output/ms_deck_<lang>.pptx)")
    parser.add_argument("--lang", default="zh", choices=["zh", "en", "bilingual"],
                        help="Language: zh (default), en, bilingual")
    parser.add_argument("--theme", default="classic",
                        help="Theme name (default: classic)")
    args = parser.parse_args(argv)

    # Determine output path
    if args.output:
        out_path = args.output
    else:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        os.makedirs(base_dir, exist_ok=True)
        out_path = os.path.join(base_dir, f"ms_deck_{args.lang}.pptx")

    # Generate deck with sample data
    data = sample_data()
    saved = make_deck(data, out_path, theme=args.theme, language=args.lang)

    # Print result
    size = os.path.getsize(saved)
    from pptx import Presentation
    total_slides = len(Presentation(saved).slides)
    print(f"[OK] {saved}  size={size:,} bytes, slides={total_slides}")


if __name__ == "__main__":
    main()
