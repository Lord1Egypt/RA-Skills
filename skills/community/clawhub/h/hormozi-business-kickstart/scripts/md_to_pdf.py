#!/usr/bin/env python3
"""
md_to_pdf.py — Convert Markdown to a simple, clean, A4-centered PDF.

Part of the hormozi-business-kickstart skill.
Generates a polished PDF from any Markdown file using reportlab + NotoSans.
- A4 landscape by default (smaller, more pages, more readable)
- Headings and table cells CENTERED
- Body text justified
- Clean header/footer

Usage:
    python3 md_to_pdf.py <input.md> <output.pdf> [options]

Options:
    --title "TITLE"         Document title (defaults to first H1)
    --author "NAME"         Author name
    --business "NAME"       Business name (shown in header)
    --location "PLACE"      Location (shown in header)
    --primary "#1A3A52"     Primary color (hex, default navy)
    --accent "#D35400"      Accent color (hex, default orange)
    --size a4|a3|a2         Page size (default a4 landscape)
    --portrait              Portrait orientation (default landscape)
    --no-header             Skip the page header
    --no-footer             Skip the page footer

Examples:
    python3 md_to_pdf.py manual.md manual.pdf
    python3 md_to_pdf.py manual.md manual.pdf --size a4 --business "Ponovo Novo" --location "Belgrade"
"""
import argparse
import re
import sys
import os
from pathlib import Path

from reportlab.lib.pagesizes import A2, A3, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# Register NotoSans for Cyrillic + Latin support if available
try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    if os.path.exists('/tmp/NotoSans-Regular.ttf') and os.path.exists('/tmp/NotoSans-Bold.ttf'):
        pdfmetrics.registerFont(TTFont('Body', '/tmp/NotoSans-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Body-Bold', '/tmp/NotoSans-Bold.ttf'))
        BODY_FONT = 'Body'
        BODY_FONT_BOLD = 'Body-Bold'
    else:
        BODY_FONT = 'Helvetica'
        BODY_FONT_BOLD = 'Helvetica-Bold'
except Exception:
    BODY_FONT = 'Helvetica'
    BODY_FONT_BOLD = 'Helvetica-Bold'


PAGE_SIZES = {
    "a4": (A4[1], A4[0]),   # landscape: 29.7 x 21.0 cm
    "a3": (A3[1], A3[0]),
    "a2": (A2[1], A2[0]),
}


def hex_to_color(hex_str):
    return HexColor(hex_str if hex_str.startswith('#') else '#' + hex_str)


def make_styles(primary, accent, text, muted):
    """Build paragraph styles — ALL HEADINGS CENTERED, body justified."""
    return {
        'H1': ParagraphStyle('H1', fontName=BODY_FONT_BOLD, fontSize=22,
                             textColor=primary, spaceAfter=10, spaceBefore=16, leading=26,
                             alignment=TA_CENTER),
        'H2': ParagraphStyle('H2', fontName=BODY_FONT_BOLD, fontSize=16,
                             textColor=primary, spaceAfter=8, spaceBefore=12, leading=20,
                             alignment=TA_CENTER),
        'H3': ParagraphStyle('H3', fontName=BODY_FONT_BOLD, fontSize=13,
                             textColor=accent, spaceAfter=6, spaceBefore=8, leading=16,
                             alignment=TA_CENTER),
        'H4': ParagraphStyle('H4', fontName=BODY_FONT_BOLD, fontSize=11,
                             textColor=primary, spaceAfter=4, spaceBefore=6, leading=14,
                             alignment=TA_CENTER),
        'BODY': ParagraphStyle('BODY', fontName=BODY_FONT, fontSize=10,
                               textColor=text, leading=14, alignment=TA_CENTER, spaceAfter=4),
        'BODY_CENTER': ParagraphStyle('BODY_CENTER', fontName=BODY_FONT, fontSize=10,
                                      textColor=text, leading=14, alignment=TA_CENTER, spaceAfter=4),
        'QUOTE': ParagraphStyle('QUOTE', fontName=BODY_FONT_BOLD, fontSize=12,
                                leftIndent=20, rightIndent=20, textColor=accent,
                                spaceAfter=10, spaceBefore=10, leading=16,
                                alignment=TA_CENTER),
        'LIST': ParagraphStyle('LIST', fontName=BODY_FONT, fontSize=10,
                               textColor=text, leading=13, alignment=TA_CENTER,
                               leftIndent=20, spaceAfter=2),
        'LIST_BOLD': ParagraphStyle('LIST_BOLD', fontName=BODY_FONT_BOLD, fontSize=10,
                                    textColor=text, leading=13, alignment=TA_CENTER,
                                    leftIndent=20, spaceAfter=2),
        'TABLE_HEAD': ParagraphStyle('TABLE_HEAD', fontName=BODY_FONT_BOLD, fontSize=9,
                                     textColor=HexColor('#ffffff'), leading=12,
                                     alignment=TA_CENTER),
        'TABLE_CELL': ParagraphStyle('TABLE_CELL', fontName=BODY_FONT, fontSize=9,
                                     textColor=text, leading=12, alignment=TA_CENTER),
        'SMALL': ParagraphStyle('SMALL', fontName=BODY_FONT, fontSize=8, textColor=muted),
    }


