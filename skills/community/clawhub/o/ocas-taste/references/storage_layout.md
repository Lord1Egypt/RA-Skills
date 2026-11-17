# Storage Layout

## Data directory

```
{agent_root}/commons/data/ocas-taste/
  config.json
  signals.jsonl       ← consumption signals (calendar, doordash, hotels, opentable, yelp, instacart, tock, amazon, spotify)
  items.jsonl         ← entities (restaurants, venues, media items)
  links.jsonl         ← entity relationship links
  decisions.jsonl     ← audit log
  extractions.jsonl   ← raw email/calendar extractions
  intents.jsonl       ← intent tracking for scan/enrich/recommend operations
  evidence.jsonl      ← evidence records for recovery contract
  scripts/            ← taste_full_enrich.py, taste_cleanup_and_enrich.py
  music/
    spotify_sync_checkpoint.json
  signals/
    signals.jsonl     ← Styx purchase signals (rainbow_grocery, etc.) — SEPARATE store from root signals.jsonl
  items/
    items.jsonl       ← Styx purchase item records — SEPARATE store from root items.jsonl
```

### ⚠️ Two signal stores

Signals are split across two locations. **Both must be counted for totals.**

| File | Contents | Source |
|---|---|---|
| `signals.jsonl` (root) | Calendar, DoorDash, Hotels.com, OpenTable, Yelp, Instacart, Tock, Amazon, Spotify | Email/calendar scans |
| `signals/signals.jsonl` (subdir) | Styx purchase transactions (grocery, retail) | Styx delta ingestion |

The `scan-calendar` command's output `signals_created` field reports the Styx delta count, **not** the calendar signal count. Calendar signals are promoted to the root `signals.jsonl` via `_process_extractions()` but the output JSON conflates the two. To get the actual calendar signal count, query `signals.jsonl` for `extraction_source == 'calendar'`.

## Journal directory

```
{agent_root}/commons/journals/ocas-taste/
  YYYY-MM-DD/
    {run_id}.json
```

## Enrichment pipeline

```bash
python3 scripts/taste_full_enrich.py        # Full scan: styx + email + existing items
python3 scripts/taste_cleanup_and_enrich.py  # Dedup + retry failed items
```

## Name matching / rename patterns

Styx merchants frequently have messy names from Plaid. See `references/enrichment.md` for the full list of observed patterns and normalization rules. Key principle: cross-source dedup means same restaurant via email + calendar + styx = one entry. Normalize by lowercasing, stripping articles, location suffixes, and venue-type suffixes.

⚠️ LEGACY: An old data path may exist but is STALE. Active data is ONLY under `{agent_root}/commons/data/ocas-taste/`.