# Yahoo Finance (yahoo-finance-mcp)

Comprehensive financial data from Yahoo Finance via MCP. Provides stock prices, financial statements, holder info, analyst recommendations, options data, and news. No API key required.

## Prerequisites

```bash
# No install needed — uvx fetches from GitHub on first use
# For persistent install:
uv tool install --from git+https://github.com/Alex2Yang97/yahoo-finance-mcp yahoo-finance-mcp
```

## Actions

### `historical_prices`
Get historical OHLCV data.

```bash
python3 scripts/reach.py query yahoo_finance historical_prices '{"symbol": "AAPL", "period": "6mo", "interval": "1d"}'
```

Params:
- `symbol` (string, required) — Ticker symbol
- `period` (string, default: "1mo") — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
- `interval` (string, default: "1d") — 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

### `stock_info`
Get comprehensive stock metrics (P/E, market cap, beta, 52-week high/low, etc.).

```bash
python3 scripts/reach.py query yahoo_finance stock_info '{"symbol": "AAPL"}'
```

### `news`
Get latest news articles.

```bash
python3 scripts/reach.py query yahoo_finance news '{"symbol": "AAPL", "count": 10}'
```

### `financial_statement`
Get income statement, balance sheet, or cash flow.

```bash
python3 scripts/reach.py query yahoo_finance financial_statement '{"symbol": "AAPL", "statement_type": "income", "period": "quarterly"}'
```

Params:
- `statement_type` — income, balance_sheet, cashflow
- `period` — annual, quarterly

### `holder_info`
Get holder information.

```bash
python3 scripts/reach.py query yahoo_finance holder_info '{"symbol": "AAPL", "holder_type": "insider"}'
```

Params:
- `holder_type` — major_holders, institutional_holders, mutual_fund_holders, insider_transactions

### `recommendations`
Get analyst recommendations.

```bash
python3 scripts/reach.py query yahoo_finance recommendations '{"symbol": "AAPL"}'
```

### `options_chain`
Get options chain.

```bash
python3 scripts/reach.py query yahoo_finance options_chain '{"symbol": "AAPL", "expiration": "2026-06-20", "option_type": "calls"}'
```

### `stock_actions`
Get dividends and stock splits.

```bash
python3 scripts/reach.py query yahoo_finance stock_actions '{"symbol": "AAPL"}'
```

## Integration with Rally

Rally uses Yahoo Finance MCP as a **supplementary data source**:

| Rally Signal | Yahoo Finance MCP tool | Purpose |
|---|---|---|
| Quality / Safety | `financial_statement` | Real financials for quality scoring |
| Momentum | `historical_prices` | Price data (supplements direct YF v8) |
| Sentiment | `news` | News articles (supplements Finnhub) |
| Sentiment | `recommendations` | Analyst recs (supplements Finnhub) |
| Flow | `holder_info` (insider) | Insider transactions (supplements Massive) |

**Graceful degradation**: If the MCP server is unavailable, Rally falls back to:
- Direct YF v8 API for price data
- Finnhub for news and recommendations
- Massive for insider/congressional flow

## Pitfalls

- **Rate limits** — Yahoo Finance API can be rate-limited. Throttle to ~5 req/sec.
- **yfinance library** — The MCP server uses the `yfinance` Python library, which scrapes Yahoo Finance. Yahoo may change their API without notice.
- **MCP server startup** — First call may be slow (~10s) as uvx downloads from GitHub. Subsequent calls are fast.
- **Data freshness** — Yahoo Finance data may be delayed 15-20 minutes for some exchanges.
