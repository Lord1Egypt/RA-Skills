---
name: pdf-creation
description: fpdf2 PDF creation — Unicode-safe alternative to reportlab.
version: 1.0.0
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
    requires:
      bins: [python3]
---

# PDF Creation — fpdf2 Alternative

Use when reportlab is unavailable (PIL dependency conflict in alternate
venvs, uv-managed Python), or when you need a lighter-weight path to
Unicode-aware searchable-text PDFs.

## When to Choose fpdf2 Over reportlab

| Situation | Pick |
|-----------|------|
| Complex multi-page styled docs with tables, headers, footers | reportlab (Platypus) |
| PIL/Imaging not available or version conflict | fpdf2 |
| Need Unicode without configuring custom fonts | fpdf2 (register a TTF font) |
| Simple docs, fast iteration | fpdf2 |

## Prerequisites

```bash
pip install fpdf2
```

Also install a Unicode-capable TTF font (fpdf2's built-in Helvetica/Times/Courier
only cover Latin-1 — they raise FPDFUnicodeEncodingException on any character
outside that range). Available on most Linux:
`/usr/share/fonts/dejavu-sans-fonts/` or `/usr/share/fonts/truetype/dejavu/`.

## Quickstart

```python
from fpdf import FPDF
FONT_DIR = "/usr/share/fonts/dejavu-sans-fonts"
pdf = FPDF("P", "mm", "A4")
pdf.add_font("DJS", "",  f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("DJS", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.add_font("DJS", "I", f"{FONT_DIR}/DejaVuSans-Oblique.ttf")
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_font("DJS", "B", 26)
pdf.cell(0, 10, "Title", align="C")
pdf.ln(12)
pdf.set_font("DJS", "", 9.5)
pdf.multi_cell(0, 5, "Unicode-safe text with em-dashes and arrows.")
pdf.output("output.pdf")
```

## Tables (fpdf2 >= 2.8)

Uses context manager + FontFace for styling.

Key API points:
| Parameter | Notes |
|-----------|-------|
| first_row_as_headings=True | NOT first_row_as_header (was renamed) |
| headings_style=FontFace(...) | FontFace with family, emphasis, size_pt, color, fill_color |
| cell_fill_mode="ROWS" | Alternating row background |
| cell_fill_color=(R,G,B) | RGB tuple for alternating rows |
| width= | Must be <= pdf.epw (effective page width) |

```python
from fpdf import FPDF, FontFace
FONT_DIR = "/usr/share/fonts/dejavu-sans-fonts"
pdf = FPDF("P", "mm", "A4")
pdf.add_font("DJS", "",  f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("DJS", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.set_margins(20, 18, 20)
pdf.add_page()

hdr = FontFace(family="DJS", emphasis="BOLD", size_pt=8,
               color=(255,255,255), fill_color=(26,39,68))
cell = FontFace(family="DJS", emphasis="", size_pt=7.5, color=(26,32,44))

with pdf.table(col_widths=[42,50,84], text_align="LEFT",
    first_row_as_headings=True, headings_style=hdr, width=170,
    borders_layout="MINIMAL", cell_fill_color=(247,250,252),
    cell_fill_mode="ROWS", line_height=4.5) as tbl:
    for row in [["Module","Function","Returns"],["os.path","join","str"]]:
        r = tbl.row()
        for t in row:
            r.cell(t, style=cell)
pdf.output("table.pdf")
```

## Pitfalls

- Built-in fonts (Helvetica, Times, Courier) do NOT support Unicode. Em-dash,
  arrows, bullets raise FPDFUnicodeEncodingException. Must register a TTF
  Unicode font for non-ASCII text.
- fpdf2 >= 2.5: uni=True on add_font() is deprecated and unnecessary.
- pillow is optional. Missing it gives a harmless warning; images unavailable
  but text/tables work.
- Table width must not exceed pdf.epw or ValueError is raised.
- Coordinates: top-left origin, mm — unlike reportlab's bottom-left points.
- Row.cell() does NOT accept fill_color directly. Use table-level
  cell_fill_color/cell_fill_mode for rows and headings_style for headers.
