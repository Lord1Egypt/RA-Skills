---
name: pacifica
description: Trade perpetuals on Pacifica via 36 MCP tools. Market data, account monitoring, order execution, subaccounts, and real-time WebSocket streaming on Solana. Trigger when the user asks about crypto prices, perps, trading, positions, orders, funding rates, or Pacifica. Skip for general knowledge, math, or questions answerable from training data.
version: 1.0.0
---

# Pacifica MCP Skill

## When to Use

Trigger when the user:
- Asks about crypto prices, perps, or trading on Pacifica / Solana
- Wants to check their trading account, positions, or open orders
- Wants to place, modify, or cancel trades
- Wants market data (orderbooks, candles, funding rates, recent trades)
- Mentions BTC, ETH, SOL, or any perpetual contract on Pacifica
- Wants real-time price/trade monitoring via WebSocket

## When NOT to Use

- General knowledge ("What is a perpetual contract?")
- Math or computation ("What's 10x leverage on $1000?")
- Questions answerable from training data alone

## Tool Selection

| User Intent | Tool | Key Params |
|---|---|---|
| Price of X | `pacifica-prices` | symbol |
| My account/balance | `pacifica-account` | — |
| My positions | `pacifica-positions` | — |
| Open a long / buy | `pacifica-market-order` | symbol, side: "bid", amount |
| Open a short / sell | `pacifica-market-order` | symbol, side: "ask", amount |
| Limit order | `pacifica-limit-order` | symbol, side, amount, price, tif |
| Stop order | `pacifica-stop-order` | symbol, side, stop_price, amount |
| Set TP / SL | `pacifica-set-tpsl` | symbol, side (exit side!), take_profit_price, stop_loss_price |
| Cancel order | `pacifica-cancel-order` | symbol, order_id (omit to cancel all) |
| Cancel stop order | `pacifica-cancel-stop` | symbol, order_id |
| Edit order | `pacifica-edit-order` | symbol, order_id, price, amount |
| Batch orders | `pacifica-batch-order` | actions (array, max 10) |
| Orderbook | `pacifica-orderbook` | symbol |
| Candles / chart | `pacifica-candles` | symbol, interval, limit |
| Mark price candles | `pacifica-mark-candles` | symbol, interval, limit |
| Funding rates | `pacifica-funding-rates` | symbol, limit |
| Recent trades | `pacifica-recent-trades` | symbol |
| Available markets | `pacifica-markets` | — |
| Order history | `pacifica-order-history` | limit |
| Trade history / PnL | `pacifica-trade-history` | symbol, limit |
| Equity curve | `pacifica-portfolio` | time_range |
| Deposits / withdrawals | `pacifica-balance-history` | limit |
| Order details by ID | `pacifica-order-by-id` | order_id |
| Account settings | `pacifica-account-settings` | — |
| My open orders | `pacifica-orders` | — |
| Set leverage | `pacifica-set-leverage` | symbol, leverage |
| Cross / isolated margin | `pacifica-set-margin-mode` | symbol, is_isolated |
| Wallet address | `pacifica-wallet` | — |
| Create subaccount | `pacifica-create-subaccount` | — |
| List subaccounts | `pacifica-list-subaccounts` | — |
| Transfer USDC to subaccount | `pacifica-transfer-funds` | to_account, amount |
| Withdraw USDC | `pacifica-withdraw` | amount |
| All available tools | `pacifica-tools` | — |
| Watch trades live | `pacifica-watch` | channel, symbol, duration |
| Monitor real-time | `pacifica-watch-start` → `pacifica-watch-read` → `pacifica-watch-stop` | channel, symbol |

## Parameter Guide

