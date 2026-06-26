---
name: openclaw-pdf-reader
version: 1.0.0
description: Read, extract, and analyze PDF files. Use when the user needs to: (1) Extract text from PDF documents, (2) Analyze PDF content, (3) Summarize PDF documents, (4) Search for specific information in PDFs, (5) Extract tables from PDFs
---

# PDF Reader Skill

Extract and analyze content from PDF files using pdfplumber and PyMuPDF.

## Quick Start

For basic text extraction, use the provided script:

```bash
python scripts/extract_pdf.py <path-to-pdf>
```

## Capabilities

- **Text extraction** - Extract all text from PDF pages
- **Table extraction** - Extract tables as structured data
- **Metadata** - Get PDF metadata (author, pages, etc.)
- **Page-specific** - Extract from specific pages or ranges
- **Search** - Find specific text within PDF

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_pdf.py` | Extract text from PDF |
| `scripts/analyze_pdf.py` | Analyze and summarize PDF content |

## References

- `references/pdf-libraries.md` - Python PDF library documentation

## Usage Examples

**Extract all text:**
```
python scripts/extract_pdf.py document.pdf
```

**Extract specific page:**
```
python scripts/extract_pdf.py document.pdf --page 5
```

**Analyze and summarize:**
```
python scripts/analyze_pdf.py document.pdf
```
