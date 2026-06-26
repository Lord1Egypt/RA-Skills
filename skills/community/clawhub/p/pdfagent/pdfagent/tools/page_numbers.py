from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from ..core.overlay import apply_overlay
from ..core.ranges import parse_page_ranges


def add_page_numbers(
    input_path: Path,
    output_path: Path,
    *,
    start: int = 1,
    position: str = "bottom-center",
    font: str = "Helvetica",
    size: int = 11,
    color: tuple[float, float, float] = (0, 0, 0),
    pages: str | None = None,
) -> None:
    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    def _draw(c, page_num: int, width: float, height: float) -> None:
        idx = page_num - 1
        if idx not in target_pages:
            return
        c.setFillColorRGB(*color)
        c.setFont(font, size)
        num = start + idx
        x, y = _position_xy(position, width, height)
        c.drawCentredString(x, y, str(num))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)


def _position_xy(position: str, width: float, height: float) -> tuple[float, float]:
    pos = position.lower()
    if pos == "top-left":
        return (width * 0.1, height * 0.9)
    if pos == "top-right":
        return (width * 0.9, height * 0.9)
    if pos == "bottom-left":
        return (width * 0.1, height * 0.1)
    if pos == "bottom-right":
        return (width * 0.9, height * 0.1)
    if pos == "bottom-center":
        return (width / 2, height * 0.1)
    return (width / 2, height * 0.9)