def make_flowables(md, styles, primary):
    flow = []
    lines = md.split('\n')
    i = 0
    table_rows = []
    list_items = []
    in_code_block = False
    code_buffer = []

    def flush_list():
        nonlocal list_items
        if list_items:
            for it in list_items:
                # Check if item starts with ** (bold lead-in)
                is_bold_lead = it.startswith('**')
                style = styles['LIST_BOLD'] if is_bold_lead else styles['LIST']
                # Strip leading ** for the bullet, keep the bold
                display = it
                flow.append(Paragraph(f"• {display}", style))
                flow.append(Spacer(1, 1))
            list_items = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            n_cols = max(len(r) for r in table_rows)
            for r in table_rows:
                while len(r) < n_cols:
                    r.append('')
            data = []
            for ri, row in enumerate(table_rows):
                cells = []
                for c in row:
                    style = styles['TABLE_HEAD'] if ri == 0 else styles['TABLE_CELL']
                    cells.append(Paragraph(str(c).replace('**', ''), style))
                data.append(cells)
            t = Table(data, colWidths=None, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), primary),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#F4F6F7')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            flow.append(Spacer(1, 4))
            flow.append(t)
            flow.append(Spacer(1, 6))
            table_rows = []

    while i < len(lines):
        line = lines[i]
        s = line.rstrip()

        if s.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_buffer = []
            else:
                in_code_block = False
                code_text = '\n'.join(code_buffer).replace('<', '&lt;').replace('>', '&gt;')
                flow.append(Paragraph(f'<font name="Courier">{code_text}</font>', styles['SMALL']))
                code_buffer = []
            i += 1
            continue
        if in_code_block:
            code_buffer.append(s)
            i += 1
            continue

        if s.startswith('# '):
            flush_list(); flush_table()
            flow.append(Paragraph(s[2:].strip(), styles['H1']))
        elif s.startswith('## '):
            flush_list(); flush_table()
            flow.append(Paragraph(s[3:].strip(), styles['H2']))
            flow.append(Spacer(1, 2))
        elif s.startswith('### '):
            flush_list(); flush_table()
            flow.append(Paragraph(s[4:].strip(), styles['H3']))
        elif s.startswith('#### '):
            flush_list(); flush_table()
            flow.append(Paragraph(s[5:].strip(), styles['H4']))

        elif '|' in s and s.strip().startswith('|'):
            flush_list()
            cells = [c.strip() for c in s.strip('|').split('|')]
            if not all(re.match(r'^[-:\s]+$', c) for c in cells):
                table_rows.append(cells)

        elif s == '':
            flush_list(); flush_table()
            flow.append(Spacer(1, 4))

        elif s.startswith('> '):
            flush_list(); flush_table()
            flow.append(Paragraph(s[2:].strip(), styles['QUOTE']))

        elif s.startswith('- ') or s.startswith('* ') or re.match(r'^\d+\.\s', s):
            flush_table()
            cleaned = re.sub(r'^[-*\d.]+\s+', '', s)
            list_items.append(cleaned)

        elif s == '---':
            flush_list(); flush_table()
            flow.append(Spacer(1, 8))

        elif s.startswith('    '):
            flush_list(); flush_table()
            flow.append(Paragraph(f'<font name="Courier">{s.strip()}</font>', styles['SMALL']))

        else:
            flush_list(); flush_table()
            text_str = s
            text_str = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_str)
            text_str = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text_str)
            flow.append(Paragraph(text_str, styles['BODY']))

        i += 1

    flush_list()
    flush_table()
    return flow


