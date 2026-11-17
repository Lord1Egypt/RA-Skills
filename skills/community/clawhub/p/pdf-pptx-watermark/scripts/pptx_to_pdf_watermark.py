#!/usr/bin/env python3
"""
PDF Watermark Tool - with JSON config support.
Usage:
  python3 pptx_to_pdf_watermark.py input.pptx output.pdf [config.json]
  python3 pptx_to_pdf_watermark.py input.pdf output.pdf [config.json]
  python3 pptx_to_pdf_watermark.py --config-only input.pdf output.pdf [config.json]
"""
import sys
import subprocess
import os
import tempfile
import json
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Cross-platform font registration: macOS → STHeiti, Linux → Noto/WenQuanYi, Windows → SimSun
CJK_FONT = None
_font_candidates = [
    ('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc', {'subfontIndex': 0}),  # macOS
    ('NotoSansCJK', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', {'subfontIndex': 0}),  # Linux Noto
    ('WenQuanYi', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', {}),  # Linux WenQuanYi
    ('SimSun', 'C:/Windows/Fonts/simsun.ttc', {'subfontIndex': 0}),  # Windows
]
for _fname, _fpath, _kw in _font_candidates:
    try:
        pdfmetrics.registerFont(TTFont(_fname, _fpath, **_kw))
        CJK_FONT = _fname
        break
    except Exception:
        continue
# Fallback: reportlab built-in Helvetica (no CJK support, but won't crash)
if CJK_FONT is None:
    CJK_FONT = 'Helvetica'

DEFAULT_CONFIG = {
    "text": "内部资料 请勿外传",
    "fontSize": 60,
    "opacity": 0.15,
    "rotation": 45,
    "color": [0.5, 0.5, 0.5],
    "pattern": "diagonal",       # diagonal | grid | center
    "repeatX": 3,
    "repeatY": 3,
    "offsetX": 200,
    "offsetY": 200
}

def load_config(config_path=None):
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        cfg = {**DEFAULT_CONFIG, **user_config}
    else:
        cfg = DEFAULT_CONFIG.copy()
    return cfg

def pptx_to_pdf(pptx_path, output_dir):
    """Convert PPTX to PDF via LibreOffice."""
    result = subprocess.run(
        ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, pptx_path],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice error: {result.stderr}")
    base = os.path.splitext(os.path.basename(pptx_path))[0]
    pdf_path = os.path.join(output_dir, base + '.pdf')
    if os.path.exists(pdf_path):
        return pdf_path
    raise RuntimeError("PDF not found after conversion")

def add_watermark(input_pdf, output_pdf, config):
    """Add watermark to every page of a PDF using the given config."""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    text = config.get("text", "CONFIDENTIAL")
    font_size = config.get("fontSize", 60)
    opacity = config.get("opacity", 0.15)
    rotation = config.get("rotation", 45)
    color = config.get("color", [0.5, 0.5, 0.5])
    pattern = config.get("pattern", "diagonal")
    repeat_x = config.get("repeatX", 3)
    repeat_y = config.get("repeatY", 3)
    offset_x = config.get("offsetX", 200)
    offset_y = config.get("offsetY", 200)

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pw = float(page.mediabox.width)
        ph = float(page.mediabox.height)

        wm_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        wm_path = wm_pdf.name
        wm_pdf.close()

        c = canvas.Canvas(wm_path, pagesize=(pw, ph))
        c.saveState()
        c.setFillColor(Color(color[0], color[1], color[2], alpha=opacity))
        c.setFont(CJK_FONT, font_size)

        if pattern == "center":
            c.translate(pw / 2, ph / 2)
            c.rotate(rotation)
            c.drawCentredString(0, 0, text)
        elif pattern == "grid":
            for iy in range(repeat_y):
                for ix in range(repeat_x):
                    x = (ix + 1) * pw / (repeat_x + 1)
                    y = (iy + 1) * ph / (repeat_y + 1)
                    c.saveState()
                    c.translate(x, y)
                    c.rotate(rotation)
                    c.drawCentredString(0, 0, text)
                    c.restoreState()
        else:  # diagonal
            c.translate(pw / 2, ph / 2)
            c.rotate(rotation)
            c.drawCentredString(0, 0, text)
            c.drawCentredString(-offset_x, offset_y, text)
            c.drawCentredString(offset_x, -offset_y, text)
            # Add more for larger pages
            c.drawCentredString(-2 * offset_x, 2 * offset_y, text)
            c.drawCentredString(2 * offset_x, -2 * offset_y, text)

        c.restoreState()
        c.save()

        wm_reader = PdfReader(wm_path)
        wm_page = wm_reader.pages[0]
        page.merge_page(wm_page)
        writer.add_page(page)
        os.unlink(wm_path)

    with open(output_pdf, 'wb') as f:
        writer.write(f)

def generate_preview(config, output_path):
    """Generate a single-page preview PDF with the watermark on a white page."""
    pw, ph = 595, 842  # A4 size in points
    text = config.get("text", "CONFIDENTIAL")
    font_size = config.get("fontSize", 60)
    opacity = config.get("opacity", 0.15)
    rotation = config.get("rotation", 45)
    color = config.get("color", [0.5, 0.5, 0.5])
    pattern = config.get("pattern", "diagonal")
    repeat_x = config.get("repeatX", 3)
    repeat_y = config.get("repeatY", 3)
    offset_x = config.get("offsetX", 200)
    offset_y = config.get("offsetY", 200)

    c = canvas.Canvas(output_path, pagesize=(pw, ph))
    # Light gray background to simulate page
    c.setFillColor(Color(0.95, 0.95, 0.95))
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    # Sample content lines
    c.setFillColor(Color(0.8, 0.8, 0.8))
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Sample document content - Line 1")
    c.drawString(50, 730, "Sample document content - Line 2")
    c.drawString(50, 710, "Sample document content - Line 3")
    c.drawString(50, 690, "...")
    # Draw watermark
    c.saveState()
    c.setFillColor(Color(color[0], color[1], color[2], alpha=opacity))
    c.setFont(CJK_FONT, font_size)

    if pattern == "center":
        c.translate(pw / 2, ph / 2)
        c.rotate(rotation)
        c.drawCentredString(0, 0, text)
    elif pattern == "grid":
        for iy in range(repeat_y):
            for ix in range(repeat_x):
                x = (ix + 1) * pw / (repeat_x + 1)
                y = (iy + 1) * ph / (repeat_y + 1)
                c.saveState()
                c.translate(x, y)
                c.rotate(rotation)
                c.drawCentredString(0, 0, text)
                c.restoreState()
    else:
        c.translate(pw / 2, ph / 2)
        c.rotate(rotation)
        c.drawCentredString(0, 0, text)
        c.drawCentredString(-offset_x, offset_y, text)
        c.drawCentredString(offset_x, -offset_y, text)
        c.drawCentredString(-2 * offset_x, 2 * offset_y, text)
        c.drawCentredString(2 * offset_x, -2 * offset_y, text)

    c.restoreState()
    c.save()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 pptx_to_pdf_watermark.py <input.pptx|input.pdf> <output.pdf> [config.json]")
        print("       python3 pptx_to_pdf_watermark.py --preview <config.json> <output.pdf>")
        sys.exit(1)

    if sys.argv[1] == '--preview':
        config = load_config(sys.argv[2])
        generate_preview(config, sys.argv[3])
        print(f"Preview saved: {sys.argv[3]}")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        config = load_config(sys.argv[3] if len(sys.argv) > 3 else None)

        # Convert if needed
        ext = os.path.splitext(input_file)[1].lower()
        if ext in ('.pptx', '.ppt'):
            tmp_dir = tempfile.mkdtemp()
            pdf_path = pptx_to_pdf(input_file, tmp_dir)
        else:
            pdf_path = input_file

        add_watermark(pdf_path, output_file, config)
        print(f"Watermarked PDF saved: {output_file}")
