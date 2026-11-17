# Styx → Taste Delta Ingestion

Daily workflow for pulling new restaurant/food transactions from Styx that aren't yet in the Taste model, enriching them via Google Places, and persisting signals + items.

## When to use

- Part of the `taste:scan` cron job (13:12), after email/calendar scan
- Anytime after Styx has ingested new transactions (e.g., after `plaid-transaction-sync`)
- Standalone recovery: backfill gaps when email/calendar auth is broken

## Prerequisites

- Styx database at `~/.hermes/data/styx.db` with `transaction_merchants` and `merchants` tables
- Transaction database at `~/.hermes/data/transactions.db` (attached as `txndb`)
- Google Places API key at `~/.hermes/secrets/plaid.env` as `GOOGLE_PLACES_API_KEY`
- Taste data directory at `~/.hermes/commons/data/ocas-taste/`

## Workflow

### 1. Query Styx for food transactions

```sql
SELECT t.transaction_id, t.name as raw_name, t.amount, t.date,
       m.name as merchant_name, m.category, m.city, tm.confidence
FROM transaction_merchants tm
JOIN merchants m ON tm.merchant_id = m.id
JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
WHERE (m.category IN ('restaurant', 'cafe', 'bar', 'food')
   OR t.personal_finance_category = 'FOOD_AND_DRINK')
  AND tm.confidence >= 0.7
ORDER BY t.date DESC
```

### 2. Deduplicate against existing Taste model

Before enriching, load existing items and signal dedup keys:

- **Item dedup**: check `items.jsonl` for domain=food, match on `name.lower().strip()`
- **Signal dedup**: check `signals.jsonl` for domain=food + source=styx, match on `dedup_key` (format: `styx:{merchant_lower}:{date[:10]}`)
- Only process rows where BOTH the item name is new AND the dedup key is new

### 3. Group by unique merchant

Multiple transactions may be for the same merchant (repeat visits). Group by `merchant_name.lower()` to:
- Avoid redundant Google Places API calls
- Aggregate visit count, total spend, latest date per venue
- Create ONE ItemRecord per unique venue, ONE ConsumptionSignal per transaction

### 4. Enrich each unique venue via Google Places

Use the **legacy Places API** text search endpoint (the v1 API at `places.googleapis.com/v1/places:searchText` returns 400 — do NOT use it):

```
GET https://maps.googleapis.com/maps/api/place/textsearch/json?query={merchant_name} restaurant {city}&key={API_KEY}
```

**Rate limit**: ~100 req/sec. Use 100ms delay between requests to stay safe.

**Styx merchant name truncation**: Styx truncates merchant names to ~15 characters (e.g., "Cha-ya-mi" for "Chaya Mistercharli", "Mr.charli" for "Mr. Charlie's"). Google Places text search handles truncated names well — always use the first result. Validated at 100% match rate (124/124 venues) in May 2026. Re-validated 2026-06-17: 8/8 merchants enriched successfully.

**Extract from the first result**:
- `name` → `ItemRecord.name` (the canonical display name)
- `formatted_address` or `vicinity` → parse neighborhood (first comma-separated segment) and city (second-to-last)
- `price_level` → map to numeric: 0=1, 1=1, 2=2, 3=3, 4=4
- `rating` → numeric rating (may be absent for new/unrated venues)
- `types` → extract cuisine types, filtering out generic values (`point_of_interest`, `establishment`, `food`, `restaurant`)
- `place_id` → for future dedup

**Python pattern (confirmed working 2026-06-17)**:
```python
import urllib.request, urllib.parse
params = urllib.parse.urlencode({'query': f'{merchant_name} restaurant', 'key': api_key})
url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?{params}'
with urllib.request.urlopen(url, timeout=10) as resp:
    data = json.loads(resp.read())
    if data.get('status') == 'OK' and data.get('results'):
        result = data['results'][0]
```

### 5. Build ItemRecord

