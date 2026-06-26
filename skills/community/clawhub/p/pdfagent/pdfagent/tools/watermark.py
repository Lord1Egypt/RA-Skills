from __future__ import annotations

from pathlib import Path

from reportlab.lib.utils import ImageReader

from ..core.overlay import apply_overlay
from ..core.ranges import parse_page_ranges
from pypdf import PdfReader


def add_watermark(
    input_path: Path,
    output_path: Path,
    *,
    text: str | None = None,
    image: Path | None = None,
    opacity: float = 0.3,
    rotation: int = 45,
    position: str = "center",
    pages: str | None = None,
) -> None:
    if not text and not image:
        raise ValueError("Provide --text or --image")
    if text and image:
        raise ValueError("Provide only one of --text or --image")

    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    def _draw(c, page_num: int, width: float, height: float) -> None:
        if (page_num - 1) not in target_pages:
            return
        try:
            c.setFillAlpha(opacity)
        except Exception:
            pass
        c.saveState()
        if rotation:
            c.translate(width / 2, height / 2)
            c.rotate(rotation)
            c.translate(-width / 2, -height / 2)

        x, y = _position_xy(position, width, height)
        if text:
            c.setFont("Helvetica", 36)
            c.drawCentredString(x, y, text)
        else:
            img = ImageReader(str(image))
            iw, ih = img.getSize()
            scale = min(width / iw, height / ih) * 0.5
            c.drawImage(img, x - (iw * scale / 2), y - (ih * scale / 2), iw * scale, ih * scale)
        c.restoreState()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)


def _position_xy(position: str, width: float, height: float) -> tuple[float, float]:
    pos = position.lower()
    if pos == "center":
        return (width / 2, height / 2)
    if pos == "top-left":
        return (width * 0.15, height * 0.85)
    if pos == "top-right":
        return (width * 0.85, height * 0.85)
    if pos == "bottom-left":
        return (width * 0.15, height * 0.15)
    if pos == "bottom-right":
        return (width * 0.85, height * 0.15)
    return (width / 2, height / 2)
