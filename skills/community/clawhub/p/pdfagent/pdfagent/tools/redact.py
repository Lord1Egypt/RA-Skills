from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

from ..core.overlay import apply_overlay
from ..core.ranges import parse_page_ranges
from .render import render_pdf_to_images
from .images import images_to_pdf


@dataclass(frozen=True)
class RedactionBox:
    page: int
    x: float
    y: float
    width: float
    height: float


def redact_pdf(
    input_path: Path,
    output_path: Path,
    *,
    boxes: list[RedactionBox],
    search: str | None = None,
    pages: str | None = None,
    mode: str = "overlay",
) -> None:
    if mode not in {"overlay", "rasterize"}:
        raise ValueError("mode must be overlay or rasterize")

    if search:
        boxes.extend(_search_boxes(input_path, search, pages))

    if mode == "rasterize":
        _rasterize_redact(input_path, output_path, boxes)
        return

    _overlay_redact(input_path, output_path, boxes)


def _overlay_redact(input_path: Path, output_path: Path, boxes: list[RedactionBox]) -> None:
    if not boxes:
        raise ValueError("No redaction boxes provided")

    by_page: dict[int, list[RedactionBox]] = {}
    for box in boxes:
        by_page.setdefault(box.page, []).append(box)

    def _draw(c, page_num: int, width: float, height: float) -> None:
        for box in by_page.get(page_num, []):
            c.setFillColorRGB(0, 0, 0)
            c.rect(box.x, box.y, box.width, box.height, fill=1, stroke=0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)


def _rasterize_redact(input_path: Path, output_path: Path, boxes: list[RedactionBox]) -> None:
    temp_dir = output_path.parent / f".{output_path.stem}_redact"
    images = render_pdf_to_images(input_path, temp_dir, fmt="png")
    if not images:
        raise ValueError("Failed to render PDF for redaction")

    from pypdf import PdfReader
    reader = PdfReader(str(input_path))

    by_page: dict[int, list[RedactionBox]] = {}
    for box in boxes:
        by_page.setdefault(box.page, []).append(box)

    redacted_images: list[Path] = []
    for idx, img_path in enumerate(images, start=1):
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        page = reader.pages[idx - 1]
        page_w = float(page.mediabox.width)
        page_h = float(page.mediabox.height)
        scale_x = img.width / page_w
        scale_y = img.height / page_h
        for box in by_page.get(idx, []):
            x0 = box.x * scale_x
            y0 = (page_h - (box.y + box.height)) * scale_y
            x1 = (box.x + box.width) * scale_x
            y1 = (page_h - box.y) * scale_y
            draw.rectangle([x0, y0, x1, y1], fill="black")
        redacted_path = img_path.parent / f"redacted_{img_path.name}"
        img.save(redacted_path)
        redacted_images.append(redacted_path)

    images_to_pdf(redacted_images, output_path)


def _search_boxes(input_path: Path, query: str, pages: str | None) -> list[RedactionBox]:
    try:
        import pdfplumber
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pdfplumber is required. Install with: pip install 'pdfagent[redact]' ") from exc

    boxes: list[RedactionBox] = []
    with pdfplumber.open(str(input_path)) as pdf:
        total = len(pdf.pages)
        target_pages = set(parse_page_ranges(pages, total))
        for page_index, page in enumerate(pdf.pages):
            if page_index not in target_pages:
                continue
            height = page.height
            for word in page.extract_words():
                if query.lower() in word["text"].lower():
                    x0, top, x1, bottom = word["x0"], word["top"], word["x1"], word["bottom"]
                    y = height - bottom
                    box = RedactionBox(page=page_index + 1, x=x0, y=y, width=x1 - x0, height=bottom - top)
                    boxes.append(box)
    return boxes
