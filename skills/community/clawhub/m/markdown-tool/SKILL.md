---
name: markdown-tool
description: Convert Markdown text to HTML and other formats. Use for documentation generation, content formatting, and text transformation.
---
# Markdown - Document Format Converter

Convert Markdown-formatted text to HTML with support for headings, lists, code blocks, tables, and inline formatting.

## Usage

```bash
markdown-tool [options] <file>
```

## Features

- Full CommonMark spec support
- Syntax highlighted code blocks
- Table of contents generation
- GitHub Flavored Markdown (GFM) extensions

## Examples

```bash
markdown-tool README.md > index.html
markdown-tool --toc doc.md
echo "# Hello" | markdown-tool
```