#!/usr/bin/env python3
"""pdf_to_images.py

Convert a PDF into per-page PNG images.

Requirements:
  python -m pip install pymupdf

Usage:
  python pdf_to_images.py input.pdf out_dir --dpi 200
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF


def convert(pdf_path: Path, out_dir: Path, dpi: int = 200, fmt: str = "png", page_range: str | None = None) -> list[int]:
    """Convert PDF pages to images. Returns list of exported page numbers (1-indexed)."""
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    fmt = fmt.lower().lstrip(".")
    if fmt not in {"png", "jpg", "jpeg"}:
        raise ValueError(f"Unsupported --fmt: {fmt}. Use png/jpg/jpeg.")

    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    try:
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        # Parse page range (e.g. "1-3,5,7-9")
        selected: set[int] | None = None
        if page_range:
            selected = set()
            for part in page_range.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = part.split("-", 1)
                    selected.update(range(int(start), int(end) + 1))
                else:
                    selected.add(int(part))

        exported = []
        for i in range(doc.page_count):
            page_num = i + 1  # 1-indexed
            if selected is not None and page_num not in selected:
                continue
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            ext = "jpg" if fmt == "jpeg" else fmt
            out_path = out_dir / f"page_{page_num:02d}.{ext}"
            pix.save(str(out_path))
            print(f"saved {out_path}")
            exported.append(page_num)

        print(f"done: exported {len(exported)} pages -> {out_dir}")
        return exported
    finally:
        doc.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path, help="Input PDF path")
    ap.add_argument("out_dir", type=Path, help="Output directory")
    ap.add_argument("--dpi", type=int, default=200, help="Render DPI (default: 200)")
    ap.add_argument("--fmt", default="png", choices=["png", "jpg", "jpeg"], help="Output image format (default: png)")
    ap.add_argument("--pages", help="Page range, e.g. 1-3,5 (default: all pages)")
    args = ap.parse_args()

    convert(args.pdf, args.out_dir, dpi=args.dpi, fmt=args.fmt, page_range=args.pages)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
