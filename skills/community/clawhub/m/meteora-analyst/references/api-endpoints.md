# Meteora API Endpoints — Complete Reference (Verified)

All endpoints have been verified and return real-time data.

## 1. DLMM API

**Base URL:** `https://dlmm.datapi.meteora.ag`
**Rate Limit:** 30 RPS

### Pools

#### GET /pools
Paginated list of all DLMM pools.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page (default: 10) |
| `page` | integer | Page number |
| `search_term` | string | Filter by token name or mint address |
| `sort_key` | string | Field to sort by |
| `order_by` | string | Sort direction: `asc` or `desc` |

**Response:**
```json
{
  "total": 102346,
  "pages": 10235,
  "current_page": 1,
  "page_size": 10,
  "data": [...]
}
```

**Pool fields in `data`:**
| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Pool address |
| `name` | string | Pair name (e.g. "SOL-USDC") |
| `token_x` | object | Token X info (address, name, symbol, decimals, is_verified, holders, price, market_cap, total_supply, freeze_authority_disabled) |
| `token_y` | object | Token Y info (same structure) |
| `token_x_amount` | number | Token X amount in the pool |
| `token_y_amount` | number | Token Y amount in the pool |
| `reserve_x` | string | Reserve X address |
| `reserve_y` | string | Reserve Y address |
| `created_at` | number | Creation timestamp (ms) |
| `pool_config.bin_step` | integer | Pool bin step |
| `pool_config.base_fee_pct` | number | Base fee (%) |
| `pool_config.max_fee_pct` | number | Max fee (%) |
| `pool_config.protocol_fee_pct` | number | Protocol fee (%) |
| `dynamic_fee_pct` | number | Current dynamic fee (%) |
| `tvl` | number | Total Value Locked (USD) |
| `current_price` | number | Current price |
| `apr` | number | Estimated APR |
| `apy` | number | Estimated APY |
| `has_farm` | boolean | Whether pool has a farm |
| `farm_apr` | number | Farm APR |
| `farm_apy` | number | Farm APY |
| `volume` | object | Volume by time window: `30m`, `1h`, `2h`, `4h`, `12h`, `24h` |
| `fees` | object | Fees by time window: `30m`, `1h`, `2h`, `4h`, `12h`, `24h` |
| `protocol_fees` | object | Protocol fees by time window |
| `fee_tvl_ratio` | object | Fees/TVL ratio by time window |
| `cumulative_metrics.volume` | number | Cumulative historical volume |
| `cumulative_metrics.trade_fee` | number | Cumulative historical fees |
| `is_blacklisted` | boolean | Whether pool is blacklisted |
| `launchpad` | string | Associated launchpad |
| `tags` | array | Pool tags |

#### GET /pools/groups
Paginated list of pool groups (same token pair with different bin steps grouped together).

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Number of results |
| `page` | integer | Page number |

**Group fields:**
| Field | Description |
|-------|-------------|
| `lexical_order_mints` | Mints concatenated in lexicographic order |
| `group_name` | Pair name (e.g. "SOL-USDC") |
| `token_x` | Token X mint address |
| `token_y` | Token Y mint address |
| `pool_count` | Number of pools in the group |
| `total_tvl` | Total TVL of the group |
| `total_volume` | Total volume of the group |
| `max_fee_tvl_ratio` | Best fees/TVL ratio |
| `has_farm` | Whether any pool has a farm |

#### GET /pools/groups/{lexical_order_mints}
Pools belonging to a specific group.

#### GET /pools/{address}
Single pool detail by address.

#### GET /pools/{address}/ohlcv
OHLCV candle data for a pool over a time range.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `start_time` | integer | Unix start timestamp |
| `end_time` | integer | Unix end timestamp |

#### GET /pools/{address}/volume/history
Historical volume for a pool aggregated into time buckets.

### Stats

#### GET /stats/protocol_metrics
Global DLMM protocol metrics.

**Verified response:**
```json
{
  "total_tvl": 266010597.54,
  "volume_24h": 68555558.40,
  "fee_24h": 273190.33,
  "total_volume": 286006645281.82,
  "total_fees": 1357981093.07,
  "total_pools": 140034
}
```

---

## 2. DAMM v1 API

**Base URL:** `https://amm-v2.meteora.ag`
**Swagger:** `https://amm-v2.meteora.ag/swagger-ui/`

