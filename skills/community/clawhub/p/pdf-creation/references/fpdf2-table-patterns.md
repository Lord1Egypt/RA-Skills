# fpdf2 Table Patterns — Reference

API version: fpdf2 >= 2.8
Tested with: 2.8.7 (July 2026)

## Table Constructor Parameters

Context manager: `with pdf.table(...) as tbl:`

| Parameter | Type | Notes |
|-----------|------|-------|
| col_widths | list[float] | Column widths in mm. Sum must not exceed pdf.epw. |
| text_align | str | "LEFT", "CENTER", "RIGHT", "JUSTIFY" |
| first_row_as_headings | bool | True = first row styled via headings_style (default: True) |
| headings_style | FontFace | FontFace with family, emphasis, size_pt, color, fill_color |
| width | float | Total table width. Must be <= pdf.epw. Omit to use full epw. |
| borders_layout | str | "MINIMAL", "ALL", "NONE", "INTERNAL", "HORIZONTAL_LINES" |
| cell_fill_color | tuple | (R,G,B) for alternating row fills |
| cell_fill_mode | str | "NONE", "ROWS" (alters every other row), "COLUMNS" |
| line_height | float | Row height in mm |
| gutter_height | float | Extra space between rows (default 0) |
| gutter_width | float | Extra space between columns (default 0) |

## FontFace Constructor

```python
from fpdf import FontFace

ff = FontFace(
    family="DJS",        # font family name registered via add_font()
    emphasis="BOLD",     # "" = normal, "BOLD", "I" (italic), "BI" (bold italic)
    size_pt=8,           # font size in points
    color=(255,255,255), # RGB text color
    fill_color=(26,39,68), # RGB background color (for headings)
)
```

## Row Rendering

```python
with pdf.table(...) as tbl:
    for row_data in data:
        r = tbl.row()
        for cell_text in row_data:
            r.cell(
                cell_text,
                style=some_fontface,   # per-cell FontFace override
                align="LEFT",          # optional per-cell alignment override
                colspan=1,             # merge this many columns
                rowspan=1,             # merge this many rows
            )
```

## Parameter Naming Pitfalls

| Wrong (obsolete) | Right (current) |
|---|---|
| first_row_as_header | first_row_as_headings |
| uni=True on add_font() | Omit entirely (TTF fonts are always Unicode) |

## Effective Page Width

```python
epw = pdf.w - pdf.l_margin - pdf.r_margin
# For A4 (210mm) with 20mm margins: epw = 170mm
```

## Full Working Example

```python
from fpdf import FPDF, FontFace

FONT_DIR = "/usr/share/fonts/dejavu-sans-fonts"
pdf = FPDF("P", "mm", "A4")
pdf.add_font("DJS", "",  f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("DJS", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.set_margins(20, 18, 20)
pdf.add_page()
pdf.set_font("DJS", "B", 14)
pdf.cell(0, 8, "Module Reference Table")
pdf.ln(12)

hdr = FontFace(family="DJS", emphasis="BOLD", size_pt=8,
               color=(255,255,255), fill_color=(26,39,68))
cell = FontFace(family="DJS", emphasis="", size_pt=7.5, color=(26,32,44))

data = [
    ["Module",   "Function",     "Returns"],
    ["os.path",  "join",         "str"],
    ["json",     "loads",        "dict"],
    ["datetime", "today()",      "date object"],
]

with pdf.table(
    col_widths=[42, 50, 78],
    text_align="LEFT",
    first_row_as_headings=True,
    headings_style=hdr,
    width=170,
    borders_layout="MINIMAL",
    cell_fill_color=(247, 250, 252),
    cell_fill_mode="ROWS",
    line_height=4.5,
) as tbl:
    for row_data in data:
        r = tbl.row()
        for t in row_data:
            r.cell(t, style=cell)

pdf.output("reference_table.pdf")
```
