---
name: lantern-works
description: >-
  Look up tracked hourly GPU rental prices (H100, A100, RTX 4090 and more) with
  vendor source links, check dates and day-over-day price changes, and search
  work-stack tool deals (compute, search, crawl, hosting, email) through the
  Lantern Works hosted MCP server or its public JSON API. No API key needed.
  Some result links are referral links and are flagged in the data.
version: 1.0.4
metadata:
  openclaw:
    emoji: "🏮"
    homepage: https://thelanternworks.com/install/?ref=clawhub
    requires:
      anyBins:
        - curl
        - uvx
---

# Lantern Works — GPU prices and work-stack deals

Public, read-only data. No authentication, no environment variables.

## Hosted MCP server (Streamable HTTP)

Endpoint: `https://lantern-works-mcp.lantern-works.workers.dev/mcp?ref=clawhub`

Local alternative (stdio): `uvx lantern-works-deals-mcp` (PyPI, MIT license).

Tools (9):
| Tool | What it does |
|---|---|
| `compare_gpu_prices` | Tracked hourly rental prices for one GPU model (e.g. H100, A100 SXM, RTX 4090, L40S), cheapest first |
| `get_price_changes` | GPU price changes among tracked providers, newest first (old/new price, change_pct, source_url) |
| `optimize_stack` | Cheapest suitable monthly stack among tracked providers for quantities you set |
| `optimize_agent_stack` | Estimate a monthly stack cost from a short free-text description of the agent |
| `estimate_job_cost` | Cost of one GPU job among tracked providers (compute subtotal), cheapest first, from hours or throughput |
| `search_deals` | Search agent work-stack deals (compute, search, email, unblock, hosting…) |
| `compare_deals` | Compare 2–5 deals side by side (price, unit, offer type, verification) |
| `get_deal` | One deal's public record by id |
| `rebuild_quote` | Reopen a past quote from a `receipt` returned by optimize_stack, optimize_agent_stack, or estimate_job_cost; checks integrity and revalidates GPU lines against today's feed |

## Public JSON API (GET, no auth)

- GPU prices: `https://thelanternworks.com/api/v1/gpu-prices.json?ref=clawhub`
  (keys include `rates`, `vendors`, `feed_updated_at`, `prices_verified_through`, `methodology`; each rate row has `gpu`, `vram_gb`, `price_usd`, `hourly_equiv_usd`, `tier`, `billing`, `interruptible`, `affiliate`, `verified_at` and a source link)
- GPU price changes: `https://thelanternworks.com/api/v1/gpu-price-changes.json?ref=clawhub` (RSS: `.xml`)
- Work-stack deals: `https://thelanternworks.com/api/v1/deals.json?ref=clawhub`

```bash
curl -s 'https://thelanternworks.com/api/v1/gpu-prices.json?ref=clawhub' | jq '.rates[] | select(.gpu=="H100") | {advertiser, hourly_equiv_usd, tier, verified_at, affiliate}'
```

## Reading the data correctly

- "Cheapest" means cheapest **among tracked providers only**, not the whole market.
- Prices are re-read daily from each vendor's own pricing page; always report the `verified_at` / check date and link the source so the user can confirm.
- `price_usd: null` means the price is **unknown**, not free.
- Rows with `affiliate: true` use referral links; Lantern Works may earn a referral reward. Tell the user when a link you share is a referral link, and offer the vendor's direct pricing page.
- Present options neutrally and let the user's needs (price, availability, interruptibility, billing unit) decide.

## When not to use

Consumer/entertainment purchases (streaming, gaming, food delivery, etc.).

More: https://thelanternworks.com/install/?ref=clawhub
