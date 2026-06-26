from __future__ import annotations

import io
from typing import Callable

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def apply_overlay(
    input_path: str,
    output_path: str,
    draw_fn: Callable[[canvas.Canvas, int, float, float], None],
) -> None:
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        draw_fn(c, page_index, width, height)
        c.showPage()
        c.save()

        packet.seek(0)
        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
