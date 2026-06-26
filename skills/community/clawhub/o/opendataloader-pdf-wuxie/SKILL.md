---
name: opendataloader-pdf
description: PDF parsing tool for AI/RAG. Convert PDF to Markdown, JSON, HTML with layout preservation, bounding boxes, and image extraction. Use when you need to extract content from PDF files for AI processing, RAG pipelines, or document analysis.
metadata:
  {
    "author": "wuxie-guru",
    "version": "1.0.0",
    "license": "MIT",
    "homepage": "https://github.com/opendataloader-project/opendataloader-pdf",
    "tags": ["pdf", "parser", "markdown", "json", "rag", "document"]
  }
---

# opendataloader-pdf Skill

PDF parsing tool for AI/RAG scenarios. Converts PDF to Markdown, JSON, HTML with layout preservation.

## Installation

```bash
pipx install opendataloader-pdf
```

Requires Java runtime (bundled JAR is included).

## Quick Usage

```bash
# PDF to Markdown (most common)
opendataloader-pdf input.pdf -o output_dir -f markdown

# PDF to JSON (with bounding boxes)
opendataloader-pdf input.pdf -o output_dir -f json

# Multiple formats at once
opendataloader-pdf input.pdf -o output_dir -f json,markdown,html

# Extract specific pages
opendataloader-pdf input.pdf -o output_dir -f markdown --pages "1,3,5-10"

# Extract images
opendataloader-pdf input.pdf -o output_dir -f markdown --image-dir images/

# Use PDF structure tree (for tagged PDFs)
opendataloader-pdf input.pdf -o output_dir -f markdown --use-struct-tree

# Output to stdout
opendataloader-pdf input.pdf -f markdown --to-stdout
```

## Output Formats

| Format | Description |
|--------|-------------|
| `json` | Structured JSON with bounding boxes, fonts, reading order |
| `markdown` | Markdown text with images as references |
| `html` | HTML with styling |
| `text` | Plain text |
| `pdf` | Rebuilt PDF |
| `markdown-with-html` | Markdown with HTML for complex elements |
| `markdown-with-images` | Markdown with embedded base64 images |

## Key Options

| Option | Description |
|--------|-------------|
| `--pages` | Page range, e.g., "1,3,5-10" |
| `--image-dir` | Directory for extracted images |
| `--use-struct-tree` | Use PDF structure tree for reading order |
| `--table-method` | Table detection: `default` (border-based) or `cluster` |
| `--reading-order` | Algorithm: `off` or `xycut` (default) |
| `--hybrid` | Hybrid AI mode: `docling-fast` for complex tables |
| `--sanitize` | Remove sensitive data (emails, phones, etc.) |
| `--include-header-footer` | Include page headers/footers |

## Examples

### Basic Conversion

```bash
# Convert to markdown
opendataloader-pdf document.pdf -o ./output -f markdown

# Convert to JSON with structure
opendataloader-pdf document.pdf -o ./output -f json --use-struct-tree
```

### Batch Processing

```bash
# Multiple files
opendataloader-pdf "file1.pdf" "file2.pdf" "folder/" -o output/

# All PDFs in directory
opendataloader-pdf ./pdfs/ -o ./output/ -f markdown
```

### Advanced Options

```bash
# Use AI hybrid mode for complex tables
opendataloader-pdf input.pdf -o output/ -f markdown --hybrid docling-fast

# Extract only pages 1-5
opendataloader-pdf input.pdf -o output/ -f markdown --pages "1-5"

# Sanitize sensitive data
opendataloader-pdf input.pdf -o output/ -f json --sanitize
```

## Performance Notes

- Each `convert()` call spawns a JVM process
- For batch processing, pass multiple files in one call
- ~6 seconds for typical 300-page PDF
- Images extracted to `{output_name}_images/` directory

## Troubleshooting

### Java not found
Ensure Java runtime is installed. The tool bundles its own PDFBox JAR.

### Font warnings
Warnings about missing fonts are normal and don't affect output quality.

### Slow performance
Use batch mode (multiple files in one call) instead of calling repeatedly.
