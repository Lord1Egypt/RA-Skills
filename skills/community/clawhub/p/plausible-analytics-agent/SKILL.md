---
name: plausible-analytics
description: Track pageviews and custom events via the Plausible Events API, and query stats (top pages, top sources, countries, realtime visitors). Use when you need to send analytics events or fetch analytics data from a self-hosted or plausible.io site.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "env": ["PLAUSIBLE_SITE_DOMAIN", "PLAUSIBLE_API_KEY"],
          },
      },
  }
---

# Plausible Analytics

Track events and query stats from Plausible Analytics (self-hosted or plausible.io).

## Configuration

Set these environment variables before use:

```bash
# Your site domain (e.g. example.com)
export PLAUSIBLE_SITE_DOMAIN="example.com"

# Your Plausible API key (for stats endpoints)
export PLAUSIBLE_API_KEY="your-api-key"

# Plausible base URL (default: https://plausible.io for hosted)
# For self-hosted, set to your instance URL
export PLAUSIBLE_BASE_URL="https://plausible.io"
```

## Track Pageview

```bash
bash skills/plausible-analytics/scripts/track.sh \
  --domain "$PLAUSIBLE_SITE_DOMAIN" \
  --url "https://example.com/blog/post-1" \
  --referrer "https://google.com"
```

Options:
- `--domain` — Site domain (default: $PLAUSIBLE_SITE_DOMAIN)
- `--url` — Page URL being viewed (required)
- `--referrer` — Referring URL (optional)
- `--base-url` — Plausible base URL (default: $PLAUSIBLE_BASE_URL)

## Track Custom Event

```bash
bash skills/plausible-analytics/scripts/track.sh \
  --domain "$PLAUSIBLE_SITE_DOMAIN" \
  --event "Signup" \
  --props "{\"plan\":\"pro\",\"source\":\"newsletter\"}"
```

Options:
- `--domain` — Site domain
- `--event` — Custom event name (e.g. "Signup", "Button Click")
- `--props` — JSON object with event properties (optional)
- `--base-url` — Plausible base URL

## Get Stats Summary

```bash
bash skills/plausible-analytics/scripts/stats.sh \
  --domain "$PLAUSIBLE_SITE_DOMAIN" \
  --period "30d" \
  --compare "previous_period"
```

Options:
- `--domain` — Site domain
- `--period` — Time period: `6mo`, `12mo`, `day`, `7d`, `30d`, `month` (default: 30d)
- `--compare` — Compare to previous period: `previous_period` (optional)
- `--base-url` — Plausible base URL (default: $PLAUSIBLE_BASE_URL)

Returns: pageviews, unique visitors, bounce rate, visit duration, total pageviews

## Get Top Pages

```bash
bash skills/plausible-analytics/scripts/top-pages.sh \
  --domain "$PLAUSIBLE_SITE_DOMAIN" \
  --period "30d" \
  --limit 10
```

Options:
- `--domain` — Site domain
- `--period` — Time period (default: 30d)
- `--limit` — Number of pages to return (default: 10)
- `--base-url` — Plausible base URL

## Get Realtime Visitors

```bash
bash skills/plausible-analytics/scripts/realtime.sh \
  --domain "$PLAUSIBLE_SITE_DOMAIN"
```

Options:
- `--domain` — Site domain
- `--base-url` — Plausible base URL

Returns: current visitors on site, pageviews in last 30 min, top pages currently viewed

## Notes

- The Events API (`/api/event`) is used without authentication for tracking
- The Stats API (`/api/v1/stats`) requires `PLAUSIBLE_API_KEY` set in the request header
- For self-hosted Plausible, set `PLAUSIBLE_BASE_URL` to your instance
- All scripts output JSON or plain text depending on the endpoint
