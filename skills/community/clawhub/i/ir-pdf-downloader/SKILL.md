---
name: ir-pdf-downloader
description: Discover and download static PDF files from Investor Relations (IR) sites, including annual reports and quarterly result PDFs. Use when the task is to find a PDF URL, probe common IR PDF paths, query Wayback for archived PDF links, or download a known static PDF document. Do not use for structured SEC/XBRL financial analysis; use sec-finance for that.
---

# IR PDF Downloader

Use this skill for **documents**, not financial metrics.

## Scope

- Find likely PDF URLs from an IR domain
- Search Wayback Machine for archived PDF links
- Use SEC EDGAR only as a **PDF discovery** source
- Download known static PDF URLs with proper headers

## Do not use this skill for

- Revenue / net income / EPS analysis
- SEC XBRL/companyfacts queries
- Filing data normalization

Use `sec-finance` for those.

## Core commands

```bash
# Download a known static PDF URL
python3 scripts/download_ir_pdf.py "https://ir.jd.com/static-files/..."

# Discover likely PDFs from an IR domain
python3 scripts/find_ir_pdf.py --domain ir.baidu.com --year 2024

# Search by company alias (uses shared issuer map when available)
python3 scripts/find_ir_pdf.py --company Alibaba

# Search only Wayback
python3 scripts/find_ir_pdf.py --domain ir.alibabagroup.com --sources wayback
```

## Workflow

1. If the PDF URL is already known, use `download_ir_pdf.py` directly.
2. If only the company or IR domain is known, use `find_ir_pdf.py` to discover likely URLs.
3. If discovery succeeds, pass the resulting URL to `download_ir_pdf.py`.
4. If the user actually wants structured financial numbers rather than the document itself, stop and switch to `sec-finance`.

## Notes

- Issuer hints for aliases, IR domains, and validated CIKs live in `references/issuers.json`.
- Keep this skill focused on **PDF discovery and download**.
- Do not duplicate structured-finance guidance here.
