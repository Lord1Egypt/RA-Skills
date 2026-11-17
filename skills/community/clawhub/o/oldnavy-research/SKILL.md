---
name: oldnavy-research
description: Researches Old Navy's catalog (and its Gap Inc. sibling storefronts Gap, Banana Republic, Athleta) — categories, products, colors/sizes, in-store pickup availability, and reviews — using the Crawlora API, returning clean JSON. Use when the user asks to find a product on Old Navy/Gap/Banana Republic/Athleta, browse a category, check in-store pickup stock at a specific store, or pull product reviews — instead of scraping oldnavy.com.
---

# Old Navy research

Browse and search Old Navy's catalog (and its Gap Inc. sibling storefronts —
Gap, Banana Republic, Athleta) and pull product detail, per-store pickup
availability, and reviews — all as normalized JSON from the Crawlora API,
with no HTML scraping.

## When to use this skill

- "What does X cost on Old Navy?" or "find X on Old Navy/Gap/Banana
  Republic/Athleta."
- "Browse this Old Navy category" / "what's in Old Navy's [department]?"
- "Is this Old Navy item in stock for pickup near me?"
- "Pull the reviews for this Old Navy product."
- "Find the nearest Old Navy/Gap/Banana Republic/Athleta store."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Find a category id** — `/oldnavy/categories` lists the storefront's own
   navigation as name/`cid` pairs; omit `cid` for the top-level divisions
   (Women, Men, Boys, Toddler), or pass one to list the categories nested
   under it.
2. **Browse or search** — `/oldnavy/category` (`cid`) or `/oldnavy/search`
   (`keyword`) return paginated product summaries with pricing, review
   scores, and every purchasable color variant (`colors[].id`).
3. **Detail** — `/oldnavy/product` (`pid`, a *color-specific* id from a
   result's `colors[].id`, not the base product id) fetches name,
   description, images, rating, and every size offered in that color as a
   priced offer.
4. **Availability** — `/oldnavy/product/availability` (`pid` plus
   `store_id`, or `zip`, or `lat`+`lng`) checks per-size in-store pickup
   stock at one or more physical stores.
5. **Reviews** — `/oldnavy/product/reviews` (`pid`) pulls one page of
   customer reviews plus the rating summary/histogram.
6. **Nearby stores** — `/oldnavy/stores` (`search` and/or `lat`+`lng`) looks
   up physical store locations (address, phone, distance, specialties).

Every call above takes `brand` (`on` Old Navy, `gap` Gap, `br` Banana
Republic, `at` Athleta; defaults to `on`) to pick the storefront — a `cid`
or `pid` only works against the brand it was found under.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Top-level Old Navy divisions, then categories under one:
scripts/crawlora.sh /oldnavy/categories | jq '.'
scripts/crawlora.sh /oldnavy/categories cid=5155 | jq '.'

# Search (defaults to brand=on; pass brand=gap/br/at for the siblings):
scripts/crawlora.sh /oldnavy/search keyword="linen shirt" | jq '.'

# Browse a category:
scripts/crawlora.sh /oldnavy/category cid=5155 page=1 | jq '.'

# Product detail (pid is color-specific, from a search/category colors[].id):
scripts/crawlora.sh /oldnavy/product pid=123456002 | jq '.data'

# In-store pickup availability near a zip code:
scripts/crawlora.sh /oldnavy/product/availability pid=123456002 zip=94103 | jq '.'

# Reviews:
scripts/crawlora.sh /oldnavy/product/reviews pid=123456002 page=1 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Old Navy
endpoint this skill uses (method, path, params, description).

## Examples

- **Category sweep:** `/oldnavy/categories` to find a division's `cid`, then
  `/oldnavy/category` paginated to list products and their color variants.
- **Product due diligence:** `/oldnavy/product` for price/rating detail on a
  color variant, then `/oldnavy/product/reviews` (same `pid`) to summarize
  what customers say before recommending it.
- **Check local pickup:** `/oldnavy/search` or `/oldnavy/category` to get a
  `pid`, then `/oldnavy/product/availability` with `zip` (or `store_id`
  from `/oldnavy/stores`) to see which sizes are in stock nearby.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Old Navy/Gap/Banana Republic/Athleta product and category pages; respect each storefront's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`brand` selects the storefront** (`on`/`gap`/`br`/`at`, defaults to
  `on`) on every endpoint except `/oldnavy/categories`, which currently
  only supports `on` — Gap, Banana Republic, and Athleta render their
  category navigation client-side with no server-rendered id to scrape. A
  `cid` or `pid` only resolves against the brand it was found under.
- **Product identity is `pid`**, a color-specific id from a search/category
  result's `colors[].id` field — not the bare base product id.
  `/oldnavy/product`, `/oldnavy/product/availability`, and
  `/oldnavy/product/reviews` all key off it.
- **`/oldnavy/search` is best-effort relevance, not a guaranteed keyword
  match** — an obscure or nonsense keyword can fall back to the upstream
  index's own recommended results with no signal distinguishing that from
  a true match.
- Pagination is one-based `page` everywhere it applies (`category`,
  `search`, `product/reviews` at 10 reviews/page); a product with no
  reviews yet returns a well-formed empty result, not an error.
- `/oldnavy/product/availability` and `/oldnavy/stores` both accept
  location either as `store_id` (comma-separated) / `search`, or via
  `zip`, or via `lat`+`lng` together — `/oldnavy/stores` is location
  lookup only and doesn't report per-item stock.
