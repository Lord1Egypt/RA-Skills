---
name: google-trends
description: Fetch and structure Google Trends daily trending-search data by country/region via the public RSS feed. Use when users ask for Google Trends snapshots, country comparisons, top daily searches, related news context, or export-ready trend tables (JSON/CSV/markdown) for Sheets/docs/reporting.
---

# Google Trends

Use this skill to get **Google Trends daily trending searches** quickly, without browser scraping.

## Quick start

```bash
python scripts/google_trends_rss.py list-geos
python scripts/google_trends_rss.py daily --geo HK --limit 20 --sort traffic --format table
python scripts/google_trends_rss.py daily --geo US --sort traffic --format json --out /tmp/us-trends.json
python scripts/google_trends_rss.py daily --geo JP --sort traffic --out /tmp/jp-trends.csv
```

## Workflow

1. Pick geo code (`HK`, `US`, `JP`, etc.).
2. Fetch daily trends with `daily --geo <CODE>`.
3. Choose output format:
   - `table` for terminal quick check
   - `json` for downstream automation
   - `markdown` for chat/report paste
4. If needed, save with `--out`:
   - `.json` for structured pipelines
   - `.csv` for Sheets import

## Commands

### 1) List common geo codes

```bash
python scripts/google_trends_rss.py list-geos
```

### 2) Fetch daily trends

```bash
python scripts/google_trends_rss.py daily --geo HK --limit 20 --sort traffic --format table
```

Options:
- `--geo` (required): region code
- `--limit` (default `20`): max trend rows
- `--format` (`table|json|markdown`, default `table`)
- `--sort` (`traffic|feed|recency`, default `traffic`)
  - `traffic`: hottest-first by `approx_traffic`
  - `feed`: keep RSS original order
  - `recency`: newest-first by pubDate
- `--out`: optional file path (`.json` or `.csv`)
- `--timeout` (default `20`)

## Output schema

Each trend includes:
- `title`
- `approx_traffic`
- `link`
- `pub_date`
- `picture`
- up to 2 related news items (`title/snippet/url/source`)

## Notes

- This skill targets **daily trending searches** feed (not full historical keyword timeseries).
- Feed source: Google Trends RSS endpoint by geo.
- Keep parsing defensive; feed fields can evolve.
- For implementation details aligned to the existing connector repo, read:
  - `references/google-trends-connector-notes.md`

## Resources

- Script: `scripts/google_trends_rss.py`
- Reference: `references/google-trends-connector-notes.md`
