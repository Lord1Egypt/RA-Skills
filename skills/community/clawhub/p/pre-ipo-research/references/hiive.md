# Hiive50 manual snapshot

Use --platform hiive. The source universe is the application's Hiive50 at
https://app.hiive.com/hiive50, not the public site's separate quarterly ranking.
The distributed skill reads Observer APIs only; it never opens an authenticated
Hiive session, captures cookies or imports snapshots.

Filters: --industry; --status listed|removed|all (default listed).
Sorts: name_asc (default), change3m_desc, hiive_price_desc, orders_desc.
assetId is the exact UUID or registered stable fallback returned by the API;
never derive it from companyName. Placeholder company links and null detail
fields do not make a company disappear from the constituent list.

- hiivePrice: platform model-estimated per-security USD reference price.
- change3mPct: source three-month change, already in percent, including negatives.
- highestBid / lowestAsk: independent source quotes; not executable guarantees.
- activeListings / activeBids: counts; zero is zero and null remains unavailable.
  orders_desc uses the existing server's combined count ordering, including its
  treatment of missing counts; do not infer fully observed liquidity from rank.
- description retains saved source text or available reused Chinese content;
  null means no captured profile, not a nonexistent business.
- sourceUrl, companyUrl and reportHref have different purposes; preserve them.

summary.snapshotMode is manual. Show sourceUpdatedAt (source page time),
fetchedAt (collection time) and lastSuccessfulAt (Observer import time) as
distinct labels, even when their returned values happen to be identical.
There is no 15-minute stale rule or guaranteed daily update for Hiive.

Summary includes total retained records, listedCount, removedCount,
marketCoverage (current constituents with price), and industries with counts.
Application order is not an official rank. Do not infer company valuations,
investment returns or availability from missing bid/ask.

    node scripts/query-preipo.mjs search Replit --platform hiive
    node scripts/query-preipo.mjs list --platform hiive --sort change3m_desc
