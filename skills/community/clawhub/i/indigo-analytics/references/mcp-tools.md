# Analytics MCP Tools Reference

Detailed reference for all protocol analytics MCP tools.

## get_tvl

Get the total value locked (TVL) in Indigo Protocol across all pools and CDPs.

**Parameters:** None

**Returns:** TVL data object:
- `tvl` — Total value locked in USD
- `tvlAda` — Total value locked in ADA
- `source` — Data source (e.g., DefiLlama)

---

## get_protocol_stats

Get protocol-wide statistics and metrics.

**Parameters:** None

**Returns:** Protocol statistics object:
- `totalCdps` — Number of active CDPs
- `totalMintedAssets` — Number of iAsset types with active CDPs
- `cdpCollateralTotal` — Total ADA locked in CDPs
- `stabilityPoolTotal` — Total iAssets in stability pools
- `stakingTotal` — Total INDY staked
- `poolUtilization` — Overall pool utilization percentage

---

## get_apr_rewards

Get APR reward rates across all Indigo pools.

**Parameters:** None

**Returns:** Array of pool reward objects:
- `pool` — Pool name/identifier
- `asset` — iAsset or token type
- `apr` — Annual percentage rate
- `tvl` — Total value locked in this pool

---

## get_apr_by_key

Get APR reward rate for a specific pool.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | `string` | Yes | Pool key identifier (e.g., "iUSD-stability") |

**Returns:** Single pool reward object with APR, TVL, and reward breakdown.

---

## get_dex_yields

Get current DEX yield data for Indigo iAsset trading pairs.

**Parameters:** None

**Returns:** Array of yield objects:
- `pair` — Trading pair (e.g., "iUSD/ADA")
- `dex` — DEX name (e.g., "Minswap")
- `apy` — Annual percentage yield
- `tvl` — Liquidity in USD
- `volume24h` — 24-hour trading volume
