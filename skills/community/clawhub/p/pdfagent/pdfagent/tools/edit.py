from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.utils import ImageReader

from ..core.overlay import apply_overlay
from ..core.ranges import parse_page_ranges


def add_text(
    input_path: Path,
    output_path: Path,
    *,
    text: str,
    x: float,
    y: float,
    font: str = "Helvetica",
    size: int = 12,
    pages: str | None = None,
) -> None:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    def _draw(c, page_num: int, width: float, height: float) -> None:
        if (page_num - 1) not in target_pages:
            return
        c.setFont(font, size)
        c.drawString(x, y, text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)


def add_image(
    input_path: Path,
    output_path: Path,
    *,
    image: Path,
    x: float,
    y: float,
    width: float | None = None,
    height: float | None = None,
    pages: str | None = None,
) -> None:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    def _draw(c, page_num: int, page_width: float, page_height: float) -> None:
        if (page_num - 1) not in target_pages:
            return
        img = ImageReader(str(image))
        iw, ih = img.getSize()
        w = width if width else iw
        h = height if height else ih
        c.drawImage(img, x, y, w, h)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)
