# REST API

```
POST https://api.hydromancer.xyz/info          (testnet: https://api-testnet.hydromancer.xyz/info)
Authorization: Bearer $HYDROMANCER_API_KEY
Content-Type: application/json
User-Agent: <your app>                          (required in practice: the default Python-urllib agent gets HTTP 403 / 1010)

{"type": "<endpoint>", ...fields}
```

Every endpoint uses the same URL; the `type` field selects it. Field names, defaults and limits differ per endpoint, so open the endpoint's docs page (append `.md` for Markdown) before coding against it. Errors come back as JSON: `400 {"error": "Invalid Ethereum address: …"}`, `401 {"error": "Invalid API key"}`, `429` (see [rate-limits.md](rate-limits.md)), `502 {"error": "Timeout error"}`.

## Examples (tested)

```bash
curl -sS --fail-with-body https://api.hydromancer.xyz/info \
  -H "Authorization: Bearer $HYDROMANCER_API_KEY" -H "Content-Type: application/json" \
  -d '{"type": "liquidationHistoryByTime", "coin": "BTC", "startTime": 1793220000000, "limit": 100}'
# startTime is Unix milliseconds; use a recent value.
```

```python
import os, requests
r = requests.post("https://api.hydromancer.xyz/info",
                  headers={"Authorization": f"Bearer {os.environ['HYDROMANCER_API_KEY']}"},
                  json={"type": "batchClearinghouseStates", "users": ["0xdfc24b077bc1425ad1dea75bcb6f8158e10df303"]},
                  timeout=60)
r.raise_for_status()
data = r.json()   # {"successful_states": ..., "failed_wallets": ...}
```

Field notes for common endpoints:
- `clearinghouseState`: `user`. Returns `marginSummary`, `crossMarginSummary`, `withdrawable`, `assetPositions`, `time`.
- `batchClearinghouseStates`: `users` (up to 1,000; 100 with `"dex": "ALL_DEXES"`), optional `dex`. Weight 2 per user, capped at 100 points; with `ALL_DEXES` the cost is multiplied by the number of DEXs.
- `userFillsByTime`: `user`, `startTime` or `cursor`, optional `endTime`, `builder`, `dex`, `venue`, `aggregateByTime`, `limit` (default 2000; larger values are capped at 2000). Returns a list, oldest first; each fill has `time` and `txIndex`, so the next cursor is `f"{time}_{txIndex}"` from the last record.
- `liquidationHistoryByTime`: optional `coin` (omit for market-wide; HIP-3 as `"xyz:JPY"`), `startTime`, `endTime`, `limit` (default 500, max 1000). Returns a list of fills.
- `outcomeMeta`: optional `venue`, `deployedBy` (`"all"`, `"validator"` or `"venue"`). HIP-4 outcomes with `sideSpecs`.
- `perpSnapshots`: `market_names`, e.g. `["BTC"]`, `["xyz:BTC"]` or `["ALL:ALL_DEXES"]`. Binary response (zstd-compressed MessagePack; `scripts/hydromancer.py` doesn't decode it); call `perpSnapshotTimestamp` (weight 1) first to see whether a new snapshot exists.

## Endpoint catalog

Generated from https://docs.hydromancer.xyz/llms.txt. Descriptions follow the docs, lightly edited.

### User position data

Endpoints for querying perp and spot account summaries, asset data and leverage settings for one or many users.

| type | What it returns | Docs |
|---|---|---|
| `clearinghouseState` | Get the complete clearinghouse state for a single user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/clearinghousestate) |
| `batchClearinghouseStates` | Get clearinghouse states for multiple users in a single request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/batchclearinghousestates) |
| `portfolioState` | Get clearinghouse state, spot clearinghouse state, and account abstraction mode for a single user in one request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/portfoliostate) |
| `batchPortfolioStates` | Get clearinghouse states for perp and spot of multiple users in a single request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/batchportfoliostates) |
| `activeAssetData` | Get asset data for a specific user and coin. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/activeassetdata) |
| `spotClearinghouseState` | Get the spot clearinghouse state for a single user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/spotclearinghousestate) |
| `userAbstraction` | Get the account abstraction mode for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/userabstraction) |
| `userDexAbstraction` | Check whether a Hyperliquid wallet has per-DEX abstraction enabled, in one API request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/userdexabstraction) |
| `webData2` | Get aggregated web data including clearinghouse state, metadata, and market info. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/webdata2) |
| `webData3` | Get a lightweight account summary for a user: agent wallet, account mode, cumulative ledger and per-DEX vault equity. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-position-data/webdata3) |

