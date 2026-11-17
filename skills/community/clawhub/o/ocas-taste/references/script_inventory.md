# Script Inventory

Quick reference for what each script in `scripts/` does and when to use it.

| Script | Purpose | Full pipeline? | Needs OAuth? | Needs GOOGLE_PLACES_API_KEY? |
|---|---|---|---|---|
| `taste_scan.py` | Email/calendar scan + CLI entry point | Email/calendar only | Yes (Gmail/Calendar) | No |
| `taste_full_enrich.py` | Styx delta + cross-source dedup + enrichment | Yes (Styx→Taste) | No | Yes |
| `taste_cleanup_and_enrich.py` | Cross-source dedup + retry failed enrichments | Recovery only | No | Yes |
| `clean_signals.py` | Remove generic meal titles + dedup signals | Dedup only | No | No |
| `email_scan.py` | Standalone email scanner | Email-only | Yes | No |
| `run_historical_scans.py` | Orchestrator for historical email + calendar scans | Email/calendar only | Yes | No |

## Key Distinction

**`taste_scan.py scan-historical N`** scans Gmail only. It fails entirely if OAuth is broken.

**`taste_full_enrich.py [--limit N]`** runs the full Styx-to-Taste pipeline:
1. Queries styx.db for food merchants not yet in taste
2. Scans email extractions for restaurants not in taste
3. Cross-source dedup
4. Enriches all unenriched items via Google Places
5. Works without OAuth -- uses `GOOGLE_PLACES_API_KEY` from `<hermes-home>/secrets/plaid.env`

**`clean_signals.py <path>`** deduplicates signals JSONL:
- Removes generic meal titles (Breakfast, Lunch, Dinner, Brunch)
- Deduplicates on (venue_name, event_date, extraction_source, domain)
- Overwrites the file in-place with cleaned set
- Run after enrichment passes

## Non-Food Merchant Enrichment

**`styx_places_enrich.py`** (in `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/`) handles food merchants only. For non-food categories (retail, service, transport, entertainment, home, etc.), use an ad-hoc approach:
1. Query styx.db for merchants WHERE `(address IS NULL OR address = '')` AND category NOT IN financial categories
2. Call Google Places text search API for each
3. Update merchants table with address, city, state

## When OAuth is Broken

What still works:
- `taste_full_enrich.py` (Styx delta + enrichment)
- Manual signal ingestion
- `taste_cleanup_and_enrich.py` (dedup + retry)
- `clean_signals.py` (signal dedup)
- Enrichment via Places API

What fails:
- `taste_scan.py scan-historical` (email)
- `taste_scan.py scan-calendar` (calendar)
- Any MCP-based Gmail/Calendar access
- Spotify sync (separate auth issue)

## Invocation

**IMPORTANT:** Do NOT use the ocas-taste venv Python (`<hermes-home>/commons/data/ocas-taste/venv/bin/python3`) — it's Python 3.14 and lacks `googleapiclient`. Use the hermes-agent venv instead:

```bash
<hermes-venv>/bin/python3.13 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/<script>.py [args]
```

**Correct script path:** `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/`
**WRONG path:** `<hermes-home>/skills/ocas-taste/scripts/` (does not exist)
