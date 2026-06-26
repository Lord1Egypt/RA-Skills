---
name: markdown-export
description: Convert a Markdown file or raw Markdown string into polished DOCX or HTML output from one unified skill. Supports custom DOCX reference templates, custom Pandoc HTML templates, custom CSS, and includes built-in templates for both formats. Use this skill when the user asks to export Markdown into Word, HTML, or multiple publication formats from the same source.
---

# Markdown Export

Use this skill when the user wants one Markdown source exported into `docx`, `html`, or both.

## What this skill provides

- One unified CLI for both `docx` and `html`
- Input from either a Markdown file or a raw Markdown string
- Built-in templates for both output formats
- Custom template support for both output formats
- Optional table of contents, numbered headings, metadata, and resource-path support
- HTML layout controls for optional TOC panel and plain article body rendering

## Formats

- `docx`
  Uses a Word `reference.docx` style template
- `html`
  Uses a Pandoc HTML template plus CSS

## Built-in template names

### DOCX

- `modern-blue`
- `executive-serif`
- `warm-notebook`
- `minimal-gray`

### HTML

- `docs-slate`
- `magazine-amber`
- `product-midnight`
- `serif-paper`

List everything with:

```bash
python3 scripts/export_markdown.py --list-templates
```

Only list one format with:

```bash
python3 scripts/export_markdown.py --format html --list-templates
```

## Main examples

### Markdown to DOCX

```bash
python3 scripts/export_markdown.py \
  --format docx \
  --input-file /abs/path/source.md \
  --output /abs/path/output.docx \
  --builtin-template modern-blue \
  --toc \
  --number-sections
```

### Markdown to HTML

```bash
python3 scripts/export_markdown.py \
  --format html \
  --input-file /abs/path/source.md \
  --output /abs/path/output.html \
  --builtin-template docs-slate \
  --toc \
  --embed-assets
```

### Markdown to HTML Without TOC Background Card

```bash
python3 scripts/export_markdown.py \
  --format html \
  --input-file /abs/path/source.md \
  --output /abs/path/output.html \
  --builtin-template docs-slate \
  --embed-assets \
  --no-body-background
```

### Raw string

```bash
python3 scripts/export_markdown.py \
  --format html \
  --markdown '# Release Notes\n\n- Export to both HTML and DOCX with one skill' \
  --output /abs/path/release.html \
  --builtin-template magazine-amber \
  --title 'Release Notes'
```

## Template rules

- `docx`
  `--template` must point to a `.docx` reference document
- `html`
  `--template` must point to a Pandoc HTML template that contains `$body$`
- For HTML, built-in CSS is automatically applied when using a built-in template
- For HTML, extra `--css` files are appended after built-in CSS
- For HTML, omitting `--toc` removes the TOC panel and expands the article body to full width
- For HTML, `--no-body-background` removes the article panel background, border, and shadow while keeping the page theme

## Bundled files

- Unified converter: `scripts/export_markdown.py`
- DOCX built-in templates: `assets/docx/templates/*.docx`
- HTML built-in templates: `assets/html/templates/*.html`
- HTML built-in styles: `assets/html/styles/*.css`

## Notes

- This skill expects `pandoc` to be installed and available on `PATH`
- If the user already has a brand template, prefer passing `--template`
