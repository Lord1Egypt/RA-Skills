---
name: millimetric-query
description: Query Millimetric analytics — top sources, aggregate stats, raw events, and the Facebook social-vs-paid split. Use when the user asks "where does my traffic come from", "how many signups this week", "show recent events", "FB paid vs organic", or wants to pull analytics numbers from the command line.
metadata: { "openclaw": { "requires": { "env": ["MILLIMETRIC_RK"], "bins": ["curl", "jq"] }, "primaryEnv": "MILLIMETRIC_RK", "emoji": "📊", "homepage": "https://api.millimetric.ai", "install": [{ "kind": "brew", "formula": "jq", "bins": ["jq"], "label": "Install jq (brew)" }] } }
---

# Millimetric Query

Read-only analytics queries against Millimetric. Uses an `rk_live_…` key (read scope). The headline feature is `/v1/sources` — it's the endpoint that surfaces Facebook **social** vs Facebook **paid** as separate rows.

## When to Use

- User asks for traffic sources, breakdowns, top channels
- "How many signups / purchases / pageviews in the last N days"
- Facebook (or any source) paid-vs-organic split
- Pulling raw events for debugging or ad-hoc analysis
- Building a quick dashboard / cron report from the CLI

## When NOT to Use

- Sending events → `millimetric-track`
- Connecting an agent natively → `millimetric-mcp-setup` (MCP is usually nicer for AI)

## Setup

```bash
export MILLIMETRIC_RK=rk_live_...                   # read-only key
export MILLIMETRIC_HOST=https://api.millimetric.ai
```

## Quick start

### Top sources (with FB social vs paid)

```bash
curl -sG "$MILLIMETRIC_HOST/v1/sources" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "from=2026-05-01T00:00:00Z" \
  --data-urlencode "to=2026-06-01T00:00:00Z" \
  --data-urlencode "breakdown=source_medium" | jq
```

Returns rows like:

```json
{ "source": "facebook", "medium": "paid",   "events": 6, "uniques": 6, "paid_share": 1.0 }
{ "source": "facebook", "medium": "social", "events": 3, "uniques": 3, "paid_share": 0.0 }
```

For "what % of each source is paid", use `breakdown=source` — `paid_share` becomes meaningful (0.0 → 1.0).

### Aggregate stats

```bash
# Daily signups grouped by source/medium
curl -sG "$MILLIMETRIC_HOST/v1/stats" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "metric=count" \
  --data-urlencode "from=2026-05-01T00:00:00Z" \
  --data-urlencode "to=2026-05-17T00:00:00Z" \
  --data-urlencode "event=signup" \
  --data-urlencode "group_by=source,medium" \
  --data-urlencode "interval=day" | jq
```

Parameters:

| Param | Values |
|-------|--------|
| `metric` | `count`, `uniques` |
| `from` / `to` | ISO 8601 (inclusive / exclusive) |
| `event` | optional event name filter |
| `group_by` | comma list — any of `source`, `medium`, `campaign`, `country`, `device_type`, `browser`, `os`, `path`, `event_name` |
| `interval` | `hour`, `day`, `week`, `month` (omit for a single bucket) |

### Raw events

```bash
curl -sG "$MILLIMETRIC_HOST/v1/query" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "from=2026-05-01T00:00:00Z" \
  --data-urlencode "to=2026-05-17T00:00:00Z" \
  --data-urlencode "event=signup" \
  --data-urlencode "limit=100" | jq
```

Filters: `event`, `source`, `medium`, `country`, `user_id`, `anonymous_id`, `limit` (1–1000).

## Recipes

### "What's our Facebook paid-vs-organic split this month?"

```bash
curl -sG "$MILLIMETRIC_HOST/v1/sources" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "from=$(date -u -v1d +%Y-%m-%dT00:00:00Z)" \
  --data-urlencode "to=$(date -u +%Y-%m-%dT00:00:00Z)" \
  | jq '.rows[] | select(.source=="facebook")'
```

### "Daily unique signups by country, last 7 days"

```bash
curl -sG "$MILLIMETRIC_HOST/v1/stats" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "metric=uniques" \
  --data-urlencode "event=signup" \
  --data-urlencode "from=$(date -u -v-7d +%Y-%m-%dT00:00:00Z)" \
  --data-urlencode "to=$(date -u +%Y-%m-%dT00:00:00Z)" \
  --data-urlencode "group_by=country" \
  --data-urlencode "interval=day" | jq
```

### "What did user_42 do this week?"

```bash
curl -sG "$MILLIMETRIC_HOST/v1/query" \
  -H "Authorization: Bearer $MILLIMETRIC_RK" \
  --data-urlencode "user_id=user_42" \
  --data-urlencode "from=$(date -u -v-7d +%Y-%m-%dT00:00:00Z)" \
  --data-urlencode "to=$(date -u +%Y-%m-%dT00:00:00Z)" \
  --data-urlencode "limit=200" \
  | jq '.rows[] | { ts: .timestamp, event: .event_name, source: .source, medium: .medium }'
```

## Reading the attribution columns

Every event has `source` / `medium` / `source_confidence` / `source_rule_id` set by the server-side classifier. The rule cascade (first-match):

1. Network click IDs (`gclid`, `msclkid`, `ttclid`, `li_fat_id`) → paid / **high**
2. `fbclid` via `l.facebook.com` / `lm.facebook.com` → facebook/paid / **high**
3. `fbclid` + `utm_source=facebook|instagram|meta` → paid / **high**
4. `utm_medium=cpc|paid|paid_social|cpm|display` → paid / **high**
5. `fbclid` alone → facebook/paid / **medium**
6. Explicit UTM → source/utm_medium / **high**
7. Facebook referrer, no `fbclid` → facebook/**social** / medium
8. Other social referrers (twitter, linkedin, reddit, tiktok, …) → social / medium
9. Search engines → organic / medium
10. Email clients → email/email / medium
11. Same-host referrer → internal/direct / high
12. Nothing → direct/direct / high
13. Else → host slug / referral / **low**

`source_rule_id` lets you audit which rule matched.

## Common errors

| Status | `error` | Fix |
|--------|---------|-----|
| 401 | `invalid_api_key` | Wrong key; must be `rk_*`. |
| 403 | `insufficient_scope` | Used `pk_*`/`sk_*` — read endpoints want `rk_*`. |
| 400 | `invalid_group_by` | Unknown column in `group_by`. |
| 400 | `invalid_params` | Bad ISO dates or out-of-range `limit`. |

## See also

- Sending events → `millimetric-track`
- Native MCP for agents → `millimetric-mcp-setup`
