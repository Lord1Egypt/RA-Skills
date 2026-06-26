# krx-stock-cli

Zero-config CLI for Korean Exchange (KRX) stock market data. Fetch daily OHLCV, latest-close snapshots, market-cap rankings, index histories (KOSPI/KOSDAQ/KOSPI200/KRX100), and ticker ↔ name lookups for KOSPI / KOSDAQ / KONEX / ETF tickers. No API key required.

Backed by [`FinanceDataReader`](https://github.com/FinanceData/FinanceDataReader).

## Why

Korean quant devs, retail investors, and fintech builders need reliable, scriptable access to KRX data. Existing libraries are Python-only and require boilerplate. This skill wraps the most useful operations in a single CLI with JSON/CSV output, so any agent or shell script can consume KRX data directly.

Pairs well with:

- **opendart-cli** — DART filings & financial statements
- **toss-payments-cli** — Toss Payments API
- **naver-papago-translate** — translate Korean disclosures

## Install

```bash
git clone https://github.com/ChloePark85/krx-stock-cli.git
cd krx-stock-cli
pip install -r scripts/requirements.txt
```

Or via ClawHub:

```bash
clawhub install krx-stock-cli
```

## Quick start

```bash
# Ticker lookup
python scripts/krx.py ticker "삼성전자"
python scripts/krx.py ticker 005930

# OHLCV — last 30 days
python scripts/krx.py ohlcv 005930 --days 30

# Latest-close snapshot
python scripts/krx.py snapshot 005930

# Market-cap top-50 on KOSPI
python scripts/krx.py marketcap --market KOSPI --top 50

# KOSPI index — last 90 days, CSV
python scripts/krx.py index KS11 --days 90 --csv
```

See [`SKILL.md`](./SKILL.md) for the full command reference.

## Index codes

| Code | Name |
| --- | --- |
| KS11 | KOSPI |
| KQ11 | KOSDAQ |
| KS200 | KOSPI 200 |
| KRX100 | KRX 100 |
| IXIC | NASDAQ Composite |
| US500 | S&P 500 |
| N225 | Nikkei 225 |

Run `python scripts/krx.py index-list` for the curated list.

## Output

- Default: pretty-printed JSON (UTF-8, Korean characters preserved).
- `--csv`: Pandas-style CSV to stdout for tabular commands.
- Errors go to stderr as `{"error":"…"}` with a non-zero exit code.

## Rate limits

Public endpoints — keep multi-ticker jobs to ~1 req/sec. On `403`, back off 60 s.

## License

MIT — see [`LICENSE`](./LICENSE).

## Contributing

Issues and PRs welcome. If upstream data formats change, open an issue with the failing command and raw response.
