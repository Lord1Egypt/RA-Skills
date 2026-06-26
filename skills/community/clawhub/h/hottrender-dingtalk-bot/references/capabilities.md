# Basic Crawler Capability Map

## Runtime Scope

This skill now keeps only the basic crawling capability:

- Four-region daily hotspot trends
- Custom keyword / vertical hotspot discovery
- Markdown and JSON outputs
- Provider errors surfaced explicitly

Excluded on purpose:

- DingTalk push
- OSS publishing
- ActionCard HTML pages
- lp-ads workspace
- worker queue APIs
- database persistence
- LLM translation or summaries

## Entry Points

Daily trends:

```text
scripts/fetch_daily_trends.py
```

Custom keyword hotspots:

```text
scripts/fetch_keyword_hotspots.py
```

Shared orchestration:

```text
src/crawler.py
```

## Providers

Default daily platforms:

- `google`: Google News RSS, supports all four regions
- `youtube`: public YouTube search page, supports all four regions
- `x`: Trends24 regional trends; some regions may be unsupported and should report explicit errors

Default keyword platforms:

- `google`
- `youtube`

Optional:

- `tiktok`: requires `requirements-tiktok.txt`, Playwright browser install, usable network/session, and often `TIKTOK_MS_TOKEN`

## Data Contract

All providers return `TrendItem`:

```text
platform
region
title_original
summary_zh
raw_url
source_type
source_engine
trust_level
content_type
published_at
fetched_at
rank
keyword
meta_json
```

Downstream scripts should depend on `TrendItem`, not provider-specific fields.

## Output

When output is `.md`, scripts also write a sibling `.json` file:

```text
out/daily_trends.md
out/daily_trends.json
out/keyword_hotspots.md
out/keyword_hotspots.json
```

Use the JSON for raw records and the Markdown for quick human inspection.
