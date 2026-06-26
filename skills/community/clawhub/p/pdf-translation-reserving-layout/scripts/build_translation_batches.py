#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def flush_batch(output_dir: Path, batch_index: int, batch_pages: list[dict]) -> None:
    if not batch_pages:
        return
    output_path = output_dir / f"batch-{batch_index:03d}.json"
    payload = {
        "batch": batch_index,
        "pages": batch_pages,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Split extracted PDF page JSONL into translation batches.")
    parser.add_argument("--input", required=True, help="Input JSONL from extract_pdf_pages.py")
    parser.add_argument("--output-dir", required=True, help="Directory to write batch JSON files")
    parser.add_argument("--max-pages", type=int, default=8, help="Maximum pages per batch")
    parser.add_argument("--max-chars", type=int, default=18000, help="Maximum source characters per batch")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = [json.loads(line) for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    batch_index = 1
    batch_pages: list[dict] = []
    batch_chars = 0

    for page in pages:
        page_chars = len(page.get("text", ""))
        if batch_pages and (len(batch_pages) >= args.max_pages or batch_chars + page_chars > args.max_chars):
            flush_batch(output_dir, batch_index, batch_pages)
            batch_index += 1
            batch_pages = []
            batch_chars = 0

        batch_pages.append(page)
        batch_chars += page_chars

    flush_batch(output_dir, batch_index, batch_pages)
    total_batches = batch_index if batch_pages else batch_index - 1
    print(f"Wrote {total_batches} batch file(s) to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
