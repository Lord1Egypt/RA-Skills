#!/usr/bin/env python3
"""
Premium Enterprise PDF Generator for OPENCLAW
Converts markdown to a premium enterprise-style PDF with de-AI text humanization.

Usage:
    python3 generate_pdf.py --input "# Title\n\nContent..." --output report.pdf [--title "Report"] [--logo logo.png]
    python3 generate_pdf.py --input document.md --output report.pdf
"""

import argparse
import os
import re
import sys
from datetime import datetime

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Flowable


# ---------------------------------------------------------------------------
# DESIGN SYSTEM — Navy + Gold (60-30-10 rule)
# ---------------------------------------------------------------------------

COLOR_NAVY = colors.HexColor("#1A2B4A")
COLOR_GOLD = colors.HexColor("#C9A84C")
COLOR_WHITE = colors.HexColor("#FFFFFF")
COLOR_LIGHT_GRAY = colors.HexColor("#F8F9FA")
COLOR_MEDIUM_GRAY = colors.HexColor("#E8E8E8")
COLOR_TEXT = colors.HexColor("#2D2D2D")
COLOR_TEXT_LIGHT = colors.HexColor("#6B7280")
COLOR_CODE_BG = colors.HexColor("#F0F0F0")
COLOR_BLOCKQUOTE_BG = colors.HexColor("#F5F3EE")

MARGIN = 72  # 1 inch
HEADER_HEIGHT = 55
FOOTER_HEIGHT = 35
PAGE_WIDTH, PAGE_HEIGHT = A4


# ---------------------------------------------------------------------------
# DE-AI TEXT TRANSFORMER
# ---------------------------------------------------------------------------

def deai_transform(text: str) -> str:
    """Apply de-AI transformations to humanize LLM-generated text."""

    # --- Em dash and en dash ---
    # Em dash between clauses: replace with period + space (start new sentence)
    text = re.sub(r'\s*—\s*', ', ', text)
    # En dash between words: replace with hyphen
    text = re.sub(r'\s*–\s*', ' - ', text)

    # --- Overly formal / AI filler phrases ---
    replacements = [
        # Formal transitions
        (r'\bIn conclusion,\s*', 'To wrap up, '),
        (r'\bIn summary,\s*', 'Overall, '),
        (r'\bFurthermore,\s*', 'Also, '),
        (r'\bMoreover,\s*', 'What\'s more, '),
        (r'\bAdditionally,\s*', 'And '),
        (r'\bConsequently,\s*', 'So '),
        (r'\bSubsequently,\s*', 'Then '),
        (r'\bNevertheless,\s*', 'Still, '),
        (r'\bNotwithstanding,?\s*', 'That said, '),

        # AI filler openers
        (r'\bIt is important to note that\s*', 'Note that '),
        (r'\bIt is worth noting that\s*', 'Worth noting: '),
        (r'\bIt should be noted that\s*', 'Note that '),
        (r'\bIt is essential to\s*', 'You need to '),
        (r'\bIt is crucial to\s*', 'Critically, '),
        (r'\bOne must consider\s*', 'Consider '),
        (r'\bIt is imperative that\s*', 'Make sure '),

        # Formal verb substitutions
        (r'\butilize[sd]?\b', 'use'),
        (r'\butilizing\b', 'using'),
        (r'\butilization\b', 'use'),
        (r'\bleverag(e|ing|ed)\b', lambda m: {'e': 'use', 'ing': 'using', 'ed': 'used'}[m.group(1)]),
        (r'\bfacilitate\b', 'help'),
        (r'\bimplement\b', 'build'),
        (r'\bimplementation\b', 'setup'),
        (r'\bdemonstrate\b', 'show'),
        (r'\bascertain\b', 'find out'),
        (r'\bcommence\b', 'start'),
        (r'\bterminate\b', 'end'),
        (r'\bprocure\b', 'get'),

        # AI buzzwords
        (r'\bdelve into\b', 'explore'),
        (r'\bdelving into\b', 'exploring'),
        (r'\bcomprehensive\b', 'complete'),
        (r'\brobust\b', 'solid'),
        (r'\bseamless(ly)?\b', 'smooth\\1'),
        (r'\bcutting-edge\b', 'advanced'),
        (r'\bstate-of-the-art\b', 'modern'),
        (r'\bsynerg(y|ize|istic)\b', 'collaboration'),
        (r'\bparadigm shift\b', 'major change'),
        (r'\bgame-changer\b', 'major shift'),
        (r'\bholistic\b', 'complete'),
        (r'\bpivot\b', 'shift'),
        (r'\bscalable\b', 'flexible'),
        (r'\boptimize\b', 'improve'),
        (r'\boptimization\b', 'improvement'),
        (r'\bIn order to\b', 'To'),
        (r'\bin order to\b', 'to'),

        # Unnecessary qualifiers
        (r'\bvery unique\b', 'unique'),
        (r'\babsolutely essential\b', 'essential'),
        (r'\bentirely new\b', 'new'),
        (r'\bbasically\b', ''),
        (r'\bliterally\b', ''),
        (r'\bactually\b', ''),
        (r'\bquite\b', ''),
        (r'\brather\b', ''),

        # AI list intros
        (r'^Here are (the|some|a few)\s+', '', re.MULTILINE),
        (r'^The following (are|is)\s+', '', re.MULTILINE),
        (r':\s*\n\s*\n', ':\n', ),
    ]

    for pattern_args in replacements:
        if len(pattern_args) == 2:
            pattern, replacement = pattern_args
            flags = 0
        else:
            pattern, replacement, flags = pattern_args

        if callable(replacement):
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | flags)
        else:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | flags)

    # --- Clean up spacing artifacts ---
    # Remove double spaces
    text = re.sub(r'  +', ' ', text)
    # Fix ". ," or ", ." artifacts
    text = re.sub(r'\.\s+,', '.', text)
    text = re.sub(r',\s+\.', '.', text)
    # Remove trailing spaces on lines
    text = re.sub(r' +\n', '\n', text)
    # Normalize multiple blank lines to max 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# ---------------------------------------------------------------------------
