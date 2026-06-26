---
name: markdown-mobile-export
description: >-
  Use when a task needs a local Markdown file path or pasted Markdown text
  converted into a faithful mobile-friendly PNG/JPG long image for
  phone-readable articles, guides, notes, or reports, with HTML kept beside
  the image for inspection.
argument-hint: "[--input-file path | --markdown-text text]"
metadata:
  version: 0.1.0
---

# Markdown Mobile Export

Faithful Markdown → mobile long image, no content rewriting.

## When to Use

- Local `.md` file → phone-friendly long image
- Pasted Markdown text → PNG or JPG
- Article-style faithful export (not poster or carousel redesign)
- Intermediate HTML needed for inspection alongside image

## Do Not Use

- Poster redesigns where content should be rewritten into marketing blocks
- Carousel slicing across multiple images
- Rich web app UI design work
- PDF output

## Quick Start

```bash
# From file
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --input-file /path/to/file.md

# From pasted text
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --markdown-text "# Title\n\nBody"

# Custom output path and format
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --input-file /path/to/file.md \
  --output-image /path/to/output.png \
  --format jpg
```

## Defaults

| Aspect  | Default                                              |
|---------|------------------------------------------------------|
| Input   | Markdown file path or pasted text                    |
| Output  | PNG long image + HTML sidecar retained on disk       |
| Style   | Faithful conversion, mobile-first, zh-CN typography  |
| Width   | 820px card layout with warm earth-tone theme         |
| Browser | Local Chrome/Chromium/Edge/Brave → Playwright fallback |

## Workflow

1. Resolve input (`--input-file` or `--markdown-text`)
2. Normalize pasted text into a concrete `.source.md` file when needed
3. Render mobile-friendly HTML with embedded CSS
4. Detect local Chromium-family browser
5. Capture full-page screenshot (segmented stitch with overlap)
6. Fall back to Playwright Chromium if no local browser is usable
7. Print JSON result with `output_html` and `output_image` paths

## Scripts

| Script                                  | Purpose                              |
|-----------------------------------------|--------------------------------------|
| `scripts/markdown_to_long_image.py`     | CLI entry point, orchestrates pipeline |
| `scripts/render_markdown_mobile_long_image.py` | Markdown → styled mobile HTML  |
| `scripts/export_long_image.py`          | Browser detection + screenshot export |

## References

| Topic            | File                           |
|------------------|--------------------------------|
| Pipeline details | `references/workflow.md`       |
| Common issues    | `references/troubleshooting.md` |

## Validation

After generating output, verify:

1. HTML file exists at reported path
2. Image file exists and is non-zero bytes
3. Image is full-page capture (not single viewport crop)
4. Remote images loaded without broken placeholders