def make_header_footer(canvas, doc, title, business, location, primary_hex, muted_hex, page_w_cm):
    """Draw simple header (business + location) and footer (title + page number)."""
    canvas.saveState()
    canvas.setFont(BODY_FONT, 8)
    canvas.setFillColor(hex_to_color(muted_hex))
    canvas.drawString(1.5 * cm, 1 * cm, title or "")
    canvas.drawCentredString(page_w_cm / 2 * cm, 1 * cm, f"Stranica {doc.page}")
    canvas.drawRightString(page_w_cm * cm - 1.5 * cm, 1 * cm, "Built on Hormozi's $100M Trilogy · 2026")
    canvas.setStrokeColor(hex_to_color(primary_hex))
    canvas.setLineWidth(0.5)
    header_y = (29.7 - 1.2) * cm if page_w_cm == 42 else (21 - 1.2) * cm
    canvas.line(1.5 * cm, header_y, page_w_cm * cm - 1.5 * cm, header_y)
    canvas.setFont(BODY_FONT_BOLD, 8)
    canvas.setFillColor(hex_to_color(primary_hex))
    if business:
        canvas.drawString(1.5 * cm, header_y + 0.2 * cm, business.upper())
    if location:
        canvas.drawRightString(page_w_cm * cm - 1.5 * cm, header_y + 0.2 * cm, location)
    canvas.restoreState()


def md_to_pdf(input_path, output_path, title=None, author=None, business=None,
              location=None, primary="#1A3A52", accent="#D35400",
              size="a4", portrait=False, header=True, footer=True):
    md_path = Path(input_path)
    if not md_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    md = md_path.read_text(encoding='utf-8')
    lines = md.split('\n')

    PRIMARY = hex_to_color(primary)
    ACCENT = hex_to_color(accent)
    TEXT = hex_to_color('#2c3e50')
    MUTED = hex_to_color('#7f8c8d')
    PRIMARY_HEX = primary.lstrip('#').upper()
    MUTED_HEX = '#7f8c8d'

    page_w, page_h = PAGE_SIZES.get(size.lower(), PAGE_SIZES["a4"])
    if portrait:
        page_w, page_h = page_h, page_w
    page_w_cm = page_w / cm

    if title is None:
        for line in lines:
            s = line.rstrip()
            if s.startswith('# '):
                title = s[2:].strip()
                break
    if title is None:
        title = md_path.stem.replace('_', ' ').replace('-', ' ').title()

    styles = make_styles(PRIMARY, ACCENT, TEXT, MUTED)

    doc = SimpleDocTemplate(
        output_path, pagesize=(page_w, page_h),
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title=title, author=author or ""
    )

    flow = make_flowables(md, styles, PRIMARY)

    if header or footer:
        def hf(canvas, doc_obj):
            make_header_footer(canvas, doc_obj, title,
                               business if header else "",
                               location if header else "",
                               PRIMARY_HEX, MUTED_HEX, page_w_cm)
        doc.build(flow, onFirstPage=hf, onLaterPages=hf)
    else:
        doc.build(flow)

    print(f"✓ PDF generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to a clean A4-centered PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("input", help="Input Markdown file (.md)")
    parser.add_argument("output", help="Output PDF file (.pdf)")
    parser.add_argument("--title", help="Document title (defaults to first H1)")
    parser.add_argument("--author", help="Author name")
    parser.add_argument("--business", help="Business name (shown in header)")
    parser.add_argument("--location", help="Location (shown in header)")
    parser.add_argument("--primary", default="#1A3A52", help="Primary color hex (default: #1A3A52)")
    parser.add_argument("--accent", default="#D35400", help="Accent color hex (default: #D35400)")
    parser.add_argument("--size", default="a4", choices=["a2", "a3", "a4"], help="Page size (default: a4)")
    parser.add_argument("--portrait", action="store_true", help="Portrait orientation (default: landscape)")
    parser.add_argument("--no-header", action="store_true", help="Skip the page header")
    parser.add_argument("--no-footer", action="store_true", help="Skip the page footer")

    args = parser.parse_args()
    md_to_pdf(
        input_path=args.input,
        output_path=args.output,
        title=args.title,
        author=args.author,
        business=args.business,
        location=args.location,
        primary=args.primary,
        accent=args.accent,
        size=args.size,
        portrait=args.portrait,
        header=not args.no_header,
        footer=not args.no_footer,
    )


if __name__ == "__main__":
    main()
