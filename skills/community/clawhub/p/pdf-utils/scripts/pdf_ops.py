#!/usr/bin/env python3
"""Utility PDF operations with PyMuPDF: merge, split, render."""
from __future__ import annotations

import argparse
import os
import sys

import fitz


def merge_pdfs(paths: list[str], out: str) -> None:
    merged = fitz.open()
    try:
        for path in paths:
            src = fitz.open(path)
            try:
                merged.insert_pdf(src)
            finally:
                src.close()
        merged.save(out)
    finally:
        merged.close()


def split_pdf(src: str, start: int, end: int, out: str) -> None:
    doc = fitz.open(src)
    part = fitz.open()
    try:
        if start < 1 or end < start or end > doc.page_count:
            raise ValueError(f"invalid page range {start}-{end}; PDF has {doc.page_count} pages")
        part.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
        part.save(out)
    finally:
        doc.close()
        part.close()


def page_to_image(src: str, page: int, scale: float, out: str) -> None:
    doc = fitz.open(src)
    try:
        if page < 1 or page > doc.page_count:
            raise ValueError(f"invalid page {page}; PDF has {doc.page_count} pages")
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(scale, scale)).save(out)
    finally:
        doc.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Utility PDF operations with PyMuPDF.")
    sub = parser.add_subparsers(dest="command", required=True)

    merge = sub.add_parser("merge", help="Merge multiple PDFs into one")
    merge.add_argument("inputs", nargs="+", help="Input PDF files")
    merge.add_argument("--out", required=True, help="Output PDF path")

    split = sub.add_parser("split", help="Split an inclusive page range into a new PDF")
    split.add_argument("input", help="Input PDF file")
    split.add_argument("--start", type=int, required=True, help="Start page (1-indexed)")
    split.add_argument("--end", type=int, required=True, help="End page (1-indexed, inclusive)")
    split.add_argument("--out", required=True, help="Output PDF path")

    render = sub.add_parser("render", help="Render one PDF page to an image")
    render.add_argument("input", help="Input PDF file")
    render.add_argument("--page", type=int, default=1, help="Page number (1-indexed)")
    render.add_argument("--scale", type=float, default=2.0, help="Render scale")
    render.add_argument("--out", required=True, help="Output image path")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        if args.command == "merge":
            inputs = [os.path.expanduser(path) for path in args.inputs]
            missing = [path for path in inputs if not os.path.exists(path)]
            if missing:
                raise FileNotFoundError(f"missing input file(s): {', '.join(missing)}")
            merge_pdfs(inputs, os.path.expanduser(args.out))
            print(f"Merged {len(inputs)} PDF(s) -> {os.path.expanduser(args.out)}")
        elif args.command == "split":
            split_pdf(os.path.expanduser(args.input), args.start, args.end, os.path.expanduser(args.out))
            print(f"Split pages {args.start}-{args.end} -> {os.path.expanduser(args.out)}")
        elif args.command == "render":
            page_to_image(os.path.expanduser(args.input), args.page, args.scale, os.path.expanduser(args.out))
            print(f"Rendered page {args.page} -> {os.path.expanduser(args.out)}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