```json
{
  "item_id": "<uuid>",
  "name": "<Places displayName>",
  "venue_name": "<raw Styx merchant name>",
  "domain": "food",
  "category": "<styx category>",
  "cuisine": ["<from types>"],
  "price_level": <1-4>,
  "price_label": "<$ repeated>",
  "neighborhood": "<from address>",
  "city": "<from address>",
  "address": "<full address>",
  "rating": <float or null>,
  "source": "styx",
  "signal_count": <number of transactions>,
  "visit_dates": ["<date1>", "<date2>", ...],
  "last_seen": "<latest date>",
  "total_spend": <sum of amounts>,
  "avg_spend": <total / count>,
  "enriched": true,
  "enriched_at": "<ISO timestamp>",
  "enrichment_source": "google_places_legacy",
  "created_at": "<ISO timestamp>"
}
```

### 6. Build ConsumptionSignals

One per transaction (not one per venue):

```json
{
  "signal_id": "<uuid>",
  "item_id": "<matching ItemRecord.item_id>",
  "dedup_key": "styx:{merchant_lower}:{date[:10]}",
  "domain": "food",
  "source": "styx",
  "signal_type": "purchase",
  "venue_name": "<Places displayName>",
  "merchant_name": "<raw Styx name>",
  "amount": <float>,
  "date": "<YYYY-MM-DD>",
  "confidence": "<from styx>",
  "created_at": "<ISO timestamp>"
}
```

### 7. Dedup key format

`styx:{merchant_name_lowercase}:{date_YYYY_MM_DD}`

- Same merchant on different dates = separate signals (correct — these are separate visits)
- Same merchant on same date from different sources = dedup (keep styx over calendar over email)

### 8. Persist

Append to JSONL files (never overwrite):
- `items.jsonl` — one line per new ItemRecord
- `signals.jsonl` — one line per new ConsumptionSignal
- `journal.jsonl` — one observation entry per venue enriched

### 9. Update scan watermark

Update `config.json` email_scan.last_scan_timestamp even when email/calendar scan is skipped due to auth failure.

## Filtering out non-food merchants

**Skip list** — do NOT enrich these (they are platforms, not restaurants):
- Payment processors: "Blackbird", "Toast" (payment), "Square", "Stripe", "PayPal", "Venmo"
- Delivery platforms: "DoorDash", "Uber Eats", "GrubHub", "Postmates", "Instacart"
- Ride-sharing: "Uber"

**Exception list** — these contain skip words but ARE real restaurants:
- "Blckbrd" with styx category "bar" → real bar, not Blackbird the payment processor. Verify via Google Places match and category.
- "Toast Eatery" → real cafe, not Toast payment

## Edge cases

- **Google Places returns no results**: Use the raw Styx name as `display_name`, mark `enriched: false`, queue for retry via web search (Sift)
- **Merchant city is null**: Common in Styx data — address enrichment from Places backfills this
- **Very low confidence (<0.7) Styx match**: Skip — the merchant association is unreliable
- **execute_code blocked in cron mode**: Use `terminal()` with heredoc (`python3 << 'PYEOF'`) instead of `execute_code` for inline Python

## Verification

After running:
- New line count in items.jsonl should increase by number of unique venues
- New line count in signals.jsonl should increase by number of transactions
- All new items should have `enriched: true` (unless Places returned no results)
- Cross-check: `wc -l items.jsonl` before and after

## Schema compliance note

The bundled `taste_full_enrich.py` script does **not** produce schema-compliant output:
- Items get `item_id: "item-{slug}"` instead of a UUID
- Signals use `strength` field instead of `signal_type`
- Items may get `domain: "restaurant"` instead of `domain: "food"`

When writing custom delta scripts, follow the schemas in sections 5 and 6 above exactly. Use `uuid.uuid4()` for item_ids, `signal_type: "purchase"`, and `domain: "food"` for all food/restaurant items.