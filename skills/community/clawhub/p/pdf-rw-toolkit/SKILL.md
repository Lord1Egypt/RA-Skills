---
name: pdf
description: Read, extract, and generate PDF files. Use when user asks to read PDF content, extract text/tables, merge PDFs, fill forms, or generate PDFs from HTML/Markdown.
metadata:
  openclaw:
    requires:
      bins: [python3]
      pip: [pdfplumber, pypdf, weasyprint]
---

# PDF Skill

Read, extract, analyze, and generate PDF documents.

## Capabilities

- **Extract text** from PDF (full or per-page)
- **Extract tables** from PDF as CSV/JSON
- **Get metadata** (title, author, pages, etc.)
- **Merge** multiple PDFs into one
- **Split** PDF by page ranges
- **Generate PDF** from HTML or Markdown
- **Fill PDF forms**

## Scripts

All scripts are in `scripts/` relative to this skill directory.

### Read / Extract

```bash
# Extract all text
python3 scripts/pdf_read.py <file.pdf>

# Extract text from specific pages (1-indexed)
python3 scripts/pdf_read.py <file.pdf> --pages 1,3,5-10

# Extract tables as CSV
python3 scripts/pdf_read.py <file.pdf> --tables --format csv

# Extract tables as JSON
python3 scripts/pdf_read.py <file.pdf> --tables --format json

# Get PDF metadata and page count
python3 scripts/pdf_read.py <file.pdf> --info
```

### Merge / Split

```bash
# Merge multiple PDFs
python3 scripts/pdf_merge.py output.pdf input1.pdf input2.pdf input3.pdf

# Split: extract specific pages
python3 scripts/pdf_split.py input.pdf output.pdf --pages 1,3,5-10
```

### Generate

```bash
# Generate PDF from HTML file
python3 scripts/pdf_generate.py input.html output.pdf

# Generate PDF from HTML string
python3 scripts/pdf_generate.py --html "<h1>Hello</h1><p>World</p>" output.pdf

# Generate PDF from Markdown (converted to HTML first)
python3 scripts/pdf_generate.py input.md output.pdf
```

## Usage Notes

- For large PDFs, use `--pages` to limit extraction scope
- Table extraction works best with well-structured tables; complex layouts may need manual cleanup
- PDF generation via WeasyPrint supports CSS styling — pass a `--css` file for custom styles
- All paths can be absolute or relative to the workspace
