# Flat Files — Bulk Historical CSV Downloads

For large historical datasets (backtesting, ML). Data available ~11:00 AM ET the following day.
Requires `MASSIVE_S3_ACCESS_KEY` and `MASSIVE_S3_SECRET_KEY` from https://massive.com/dashboard/keys

S3 endpoint: `https://files.massive.com`
Bucket: `flatfiles`

---

## Available Asset Classes & Data Types

| Asset Class | Data Types |
|---|---|
| Stocks | trades, quotes, minute_aggs, day_aggs |
| Options | trades, quotes, minute_aggs, day_aggs |
| Futures | trades, quotes, minute_aggs, day_aggs |
| Indices | minute_aggs, day_aggs |
| Forex | quotes, minute_aggs, day_aggs |
| Crypto | trades, quotes, minute_aggs, day_aggs |

---

## Python Boto3 Download

```python
import boto3
import os

s3 = boto3.client(
    "s3",
    endpoint_url="https://files.massive.com",
    aws_access_key_id=os.environ["MASSIVE_S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MASSIVE_S3_SECRET_KEY"],
)

# List available files for a dataset
response = s3.list_objects_v2(
    Bucket="flatfiles",
    Prefix="stocks/day_aggs/2024/",  # path format: {asset}/{data_type}/{year}/
)
for obj in response["Contents"]:
    print(obj["Key"])

# Download a specific file
s3.download_file(
    Bucket="flatfiles",
    Key="stocks/day_aggs/2024/2024-01-02.csv.gz",
    Filename="2024-01-02.csv.gz",
)
```

---

## CSV Structure (Minute Aggregates example)

```
ticker,volume,open,close,high,low,window_start,transactions
AAPL,4930,200.29,200.5,200.63,200.29,1744792500000000000,129
MSFT,1815,415.39,415.34,415.61,415.34,1744792560000000000,57
```

`window_start` is a Unix nanosecond timestamp.

---

## Path Format

```
{asset_class}/{data_type}/{year}/{YYYY-MM-DD}.csv.gz
```

Examples:
- `stocks/day_aggs/2024/2024-01-02.csv.gz`
- `options/trades/2024/2024-06-21.csv.gz`
- `crypto/minute_aggs/2024/2024-01-02.csv.gz`
