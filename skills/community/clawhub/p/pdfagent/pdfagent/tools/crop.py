from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ..core.ranges import parse_page_ranges


def crop_pdf(
    input_path: Path,
    output_path: Path,
    *,
    left: float,
    top: float,
    right: float,
    bottom: float,
    pages: str | None = None,
    apply_media: bool = False,
) -> None:
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    for idx, page in enumerate(reader.pages):
        if idx in target_pages:
            media = page.mediabox
            new_left = media.left + left
            new_bottom = media.bottom + bottom
            new_right = media.right - right
            new_top = media.top - top
            page.cropbox.lower_left = (new_left, new_bottom)
            page.cropbox.upper_right = (new_right, new_top)
            if apply_media:
                page.mediabox.lower_left = (new_left, new_bottom)
                page.mediabox.upper_right = (new_right, new_top)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)
