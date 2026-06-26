# Workflow

## Purpose

This skill converts Markdown into a faithful mobile long image.

The workflow is intentionally simple:

1. Resolve Markdown input
2. Render mobile HTML
3. Detect a local browser
4. Capture a full-page screenshot
5. Fall back to Playwright only if no local browser is available

## Input Modes

### Local File

```bash
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --input-file /absolute/path/to/article.md
```

### Pasted Markdown

```bash
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --markdown-text "# Title\n\nParagraph"
```

## Output Modes

### PNG

```bash
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --input-file /absolute/path/to/article.md \
  --format png \
  --output-image /absolute/path/to/article.mobile.png
```

### JPG

```bash
python3 {baseDir}/scripts/markdown_to_long_image.py \
  --input-file /absolute/path/to/article.md \
  --format jpg \
  --output-image /absolute/path/to/article.mobile.jpg
```

## What The Entry Script Produces

- normalized markdown path when text input is used
- rendered HTML file
- exported image file

## Rendering Defaults

- faithful article-style layout
- mobile-first content width
- strong readability
- preserved heading hierarchy
- preserved tables and images
- blockquotes styled for scanning
- full-page screenshot output
