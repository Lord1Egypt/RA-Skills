---
name: md-2-html
description: Convert Markdown files to formatted HTML. Use when the user asks to convert, export, or save a Markdown file as HTML format. Triggers on phrases like "convert md to html", "markdown to html", "转成html", "md转html", "markdown转html". Also useful for AI content pipelines that generate Markdown but need browser-ready HTML output.
---

# Markdown to HTML Converter

Convert Markdown files or strings to well-formatted HTML, suitable for web display or CMS publishing.

## Quick Start

```bash
node scripts/md2html.js <input.md> [output.html]
```

**Or via stdin:**

```bash
echo "# Hello World" | node scripts/md2html.js -
```

**Or as a Node.js module:**

```javascript
var converter = require('./scripts/md2html.js');
var html = converter.markdownToHtml(markdownString);
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `input.md` | Yes | Path to source Markdown file, or `-` for stdin |
| `output.html` | No | Output path (defaults to input name with .html) |

## Supported Markdown Features

| Feature | Markdown Syntax | HTML Output |
|---------|----------------|-------------|
| Headings | `# h1` through `###### h6` | `<h1>` through `<h6>` |
| Bold | `**text**` | `<strong>text</strong>` |
| Italic | `*text*` | `<em>text</em>` |
| Inline code | `` `code` `` | `<code>code</code>` |
| Code blocks | ` ```lang ``` ` | `<pre><code class="language-lang">` |
| Links | `[text](url)` | `<a href="url" target="_blank">text</a>` |
| Images | `![alt](url)` | `<img src="url" alt="alt">` |
| Unordered lists | `- item` or `* item` | `<ul><li>item</li></ul>` |
| Ordered lists | `1. item` | `<ol><li>item</li></ol>` |
| Blockquotes | `> text` | `<blockquote><p>text</p></blockquote>` |
| Horizontal rule | `---` or `***` | `<hr>` |
| Paragraphs | Blank line separation | `<p>text</p>` |

## Design Principles

- **Zero dependencies** — Pure Node.js, works with v0.12+ (no npm install needed)
- **CMS-friendly** — Output is clean HTML suitable for direct database insertion
- **No wrapper HTML** — Outputs content HTML only (no `<html>`, `<head>`, `<body>`)
- **Safe escaping** — Code blocks escape `<` and `>` to prevent XSS

## Typical Use Cases

1. **AI Content Pipeline** — LLM generates Markdown → convert to HTML → publish to CMS
2. **Static site generation** — Batch convert `.md` files to `.html`
3. **Documentation** — Convert README.md to HTML for web display

## Pipeline Integration Example

For automated AI content pipelines that generate Markdown but publish HTML:

```javascript
var converter = require('./scripts/md2html.js');
var rawMarkdown = llmResponse.choices[0].message.content;
var htmlContent = converter.markdownToHtml(rawMarkdown);
// Now publish htmlContent to your CMS API
```