---
name: markdown-to-pdf
description: Convert Markdown files to beautiful PDF documents. Supports custom styling, code highlighting, and multiple output options. Use when users need to convert MD to PDF for documentation, notes, reports, or sharing.
---

# markdown-to-pdf

## Overview

Convert Markdown text or files to professional-looking PDF documents. Uses `markdown` package to convert MD to HTML, then `wkhtmltopdf` to generate PDF. Supports code syntax highlighting and custom CSS styling.

## Features

- **Convert MD file to PDF**: Take a Markdown file and output a ready-to-share PDF
- **Standalone output**: Embeds all styles, no external dependencies
- **Code highlighting**: Automatic syntax highlighting for code blocks
- **Custom CSS**: Option to provide custom CSS for styling

## Dependencies

```bash
pip install markdown pygments
# You also need wkhtmltopdf installed:
# macOS: brew install wkhtmltopdf
# Ubuntu/Debian: sudo apt install wkhtmltopdf
```

## Usage

### Basic conversion
```bash
python3 scripts/convert.py input.md output.pdf
```

### With custom CSS
```bash
python3 scripts/convert.py --css custom.css input.md output.pdf
```

## Resources

### scripts/
- `convert.py` - Convert Markdown file to PDF

