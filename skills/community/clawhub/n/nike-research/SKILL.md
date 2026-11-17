---
name: nike-research
description: Researches Nike's catalog — categories, search, product detail, colorways, reviews, and nearby stores — using the Crawlora API, returning clean JSON. Use when the user asks to find a Nike product, browse a Nike category, compare Nike colorways/prices, pull Nike product reviews, or locate nearby Nike stores — instead of scraping nike.com.
---

# Nike research

Browse and search Nike's catalog and pull product detail, colorways,
reviews, and nearby store locations — all as normalized JSON from the
Crawlora API, with no HTML scraping.

## When to use this skill

- "What does X cost on Nike?" or "find X on Nike."
- "Browse this Nike category" / "what's in Nike's [Men's Running Shoes]?"
- "Compare colorways/prices for this Nike shoe."
- "Pull the reviews for this Nike product."
- "Find the nearest Nike store to [location]."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse categories** — `/nike/categories` lists Nike's Men/Women/Kids/Jordan
   taxonomy; each subcategory carries a `slug` for browsing.
2. **Search or browse** — `/nike/search` takes exactly one of `keyword` or
   `category` (never both). `keyword` runs Nike's own relevance search;
   `category` browses a taxonomy slug (from `/nike/categories` or a prior
   response's `facet_nav`). Both return product groups with pricing,
   colorway images, and every purchasable color variant, paginated with
   `page`. Use `/nike/suggest` (`query`) first if you want typeahead ideas
   for a vague keyword.
3. **Product detail** — `/nike/product` fetches one color variant, keyed by
   the pair `slug` + `style_color` pulled from a search result's
   `colors[].slug` / `colors[].style_color` — there's no single product id.
4. **Reviews** — `/nike/product/reviews` (same `slug` + `style_color` pair,
   paginated with `page`) returns written reviews plus an aggregate rating
   breakdown.
5. **Nearby stores** — `/nike/stores` (`lat`, `lng`, optional `radius_miles`)
   returns nearby physical stores with address, phone, and distance.
6. **Compare** the JSON fields (price, colorway, rating, distance) across
   items or stores and answer.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Browse a category (slug from /nike/categories):
scripts/crawlora.sh /nike/search category="mens-shoes" | jq '.'

# Keyword search:
scripts/crawlora.sh /nike/search keyword="air max" page=2 | jq '.'

# Product detail (slug + style_color from a search result's colors[]):
scripts/crawlora.sh /nike/product slug="nike-air-max-90-mens-shoes-6n3vKB" style_color="CN8490-002" | jq '.data'

# Reviews:
scripts/crawlora.sh /nike/product/reviews slug="nike-air-max-90-mens-shoes-6n3vKB" style_color="CN8490-002" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Nike
endpoint this skill uses (method, path, params, description).

## Examples

- **Category sweep with colorway comparison:** `/nike/categories` to find a
  subcategory `slug`, then `/nike/search` with `category` set, paginated, to
  list products and compare price/colorway across each result's `colors[]`.
- **Product due diligence:** `/nike/search` (or `/nike/suggest`) to find a
  product's `slug`/`style_color`, then `/nike/product` for pricing/sizes and
  `/nike/product/reviews` to summarize the rating breakdown and what
  reviewers say before recommending it.
- **Nearest store lookup:** `/nike/stores` with a location's `lat`/`lng` to
  list nearby stores by distance, with address and phone for the closest
  match.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Nike product/category/store pages; respect Nike's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`/nike/search` takes exactly one of `keyword` or `category`** — passing
  both, or neither, is invalid.
- **Product identity is `slug` + `style_color` together**, not a single SKU
  or product id — `/nike/product` and `/nike/product/reviews` both require
  the pair, sourced from a search result's `colors[].slug` /
  `colors[].style_color`.
- **Keyword search is best-effort relevance, not a guaranteed match:** for
  an obscure or nonsense keyword, Nike's own index falls back to its
  recommended results instead of an empty list, and the response has no
  reliable signal to tell a true match from that fallback — don't treat a
  non-empty `keyword` result as proof the term was actually found. A
  punctuation-only/structurally-empty query does return a genuine empty
  result.
- Results are paginated — pass `page` to walk `/nike/search` and
  `/nike/product/reviews`; requesting a page past the last one returns a
  not-found error on both.
