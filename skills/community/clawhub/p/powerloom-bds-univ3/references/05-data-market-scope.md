# Data market scope (ETH mainnet Uniswap V3)

## Canonical worked example (single pool)

| Pool | Address | Fee tier |
|------|---------|----------|
| WETH/USDC | `0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640` | 0.05% |

Some fee tiers (e.g. 0.3% WETH/USDC) may **not** be indexed in this data market — check `bds_mpp_pool_pool_address_metadata` / `bds_mpp_dailyActivePools` before assuming coverage.

## Multi-pool / token-first

- **All pools / all trades (bounded):** `bds_mpp_snapshot_allTrades` (skill + cron). Streaming variants may exist on MCP for direct use outside the skill.
- **Token-scoped:** `bds_mpp_token_token_address_pools`, `bds_mpp_tradeVolumeAllPools_token_address_time_interval`.
- **Single pool:** `bds_mpp_snapshot_trades_pool_address` — use only when the user explicitly wants one pool.
