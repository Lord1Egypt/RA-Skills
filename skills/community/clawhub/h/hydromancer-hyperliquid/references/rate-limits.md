# Rate limits and weights

## REST budget

Each key has a per-minute weight budget (currently 5,000 to 50,000, depending on the key; the `X-RateLimit-Limit` response header shows yours). Most requests cost **2**. Heavier ones, for example:

| Weight | Endpoints |
|---|---|
| 5 | `builderFills`, `builderFillsByTime`, `builderOrdersByTime`, `fundingHistory`, `liquidationHistoryByTime`, `openInterestHistory`, `currentDepth`, `portfolioState`, `apiUsage`, staking history endpoints |
| 10 | `userFills`, `userFillsByTime`, `fillsByTime`, `tradesByTime`, `historicalOrders`, `orderStatusByOid`, `userFunding`, `userNonFundingLedgerUpdates`, `marketLiquidity`, `slippageHistory`, `perpPriceHistoryByTime`, `allPerpMetas` |
| 20 | `userPnlSummary`, `userCompletedTrades(ByTime)`, `metaAndAssetCtxs`, `candleSnapshot`, `registeredOutcomes(ById)`, `settledOutcomes(ById)`, `outcomeVenueStats`, leverage / isolated-margin / TWAP history |
| 100 | `builderApprovedFillsByTime`, `builderApprovedFundingByTime`, `builderApprovedNonFundingLedgerUpdatesByTime` |
| 200 | `userPnlLeaderboard` |
| per user | `batchClearinghouseStates` 2 per user (max 100 points; up to 1,000 users, 100 with `ALL_DEXES`), `batchPortfolioStates` 3 per user (max 200 points; up to 500 users, 100 with `ALL_DEXES`), `batchPerpAnnotations` 1 per item (max 25 points). With `ALL_DEXES` the cost is multiplied by the number of DEXs. |

## Windowed endpoints (own limits, outside the budget)

| Endpoint | Limit |
|---|---|
| `perpSnapshots`, `spotSnapshots`, `perpTwapSnapshots`, `spotTwapSnapshots`, `accountValueSnapshots`, `fundingPayments`, `registeredOutcomesSnapshot`, `globalStakingSummary` | 5 requests / 10 min |
| `l4Book` | 20 / 5 min |
| `tpslBook` | 10 / 5 min |
| `l2Book` | 60 / 5 min |
| `l2BookDiffSnapshot` | 300 / 5 min |

The `*SnapshotTimestamp` endpoints cost 1 and tell you whether a new snapshot is out before you spend a windowed request.

## Handling 429

Admitted responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` and `X-RateLimit-Cost`. A 429 adds `Retry-After` and a JSON body with `retryAfterSecs`, `remaining`, `required` and `correlationId`. Wait for `Retry-After` (or `retryAfterSecs`) plus a little jitter; otherwise back off exponentially, capped around 30 seconds, with a limit on attempts. `scripts/hydromancer.py` does this.

Weights are separate from token usage. Current table: https://docs.hydromancer.xyz/readme/rest-api/rate-limits-and-user-limits
