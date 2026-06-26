#!/usr/bin/env python3
"""CLI for MMOutput multi-modal output generation."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .converter import MMOutputGenerator


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Convert HTML to PDF, PNG, or DOCX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.html --format pdf --output poster.pdf
  %(prog)s input.html --format png --output poster.png --full-page
  %(prog)s input.html --format all --output-dir ./outputs/
        """
    )

    parser.add_argument("input", nargs="+", help="Input HTML file(s)")
    parser.add_argument("--format", "-f", choices=["pdf", "png", "docx", "pptx", "all"], default="all", help="Output format (default: all)")
    parser.add_argument("--output", "-o", help="Output path (single input, single format)")
    parser.add_argument("--output-dir", "-d", default="./mm_outputs", help="Output directory (default: ./mm_outputs)")
    parser.add_argument("--page-size", default="A4", choices=["A4", "Letter", "Legal", "A3", "A5"], help="PDF page size (default: A4)")
    parser.add_argument("--landscape", action="store_true", help="PDF landscape orientation")
    parser.add_argument("--margin", default="1cm", help="PDF margins (default: 1cm)")
    parser.add_argument("--full-page", action="store_true", default=True, help="PNG full page capture (default: True)")
    parser.add_argument("--viewport-width", type=int, default=1200, help="PNG viewport width (default: 1200)")
    parser.add_argument("--viewport-height", type=int, default=1600, help="PNG viewport height (default: 1600)")
    parser.add_argument("--no-images", action="store_true", help="Exclude images from DOCX")
    parser.add_argument("--chrome-path", help="Chrome/Chromium executable path")

    args = parser.parse_args()

    # Validate inputs
    inputs = [Path(f) for f in args.input]
    for f in inputs:
        if not f.exists():
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)
        if f.suffix.lower() != ".html":
            print(f"Warning: Not an HTML file: {f}", file=sys.stderr)

    # Determine formats
    formats = ["pdf", "png", "docx", "pptx"] if args.format == "all" else [args.format]

    # Setup output
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.output and len(inputs) == 1 and args.format != "all":
        # Single file + single format + explicit output
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        gen = MMOutputGenerator(chrome_path=args.chrome_path)

        if args.format == "pdf":
            margin = {k: args.margin for k in ["top", "right", "bottom", "left"]}
            result = gen.html_to_pdf(inputs[0], out, page_size=args.page_size, margin=margin, landscape=args.landscape)
        elif args.format == "png":
            result = gen.html_to_png(inputs[0], out, full_page=args.full_page, viewport_size=(args.viewport_width, args.viewport_height))
        elif args.format == "docx":
            result = gen.html_to_docx(inputs[0], out, include_images=not args.no_images)
        elif args.format == "pptx":
            result = gen.html_to_pptx(inputs[0], out)

        gen._close_browser()
        print(f"\nDone: {result}")
        return

    # Batch mode
    gen = MMOutputGenerator(chrome_path=args.chrome_path)
    results = []
    for f in inputs:
        print(f"\nProcessing: {f}")
        result = gen.convert_all(f, output_dir, formats=formats)
        results.append((f.name, result))

    gen._close_browser()

    # Print summary
    print("\n" + "=" * 40 + "\nSummary\n" + "=" * 40)
    for name, result in results:
        print(f"\n{name}:")
        for fmt, path in result.items():
            print(f"  {fmt.upper()}: {path}")


if __name__ == "__main__":
    main()
