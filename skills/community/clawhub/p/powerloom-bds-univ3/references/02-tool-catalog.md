# BDS MCP tool catalog (representative)

All calls are metered unless noted. **Defaults:** `POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS=60000` (raise for large `bds_mpp_snapshot_allTrades` responses under backlog, e.g. `120000`).

**Skill note:** `powerloom-bds-univ3` recipes use **snapshot** tools only (`bds_mpp_snapshot_*`). Streaming catalog tools exist on the hosted MCP server for direct/advanced use but are **not** invoked by shipped scripts.

| Tool | What | Typical latency | Skill usage |
|------|------|-----------------|-------------|
| `bds_mpp_snapshot_allTrades` | One-shot all pools (bounded batch) | 8–45s | `whale-cron.mjs`, DeFi Analyst multi |
| `bds_mpp_snapshot_trades_pool_address` | One pool snapshot | 2–15s | `whale-radar.mjs`, `token-flow.mjs` |
| `bds_mpp_stream_allTrades` | Streaming batches (long-lived upstream) | varies | **Not used by skill** |

See the live server’s `tools/list` for the full catalog.
