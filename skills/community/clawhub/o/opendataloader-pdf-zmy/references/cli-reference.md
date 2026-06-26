# OpenDataLoader PDF — CLI Reference

## Basic CLI

```bash
# Single file
opendataloader-pdf document.pdf

# Multiple files + folder
opendataloader-pdf file1.pdf file2.pdf folder/

# Output to specific directory
opendataloader-pdf document.pdf -o output/
```

## Hybrid Mode (AI-Enhanced Parsing)

Hybrid mode requires a backend server running first:

```bash
# Terminal 1: Start backend
opendataloader-pdf-hybrid --port 5002

# Terminal 2: Process PDFs
opendataloader-pdf --hybrid docling-fast document.pdf
```

### Backend Options

```bash
# Standard hybrid backend
opendataloader-pdf-hybrid --port 5002

# Force OCR on all pages (scanned PDFs)
opendataloader-pdf-hybrid --port 5002 --force-ocr

# Specific OCR languages (comma-separated)
opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "chi_sim,eng"

# Extract math formulas as LaTeX
opendataloader-pdf-hybrid --enrich-formula

# AI description for charts/images
opendataloader-pdf-hybrid --enrich-picture-description

# Combine multiple enrichments
opendataloader-pdf-hybrid --port 5002 --force-ocr --enrich-formula --enrich-picture-description
```

### Hybrid Backend Flags

| Flag | Description |
|------|-------------|
| `--port` | Backend port (default: 5002) |
| `--force-ocr` | Force OCR on all pages |
| `--ocr-lang` | OCR languages, comma-separated |
| `--enrich-formula` | Extract formulas as LaTeX |
| `--enrich-picture-description` | AI describe charts/images |

### Processing Flags

```bash
# Fast hybrid (default)
opendataloader-pdf --hybrid docling-fast document.pdf

# Full hybrid (with formula + chart enrichment)
opendataloader-pdf --hybrid docling-fast --hybrid-mode full document.pdf

# Sanitize output (remove prompt injection)
opendataloader-pdf document.pdf --sanitize

# Use PDF structure tree (if available)
opendataloader-pdf document.pdf --use-struct-tree

# Custom output directory
opendataloader-pdf document.pdf -o ./output/

# Multiple output formats
opendataloader-pdf document.pdf -o ./output/ --format json --format markdown
```

## Output Formats

```bash
# Markdown only
opendataloader-pdf document.pdf --format markdown

# JSON only (with bounding boxes)
opendataloader-pdf document.pdf --format json

# Multiple formats at once
opendataloader-pdf document.pdf --format json --format markdown --format html

# Image output modes
opendataloader-pdf document.pdf --image-output embedded   # Base64 in JSON
opendataloader-pdf document.pdf --image-output external    # Separate image files
opendataloader-pdf document.pdf --image-output off       # No images (default)
```

## Environment Variables

```bash
# Java path (if not on PATH)
export JAVA_HOME=/path/to/java11

# Hybrid backend URL (for remote processing)
export OPENDATALOADER_HYBRID_URL=http://localhost:5002
```
