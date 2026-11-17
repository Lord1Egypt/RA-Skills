---
name: microsoft-store-research
description: Research Microsoft Store apps and games using Crawlora search, categories, charts, publisher listings, product details, and reviews. Use to compare Windows apps, investigate a publisher, inspect store awards, or sample regional app reviews.
---

# Microsoft Store research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Compare Microsoft Store listings, regional offers, charts, and review evidence.
Keep Windows apps, games, subscriptions, themes, and device listings distinct.

## Discover, sample, and verify

- Fix store `country` and display `locale` before discovery. Search with a clear
  `media_type`; `all` ignores the category filter. Discover exact categories via
  `microsoftstore_categories`, including department-specific differences.
- Resolve the returned `product_id` before product, related, review, or review
  summary requests. Inspect publisher and listing kind to avoid confusing a
  similarly named third-party app with an official product.
- Charts use their own documented `list` values. App subcategories require their
  parent category on charts; a chart subcategory is not a valid search category.
  Award `editorial_id` values link to the editorial endpoint; do not invent IDs.
- Search follows opaque `next_cursor`; charts and reviews use documented page
  parameters. Stop at the budget or pagination end and record the sample coverage.
- Use publisher, spotlight, recommendation, and event surfaces only when they
  address the request. Related listings are recommendations, not verified clones.

```sh
scripts/crawlora.sh /microsoftstore/categories
scripts/crawlora.sh /microsoftstore/search query="note taking" media_type=apps country=US locale=en-US
scripts/crawlora.sh /microsoftstore/charts list=TopFree media_type=apps country=US locale=en-US
# Use a returned product_id for both calls:
# scripts/crawlora.sh /microsoftstore/product product_id="$PRODUCT_ID" country=US locale=en-US
# scripts/crawlora.sh /microsoftstore/reviews product_id="$PRODUCT_ID" sort=MostRecent page=1
```

## Compare and deliver

Preserve price currency, region, observation time, listing kind, publisher,
platform requirements, and available release dates. A free listing can still
have paid features; do not infer licensing or total cost from its sticker price.
Formatted rating counts such as `34K` are approximate, not exact review totals.
Keep review-page samples separate from aggregate ratings and review summaries;
a few reviews cannot establish population sentiment or download counts. A chart
position is not revenue or installation volume. Return a sourced comparison,
review themes with sample size, and compatibility/pricing questions still open.
Do not install apps, subscribe, or purchase from a store research request.
