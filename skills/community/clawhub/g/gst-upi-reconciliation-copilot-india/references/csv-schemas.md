# CSV Schemas (Flexible Columns)

Use these preferred columns. The script also accepts common aliases.

## GST invoice CSV

Required intent:
- Invoice identifier
- Invoice date
- Invoice total

Preferred columns:
- `invoice_no`
- `invoice_date`
- `customer_name`
- `taxable_value`
- `gst_amount`
- `total_amount`

Accepted aliases:
- `invoice_number` -> `invoice_no`
- `date` -> `invoice_date`
- `party_name` / `customer` -> `customer_name`
- `taxable` -> `taxable_value`
- `tax_amount` -> `gst_amount`
- `grand_total` / `invoice_total` -> `total_amount`

## UPI transaction CSV

Required intent:
- Transaction date
- Transaction amount
- Transaction status

Preferred columns:
- `txn_date`
- `amount`
- `status`
- `txn_id`
- `utr`
- `payer_name`
- `note`

Accepted aliases:
- `date` / `transaction_date` -> `txn_date`
- `txn_amount` -> `amount`
- `transaction_id` -> `txn_id`
- `rrn` -> `utr`
- `payer` -> `payer_name`
- `description` / `remarks` -> `note`

## Matching logic summary

1. Match only successful UPI rows (`success`, `completed`, `captured`, `paid`)
2. Amount equality with tolerance ±0.01
3. Date difference must be within configured window (default 7 days)
4. Add confidence boosts for invoice/token overlap in UPI notes/UTR/txn_id
5. One UPI row can reconcile only one GST invoice

## Output files

Given `--output-prefix out/recon_mar`:
- `out/recon_mar_reconciled.csv`
- `out/recon_mar_gst_unmatched.csv`
- `out/recon_mar_upi_unmatched.csv`
- `out/recon_mar_summary.json`
