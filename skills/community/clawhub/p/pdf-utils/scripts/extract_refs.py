#!/usr/bin/env python3
"""
Extract arXiv references from a PDF and optionally download all papers.

Usage:
  python3 extract_refs.py <pdf_file>                     # extract IDs only
  python3 extract_refs.py <pdf_file> --download          # extract + download
  python3 extract_refs.py <pdf_file> --download --out ~/papers/
  python3 extract_refs.py <pdf_file> --list              # show all references nicely
  python3 extract_refs.py <pdf_file> --refpages          # show which pages contain references
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Optional

import fitz

from scripts.arxiv_utils import extract_arxiv_ids_from_text

REFERENCE_PATTERNS = ("参考文献", "References", "REFERENCES")
ENTRY_SPLIT_PATTERN = re.compile(
    r"(?=\n\s*(?:\[\d+\]|\d+\.|\(\d+\)))|(?=\n\s*(?:\[[A-Za-z]\d{2,}\]))"
)


def extract_arxiv_ids(filepath: str) -> list[str]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF not found: {filepath}")

    try:
        doc = fitz.open(filepath)
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot open PDF (possibly corrupt): {filepath}") from e

    try:
        full_text = "\n".join(p.get_text() for p in doc)
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot read text from PDF: {filepath}") from e
    finally:
        doc.close()

    return extract_arxiv_ids_from_text(full_text)


def extract_reference_section(filepath: str) -> tuple[Optional[str], int]:
    try:
        doc = fitz.open(filepath)
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot open PDF: {filepath}") from e

    try:
        for i, page in enumerate(doc):
            try:
                text = page.get_text()
            except fitz.FitzError:
                continue
            for pattern in REFERENCE_PATTERNS:
                idx = text.find(pattern)
                if idx != -1:
                    return text[idx:], i
    finally:
        doc.close()
    return None, -1


def refpages(filepath: str) -> list[int]:
    try:
        doc = fitz.open(filepath)
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot open PDF: {filepath}") from e

    results: list[int] = []
    try:
        for i, page in enumerate(doc):
            try:
                text = page.get_text()
            except fitz.FitzError:
                continue
            if any(pattern in text for pattern in REFERENCE_PATTERNS):
                results.append(i + 1)
    finally:
        doc.close()
    return results


def download_papers(
    arxiv_ids: list[str],
    out_dir: str = "papers",
    size_limit_kb: float = 50,
    timeout: int = 60,
) -> dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    results: dict[str, str] = {}

    for i, aid in enumerate(arxiv_ids, 1):
        out_path = os.path.join(out_dir, f"{aid}.pdf")

        if os.path.exists(out_path):
            size = os.path.getsize(out_path) / 1024
            if size > size_limit_kb:
                print(f"  [{i:02d}/{len(arxiv_ids)}] skip   {aid} ({size:.0f}KB exists)")
                results[aid] = "skip"
                continue
            os.remove(out_path)

        url = f"https://arxiv.org/pdf/{aid}"
        print(f"  [{i:02d}/{len(arxiv_ids)}] download {aid}...", end=" ", flush=True)

        try:
            result = subprocess.run(
                ["curl", "-sL", url, "-o", out_path, "-m", str(timeout)],
                capture_output=True,
                timeout=timeout + 5,
            )
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            results[aid] = "fail"
            if os.path.exists(out_path):
                os.remove(out_path)
            continue

        if result.returncode != 0:
            print("CURL_ERROR")
            results[aid] = "fail"
            if os.path.exists(out_path):
                os.remove(out_path)
            continue

        size = os.path.getsize(out_path) / 1024 if os.path.exists(out_path) else 0
        if size > size_limit_kb:
            print(f"{size:.0f}KB")
            results[aid] = "ok"
        else:
            print(f"TOO_SMALL ({size:.0f}KB)")
            results[aid] = "fail"
            if os.path.exists(out_path):
                os.remove(out_path)

    return results


def split_reference_entries(ref_text: str) -> list[str]:
    parts = [part.strip() for part in ENTRY_SPLIT_PATTERN.split(ref_text) if part.strip()]
    if len(parts) <= 1:
        return [ref_text.strip()] if ref_text.strip() else []
    return parts[1:] if any(p in parts[0] for p in REFERENCE_PATTERNS) else parts


def list_refs(filepath: str, max_entries: int = 30) -> None:
    try:
        doc = fitz.open(filepath)
    except fitz.FitzError as e:
        raise RuntimeError(f"Cannot open PDF: {filepath}") from e

    try:
        full_text = "\n".join(p.get_text() for p in doc)
    finally:
        doc.close()

    ref_text = None
    for pattern in REFERENCE_PATTERNS:
        idx = full_text.find(pattern)
        if idx != -1:
            ref_text = full_text[idx:]
            break

    if not ref_text:
        print("No references section found.")
        return

    entries = split_reference_entries(ref_text)
    shown = 0
    for entry in entries:
        if shown >= max_entries:
            print(f"\n{'=' * 60}\n  ... ({len(entries) - max_entries} more references)")
            break
        ids = extract_arxiv_ids_from_text(entry)
        arxiv_link = f"https://arxiv.org/abs/{ids[0]}" if ids else ""
        first_line = entry.split("\n")[0].strip()
        print(f"\n{'=' * 60}\n{first_line}")
        if arxiv_link:
            print(f"  -> {arxiv_link}")
        shown += 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract arXiv references from a PDF and optionally download papers."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--download", action="store_true", help="Download all referenced papers")
    parser.add_argument("--out", default="papers", help="Output directory (default: papers/)")
    parser.add_argument("--list", action="store_true", help="List all references in readable format")
    parser.add_argument("--refpages", action="store_true", help="Show which pages contain references")
    parser.add_argument("--timeout", type=int, default=60, help="Download timeout per paper (default: 60s)")
    args = parser.parse_args()

    pdf_file = os.path.expanduser(args.pdf_file)
    if not os.path.exists(pdf_file):
        print(f"Error: File not found: {pdf_file}", file=sys.stderr)
        sys.exit(1)

    print(f"File: {pdf_file}")
    try:
        doc = fitz.open(pdf_file)
        print(f"Pages: {doc.page_count}")
        doc.close()
    except fitz.FitzError as e:
        print(f"Error: Cannot open PDF: {e}", file=sys.stderr)
        sys.exit(1)

    if args.refpages:
        pages = refpages(pdf_file)
        print(f"\nReference section on pages: {pages}")
        return

    if args.list:
        print("\nListing all references...\n")
        list_refs(pdf_file)
        return

    try:
        ids = extract_arxiv_ids(pdf_file)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not ids:
        print("\nNo arXiv IDs found.")
        sys.exit(0)

    print(f"\nFound {len(ids)} arXiv ID(s):")
    for i, aid in enumerate(ids, 1):
        print(f"  {i:02d}. https://arxiv.org/abs/{aid}")

    if args.download:
        print(f"\nDownloading to {args.out}/ ...")
        out_dir = os.path.expanduser(args.out)
        results = download_papers(ids, out_dir, timeout=args.timeout)
        ok = sum(1 for v in results.values() if v == "ok")
        skip = sum(1 for v in results.values() if v == "skip")
        fail = sum(1 for v in results.values() if v == "fail")
        print(f"\nDone — ok: {ok}, skipped: {skip}, failed: {fail}")


if __name__ == "__main__":
    main()