# MARKDOWN PARSER
# ---------------------------------------------------------------------------

class Block:
    """Represents a parsed markdown block."""
    def __init__(self, kind: str, content, level: int = 0, ordered: bool = False):
        self.kind = kind      # heading, paragraph, list, code, blockquote, hr, spacer
        self.content = content
        self.level = level    # for headings: 1-4; for lists: nesting
        self.ordered = ordered


def parse_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to ReportLab XML."""
    # Escape XML special chars first (preserve & for later)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Bold+italic: ***text*** or ___text___
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'___(.+?)___', r'<b><i>\1</i></b>', text)

    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)

    # Italic: *text* or _text_
    text = re.sub(r'\*([^*]+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+?)_', r'<i>\1</i>', text)

    # Inline code: `code`
    text = re.sub(
        r'`([^`]+?)`',
        r'<font name="Courier" size="9" color="#555555">\1</font>',
        text
    )

    # Links: [text](url) — show as bold text (PDF can't hyperlink easily without extras)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<b>\1</b>', text)

    return text


def parse_markdown(text: str) -> list:
    """Parse markdown text into a list of Block objects."""
    blocks = []
    lines = text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- Fenced code block ---
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append(Block('code', '\n'.join(code_lines), level=0))
            i += 1
            continue

        # --- Horizontal rule ---
        if re.match(r'^(\*\*\*|---|___)\s*$', line.strip()):
            blocks.append(Block('hr', ''))
            i += 1
            continue

        # --- Heading ---
        heading_match = re.match(r'^(#{1,4})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            blocks.append(Block('heading', content, level=level))
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith('> ') or line == '>':
            quote_lines = []
            while i < len(lines) and (lines[i].startswith('> ') or lines[i] == '>'):
                quote_lines.append(lines[i][2:] if lines[i].startswith('> ') else '')
                i += 1
            blocks.append(Block('blockquote', ' '.join(quote_lines)))
            continue

        # --- Unordered list ---
        ul_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if ul_match:
            items = []
            while i < len(lines):
                m = re.match(r'^(\s*)[-*+]\s+(.+)$', lines[i])
                if m:
                    indent = len(m.group(1)) // 2
                    items.append((indent, m.group(2).strip()))
                    i += 1
                elif lines[i].strip() == '':
                    break
                else:
                    break
            blocks.append(Block('list', items, ordered=False))
            continue

        # --- Ordered list ---
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ol_match:
            items = []
            counter = [0]  # mutable for closure-like tracking
            while i < len(lines):
                m = re.match(r'^(\s*)\d+\.\s+(.+)$', lines[i])
                if m:
                    indent = len(m.group(1)) // 2
                    counter[0] += 1
                    items.append((indent, m.group(2).strip(), counter[0]))
                    i += 1
                elif lines[i].strip() == '':
                    break
                else:
                    break
            blocks.append(Block('list', items, ordered=True))
            continue

        # --- Blank line → spacer ---
        if line.strip() == '':
            blocks.append(Block('spacer', ''))
            i += 1
            continue

        # --- Paragraph: accumulate consecutive non-special lines ---
        para_lines = []
        while i < len(lines):
            l = lines[i]
            if l.strip() == '':
                break
            if re.match(r'^#{1,4}\s', l) or re.match(r'^(\*\*\*|---|___)\s*$', l.strip()):
                break
            if l.startswith('```') or l.startswith('> ') or re.match(r'^(\s*)[-*+]\s', l) or re.match(r'^\s*\d+\.\s', l):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            blocks.append(Block('paragraph', ' '.join(para_lines)))
        continue

    return blocks


# ---------------------------------------------------------------------------
# HEADER / FOOTER CANVAS
# ---------------------------------------------------------------------------

class HeaderFooterCanvas:
    """Mixin-style class to draw headers and footers on each page."""

    def __init__(self, title: str, logo_path: str = None):
        self.doc_title = title
        self.logo_path = logo_path

    def draw_header(self, canvas, doc):
        canvas.saveState()
        page_width = doc.pagesize[0]

        # Header background strip
        canvas.setFillColor(COLOR_NAVY)
        canvas.rect(0, PAGE_HEIGHT - HEADER_HEIGHT, page_width, HEADER_HEIGHT, fill=1, stroke=0)

        # Gold accent line below header
        canvas.setFillColor(COLOR_GOLD)
        canvas.rect(0, PAGE_HEIGHT - HEADER_HEIGHT - 3, page_width, 3, fill=1, stroke=0)

        # Logo (if provided and file exists)
        logo_drawn = False
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo_x = MARGIN
                logo_y = PAGE_HEIGHT - HEADER_HEIGHT + 8
                logo_h = HEADER_HEIGHT - 16
                img = Image(self.logo_path, height=logo_h, width=logo_h * 2)
                img.drawOn(canvas, logo_x, logo_y)
                logo_drawn = True
            except Exception:
                logo_drawn = False

        # Document title in header
        title_x = MARGIN + (logo_drawn and HEADER_HEIGHT * 2 + 10 or 0)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(COLOR_WHITE)
        canvas.drawString(title_x, PAGE_HEIGHT - HEADER_HEIGHT + 20, self.doc_title)

        # Date (top-right)
        date_str = datetime.now().strftime('%B %d, %Y')
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#B8C5D6'))
        canvas.drawRightString(page_width - MARGIN, PAGE_HEIGHT - HEADER_HEIGHT + 20, date_str)

        canvas.restoreState()

    def draw_footer(self, canvas, doc):
        canvas.saveState()
        page_width = doc.pagesize[0]
        page_num = doc.page

        # Footer separator line (navy)
        canvas.setStrokeColor(COLOR_NAVY)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, FOOTER_HEIGHT, page_width - MARGIN, FOOTER_HEIGHT)

        # Gold accent dot in center
        canvas.setFillColor(COLOR_GOLD)
        canvas.circle(page_width / 2, FOOTER_HEIGHT - 12, 3, fill=1, stroke=0)

        # Page number
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(COLOR_TEXT_LIGHT)
        canvas.drawCentredString(page_width / 2, FOOTER_HEIGHT - 25, str(page_num))

        # Brand/company text (left side of footer)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(COLOR_TEXT_LIGHT)
        canvas.drawString(MARGIN, FOOTER_HEIGHT - 18, 'CONFIDENTIAL')

        canvas.restoreState()


# ---------------------------------------------------------------------------
# PDF DOCUMENT BUILDER
# ---------------------------------------------------------------------------

def build_styles():
    """Return a dict of ParagraphStyle objects."""
    base = getSampleStyleSheet()

    styles = {}

    styles['h1'] = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=COLOR_NAVY,
        spaceBefore=24,
        spaceAfter=8,
        alignment=TA_LEFT,
    )
    styles['h2'] = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=COLOR_NAVY,
        spaceBefore=20,
        spaceAfter=4,
        alignment=TA_LEFT,
    )
    styles['h3'] = ParagraphStyle(
        'H3',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=22,
        textColor=COLOR_NAVY,
        spaceBefore=16,
        spaceAfter=4,
        alignment=TA_LEFT,
    )
    styles['h4'] = ParagraphStyle(
        'H4',
        fontName='Helvetica-BoldOblique',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#374151'),
        spaceBefore=12,
        spaceAfter=2,
        alignment=TA_LEFT,
    )
    styles['body'] = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        textColor=COLOR_TEXT,
        spaceBefore=4,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    )
    styles['list_item'] = ParagraphStyle(
        'ListItem',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=COLOR_TEXT,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=18,
        bulletIndent=0,
        alignment=TA_LEFT,
    )
    styles['list_item_ordered'] = ParagraphStyle(
        'ListItemOrdered',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=COLOR_TEXT,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=24,
        bulletIndent=0,
        alignment=TA_LEFT,
    )
    styles['code'] = ParagraphStyle(
        'Code',
        fontName='Courier',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=12,
        rightIndent=12,
        backColor=COLOR_CODE_BG,
        borderColor=COLOR_MEDIUM_GRAY,
        borderWidth=0.5,
        borderPadding=(8, 8, 8, 8),
        alignment=TA_LEFT,
    )
    styles['blockquote'] = ParagraphStyle(
        'Blockquote',
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=17,
        textColor=colors.HexColor('#4B5563'),
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=20,
        rightIndent=12,
        backColor=COLOR_BLOCKQUOTE_BG,
        borderColor=COLOR_GOLD,
        borderWidth=3,
        borderPadding=(8, 8, 8, 8),
        alignment=TA_LEFT,
    )

    return styles


class GoldRuler(Flowable):
    """A horizontal gold rule for visual separation."""

    def __init__(self, width=None, thickness=1.5, spaceAbove=6, spaceBelow=12):
        super().__init__()
        self._width = width
        self.thickness = thickness
        self.spaceAbove = spaceAbove
        self.spaceBelow = spaceBelow
        self.height = thickness + spaceAbove + spaceBelow

    def wrap(self, aW, aH):
        self.width = self._width or aW
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(COLOR_GOLD)
        self.canv.setLineWidth(self.thickness)
        y = self.spaceBelow
        self.canv.line(0, y, self.width, y)
        self.canv.restoreState()


def make_page_template(title: str, logo_path: str = None):
    """Create a PageTemplate with header and footer frames."""
    hfc = HeaderFooterCanvas(title, logo_path)

    content_frame = Frame(
        MARGIN,
        FOOTER_HEIGHT + 8,
        PAGE_WIDTH - 2 * MARGIN,
        PAGE_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - 20,
        id='main',
        leftPadding=0,
        rightPadding=0,
        topPadding=6,
        bottomPadding=6,
    )

    def on_page(canvas, doc):
        hfc.draw_header(canvas, doc)
        hfc.draw_footer(canvas, doc)

    return PageTemplate(id='main', frames=[content_frame], onPage=on_page)


def render_pdf(blocks: list, output_path: str, title: str, logo_path: str = None):
    """Render parsed markdown blocks to a premium enterprise PDF."""
    styles = build_styles()
    story = []

    for i, block in enumerate(blocks):
        kind = block.kind

        if kind == 'spacer':
            story.append(Spacer(1, 6))

        elif kind == 'hr':
            story.append(GoldRuler(spaceAbove=8, spaceBelow=8))

        elif kind == 'heading':
            level = block.level
            style_key = f'h{min(level, 4)}'
            text = parse_inline(block.content)
            heading_para = Paragraph(text, styles[style_key])
            # Keep heading + gold rule together; prevents orphan heading at page bottom
            if level in (1, 2):
                story.append(KeepTogether([
                    heading_para,
                    GoldRuler(thickness=1.0, spaceAbove=2, spaceBelow=10),
                ]))
            else:
                story.append(heading_para)

        elif kind == 'paragraph':
            text = parse_inline(block.content)
            story.append(Paragraph(text, styles['body']))

        elif kind == 'code':
            # Use Preformatted to preserve whitespace and indentation natively
            code_style = ParagraphStyle(
                'CodeBlock',
                fontName='Courier',
                fontSize=9,
                leading=13,
                textColor=colors.HexColor('#1F2937'),
                spaceBefore=8,
                spaceAfter=8,
                leftIndent=12,
                backColor=COLOR_CODE_BG,
            )
            story.append(Preformatted(block.content, code_style))

        elif kind == 'blockquote':
            text = parse_inline(block.content)
            bq_para = Paragraph(text, styles['blockquote'])
            # Wrap in Table to achieve gold left border (CSS border-left equivalent)
            bq_table = Table(
                [[bq_para]],
                colWidths=[PAGE_WIDTH - 2 * MARGIN],
                style=TableStyle([
                    ('LEFTPADDING',   (0, 0), (-1, -1), 14),
                    ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
                    ('TOPPADDING',    (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND',    (0, 0), (-1, -1), COLOR_BLOCKQUOTE_BG),
                    ('LINEBEFORE',    (0, 0), (0, -1), 4, COLOR_GOLD),
                ]),
            )
            story.append(bq_table)
            story.append(Spacer(1, 6))

        elif kind == 'list':
            items = block.content
            list_items = []
            for item_data in items:
                if block.ordered:
                    _indent, item_text, num = item_data
                    text = parse_inline(item_text)
                    li = ListItem(
                        Paragraph(text, styles['list_item_ordered']),
                        value=num,
                    )
                else:
                    _indent, item_text = item_data
                    text = parse_inline(item_text)
                    li = ListItem(
                        Paragraph(text, styles['list_item']),
                    )
                list_items.append(li)

            story.append(ListFlowable(
                list_items,
                bulletType='1' if block.ordered else 'bullet',
                bulletColor=COLOR_GOLD,
                bulletFontSize=10,
                leftIndent=20,
                spaceBefore=4,
                spaceAfter=8,
            ))

    # Build the document
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=HEADER_HEIGHT + 16,
        bottomMargin=FOOTER_HEIGHT + 16,
        title=title,
        author='OpenClaw Premium PDF Skill',
    )

    page_template = make_page_template(title, logo_path)
    doc.addPageTemplates([page_template])

    doc.build(story)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate a premium enterprise PDF from markdown input.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Markdown content as string or path to a .md file',
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output PDF file path',
    )
    parser.add_argument(
        '--title', '-t',
        default='Enterprise Report',
        help='Document title shown in header (default: "Enterprise Report")',
    )
    parser.add_argument(
        '--logo',
        default=None,
        help='Path to a logo image file (PNG/JPG) to display in the header',
    )
    return parser.parse_args()


def load_markdown(input_arg: str) -> str:
    """Load markdown from a file path or return the string directly."""
    # Check if it looks like a file path
    if '\n' not in input_arg and os.path.isfile(input_arg):
        with open(input_arg, 'r', encoding='utf-8') as f:
            return f.read()
    # Otherwise treat as raw markdown string
    # Handle escaped newlines from CLI
    return input_arg.replace('\\n', '\n')


def main():
    args = parse_args()

    # 1. Load markdown
    try:
        markdown_text = load_markdown(args.input)
    except Exception as e:
        print(f'Error loading input: {e}', file=sys.stderr)
        sys.exit(1)

    if not markdown_text.strip():
        print('Error: input is empty.', file=sys.stderr)
        sys.exit(1)

    # 2. Apply de-AI transformation
    humanized_text = deai_transform(markdown_text)

    # 3. Parse markdown into blocks
    blocks = parse_markdown(humanized_text)

    if not blocks:
        print('Error: could not parse any content from input.', file=sys.stderr)
        sys.exit(1)

    # 4. Ensure output directory exists
    output_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(output_dir, exist_ok=True)

    # 5. Render PDF
    try:
        render_pdf(blocks, args.output, args.title, args.logo)
    except Exception as e:
        print(f'Error generating PDF: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(f'PDF generated successfully: {os.path.abspath(args.output)}')


if __name__ == '__main__':
    main()