- **symbol**: Perps use uppercase with no suffix — `BTC`, `ETH`, `SOL`, `DOGE`. Spot markets use `SOL-USDC`, `BTC-USDC`, `ETH-USDC`. Run `pacifica-markets` to discover all symbols.
- **side**: `"bid"` = long/buy, `"ask"` = short/sell
- **amount**: Always a decimal string (`"0.1"`, `"1.5"`). Min order value is $10.
- **price**: Always a decimal string (`"70000"`, `"3500"`)
- **tif**: `GTC` (default), `IOC` (immediate-or-cancel), `ALO` (post-only), `TOB` (top-of-book)
- **interval**: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`

## Critical Behaviors

- **set-tpsl side is the EXIT side**, not the position side. Long position → `side: "ask"`. Short position → `side: "bid"`.
- **null responses mean success** for: `set-leverage`, `set-margin-mode`, `set-tpsl`. Verify changes with `pacifica-account-settings` or `pacifica-positions`.
- **Deposits** happen on the Pacifica web app ([test-app.pacifica.fi](https://test-app.pacifica.fi) testnet, [pacifica.fi](https://pacifica.fi) mainnet). Not through MCP or CLI.
- **Wallet auto-generated** on first run at `~/.pacifica-mcp/config.json`. Users import the private key into Phantom/Backpack to deposit.
- **Order confirmation**: For interactive use, briefly confirm order details with the user before placing. For autonomous/bot use, execute directly.
- **Withdrawals are USDC only**. If user has SOL or other spot assets and wants to withdraw, they must sell on the spot market first (e.g. `pacifica-market-order symbol: "SOL-USDC" side: "ask"`) to convert to USDC, then withdraw.
- **Subaccount funding**: Deposit to main account first via web app, then use `pacifica-transfer-funds` to move USDC to the subaccount. Min transfer: $10.
- **Spot markets** (SOL-USDC, BTC-USDC, ETH-USDC): Same order tools work. Use the spot symbol format. Max leverage is 1x (no leverage on spot).

## WebSocket (Real-Time)

| Mode | Tools | Use Case |
|---|---|---|
| Snapshot | `pacifica-watch` | Quick check: collect events for N seconds (max 60) |
| Persistent | `watch-start` → `watch-read` → `watch-stop` | Ongoing monitoring |

Channels: `prices`, `trades`, `orderbook`, `account_info`, `account_positions`, `account_trades`

- `trades` and `orderbook` require a `symbol` parameter.
- `prices` streams ALL markets — use `summary_only: true` on `watch-read` to avoid data flooding.
- `watch-read` supports `max_events` (default 100) and `summary_only` (default false).

## Free vs Wallet-Required

**Free:** markets, prices, orderbook, candles, mark-candles, recent-trades, funding-rates, account, positions, orders, order-history, trade-history, portfolio, balance-history, order-by-id, account-settings, wallet, tools, watch, watch-start, watch-read, watch-stop

**Wallet (signed):** market-order, limit-order, stop-order, set-tpsl, cancel-order, cancel-stop, edit-order, batch-order, set-leverage, set-margin-mode, create-subaccount, list-subaccounts, transfer-funds, withdraw

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| 404 account | Not deposited yet | Direct to test-app.pacifica.fi or pacifica.fi |
| 422 amount too low | Order < $10 minimum | Increase amount |
| 429 rate limited | Too many requests | Back off, retry |
| Verification failed | Bad signature | Check wallet with `pacifica-wallet` |

## Example Workflows

### Open a leveraged long
```
1. pacifica-prices (symbol: "BTC") → check mark price
2. pacifica-set-leverage (symbol: "BTC", leverage: 10)
3. pacifica-market-order (symbol: "BTC", side: "bid", amount: "0.01")
4. pacifica-positions → confirm position opened
```

### Risk management
```
1. pacifica-positions → note position side
2. pacifica-set-tpsl (symbol: "BTC", side: "ask", take_profit_price: "100000", stop_loss_price: "60000")
   (side is "ask" because exiting a long)
```

### Monitor and react
```
1. pacifica-watch-start (channel: "trades", symbol: "BTC")
2. pacifica-watch-read (subscription_id: "...", summary_only: true) → check activity
3. pacifica-watch-stop → cleanup
```

## CLI Alternative

The same 36 tools are available as a standalone CLI for terminal use:

```bash
npm install -g @pacifica-dev/cli

pacifica prices --symbol BTC
pacifica positions
pacifica market-order --symbol SOL --side bid --amount 0.5
pacifica wallet
pacifica watch --channel trades --symbol ETH --duration 10
```

Output is JSON. Pipe to `jq` for filtering: `pacifica prices --symbol BTC | jq '.mark'`

## Install

```bash
# MCP server (Claude Code, Cursor, Windsurf, VS Code Copilot, etc.)
claude mcp add pacifica npx @pacifica-dev/mcp

# Standalone CLI
npm install -g @pacifica-dev/cli
```
