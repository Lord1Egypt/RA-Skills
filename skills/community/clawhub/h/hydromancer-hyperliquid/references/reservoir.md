# Reservoir: historical Hyperliquid data on S3

Archive of Hyperliquid exchange data, stored as Parquet in `s3://hydromancer-reservoir` (region `ap-northeast-1`). No Hydromancer API key is needed. The bucket is **requester-pays**: the data is free, but AWS bills your account for requests and transfer, so you need AWS credentials.

Docs: https://docs.hydromancer.xyz/reservoir · schemas: [fills](https://docs.hydromancer.xyz/reservoir/schema-reference/fills), [candles](https://docs.hydromancer.xyz/reservoir/schema-reference/candles), [snapshots](https://docs.hydromancer.xyz/reservoir/schema-reference/snapshots), [orderbook](https://docs.hydromancer.xyz/reservoir/schema-reference/orderbook)

## Datasets (Hyperliquid core markets)

| Dataset | Path |
|---|---|
| All perp fills | `by_dex/hyperliquid/fills/perp/all/date=YYYY-MM-DD/` |
| Liquidations | `by_dex/hyperliquid/fills/perp/liquidations/date=YYYY-MM-DD/` |
| ADL | `by_dex/hyperliquid/fills/perp/adl/date=YYYY-MM-DD/` |
| Builder fills | `by_dex/hyperliquid/fills/perp/builder_fills/date=YYYY-MM-DD/` |
| TWAP fills | `by_dex/hyperliquid/fills/perp/twap_fills/date=YYYY-MM-DD/` |
| Spot fills | `global/fills/spot/all/date=YYYY-MM-DD/` |
| 1-second candles | `by_dex/hyperliquid/candles/1s/date=YYYY-MM-DD/` |
| Perp position snapshots (daily) | `by_dex/hyperliquid/snapshots/perp/date=YYYY-MM-DD/` |
| Spot holdings snapshots (daily) | `global/snapshots/spot/date=YYYY-MM-DD/` |
| Account values (daily) | `global/snapshots/account_values/date=YYYY-MM-DD/` |
| L2 order book, 20 levels, 1-minute | `by_dex/hyperliquid/orderbook/1m/{asset_class}/date=YYYY-MM-DD/{coin}.parquet` (see the orderbook schema page for `asset_class` values) |

HIP-3 DEXs have their own folders under `by_dex/<dex>/`; see the per-DEX pages in the docs. HIP-3 coins keep the `dex:` prefix inside fills, candles and snapshots (`coin = 'xyz:AAPL'`, `market = 'xyz:AAPL'`); only order-book file names drop it (`by_dex/xyz/orderbook/1m/perps/date=…/AAPL.parquet`). Sub-datasets (liquidations, ADL…) only have files for dates with events. Check the docs for current coverage dates before assuming a range exists.

## Access

AWS CLI (always pass `--request-payer requester`):

```bash
aws s3 ls s3://hydromancer-reservoir/by_dex/ --request-payer requester
aws s3 cp s3://hydromancer-reservoir/by_dex/hyperliquid/fills/perp/liquidations/date=2026-10-18/fills.parquet \
  ./liquidations-2026-10-18.parquet --request-payer requester
```

DuckDB reads only the columns and row groups a query needs. It needs `duckdb` and `pytz` (tested versions pinned in `requirements.txt`); without `pytz`, Python fetches of timestamp columns fail with `No module named 'pytz'`.

Connect by exporting your active AWS CLI session into environment variables. A plain `PROVIDER credential_chain` secret fails with `aws login` sessions (`Secret Validation Failure … Credential Chain: 'config'`), and every query after it returns 403:

```python
import json, os, subprocess, duckdb

creds = json.loads(subprocess.check_output(
    ["aws", "configure", "export-credentials", "--format", "process"], text=True))
for src, dst in [("AccessKeyId", "AWS_ACCESS_KEY_ID"),
                 ("SecretAccessKey", "AWS_SECRET_ACCESS_KEY"),
                 ("SessionToken", "AWS_SESSION_TOKEN")]:
    if creds.get(src):
        os.environ[dst] = creds[src]   # in memory only; never print or save these

con = duckdb.connect()
con.execute("SET TimeZone = 'UTC';")
con.execute("""CREATE SECRET (TYPE s3, PROVIDER credential_chain, CHAIN 'env',
               REGION 'ap-northeast-1');
               SET s3_requester_pays = true;""")
```

Then run queries with `con.execute(sql).fetchall()`:

```sql

-- BTC fills for one day
SELECT timestamp, side, price, size, direction, address
FROM read_parquet('s3://hydromancer-reservoir/by_dex/hyperliquid/fills/perp/all/date=2026-03-22/fills.parquet')
WHERE coin = 'BTC'
ORDER BY timestamp;

-- 1-minute candles built from 1-second candles
SELECT time_bucket(INTERVAL '1 minute', timestamp) AS minute,
       first(open) AS open, max(high) AS high, min(low) AS low, last(close) AS close,
       sum(volume) AS volume, sum(trade_count) AS trades
FROM read_parquet('s3://hydromancer-reservoir/by_dex/hyperliquid/candles/1s/date=2026-03-22/candles.parquet')
WHERE coin = 'BTC'
GROUP BY minute ORDER BY minute;

-- Largest BTC positions in a daily snapshot
SELECT user, size, notional, entry_price, leverage, leverage_type
FROM read_parquet('s3://hydromancer-reservoir/by_dex/hyperliquid/snapshots/perp/date=2026-03-22/*.parquet')
WHERE market = 'BTC'
ORDER BY abs(size) DESC LIMIT 10;
```

Tested on DuckDB 1.4.5 with this setup, using both a root `aws login` session and a read-only IAM user signed in with `aws login`: all three queries return data. Without `s3_requester_pays = true` you get HTTP 403; with a region other than `ap-northeast-1`, HTTP 301.

## Cost control

- A wildcard path reads (and bills) every file it matches. Keep date ranges tight and select only needed columns.
- A daily snapshot isn't necessarily the daily close; the file name gives the block and time.
- Prefer `aws s3 sync` with `--include` patterns over repeated full scans when you need many days locally.
