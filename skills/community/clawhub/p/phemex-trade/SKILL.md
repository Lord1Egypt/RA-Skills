---
name: phemex-trade
description: Trade on Phemex (USDT-M futures, Coin-M futures, Spot) — place orders, manage positions, check balances, and query market data. Use when the user wants to (1) check crypto prices or market data on Phemex, (2) place, amend, or cancel orders, (3) view account balances or positions, (4) set leverage or switch position modes, (5) transfer funds between spot and futures wallets, or (6) any task involving the Phemex exchange.
homepage: https://github.com/betta2moon/phemex-trade-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["phemex-cli"], "env": ["PHEMEX_API_KEY", "PHEMEX_API_SECRET"] },
        "primaryEnv": "PHEMEX_API_KEY",
        "install":
          [
            {
              "id": "phemex-trade-mcp",
              "kind": "node",
              "package": "phemex-trade-mcp",
              "bins": ["phemex-cli"],
              "label": "Install Phemex CLI (node)",
            },
          ],
      },
  }
---

# Phemex Trading

Trade on Phemex via the phemex-cli tool. Supports USDT-M futures, Coin-M futures, and Spot markets.

## What's New in v1.2.0

1. **`list_symbols` tool** — Discover all available trading pairs, filtered by contract type. No more guessing symbol names.
2. **Config file (`~/.phemexrc`)** — Store API credentials persistently. No need to `export` env vars every session.
3. **`--help` for every tool** — Run `phemex-cli <tool> --help` to see parameters, defaults, and usage examples inline.
4. **Friendly field names** — API field suffixes (`closeRp`, `fundingRateRr`) are mapped to readable names (`closePrice`, `fundingRate`). Use `--raw` to get the original names.
5. **Enhanced error messages** — Errors now include `suggestion` and `tip` fields with actionable guidance instead of raw API codes.

## Before you start

Ensure you have the latest version installed:

```bash
npm install -g phemex-trade-mcp@latest
```

## How to call tools

```bash
phemex-cli <tool_name> --param1 value1 --param2 value2
```

Or with JSON args:

```bash
phemex-cli <tool_name> '{"param1":"value1","param2":"value2"}'
```

Output is always JSON. Credentials are loaded from environment variables or `~/.phemexrc` (see Setup).

### Tool help

Every tool supports `--help` with full parameter docs and examples:

```bash
phemex-cli place_order --help
```

Output:

```
Usage: phemex-cli place_order [options]

Place an order (Market, Limit, Stop, StopLimit)

Required Parameters:
  --symbol <string>          Trading pair (e.g. BTCUSDT)
  --side <string>            Buy or Sell
  --orderQty <number>        Quantity. linear: base amount (0.01 = 0.01 BTC). ...
  --ordType <string>         Order type: Market, Limit, Stop, StopLimit

Optional Parameters:
  --price <number>           Limit price (required for Limit/StopLimit)
  --timeInForce <string>     GoodTillCancel, PostOnly, ... [default: GoodTillCancel]
  --reduceOnly <boolean>     Only reduce position [default: false]
  ...

Examples:
  phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 0.01 --ordType Market
  phemex-cli place_order --symbol BTCUSDT --side Sell --orderQty 0.01 --ordType Limit --price 90000 --timeInForce PostOnly
```

More help examples:

```bash
phemex-cli get_ticker --help        # see params for price ticker
phemex-cli get_klines --help        # see resolution values for candlesticks
phemex-cli set_leverage --help      # see leverage param format
phemex-cli transfer_funds --help    # see direction values
phemex-cli list_symbols --help      # see contractType filter
```

### Friendly field names

By default, output uses readable field names:

```bash
phemex-cli get_ticker --symbol BTCUSDT
```

```json
{
  "closePrice": "70549.9",
  "openPrice": "70192.7",
  "highPrice": "70750",
  "lowPrice": "69160",
  "markPrice": "70549.9",
  "fundingRate": "-0.00003417",
  "volume": "5303.525",
  "turnover": "371204351.5978"
}
```

Use `--raw` to get original API field names (for scripts that depend on old format):

```bash
phemex-cli get_ticker --symbol BTCUSDT --raw
```

```json
{
  "closeRp": "70549.9",
  "openRp": "70192.7",
  "highRp": "70750",
  "lowRp": "69160",
  "markPriceRp": "70549.9",
  "fundingRateRr": "-0.00003417",
  "volumeRq": "5303.525",
  "turnoverRv": "371204351.5978"
}
```

**Field name mapping reference:**

