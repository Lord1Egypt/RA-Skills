# Receipt product ingestion

Use this when Taste has access to itemized receipts (Rainbow Grocery, grocery stores, retail receipts, delivery line items). The goal is not transaction totals or spend analysis; totals are only matching/idempotency support. The Taste value is product-level behavioral evidence.

## Required output shape

A receipt ingestion pipeline must produce all of these layers:

1. **Raw/parsed receipt cache** — enough source metadata to avoid reprocessing the same email/receipt.
2. **Styx receipt line items** — one row per purchased product/PLU/UPC with receipt number, date, merchant, product name, department, quantity/weight, and matched transaction id when available.
3. **Taste venue signal** — one coarse `source_type: purchase` signal per receipt/visit for the store/merchant.
4. **Taste product items** — one canonical `ItemRecord` per distinct product/PLU/UPC, e.g. `category: grocery_product`, `source: rainbow_receipts_product`, with `signal_count`, `visit_dates`, `first_seen`, `last_seen`, and metadata containing PLU/UPC, departments, brands/categories if available, and purchase count.
5. **Taste product signals** — one `source_type: product_purchase` signal per receipt line item, linked by `item_id` to the product item and carrying receipt number, PLU/UPC, product name, department, quantity/weight, transaction id, and source line item id.

If only the venue/store purchase signal exists, the task is incomplete even if transaction matching and totals are correct.

## Operating rule

When the user asks whether receipts are being parsed “for products to add to Taste,” verify product-level `items.jsonl` and product-level `signals.jsonl`, not just `receipt_line_items` or store-level purchase signals.

Quick verification pattern:

```python
import json
items='<hermes-home>/commons/data/ocas-taste/items.jsonl'
sigs='<hermes-home>/commons/data/ocas-taste/signals.jsonl'
product_items=sum(1 for l in open(items) if 'rainbow_receipts_product' in l)
product_signals=sum(1 for l in open(sigs) if 'sig-rainbow-product-' in l)
print(product_items, product_signals)
```

## Idempotency pattern

Receipt ingestion should be re-runnable:

- Skip Styx line-item insertion for receipt numbers already present.
- Skip or rewrite coarse receipt signals by stable `sig-{merchant}-{receipt_number}` ids.
- For product items/signals, prefer deterministic rewrite of that product-source subset: read existing JSONL, keep rows not from the receipt-product source, append regenerated product items/signals from authoritative Styx line items.
- Do not append updated product items on every run; that creates duplicate canonical products.

## Cron pattern

For recurring receipt ingestion, use a deterministic script-only cron where possible:

1. Backfill/fetch new receipt emails.
2. Parse line items into Styx.
3. Sync Styx receipt line items into Taste product items and `product_purchase` signals.
4. Emit concise counts.

Avoid agent-driven cron for this class when the pipeline is already encoded; it is slower, noisier, and more likely to stop at a narrative summary instead of completing product sync.

## Communication pitfall

Do not frame success around spend/cost totals. Totals matter only for transaction matching. User-facing status should foreground product coverage: distinct product items, product purchase signals, receipt line items, idempotency, and schedule/monitoring state.