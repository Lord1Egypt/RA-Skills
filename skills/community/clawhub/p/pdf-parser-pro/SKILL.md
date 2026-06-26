---
name: pdf-to-markdown
description: Convert any PDF to Markdown, JSON, and HTML using OpenDataLoader. Supports digital PDFs, scanned PDFs with OCR, and complex layouts with table extraction and reading-order detection. Use when a user shares a PDF and wants it parsed into readable text, structured data, or searchable content.
metadata:
  {
    "openclaw": {
      "emoji": "📄",
      "homepage": "https://clawhub.com"
    }
  }
---

# pdf-to-markdown

Convert any PDF to **Markdown**, **JSON**, or **HTML** using OpenDataLoader PDF — the #1 ranked open-source PDF parser.

## Features

- **Markdown** — clean readable text with correct reading order
- **JSON** — structured data with bounding boxes, font sizes, page numbers
- **HTML** — rich HTML output preserving layout
- **OCR** — built-in OCR for scanned PDFs (80+ languages)
- **Tables** — complex table extraction (0.93 accuracy)
- **Reading order** — XY-Cut++ algorithm for multi-column layouts
- **No API key** — fully self-hosted, open-source

## Requirements

### Java 11+ (symlink setup)

OpenDataLoader requires Java. After installing, create a symlink so Python subprocesses can find it:

```bash
# Find your Java install
ls ~/jdk-*/bin/java 2>/dev/null || ls /opt/jdk*/bin/java 2>/dev/null

# Create symlink
ln -sf /path/to/java/bin/java ~/.local/bin/java
```

### Python 3.10+

```bash
pip install opendataloader-pdf
```

Or use the auto-install script (handles Java + Python automatically):

```bash
curl -fsSL https://raw.githubusercontent.com/opendataloader-project/opendataloader-pdf/main/scripts/install.sh | bash
```

## Usage

### CLI

```bash
# Basic — markdown + json output
pdf2md document.pdf ./output

# HTML + JSON output
pdf2md document.pdf ./output html,json

# Markdown only
pdf2md document.pdf ./output markdown
```

### Python

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path="document.pdf",
    output_dir="./output",
    format="markdown,json"
)
```

### Supported Input Formats

| Type | Example | OCR Needed |
|------|---------|------------|
| Digital PDF | Text-based PDFs | No |
| Scanned PDF | Image-only scans | Yes (built-in) |
| Tagged PDF | Accessibility PDFs | No |
| Multi-column | Academic papers | No |
| Tables | Data reports | No |

## Output Formats

### Markdown
Clean text with heading hierarchy, bullet lists, and paragraph structure.

### JSON
```json
{
  "file name": "document.pdf",
  "number of pages": 5,
  "author": "Author Name",
  "kids": [
    {
      "type": "heading",
      "level": "Doctitle",
      "page number": 1,
      "bounding box": [100.0, 744.5, 404.0, 773.1],
      "font": "Helvetica-Bold",
      "font size": 24.0,
      "content": "Document Title"
    },
    {
      "type": "paragraph",
      "page number": 1,
      "bounding box": [100.0, 676.8, 316.3, 713.0],
      "font": "Helvetica",
      "font size": 14.0,
      "content": "Paragraph text..."
    }
  ]
}
```

## Installation

### OpenClaw Skill Install

```bash
clawhub install pdf-to-markdown
```

### Manual Install

```bash
# Install dependencies
pip install opendataloader-pdf

# Make script executable
chmod +x scripts/pdf2md
```

## Architecture

```
PDF Input
    │
    ▼
OpenDataLoader PDF (JVM)
    │
    ├── PDFBox    ──► Text extraction + layout analysis
    ├── veraPDF   ──► PDF validation + structure
    └── Tesseract ──► OCR (scanned PDFs)
    │
    ▼
Output: Markdown / JSON / HTML
```

## Benchmark

| Metric | Score |
|--------|-------|
| Overall extraction accuracy | 0.90 |
| Table extraction accuracy | 0.93 |
| Processing speed (local) | 0.05s/page |

*Benchmarks on 200 real-world PDFs including multi-column and scientific papers.*

## Common Use Cases

- **RAG pipelines** — convert PDFs to chunkable markdown
- **Document parsing** — extract text from research papers
- **Accessibility** — convert PDFs to structured data
- **Data extraction** — pull tables from reports
- **Content migration** — PDF to markdown for wikis/docs

## See Also

- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) — upstream project
- [PDF/UA](https://pdfa.org) — PDF accessibility standard
- [veraPDF](https://verapdf.org) — PDF/A validator
