---
name: ledgerai
description: AI bookkeeping via LedgerAI API — invoice processing, expense categorization, financial reports, receipt scanning. Use when user needs automated bookkeeping, invoice parsing, expense tracking, financial report generation, or receipt processing. Free tier available (100 req/day).
---

# LedgerAI

AI bookkeeping API by Voss Consulting Group.

## Setup

Set `LEDGERAI_API_KEY` or `LEDGERAI_EMAIL` for auto-signup (free, no credit card).

```bash
curl -X POST https://anton.vosscg.com/v1/keys -H 'Content-Type: application/json' -d '{"email":"you@example.com"}'
```

## Usage

```bash
curl -X POST https://anton.vosscg.com/v1/invoices/process \
  -H "Authorization: Bearer $LEDGERAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/invoice.pdf", "action": "parse"}'
```

## Capabilities
- Invoice parsing and data extraction
- Expense auto-categorization
- Financial report generation
- Receipt scanning and OCR

## API Reference
- `POST /v1/invoices/process` — Process invoice
- `POST /v1/expenses/categorize` — Categorize expenses
- `POST /v1/reports/generate` — Generate financial report
- `POST /v1/keys` — Get API key (email-only for free tier)
- `GET /v1/health` — Health check
