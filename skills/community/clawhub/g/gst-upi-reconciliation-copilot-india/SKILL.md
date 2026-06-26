---
name: gst-upi-reconciliation-copilot-india
description: Reconcile Indian GST invoice data with UPI transaction statements and produce audit-ready matched/unmatched reports. Use when the user asks to reconcile GST vs UPI collections, find missing payments, detect unmatched invoices, prepare month-end books, or investigate cashflow gaps from CSV exports (Tally/Zoho/ERP + bank/payment app exports).
---

# GST + UPI Reconciliation Copilot (India)

Perform deterministic reconciliation between GST invoice CSV data and UPI transaction CSV data.
Generate four outputs: reconciled rows, GST-unmatched rows, UPI-unmatched rows, and a summary JSON.

## Quick workflow

1. Confirm both input files are CSV and represent:
   - GST invoices/sales register
   - UPI collections/statement
2. Validate required intent-level fields exist (invoice id/date/total, txn date/amount/status).
3. Run:

```bash
python3 scripts/reconcile_gst_upi.py \
  --gst-csv /path/gst.csv \
  --upi-csv /path/upi.csv \
  --output-prefix /path/out/recon_2026_03 \
  --date-window-days 7
```

4. Read and report key metrics from `*_summary.json`:
   - matched rows
   - unmatched GST rows
   - unmatched UPI rows
   - reconciliation coverage %
5. Provide next actions for unmatched rows (follow-up / corrections / data cleanup).

## Matching policy

- Match only UPI rows with success-like status: `success`, `completed`, `captured`, `paid`.
- Require amount match (±0.01 tolerance).
- Enforce date window (default 7 days).
- Boost confidence if invoice number or customer tokens appear in UPI note/txn_id/UTR.
- Ensure one UPI transaction maps to one invoice only.

## Edge-case handling

- Ignore failed/pending/reversed UPI statuses for settlement matching.
- Preserve GST rows with empty/invalid dates as unmatched (do not force guesswork).
- Preserve UPI rows with missing amount as unmatched.
- Support flexible date formats in both files.
- Handle currency symbols and commas in amount fields.

## Required outputs to share with user

Always return:

1. Reconciliation snapshot:
   - matched rows / total GST rows
   - matched amount / total GST amount
2. File paths generated:
   - `*_reconciled.csv`
   - `*_gst_unmatched.csv`
   - `*_upi_unmatched.csv`
   - `*_summary.json`
3. Priority action items:
   - high-value unmatched GST invoices
   - suspicious UPI rows (success + high amount + no invoice)

## References

- Read `references/csv-schemas.md` for accepted columns and alias mapping.
