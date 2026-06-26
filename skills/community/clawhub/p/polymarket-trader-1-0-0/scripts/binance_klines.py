"""Fetch Binance klines and print JSON.

Examples:
  python binance_klines.py --symbol ETHUSDT --interval 1m --limit 60
  python binance_klines.py --symbol BTCUSDT --interval 1h --limit 1
"""

import argparse
import json
import sys
from urllib.parse import urlencode
import urllib.request

BASE = "https://api.binance.com"


def fetch(path: str, params: dict) -> list:
    url = f"{BASE}{path}?{urlencode(params)}"
    with urllib.request.urlopen(url, timeout=20) as r:
        data = r.read().decode("utf-8")
    return json.loads(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTCUSDT", help="분석할 심볼 (예: ETHUSDT)")
    ap.add_argument("--interval", default="1m")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--startTime", type=int, default=None)
    args = ap.parse_args()

    params = {"symbol": args.symbol, "interval": args.interval, "limit": args.limit}
    if args.startTime is not None:
        params["startTime"] = int(args.startTime)

    data = fetch("/api/v3/klines", params)
    sys.stdout.write(json.dumps(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
