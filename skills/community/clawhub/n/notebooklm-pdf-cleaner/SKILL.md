---
name: notebooklm-pdf-cleaner
description: Create a presentation-ready copy of a NotebookLM-exported slide-deck PDF by masking the small visible NotebookLM footer badge at the bottom-right of each page. Use when the user wants a cleaner NotebookLM PDF export for sharing, presenting, or emailing. This skill is narrowly scoped to NotebookLM slide-deck PDFs and does not act as a general watermark-removal tool.
---

# NotebookLM PDF Cleaner

Use this skill for **NotebookLM slide-deck PDFs** that contain the small visible **NotebookLM** footer badge in the bottom-right corner.

## Default behavior

The default behavior is intentionally narrow and safe:
- keep the original PDF unchanged
- write a new `*-clean.pdf` copy
- mask the small bottom-right NotebookLM footer area on each page

It does **not** remove arbitrary watermarks or redesign slides.

## Script

```bash
python3 {baseDir}/scripts/clean_notebooklm_pdf.py /path/to/input.pdf
```

By default it writes:

```bash
/path/to/input-clean.pdf
```

## Useful flags

```bash
# Explicit output path
python3 {baseDir}/scripts/clean_notebooklm_pdf.py in.pdf --out out.pdf

# Inspect only (no output file written)
python3 {baseDir}/scripts/clean_notebooklm_pdf.py in.pdf --inspect

# Tune the bottom-right footer mask in PDF points (origin = bottom-left)
python3 {baseDir}/scripts/clean_notebooklm_pdf.py in.pdf --mask-x 1208 --mask-y 0 --mask-w 168 --mask-h 32

# Optional advanced hygiene flags
python3 {baseDir}/scripts/clean_notebooklm_pdf.py in.pdf --strip-metadata --strip-annots
```

## Safety checks

- Refuse non-PDF input
- Refuse overwrite of the source file
- Refuse overwrite of an existing output unless `--force` is used
- Keep metadata/annotation stripping **off by default**

## Defaults

The default mask is tuned for common 16:9 NotebookLM slide-deck exports:
- `mask-x = 1208`
- `mask-y = 0`
- `mask-w = 168`
- `mask-h = 32`

These values are scaled automatically for each page size.

## Recommended workflow

1. Keep the original PDF
2. Create `*-clean.pdf`
3. Spot-check page 1 and one later page
4. If needed, adjust the mask values and rerun
5. Share or email the cleaned copy
