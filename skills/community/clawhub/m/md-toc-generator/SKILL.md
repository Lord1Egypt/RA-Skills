---
name: md-toc-generator
description: Generate and update table-of-contents (TOC) sections for Markdown files. Use when working with long Markdown documents, READMEs, or technical docs that need a navigable TOC, or when asked to add/update a table of contents in a .md file.
---

# Markdown TOC Generator

Generate a table of contents from the headings in a Markdown file and insert or refresh it.

## Quick start

```bash
python3 scripts/generate_toc.py <path-to-file.md> [--max-depth 3] [--in-place]
```

- Without `--in-place`: prints the TOC to stdout.
- With `--in-place`: inserts the TOC right after the first heading (or updates an existing `<!-- toc -->` block).

## TOC placement

- If the file contains `<!-- toc -->` and `<!-- /toc -->` markers, the block between them is replaced.
- Otherwise the TOC is inserted immediately after the first `# ` heading.

## Anchor rules

- Lowercase the heading text.
- Replace spaces with hyphens.
- Strip punctuation except hyphens and underscores.
- Duplicate anchors get `-1`, `-2`, … suffixes.

## Examples

```bash
# Print TOC only
python3 scripts/generate_toc.py docs/guide.md

# Insert / refresh TOC in place
python3 scripts/generate_toc.py README.md --in-place --max-depth 4
```
