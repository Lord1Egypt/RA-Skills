---
name: markdown-to-html
description: Convert a Markdown file or raw Markdown string into a polished HTML document. Supports custom Pandoc HTML templates, custom CSS, and includes built-in HTML template themes. Use this skill when the user asks to export Markdown to HTML, generate a beautiful web page from Markdown, or render Markdown into a branded standalone HTML file.
---

# Markdown To HTML

Use this skill when the user wants a Markdown file or Markdown string converted into a polished HTML page.

## What this skill provides

- Deterministic conversion through `pandoc`
- Input from either a Markdown file or a raw Markdown string
- Custom HTML template support through `--template /path/to/template.html`
- Custom CSS support through `--css /path/to/file.css`
- Built-in HTML themes in `assets/templates/` and `assets/styles/`
- Optional table of contents, numbered headings, metadata, and embedded assets

## Quick workflow

1. Choose the input source.
   File input: pass `--input-file /abs/path/file.md`
   Raw string input: pass `--markdown '...'`
2. Choose a layout.
   Use `--template` for a fully custom Pandoc HTML template.
   Otherwise use `--builtin-template`.
3. Optionally add one or more CSS files with `--css`.
4. Set output with `--output /abs/path/output.html`.
5. Optional layout flags:
   Use `--toc` to render a table of contents panel.
   Use `--no-body-background` to remove the article card background, border, and shadow.

## Built-in templates

- `docs-slate`: technical docs layout with restrained slate tones
- `magazine-amber`: editorial landing-page feel with warm contrast
- `product-midnight`: dark product narrative with stronger gradients
- `serif-paper`: print-inspired article layout

List them at runtime with:

```bash
python3 scripts/markdown_to_html.py --list-templates
```

## Main command

```bash
python3 scripts/markdown_to_html.py \
  --input-file /abs/path/source.md \
  --output /abs/path/output.html \
  --builtin-template docs-slate \
  --toc \
  --number-sections \
  --embed-assets
```

## Raw string example

```bash
python3 scripts/markdown_to_html.py \
  --markdown '# Release Notes\n\n- Added HTML export\n- Added built-in themes' \
  --output /abs/path/release.html \
  --builtin-template magazine-amber \
  --title 'Release Notes'
```

## Template rules

- `--template` overrides `--builtin-template`
- Built-in templates automatically include their matching built-in CSS
- Extra `--css` files are appended after the built-in CSS, so local overrides win
- `--number-sections` enables Pandoc heading numbering in the generated HTML
- When `--number-sections` is enabled, avoid manually writing heading prefixes like `1.`, `2.1`, or `3.2` inside the Markdown heading text, or the output will show duplicated numbering such as `1.2.1 2.1 Title`
- When `--toc` is omitted, the built-in templates render only the article body and expand it to the full content width
- `--no-body-background` removes the article panel background, border, and shadow while keeping the overall page theme

## Bundled files

- Converter: `scripts/markdown_to_html.py`
- Built-in templates: `assets/templates/*.html`
- Built-in CSS themes: `assets/styles/*.css`

## Notes

- This skill expects `pandoc` to be installed and available on `PATH`
- Custom templates should be valid Pandoc HTML templates and include `$body$`
- If you want a table of contents without visible heading numbers in the HTML body, use `--toc` without `--number-sections`
