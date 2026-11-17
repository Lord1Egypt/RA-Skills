# WebSocket

```
wss://api.hydromancer.xyz/ws?token=$HYDROMANCER_API_KEY        (testnet: wss://api-testnet.hydromancer.xyz/ws)
```

The key is accepted only as the `token` query parameter; an `Authorization` header is answered with "Missing token query parameter". Because URLs can be logged by proxies, load balancers and crash reporters: connect from server-side code only, never log the full URL, mask `token=` in errors, use a separate key per app and environment, and ask Hydromancer (data@hydromancer.xyz) to revoke and reissue a key whose URL may have been logged.

## Messages

Subscribe (the optional `requestId`, up to 128 characters, is echoed back):

```json
{"method": "subscribe", "requestId": "trades-1", "subscription": {"type": "trades", "coins": ["BTC"]}}
```

Unsubscribe with `"method": "unsubscribe"` and the same `subscription`. On connect the server sends `{"type": "connected", "clientId": …, "sessionId": …}`. Each subscribe is answered with `{"type": "subscriptionUpdate", "operation": "subscribe", "subscribed": [...], "failed": [...]}`, which may include advisory `warnings` (for example `inactive_coins`). Ignore unknown fields and message types; the protocol adds them over time.

Live messages carry the channel `type`, a per-subscription `seq` and a `cursor`, for example:

```json
{"type": "trades", "channel": "trades", "seq": 1, "cursor": "1201104261:1793245771014", "trades": [{"coin": "BTC", "side": "B", "px": "79872", "sz": "0.00043", "time": 1793245771014, "tid": 470769276987761, "users": ["0x…", "0x…"]}]}
```

## Heartbeat

The server sends `{"type": "ping"}` every 60 seconds. Reply `{"type": "pong"}` (JSON, on the same socket) or the connection is closed. Library-level WebSocket pings don't cover this. `scripts/stream_trades.py` shows the loop; tested for 150 seconds with three pings answered.

## Sessions, cursors and replay

- Save `sessionId` from the `connected` message, and the `cursor` from each message after you have processed it (an opaque string).
- **To resume, reconnect with both on the URL:** `wss://api.hydromancer.xyz/ws?token=…&sessionId=<id>&cursor=<last cursor>`. The server restores all your subscriptions and replays what you missed, so don't subscribe again. (A subscribe request carrying a `cursor` replays just that subscription.)
- Replay arrives as `{"type": "replay", …}` chunks before the live stream resumes. Each chunk has its own `cursor`; update yours as chunks arrive. `hasMore` is `false` on the last chunk, and `hasGap: true` marks a replay that could not cover the whole gap.
- Replay windows: up to 3 minutes for `l4BookUpdates`, 5 minutes for order updates, 15 minutes for other replayable channels, or 30 seconds where only the in-memory cache serves them. An older cursor replays only the last window.
- `bbo`, `l2Book`, `allActiveAssetCtx` and `setOracleUpdates` are live-only (their cursor is `"0"`).
- On a `resync required` error, reconnect without the cursor and without the `sessionId`, then rebuild: subscribe, buffer live updates, fetch a REST snapshot (for example `l2BookDiffSnapshot` or `l4Book`), then apply buffered updates newer than the snapshot.
- Don't send a burst of subscribes while a replay is running.
- Full details: https://docs.hydromancer.xyz/readme/websocket/session-management-and-reconnection

## Limits

Limits depend on the key. Current ranges:

- Connections 50 to 1,000; total subscriptions 500 to 10,000; inbound messages 300 to 6,000 per minute.
- Per-coin streams, for example: `l4BookUpdates` 10 to 200 coins, `l2Book` 10 to 100, `bbo` 20 to 200, `trades` and `allFills` 20 to 200 coins.
- Each address in `userFills`, `userOrderUpdates` and similar counts as one subscription.
- All-coin streams (`allFills` or `trades` with no coin filter, `l4BookUpdatesAll` and so on) need extra permission on the key.
- Current table: https://docs.hydromancer.xyz/readme/websocket/rate-limits-user-limits-and-heartbeats

## Channel catalog

Generated from https://docs.hydromancer.xyz/llms.txt.

### Builder data

Stream live orders, fills, funding and ledger events for a builder and its fee-approved users.

