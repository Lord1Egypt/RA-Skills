# Receipt Line Item Enrichment for Grocery Stores

## Overview

Styx supports `receipt_line_items` table for granular product-level data extracted from grocery receipt emails. This enables per-item spending analysis, product frequency tracking, and Taste enrichment.

## Supported Receipt Format: Rainbow Grocery Cooperative

Rainbow Grocery sends eReceipt emails with a single-line concatenated format. All items, departments, and metadata are packed into one long line.

### Parsing Algorithm (v3 — working)

1. **Extract items section**: Between `Terminal: XX` and `SUBTOTAL`
2. **Insert department markers**: Split by known headers (BULK, HERBS, PACKAGED, PRODUCE, REFRIGERATED, FROZEN, CHEESE, BAKERY, BATH AND BODY, etc.)
3. **Find price markers**: Pattern `\$(\d+\.\d{2})\s+([TE])`
4. **Work backwards from each price**: Extract last `CODE NAME` pair. Code is numeric (2+ digits). Clean up qty/weight/tare bleed from previous item.
5. **Look ahead for qty/weight**: `X.XX lb @ $X.XX/lb` or `X @ $X.XX`
6. **Skip**: BAG CREDIT, SF BAG, CRV, COUPON, GREENBACKS, Price Override

### Product Identification

**UPC codes (10+ digits)**: Open Food Facts API (free, no auth):
`https://world.openfoodfacts.org/api/v0/product/{UPC}.json` with User-Agent `IndigoKarasu/1.0`

**PLU codes (4-5 digit)**: No free real-time API. Use receipt text name as-is.

### Table Schema

`receipt_line_items`: transaction_id, message_id, receipt_number, plu_upc, product_name, brand, category, subcategory, department, price, tax_code, quantity, unit_price, weight_lb, price_per_lb, is_bulk, is_organic, source_receipt_date, match_method, match_confidence, merchant_name, created_at.

Full DDL: See `references/schema.md` → `receipt_line_items` CREATE TABLE. **The table must exist before inserting** — if styx.db is empty, initialize all tables from schema.md first.

### Gmail Search Patterns

For Rainbow Grocery eReceipts:
- Exact phrase: `"eReceipt from Rainbow Grocery" newer_than:7d` — most precise
- Broad: `from:rainbow.coop "Receipt #" newer_than:14d` — catches edge cases
- The `newer_than` filter uses Gmail's internal date, which may differ from the receipt date printed in the email body. Always cross-check the email body date against the transaction date.

### Known Issues

- Name bleed: Qty info from previous item can contaminate next item's name
- Use Open Food Facts for brand/name enrichment when UPC is available
- Department-based classification as fallback