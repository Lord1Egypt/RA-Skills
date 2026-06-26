---
name: pdf-generator
description: "Generate professional PDF documents from structured JSON data. Use when user wants to create, export, or save content as a PDF file. Supports styled titles, tables, lists, highlights, images, and page breaks. Trigger phrases: Export as PDF, Generate PDF, Create PDF report, Save as PDF, PDF erstellen, PDF generieren, als PDF speichern."
---

# PDF Generator

Generate styled PDF documents from structured JSON data using ReportLab.

## Quick Start

```bash
python scripts/generate_pdf.py --output report.pdf --data '{
  "title": "Monthly Report",
  "subtitle": "March 2026",
  "author": "PragDev",
  "sections": [
    {"type": "text", "text": "Introduction text here."},
    {"type": "highlight", "text": "Key metric: +15%"},
    {"type": "list", "items": ["Item 1", "Item 2"]}
  ]
}'
```

## JSON Schema Reference

See `references/schema.md` for complete schema documentation.

## Output

- PDF saved to path specified by `--output` or `data.output`
- Default: `output.pdf` in current directory

## Tips

- Use `accent_color` and `header_color` for brand colors
- Tables auto-alternate row backgrounds
- Images must exist at the specified path
- Page breaks create new pages