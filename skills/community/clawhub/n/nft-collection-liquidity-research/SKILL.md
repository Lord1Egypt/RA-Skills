---
name: nft-collection-liquidity-research
description: Compare observed OpenSea collection depth, bids/asks, activity, holders, and traits through Crawlora. Use for a source-attributed liquidity snapshot with chain/contract/item identity, cumulative quantities, currencies, eligibility, observation time, and incomplete coverage preserved.
---

# NFT collection liquidity research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Describe observed marketplace depth and activity for a supplied or discovered
collection set. Establish chain, contract/collection identity, item/trait scope,
quote currency, time window, and what depth/activity comparison is needed.

## Resolve collection identity and distinct surfaces

- Discover chains/categories and collection slugs, then verify actual contract,
  chain, creator, and canonical URL when supplied. Similar display names and
  collection slugs do not prove authenticity or that two contracts represent the
  same assets. Item identity needs chain + contract + token ID, not token ID alone.
- Keep active listings, offers, collection/trait offers, sales, transfers, mints,
  and holder balances separate. `event_types=SALE` selects a sales feed; transfer
  or mint events are not purchases. A top-sales shelf is fixed-size and price-ranked,
  not a chronological complete sales history. Copy opaque returned page cursors.
- Collection depth exposes price levels with cumulative quantities. Preserve
  ladder order and distinguish cumulative depth from marginal quantity; adding
  cumulative levels double counts inventory. Confirm quantity/price basis and
  asset standard rather than equating every row with one unique NFT.
- Offer/listing eligibility, expiration, fees, balances, approvals, and execution
  can differ or be unreported. Keep observed quote/depth separate from evidence
  of a completed sale. Missing detail does not establish a valid fillable order.

```sh
scripts/crawlora.sh /opensea/chains
scripts/crawlora.sh /opensea/search/collections query="art" limit=5
# Resolve a verified collection slug before:
# scripts/crawlora.sh "/opensea/collection/$SLUG/depth"
# scripts/crawlora.sh "/opensea/collection/$SLUG/activity" event_types=SALE limit=20
```

## Compare depth with compatible measures

Use the same item/trait eligibility, timestamp, currency and price basis for
bid/ask comparisons. ETH, WETH, stablecoins and source-provided USD estimates
must not silently share one unit; any conversion needs a dated basis. Preserve
source USD estimates separately from native amounts and execution costs.
A floor ask and collection bid need not cover the same eligible item.

Holder rows represent wallet balances, not unique natural people or verified
beneficial owners. A custodian/contract can hold for many users; several wallets
can belong to one person. Holdings concentration requires compatible complete
supply/balance denominators, not a top-N subtotal. Deduplicate sale events with
transaction/event identity while retaining multi-item/bundle ambiguity and
unknown price-per-item basis. Do not allege wash trading or manipulation solely
from repeated addresses, outliers, or self-transfer-like patterns.

Return collection/contract identity, currency/time and coverage ledger, correctly
interpreted ladders, sampled activity, holder/trait scope, and missing execution
conditions. Do not predict resale value, declare investment quality, connect
wallets, sign transactions, place offers, buy assets, or schedule monitoring
from a snapshot research request.
