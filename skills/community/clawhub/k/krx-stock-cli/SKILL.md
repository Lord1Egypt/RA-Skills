---
name: krx-stock-cli
description: Korean Exchange (KRX) stock market data CLI. Fetch daily OHLCV, latest-close snapshots, market-cap rankings, index histories (KOSPI/KOSDAQ/KOSPI200/KRX100), and ticker↔name lookups for KOSPI/KOSDAQ/KONEX/ETF tickers. Use when a user asks for Korean stock prices, ticker resolution, or KRX market data in JSON or CSV. No API key required.
license: MIT
---

# KRX Stock CLI

Zero-config CLI for Korean Exchange (KRX) market data: daily OHLCV, latest-close snapshots, market-cap rankings, index histories, and ticker lookups for KOSPI / KOSDAQ / KONEX / ETF tickers.

Backed by [`FinanceDataReader`](https://github.com/FinanceData/FinanceDataReader), which aggregates KRX, Naver Finance, and related public sources. No API key required.

## When to use

Trigger on:

- Korean stock price / OHLCV requests ("삼성전자 주가", "005930 price history")
- Market-cap ranking / latest close snapshots
- Index series (KOSPI, KOSDAQ, KOSPI 200, KRX 100)
- Ticker ↔ company-name resolution
- Company name substring search
- Global-index tagalong queries (S&P 500, Nasdaq, Nikkei, Shanghai)

Do **not** use for:

- Corporate filings / disclosures → use `opendart-cli`
- Fundamentals per day (PER/PBR/EPS) — not exposed; use DART financial statements instead
- Real-time ticks / order book (data is EOD; today's bar is available after market close)

## Install

```bash
pip install -r scripts/requirements.txt
```

Dependencies: `finance-datareader`, `pandas`.

## Usage

All commands are sub-commands of `scripts/krx.py`. JSON by default; pass `--csv` for CSV to stdout.

Dates accept either `YYYYMMDD` or `YYYY-MM-DD`.

### Ticker lookup

```bash
python scripts/krx.py ticker 005930            # → 삼성전자
python scripts/krx.py ticker "SK하이닉스"       # → 000660
python scripts/krx.py search 카카오 --top 5     # substring search
```

### OHLCV

```bash
python scripts/krx.py ohlcv 005930 --days 30
python scripts/krx.py ohlcv 005930 --start 20260101 --end 20260420 --csv
```

### Latest-close snapshot

```bash
python scripts/krx.py snapshot 005930
```

### Market-cap ranking

```bash
python scripts/krx.py marketcap --market KRX --top 50
python scripts/krx.py marketcap --market KOSDAQ --top 20 --csv
```

`--market` accepts `KRX`, `KOSPI`, `KOSDAQ`, `KONEX`, `ETF/KR`.

### List all tickers in a market

```bash
python scripts/krx.py list --market KOSPI --top 100
```

### Index

```bash
python scripts/krx.py index KS11 --days 90       # KOSPI
python scripts/krx.py index KS200 --days 30      # KOSPI 200
python scripts/krx.py index IXIC --days 30       # NASDAQ Composite
python scripts/krx.py index-list                 # common codes
```

Common codes: `KS11` KOSPI · `KQ11` KOSDAQ · `KS200` KOSPI 200 · `KRX100` KRX 100 · `DJI` Dow · `IXIC` Nasdaq · `US500` S&P 500 · `N225` Nikkei 225 · `SSEC` Shanghai.

## Output format

- **JSON** (default): array of records, UTF-8, Korean preserved, dates as `YYYY-MM-DD`.
- **CSV** (`--csv`): Pandas-compatible; date is the first column on time-series output.

## Error handling

- Invalid ticker → exit code `2`, `{"error":"ticker_not_found","input":"…"}` on stderr.
- Upstream error (network, schema drift) → exit code `3`, `{"error":"upstream_error",…}` on stderr.
- Empty date range (weekend / holiday) → empty array, exit code `0`.

## Rate limits

Public endpoints — keep multi-ticker jobs to ~1 req/sec and back off on `403`.

## See also

- `opendart-cli` — DART filings & financial statements
- `toss-payments-cli` — Toss Payments API
- `naver-papago-translate` — translate Korean disclosures

## License

MIT. No warranty on data accuracy — always verify against the official KRX disclosure before trading.
