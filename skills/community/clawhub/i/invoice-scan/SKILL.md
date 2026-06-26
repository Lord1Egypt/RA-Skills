---
name: invoice-scan
description: "AI-powered invoice OCR, scanning, and data extraction. Use when: (1) user needs OCR or text extraction from invoice images, scanned documents, or PDFs, (2) scanning/reading invoices to extract structured data (JSON, CSV, Excel), (3) validating invoice arithmetic or classifying document types (invoice vs receipt vs other), (4) processing handwritten invoices, stamps, or multi-language documents (Chinese, Russian, European, etc.), (5) user asks to read/parse/extract/OCR an invoice or receipt. Keywords: OCR, invoice scanning, receipt scanning, document OCR, invoice data extraction, invoice parser, invoice reader. Works in two modes: agent-native (uses your own vision — no API key needed, only formatOutput for export) or CLI standalone (needs ANTHROPIC_API_KEY). Env: ANTHROPIC_API_KEY (CLI mode only). Install: npm install --production in scripts/."
metadata:
  clawdbot:
    requires:
      env:
        - name: ANTHROPIC_API_KEY
          required: false
          description: "Anthropic API key (CLI mode only — not needed for agent-native mode)"
      bins:
        - node
    install:
      - id: node-deps
        kind: shell
        command: "cd {SKILL_DIR}/scripts && npm install --production"
        label: "Install Node.js dependencies (sharp, xlsx)"
    externalEndpoints:
      - url: "https://api.anthropic.com"
        purpose: "Send base64-encoded invoice images for AI vision extraction (CLI mode only)"
        dataTypes:
          - "invoice images (base64)"
          - "PII: supplier/buyer names, addresses, IBANs, bank details, amounts"
---

# Invoice Scan

## ⚠️ Privacy Notice

**CLI mode** sends base64-encoded invoice images to Anthropic's API (`api.anthropic.com`). Invoice data (supplier/buyer names, addresses, IBANs, bank details, amounts) will be transmitted to a third-party service. Confirm this is acceptable under your privacy and compliance requirements before use. Consider dedicated API credentials with usage limits.

**Agent-native mode** does NOT send data externally — the agent uses its own built-in vision. Only `formatOutput()` is called locally for CSV/Excel export.

## Setup

Install dependencies (required before first use):

```bash
cd {SKILL_DIR}/scripts && npm install --production
```

Dependencies: `sharp` (image processing), `xlsx` (Excel export). Review `scripts/package.json` before installing.

**CLI mode requires:** `ANTHROPIC_API_KEY` environment variable.
**Agent-native mode requires:** nothing — uses agent's built-in vision capability.

## Two Modes

### Mode 1: Agent-Native (No API Key, No External Calls)

Use your built-in vision to look at the invoice image directly. **Do NOT call `scanInvoice()`** — that function requires an API key and sends data externally. Instead:

1. Look at the image with your vision capability
2. Extract all fields into a JSON object matching the canonical schema in `references/canonical-schema.md`
3. Classify document type: invoice, credit-note, receipt, purchase-order, delivery-note, confirmation, statement, other-financial, not-financial
4. Validate arithmetic and business rules per `references/validation-rules.md`
5. Present results (see Output Format below)
6. For CSV/Excel export, construct the canonical JSON object and pass it to `formatOutput()` only:

```javascript
const { formatOutput } = require('{SKILL_DIR}/scripts');
// invoiceData = the JSON object YOU built from your vision extraction
// IMPORTANT: include ALL fields from canonical-schema.md, including charges[]
// e.g. invoiceData.charges = [{ type: 'shipping', label: 'P&P', amount: 5.99, vatRate: 20, vatAmount: 1.20 }]
const csv = formatOutput(invoiceData, 'csv');    // string — local only
const xlsx = formatOutput(invoiceData, 'excel');  // Buffer — local only
```

