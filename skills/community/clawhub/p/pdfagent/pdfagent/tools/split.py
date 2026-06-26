from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter


@dataclass(frozen=True)
class PageRange:
    start: int
    end: int


def split_every(input_path: Path, output_dir: Path, every: int) -> list[Path]:
    if every <= 0:
        raise ValueError("--every must be >= 1")

    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    outputs: list[Path] = []

    for i in range(0, total_pages, every):
        writer = PdfWriter()
        for page_index in range(i, min(i + every, total_pages)):
            writer.add_page(reader.pages[page_index])
        out_path = output_dir / f"{input_path.stem}_part_{i + 1}-{min(i + every, total_pages)}.pdf"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            writer.write(f)
        outputs.append(out_path)

    return outputs


def split_ranges(input_path: Path, output_dir: Path, ranges_spec: str) -> list[Path]:
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    ranges = _parse_ranges(ranges_spec, total_pages)
    outputs: list[Path] = []

    for r in ranges:
        writer = PdfWriter()
        for page_index in range(r.start - 1, r.end):
            writer.add_page(reader.pages[page_index])
        out_path = output_dir / f"{input_path.stem}_pages_{r.start}-{r.end}.pdf"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            writer.write(f)
        outputs.append(out_path)

    return outputs


def _parse_ranges(spec: str, total_pages: int) -> list[PageRange]:
    ranges: list[PageRange] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
        else:
            start = end = int(part)
        if start < 1 or end < 1 or start > total_pages or end > total_pages:
            raise ValueError(f"Page range out of bounds: {start}-{end} of {total_pages}")
        if end < start:
            raise ValueError(f"Invalid page range: {start}-{end}")
        ranges.append(PageRange(start, end))
    if not ranges:
        raise ValueError("No valid ranges provided")
    return ranges
