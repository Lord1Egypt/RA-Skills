---
name: google-play
description: >-
  A Google Play Store API alternative on fetcher.sh — pay-per-call in USDC
  via x402, or prepaid credits with a Bearer key, no Google Play Console
  access. Use when the user wants to search Android apps by keyword with
  price (free/paid) and country storefront filters, fetch an app's full
  details, reviews sorted by newest/rating/helpfulness, permissions, or data
  safety disclosure, list apps similar to a given app, or fetch a
  developer's app catalog. Also covers Android app store optimization (ASO)
  research, competitor app monitoring, review sentiment input, and app
  discovery without Google Play Console developer access.
keywords:
  - google-play
  - play-store
  - play-store-api
  - android-apps
  - app-store-optimization
  - aso
  - x402
  - ai-agent
---

# Google Play API

Google Play Store app search, details, reviews, permissions, data safety, and
developer catalogs — one plain HTTP GET per call, paid as you go. No Play
Console access, no developer account, no scraping the storefront HTML.

Base URL: `https://googleplay.fetcher.sh`

## Authentication

Two ways to pay, same data — full mechanics in the [`fetcher`
skill](../fetcher/SKILL.md):

```bash
# 1. Prepaid credits (recommended — get a key at https://fetcher.sh/topup
#    or via POST /api/credits/topup, see the fetcher skill)
export FETCHER_API_KEY="bby_live_xxxxxxxxxxxx"
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://googleplay.fetcher.sh/api/apps?search=meditation"

# 2. x402 pay-per-call — omit the header; a GET with no payment returns 402
#    with machine-readable payment requirements (USDC on Base, Polygon,
#    Arbitrum, Monad, or Solana). @x402/fetch signs and retries automatically.
```

Every response is `{ "status": number, "message": string, "data": ... }`; the
HTTP status mirrors `status`.

## Endpoints (7 — all GET, $0.003/call)

| Endpoint | What it returns |
| --- | --- |
| `/api/apps` | Apps matching a keyword; price and country filters |
| `/api/apps/{appId}` | An app's full details |
| `/api/apps/{appId}/reviews` | An app's reviews |
| `/api/apps/{appId}/similar` | Apps similar to a given app |
| `/api/apps/{appId}/permissions` | An app's requested permissions |
| `/api/apps/{appId}/datasafety` | An app's data safety disclosure |
| `/api/developers/{developerId}` | A developer's full app catalog |

Required on search: `search`. Optional: `price` (`all`, `free`, `paid`),
`country`, `lang`. Reviews require `country`; optional `sort` (`NEWEST`,
`RATING`, `HELPFULNESS`).

## Scenarios

**Free apps only:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "search=meditation" -G \
  --data-urlencode "price=free" \
  "https://googleplay.fetcher.sh/api/apps"
```

**Paid apps, German storefront:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "search=photo editor" -G \
  --data-urlencode "price=paid" \
  --data-urlencode "country=de" \
  "https://googleplay.fetcher.sh/api/apps"
```

**An app's full details, then reviews sorted by rating:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://googleplay.fetcher.sh/api/apps/com.spotify.music"

curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "country=us" -G \
  --data-urlencode "sort=RATING" \
  "https://googleplay.fetcher.sh/api/apps/com.spotify.music/reviews"
```

**Permissions and data safety disclosure:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://googleplay.fetcher.sh/api/apps/com.spotify.music/permissions"

curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://googleplay.fetcher.sh/api/apps/com.spotify.music/datasafety"
```

**Apps similar to a given app, and a developer's full catalog:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://googleplay.fetcher.sh/api/apps/com.spotify.music/similar"

curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "country=us" -G \
  "https://googleplay.fetcher.sh/api/developers/Spotify+AB"
```

## MCP

```json
{
  "mcpServers": {
    "google-play": {
      "url": "https://googleplay.fetcher.sh/mcp",
      "headers": { "Authorization": "Bearer bby_live_..." }
    }
  }
}
```

Free: `search_endpoints`, `describe_endpoint`, `check_balance`. Paid:
`fetch_data` (any endpoint above), `topup_credits`, plus the named shortcut
`googleplay_apps`. Drop the `headers` block to pay per call with x402
instead — see the [`fetcher` skill](../fetcher/SKILL.md) for the full flow.

## Errors

- `400` — missing/invalid parameter (message names it)
- `401` — unknown or rotated key
- `402` — payment required (x402 challenge) or `topup_required` (credits
  exhausted)
- `404` — not a priced path
- No rate limits; no refunds on upstream failures (settlement precedes
  delivery)

## Reference

- Full agent setup: <https://googleplay.fetcher.sh/skill.md>
- OpenAPI 3.1 contract: <https://googleplay.fetcher.sh/openapi.json>
- Condensed catalog: <https://googleplay.fetcher.sh/llms.txt>
- Payment, credits, and MCP deep dive: [`fetcher` skill](../fetcher/SKILL.md)
- Site: <https://googleplay.fetcher.sh>
