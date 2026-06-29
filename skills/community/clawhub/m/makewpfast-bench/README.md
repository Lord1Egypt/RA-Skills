# makewpfast-bench

Ask about the **real, measured** performance impact of any WordPress plugin or theme — straight
from your agent. Wraps the [MakeWPFast Benchmark API](https://makewpfast.com/api/): speed grades
plus TTFB, memory, and query deltas for ~52,000 WordPress.org plugins and themes, each measured
in three contexts (activation, homepage, wp-admin) against a clean WordPress baseline.

```
> how fast is WooCommerce?
WooCommerce  [woocommerce]
  Speed score: D (39/100)   measured 2026-04-19
  activation : +9ms TTFB, +6144KB, +41 queries
  homepage   : +25ms TTFB, +6144KB, +41 queries
  admin      : +2ms TTFB, +0KB, +0 queries
  7,000,000 active installs · 90% rating
```

## What it does

- **`lookup`** — benchmark one plugin/theme by name or slug
- **`compare`** — side-by-side speed comparison of several plugins/themes, with a plain-English winner
- **`audit`** — detect the active plugins of a local WordPress install (via wp-cli) and rank the heaviest
- **`me`** — your tier, quota, and usage (free, never charged)
- **`resolve`** — turn a name like "Yoast SEO" into its WordPress.org slug

## Why it's not just `curl`

The API is paid and quota-limited. This skill is built to **spend as little of your quota as possible**:

- **Local cache** (21-day TTL) — repeated questions are free.
- **Free name→slug resolution** via the WordPress.org API before any paid call, so you can say
  "WooCommerce" instead of memorizing `woocommerce` — and the agent never burns quota guessing slugs.
- **Batch guards** — refuses large uncached lookups unless you opt in.
- **An audit log** (`~/.cache/makewpfast-bench/calls.log`) so you can see exactly what used quota.

## Setup

1. Get an API key — subscribe at **https://makewpfast.com/api/** (from $49/mo).
2. Store it: `scripts/mwf-bench auth` (stored in your OS keychain or a `0600` file), or
   `export MWF_API_KEY=mwf_live_...`.

No key configured? The skill tells you where to get one and never makes a paid call.

## Requirements

- Python 3 (standard library only — zero dependencies)
- `wp-cli` (only for the `audit` command)

## Pricing

| Tier | Price | Monthly requests |
|------|-------|------------------|
| Starter | $49/mo | 50,000 |
| Pro | $149/mo | 500,000 |
| Scale | $499/mo | 5,000,000 |

The dataset and API are by [MakeWPFast](https://makewpfast.com). Questions: contact@makewpfast.com