### Asset data

Endpoints for querying mid, mark and oracle prices, live and historical.

| type | What it returns | Docs |
|---|---|---|
| `assetContext` | Get the asset context (mid-, mark- and oracle price for example) of one or more symbols. | [docs](https://docs.hydromancer.xyz/readme/rest-api/asset-data/assetcontext) |
| `oraclePriceHistory` | Returns the most recent oracle price updates for a coin in descending order (newest first). | [docs](https://docs.hydromancer.xyz/readme/rest-api/asset-data/oraclepricehistory) |
| `oraclePriceHistoryByTime` | Returns oracle price updates for a coin within a time range in ascending order (oldest first). | [docs](https://docs.hydromancer.xyz/readme/rest-api/asset-data/oraclepricehistorybytime) |
| `perpPriceHistoryByTime` | Returns the accepted oracle and mark prices of a perp within a time range | [docs](https://docs.hydromancer.xyz/readme/rest-api/asset-data/perppricehistorybytime) |
| `allMids` | Get the mid prices of all perp assets | [docs](https://docs.hydromancer.xyz/readme/rest-api/asset-data/allmids) |

### User order data

Endpoints for querying a user's open orders, with or without frontend details.

| type | What it returns | Docs |
|---|---|---|
| `openOrders` | Get the open orders for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-order-data/openorders) |
| `frontendOpenOrders` | Get a user's open orders with frontend details such as order type and trigger conditions. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-order-data/frontendopenorders) |

### Historical data

Endpoints for querying historical fills, orders, funding, ledger updates and leverage changes for users and builders.

| type | What it returns | Docs |
|---|---|---|
| `userFills` | Get the 2000 latest fills of a certain user. Includes twap fills. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/userfills) |
| `userFillsByTime` | Get trading fills for a single user within a time range. Includes twap fills. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/userfillsbytime) |
| `fillsByTime` | Market-wide fills of the last 24 hours, by time, optionally filtered by coin. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/fillsbytime) |
| `tradesByTime` | Market trades of the last 24 hours, in the WebSocket trades shape, by time, optionally filtered by coin. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/tradesbytime) |
| `userTwapSliceFills` | Get the 2000 most recent TWAP slice fills for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/usertwapslicefills) |
| `userTwapSummaries` | Get aggregated TWAP order summaries for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/usertwapsummaries) |
| `userTwapStatusesByTime` | Paginate a user's TWAP order status events by time, oldest-first. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/usertwapstatusesbytime) |
| `builderFills` | Get the 2000 latest fills submitted by a builder. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderfills) |
| `builderFillsByTime` | Get fills submitted by a builder in a certain time range | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderfillsbytime) |
| `builderApprovedFillsByTime` | Fills that occurred while a user had an active builder-fee approval for your builder address. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderapprovedfillsbytime) |
| `builderApprovedFundingByTime` | Hourly funding payments made by users who had an active builder-fee approval for your builder address. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderapprovedfundingbytime) |
| `builderApprovedNonFundingLedgerUpdatesByTime` | Deposits, withdrawals, transfers and other non-funding ledger updates made by users who had an active builder-fee approval for your builder address. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderapprovednonfundingledgerupdatesbytime) |
| `userFunding` | Get a users' funding payment history | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/userfunding) |
| `fundingHistory` | Get the funding history for a coin | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/fundinghistory) |
| `liquidationHistoryByTime` | Get historical liquidation events for a coin or market-wide | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/liquidationhistorybytime) |
| `userNonFundingLedgerUpdates` | Get a users' non funding ledger updates | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/usernonfundingledgerupdates) |
| `historicalOrders` | Get the 2000 latest order status updates of a certain user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/historicalorders) |
| `orderStatusByOid` | Get the latest status snapshot of a single order by oid or cloid. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/orderstatusbyoid) |
| `builderOrdersByTime` | Returns a builder's sent order status updates within a specified timerange. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/builderordersbytime) |
| `userLeverageUpdatesByTime` | Paginate a user's leverage change history by time, oldest-first. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/userleverageupdatesbytime) |
| `userIsolatedMarginUpdatesByTime` | Paginate a user's isolated margin update history by time, oldest-first. | [docs](https://docs.hydromancer.xyz/readme/rest-api/historical-data/userisolatedmarginupdatesbytime) |

