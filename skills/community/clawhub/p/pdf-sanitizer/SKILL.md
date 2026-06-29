---
name: pdf-sanitizer
description: "Detect and redact sensitive information in PDFs — ID numbers, phone numbers, addresses, bank cards."
metadata:
  category: Document Processing
  priority: P0
  languages: zh-CN, en
---

# PDF Sanitizer

Detect and redact sensitive information in PDF documents while preserving original layout.

## Workflow

1. **Ingest PDF** — extract text layer and metadata via pdfplumber/PyMuPDF.
2. **Scan for PII** — run regex + AI pattern matching against Chinese and international PII:
   - Chinese ID number (18-digit)
   - Chinese phone numbers
   - Bank card numbers
   - Email addresses
   - Residential addresses (Chinese)
   - Person names (context-based)
3. **Highlight** — annotate every match with bounding boxes and category labels.
4. **Confirm** — present categories to user for selection. Default: all categories enabled.
5. **Redact** — apply chosen mode per category:
   - `blackout` — solid black rectangle over sensitive text
   - `blur` — pixel-level Gaussian blur on image-rendered area
   - `placeholder` — replace with `[REDACTED]` while keeping surrounding text
6. **Rebuild PDF** — flatten redactions into final output, preserving original fonts, images, and layout.
7. **Report** — output redacted PDF + JSON report listing each redaction:
   - original snippet (truncated), category, page number, bounding box, mode applied.

## Sample Prompt

```
pdf-sanitizer redact --input contract.pdf --categories id_card,phone,address --mode blackout
pdf-sanitizer redact --input 社保材料.pdf --output clean.pdf --categories all --mode placeholder
pdf-sanitizer scan --input report.pdf
pdf-sanitizer review --input contract.pdf --page 3-7
```
