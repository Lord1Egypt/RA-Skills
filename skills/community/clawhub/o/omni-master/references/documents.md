# Document Processing

## PDF Operations
- **nano-pdf** — Natural language PDF editing
- **pdfplumber** (Python) — Text/table extraction
- **PyPDF2/pypdf** — Merge, split, rotate, encrypt
- **reportlab** — PDF generation from scratch
- **OCR**: Tesseract for scanned documents

### PDF Workflows
```python
# Extract text
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())

# Merge PDFs
from pypdf import PdfMerger
merger = PdfMerger()
merger.append("a.pdf")
merger.append("b.pdf")
merger.write("merged.pdf")
```

## Word Documents (DOCX)
- **python-docx** — Create/edit .docx files
- Supports: paragraphs, tables, images, styles, headers
- Tracked changes and comments

## Spreadsheets
- **openpyxl** — Excel (.xlsx) read/write
- **gog** — Google Sheets API
- **pandas** — CSV/Excel data manipulation
- **csv** module — Simple CSV handling

## Presentations (PPTX)
- **python-pptx** — Create/edit presentations
- Slides, shapes, text, images, charts

## Markdown
- Direct file read/write
- Convert with pandoc: `pandoc input.md -o output.pdf`
- Obsidian-compatible markdown

## Notion & Obsidian
- **notion** skill — Pages, databases, blocks
- **obsidian** skill — Vault management

## Document Workflow
1. Identify format needed
2. Choose appropriate tool
3. Create/edit content
4. Export in desired format
5. Verify output quality

## Format Conversion Matrix
| From → To | Tool |
|---|---|
| MD → PDF | pandoc |
| MD → HTML | pandoc |
| DOCX → PDF | python-docx + reportlab |
| CSV → Excel | pandas + openpyxl |
| HTML → PDF | weasyprint / wkhtmltopdf |
| Image → PDF | img2pdf |
| PDF → Text | pdfplumber |
| PDF → Images | pdf2image (poppler) |
