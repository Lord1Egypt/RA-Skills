# PreStocks products and notices

Use --platform prestocks. Observer reads the actual products list at
https://prestocks.com/products, public metrics/reference-price endpoints and
product disclosures. assetId is the Solana mint: preserve its case exactly.

Filters: --industry and --status listed|normal|attention|removed|all.
Default listed includes normal and attention, not removed.
Sorts: volume_desc (default), valuation_asc, premium_asc, holders_desc,
change30d_desc. All sorts prioritize normal before attention before removed,
then sort within the status group; do not call the first item a global raw rank.

## Metrics

- tokenPrice / markPrice: USD token market/reference prices.
- premiumPct: percentage token price deviation from reference price, already
  in percent. Negative numbers are discounts, not guaranteed bargains.
- marketCapUSD: token capitalization; NOT company valuation.
- impliedValuation / markValuation: USD company valuation proxies based on the
  platform's registered basis and effective unit adjustments, not financing
  valuations or direct ownership. Missing valid basis returns null.
- cumulativeVolumeUSD and txnCount are cumulative, not 24-hour measures.
- change30dPct is 30-day price change, not historical valuation range return.
- holderCount, circulatingSupply and totalSupply are source token metrics.
- Detail includes baselinePrice, baselineValuationBillions, basisEvents,
  unitFactor and effective baseline fields. Keep billions distinct from USD.

## Risk notices and freshness

Preserve warnings.original, summaryZh, sourceUrl, checkedAt and deadlineAt.
SpaceX/xAI or any attention-state product must retain its platform notice when
discussed, including the original source and date. After the deadline, say
“期限已过，请核验”; do not assert invalidity, actual tradability or redemption outcome.
warningCheckFailed means verification is delayed, not that the risk disappeared.

fetchedAt is retrieval time; lastSuccessfulAt is platform publication time;
warningsCheckedAt dates notice verification. Respect stale; do not present an
old snapshot as a current price.

Summary exposes total, attentionCount, removedCount, cumulativeVolumeUSD /
volumeCoverage, marketCapUSD / marketCapCoverage and industries. Do not calculate
a combined company valuation from products.

    node scripts/query-preipo.mjs list --platform prestocks --status attention
    node scripts/query-preipo.mjs list --platform prestocks --status normal --sort valuation_asc
