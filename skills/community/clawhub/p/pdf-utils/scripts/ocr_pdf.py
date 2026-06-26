#!/usr/bin/env python3
"""
OCR for image-based PDFs using tesseract + pymupdf.

Requires:
  brew install tesseract && brew install tesseract-lang  # for Chinese + English OCR
  pip3 install pytesseract Pillow pymupdf --break-system-packages

Usage:
  python3 ocr_pdf.py <pdf_file>                     # first 5 pages
  python3 ocr_pdf.py <pdf_file> --all               # all pages
  python3 ocr_pdf.py <pdf_file> --pages 0,3-5       # specific pages (0-indexed)
  python3 ocr_pdf.py <pdf_file> --extract-refs      # OCR + extract arxiv IDs
  python3 ocr_pdf.py <pdf_file> --out text.txt      # save to file
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from typing import Optional

import fitz

from scripts.arxiv_utils import extract_arxiv_ids_from_text


def _check_tesseract(lang: str) -> None:
    """Verify tesseract binary and requested language data are available."""
    import shutil

    if not shutil.which("tesseract"):
        raise RuntimeError(
            "tesseract not found. Install with: brew install tesseract tesseract-lang"
        )

    try:
        result = subprocess.run(
            ["tesseract", "--list-langs"],
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception as e:
        raise RuntimeError(f"failed to query tesseract languages: {e}") from e

    available = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    requested = {part.strip() for part in lang.split("+") if part.strip()}
    missing = sorted(requested - available)
    if missing:
        raise RuntimeError(
            "missing tesseract language data: "
            + ", ".join(missing)
            + ". Install with: brew install tesseract-lang"
        )


def pdf_page_to_image(
    pdf_path: str,
    page_num: int,
    scale: float = 3.0,
    output_dir: Optional[str] = None,
) -> str:
    doc = fitz.open(pdf_path)
    try:
        if page_num >= doc.page_count:
            raise IndexError(f"Page {page_num} out of range (PDF has {doc.page_count} pages)")
        pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(scale, scale))
    finally:
        doc.close()

    fd, img_path = tempfile.mkstemp(suffix=".png", dir=output_dir)
    os.close(fd)
    pix.save(img_path)
    return img_path


def ocr_image(img_path: str, lang: str = "chi_sim+eng") -> str:
    import pytesseract

    try:
        text = pytesseract.image_to_string(img_path, lang=lang)
    except Exception as e:
        raise RuntimeError(f"tesseract OCR failed on {img_path}: {e}") from e
    return text


def ocr_pdf(
    pdf_path: str,
    pages: Optional[str | list[int]] = None,
    lang: str = "chi_sim+eng",
    scale: float = 3.0,
    progress: bool = True,
) -> str:
    _check_tesseract(lang)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        total = doc.page_count
        doc.close()
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot open PDF (possibly corrupt): {pdf_path}") from e

    if pages == "all":
        page_range = list(range(total))
    elif isinstance(pages, str):
        nums: set[int] = set()
        for part in pages.split(","):
            part = part.strip()
            if "-" in part:
                s, e = part.split("-", 1)
                nums.update(range(int(s), int(e) + 1))
            else:
                nums.add(int(part))
        page_range = sorted(nums)
    elif isinstance(pages, (list, tuple)):
        page_range = list(pages)
    else:
        page_range = list(range(min(5, total)))

    results: list[str] = []
    errors = 0

    for i in page_range:
        if i < 0 or i >= total:
            if progress:
                print(f"  [skip] page {i} (out of bounds)")
            continue

        if progress:
            print(f"  page {i + 1}/{total}...", end=" ", flush=True)

        img_path = None
        try:
            img_path = pdf_page_to_image(pdf_path, i, scale)
            text = ocr_image(img_path, lang)
            if progress:
                print(f"{len(text)} chars")
            results.append(f"=== Page {i + 1} ===\n{text}")
        except Exception as e:
            if progress:
                print(f"ERROR: {e}")
            errors += 1
        finally:
            if img_path and os.path.exists(img_path):
                os.remove(img_path)

    if errors:
        print(f"  Warning: {errors} page(s) failed OCR.", file=sys.stderr)

    return "\n\n".join(results)


def extract_arxiv_from_text(text: str) -> list[str]:
    return extract_arxiv_ids_from_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OCR image-based PDFs with tesseract + pymupdf."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--all", action="store_true", help="OCR all pages (default: first 5 pages)")
    parser.add_argument("--pages", help="Comma-separated 0-indexed page(s)/ranges, e.g. 0,3-5")
    parser.add_argument("--lang", default="chi_sim+eng", help="Tesseract language code(s), default: chi_sim+eng")
    parser.add_argument("--scale", type=float, default=3.0, help="Render resolution multiplier (higher = slower but more accurate), default: 3.0")
    parser.add_argument("--out", help="Save OCR text to this file")
    parser.add_argument("--extract-refs", action="store_true", help="After OCR, extract arXiv IDs found in the text")
    args = parser.parse_args()

    pdf_file = os.path.expanduser(args.pdf_file)
    if not os.path.exists(pdf_file):
        print(f"Not found: {pdf_file}", file=sys.stderr)
        sys.exit(1)

    print(f"File: {pdf_file}")
    try:
        doc = fitz.open(pdf_file)
        pages_total = doc.page_count
        doc.close()
        print(f"Pages: {pages_total}")
    except fitz.FitzError as e:
        print(f"Error: Cannot open PDF: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Lang: {args.lang}")

    pages: Optional[str]
    if args.all:
        pages = "all"
    elif args.pages:
        pages = args.pages
    else:
        pages = None

    try:
        text = ocr_pdf(pdf_file, pages=pages, lang=args.lang, scale=args.scale, progress=True)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.extract_refs:
        ids = extract_arxiv_from_text(text)
        if ids:
            print(f"\n{len(ids)} arXiv ID(s) found:")
            for i, aid in enumerate(ids, 1):
                print(f"  {i:02d}. https://arxiv.org/abs/{aid}")
        else:
            print("\nNo arXiv IDs found in OCR text.")
    elif args.out:
        out_path = os.path.expanduser(args.out)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved ({len(text)} chars) -> {out_path}")
    else:
        preview = text[:2000]
        tail = f"\n...+{len(text) - 2000} chars" if len(text) > 2000 else ""
        print(f"\n--- ({len(text)} chars) ---\n{preview}{tail}")


if __name__ == "__main__":
    main()
