---
name: md2pdf
description: High-fidelity Markdown to PDF conversion with two pipelines: Pandoc + XeLaTeX for print-style documents, and browser-rendered HTML/Twemoji for emoji-heavy or WYSIWYG-friendly output. Use when users ask for polished PDF output from .md, want better visual quality than basic markdown renderers, need strong Chinese/CJK support, or specifically need emoji to survive PDF export.
---

# md2pdf

Produce polished, print-ready PDF from Markdown with a stable, reusable pipeline.

## Quick start

1. Install dependencies (Ubuntu/Debian):
   - `bash scripts/install_deps_ubuntu.sh`
2. Convert standard formal Markdown with Pandoc/XeLaTeX:
   - `bash scripts/md2pdf.sh input.md output.pdf`
3. Convert emoji-heavy or browser-like Markdown with CDP browser rendering:
   - `bash scripts/md2pdf-browser.sh input.md output.pdf`
4. Optional: enable cover page / metadata style via defaults:
   - `bash scripts/md2pdf.sh input.md output.pdf --defaults assets/defaults/hifi.yaml`

## Workflow

### 1) Choose the pipeline

Use the LaTeX pipeline when the document is mostly text/tables and should look print-formal.

Use the browser pipeline when any of these are true:

- emoji must render correctly
- HTML/CSS-like appearance matters more than TeX typography
- the Markdown contains GitHub-style formatting that is easier to preserve in HTML
- a CDP browser endpoint is already available

### 2) Prepare source markdown

- Prefer `#`/`##` heading hierarchy (for TOC quality).
- Keep code blocks fenced with language tags (for syntax highlight).
- Keep tables in GFM format.
- For very wide tables, prefer shorter cell content or convert the summary table to bullets before export.

### 3) Run the formal print pipeline

Use `scripts/md2pdf.sh` as the default entrypoint for print-style output.

It applies a professional baseline:

- `--pdf-engine=xelatex`
- Chinese font fallback (`Noto Sans CJK SC`)
- Table of contents (`--toc`)
- Section numbering (`--number-sections`)
- Reasonable margins / line spread / link coloring
- Code highlight style

### 4) Run the emoji-friendly browser pipeline

Use `scripts/md2pdf-browser.sh` when emoji support matters.

It does this:

- render Markdown to HTML
- convert emoji to Twemoji images
- connect to an existing CDP browser (`BROWSER_CDP_URL` or `http://127.0.0.1:9222`)
- print the page to PDF with browser CSS

Example:

- `BROWSER_CDP_URL=http://192.168.1.30:9222 bash scripts/md2pdf-browser.sh input.md output.pdf`

### 5) Tune output quality

Use either:

- CLI flags in `scripts/md2pdf.sh` (quick tuning), or
- defaults file (`assets/defaults/hifi.yaml`) for stable team-wide style.

Recommended adjustments:

- business report: keep `11pt`, margin `2.2cm`, TOC on
- printable manual: increase margin to `2.5cm`
- dense technical doc: keep section numbers and monospace code font
- emoji-heavy travel/share docs: prefer browser pipeline first

## Troubleshooting

- `pandoc: command not found`: run `scripts/install_deps_ubuntu.sh`.
- `xelatex not found`: ensure `texlive-xetex` installed, or switch to `scripts/md2pdf-browser.sh`.
- Emoji missing in PDF: use `scripts/md2pdf-browser.sh`; TeX engines are often poor at color emoji.
- CJK glyph squares/tofu: install `fonts-noto-cjk` and keep `CJKmainfont` as Noto Sans CJK.
- Browser script cannot connect: pass a valid CDP URL as arg 3 or set `BROWSER_CDP_URL`.
- Weird table wrapping: reduce table width in markdown or use bullets for wide summary tables.

## References

- Style baseline and knobs: `references/style-guide.md`
- Reusable defaults preset: `assets/defaults/hifi.yaml`
