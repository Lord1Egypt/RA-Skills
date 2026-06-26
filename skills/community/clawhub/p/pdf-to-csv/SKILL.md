---
name: pdf-to-csv
description: "Extract tables and text from a PDF into CSV format via the PDFAPIHub cloud API. PDFs are uploaded to pdfapihub.com for processing. Requires a CLIENT-API-KEY header."
metadata: {"openclaw": {"primaryEnv": "PDFAPIHUB_API_KEY", "requires": {"env": ["PDFAPIHUB_API_KEY"]}}}
---

# PDF to CSV

## What It Does
Extracts tables and text from a PDF into CSV format via the PDFAPIHub hosted API. Your PDF is uploaded to PDFAPIHub servers for processing and the extracted CSV is returned. Uses structured table detection when available.

## When to Use
- Extract tabular data from a PDF as CSV for data processing
- Pull invoice line items or report data into CSV

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- `file` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
This skill calls the PDFAPIHub hosted API at `https://pdfapihub.com/api`. Your PDF is sent to PDFAPIHub servers for table extraction.

Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

**Privacy note:** PDFs you process are uploaded to PDFAPIHub's cloud service. Do not send confidential documents unless you trust the service. Files are auto-deleted after 30 days.

## Use Cases
- **Data Pipeline Ingestion** — Extract PDF table data as CSV for import into databases or BI tools
- **CRM Import** — Pull contact lists from PDF exports into CSV for CRM import
- **Inventory Management** — Convert PDF inventory reports to CSV for spreadsheet tracking
- **Research Data** — Extract experimental data from PDF papers into CSV for analysis
- **Automated ETL** — Feed PDF-extracted CSV data into automated data processing pipelines

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/convert/pdf/csv \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://pdfapihub.com/sample-pdfinvoice-with-image.pdf", "output": "url" }'
```