| Suffix | Meaning | Example | Mapped to |
|--------|---------|---------|-----------|
| `Rp` | Real Price | `closeRp` | `closePrice` |
| `Rv` | Real Value | `accountBalanceRv` | `accountBalance` |
| `Rr` | Real Rate | `fundingRateRr` | `fundingRate` |
| `Rq` | Real Quantity | `volumeRq` | `volume` |

## Contract types

Every tool accepts an optional `--contractType` flag:

- `linear` (default) — USDT-M perpetual futures. Symbols end in USDT (e.g. BTCUSDT).
- `inverse` — Coin-M perpetual futures. Symbols end in USD (e.g. BTCUSD).
- `spot` — Spot trading. Symbols end in USDT (e.g. BTCUSDT). The server auto-prefixes `s` for the API.

## Tools

### Market data (no auth needed)

- `get_ticker` — 24hr price ticker. Example: `phemex-cli get_ticker --symbol BTCUSDT`
- `get_orderbook` — Order book (30 levels). Example: `phemex-cli get_orderbook --symbol BTCUSDT`
- `get_klines` — Candlestick data. Example: `phemex-cli get_klines --symbol BTCUSDT --resolution 3600 --limit 100`
- `get_recent_trades` — Recent trades. Example: `phemex-cli get_recent_trades --symbol BTCUSDT`
- `get_funding_rate` — Funding rate history. Example: `phemex-cli get_funding_rate --symbol .BTCFR8H --limit 20`

### Account (read-only, auth required)

- `get_account` — Balance and margin info. Example: `phemex-cli get_account --currency USDT`
- `get_spot_wallet` — Spot wallet balances. Example: `phemex-cli get_spot_wallet`
- `get_positions` — Current positions with PnL. Example: `phemex-cli get_positions --currency USDT`
- `get_open_orders` — Open orders. Example: `phemex-cli get_open_orders --symbol BTCUSDT`
- `get_order_history` — Closed/filled orders. Example: `phemex-cli get_order_history --symbol BTCUSDT --limit 50`
- `get_trades` — Trade execution history. Example: `phemex-cli get_trades --symbol BTCUSDT --limit 50`

### Trading (auth required)

- `place_order` — Place an order (Market, Limit, Stop, StopLimit). Key params: `--symbol`, `--side` (Buy/Sell), `--orderQty`, `--ordType`, `--price` (Limit/StopLimit), `--stopPx` (Stop/StopLimit), `--timeInForce` (GoodTillCancel/PostOnly/ImmediateOrCancel/FillOrKill), `--reduceOnly`, `--posSide` (Long/Short/Merged), `--stopLoss`, `--takeProfit`, `--qtyType` (spot only). **orderQty units differ by contract type:**
  - `linear` (USDT-M): orderQty = base currency amount (e.g. `0.01` = 0.01 BTC). To buy 10 USDT worth, calculate qty = 10 / current price.
  - `inverse` (Coin-M): orderQty = number of contracts as integer (e.g. `10` = 10 contracts). Each contract has a fixed USD value (e.g. 1 USD/contract for BTCUSD).
  - `spot`: depends on `--qtyType`. `ByBase` (default) = base currency (e.g. `0.01` = 0.01 BTC). `ByQuote` = quote currency (e.g. `50` = 50 USDT worth of BTC).
  - Example: `phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 0.01 --ordType Market`
- `amend_order` — Modify an open order. Example: `phemex-cli amend_order --symbol BTCUSDT --orderID xxx --price 95000`
- `cancel_order` — Cancel one order. Example: `phemex-cli cancel_order --symbol BTCUSDT --orderID xxx`
- `cancel_all_orders` — Cancel all orders for a symbol. Example: `phemex-cli cancel_all_orders --symbol BTCUSDT`
- `set_leverage` — Set leverage. Example: `phemex-cli set_leverage --symbol BTCUSDT --leverage 10`
- `switch_pos_mode` — Switch OneWay/Hedged. Example: `phemex-cli switch_pos_mode --symbol BTCUSDT --targetPosMode OneWay`

### Transfers (auth required)

- `transfer_funds` — Move funds between spot and futures. Example: `phemex-cli transfer_funds --currency USDT --amount 100 --direction spot_to_futures`
- `get_transfer_history` — Transfer history. Example: `phemex-cli get_transfer_history --currency USDT --limit 20`

### Utility

- `list_symbols` — List all available trading symbols, grouped by contract type.

```bash
# List all symbols (linear, inverse, spot)
phemex-cli list_symbols

# Only USDT-M perpetual futures
phemex-cli list_symbols --contractType linear

# Only Coin-M perpetual futures
phemex-cli list_symbols --contractType inverse

# Only spot pairs
phemex-cli list_symbols --contractType spot
```

