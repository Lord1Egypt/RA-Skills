#!/usr/bin/env python3
"""Convert Markdown file to PDF.

Usage:
    python3 md_to_pdf.py <input.md> [output.pdf]
    If output is omitted, writes to the same path with .pdf extension.

Dependencies: reportlab (pip install reportlab)
Uses PingFang (macOS) or SimHei (Windows) for Chinese text support.
"""

import sys
import re
import os

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable
    )
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus.flowables import HRFlowable
except ImportError:
    print("ERROR: reportlab is required. Install it with: pip install reportlab", file=sys.stderr)
    sys.exit(1)


# ── Font registration ──
FONT_NAME = 'Chinese'
FONT_FILE = None

CANDIDATES = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    'C:\\Windows\\Fonts\\simhei.ttf',
    'C:\\Windows\\Fonts\\msyh.ttc',
]

for fp in CANDIDATES:
    if os.path.exists(fp):
        FONT_FILE = fp
        break

if FONT_FILE:
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_FILE))
        pdfmetrics.registerFont(TTFont(FONT_NAME + '-Bold', FONT_FILE))  # same file for bold
    except Exception:
        FONT_NAME = 'Helvetica'

# ── Colors ──
PRIMARY = HexColor('#2471A3')
TEXT_COLOR = HexColor('#2C3E50')
LIGHT_COLOR = HexColor('#5D6D7E')
ACCENT = HexColor('#1E8449')
CODE_BG = HexColor('#F7F9FB')
WHITE = HexColor('#FFFFFF')
BORDER = HexColor('#D5DDE5')

PAGE_W, PAGE_H = A4


def build_styles():
    styles = getSampleStyleSheet()
    fn = FONT_NAME

    styles.add(ParagraphStyle(
        'CN_Title', parent=styles['Title'],
        fontName=fn, fontSize=24, leading=32,
        textColor=PRIMARY, alignment=TA_CENTER,
        spaceAfter=24,
    ))
    styles.add(ParagraphStyle(
        'CN_H2', parent=styles['Heading2'],
        fontName=fn, fontSize=16, leading=22,
        textColor=PRIMARY, spaceBefore=18, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        'CN_H3', parent=styles['Heading3'],
        fontName=fn, fontSize=13, leading=18,
        textColor=TEXT_COLOR, spaceBefore=12, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'CN_Body', parent=styles['Normal'],
        fontName=fn, fontSize=10, leading=16,
        textColor=LIGHT_COLOR, alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        'CN_Code', parent=styles['Code'],
        fontName='Courier', fontSize=8, leading=12,
        textColor=TEXT_COLOR, backColor=CODE_BG,
        borderPadding=6,
    ))
    styles.add(ParagraphStyle(
        'CN_ListItem', parent=styles['Normal'],
        fontName=fn, fontSize=10, leading=16,
        textColor=LIGHT_COLOR, leftIndent=20,
    ))
    return styles


def parse_inline(text):
    """Convert inline Markdown to HTML-like tags for reportlab."""
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  r'<font color="#2471A3"><u>\1</u></font>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`',
                  r'<font face="Courier" color="#C0392B" size="9">\1</font>', text)
    return text


def convert_md_to_pdf(md_text, output_path, title):
    styles = build_styles()
    story = []

    # Title
    story.append(Paragraph(title, styles['CN_Title']))
    story.append(Spacer(1, 12))

    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_buffer = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                code_text = '\n'.join(code_buffer)
                story.append(Paragraph(code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                                       styles['CN_Code']))
                story.append(Spacer(1, 6))
                code_buffer = []
                in_code_block = False
                i += 1
                continue
            else:
                in_code_block = True
                i += 1
                continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Skip first H1 (used as title)
        h1_match = re.match(r'^#\s+(.+)$', line)
        if h1_match and i < 3:
            i += 1
            continue

        # H2
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            story.append(Paragraph(parse_inline(h2_match.group(1)), styles['CN_H2']))
            i += 1
            continue

        # H3
        h3_match = re.match(r'^###\s+(.+)$', line)
        if h3_match:
            story.append(Paragraph(parse_inline(h3_match.group(1)), styles['CN_H3']))
            i += 1
            continue

        # HR
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            story.append(HRFlowable(width='100%', color=BORDER))
            story.append(Spacer(1, 6))
            i += 1
            continue

        # Tables
        if '|' in line and line.strip().startswith('|'):
            headers = []
            table_rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                row = lines[i]
                if re.match(r'^\|[\s\-:|]+\|$', row.strip()):
                    i += 1
                    continue
                cells = [parse_inline(c.strip()) for c in row.strip().strip('|').split('|')]
                if not headers:
                    headers = [Paragraph(c, ParagraphStyle('th', fontName=FONT_NAME,
                              fontSize=9, textColor=WHITE)) for c in cells]
                else:
                    table_rows.append([Paragraph(c, ParagraphStyle('td', fontName=FONT_NAME,
                                         fontSize=9, textColor=LIGHT_COLOR)) for c in cells])
                i += 1

            if headers or table_rows:
                all_rows = [headers] + table_rows if headers else table_rows
                col_count = len(all_rows[0]) if all_rows else 1
                col_w = (PAGE_W - 72) / col_count  # 72 = 2*36 margins

                t = Table(all_rows, colWidths=[col_w] * col_count)
                t_style = [
                    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
                    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]
                # Zebra striping
                for ri in range(1, len(all_rows)):
                    if ri % 2 == 0:
                        t_style.append(('BACKGROUND', (0, ri), (-1, ri), CODE_BG))
                t.setStyle(TableStyle(t_style))
                story.append(t)
                story.append(Spacer(1, 10))
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if ol_match:
            story.append(Paragraph(
                f'{ol_match.group(1)}. {parse_inline(ol_match.group(2))}',
                styles['CN_ListItem']
            ))
            i += 1
            continue

        # Unordered list
        ul_match = re.match(r'^[-*+]\s+(.+)$', line)
        if ul_match:
            story.append(Paragraph(
                f'\u2022 {parse_inline(ul_match.group(1))}',
                styles['CN_ListItem']
            ))
            i += 1
            continue

        # Paragraph
        if line.strip():
            story.append(Paragraph(parse_inline(line.strip()), styles['CN_Body']))
            i += 1
            continue

        # Empty line
        i += 1

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
        title=title,
    )
    doc.build(story)
    print(f'PDF generated: {output_path}')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_path)[0] + '.pdf'

    with open(input_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.splitext(os.path.basename(input_path))[0]

    convert_md_to_pdf(md_text, output_path, title)


if __name__ == '__main__':
    main()
