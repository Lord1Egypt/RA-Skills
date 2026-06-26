# Prompt patterns → tools

| User intent | Primary path |
|-------------|--------------|
| “All USDC swaps”, “every trade for token X” | **Token-Flow** (`token-flow.yaml`) — per-pool snapshots; or `bds_mpp_snapshot_allTrades` via **`whale-cron.mjs`** for all pools in one batch. |
| “Whale”, “above $X” | **`whale-cron.mjs`** (all pools, bounded) or **`whale-radar.mjs`** (fixed pool list). |
| “One pool” | `bds_mpp_snapshot_trades_pool_address` after resolving the pool. |
| “Is this CID real?” | `verify_data_provenance` with `cid`, `epoch_id`, `project_id`. |

The skill does **not** ship streaming trade consumption; use snapshot tools only.
