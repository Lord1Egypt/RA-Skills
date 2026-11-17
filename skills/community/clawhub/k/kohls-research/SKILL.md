---
name: kohls-research
description: Researches Kohl's catalog by browsing its category taxonomy (products, prices, ratings, and facets), pulls product reviews by web_id, finds nearby Kohl's stores, and returns search-box typeahead suggestions — all via the Crawlora API as clean JSON. Use when the user asks to browse a Kohl's category, discover Kohl's product ideas for a query, pull reviews for a specific Kohl's item, or find nearby Kohl's stores — instead of scraping Kohls.com.
---

# Kohl's research

Browse Kohl's own catalog taxonomy to list products with pricing and
ratings, pull a specific product's customer reviews, find nearby store
locations, and get search-box typeahead suggestions — all as normalized
JSON from the Crawlora API, with no HTML scraping.

## When to use this skill

- "What's in Kohl's [category], e.g. Room:Dorm or Department:Bedding?"
- "What would Kohl's suggest if someone starts typing '[partial query]'?"
- "Pull the reviews for this Kohl's product."
- "Find the nearest Kohl's to [city/state, ZIP, or address]."
- "Discover Kohl's subcategories under [department]."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse a category** — `/kohls/category` (`category`) returns a
   category or curated campaign page's product grid (page 1 only) plus
   `facets` for discovering further category values. `category` is
   Kohl's own taxonomy string, e.g. `"Room:Dorm"` or
   `"Department:Kitchen & Dining"`; combine multiple dimensions with a
   literal `+`, percent-encoded as `%2B` so it survives as `+` rather than
   being decoded to a space, e.g. `"Room%3ADorm%2BDepartment%3ABedding"`.
2. **Discover the taxonomy** — every `facets[].options[].category` value in
   a response is a ready-to-use `category` string for a follow-up call, so
   start from a known category and follow facets to enumerate related
   departments/rooms/brands rather than guessing strings. An unrecognized
   `category` value returns `404`; a recognized dimension with no matching
   products returns a genuine zero-result response.
3. **Get typeahead ideas** — `/kohls/suggest` (`query`) returns Kohl's own
   search-box suggestions for a partial query as a flat list of phrases
   (no product data) — useful for finding a category to browse, not for
   pulling products directly.
4. **Reviews** — `/kohls/product/reviews` (`web_id`, optional `page`, 10
   per page) pulls a specific product's reviews (title, text, rating,
   secondary ratings, reviewer, date, photos). `web_id` comes from a
   `/kohls/category` response's `products[].web_id` field.
5. **Stores** — `/kohls/stores` (`search`) finds nearby Kohl's locations
   by free-text city/state, ZIP, or address: address, phone, hours,
   distance, and badges/services.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Browse a category (product grid + facets for further categories):
scripts/crawlora.sh /kohls/category category="Room:Dorm" | jq '.'

# Combine two taxonomy dimensions (literal "+", percent-encoded as %2B):
scripts/crawlora.sh /kohls/category category="Room%3ADorm%2BDepartment%3ABedding" | jq '.'

# Reviews for a product found in a category response's products[].web_id:
scripts/crawlora.sh /kohls/product/reviews web_id=4739201 page=1 | jq '.'

# Nearby stores and typeahead suggestions:
scripts/crawlora.sh /kohls/stores search="Chicago, IL" | jq '.'
scripts/crawlora.sh /kohls/suggest query="dorm bedding" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Kohl's
endpoint this skill uses (method, path, params, description).

## Examples

- **Category sweep with reviews:** `/kohls/category` with `category="Room:Dorm"`
  to list products and pricing, pick a `products[].web_id`, then
  `/kohls/product/reviews` to summarize what buyers say before recommending it.
- **Taxonomy discovery:** `/kohls/category` on a known starting category, then
  follow `facets[].options[].category` values to find and browse related
  departments, rooms, or brand filters the user didn't name explicitly.
- **Nearby store lookup:** `/kohls/stores` with a city/state or ZIP to list
  nearby locations, hours, and services.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Kohl's category, review, store, and suggest
  pages; respect Kohl's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No full-text product search or single-product lookup exists.** Product
  discovery is only through `/kohls/category` taxonomy browsing (following
  `facets[].options[].category` values) and `/kohls/suggest` typeahead
  phrases — there is no `/kohls/product` or `/kohls/search` endpoint, so a
  free-text query has to be resolved to a `category` string (or a
  suggestion) before you can list products.
- `/kohls/category` only returns page 1 of a category's product grid —
  there is no page parameter for deeper pagination.
- `web_id` for reviews comes from a prior `/kohls/category` call's
  `products[].web_id` — there's no way to look up reviews from a bare
  product name or URL.
