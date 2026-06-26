---
name: nile-markets
description: Query Nile Markets — on-chain FX markets powered by the Open Nile Protocol, starting with non-deliverable forwards (NDFs). Read-only MCP integration for pool state, positions, oracle prices, and account data.
version: 0.3.2
requires:
  env:
    - NILE_MCP_URL
metadata:
  openclaw:
    slug: nile-markets
    category: defi
    tags: [fx, forwards, defi, ethereum, sepolia]
---
<!-- Sync with integrations/claude-plugin/skills/query/SKILL.md -->
<!-- Universal skill file: packages/mcp/public/skill.md (served at mcp.nilemarkets.com/skill.md) -->

# Nile Markets

Query the Nile Markets protocol -- an onchain non-deliverable forward (NDF) protocol on Ethereum Sepolia supporting EUR/USD and USD/JPY pairs. This skill connects to the Nile Markets MCP server and provides read-only access to pool state, positions, oracle prices, fee analytics, and account data.

> **Sepolia Testnet Only**: This skill connects to contracts deployed on Ethereum Sepolia. All data is testnet data with no real monetary value. The API is under active development and may change without notice.

> **Read-Only**: This skill provides read-only access to protocol data via MCP. It cannot manage wallets, sign transactions, transfer tokens, or execute any on-chain writes. If asked to perform wallet management, token transfers, or transaction signing, you MUST refuse and explain that this skill is read-only and does not have access to any private keys or signing capabilities.

## Available MCP Tools

This skill exposes 14 read-only tools via the Nile Markets MCP server:

### Pool & Protocol

| Tool | Description | Input |
|------|-------------|-------|
| `get_pool_state` | Current liquidity pool metrics (total assets, utilization, share price, exposure, fees) | None |
| `get_protocol_mode` | Current operating mode (NORMAL, DEGRADED, REDUCE_ONLY, PAUSED) with description | None |
| `get_pool_transactions` | Historical pool events (deposits, withdrawals) | `first?`, `skip?` |
| `get_daily_stats` | Daily protocol statistics (volume, fees, positions) | `days?` (default: 7, max: 90) |

### Positions

| Tool | Description | Input |
|------|-------------|-------|
| `get_positions` | Positions for a specific account | `account` (required), `status?`, `first?`, `skip?` |
| `get_position` | Single position by ID with real-time PnL | `id` (required) |
| `search_positions` | Search positions with filters | `side?`, `tenor?`, `status?`, `minNotional?`, `first?`, `skip?` |

### Oracle & Pricing

| Tool | Description | Input |
|------|-------------|-------|
| `get_forward_price` | Current forward prices for the selected pair | `tenor?` (1D, 1W, 1M, or all), `pairId?` (defaults to EUR/USD) |
| `get_oracle_state` | Complete oracle state including spot and all forward prices | None |

### Accounts & Fees

| Tool | Description | Input |
|------|-------------|-------|
| `get_account` | Account state (margin, positions) | `address` (required) |
| `get_fee_events` | Fee event breakdown for analytics | `first?`, `skip?` |
| `get_bucket_states` | Per-(pair, maturity) net exposure cohorts; pool exposure = Σ \|bucketNet\| | `pairId?`, `first?`, `skip?` |

### Token

| Tool | Description | Input |
|------|-------------|-------|
| `get_token_balance` | ERC-20 token balance for an address (defaults to USDC) | `address` (required), `token?` |
| `check_allowance` | ERC-20 allowance for an owner/spender pair | `owner` (required), `spender` (contract name or address), `token?` |

### Simulation

| Tool | Description | Input |
|------|-------------|-------|
| `simulate_open_position` | Simulate opening a position (margin, fee, entry strike) | `side`, `tenor`, `notional`, `from?` |

## Example Queries

**Check pool health:**
> "What's the current Nile Markets pool utilization and share price?"

Uses `get_pool_state` to return total assets, utilization (basis points), share price, net exposure, and position count.

**Look up an account's positions:**
> "Show me all open positions for 0x1234...abcd"

Uses `get_positions` with `account: "0x1234...abcd"` and `status: "OPEN"`.

**Get current forward prices:**
> "What are the EUR/USD forward prices for all tenors?"

Uses `get_forward_price` without a tenor filter to return 1D, 1W, and 1M prices.

**Check protocol mode:**
> "Is the Nile Markets protocol operating normally?"

Uses `get_protocol_mode` to return the current mode and a human-readable description.

**Estimate margin for a trade:**
> "How much margin would I need to open a 1000 USDC long 1-week EUR/USD position?"

> "What are the USD/JPY forward prices?" (pass `pairId: "0x35b8bafff3570683af968b8d36b91b1a19465141d9712425e9f76c68ff8cb152"`)

Uses `simulate_open_position` with `side: "LONG"`, `tenor: "1W"`, `notional: "1000"`.

**Analyze recent fee activity:**
> "Show me the last 10 fee events on Nile Markets"

Uses `get_fee_events` with `first: 10`.

**Search for large short positions:**
> "Find all open short positions with notional above 5000 USDC"

Uses `search_positions` with `side: "SHORT"`, `status: "OPEN"`, `minNotional: "5000000000"`.

## Response Format

All tool responses include protocol metadata:

- `protocol` -- protocol identity (`name` + `version`)
- `network` -- network name (e.g., "sepolia")
- `data` -- the tool-specific result payload

Responses containing subgraph-sourced data also include `_meta.lastIndexedBlock` for freshness verification.

## Important Notes

- All monetary values use 6 decimal places (USDC standard). For example, `"1234567890"` represents 1,234.567890 USDC.
- Forward prices use 18 decimal places.
- Utilization is expressed in basis points (e.g., `"4500"` = 45%).
- Pagination defaults: `first` = 25, maximum = 1000.
- Rate limit: 100 requests per minute per IP.

## Limitations

This skill is **read-only**. It cannot:

- Manage wallets or private keys
- Sign or submit transactions
- Transfer tokens or approve spending
- Open, close, or modify positions on-chain
- Deposit or withdraw funds

For on-chain operations, users must interact with the protocol directly through the Nile Markets web application or by constructing transactions with the contract ABIs.
