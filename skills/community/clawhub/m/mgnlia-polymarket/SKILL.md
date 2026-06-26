---
name: polymarket
description: "Browse, trade, and manage positions on Polymarket prediction markets via the polymarket CLI. Use when: user asks about prediction market odds, wants to search/browse markets, check prices, place/cancel orders, view portfolio, or interact with Polymarket CLOB. Supports JSON output for programmatic use. NOT for: general crypto trading (use other tools), non-Polymarket prediction platforms."
version: 1.0.0
---

# Polymarket CLI Skill

Trade prediction markets on Polymarket from the terminal. All commands use the `polymarket` binary.

## Prerequisites

Binary must be installed. If missing:
```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
# Or build from source:
# cargo install --path /tmp/polymarket-cli
```

## Authentication

Most read commands work without a wallet. Trading requires setup:
```bash
polymarket setup                    # Interactive wizard
# Or manually:
polymarket wallet create            # New wallet
polymarket wallet import 0xKEY...   # Import existing
polymarket approve set              # Approve contracts (needs MATIC)
```

Config stored at `~/.config/polymarket/config.json`.

## Output

**Always use `-o json` when calling from scripts/agents** for machine-readable output:
```bash
polymarket -o json markets list --limit 5
polymarket -o json clob midpoint TOKEN_ID
```

## Common Workflows

### Browse & Research

```bash
# Search markets
polymarket markets search "bitcoin" --limit 10
polymarket -o json markets search "trump" --limit 5

# Get specific market
polymarket markets get MARKET_ID_OR_SLUG

# List by category
polymarket events list --tag politics --active true --limit 20
polymarket events list --tag crypto --limit 10

# Available tags
polymarket tags list
```

### Check Prices & Orderbook

```bash
# Price info (needs token ID from market data)
polymarket clob price TOKEN_ID --side buy
polymarket clob midpoint TOKEN_ID
polymarket clob spread TOKEN_ID

# Full orderbook
polymarket clob book TOKEN_ID

# Price history
polymarket clob price-history TOKEN_ID --interval 1d --fidelity 30
# Intervals: 1m, 1h, 6h, 1d, 1w, max

# Batch queries (comma-separated)
polymarket clob midpoints "TOKEN1,TOKEN2"
```

### Trading (Requires Wallet)

```bash
# Limit order: buy 10 shares at $0.45
polymarket clob create-order --token TOKEN_ID --side buy --price 0.45 --size 10

# Market order: buy $5 worth
polymarket clob market-order --token TOKEN_ID --side buy --amount 5

# Batch orders
polymarket clob post-orders --tokens "T1,T2" --side buy --prices "0.4,0.6" --sizes "10,10"

# Cancel
polymarket clob cancel ORDER_ID
polymarket clob cancel-all

# Check orders
polymarket clob orders
polymarket clob trades
```

Order types: `GTC` (default), `FOK`, `GTD`, `FAK`. Add `--post-only` for maker-only.

### Portfolio & Positions

```bash
# Your positions
polymarket data positions 0xWALLET
polymarket data value 0xWALLET
polymarket clob balance --asset-type collateral

# Trade history
polymarket data trades 0xWALLET --limit 50

# Leaderboard
polymarket data leaderboard --period month --order-by pnl --limit 10
```

### On-Chain Operations

```bash
# Approvals
polymarket approve check
polymarket approve set

# Split USDC into YES/NO tokens
polymarket ctf split --condition 0xCOND... --amount 10

# Merge back to USDC
polymarket ctf merge --condition 0xCOND... --amount 10

# Redeem after resolution
polymarket ctf redeem --condition 0xCOND...
```

### Market Rewards

```bash
polymarket clob rewards --date 2026-02-28
polymarket clob current-rewards
polymarket clob market-reward 0xCONDITION...
polymarket clob order-scoring ORDER_ID
```

### Bridge (Deposits)

```bash
polymarket bridge deposit 0xWALLET
polymarket bridge supported-assets
```

## Data Flow: Finding Token IDs

Markets → Events → Token IDs → CLOB operations:

```bash
# 1. Search for a market
polymarket -o json markets search "bitcoin 100k" | jq '.[0]'

# 2. Get token IDs from market data
polymarket -o json markets get SLUG | jq '.clobTokenIds'
# Returns: ["TOKEN_YES", "TOKEN_NO"]

# 3. Use token IDs for CLOB
polymarket clob midpoint TOKEN_YES
polymarket clob book TOKEN_YES
```

## Tips

- Token IDs are long numeric strings (e.g., `48331043336612883...`)
- Condition IDs are hex addresses (`0x...`)
- Prices are 0-1 (displayed as cents: `0.52` = `52¢`)
- Amounts in USDC (e.g., `--amount 10` = $10)
- On-chain ops need MATIC for gas (Polygon)
- Use `polymarket shell` for interactive REPL
- Pipe JSON output to `jq` for filtering

## References

- [Polymarket CLI GitHub](https://github.com/Polymarket/polymarket-cli)
- [Polymarket Docs](https://docs.polymarket.com)
- Chain: Polygon (chainId 137)
- Collateral: USDC
