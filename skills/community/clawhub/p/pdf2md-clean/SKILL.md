---
name: pdf2md-clean
version: 1.0.0
description: "Convert PDF to Markdown using local processing. No external API calls."
license: MIT-0
author: lifei68801
tags: [pdf, markdown, conversion, local]
---

# PDF to Markdown Converter

Convert PDF documents to clean Markdown format using local processing only.

## Quick Start

```bash
python scripts/pdf2md.py input.pdf output.md
```

## Features

- **Local Processing**: No API calls, no network requests
- **Smart Formatting**: Auto-detect headers and lists
- **Clean Output**: Properly formatted Markdown

## Requirements

```bash
pip install pdfplumber
```

## Usage

```bash
# Basic usage
python scripts/pdf2md.py document.pdf

# Specify output file
python scripts/pdf2md.py document.pdf output.md
```

## How It Works

1. Extracts text from PDF using pdfplumber
2. Cleans up formatting issues
3. Detects headers and lists
4. Outputs clean Markdown

## Metadata

```yaml
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      pypi: ["pdfplumber"]
    permissions:
      - "file:read"
      - "file:write"
    behavior:
      network: none
      telemetry: none
      description: "Converts PDF to Markdown using local pdfplumber. No network requests."
```
