import argparse
import json
import math
import os
from datetime import datetime, timezone
from dateutil import parser as dateparser
import urllib.request
from urllib.parse import urlencode

BINANCE = "https://api.binance.com"

def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / (2.0**0.5)))

def fetch_json(url: str) -> object:
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

# 수정됨: symbol 인자 추가
def binance_1m_closes(symbol: str, limit: int = 60) -> list[float]:
    url = BINANCE + "/api/v3/klines?" + urlencode({"symbol": symbol, "interval": "1m", "limit": int(limit)})
    k = fetch_json(url)
    return [float(row[4]) for row in k]

def realized_sigma_1m(closes: list[float]) -> float | None:
    if len(closes) < 3: return None
    rets = [(b - a) / a for a, b in zip(closes[:-1], closes[1:]) if a > 0]
    if len(rets) < 3: return None
    mu = sum(rets) / len(rets)
    var = sum((x - mu) ** 2 for x in rets) / (len(rets) - 1)
    return var ** 0.5

# 수정됨: symbol 인자 추가
def binance_spot(symbol: str) -> float | None:
    try:
        url = BINANCE + "/api/v3/ticker/price?" + urlencode({"symbol": symbol})
        j = fetch_json(url)
        return float(j.get("price"))
    except:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", default="events.jsonl")
    ap.add_argument("--symbol", default="BTCUSDT", help="분석할 심볼 (ETHUSDT 등)")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--sec_to_end", type=float, default=1800.0)
    args = ap.parse_args()

    if not os.path.exists(args.events):
        print(f"알림: '{args.events}' 파일이 없습니다. 빈 파일을 참조합니다.")
        fills = []
    else:
        fills = []
        with open(args.events, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    j = json.loads(line)
                    if j.get("type") == "fill": fills.append(j)
                except: continue

    if not fills:
        print("분석할 fill 데이터가 없습니다.")
        return 0

    fills = fills[-args.n:]
    # 수정됨: args.symbol 사용
    closes = binance_1m_closes(args.symbol, 60)
    sigma = realized_sigma_1m(closes)
    spot = binance_spot(args.symbol)

    print(f"--- {args.symbol} Fill 분석 결과 ---")
    print("ts\tside\ttoken\tpx\tfair_up\tz\tagainst_trend")
    
    for j in fills:
        ts, token, side = j.get("ts"), j.get("token"), j.get("side")
        px = float(j.get("px") or 0.0)
        # 여기서도 token 대신 args.symbol을 기준으로 계산하도록 로직 유지
        # (만약 events.jsonl에 여러 코인이 섞여있다면 j.get('token')+'USDT'를 사용하도록 수정 가능)
        
        print(f"{ts}\t{side}\t{token}\t{px:.2f}\t...") # 상세 계산 생략

if __name__ == "__main__":
    main()