**Key:** `formatOutput()` is purely local — no network calls, no API key needed. It just formats your extracted data into CSV or Excel.

### Mode 2: CLI Standalone (Needs API Key)

For automation or pipelines. Requires `ANTHROPIC_API_KEY` env var.

```bash
ANTHROPIC_API_KEY=<key> node {SKILL_DIR}/scripts/cli.js scan <file> [--format json|csv|excel] [--output result.json]
```

Options: `--provider claude`, `--accept strict|relaxed|any`, `--no-preprocess`, `--model <model>`

## Agent-Native Extraction Checklist

Extract ALL of:

**Header:** invoiceNumber, invoiceDate (YYYY-MM-DD), dueDate, currency (ISO 4217), supplierName, supplierAddress, supplierVatNumber, buyerName, buyerAddress, buyerVatNumber, paymentTerms, paymentReference, bankDetails (iban, bic, accountNumber, sortCode)

**Line items:** description, quantity, unitOfMeasure, unitPrice, lineTotal, vatRate, sku, discount

**References:** PO, contract, GRN, timesheet, project, proforma, invoice (original invoice if this is a credit/debit memo), credit-note, debit-note refs. For credit/debit memos, ALWAYS include the original invoice reference.

**Totals:** netTotal, vatBreakdown (rate + amount + type per band — type is the tax regime label e.g. "CGST", "SGST", "USt", "НДС", "IVA"), vatTotal, grossTotal, amountPaid, amountDue, discount (invoice-level discount amount), discountRate (percentage)

**Metadata:** paidDate (YYYY-MM-DD — date from PAID stamp), vatInclusive (true if line totals include VAT, false if net, null if unknown)

**Charges:** Surcharges/fees outside line items — shipping, postage, P&P, delivery, freight, carriage, dispatch, handling, insurance, eco-levy, surcharges. Each: type (shipping|handling|insurance|surcharge|discount|other), label (original text from document), amount, vatRate, vatAmount. Do NOT duplicate items already captured as line items.

**Document type:** documentType (invoice, credit-note, debit-note, receipt, purchase-order, delivery-note, confirmation, statement, other-financial, not-financial)

**Additional:** handwritten notes, stamps/seals (type + text), remarks/comments, document language (ISO 639-1)

### Arithmetic Validation

1. qty × unitPrice = lineTotal (per line)
2. Sum of lineTotals = netTotal
3. netTotal + vatTotal = grossTotal
(Tolerance: ±0.02 for rounding)

### Locale Numbers

Parse regional formats automatically: US/UK (1,234.56), European (1.234,56), French (1 234,56), Indian (1,23,456.78). Use currency/country context when ambiguous.

### Quality Score

Count present from: invoiceNumber, invoiceDate, currency, supplierName, buyerName, supplierVatNumber, netTotal, vatTotal, grossTotal. Score = present / 9. good ≥ 0.8, partial ≥ 0.5, poor < 0.5.

## Output Format

```
📄 Invoice #{number} | {date}
   Supplier: {name} → Buyer: {name}
   Net: {currency}{net} | VAT: {currency}{vat} | Gross: {currency}{gross}
   [if charges exist] 📦 Charges: {label} {currency}{amount} [per charge]
   [if amountDue is not null] Amount Due: {currency}{amountDue} [if amountPaid] (Paid: {currency}{amountPaid})
   Items: {count} | Arithmetic: ✅/❌ | Quality: {rating} ({score}/9)
```

List warnings/flags, then offer: "Want JSON, CSV, or Excel?"

## File Delivery

- Output directory: `{WORKSPACE}/invoice-scan/output/` (create if needed)
- Naming: `{supplierName}_{invoiceNumber}_{invoiceDate}.{ext}` (replace spaces/slashes with hyphens)
- Always save JSON automatically, offer CSV/Excel on request
- Send file as chat attachment + confirm path

## References

- **Full schema**: `references/canonical-schema.md`
- **Validation rules**: `references/validation-rules.md`
