# Operations Guide

## Core scripts

- `fetch-doc.sh <path>`: Fetch and cache a doc page.
- `search.sh <keyword...>`: Keyword search across cached pages.
- `sitemap.sh`: Show canonical category map.
- `cache.sh status|clean|refresh`: Cache inspection/maintenance.
- `recent.sh [days]`: Recently cached/updated pages.
- `track-changes.sh snapshot|list|since <date>`: Snapshot-based tracking.
- `build-index.sh ...`: Stub wrapper for future advanced indexing.

## Cache behavior

- Cache path: `OPENCLAW_DOCS_CACHE_DIR` (default `.openclawdocs-cache`)
- TTL seconds: `OPENCLAW_DOCS_TTL` (default `3600`)
- Base URL: `OPENCLAW_DOCS_BASE_URL` (default `https://docs.openclaw.ai`)

## Practical guidance

- If search returns no results, fetch likely docs first then retry search.
- For stale results, run `cache.sh refresh` and fetch again.
- For incident/debug work, include date and cache freshness in your summary.
