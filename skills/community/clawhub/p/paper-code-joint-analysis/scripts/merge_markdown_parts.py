#!/usr/bin/env python3
"""Merge chunked Markdown parts into one stable reader-facing Markdown file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_part_names(parts_dir: Path) -> list[str]:
    manifest = parts_dir / "manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        parts = data.get("parts")
        if not isinstance(parts, list) or not all(isinstance(x, str) for x in parts):
            raise SystemExit("manifest.json must contain a string array field named 'parts'")
        return parts
    return [path.name for path in sorted(parts_dir.glob("*.md"))]


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Markdown section chunks into a final Markdown artifact.")
    parser.add_argument("parts_dir", help="Directory containing Markdown parts and optional manifest.json")
    parser.add_argument("output", help="Output Markdown file, for example paper_reading_report.md")
    parser.add_argument("--title", default=None, help="Optional H1 title to prepend when output would not already start with one")
    args = parser.parse_args()

    parts_dir = Path(args.parts_dir).resolve()
    output = Path(args.output).resolve()
    if not parts_dir.exists():
        raise SystemExit(f"parts_dir does not exist: {parts_dir}")
    names = load_part_names(parts_dir)
    if not names:
        raise SystemExit(f"no Markdown parts found in {parts_dir}")

    chunks: list[str] = []
    for name in names:
        path = parts_dir / name
        if not path.exists():
            raise SystemExit(f"manifest references missing part: {path}")
        text = path.read_text(encoding="utf-8").strip()
        if text:
            chunks.append(text)

    merged = "\n\n".join(chunks).strip() + "\n"
    if args.title and not merged.lstrip().startswith("# "):
        merged = f"# {args.title}\n\n{merged}"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(merged, encoding="utf-8")
    print(f"merged {len(chunks)} parts -> {output} ({len(merged)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
