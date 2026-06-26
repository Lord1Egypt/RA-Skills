from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ..core.ranges import parse_page_ranges


def rotate_pdf(input_path: Path, output_path: Path, degrees: int, pages: str | None = None) -> None:
    if degrees % 90 != 0:
        raise ValueError("Degrees must be a multiple of 90")

    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    total_pages = len(reader.pages)
    page_indices = _parse_page_indices(pages, total_pages)

    for idx, page in enumerate(reader.pages):
        if idx in page_indices:
            page.rotate(degrees)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)


def _parse_page_indices(spec: str | None, total_pages: int) -> set[int]:
    return set(parse_page_ranges(spec, total_pages))
