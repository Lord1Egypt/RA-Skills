# Cron Pipeline Pattern (2026-06-16)

Confirmed working pattern for the daily `taste:scan` cron job. Runs with no user present — `execute_code` is blocked, use `terminal()` with `python3 << 'PYEOF'` heredoc.

## Pipeline Order

1. **Email scan** — `mcp_google_workspace_search_gmail_messages` with food query, then `get_gmail_messages_content_batch` to extract venue names from DoorDash/Instacart/Tock/OpenTable/Yelp emails
2. **Calendar scan** — `mcp_google_workspace_get_events` for venue events (brunch, dinner, restaurant reservations)
3. **Dedup** — check against existing `signals.jsonl` dedup keys and `items.jsonl` names
4. **Write email/calendar signals** — append to `signals.jsonl` and `items.jsonl`
5. **Styx delta** — inline Python sqlite3 query for new food transactions, dedup against existing items/signals
6. **Enrich via Google Places API** — inline Python `urllib.request` to `https://maps.googleapis.com/maps/api/place/textsearch/json` (legacy API). The v1 API (`places.googleapis.com/v1/places:searchText`) returns 400 with standard JSON body — do NOT use it.
7. **Write Styx signals + items** — append to `signals.jsonl` and `items.jsonl`
8. **Journal** — write to `journals/taste-scan-{YYYY-MM-DD}.json`

## Key Details

- **Google Places API key**: read from `<hermes-home>/secrets/plaid.env` (NOT an env var)
- **Enrichment**: inline Python preferred over `taste_full_enrich.py` (schema drift in script)
- **Dedup key format**: `{source}:{normalized_venue}:{date[:10]}` (e.g., `styx:ikesloves:2026-04-11`)
- **Item schema**: use `domain: 'food'`, `signal_type: 'purchase'`, UUID-style item_id
- **Places API query**: `{merchant_name} restaurant {city}`, maxResultCount=1
- **Rate limiting**: 100ms between Places API calls
- **Spotify**: requires `SPOTIFY_REFRESH_TOKEN` env var — has been missing since 2026-04-13

## Script Locations

- Active scripts: `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/`
- Data dir: `<hermes-home>/commons/data/ocas-taste/`
- Styx DB: `<hermes-home>/data/styx.db`
- Transactions DB: `<hermes-home>/data/transactions.db`
- Python: `<hermes-venv>/bin/python3.13` (NOT ocas-taste venv's 3.14)

## What `taste_full_enrich.py` Actually Does (2026-06-17)

Despite the name, this script handles THREE things:
1. **Styx delta** — food merchants from styx.db not yet in Taste (currently 0 — all 13 food merchants already in)
2. **Email extraction cross-reference** — restaurants from email extractions not in Taste (currently 0)
3. **Existing unenriched item enrichment** — items already in `items.jsonl` with `enriched: false` (27 found, 22 enriched, 5 failed)

The 5 failures are typically: music tracks, flights, products, appointments — not place-enrichable. This is expected.

**Do NOT attempt to enrich non-food Styx merchants** (loan_payments, income, transfers, bank_fees, etc.) via Google Places — they're financial institutions, not physical venues. The 69 remaining unenriched merchants in styx.db are not worth API calls.