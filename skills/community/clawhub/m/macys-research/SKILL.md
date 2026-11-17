---
name: macys-research
description: Looks up a Macy's product's full detail and customer reviews by its numeric productId, and pulls Macy's own search-box (typeahead) suggestions, using the Crawlora API, returning clean JSON. Use when the user has (or can get) a Macy's product page ?ID= value and wants its price/description/variants/reviews, or wants Macy's autocomplete suggestions for a query — instead of scraping macys.com. There is no full-text product search or category browse — a known numeric productId is required as the entry point.
---

# Macy's research

Look up a specific Macy's product's detail and reviews by its numeric
productId, and pull Macy's own typeahead suggestions — all as normalized
JSON from the Crawlora API, with no HTML scraping. This skill does not
cover search or category browsing; it only works from a known productId.

## When to use this skill

- "What does this Macy's product cost / what's in the description?" given
  a macys.com product URL or its `?ID=` value.
- "Pull the reviews and rating summary for this Macy's product."
- "What does Macy's autocomplete suggest for [query]?" to discover related
  search terms.
- "Summarize this Macy's item's colors, pricing, and customer sentiment"
  for a known product.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Get a productId** — a numeric id taken from a macys.com product page's
   `?ID=` query parameter (or otherwise already known/discovered). There is
   no search or category endpoint in this skill to find one from a keyword.
2. **Detail** — `/macys/product/{productId}` returns full product content:
   name, brand, description, department/division, category breadcrumb,
   pricing (with sale detection), availability, images, aggregate rating,
   and every purchasable color variant with its own price.
3. **Reviews** — `/macys/product/reviews` (`product_id`, paginated with
   `page`) returns one page of normalized customer reviews plus a
   site-wide rating summary (count, average, recommended ratio, histogram)
   for that product.
4. **Suggest** — `/macys/suggest` (`query`) returns Macy's own search-box
   typeahead phrases for a partial query — a flat list of strings, no
   product data — useful for discovering related terms, not for finding a
   productId.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Product detail (productId is a path param):
scripts/crawlora.sh /macys/product/12345678 | jq '.data'

# Reviews for that same product, paginated:
scripts/crawlora.sh /macys/product/reviews product_id=12345678 page=1 | jq '.'

# Search-box suggestions for a partial query:
scripts/crawlora.sh /macys/suggest query="winter coat" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Macy's
endpoint this skill uses (method, path, params, description).

## Examples

- **Product due diligence:** `/macys/product/{productId}` for
  price/description/variants, then `/macys/product/reviews` (same
  `product_id`, paginated) to summarize what customers say before
  recommending it.
- **Term discovery:** `/macys/suggest` on a rough query to see Macy's own
  suggested phrases — useful context when a user asks about a product
  category, even though this skill can't browse or search that category
  directly.

## Notes & limits

- **No search or category-browse endpoint** — this skill requires a known
  numeric `productId`, sourced from a macys.com product page's `?ID=`
  query parameter, as the entry point. `/macys/suggest` only returns
  suggested search phrases (no product data), so it cannot substitute for
  search when the user doesn't already have a productId.
- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Macy's product pages; respect Macy's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- `product_id` on `/macys/product/reviews` is the same numeric id as
  `productId` on `/macys/product/{productId}` — a product with zero
  reviews, or a well-formed but unrecognized id, returns a normal, empty
  result rather than an error.
- Reviews are paginated with a 1-based `page`, defaulting to 1.
