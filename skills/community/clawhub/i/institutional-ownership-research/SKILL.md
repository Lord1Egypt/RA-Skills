---
name: institutional-ownership-research
description: Compare reported institutional-manager 13F holdings through Crawlora live SEC and stored position tools. Use for portfolio concentration, reported-position overlap, or issuer-holder evidence with manager identity, filing lag, truncation, security class, and value units preserved.
---

# Institutional ownership research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Describe reported 13F positions for selected managers or an issuer. Establish
manager versus issuer direction, the requested reporting period, and whether
concentration, overlap, or a holder shortlist is needed. These are delayed
reported positions, not complete current portfolios or real-time trades.

## Resolve managers and filing scope

- Discover manager/issuer facet values from stored positions. `manager_cik` is
  an exact manager filter; it is not the issuer's ticker or company CIK.
  `issuer_name`/`cusip` queries are best-effort holder discovery: no authoritative
  CUSIP-to-company-CIK join is supplied, so verify class and identity before joining.
- Stored search returns each manager's latest indexed filing. Live
  `sec_institutional_holdings` also returns the latest 13F-HR, with a maximum
  `limit` of 1000. Neither route offers a structured arbitrary-quarter portfolio
  history. Historical comparison needs actual comparable saved filings, not
  a fictional period parameter or presumed previous-quarter values.
- Preserve accession, report date, filing date, source URL, and collection/crawl
  time. Refresh selected managers and reconcile by accession; different filing
  dates or quarters cannot be merged silently. Submissions/filing metadata help
  locate documents and versions but do not return historical parsed holdings.
- Dataset pages have a 10,000-result window; live `count` can be less than
  `total_holdings` because of the requested limit. Keep completeness visible.
  An empty dataset may mean no indexed data, not absence of an institution's position.

```sh
scripts/crawlora.sh /datasets/sec-institutional-positions/facets facet=manager
# Use a discovered manager CIK, for example:
# scripts/crawlora.sh /datasets/sec-institutional-positions/search manager_cik="$MANAGER_CIK" page=1 page_size=100
# scripts/crawlora.sh /sec/institutional-holdings cik="$MANAGER_CIK" limit=1000
```

## Compare positions without changing their meaning

Use CUSIP plus security class, `share_type`, and `put_call` for comparable
positions. Keep options, common/preferred classes, and share/principal amounts
separate; do not sum all `shares` into a stock ownership percentage. Preserve
investment discretion and duplicate-looking rows until their accounting basis
is understood. A matching issuer name alone cannot resolve share classes.

The live parser preserves source table `value` numbers; it does not supply a
universal conversion scale. Dataset documentation describes thousands of USD,
but do not apply that multiplier to every filing or source without verifying
its reported units. Retain raw units/assumptions, and mark absolute dollar totals
unverified if the underlying filing's scale cannot be established. Cross-manager
value comparisons require compatible units and reporting periods.

For a uniformly scaled single filing, `position weight = value / total_value`
can use the same filing's full summary total even when returned holdings are
truncated; label the numerator's actual position definition. Never replace
that denominator with a top-N subtotal and call it whole-portfolio concentration.
For incomplete overlap, show returned-position overlap and missing counts;
full-set weighted overlap requires compatible units and complete comparable sets.

Return identity/filing coverage, comparable position rows, disclosed formulas,
concentration/overlap scope, and unresolved joins. Do not infer trade dates,
investor intent, current company ownership percentages, short exposure, or
investment performance from these snapshots. No trading or account action is
part of this research request.
