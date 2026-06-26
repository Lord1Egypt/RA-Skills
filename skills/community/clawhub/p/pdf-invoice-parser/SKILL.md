---
name: pdf-invoice-parser
version: 1.0.0
description: Extract structured data from PDF invoices and documents. Handles scanned PDFs (OCR) and digital PDFs. Outputs clean CSV/Excel with vendor, invoice number, dates, line items, totals.
author: TKDigital
category: Data & Analytics
tags: [pdf, invoice, ocr, data-extraction, excel, document-processing]
---

# PDF Invoice Parser

**Use when:** You need to extract structured data from PDF invoices, receipts, or financial documents.

## Capabilities

- **Digital PDFs:** Direct text extraction from searchable PDFs
- **Scanned PDFs:** OCR via Tesseract for image-based PDFs
- **Invoice fields:** Vendor name, invoice number, invoice date, due date, line items, subtotal, tax, total
- **Output formats:** CSV, JSON, or Excel-ready TSV

## Quick Start

```bash
# Install dependencies
pip install --break-system-packages PyPDF2 pymupdf pillow pytesseract

# Parse a single invoice
python3 scripts/parse-invoice.py invoice.pdf --output invoice_data.csv

# Parse multiple invoices
python3 scripts/parse-invoices.py ./invoices/ --output consolidated.csv
```

## Usage

### Parse a single invoice

```bash
python3 scripts/parse-invoice.py path/to/invoice.pdf --output output.csv
```

### Parse a directory of invoices

```bash
python3 scripts/parse-invoices.py ./invoice_directory/ --output consolidated.xlsx
```

### With OCR (for scanned PDFs)

```bash
python3 scripts/parse-invoice.py scanned_invoice.pdf --ocr --output output.csv
```

## Extracted Fields

| Field | Description |
|-------|-------------|
| vendor_name | Company/issuer name |
| invoice_number | Invoice ID/reference |
| invoice_date | Date of invoice |
| due_date | Payment due date |
| line_items | Array of {description, quantity, unit_price, total} |
| subtotal | Pre-tax total |
| tax | Tax amount |
| total | Grand total |
| currency | Detected currency (USD, EUR, etc.) |

## Output Format

CSV columns:
```
vendor_name,invoice_number,invoice_date,due_date,description,quantity,unit_price,line_total,subtotal,tax,total,currency
```

Each line item becomes a row, with invoice-level fields repeated.

## Dependencies

- **PyPDF2** — Digital PDF text extraction
- **PyMuPDF (fitz)** — Advanced PDF rendering
- **Pillow** — Image processing for OCR
- **pytesseract** — OCR engine (requires tesseract-os installed)
- **openpyxl** — Excel output support

Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install -y tesseract-ocr

# macOS
brew install tesseract
```

## Limitations

- Complex table layouts may need manual review
- Handwritten text not supported
- Very low-quality scans may have reduced accuracy
- Multi-page invoices: each page parsed separately

## Example

Input: `invoice_1234.pdf`

Output (`output.csv`):
```
vendor_name,invoice_number,invoice_date,due_date,description,quantity,unit_price,line_total,subtotal,tax,total,currency
Acme Corp,INV-2026-0042,2026-03-15,2026-04-14,Widget A,10,25.00,250.00,250.00,25.00,275.00,USD
Acme Corp,INV-2026-0042,2026-03-15,2026-04-14,Widget B,5,40.00,200.00,250.00,25.00,275.00,USD
```

## Integration with MoltyWork

For MoltyWork projects requiring PDF data extraction:

1. Download PDFs from the project
2. Run `parse-invoices.py` on the directory
3. Upload the resulting CSV/Excel as the deliverable

```bash
python3 scripts/parse-invoices.py ./project_pdfs/ --output deliverable.xlsx
```
