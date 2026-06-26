#!/usr/bin/env python3
"""
Create a sample certificate PDF for testing pdf-text-replace skill.

Generates a realistic-looking award certificate with:
- A4 page size
- Blue decorative border/frame
- Title, date, recipient name, award amount
- Mix of fields that can be replaced with the tool

Uses embedded TrueType fonts (Arial) so the replacement tool can identify
and modify text via the ToUnicode CMap tables.

Save output: demo/sample_certificate.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sample_certificate.pdf")

# Embedded TrueType font paths — these produce proper ToUnicode CMap tables
# that enable the pdf-text-replace tool to identify and swap text bytes.
FONT_REGULAR_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH    = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "ArialRegular"
FONT_BOLD    = "ArialBold"

# Color palette
NAVY      = HexColor("#1a3a5c")
GOLD      = HexColor("#c9a44b")
LIGHT_BG  = HexColor("#f8f6f0")
MID_BLUE  = HexColor("#2d6aa0")
DARK_TEXT = HexColor("#1a1a1a")


def register_fonts():
    """Register embedded TrueType fonts."""
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, FONT_REGULAR_PATH))
    pdfmetrics.registerFont(TTFont(FONT_BOLD,    FONT_BOLD_PATH))


def draw_border(c, width, height):
    """Draw a double-line decorative border."""
    margin_outer = 12 * mm
    margin_inner = 16 * mm

    c.setStrokeColor(NAVY)
    c.setLineWidth(4)
    c.rect(margin_outer, margin_outer,
           width - 2 * margin_outer, height - 2 * margin_outer)

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.rect(margin_inner, margin_inner,
           width - 2 * margin_inner, height - 2 * margin_inner)


def draw_corner_ornaments(c, width, height):
    """Draw simple corner diamond ornaments."""
    margin = 13.5 * mm
    size = 4 * mm
    corners = [
        (margin, margin),
        (width - margin, margin),
        (margin, height - margin),
        (width - margin, height - margin),
    ]
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0)
    for cx, cy in corners:
        p = c.beginPath()
        p.moveTo(cx,        cy + size)
        p.lineTo(cx + size, cy)
        p.lineTo(cx,        cy - size)
        p.lineTo(cx - size, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)


def draw_header_band(c, width, height):
    """Navy header band at the top."""
    band_h = 28 * mm
    band_y = height - 12 * mm - band_h
    c.setFillColor(NAVY)
    c.setStrokeColor(NAVY)
    c.rect(12 * mm, band_y,
           width - 24 * mm, band_h, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(12 * mm, band_y - 1.5 * mm,
           width - 24 * mm, 3 * mm, fill=1, stroke=0)
    return band_y


def draw_footer_band(c, width):
    """Thin navy footer band."""
    c.setFillColor(NAVY)
    c.rect(12 * mm, 12 * mm,
           width - 24 * mm, 14 * mm, fill=1, stroke=0)


def create_certificate():
    width, height = A4   # 595.27 x 841.89 pts
    register_fonts()

    # pageCompression=0 disables ASCII85 wrapping, leaving streams as plain
    # FlateDecode or uncompressed — required by the pdf-text-replace tool.
    c = canvas.Canvas(OUTPUT_FILE, pagesize=A4, pageCompression=0)

    # --- Background ---
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # --- Structural elements ---
    draw_footer_band(c, width)
    band_y = draw_header_band(c, width, height)
    draw_border(c, width, height)
    draw_corner_ornaments(c, width, height)

    cx = width / 2   # horizontal center

    # ── TITLE in header band ──────────────────────────────────────────────────
    c.setFillColor(white)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(cx, band_y + 9 * mm, "Demo Certificate")

    c.setFont(FONT_REGULAR, 10)
    c.drawCentredString(cx, band_y + 3 * mm, "Certificate of Excellence")

    # ── BODY CONTENT ─────────────────────────────────────────────────────────
    body_top = band_y - 18 * mm

    # Decorative horizontal rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(50 * mm, body_top, width - 50 * mm, body_top)

    # Sub-heading
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(cx, body_top - 14 * mm, "This is to certify that")

    # ── Recipient ────────────────────────────────────────────────────────────
    c.setFillColor(DARK_TEXT)
    c.setFont(FONT_REGULAR, 11)
    c.drawCentredString(cx, body_top - 26 * mm, "Recipient: Zhang San")

    # Underline beneath name
    name_y = body_top - 28 * mm
    c.setStrokeColor(MID_BLUE)
    c.setLineWidth(0.7)
    c.line(cx - 45 * mm, name_y, cx + 45 * mm, name_y)

    # ── Body paragraph ───────────────────────────────────────────────────────
    c.setFillColor(DARK_TEXT)
    c.setFont(FONT_REGULAR, 11)
    para_y = body_top - 42 * mm
    c.drawCentredString(cx, para_y,
                        "has demonstrated outstanding performance and")
    c.drawCentredString(cx, para_y - 7 * mm,
                        "is hereby awarded the annual excellence prize.")

    # ── Award amount ─────────────────────────────────────────────────────────
    # Label and value drawn separately so the tool can target "500 RMB" alone.
    award_y = para_y - 28 * mm
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 14)
    award_label_w = c.stringWidth("Award: ", FONT_BOLD, 14)
    award_total_w = c.stringWidth("Award: 500 RMB", FONT_BOLD, 14)
    award_start_x = cx - award_total_w / 2
    c.drawString(award_start_x, award_y, "Award: ")
    c.drawString(award_start_x + award_label_w, award_y, "500 RMB")

    # Gold box around award text
    box_w, box_h = 80 * mm, 14 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(cx - box_w / 2, award_y - 4 * mm, box_w, box_h, fill=0, stroke=1)

    # ── Date ─────────────────────────────────────────────────────────────────
    # The label and value are drawn separately so the replacement tool can
    # target just the date string "2025-01-01" as a standalone Tj operator.
    date_y = award_y - 22 * mm
    c.setFillColor(DARK_TEXT)
    c.setFont(FONT_REGULAR, 11)
    label_w = c.stringWidth("Date: ", FONT_REGULAR, 11)
    total_w = c.stringWidth("Date: 2025-01-01", FONT_REGULAR, 11)
    start_x = cx - total_w / 2
    c.drawString(start_x, date_y, "Date: ")
    c.drawString(start_x + label_w, date_y, "2025-01-01")

    # ── Signature section ────────────────────────────────────────────────────
    sig_y = date_y - 28 * mm
    c.setStrokeColor(DARK_TEXT)
    c.setLineWidth(0.5)
    c.line(cx - 70 * mm, sig_y, cx - 20 * mm, sig_y)
    c.line(cx + 20 * mm, sig_y, cx + 70 * mm, sig_y)

    c.setFont(FONT_REGULAR, 9)
    c.setFillColor(DARK_TEXT)
    c.drawCentredString(cx - 45 * mm, sig_y - 5 * mm, "Authorized Signatory")
    c.drawCentredString(cx + 45 * mm, sig_y - 5 * mm, "Date")

    # ── Footer text ──────────────────────────────────────────────────────────
    c.setFillColor(white)
    c.setFont(FONT_REGULAR, 8)
    c.drawCentredString(cx, 15 * mm,
                        "Issued by Excellence Awards Committee  |  Certificate No. EC-001")

    # ── Decorative seal circle ────────────────────────────────────────────────
    seal_x = width - 55 * mm
    seal_y = sig_y + 5 * mm
    c.setStrokeColor(GOLD)
    c.setFillColor(HexColor("#fdf8ec"))
    c.setLineWidth(1.5)
    c.circle(seal_x, seal_y, 18 * mm, fill=1, stroke=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.circle(seal_x, seal_y, 15 * mm, fill=0, stroke=1)
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(seal_x, seal_y + 3 * mm, "OFFICIAL")
    c.drawCentredString(seal_x, seal_y - 2 * mm, "SEAL")
    c.setFont(FONT_REGULAR, 6)
    # NOTE: intentionally not repeating "2025" here so the replacement
    # tool can target the date field unambiguously in the demo pipeline.
    c.drawCentredString(seal_x, seal_y - 7 * mm, "VALID")

    c.save()
    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_certificate()
