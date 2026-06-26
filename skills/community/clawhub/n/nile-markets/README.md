# Nile Markets OpenClaw Skill

OpenClaw skill for querying the [Nile Markets](https://docs.nilemarkets.com) protocol -- an EUR/USD non-deliverable forward (NDF) protocol on Ethereum Sepolia.

> **Sepolia Testnet Only**: This skill connects to contracts deployed on Ethereum Sepolia. All data is testnet data with no real monetary value. The API is under active development and may change without notice.

## Overview

This is a thin MCP shim that delegates all data access to the Nile Markets MCP server. It provides read-only access to:

- **Pool state** -- total assets, utilization, share price, exposure
- **Positions** -- query by account, search with filters, real-time PnL
- **Oracle prices** -- spot and forward prices for EUR/USD (1D, 1W, 1M tenors)
- **Account data** -- margin balances, position summaries
- **Fee analytics** -- fee event breakdowns, daily statistics
- **Trade simulation** -- estimate margin requirements before opening positions

The skill exposes 12 read-only MCP tools. It does not perform any on-chain writes, wallet management, or token transfers.

## Prerequisites

Set the `NILE_MCP_URL` environment variable to the Nile Markets MCP server endpoint:

```bash
# Production (Sepolia)
export NILE_MCP_URL="https://mcp.nilemarkets.com/api/mcp"

# Local development
export NILE_MCP_URL="http://localhost:3000/api/mcp"
```

## Getting Started

1. Set the MCP endpoint:
   ```bash
   export NILE_MCP_URL="https://mcp.nilemarkets.com/api/mcp"
   ```

2. Install the skill:
   ```bash
   clawhub install nile-markets
   ```

3. Query the protocol:
   ```
   What's the Nile Markets pool utilization?
   ```

## Installation

### From ClawHub

```bash
clawhub install nile-markets
```

### From Source

Contact [Nile Markets](https://docs.nilemarkets.com) for source access.

## Publishing Updates

To publish or update the skill on ClawHub:

```bash
clawhub publish ./integrations/openclaw --slug nile-markets
```

This publishes the `SKILL.md` (with YAML frontmatter and usage instructions) and the `config/mcporter.json` MCP server configuration.

## Skill Structure

```
integrations/openclaw/
├── SKILL.md                    # Skill definition (YAML frontmatter + usage instructions)
├── config/
│   └── mcporter.json           # MCP server config (OpenClaw convention)
└── README.md                   # This file
```

- **SKILL.md** -- agentskills.io format with YAML frontmatter (`name`, `description`, `version`, `requires`, `metadata.openclaw`) and markdown body containing tool documentation, example queries, and usage guidelines.
- **config/mcporter.json** -- MCP server connection config. Uses `${NILE_MCP_URL}` environment variable for the server URL with streamable HTTP transport.

## Usage Examples

Once the skill is installed, you can ask questions in natural language:

| Query | MCP Tool Used |
|-------|---------------|
| "What's the Nile Markets pool utilization?" | `get_pool_state` |
| "Show open positions for 0xABC..." | `get_positions` |
| "What are the current EUR/USD forward prices?" | `get_forward_price` |
| "Is the protocol operating normally?" | `get_protocol_mode` |
| "How much margin do I need for a 1000 USDC long 1W position?" | `simulate_open_position` |
| "Show me the last 7 days of protocol stats" | `get_daily_stats` |
| "Find all open short positions above 5000 USDC notional" | `search_positions` |
| "What's the oracle state?" | `get_oracle_state` |
| "Show recent pool deposits and withdrawals" | `get_pool_transactions` |
| "Show fee events for the last 10 transactions" | `get_fee_events` |

## Available Tools

The skill provides 12 read-only tools:

| Tool | Description |
|------|-------------|
| `get_pool_state` | Current liquidity pool metrics |
| `get_protocol_mode` | Current operating mode |
| `get_pool_transactions` | Historical deposits and withdrawals |
| `get_daily_stats` | Daily protocol statistics |
| `get_positions` | Positions for a specific account |
| `get_position` | Single position with real-time PnL |
| `search_positions` | Search and filter positions |
| `get_forward_price` | EUR/USD forward prices by tenor |
| `get_oracle_state` | Complete oracle state |
| `get_account` | Account margin and position state |
| `get_fee_events` | Fee event analytics |
| `simulate_open_position` | Estimate margin for a new position |

See [SKILL.md](./SKILL.md) for full tool documentation including input parameters and response formats.

## Documentation

- **Protocol docs**: [docs.nilemarkets.com](https://docs.nilemarkets.com)
- **MCP server docs**: [docs.nilemarkets.com/ai-agents/mcp-server](https://docs.nilemarkets.com/ai-agents/mcp-server)
- **Smart contract reference**: [docs.nilemarkets.com/smart-contracts](https://docs.nilemarkets.com/smart-contracts)

## Limitations

This skill is **read-only**. It cannot manage wallets, sign transactions, transfer tokens, or perform any on-chain writes. For on-chain operations, use the [Nile Markets web application](https://app.nilemarkets.com) or construct transactions directly with the contract ABIs.

## License

See the repository root [LICENSE](../../LICENSE) for details.