### GET /pools?address={pool_address}
Returns DAMM v1 pool information by address. **Requires `address` parameter.**

**Response fields:**
| Field | Description |
|-------|-------------|
| `pool_address` | Pool address |
| `pool_token_mints` | Mints for both tokens |
| `pool_token_amounts` | Amounts for both tokens |
| `pool_token_usd_amounts` | USD amounts |
| `lp_mint` | LP token mint |
| `pool_tvl` | Pool TVL |
| `farm_tvl` | Farm TVL |
| `farming_pool` | Farming pool address |
| `farming_apy` | Farm APY |

---

## 3. DAMM v2 API

**Base URL:** `https://damm-v2.datapi.meteora.ag`
**Rate Limit:** 10 RPS

### GET /pools
Paginated list of DAMM v2 pools. Supports advanced filters.

**Search parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `pool_address` | string | Search by address (contains) |
| `token_a_symbol` | string | Search by token A symbol (contains) |
| `token_b_symbol` | string | Search by token B symbol (contains) |
| `pool_name` | string | Search by name (contains) |
| `creator` | string | Search by creator address (contains) |
| `token_a_mint` | string | Search by token A mint (contains) |
| `token_b_mint` | string | Search by token B mint (contains) |
| `launchpad` | string | Search by launchpad (contains) |
| `farm_state` | string | Search by farm state |

**Control parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `case_sensitive` | boolean | Case-sensitive search (default: false) |
| `or_condition` | boolean | OR instead of AND for filters (default: false) |
| `verified_only` | boolean | Only pools with verified tokens |
| `order_by` | string | Sort field (default: tvl) |
| `order_dir` | string | Sort direction |
| `limit` | integer | Result limit |

**Response:**
```json
{
  "total": 56677,
  "pages": 5668,
  "current_page": 1,
  "page_size": 10,
  "data": [...]
}
```

**Pool fields in `data`:**
| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Pool address |
| `name` | string | Pool name |
| `token_x` | object | Full token X info (address, name, symbol, decimals, is_verified, holders, price, market_cap, total_supply, freeze_authority_disabled) |
| `token_y` | object | Full token Y info |
| `token_x_amount` | number | Token X amount |
| `token_y_amount` | number | Token Y amount |
| `created_at` | number | Creation timestamp (ms) |
| `pool_config` | object | Configuration: collect_fee_mode, base_fee_mode, base_fee_pct, protocol_fee_pct, dynamic_fee_initialized, pool_type, concentrated_liquidity, min_price, max_price, activation_type |
| `tvl` | number | Total Value Locked (USD) |
| `current_price` | number | Current price |
| `has_farm` | boolean | Whether pool has a farm |
| `farm_apr` | number | Farm APR |
| `farm_apy` | number | Farm APY |
| `permanent_lock_liquidity` | number | Permanently locked liquidity |
| `volume` | object | Volume by window: `30m`, `1h`, `2h`, `4h`, `12h`, `24h` |
| `fees` | object | Fees by time window |
| `protocol_fees` | object | Protocol fees by time window |

### GET /pools/{address}
Single DAMM v2 pool detail. Includes `pool_name` and `alpha_vault`.

### GET /pool-groups
DAMM v2 pool groups.

### GET /ohlcv
OHLCV data for DAMM v2 pools.

### GET /volume
DAMM v2 historical volume.

### GET /stats/protocol_metrics
Global DAMM v2 protocol metrics.

**Verified response:**
```json
{
  "total_tvl": 57757600.03,
  "volume_24h": 20497520.17,
  "fee_24h": 6280444.92,
  "total_volume": 8226206961.71,
  "total_fees": 113059862.77,
  "total_pools": 884568
}
```

---

## Important Notes

1. **All APIs are public and require no authentication.**
2. **APIs return raw JSON** — do not use `webFetch`, use native `fetch` or `curl`.
3. **Prices and USD amounts** are calculated server-side.
4. **DLMM groups pools by token pair** — the same pair can have multiple pools with different `bin_step` values.
5. **DAMM v2 has the most advanced filters** — search by symbol, mint, creator, launchpad.
6. **DAMM v1 requires an address** — does not support unfiltered listing.
7. **For cross-AMM comparisons**, query DLMM and DAMM v2 in parallel and normalize fields.
8. **Both APIs (DLMM and DAMM v2) use the same response structure** with `token_x`/`token_y` objects and time windows for volume/fees.
