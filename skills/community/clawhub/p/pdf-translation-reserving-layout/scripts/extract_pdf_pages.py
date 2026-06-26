#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


def extract_page_text(pdf_path: Path, page_number: int) -> str:
    result = subprocess.run(
        [
            "pdftotext",
            "-layout",
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            str(pdf_path),
            "-",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract PDF pages into JSONL for agent-native translation workflows.")
    parser.add_argument("--input", required=True, help="Input PDF path")
    parser.add_argument("--output", required=True, help="Output JSONL path")
    parser.add_argument("--first-page", type=int, default=1, help="First page to extract (1-based)")
    parser.add_argument("--last-page", type=int, default=0, help="Last page to extract (1-based, default: end)")
    args = parser.parse_args()

    pdf_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        print(f"Input PDF does not exist: {pdf_path}", file=sys.stderr)
        return 1

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    first_page = max(1, args.first_page)
    last_page = args.last_page or total_pages
    last_page = min(last_page, total_pages)

    if first_page > last_page:
        print("First page must be less than or equal to last page.", file=sys.stderr)
        return 1

    with output_path.open("w", encoding="utf-8") as handle:
        for page_number in range(first_page, last_page + 1):
            text = extract_page_text(pdf_path, page_number)
            record = {
                "page": page_number,
                "text": text,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote pages {first_page}-{last_page} to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
