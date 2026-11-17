# Hyperliquid contracts

Use --platform hyperliquid. Observer captures the official preipo category from
Hyperliquid's public Info API; it is not a list of directly owned company shares.

Filters: --operator (dex ID, not display name), --industry (exact summary value),
--status active|delisted|removed|all. Default status active.
Sorts: volume_desc (default), change_desc, oi_desc.
Copy the full assetId such as io:OAI; the same symbol on a different dex is a
different contract. detail/report must not strip the operator prefix.

## Fields and units

- companyName, companyId, industry and reportHref use explicit company mapping;
  unknown mappings can remain unclassified and have no research link.
- markPx, oraclePx, midPx and prevDayPx are source-unit prices, not company funding
  valuations. change24hPct is already a percentage.
- volume24h and openInterestNotional are in settlementCurrency. Never sum USDC
  and USDH buckets as an undifferentiated USD number.
- openInterest is position quantity; openInterestNotional is markPx × quantity.
- fundingRate is the hourly decimal rate: 0.00001 becomes 0.001%, not 0.00001%.
  Do not annualize or describe a quoted rate as guaranteed return.
- sourceUrl is the original market; fetchedAt is record retrieval time.
  lastSuccessfulAt is the last successful platform snapshot. Respect stale.
- removed means no longer in the observed category; delisted is a separate source
  status. active does not guarantee executable trades.

Summary exposes total, activeCount, delistedCount, removedCount, operators,
industries and currencies. Each currency has marketCount, volume24h,
volumeCoverage, openInterestNotional and openInterestCoverage. Coverage matters:
a missing quote or aggregate is not zero.

    node scripts/query-preipo.mjs list --platform hyperliquid --operator io --sort oi_desc
    node scripts/query-preipo.mjs detail io:OAI --platform hyperliquid
