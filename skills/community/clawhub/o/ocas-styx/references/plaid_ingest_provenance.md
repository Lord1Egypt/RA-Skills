# Plaid ingest provenance — fix recipe (2026-07-07)

Concrete snippets for the provenance fixes. Companion to the "Plaid ingest &
provenance pitfalls" section in SKILL.md.

## 1. Daily cron `store_transaction` must capture ALL Plaid fields
File: `<hermes-home>/profiles/indigo/scripts/plaid_sync.py` — the 7 AM
`plaid-transaction-sync` cron. SEPARATE from the styx skill's
`scripts/plaid_sync.py`. Both copies must capture the same 22 columns; this
one was found dropping `merchant_entity_id` + all `loc_*`.

Location key is `lon`, NOT `lng`:
```python
loc = tx.get('location') or {}
conn.execute('''INSERT OR REPLACE INTO transactions
  (account_id, transaction_id, amount, currency, date, authorized_date,
   name, merchant_name, category, category_id, pending, payment_channel,
   personal_finance_category,
   merchant_id, merchant_entity_id, loc_address, loc_city, loc_region,
   loc_postal, loc_country, loc_lat, loc_lng)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
  (account_id, tx.get('transaction_id'), tx.get('amount'),
   tx.get('iso_currency_code', 'USD'), tx.get('date'), tx.get('authorized_date'),
   tx.get('name'), tx.get('merchant_name'),
   json.dumps(tx.get('category')) if tx.get('category') else None,
   tx.get('category_id'), 1 if tx.get('pending') else 0, tx.get('payment_channel'),
   tx.get('personal_finance_category', {}).get('primary') if tx.get('personal_finance_category') else None,
   tx.get('merchant_id'), tx.get('merchant_entity_id'),
   loc.get('address'), loc.get('city'), loc.get('region'), loc.get('postal_code'),
   loc.get('country'), loc.get('lat'), loc.get('lon')))
```

## 2. Add + backfill `merchant_entity_id` onto `merchants` (no collision)
```sql
ALTER TABLE merchants ADD COLUMN merchant_entity_id TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS idx_merchants_entity
  ON merchants(merchant_entity_id) WHERE merchant_entity_id IS NOT NULL;
-- Assign only to the BEST merchant per entity (most linked transactions):
--   GROUP BY merchant_entity_id, merchant_id -> keep max(count) per entity_id.
--   Do NOT set it on both rows of a duplicate pair (unique index violation).
```

Live UPDATE guard (inside the COALESCE subquery in `styx_universal_enrich.py`,
all three UPDATE branches):
```sql
merchant_entity_id=COALESCE(merchant_entity_id,
  (SELECT t.merchant_entity_id FROM transaction_merchants tm
   JOIN transactions t ON t.transaction_id = tm.transaction_id
   WHERE tm.merchant_id = merchants.id AND t.merchant_entity_id IS NOT NULL
     AND NOT EXISTS (SELECT 1 FROM merchants m2
                     WHERE m2.merchant_entity_id = t.merchant_entity_id
                       AND m2.id != merchants.id) LIMIT 1))
```

## 3. Verify the daily path actually captures location
Do NOT trust the diff. Import `store_transaction` from the cron script, insert a
fake tx (with `location` + `merchant_entity_id`) into a temp copy of the real
`transactions` schema (`SELECT sql FROM sqlite_master WHERE name='transactions'`),
then assert `loc_city`/`loc_lat`/`loc_lng`/`merchant_entity_id` are non-null.
This caught the dropped-field bug in the `~/scripts` copy.

## 4. Plaid `/merchant_entity` API is 404 on this plan
`GET /merchant_entity/{id}` and `POST /merchant_entity/get` both return
`NOT_FOUND` (invalid route). Merchant identity resolution = JOIN on the raw
`merchant_entity_id` field (hybrid with `normalized_name` fallback when null),
never a live endpoint call. `build_merchant_master.py` already keys on it.