| type | What it returns | Docs |
|---|---|---|
| `builderOrderUpdates` | Stream live order updates for a specific builder from a single connection. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderorderupdates) |
| `builderFills` | Stream live fills for a specific builder from a single connection. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderfills) |
| `builderApprovedFills` | Stream every fill made by users who had an active fee approval for your builder at the time of the fill. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderapprovedfills) |
| `builderApprovedFundings` | Stream every hourly funding payment of users who had an active fee approval for your builder at the funding block. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderapprovedfundings) |
| `builderApprovedNonFundingLedgerEvents` | Stream every non-funding ledger update of users who had an active fee approval for your builder at the block. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderapprovednonfundingledgerevents) |
| `builderLiquidations` | Stream live liquidation fills of your users. Based on last touch attribution, if the last non-liquidation fill for that coin had your builder code, the liquidation will be broadcast to your channel. | [docs](https://docs.hydromancer.xyz/readme/websocket/builder-data/builderliquidations) |

### Orderbook streaming

Stream live BBO, L2 snapshots, L2 diffs and L4 orderbook updates.

| type | What it returns | Docs |
|---|---|---|
| `bbo` | Stream live best bid and offer for a coin. | [docs](https://docs.hydromancer.xyz/readme/websocket/orderbook-streaming/bbo) |
| `l2Book` | Stream live L2 orderbook snapshots per coin. | [docs](https://docs.hydromancer.xyz/readme/websocket/orderbook-streaming/l2book) |
| `l2BookDiff` | Stream live L2 orderbook diffs (incremental updates) per block. | [docs](https://docs.hydromancer.xyz/readme/websocket/orderbook-streaming/l2bookdiff) |
| `l4BookUpdates` | Stream live L4 orderbook updates per block. | [docs](https://docs.hydromancer.xyz/readme/websocket/orderbook-streaming/l4bookupdates) |

### TP/SL streaming

Stream live TP/SL trigger order updates per block.

| type | What it returns | Docs |
|---|---|---|
| `tpslUpdates` | Stream live TP/SL trigger order updates per block. | [docs](https://docs.hydromancer.xyz/readme/websocket/tp-sl-streaming/tpslupdates) |

### Candles

Stream live OHLCV candle updates for one coin or all coins.

| type | What it returns | Docs |
|---|---|---|
| `candle` | Stream live OHLCV candle updates for a specific coin and interval. | [docs](https://docs.hydromancer.xyz/readme/websocket/candles/candles) |
| `allCandles` | Stream live OHLCV candle updates for all coins at a specific interval, batched per block. Needs extra permission on the key. | [docs](https://docs.hydromancer.xyz/readme/websocket/candles/allcandles) |

### Trades data

Stream all fills, liquidation fills and live trades.

| type | What it returns | Docs |
|---|---|---|
| `allFills` | Stream all fills, optionally filtered to one or more coins. | [docs](https://docs.hydromancer.xyz/readme/websocket/trades-data/allfills) |
| `liquidationFills` | Stream all liquidation fills. | [docs](https://docs.hydromancer.xyz/readme/websocket/trades-data/liquidationfills) |
| `trades` | Live trade stream; the all-coin version needs extra permission on the key. | [docs](https://docs.hydromancer.xyz/readme/websocket/trades-data/trades) |

### Prices data and asset context

Stream live oracle, mark and mid prices and asset contexts.

| type | What it returns | Docs |
|---|---|---|
| `activeAssetCtx` | Live stream of oracle, mid and mark prices for an asset. | [docs](https://docs.hydromancer.xyz/readme/websocket/prices-data-and-asset-context/activeassetctx) |
| `allActiveAssetCtx` | Stream all asset contexts in a single batch message. Needs extra permission on the key. | [docs](https://docs.hydromancer.xyz/readme/websocket/prices-data-and-asset-context/allactiveassetctx) |
| `allMids` | Stream mid prices for every market, updated every block. Needs extra permission on the key. | [docs](https://docs.hydromancer.xyz/readme/websocket/prices-data-and-asset-context/allmids) |
| `perpPrices` | Stream the accepted oracle and mark prices of perps, one message per block. | [docs](https://docs.hydromancer.xyz/readme/websocket/prices-data-and-asset-context/perpprices) |
| `setOracleUpdates` | Live stream of oracle, mark and external perp prices for a DEX, including failed updates | [docs](https://docs.hydromancer.xyz/readme/websocket/prices-data-and-asset-context/setoracleupdates) |

### Leverage and margin updates

Stream leverage changes and isolated margin updates for specific users or all users.

| type | What it returns | Docs |
|---|---|---|
| `userLeverageUpdates` | Stream live leverage updates for specific users. | [docs](https://docs.hydromancer.xyz/readme/websocket/leverage-and-margin-updates/userleverageupdates) |
| `allLeverageUpdates` | Stream all leverage updates (cross/isolated leverage changes and isolated margin updates). | [docs](https://docs.hydromancer.xyz/readme/websocket/leverage-and-margin-updates/allleverageupdates) |
| `userIsolatedMarginUpdates` | Stream live isolated margin updates for specific users. | [docs](https://docs.hydromancer.xyz/readme/websocket/leverage-and-margin-updates/userisolatedmarginupdates) |
| `allIsolatedMarginUpdates` | Stream all isolated margin updates. | [docs](https://docs.hydromancer.xyz/readme/websocket/leverage-and-margin-updates/allisolatedmarginupdates) |

### User data

Stream live fills, order updates, TWAP statuses and ledger events for many users.

| type | What it returns | Docs |
|---|---|---|
| `userFills` | Stream live fills of many users from a single connection. | [docs](https://docs.hydromancer.xyz/readme/websocket/user-data/userfills) |
| `userOrderUpdates` | Stream live order updates of many users from a single connection. | [docs](https://docs.hydromancer.xyz/readme/websocket/user-data/userorderupdates) |
| `userTwapStatusUpdates` | Stream twap status updates for specific user addresses. | [docs](https://docs.hydromancer.xyz/readme/websocket/user-data/usertwapstatusupdates) |
| `userNonFundingLedgerEvents` | Stream specific users' non funding ledger events | [docs](https://docs.hydromancer.xyz/readme/websocket/user-data/usernonfundingledgerevents) |

### TWAP data

Stream all TWAP status updates.

| type | What it returns | Docs |
|---|---|---|
| `allTwapStatusUpdates` | Stream all twap status updates. | [docs](https://docs.hydromancer.xyz/readme/websocket/twap-data/alltwapstatusupdates) |

### Funding and deposits data

Stream all users' non-funding ledger events and hourly funding rates.

| type | What it returns | Docs |
|---|---|---|
| `allUserNonFundingLedgerEvents` | Stream all user non funding ledger events. | [docs](https://docs.hydromancer.xyz/readme/websocket/funding-and-deposits-data/allusernonfundingledgerevents) |
| `fundingRates` | Stream per-coin funding rates. Broadcasts once per hour when funding is applied. | [docs](https://docs.hydromancer.xyz/readme/websocket/funding-and-deposits-data/fundingrates) |
