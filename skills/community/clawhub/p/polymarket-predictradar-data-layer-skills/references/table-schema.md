# Polymarket Shared Analytics Fields / API Field Reference

## Trade Activity Fields → GET /activity

**Shared Analytics Query Source**: `trades`
**Corresponding API**: `GET https://data-api.polymarket.com/activity?user=<address>`

| Analytics Field | API Field | Type | Description |
|----------------|-----------|------|-------------|
| `wallet_address` | `proxyWallet` | String | User wallet address (lowercase) |
| `condition_id` | `conditionId` | String | Market unique identifier |
| `traded_at` | `timestamp` | DateTime / Unix int | Trade timestamp |
| `amount` | `usdcSize` | Float64 | Trade amount (USDC), needs `toFloat64()` |
| `side` | `side` | String | `buy` / `sell` |
| `outcome_side` | `outcome` | String | Bet direction (Yes/No, etc.) |
| `outcome_index` | `outcomeIndex` | Int | Outcome index |
| `price` | `price` | Float64 | Average fill price (0~1) |
| _(none)_ | `size` | Float64 | Filled token quantity (API only) |
| _(none)_ | `transactionHash` | String | On-chain transaction hash (API only) |
| _(none)_ | `title` | String | Market title (API only, needs Gamma) |
| _(none)_ | `type` | String | TRADE / REDEEM / SPLIT, etc. |

**Capabilities unique to Shared Analytics** (not in API):

| Field | Description |
|-------|-------------|
| Full history | Shared analytics supports complete history, API `offset` max 10000 records |
| Full table aggregation | Can `GROUP BY` across all users, API only per-user |

---

## Position Summary Fields → GET /positions

**Shared Analytics Query Source**: `positions`
**Corresponding API**: `GET https://data-api.polymarket.com/positions?user=<address>`

| Analytics Field | API Field | Type | Description |
|----------------|-----------|------|-------------|
| `wallet_address` | `proxyWallet` | String | User wallet address (lowercase) |
| `condition_id` | `conditionId` | String | Market unique identifier |
| `asset` | `asset` | String | CTF token address |
| `total_bought` | `totalBought` / `initialValue` | Float64 | Cumulative bought amount (USDC) |
| `realized_pnl` | `realizedPnl` / `cashPnl` | Float64 | Realized PnL |
| `unrealized_pnl` | _(needs calculation)_ | Float64 | Unrealized PnL (`currentValue - initialValue`) |
| `is_closed` | _(no direct field)_ | UInt8 | 1=closed (API has no this field, needs inference) |
| _(none)_ | `size` | Float64 | Current held token quantity |
| _(none)_ | `avgPrice` | Float64 | Average bought price |
| _(none)_ | `curPrice` | Float64 | Current market price |
| _(none)_ | `currentValue` | Float64 | Current position market value |
| _(none)_ | `percentPnl` | Float64 | PnL percentage |
| _(none)_ | `title` / `outcome` | String | Market / outcome name |
| _(none)_ | `endDate` | String | Market end date |

**Capabilities unique to Shared Analytics**:

- `is_closed = 1` is used for win rate calculation (in API, needs `redeemable` field for indirect judgment)
- `HAVING sum(total_bought) >= 1000` filters out small test addresses

---

## Gamma API (Market Metadata)

**Base URL**: `https://gamma-api.polymarket.com`

### Common Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /markets?condition_ids=x,y&limit=200` | Batch query by condition_id, max 200/request |
| `GET /markets?limit=500&offset=N&order=volumeNum&ascending=false` | Paginated scan by volume |

### Return Fields

| Field | Type | Description |
|-------|------|-------------|
| `conditionId` | String | Consistent with `condition_id` in shared analytics (sometimes also written as `condition_id`) |
| `question` | String | Market question text (main basis for domain classification) |
| `category` | String | Category (e.g., `crypto`, `politics`) — may be empty for high-volume markets |
| `tags` | Array | Tags, each item contains `id`, `slug`, `label`, can use id for precise domain mapping |
| `volumeNum` | Number | Total market volume (used for sorting during scan) |
| `active` | Boolean | Whether active |
| `closed` | Boolean | Whether closed |

### Tag ID → Domain Code (Precise Mapping)

| Tag ID | Domain | Meaning |
|--------|--------|---------|
| 2 | POL | Politics |
| 100265 | GEO | Geopolitics |
| 120 | FIN | Finance |
| 21 | CRY | Crypto |
| 100639 | SPT | Sports |
| 1401 | TEC | Tech AI |
| 596 | CUL | Entertainment |

Prioritize Tag ID matching, use `question` keyword rules as fallback when ID matching fails (see `Q_RULES` in `tag-all-domains.js`).

---

## Common SQL Quick Reference

```sql
-- User basic metrics for last 30 days
SELECT wallet_address,
       count() / 30.0                  AS daily_30d,
       avg(toFloat64(amount))          AS avg_amount,
       sum(toFloat64(amount))          AS total_volume,
       countDistinct(condition_id)     AS market_count
FROM default.trades
WHERE wallet_address = '0x...'
  AND traded_at >= now() - INTERVAL 30 DAY
GROUP BY wallet_address;

-- User win rate / PnL
SELECT wallet_address,
       sum(toFloat64(realized_pnl))     AS total_realized_pnl,
       countIf(is_closed=1 AND toFloat64(realized_pnl)>0)
         / greatest(countIf(is_closed=1), 1) AS win_rate
FROM default.positions
WHERE wallet_address = '0x...'
GROUP BY wallet_address;

-- Global p60 amount threshold
SELECT quantile(0.6)(amount) AS p60
FROM default.trades
WHERE traded_at IS NOT NULL AND amount > 0;
```
