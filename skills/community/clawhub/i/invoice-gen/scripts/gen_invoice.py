#!/usr/bin/env python3
"""Generate professional PDF invoices with CJK support."""

import argparse
import os
import sys
from datetime import datetime, timedelta

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
except ImportError:
    print("Error: reportlab required. Install with: pip3 install reportlab")
    sys.exit(1)


CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "CNY": "¥", "JPY": "¥",
    "AUD": "A$", "CAD": "C$", "CHF": "CHF", "KRW": "₩", "INR": "₹",
}


def find_cjk_font():
    """Find a CJK font on the system."""
    font_paths = [
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for p in font_paths:
        if os.path.exists(p):
            return p
    # Search
    import glob
    for pattern in ["/usr/share/fonts/**/Noto*CJK*.tt[cf]", "/usr/share/fonts/**/wqy*.tt[cf]"]:
        found = glob.glob(pattern, recursive=True)
        if found:
            return found[0]
    return None


def generate_invoice(args):
    """Generate a PDF invoice."""
    w, h = A4
    c = canvas.Canvas(args.output, pagesize=A4)

    # Try CJK font
    font_name = "Helvetica"
    font_bold = "Helvetica-Bold"
    cjk_font = find_cjk_font()
    if cjk_font:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        try:
            pdfmetrics.registerFont(TTFont("CJK", cjk_font, subfontIndex=0))
            font_name = "CJK"
            font_bold = "CJK"
        except Exception:
            pass

    sym = CURRENCY_SYMBOLS.get(args.currency, args.currency + " ")
    y = h - 40 * mm

    # Header
    c.setFont(font_bold, 24)
    c.drawString(20 * mm, y, "INVOICE")
    c.setFont(font_name, 10)
    c.drawRightString(w - 20 * mm, y, f"#{args.number}")
    y -= 8 * mm
    c.drawRightString(w - 20 * mm, y, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    y -= 5 * mm
    if args.due:
        c.drawRightString(w - 20 * mm, y, f"Due: {args.due}")
    y -= 12 * mm

    # From / To
    c.setFont(font_bold, 10)
    c.drawString(20 * mm, y, "FROM:")
    c.drawString(105 * mm, y, "TO:")
    y -= 5 * mm
    c.setFont(font_name, 9)
    for line in args.sender.split(","):
        c.drawString(20 * mm, y, line.strip())
        y -= 4 * mm
    y_save = y
    y = y_save + (len(args.sender.split(",")) * 4 * mm)
    for line in args.to.split(","):
        c.drawString(105 * mm, y, line.strip())
        y -= 4 * mm
    y = min(y, y_save) - 10 * mm

    # Table header
    c.setFillColor(colors.HexColor("#333333"))
    c.rect(20 * mm, y - 1 * mm, w - 40 * mm, 7 * mm, fill=True)
    c.setFillColor(colors.white)
    c.setFont(font_bold, 9)
    c.drawString(22 * mm, y, "Description")
    c.drawRightString(120 * mm, y, "Qty")
    c.drawRightString(150 * mm, y, "Unit Price")
    c.drawRightString(w - 22 * mm, y, "Amount")
    y -= 8 * mm

    # Items
    c.setFillColor(colors.black)
    c.setFont(font_name, 9)
    subtotal = 0
    for item_str in args.items:
        parts = item_str.split("|")
        if len(parts) != 3:
            print(f"Warning: Skipping malformed item: {item_str}")
            continue
        desc, qty, price = parts[0].strip(), float(parts[1]), float(parts[2])
        amount = qty * price
        subtotal += amount

        c.drawString(22 * mm, y, desc[:50])
        c.drawRightString(120 * mm, y, f"{qty:g}")
        c.drawRightString(150 * mm, y, f"{sym}{price:,.2f}")
        c.drawRightString(w - 22 * mm, y, f"{sym}{amount:,.2f}")
        y -= 6 * mm

        # Light separator
        c.setStrokeColor(colors.HexColor("#EEEEEE"))
        c.line(20 * mm, y + 2 * mm, w - 20 * mm, y + 2 * mm)

    # Totals
    y -= 5 * mm
    c.setStrokeColor(colors.HexColor("#333333"))
    c.line(130 * mm, y + 3 * mm, w - 20 * mm, y + 3 * mm)

    c.setFont(font_name, 10)
    c.drawRightString(155 * mm, y, "Subtotal:")
    c.drawRightString(w - 22 * mm, y, f"{sym}{subtotal:,.2f}")
    y -= 6 * mm

    tax_amount = 0
    if args.tax and args.tax > 0:
        tax_amount = subtotal * args.tax / 100
        c.drawRightString(155 * mm, y, f"Tax ({args.tax}%):")
        c.drawRightString(w - 22 * mm, y, f"{sym}{tax_amount:,.2f}")
        y -= 6 * mm

    total = subtotal + tax_amount
    c.setFont(font_bold, 12)
    c.drawRightString(155 * mm, y, "TOTAL:")
    c.drawRightString(w - 22 * mm, y, f"{sym}{total:,.2f}")
    y -= 15 * mm

    # Notes
    if args.notes:
        c.setFont(font_bold, 9)
        c.drawString(20 * mm, y, "Notes:")
        y -= 5 * mm
        c.setFont(font_name, 9)
        for line in args.notes.split("\\n"):
            c.drawString(20 * mm, y, line)
            y -= 4 * mm

    # Footer
    c.setFont(font_name, 8)
    c.setFillColor(colors.HexColor("#999999"))
    c.drawCentredString(w / 2, 15 * mm, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    c.save()
    print(f"Invoice generated: {args.output} ({sym}{total:,.2f})")


def main():
    parser = argparse.ArgumentParser(description="Generate PDF Invoice")
    parser.add_argument("--from", dest="sender", required=True, help="Sender info (comma-separated lines)")
    parser.add_argument("--to", required=True, help="Client info (comma-separated lines)")
    parser.add_argument("--items", nargs="+", required=True, help="Items: 'desc|qty|price'")
    parser.add_argument("--tax", type=float, default=0, help="Tax percentage")
    parser.add_argument("--currency", default="USD", help="Currency code")
    parser.add_argument("--due", default="", help="Payment terms")
    parser.add_argument("--number", default=f"INV-{datetime.now().strftime('%Y%m%d')}-001", help="Invoice number")
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument("--output", default="invoice.pdf", help="Output PDF path")

    args = parser.parse_args()
    generate_invoice(args)


if __name__ == "__main__":
    main()
