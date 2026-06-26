---
name: leapcat-market
description: Access real-time stock quotes, K-line charts, market indices, stock search, and platform configuration on Leapcat via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat Market Data Skill

Access market data, stock quotes, K-line charts, indices, and platform configuration. All commands in this skill are **public and do not require authentication**.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- No authentication required for any command in this skill

## Commands

### market quote

Get the real-time quote for a specific stock.

```bash
npx leapcat@0.1.1 market quote --symbol <symbol> --exchange <exchange> --json
```

**Parameters:**
- `--symbol <symbol>` — Stock ticker symbol (e.g., `AAPL`, `9988.HK`)
- `--exchange <exchange>` — Exchange code (e.g., `NASDAQ`, `HKEX`)

### market kline

Get historical K-line (candlestick) data for a stock.

```bash
npx leapcat@0.1.1 market kline --symbol <symbol> --exchange <exchange> --period <period> --json
```

**Parameters:**
- `--symbol <symbol>` — Stock ticker symbol
- `--exchange <exchange>` — Exchange code
- `--period <period>` — K-line period (e.g., `1m`, `5m`, `15m`, `1h`, `1d`, `1w`)

### market kline-latest

Get the latest K-line data point for a stock.

```bash
npx leapcat@0.1.1 market kline-latest --symbol <symbol> --exchange <exchange> --period <period> --json
```

**Parameters:**
- `--symbol <symbol>` — Stock ticker symbol
- `--exchange <exchange>` — Exchange code
- `--period <period>` — K-line period

### market stock-detail

Get detailed information about a specific stock (company info, sector, market cap, etc.).

```bash
npx leapcat@0.1.1 market stock-detail --symbol <symbol> --exchange <exchange> --json
```

**Parameters:**
- `--symbol <symbol>` — Stock ticker symbol
- `--exchange <exchange>` — Exchange code

### market indices

Get current market index data (e.g., S&P 500, Hang Seng, NASDAQ Composite).

```bash
npx leapcat@0.1.1 market indices --json
```

### market overview

Get a general market overview including major market movements and summaries.

```bash
npx leapcat@0.1.1 market overview --json
```

### market stocks

List available stocks, optionally filtered by exchange or keyword. Useful for searching stocks by name.

```bash
npx leapcat@0.1.1 market stocks [--exchange <exchange>] [--keyword <search-term>] --json
```

**Parameters:**
- `--exchange <exchange>` — Filter by exchange code (optional)
- `--keyword <search-term>` — Search stocks by name or symbol (optional)

### config exchange-rate

Get current exchange rates used by the platform.

```bash
npx leapcat@0.1.1 config exchange-rate --json
```

### config fee-rate

Get the platform's trading fee rate schedule.

```bash
npx leapcat@0.1.1 config fee-rate --json
```

### config withdrawal-fees

Get the fee schedule for withdrawals.

```bash
npx leapcat@0.1.1 config withdrawal-fees --json
```

## Workflow

### Browse the Market

1. **Market overview** — Run `market overview --json` for a high-level market summary.
2. **View indices** — Run `market indices --json` to see major index performance.
3. **Search stocks** — Run `market stocks --keyword <term> --json` to find stocks by name or symbol.

### Research a Specific Stock

1. **Get stock detail** — Run `market stock-detail --symbol <symbol> --exchange <exchange> --json` for company information.
2. **Get current quote** — Run `market quote --symbol <symbol> --exchange <exchange> --json` for real-time pricing.
3. **View price history** — Run `market kline --symbol <symbol> --exchange <exchange> --period 1d --json` for historical price data.

### Check Platform Configuration

1. **Exchange rates** — Run `config exchange-rate --json` to see currency conversion rates.
2. **Fee rates** — Run `config fee-rate --json` to understand trading costs.
3. **Withdrawal fees** — Run `config withdrawal-fees --json` to see withdrawal cost structure.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `INVALID_SYMBOL` | Unrecognized stock symbol | Search with `market stocks --keyword <term> --json` |
| `INVALID_EXCHANGE` | Unrecognized exchange code | Check available exchanges via `market stocks --json` |
| `INVALID_PERIOD` | Unsupported K-line period | Use one of: `1m`, `5m`, `15m`, `1h`, `1d`, `1w` |
| `MARKET_DATA_UNAVAILABLE` | Data source temporarily unavailable | Retry after a short delay |
