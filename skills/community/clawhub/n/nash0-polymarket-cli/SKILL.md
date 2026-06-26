---
name: polymarket-cli
description: "Use the Polymarket CLI (`polymarket`) to browse markets, inspect order books and prices, check public wallet data, review account state, and place or cancel orders. Use when a user asks to interact with Polymarket from the terminal, especially for: (1) listing, searching, and fetching markets or events, (2) reading CLOB books, spreads, midpoints, and price history, (3) checking positions, volume, holders, or leaderboards, (4) reviewing approval or account status, or (5) trading via `clob` commands. Never run wallet-management commands or read local private-key config files." 
---

# Polymarket CLI

Use the `polymarket` binary directly. Prefer read-only commands by default, use `-o json` for structured output, and treat any trading or on-chain action as sensitive.

## Safety rules

Never read `~/.config/polymarket/config.json` or any file that may contain private keys.

Never run wallet-management commands yourself. The user must run these directly:
- `polymarket wallet create`
- `polymarket wallet import`
- `polymarket wallet show`
- `polymarket wallet reset`
- `polymarket wallet address`
- `polymarket setup`

Ask before running any command that can:
- place, modify, or cancel orders
- approve contracts
- split, merge, redeem, or bridge assets
- create/delete API keys or notifications
- write private keys or config

Safe to run without extra confirmation:
- `markets`, `events`, `tags`, `series`, `comments`, `profiles`, `sports`
- read-only `clob` commands like `book`, `price`, `midpoint`, `spread`, `price-history`, `market`
- public `data` commands for wallets, markets, holders, volume, leaderboards
- health/version/help commands

Read-only authenticated commands are allowed only when they do not reveal secrets and do not modify state.

## Quick start

Check availability first:

```bash
polymarket --help
polymarket --version
```

Use JSON for agent work:

```bash
polymarket -o json markets list --limit 5
polymarket -o json markets search "bitcoin" --limit 5
polymarket -o json clob midpoint TOKEN_ID
```

## Opinionated workflows

### Research a market

Use this when the user wants a quick market read without trading.

1. Search likely candidates:

```bash
polymarket -o json markets search "QUERY" --limit 10
```

2. Pick the most relevant slug or tokenized market.
3. If needed, inspect details:

```bash
polymarket -o json markets get MARKET_ID_OR_SLUG
```

4. If token IDs are available, inspect price/action:

```bash
polymarket -o json clob midpoint TOKEN_ID
polymarket -o json clob spread TOKEN_ID
polymarket -o json clob book TOKEN_ID
polymarket -o json clob price-history TOKEN_ID --interval 1d --fidelity 30
```

Summarize with: question, current odds, spread/liquidity hints, recent price context, and any obvious caveats.

### Check a wallet safely

Use this when the user wants exposure, PnL-ish status, or activity without changing anything.

```bash
polymarket -o json data positions 0xWALLET
polymarket -o json data value 0xWALLET
polymarket -o json data trades 0xWALLET --limit 50
```

If the local configured wallet is relevant and the user wants account state, use read-only authenticated checks that do not expose secrets:

```bash
polymarket -o json clob balance --asset-type collateral
polymarket -o json clob orders
polymarket -o json clob trades
polymarket approve check
```

Do not run `wallet show`; tell the user to run wallet-management commands themselves.

### Place a limit order safely

Do not run until the user confirms all of:
- market or token
- side (`buy`/`sell`)
- price
- size or amount
- whether post-only is desired

Recommended sequence:

```bash
# 1) Verify market context first
polymarket -o json clob midpoint TOKEN_ID
polymarket -o json clob spread TOKEN_ID
polymarket -o json clob book TOKEN_ID

# 2) Then place only after confirmation
polymarket clob create-order --token TOKEN_ID --side buy --price 0.50 --size 10
```

Repeat the full order back to the user before execution.

## Common tasks

### Browse markets and events

```bash
polymarket markets list --limit 10
polymarket markets search "election" --limit 5
polymarket markets get MARKET_ID_OR_SLUG
polymarket events list --limit 10
polymarket events get EVENT_ID
```

### Inspect price/action on the CLOB

```bash
polymarket clob ok
polymarket clob book TOKEN_ID
polymarket clob midpoint TOKEN_ID
polymarket clob spread TOKEN_ID
polymarket clob price-history TOKEN_ID --interval 1d --fidelity 30
```

### Inspect public wallet/market data

```bash
polymarket data positions 0xWALLET
polymarket data value 0xWALLET
polymarket data trades 0xWALLET --limit 50
polymarket data holders 0xCONDITION_ID
polymarket data open-interest 0xCONDITION_ID
polymarket data leaderboard --period month --order-by pnl --limit 10
```

### Wallet and setup

Wallet-management commands are user-only. Do not run them yourself. If the user wants setup help, tell them which command to run locally.

```bash
# user-only
polymarket setup
polymarket wallet create
polymarket wallet import 0xPRIVATE_KEY
polymarket wallet show

# agent may run read-only approval checks
polymarket approve check

# agent must ask before any on-chain approval write
polymarket approve set
```

### Trading

Only run after confirmation.

```bash
polymarket clob create-order --token TOKEN_ID --side buy --price 0.50 --size 10
polymarket clob market-order --token TOKEN_ID --side buy --amount 5
polymarket clob orders
polymarket clob cancel ORDER_ID
polymarket clob cancel-all
```

## Working style

1. Prefer read-only discovery first.
2. If the user wants trading, verify the exact token/market, side, size/amount, and price before running anything.
3. For scripts and summaries, use `-o json` and parse the result.
4. If a command fails, rerun with `--help` on the relevant subcommand to inspect flags.
5. If the CLI is missing, tell the user how to install it:

```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```

## Reference

Read `references/command-map.md` when you need a fuller command inventory or a reminder of which areas are read-only vs sensitive.
