---
name: pdf-to-xlsx
description: "Extract tables and text from a PDF into an Excel workbook (XLSX). Each page becomes a separate sheet."
---

# PDF to Excel

## What It Does
Extracts tables and text from a PDF into an Excel workbook. Each page becomes a separate sheet. Uses PyMuPDF table detection with fallback to line-by-line text extraction.

## When to Use
- Extract tabular data from PDF invoices or reports
- Convert PDF financial statements to Excel
- Pull structured data from PDF tables

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- `file` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Invoice Data Extraction** — Pull line items and totals from PDF invoices into Excel for accounting
- **Financial Statement Analysis** — Convert PDF bank statements to Excel for analysis and reconciliation
- **Report Data Mining** — Extract tabular data from PDF reports for further processing
- **Procurement** — Convert PDF purchase orders into spreadsheets for tracking
- **Tax Preparation** — Extract financial data from PDF tax documents into Excel

## Aliases
- `/v1/convert/pdf/excel` is an alias

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/pdf/xlsx \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://pdfapihub.com/sample-pdfinvoice-with-image.pdf", "output": "url" }'
```
