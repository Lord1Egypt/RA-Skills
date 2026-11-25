# -*- coding: utf-8 -*-
"""PolicyForge: render marked-up text into a Chinese official-format .docx.

Requires: python-docx  (pip install python-docx)

Usage
    python make_gongwen_docx.py source.md output.docx
    python make_gongwen_docx.py source.md output.docx --no-detect
    python make_gongwen_docx.py source.md output.docx --body-font 仿宋 --line-pt 28

Markup contract
    # 标题                     main title (22pt, centred)
    ## ——副标题                subtitle (14pt, centred)
    ## 一、xxx                 level-1 heading (16pt, first-line indent 2 chars)
    ### （一）xxx              level-2 heading (16pt bold, indent 2 chars)
    | a | b |                  table (second row must be the separator row)
    > 原文摘录                 quote block (left rule + indent)
    - item                     auto-numbered item
    plain line                 body text (16pt, exact line spacing, indent 2 chars)
    【填入：X】                placeholder, rendered bold red
    ## 附：xxx                 starts a new page

Layout notes (the six silent failures)
    * run.font.name does not change Chinese glyphs; w:rFonts/@w:eastAsia must be set.
    * page size defaults to Letter; A4 has to be set explicitly.
    * exact line spacing needs both the rule and a point value.
    * tables need column width and cell width; setting one is ignored.
    * cell shading must use the clear/overlay value; the solid value renders black.
    * the page-number field needs begin, instrText and end inside one run.

Page forecast
    16pt body text in a 15.6 cm text block gives roughly 27 characters per line and
    22 lines per page, so about 600 characters per page. The script prints the forecast
    before writing, so a surprise page count is caught before the render.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:  # pragma: no cover
    print("python-docx is required:  pip install python-docx")
    raise SystemExit(2)

TITLE_PT = 22.0
SUBTITLE_PT = 14.0
BODY_PT = 16.0
LINE_PT = 29.0
TABLE_PT = 9.5
INDENT_MULT = 2.0
HEADER_FILL = "DCE6F1"
COLOR_RED = RGBColor(0xC0, 0x00, 0x00)
COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
LATIN_FONT = "Times New Roman"

FONT_CHAINS = {
    "title": ["方正小标宋简体", "方正小标宋_GBK", "华文中宋", "黑体"],
    "h1": ["黑体", "微软雅黑"],
    "h2": ["楷体_GB2312", "楷体", "KaiTi"],
    "body": ["仿宋_GB2312", "仿宋", "FangSong", "宋体"],
}
FONT_FALLBACK = {"title": "黑体", "h1": "黑体", "h2": "楷体", "body": "仿宋"}

PLACEHOLDER = re.compile(r"(【[^】]*】)")
TABLE_RULE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")


def utf8_console() -> None:
    """Align stdout with a UTF-8 console code page so Chinese output is not mangled."""
    if os.name != "nt":
        return
    try:
        import ctypes

        if ctypes.windll.kernel32.GetConsoleOutputCP() == 65001:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def installed_fonts() -> set[str]:
    """Ask Word for the installed font list; return empty on any failure."""
    try:
        import win32com.client  # type: ignore

        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        try:
            return {str(name) for name in word.FontNames}
        finally:
            word.Quit()
    except Exception:
        return set()


def pick_fonts(overrides: dict[str, str], detect: bool) -> dict[str, str]:
    available = installed_fonts() if detect else set()
    chosen = {}
    for role, chain in FONT_CHAINS.items():
        if overrides.get(role):
            chosen[role] = overrides[role]
            continue
        hit = next((name for name in chain if name in available), None)
        chosen[role] = hit or FONT_FALLBACK[role]
    label = "detected" if available else "fallback (Word font list unavailable)"
    print("[fonts] %s" % label)
    for role in ("title", "h1", "h2", "body"):
        print("  %-5s -> %s" % (role, chosen[role]))
    return chosen


def set_run(run, eastasia: str, size: float, bold: bool = False, color=COLOR_BLACK):
    """Apply font, size and colour; Chinese glyphs come from w:eastAsia."""
    run.font.name = LATIN_FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr, value in (
        ("w:ascii", LATIN_FONT),
        ("w:hAnsi", LATIN_FONT),
        ("w:eastAsia", eastasia),
        ("w:cs", LATIN_FONT),
    ):
        rfonts.set(qn(attr), value)
    return run


def add_text(paragraph, text: str, eastasia: str, size: float, bold: bool = False) -> None:
    """Split on 【…】 placeholders so they always render bold red."""
    for segment in PLACEHOLDER.split(text):
        if not segment:
            continue
        if segment.startswith("【") and segment.endswith("】"):
            set_run(paragraph.add_run(segment), eastasia, size, True, COLOR_RED)
        else:
            set_run(paragraph.add_run(segment), eastasia, size, bold)


def shade(cell, fill: str) -> None:
    tcpr = cell._tc.get_or_add_tcPr()
    for old in tcpr.findall(qn("w:shd")):
        tcpr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def repeat_header(row) -> None:
    trpr = row._tr.get_or_add_trPr()
    flag = OxmlElement("w:tblHeader")
    flag.set(qn("w:val"), "true")
    trpr.append(flag)


def add_page_number(footer_paragraph, eastasia: str) -> None:
    """Page footer as a field:  — N —  (begin + instrText + end in one run)."""
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(footer_paragraph.add_run("— "), eastasia, 14)
    run = footer_paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, end):
        run._r.append(node)
    set_run(run, eastasia, 14)
    set_run(footer_paragraph.add_run(" —"), eastasia, 14)


def add_page_break(document) -> None:
    paragraph = document.add_paragraph()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    paragraph.add_run()._r.append(br)


def forecast(lines: list[str]) -> int:
    chars = sum(len(re.sub(r"\s", "", ln)) for ln in lines if not ln.strip().startswith("|"))
    tables = sum(1 for ln in lines if ln.strip().startswith("|")) // 3
    pages = round(chars / 600.0) + max(1, tables // 4)
    print("[forecast] body characters %d -> about %d page(s) at 600 chars/page" % (chars, max(1, pages)))
    return pages


def build(src: str, out: str, fonts: dict[str, str], body_pt: float, line_pt: float,
          page_numbers: bool) -> str:
    with open(src, "r", encoding="utf-8-sig") as fh:
        lines = fh.read().split("\n")
    forecast(lines)

    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    section.top_margin, section.bottom_margin = Cm(3.7), Cm(3.5)
    section.left_margin, section.right_margin = Cm(2.8), Cm(2.6)
    usable_cm = 21.0 - 2.8 - 2.6

    normal = document.styles["Normal"]
    normal.font.size = Pt(body_pt)
    normal.font.name = LATIN_FONT
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), fonts["body"])
    if page_numbers:
        add_page_number(section.footer.paragraphs[0], fonts["body"])

    def body_paragraph(before: float = 0, after: float = 0) -> object:
        paragraph = document.add_paragraph()
        fmt = paragraph.paragraph_format
        fmt.first_line_indent = Pt(body_pt * INDENT_MULT)
        fmt.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        fmt.line_spacing = Pt(line_pt)
        fmt.space_before = Pt(before)
        fmt.space_after = Pt(after)
        return paragraph

    index = 0
    numbered_items = 0
    title_written = False
    tables = 0

    while index < len(lines):
        raw = lines[index].rstrip()
        stripped = raw.strip()

        if not stripped:
            index += 1
            continue

        if raw.startswith("# ") and not raw.startswith("## "):
            if not title_written:
                paragraph = document.add_paragraph()
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.space_before = Pt(24)
                paragraph.paragraph_format.space_after = Pt(10)
                paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                paragraph.paragraph_format.line_spacing = Pt(38)
                add_text(paragraph, raw[2:].strip(), fonts["title"], TITLE_PT)
                title_written = True
            index += 1
            continue

        if raw.startswith("## ——") or raw.startswith("## --"):
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_after = Pt(22)
            paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            paragraph.paragraph_format.line_spacing = Pt(28)
            add_text(paragraph, raw[3:].strip(), fonts["h2"], SUBTITLE_PT, bold=True)
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and TABLE_RULE.match(lines[index + 1]):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                if not TABLE_RULE.match(lines[index]):
                    rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            if rows:
                columns = max(len(row) for row in rows)
                rows = [row + [""] * (columns - len(row)) for row in rows]
                table = document.add_table(rows=len(rows), cols=columns)
                table.style = "Table Grid"
                table.autofit = False
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                width = usable_cm / columns
                for row_index, row in enumerate(rows):
                    for column_index in range(columns):
                        cell = table.cell(row_index, column_index)
                        cell.width = Cm(width)
                        paragraph = cell.paragraphs[0]
                        paragraph.paragraph_format.space_before = Pt(1)
                        paragraph.paragraph_format.space_after = Pt(1)
                        paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                        if row_index == 0:
                            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            add_text(paragraph, row[column_index], fonts["body"], TABLE_PT, bold=True)
                            shade(cell, HEADER_FILL)
                        else:
                            add_text(paragraph, row[column_index], fonts["body"], TABLE_PT)
                repeat_header(table.rows[0])
                tables += 1
            continue

        if raw.startswith("## ") and not raw.startswith("### "):
            text = raw[3:].strip()
            if text.startswith("附"):
                add_page_break(document)
            numbered_items = 0
            paragraph = body_paragraph(12, 6)
            add_text(paragraph, text, fonts["h1"], body_pt)
            index += 1
            continue

        if raw.startswith("### "):
            numbered_items = 0
            paragraph = body_paragraph(8, 4)
            add_text(paragraph, raw[4:].strip(), fonts["h2"], body_pt, bold=True)
            index += 1
            continue

        if stripped.startswith(">"):
            paragraph = document.add_paragraph()
            fmt = paragraph.paragraph_format
            fmt.left_indent = Cm(0.7)
            fmt.right_indent = Cm(0.3)
            fmt.space_before, fmt.space_after = Pt(2), Pt(4)
            fmt.line_spacing = 1.25
            ppr = paragraph._p.get_or_add_pPr()
            border = OxmlElement("w:pBdr")
            left = OxmlElement("w:left")
            left.set(qn("w:val"), "single")
            left.set(qn("w:sz"), "18")
            left.set(qn("w:space"), "10")
            left.set(qn("w:color"), "1F4E79")
            border.append(left)
            ppr.append(border)
            add_text(paragraph, stripped.lstrip(">").strip(), fonts["body"], SUBTITLE_PT)
            index += 1
            continue

        match = re.match(r"^[-*]\s+(.*)$", stripped)
        if match:
            numbered_items += 1
            paragraph = body_paragraph()
            add_text(paragraph, "%d.%s" % (numbered_items, match.group(1)), fonts["body"], body_pt)
            index += 1
            continue

        paragraph = body_paragraph()
        add_text(paragraph, stripped, fonts["body"], body_pt)
        index += 1

    document.save(out)

    check = Document(out)
    characters = 0
    red_runs = 0
    blocks = [p for p in check.paragraphs]
    for table in check.tables:
        for row in table.rows:
            for cell in row.cells:
                blocks.extend(cell.paragraphs)
    for paragraph in blocks:
        characters += len(re.sub(r"\s", "", paragraph.text))
        red_runs += sum(
            1 for run in paragraph.runs if run.font.color and run.font.color.rgb == COLOR_RED
        )
    print("\n[out] %s" % os.path.abspath(out))
    print("[stat] paragraphs %d  tables %d  characters %d  forecast ~%d page(s)"
          % (len(check.paragraphs), len(check.tables), characters, max(1, round(characters / 600))))
    print("[stat] red placeholder runs: %d" % red_runs)
    print("[stat] table sizes: %s" % [(len(t.rows), len(t.columns)) for t in check.tables])
    print("\n[next] convert to PDF and inspect representative pages: "
          "python verify_docx_render.py %s" % os.path.basename(out))
    return out


def main(argv: list[str]) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Render marked-up text to official-format .docx")
    parser.add_argument("source", help="markup source file (.md or .txt)")
    parser.add_argument("output", help="target .docx path")
    parser.add_argument("--no-detect", action="store_true", help="skip Word font detection")
    parser.add_argument("--no-page-numbers", action="store_true", help="omit the page-number field")
    parser.add_argument("--body-pt", type=float, default=BODY_PT, help="body font size (default 16)")
    parser.add_argument("--line-pt", type=float, default=LINE_PT, help="exact line spacing (default 29)")
    for role in ("title", "h1", "h2", "body"):
        parser.add_argument("--%s-font" % role, default="", help="override the %s font" % role)
    args = parser.parse_args(argv)

    if not os.path.exists(args.source):
        print("[ERR] source not found: %s" % args.source)
        return 1

    overrides = {
        "title": args.title_font,
        "h1": args.h1_font,
        "h2": args.h2_font,
        "body": args.body_font,
    }
    fonts = pick_fonts(overrides, detect=not args.no_detect)
    build(
        args.source,
        args.output,
        fonts,
        body_pt=args.body_pt,
        line_pt=args.line_pt,
        page_numbers=not args.no_page_numbers,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
