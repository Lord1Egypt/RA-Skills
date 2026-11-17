---
name: google-finance-research
description: Retrieve Google Finance quote, company, chart, financial, news, related-instrument, and market snapshots using Crawlora. Use for source-attributed market lookups, instrument comparisons, or Google Finance market briefs; excludes trading and portfolio actions.
---

# Google Finance market snapshots

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Retrieve public Google Finance observations and compare like instruments.
This workflow supplies sourced market data, not a personalised trading decision.

## Resolve instruments and requested surfaces

- Use `google_finance_search` or `google_finance_context` to resolve an instrument
  before quoting it. Preserve the exchange-qualified quote such as `AAPL:NASDAQ`,
  currency, instrument type, and market; a ticker alone can be ambiguous.
- Fetch quote/company/financial/chart/news/related/classification surfaces only
  for the requested brief. `google_finance_ticker` is a distinct lookup route;
  do not replace an exchange-qualified quote with an arbitrary search hit.
- Chart windows must be documented values (`1d`, `5d`, `1m`, `6m`, `ytd`, `1y`,
  `5y`, `max`). Match time window, currency, exchange session, and sampling before
  comparing series. Do not infer split/dividend adjustment or a live executable
  price unless the returned evidence actually establishes it.
- Market overview, indices, movers, featured, trending, top, and earnings routes
  are snapshots of different source selections. Category-stock/news and category
  filters take numeric source category IDs. Use only IDs returned by market
  metadata/results or documented in the reference; if no usable ID is available,
  leave that slice unqueried instead of inventing a sector-to-ID mapping.

```sh
scripts/crawlora.sh /google/finance/search q="Apple"
scripts/crawlora.sh /google/finance/markets/indices
# After verifying the quote identifier from search:
# scripts/crawlora.sh "/google/finance/quote/$QUOTE_ID"
# scripts/crawlora.sh "/google/finance/chart/$QUOTE_ID" window=1m
# scripts/crawlora.sh "/google/finance/financials/$QUOTE_ID"
```

## Preserve measurement and uncertainty

Show source timestamp where supplied and collection time separately. Mark delay
or freshness unknown if the source does not state it; polling does not make a
quote real-time. Keep reported financial periods, units, currency, and estimates
separate. A missing metric is unknown, not zero. Attribute news and analyst
articles, and avoid treating related instruments as equivalent risk exposures.
Return a quote/period comparison table with provenance and missing fields.
Market movers and historical returns do not establish future performance.
Do not place orders, access accounts, or create a portfolio from this request.
