# Recipes

Each recipe names the endpoints; check their docs pages for every field before you write code.

## Track whales and market-wide positioning

1. **Every open position at once:** REST `perpSnapshots` with `"market_names": ["BTC"]` (or `["ALL:ALL_DEXES"]`). The response is zstd-compressed MessagePack; decode with `zstandard` + `msgpack`. Limit: 5 requests per 10 minutes, so poll `perpSnapshotTimestamp` (weight 1) and fetch only when it changes.
2. **A watchlist of wallets:** `batchClearinghouseStates` with up to 1,000 `users` per request (`python scripts/hydromancer.py positions 0x… 0x…`).
3. **Live activity for those wallets:** WebSocket `userFills` and `userOrderUpdates` with an `addresses` list (each address counts as one subscription).
4. **Past days:** Reservoir `by_dex/hyperliquid/snapshots/perp/date=…/` (daily position snapshots).

## A wallet's trade history (tax, PnL, analytics)

- Page `userFillsByTime`: send `startTime` on the first call, then `cursor` = `"<time>_<txIndex>"` of the last fill on each following call, until a page comes back shorter than `limit`. `python scripts/hydromancer.py fills 0x… --hours 720` does this and de-duplicates by `tid`. Tested: paging a busy wallet in pages of 300 returned exactly the same 1,798 fills as one large request.
- Hyperliquid's own API only reaches a user's 10,000 most recent fills; Hydromancer's history endpoints and Reservoir fills (`by_dex/hyperliquid/fills/perp/all/`, filtered by `address`) go further back. Hydromancer's docs say its backfill covers full history for most traders but not for some very high-volume addresses; check the endpoint page for coverage.
- Realised PnL per closed position: `userCompletedTrades` / `userCompletedTradesByTime`; summary stats: `userPnlSummary`.
- Funding and transfers: `userFunding`, `userNonFundingLedgerUpdates`.

## Builder-code revenue and users

- Fills routed through your builder code: `builderFillsByTime` (`builder`, `startTime` or `cursor`, `limit` max 2000). Live: WebSocket `builderFills`, `builderOrderUpdates`, `builderLiquidations`.
- Everything your fee-approved users did, even outside your app: `builderApprovedFillsByTime`, `builderApprovedFundingByTime`, `builderApprovedNonFundingLedgerUpdatesByTime` (weight 100 each), or the matching `builderApproved*` WebSocket channels.
- Which builders a user has approved: `approvedBuilders`; the cap a user set for you: `maxBuilderFee`.
- History for research: Reservoir `by_dex/hyperliquid/fills/perp/builder_fills/`.

## Liquidation feed and history

- Live: WebSocket `{"method": "subscribe", "subscription": {"type": "liquidationFills"}}` (optional `"aggregateByTime": true`).
- Recent history: REST `liquidationHistoryByTime` with optional `coin` (omit for market-wide), `startTime`, `endTime`, `limit` up to 1000 (`python scripts/hydromancer.py liquidations --coin BTC --hours 6`).
- Long history: Reservoir `by_dex/hyperliquid/fills/perp/liquidations/` and `…/adl/`.

## A local L4 order book (every resting order, with its owner)

1. Subscribe to WebSocket `l4BookUpdates` with `"coins": ["BTC"]` and buffer the updates.
2. Fetch a REST `l4Book` snapshot (20 requests per 5 minutes).
3. Apply buffered updates newer than the snapshot's height, then keep applying live ones.
4. On `resync required`, start again from step 1.

The SDK does this for you: `from hydromancer_sdk import OrderbookStream` / `L4OrderbookClient` (Python 3.11+, pinned by commit in `requirements-sdk.txt`). Guide: https://docs.hydromancer.xyz/readme/builder-guides/l4-orderbook-streaming

## HIP-4 prediction markets

- Active outcomes and their sides: `outcomeMeta` (optional `venue`, `deployedBy`).
- New markets: `registeredOutcomes`; results with settle data and trading stats: `settledOutcomes` / `settledOutcomesById`.
- Live registration and settlement events: WebSocket `hip4MarketEvents` (filter by `venue`).

## Backtesting

- Prices and trades: Reservoir 1-second candles and fills (see [reservoir.md](reservoir.md)); aggregate candles to your bar size in DuckDB.
- Execution realism: Reservoir 1-minute L2 order book snapshots, or REST `slippageHistory` / `marketLiquidityHistory` for a market and notional size.
- Funding: REST `fundingHistory` per coin.