Example output:

```json
{
  "linear": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", ...],
  "inverse": ["BTCUSD", "ETHUSD", ...],
  "spot": ["BTCUSDT", "ETHUSDT", ...]
}
```

Use `list_symbols` to discover valid symbol names before trading. This avoids "invalid symbol" errors.

## Error messages

Errors return structured JSON with actionable guidance. Examples:

**Invalid symbol:**

```bash
phemex-cli get_ticker --symbol INVALIDXXX
```

```json
{
  "error": "Invalid symbol: INVALIDXXX",
  "code": 6001,
  "suggestion": "Symbol \"INVALIDXXX\" is not recognized. Check spelling and contract type.",
  "tip": "Run \"phemex-cli list_symbols\" to see all available symbols."
}
```

**Common typo (BTCUSD instead of BTCUSDT):**

```bash
phemex-cli get_ticker --symbol BTCUSD
```

```json
{
  "error": "Invalid symbol: BTCUSD",
  "code": 6001,
  "suggestion": "Did you mean BTCUSDT? For USDT perpetuals, use symbols ending in USDT (e.g. BTCUSDT).",
  "tip": "Run \"phemex-cli list_symbols\" to see all available symbols."
}
```

**Order quantity too large:**

```json
{
  "error": "Order quantity too large",
  "code": "TE_QTY_TOO_LARGE",
  "suggestion": "The order quantity exceeds the maximum allowed for BTCUSDT.",
  "tip": "Reduce --orderQty or check the symbol's max order size on Phemex."
}
```

**Other enhanced errors:** insufficient balance, invalid API key, rate limiting, invalid leverage, order not found — all include `suggestion` and `tip` fields.

## Safety rules

1. **Always confirm before placing orders.** Before calling `place_order`, show the user exactly what the order will do: symbol, side, quantity, type, price. Ask for confirmation.
2. **Always confirm before cancelling all orders.** Before calling `cancel_all_orders`, list the open orders first and confirm with the user.
3. **Explain leverage changes.** Before calling `set_leverage`, explain the implications (higher leverage = higher liquidation risk).
4. **Show context before trading.** Before suggesting a trade, show current positions and account balance so the user can make an informed decision.
5. **Never auto-trade.** Do not place orders without explicit user instruction.

## Common workflows

### Check a price

```bash
phemex-cli get_ticker --symbol BTCUSDT
```

### Discover available symbols

```bash
phemex-cli list_symbols --contractType linear
```

### Place a market buy (USDT-M futures)

```bash
phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 0.01 --ordType Market
```

### Place a limit sell (Coin-M futures)

```bash
phemex-cli place_order --symbol BTCUSD --side Sell --orderQty 10 --ordType Limit --price 100000 --contractType inverse
```

### Buy spot

```bash
phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 10 --ordType Market --contractType spot --qtyType ByQuote
```

### Check positions

```bash
phemex-cli get_positions --currency USDT
```

### Get help for any command

```bash
phemex-cli place_order --help
```

## Setup

### Option 1: Config file (recommended)

Create `~/.phemexrc` — credentials persist across sessions without exporting env vars:

```bash
# ~/.phemexrc
PHEMEX_API_KEY=your-api-key
PHEMEX_API_SECRET=your-api-secret
PHEMEX_API_URL=https://api.phemex.com

# Optional: max order value limit (USD)
PHEMEX_MAX_ORDER_VALUE=1000
```

That's it. All `phemex-cli` commands will pick up these values automatically.

### Option 2: Environment variables

```bash
export PHEMEX_API_KEY=your-api-key
export PHEMEX_API_SECRET=your-api-secret
export PHEMEX_API_URL=https://api.phemex.com
```

### Configuration priority

Settings are loaded in this order (highest priority first):

1. Command-line arguments
2. Environment variables
3. `~/.phemexrc` config file
4. Defaults (testnet URL)

This means env vars always override the config file, so you can safely keep production creds in `~/.phemexrc` and temporarily override with `PHEMEX_API_URL=https://testnet-api.phemex.com phemex-cli ...` for testing.

### Steps

1. Create a Phemex account at https://phemex.com
2. Create an API key (Account → API Management)
3. Save credentials to `~/.phemexrc` or export as environment variables
4. Verify: `phemex-cli list_symbols --contractType linear` should return symbols
5. Optionally set `PHEMEX_API_URL` (defaults to testnet `https://testnet-api.phemex.com` for safety; set to `https://api.phemex.com` for real trading)
6. Optionally set `PHEMEX_MAX_ORDER_VALUE` to limit maximum order size (USD)
