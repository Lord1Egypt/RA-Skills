# MakeWPFast Benchmark API — reference

Base URL: `https://makewpfast.com/wp-json/mwf-api/v1`
Auth: `Authorization: Bearer <key>` on every request. Get a key at https://makewpfast.com/api/

The `mwf-bench` CLI wraps all of this. This reference is for understanding the raw API and the
fields the CLI surfaces.

## Endpoints

| Method | Path | Quota? | Notes |
|--------|------|--------|-------|
| GET | `/plugins/{slug}` | yes (1 req) | Benchmark for a WordPress.org plugin. Slug must match `[a-z0-9][a-z0-9-]*`. |
| GET | `/themes/{slug}` | yes (1 req) | Same shape, for themes. |
| GET | `/me` | **no** | Your tier, quota, usage, reset date. Works even when over quota. |

There is **no list or search endpoint** — lookups are by exact slug only. The CLI resolves
human names to slugs using the *free* WordPress.org API before calling the paid endpoint.

## Response shape (plugins / themes)

```json
{
  "slug": "akismet",
  "type": "plugin",
  "name": "Akismet Anti-Spam",
  "benchmarked": true,
  "benchmarked_at": "2026-05-16 12:00:00",
  "speed_score": { "grade": "B+", "numeric": 78 },
  "contexts": {
    "activation": { "ttfb_delta_ms": 18, "memory_delta_kb": 2048, "queries_delta": 2 },
    "homepage":   { "ttfb_delta_ms":  5, "memory_delta_kb": 1024, "queries_delta": 1 },
    "admin":      { "ttfb_delta_ms": 22, "memory_delta_kb": 3072, "queries_delta": 4 }
  },
  "metadata": { "active_installs": 5000000, "rating_percent": 94 },
  "links": { "profile": "https://makewpfast.com/plugins/akismet/" }
}
```

- A context object can be `null` → that scenario wasn't measured. Not the same as zero impact.
- `benchmarked: false` → slug is known but no benchmark yet (all deltas absent).
- `speed_score.numeric` is 0–100 (higher = faster/lighter); `grade` is the A–F label.
- Deltas are measured against a clean WordPress baseline: TTFB ms, memory KB, queries raw count.

## `/me` shape

```json
{ "tier": "starter", "customer_email": "you@example.com", "monthly_quota": 50000,
  "used_this_period": 12, "remaining": 49988, "period_resets_at": "2026-07-15 00:00:00",
  "key_prefix": "mwf_live_ab", "status": "active" }
```

## Status codes

| Code | Meaning | CLI behavior |
|------|---------|--------------|
| 200 | OK | caches the row; prints data |
| 401 | missing/invalid key | prints subscribe link, no retry |
| 403 | key revoked/suspended | prints subscribe link, no retry |
| 404 | slug not in dataset | reports "not in dataset" |
| 429 | monthly quota exceeded | prints reset/upgrade link, no retry |

Rate-limit headers on every 200: `X-RateLimit-Limit`, `X-RateLimit-Remaining`,
`X-RateLimit-Reset`.

## Caching

Responses are served `Cache-Control: private, no-store` (per-request auth → not edge-cached).
The client MUST cache. `mwf-bench` caches each row under `~/.cache/makewpfast-bench/bench/`
with a 21-day TTL, name→slug resolutions in `resolve.json` (cached indefinitely — slugs are
stable), and an append-only `calls.log` recording every request (hit/miss/status) so you can
audit quota usage.

## Pricing tiers

| Tier | Price | Monthly requests |
|------|-------|------------------|
| Starter | $49/mo | 50,000 |
| Pro | $149/mo | 500,000 |
| Scale | $499/mo | 5,000,000 |

Soft 429 at the cap, no overage billing. Enterprise/SLA: contact@makewpfast.com.
