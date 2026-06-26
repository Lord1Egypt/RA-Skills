---
name: html-markdown-hybrid
description: Combine high-quality Markdown to HTML rendering with robust HTML to Markdown extraction in one skill. Use when converting Markdown into nicer-looking standalone HTML pages, or when converting HTML files, raw HTML, URLs, and directories into clean Markdown with article/docs/forum cleanup profiles. Prefer the Python renderer for best-looking Markdown to HTML output, and use the Node pipeline for HTML to Markdown, batch mode, metadata, reports, and advanced profile-based cleanup.
---

# HTML Markdown Hybrid

## Overview

This skill combines the best parts of two separate tools:

- `scripts/pretty_markdown_to_html.py` for better-looking Markdown to HTML output
- `scripts/html_to_markdown.mjs` for stronger HTML to Markdown conversion, URL fetching, cleanup profiles, metadata, and reports
- `scripts/markdown_to_html.mjs` as an optional Node-based Markdown to HTML fallback when batch directory conversion or theme switching is more important than final polish

## Decision rule

Use this skill when the task is any of the following:
- turn Markdown into a presentable standalone HTML page
- convert a web page, raw HTML, or HTML file into clean Markdown
- batch-convert many Markdown or HTML files
- keep article-style readability cleanup or metadata during conversion
- compare conversion quality between a pretty renderer and a more configurable pipeline

## Recommended default path

### Markdown → HTML

Use the Python renderer first when visual output quality matters most.

```bash
python scripts/pretty_markdown_to_html.py input.md -o output.html --theme light --title "Document"
```

Use this for:
- AI日报转网页
- 文档展示页
- 报告、newsletter、分享页
- 任何最终要给人直接阅读的 HTML 页面

Why this is the default:
- it produces cleaner default styling
- it embeds CSS inline
- it is lighter and simpler to run
- this copy is patched to read and write UTF-8 explicitly on Windows

### HTML → Markdown

Use the Node pipeline first for HTML extraction and cleanup.

```bash
node scripts/html_to_markdown.mjs \
  --url "https://example.com/article" \
  --out ./article.md \
  --profile article \
  --engine best \
  --meta-frontmatter true \
  --report ./article.report.json
```

Use this for:
- 网页文章转 Markdown
- HTML 文件清洗后转 Markdown
- 批量转换目录
- URL 列表抓取转 Markdown

Read `references/profiles.md` when choosing `article`, `docs`, `forum`, or `custom`.

## Optional fallback: Markdown → HTML with Node

Use the Node renderer when you need directory batch conversion or its built-in themes.

```bash
node scripts/markdown_to_html.mjs \
  --file ./README.md \
  --out ./README.html \
  --theme github
```

Use it when:
- converting an entire markdown directory to HTML
- the `github` or `minimal` theme is specifically desired
- one workflow should stay entirely inside Node

Do not make this the first choice when the user explicitly cares most about frontend presentation quality.

## Quick chooser

- Best-looking Markdown page → `pretty_markdown_to_html.py`
- Web article to clean Markdown → `html_to_markdown.mjs --profile article`
- Docs portal to Markdown → `html_to_markdown.mjs --profile docs`
- Batch Markdown folder to HTML → `markdown_to_html.mjs --input-dir ... --output-dir ...`
- Need metadata/report/frontmatter → use the Node HTML to Markdown script

## Files in this skill

- `scripts/pretty_markdown_to_html.py`
- `scripts/html_to_markdown.mjs`
- `scripts/markdown_to_html.mjs`
- `references/profiles.md`
- `package.json`

## Setup notes

The Node scripts depend on packages listed in `package.json`.
If dependencies are not installed yet, run:

```bash
npm install
```

from the skill directory before using the Node scripts.

The Python renderer uses only the standard library and needs no extra dependencies.

## Practical recommendation

For the exact kind of comparison where the same AI news markdown was rendered two ways, prefer:
- Markdown source → `pretty_markdown_to_html.py`
- HTML/article source → `html_to_markdown.mjs`

That gives the stronger visual result in one direction and the stronger cleanup/extraction result in the other.
