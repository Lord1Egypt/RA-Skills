# alpha_vantage — equities, FX, and fundamentals

## What this source has

Alpha Vantage offers a unified API for stock prices (daily/intraday/weekly/monthly), FX rates, crypto, technical indicators, and company fundamentals (overview, income statement, balance sheet, cash flow, earnings). Each "function" is its own endpoint behind the same `/query` URL — `function=TIME_SERIES_DAILY`, `function=GLOBAL_QUOTE`, `function=OVERVIEW`, `function=FX_DAILY`, etc.

Coverage is global equities (NYSE, NASDAQ, LSE, TSE, etc.), forex pairs, hundreds of indicators. Daily data goes back ~20 years for major US tickers; intraday goes back 1-2 years.

Use Alpha Vantage for: stock OHLCV, current quote, basic company overview, FX time series. Pair with `sec_edgar` when you need authoritative US filings (Alpha Vantage's fundamentals are derived). The 25-call daily cap is the dominant constraint — budget aggressively.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `ALPHA_VANTAGE_KEY` |
| Account URL | https://www.alphavantage.co/support/#api-key |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Signup is a single form; key issued instantly.

## Limits

| | |
|---|---|
| Daily | **25** |
| Monthly | **750** (implied: 25/day) |
| Rate | 5 req/min |

The 25/day cap is a hard wall on the free tier — once hit, every subsequent call returns the same JSON with a `"Information"` key explaining the limit, NOT a 429. Detect by inspecting the response body.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `time_series_daily` | Daily OHLCV for an equity | `symbol` |
| `global_quote` | Latest snapshot quote | `symbol` |
| `fx_daily` | Daily FX rates | `from_symbol`, `to_symbol` |
| `overview` | Company fundamentals overview | `symbol` |

## Worked examples

```bash
# Daily OHLCV for AAPL (compact = last 100 days)
python3 scripts/reach.py query alpha_vantage time_series_daily '{
  "symbol": "AAPL",
  "outputsize": "compact"
}'

# Current quote
python3 scripts/reach.py query alpha_vantage global_quote '{"symbol": "AAPL"}'

# EUR/USD daily FX
python3 scripts/reach.py query alpha_vantage fx_daily '{
  "from_symbol": "EUR",
  "to_symbol": "USD"
}'

# Company overview
python3 scripts/reach.py query alpha_vantage overview '{"symbol": "MSFT"}'
```

## Response shape

- `time_series_daily`: `{"Meta Data": {"1. Information": "...", "2. Symbol": "AAPL", "3. Last Refreshed": "2026-04-25", ...}, "Time Series (Daily)": {"2026-04-25": {"1. open": "...", "2. high": "...", "3. low": "...", "4. close": "...", "5. volume": "..."}, ...}}`. Field names are numbered strings — quirky but stable.
- `global_quote`: `{"Global Quote": {"01. symbol": "AAPL", "02. open": "...", "03. high": "...", "04. low": "...", "05. price": "...", "06. volume": "...", "07. latest trading day": "...", "08. previous close": "...", "09. change": "...", "10. change percent": "...%"}}`.
- `fx_daily`: similar shape with `"Time Series FX (Daily)"`.
- `overview`: flat object with `Symbol, AssetType, Name, Description, CIK, Exchange, Currency, Country, Sector, Industry, MarketCapitalization, EBITDA, PERatio, PEGRatio, BookValue, DividendPerShare, EPS, RevenuePerShareTTM, ProfitMargin, ...` — ~60 fields, all stringified.

## Pitfalls

- **25 calls/day is HARD.** Cache aggressively; budget calls before sequencing. Once exhausted, every call returns a 200 with `Information: "We have detected your API key as ... If you would like to target a higher API call frequency..."`. Detect this string explicitly.
- **All numeric values are strings.** `"4. close": "189.45"` — convert to float.
- **Field names are numbered prefixes.** `"1. open"`, `"05. price"`. Don't try to rename via auto-deserializer; treat keys literally.
- **`outputsize: "compact"` returns 100 days; `"full"` returns 20+ years.** Default is compact. Full responses are large (hundreds of KB).
- **Symbols include exchange suffix for non-US.** `IBM`, `BARC.LON`, `7203.TYO`. Documentation lists supported symbol formats per exchange.
- **`CIK` in `overview`** ties back to `sec_edgar` — use it for cross-source joins on US companies.
- **Adjusted vs unadjusted.** `time_series_daily` returns unadjusted prices on the free tier; adjusted (split/dividend-corrected) is now premium-only. Be careful with long histories around stock splits.
- **`global_quote` change percent has a literal `%` suffix.** `"10. change percent": "1.43%"` — strip the `%` before parsing.
- **5 req/min rate** — sustained burst returns a `Note` field warning of throttling.

## Source links

- API docs: https://www.alphavantage.co/documentation/
- Limits: https://www.alphavantage.co/premium/
- Symbol search: https://www.alphavantage.co/query?function=SYMBOL_SEARCH&...
