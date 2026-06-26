# Source Ingestion (v0.3)

Use `scripts/source_ingest.py` to normalize candidate links before ranking.

## Inputs

- `--youtube` (repeatable): channel id/user/feed URL
- `--x-json`: optional normalized list from X integration
- `--web-json`: optional normalized list from web search ingestion

## Output

JSON array with items:
`{title, url, snippet, source, freshness}`

Then pass this file to `scripts/discover_content.py --candidates ...`.