### User performance

Endpoints for analyzing a user's trading performance — realized PnL from closed positions, win/loss stats, fees, funding, ranked leaderboards, and (coming soon) unrealized PnL, ROI, and other metrics.

| type | What it returns | Docs |
|---|---|---|
| `userPnlSummary` | Aggregate realized-PnL stats for a single user, computed from completed trades. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-performance/userpnlsummary) |
| `userPnlLeaderboard` | Top traders ranked by realized PnL, win rate, or volume, with quality filters. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-performance/userpnlleaderboard) |
| `userCompletedTrades` | Get a user's most recent completed (fully closed) positions, newest-first. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-performance/usercompletedtrades) |
| `userCompletedTradesByTime` | Paginate a user's completed (fully closed) positions by close time, oldest-first. | [docs](https://docs.hydromancer.xyz/readme/rest-api/user-performance/usercompletedtradesbytime) |

### Outcomes

Endpoints for querying prediction market outcomes.

| type | What it returns | Docs |
|---|---|---|
| `outcomeMeta` | Get metadata for all registered prediction market outcomes. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcomemeta) |
| `settledOutcome` | Get the settlement spec and result for a single prediction market outcome. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/settledoutcome) |
| `settledOutcomesById` | Get settled prediction market outcomes by their outcome IDs or asset IDs. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/settledoutcomesbyid) |
| `settledOutcomes` | Get recent settled prediction market outcomes. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/settledoutcomes) |
| `registeredOutcomesById` | Get registered prediction market outcomes by their outcome IDs or asset IDs. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/registeredoutcomesbyid) |
| `registeredOutcomes` | Get recent registered prediction market outcomes. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/registeredoutcomes) |
| `registeredOutcomesSnapshot` | Per-side balance snapshots of every active prediction market outcome (zstd+msgpack). | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/registeredoutcomessnapshot) |
| `outcomeTemplatesOverview` | List all registered permissionless HIP-4 outcome templates. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcometemplatesoverview) |
| `outcomeTemplates` | Returns the live list of registered outcome templates. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcometemplates) |
| `outcomeDeployerLimits` | Returns a venue's remaining outcome-deployment allowance: how many more outcomes it may deploy today, and how many more it may hold active at once. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcomedeployerlimits) |
| `outcomeVenuesOverview` | List permissionless HIP-4 venues, their lifecycle, and sub-deployer permissions. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcomevenuesoverview) |
| `outcomeVenueStats` | Market counts, lifetime and 24-hour trading stats, and open interest per HIP-4 venue, plus validator-deployed markets. | [docs](https://docs.hydromancer.xyz/readme/rest-api/outcomes/outcomevenuestats) |

### Vaults

Endpoints for querying vault summaries, user vault equities and the vaults a user leads.

| type | What it returns | Docs |
|---|---|---|
| `vaultSummaries` | Returns summary information for vaults. Usually `[]` on both Hydromancer and Hyperliquid (it appears to list only very new vaults); for a wallet's vaults use `leadingVaults` or `userVaultEquities`. | [docs](https://docs.hydromancer.xyz/readme/rest-api/vaults/vaultsummaries) |
| `userVaultEquities` | Returns vault equity information for a specific user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/vaults/uservaultequities) |
| `leadingVaults` | Returns vaults that a user is leading. | [docs](https://docs.hydromancer.xyz/readme/rest-api/vaults/leadingvaults) |

### Roles and agents

Endpoints for querying a wallet's role, its API key names and the multisigs it signs for.

| type | What it returns | Docs |
|---|---|---|
| `userRole` | Get the role of a user account. | [docs](https://docs.hydromancer.xyz/readme/rest-api/roles-and-agents/userrole) |
| `extraAgents` | Get the extra agents (API wallets) for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/roles-and-agents/extraagents) |
| `multiSigsBySigner` | Get multisig accounts associated with an address. | [docs](https://docs.hydromancer.xyz/readme/rest-api/roles-and-agents/multisigsbysigner) |
| `approvedBuilders` | Returns the list of builder addresses a user has approved to charge builder fees. | [docs](https://docs.hydromancer.xyz/readme/rest-api/roles-and-agents/approvedbuilders) |

### Metadata

Retrieve metadata about perpetual and spot markets, margin requirements, exchange status, available DEXes, and perp asset annotations and limits.

| type | What it returns | Docs |
|---|---|---|
| `meta` | Returns metadata for perpetual markets including asset names, size decimals, and max leverage. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/meta) |
| `metaAndAssetCtxs` | Returns perpetual market metadata together with the per-asset trading context (prices, open interest, and 24h volume) in a single request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/metaandassetctxs) |
| `spotMeta` | Returns metadata for spot markets including token names, size decimals, and trading pair information. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/spotmeta) |
| `marginTable` | Returns the margin requirements table for a specific perpetual asset by index. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/margintable) |
| `perpDexs` | Returns the list of all available perpetual DEXes. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpdexs) |
| `allPerpMetas` | Returns the perpetuals metadata — universe definitions and margin tables — for every perp DEX in a single response. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/allperpmetas) |
| `perpAnnotation` | Returns the human-readable annotation (category, description, and keywords) for a single perpetual asset. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpannotation) |
| `batchPerpAnnotations` | Get human-readable annotations for multiple perpetual assets in a single request. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/batchperpannotations) |
| `perpCategories` | Returns the category for every annotated perpetual asset as a list of [coin, category] pairs. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpcategories) |
| `perpConciseAnnotations` | Returns concise annotations for every annotated perpetual asset as a list of [coin, annotation] pairs. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpconciseannotations) |
| `perpDexStatus` | Returns the status of a builder-deployed (HIP-3) perp DEX, including its total net deposits. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpdexstatus) |
| `perpDexLimits` | Returns the open-interest and transfer limits for a builder-deployed (HIP-3) perp DEX, including the per-asset open-interest caps. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/perpdexlimits) |
| `exchangeStatus` | Returns the current status of the exchange. | [docs](https://docs.hydromancer.xyz/readme/rest-api/metadata/exchangestatus) |

### Token deployment

Endpoints for querying spot deploy state and perp deploy auction status.

| type | What it returns | Docs |
|---|---|---|
| `spotDeployState` | Get the spot deploy state for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/token-deployment/spotdeploystate) |
| `perpDeployAuctionStatus` | Get the current perp deploy auction status. | [docs](https://docs.hydromancer.xyz/readme/rest-api/token-deployment/perpdeployauctionstatus) |
| `spotPairDeployAuctionStatus` | Returns the current status of the spot trading-pair deploy auction, including timing and gas pricing. | [docs](https://docs.hydromancer.xyz/readme/rest-api/token-deployment/spotpairdeployauctionstatus) |

### Borrow / Lend

Retrieve borrow/lend reserve state and per-user borrow/lend positions.

| type | What it returns | Docs |
|---|---|---|
| `allBorrowLendReserveStates` | Get the borrow/lend reserve state of every token. | [docs](https://docs.hydromancer.xyz/readme/rest-api/borrow-lend/allborrowlendreservestates) |
| `borrowLendReserveState` | Returns the borrow/lend reserve state for a single token by its token index. | [docs](https://docs.hydromancer.xyz/readme/rest-api/borrow-lend/borrowlendreservestate) |
| `borrowLendUserState` | Returns a user's borrow/lend positions and account health. | [docs](https://docs.hydromancer.xyz/readme/rest-api/borrow-lend/borrowlenduserstate) |

### Staking

Endpoints for querying validators, stakers, staking events and per-user staking balances.

| type | What it returns | Docs |
|---|---|---|
| `stakingOverview` | Get a summary of all validators and their staking stats. | [docs](https://docs.hydromancer.xyz/readme/rest-api/staking/stakingoverview) |
| `stakingValidatorStakers` | Get the full staker list for a specific validator. | [docs](https://docs.hydromancer.xyz/readme/rest-api/staking/stakingvalidatorstakers) |
| `validatorAprHistory` | Query a validator's weekly net staking APR and rewards distributed to delegators. | [docs](https://docs.hydromancer.xyz/readme/rest-api/staking/validatoraprhistory) |
| `stakingEvents` | Query historical staking events (delegate, undelegate, withdrawal). | [docs](https://docs.hydromancer.xyz/readme/rest-api/staking/stakingevents) |
| `globalStakingSummary` | Get per-user staking balances across all of Hyperliquid — delegated, pending unstake, and available staking balance. | [docs](https://docs.hydromancer.xyz/readme/rest-api/staking/globalstakingsummary) |

### Delegations

Endpoints for querying a user's staking delegations, summary and history, plus validator L1 votes.

| type | What it returns | Docs |
|---|---|---|
| `delegations` | Get delegation information for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/delegations) |
| `delegatorSummary` | Get a summary of a user's delegation status. | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/delegatorsummary) |
| `delegatorHistory` | Query a user's staking history (delegations, deposits, withdrawals). | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/delegatorhistory) |
| `delegatorRewards` | Query a user's daily HYPE staking rewards (delegation + commission). | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/delegatorrewards) |
| `maxBuilderFee` | Get the maximum builder fee a user has approved for a specific builder. | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/maxbuilderfee) |
| `validatorL1Votes` | Get the current validator L1 votes. | [docs](https://docs.hydromancer.xyz/readme/rest-api/delegations/validatorl1votes) |

### Fees

Endpoints for querying a user's trading fees.

| type | What it returns | Docs |
|---|---|---|
| `userFees` | Get fee information for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/fees/userfees) |

### API Usage

Endpoints for checking your Hydromancer API usage.

| type | What it returns | Docs |
|---|---|---|
| `apiUsage` | Get your Hydromancer API usage statistics broken down by day and request type. | [docs](https://docs.hydromancer.xyz/readme/rest-api/api-usage/apiusage) |

### Subaccounts

Endpoints for querying a user's subaccounts.

| type | What it returns | Docs |
|---|---|---|
| `subAccounts` | Get subaccount information for a user. | [docs](https://docs.hydromancer.xyz/readme/rest-api/subaccounts/subaccounts) |

### Candlesticks

| type | What it returns | Docs |
|---|---|---|
| `candleSnapshot` | Get OHLCV candlestick data for any coin and interval. | [docs](https://docs.hydromancer.xyz/readme/rest-api/candlesticks/candlesnapshot) |

### Market data

Endpoints for market-wide data: open interest history, position and TWAP snapshots, L4 orderbooks, liquidity, slippage and funding payments.

| type | What it returns | Docs |
|---|---|---|
| `openInterestHistory` | Historical OHLC of open interest, per coin or per sector, in contracts and USD. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/openinteresthistory) |
| `perpSnapshots` | Market-wide snapshot of every trader's perp positions (binary; see SKILL.md). | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/perpsnapshot) |
| `perpTwapSnapshots` | Endpoint to get all active TWAP orders across all Hyperliquid perpetual markets. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/perptwapsnapshot) |
| `accountValueSnapshots` | Snapshot of every account's value, with optional filtering by a specific type of collateral or HIP-3 DEX. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/accountvaluesnapshot) |
| `spotSnapshots` | Market-wide snapshot of every holder's spot balances (binary; see SKILL.md). | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/spotsnapshot) |
| `spotTwapSnapshots` | Endpoint to get all active TWAP orders across all Hyperliquid spot markets. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/spottwapsnapshot) |
| `l4Book` | Get L4 orderbook snapshot for perpetual markets. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/l4book) |
| `l2Book` | Get L2 orderbook snapshot with aggregated price levels. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/l2book) |
| `l2BookDiffSnapshot` | Get L2 orderbook snapshot for bootstrapping the l2BookDiff WebSocket stream. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/l2bookdiffsnapshot) |
| `tpslBook` | Get a snapshot of all active TP/SL trigger orders. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/tpslbook) |
| `marketLiquidity` | Get aggregated orderbook depth for a specific market | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/marketliquidity) |
| `marketLiquidityHistory` | Get hourly-averaged orderbook depth history for a specific market. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/marketliquidityhistory) |
| `slippageHistory` | Get historical slippage estimates for a specific market and notional size. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/slippagehistory) |
| `currentDepth` | Get current cumulative orderbook depth at multiple BPS levels for all markets. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/currentdepth) |
| `fundingPayments` | Get all funding payments for the most recent hour across all markets and users as a compressed snapshot. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/fundingpayments) |
| `maxMarketOrderNtls` | Get the maximum market order notional sizes by leverage tier. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/maxmarketorderntls) |
| `perpsAtOpenInterestCap` | Get the list of perp assets currently at their open interest cap. | [docs](https://docs.hydromancer.xyz/readme/rest-api/market-data/perpsatopeninterestcap) |
