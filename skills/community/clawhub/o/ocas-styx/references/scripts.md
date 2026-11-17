# Styx Scripts

Styx owns all transaction-related scripts:

- `plaid_sync.py` — daily incremental Plaid transaction sync
- `plaid_history.py` — full 24-month historical pull
- `plaid_repull.py` — transaction re-pull utility
- `enrich.py` — merchant enrichment pipeline (SearXNG + LLM)
- `llm_resolve.py` — LLM-based merchant resolution
- `resolve.py` — transaction name resolution
- `query.py` — query helper for the Styx database
- `seed.py` — database seeding and schema migrations
- `styx_parser.py` — transaction parser
- `styx_places_enrich.py` — Google Places enrichment for venues

Plaid scripts are also wrapped from `~/.hermes/scripts/` for cron compatibility.

## Related reference files

- `references/schema.md` — Full SQL DDL for merchants, transaction_merchants, enrichment_runs tables
- `references/query-api.md` — Python query patterns for consumer skills (category transactions, spending by merchant, unresolved)
- `references/enrichment-pipeline.md` — Pipeline stage details and name cleaning rules