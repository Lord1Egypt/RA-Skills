# pyright: reportMissingImports=false
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from constants import (
    PDF_DEFAULT_FONT,
    PDF_DEFAULT_FONT_SIZE,
    PDF_DEFAULT_MARGIN,
    PDF_LINE_HEIGHT,
)
from utils import ensure_output_dir, resolve_path


def _wrap_line(
    text: str, max_width: float, c: canvas.Canvas, font: str, size: int
) -> list[str]:
    """Wrap a single line of text to fit within max_width points."""
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip() if current else word
        if c.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def create_pdf_from_text(
    text: str,
    output_str: str,
    font: str = PDF_DEFAULT_FONT,
    font_size: int = PDF_DEFAULT_FONT_SIZE,
    margin: int = PDF_DEFAULT_MARGIN,
) -> dict:
    """Create a PDF from a plain-text string using ReportLab."""
    output = resolve_path(output_str)
    err = ensure_output_dir(output)
    if err:
        return {"error": err}

    try:
        page_w, page_h = A4
        usable_w = page_w - 2 * margin
        line_h = PDF_LINE_HEIGHT

        c = canvas.Canvas(str(output), pagesize=A4)
        c.setFont(font, font_size)

        y = page_h - margin
        total_pages = 1

        for raw_line in text.splitlines():
            wrapped = _wrap_line(raw_line, usable_w, c, font, font_size)
            for line in wrapped:
                if y < margin + line_h:
                    c.showPage()
                    c.setFont(font, font_size)
                    y = page_h - margin
                    total_pages += 1
                c.drawString(margin, y, line)
                y -= line_h

        c.save()
        return {
            "output": str(output),
            "pages": total_pages,
            "chars": len(text),
        }
    except Exception as exc:
        return {"error": f"Could not create PDF: {exc}"}
