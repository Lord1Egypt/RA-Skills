---
name: md2pdf
description: Convert Markdown files to PDF using Pandoc. Use when the user wants to export, convert, or generate a PDF from a .md file. Triggers: "convert md to pdf", "export pdf", "markdown to pdf", "generate pdf from markdown", "md to pdf", "导出PDF", "转成PDF", "markdown转pdf", "生成PDF".
---

# md2pdf

Convert Markdown files to beautifully typeset PDF using Pandoc + LaTeX.

## Prerequisites

- **pandoc** — `winget install pandoc` or <https://pandoc.org/installing.html>
- **LaTeX engine** — XeLaTeX recommended (bundled with TeX Live or MiKTeX). Install via:
  - `winget install MiKTeX` or <https://miktex.org/download>
  - Or `winget install TeXLive` for TeX Live

The script auto-detects available engines in order: `xelatex` > `lualatex` > `pdflatex`.

## Quick Start

Run the bundled script:

```bash
python scripts/md2pdf.py <input.md> [output.pdf]
```

Options:
- `--toc` — Include table of contents
- `--css <file>` — Apply custom CSS stylesheet
- `--highlight <style>` — Code highlight style (default: `tango`)

## Default Behavior

The script applies these defaults when using XeLaTeX/LuaLaTeX (the preferred engines):

- **CJK support**: SimSun (serif), SimHei (sans), Microsoft YaHei (mono)
- **Margin**: 1 inch all sides
- **Code blocks**: syntax highlighted with Pygments

## Workflow

1. Confirm the input `.md` file exists and is readable
2. Run `scripts/md2pdf.py` with appropriate options
3. If pandoc or LaTeX is missing, report the installation instructions to the user
4. Return the generated PDF path to the user (send the file if applicable)

## Advanced: Direct Pandoc Calls

For options not covered by the script, call pandoc directly:

```bash
# Custom LaTeX template
pandoc input.md -o output.pdf --pdf-engine=xelatex --template=custom.tex

# Specific page size
pandoc input.md -o output.pdf --pdf-engine=xelatex -V geometry:margin=2cm -V papersize:a4

# Metadata
pandoc input.md -o output.pdf --pdf-engine=xelatex -V title="My Report" -V author="Author"
```
