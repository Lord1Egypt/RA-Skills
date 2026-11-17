# Storage Layout

## Database

Styx maintains its own SQLite database at `<hermes-home>/data/styx.db`.
**IMPORTANT:** Hardcode this path. Do NOT use `{agent_root}` — it resolves to the indigo profile home, not the shared data directory.

The active DBs are:
- `<hermes-home>/data/transactions.db` — raw Plaid transaction data
- `<hermes-home>/data/styx.db` — enriched merchant data

A second copy exists at `<hermes-home>/commons/data/ocas-styx/styx.db` but it is a stale 0-byte stub — ignore it.

## Files

| File | Purpose |
|------|---------|
| `{agent_root}/data/styx.db` | Enriched merchant data + transaction links |
| `{agent_root}/data/transactions.db` | Raw Plaid transaction data (read-only) |
| `{agent_root}/data/styx/review_queue.jsonl` | Low-confidence matches for manual review |
| `{agent_root}/data/styx/intents.jsonl` | Enrichment intent log |
| `{agent_root}/data/styx/evidence.jsonl` | Evidence records for each enrichment run |
| `{skill_root}/scripts/enrich.py` | LLM enrichment pipeline |
| `{skill_root}/scripts/styx_places_enrich.py` | Google Places enrichment (food-only) |
| `<hermes-home>/commons/data/ocas-styx/styx_universal_enrich.py` | Google Places enrichment (all categories) |
| `{skill_root}/scripts/query.py` | Query helper |
