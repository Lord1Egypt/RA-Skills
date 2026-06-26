"""Compute simple regime/stabilization metrics from Binance 1m closes.

Outputs ret5/ret15/slope10 and a stabilized boolean.
"""

import argparse
import json
import math
import urllib.request
from urllib.parse import urlencode

BASE = "https://api.binance.com"


def fetch_klines(symbol: str, interval: str, limit: int) -> list:
    url = f"{BASE}/api/v3/klines?" + urlencode({"symbol": symbol, "interval": interval, "limit": limit})
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def closes_from_klines(k: list) -> list[float]:
    return [float(row[4]) for row in k]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTCUSDT", help="분석할 심볼 (예: ETHUSDT)")
    ap.add_argument("--minutes", type=int, default=60)
    args = ap.parse_args()

    # 데이터 가져오기
    k = fetch_klines(args.symbol, "1m", args.minutes)
    c = closes_from_klines(k)
    
    if len(c) < 32:
        print(json.dumps({"ok": False, "reason": "not_enough_data", "n": len(c)}))
        return 1

    ret5 = c[-1] / c[-6] - 1.0
    ret15 = c[-1] / c[-16] - 1.0
    slope10 = c[-1] - c[-11]
    
    last15_low = min(c[-16:])
    prev15_low = min(c[-31:-15])
    
    # 이더리움 등 다른 코인에서도 작동하는 범용 안정화 지표
    stabilized = (ret5 > 0) and (ret15 > 0) and (c[-1] > last15_low)
    
    result = {
        "symbol": args.symbol,
        "last": c[-1],
        "ret5": ret5,
        "ret15": ret15,
        "slope10": slope10,
        "stabilized": stabilized
    }
    
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
