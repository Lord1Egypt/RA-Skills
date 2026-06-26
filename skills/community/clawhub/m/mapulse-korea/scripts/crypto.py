#!/usr/bin/env python3
"""
Mapulse Crypto — Binance + OKX 实时价格
零延迟, 无需API Key
"""

import requests
import re
import time

# 币种别名
CRYPTO_ALIASES = {
    # 英文
    "btc": "BTCUSDT", "bitcoin": "BTCUSDT",
    "eth": "ETHUSDT", "ethereum": "ETHUSDT",
    "sol": "SOLUSDT", "solana": "SOLUSDT",
    "bnb": "BNBUSDT",
    "xrp": "XRPUSDT", "ripple": "XRPUSDT",
    "ada": "ADAUSDT", "cardano": "ADAUSDT",
    "doge": "DOGEUSDT", "dogecoin": "DOGEUSDT",
    "dot": "DOTUSDT", "polkadot": "DOTUSDT",
    "avax": "AVAXUSDT", "avalanche": "AVAXUSDT",
    "matic": "MATICUSDT", "polygon": "MATICUSDT",
    "link": "LINKUSDT", "chainlink": "LINKUSDT",
    "uni": "UNIUSDT", "uniswap": "UNIUSDT",
    "atom": "ATOMUSDT", "cosmos": "ATOMUSDT",
    "near": "NEARUSDT",
    "apt": "APTUSDT", "aptos": "APTUSDT",
    "arb": "ARBUSDT", "arbitrum": "ARBUSDT",
    "op": "OPUSDT", "optimism": "OPUSDT",
    "sui": "SUIUSDT",
    "ton": "TONUSDT", "toncoin": "TONUSDT",
    "map": "MAPUSDT", "mapo": "MAPUSDT",
    "pepe": "PEPEUSDT",
    "wld": "WLDUSDT", "worldcoin": "WLDUSDT",
    "sei": "SEIUSDT",
    "tia": "TIAUSDT", "celestia": "TIAUSDT",
    "jup": "JUPUSDT", "jupiter": "JUPUSDT",
    # 韩文
    "비트코인": "BTCUSDT", "비트": "BTCUSDT",
    "이더리움": "ETHUSDT", "이더": "ETHUSDT",
    "솔라나": "SOLUSDT", "리플": "XRPUSDT",
    "도지": "DOGEUSDT", "도지코인": "DOGEUSDT",
    "에이다": "ADAUSDT", "폴리곤": "MATICUSDT",
    "아발란체": "AVAXUSDT", "체인링크": "LINKUSDT",
    "톤코인": "TONUSDT",
    # 中文
    "比特币": "BTCUSDT", "以太坊": "ETHUSDT",
    "瑞波": "XRPUSDT", "狗狗币": "DOGEUSDT",
    "索拉纳": "SOLUSDT",
}

# Binance symbol → OKX instId 변환
def _to_okx(symbol):
    # BTCUSDT → BTC-USDT
    return symbol.replace("USDT", "-USDT")


def resolve_crypto(text):
    """텍스트에서 암호화폐 심볼 추출"""
    t = text.lower().strip()

    # 직접 심볼 (BTCUSDT)
    if re.match(r'^[A-Z]{2,10}USDT$', text.upper()):
        return text.upper()

    # 별명
    for alias, symbol in CRYPTO_ALIASES.items():
        if alias in t:
            return symbol

    return None


def is_crypto_query(text):
    """암호화폐 관련 질문인지"""
    t = text.lower()
    if any(w in t for w in ["코인", "crypto", "币", "coin", "token", "토큰"]):
        return True
    return resolve_crypto(text) is not None


def fetch_price(symbol):
    """Binance + OKX 실시간 가격"""
    result = {"symbol": symbol, "base": symbol.replace("USDT", "")}

    # Binance 24hr
    try:
        r = requests.get(
            f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}",
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()
            result["binance"] = {
                "price": float(d["lastPrice"]),
                "high": float(d["highPrice"]),
                "low": float(d["lowPrice"]),
                "volume": float(d["volume"]),
                "change": float(d["priceChange"]),
                "change_pct": float(d["priceChangePercent"]),
            }
    except:
        pass

    # OKX
    try:
        okx_id = _to_okx(symbol)
        r = requests.get(
            f"https://www.okx.com/api/v5/market/ticker?instId={okx_id}",
            timeout=5
        )
        if r.status_code == 200:
            d = r.json()["data"][0]
            result["okx"] = {
                "price": float(d["last"]),
                "high": float(d["high24h"]),
                "low": float(d["low24h"]),
                "volume": float(d["vol24h"]),
                "change": float(d["last"]) - float(d["open24h"]),
                "change_pct": ((float(d["last"]) / float(d["open24h"])) - 1) * 100,
            }
    except:
        pass

    return result


def format_price(data, lang="ko"):
    """가격 포맷"""
    base = data.get("base", "?")
    bn = data.get("binance")
    ox = data.get("okx")

    if not bn and not ox:
        return f"❌ {base} 가격을 가져올 수 없습니다."

    # 대표 가격
    price = bn["price"] if bn else ox["price"]
    change_pct = bn["change_pct"] if bn else ox["change_pct"]
    arrow = "🟢" if change_pct > 0 else "🔴" if change_pct < 0 else "⚪"

    # 가격 포맷 (소수점 자동)
    if price >= 100:
        price_str = f"${price:,.2f}"
    elif price >= 1:
        price_str = f"${price:,.4f}"
    else:
        price_str = f"${price:,.8f}"

    lines = [
        f"{arrow} *{base}/USDT*",
        "",
    ]

    # 양쪽 거래소
    if bn:
        lines.append(f"*Binance:* ${bn['price']:,.2f}" if bn['price'] >= 1 else f"*Binance:* ${bn['price']:,.8f}")
    if ox:
        lines.append(f"*OKX:*        ${ox['price']:,.2f}" if ox['price'] >= 1 else f"*OKX:*        ${ox['price']:,.8f}")

    lines.append("")

    # 상세
    p = bn or ox
    lines.extend([
        f"📈 24h 변동: {p['change']:+,.2f} ({p['change_pct']:+.2f}%)",
        f"📊 24h 고가: ${p['high']:,.2f}" if p['high'] >= 1 else f"📊 24h 고가: ${p['high']:,.8f}",
        f"📉 24h 저가: ${p['low']:,.2f}" if p['low'] >= 1 else f"📉 24h 저가: ${p['low']:,.8f}",
        f"📦 24h 거래량: {p['volume']:,.2f} {base}",
    ])

    # 차이
    if bn and ox:
        spread = abs(bn["price"] - ox["price"])
        spread_pct = (spread / bn["price"]) * 100
        if spread_pct > 0.05:
            lines.append(f"\n⚡ 거래소 차이: ${spread:,.2f} ({spread_pct:.3f}%)")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "BTC"
    symbol = resolve_crypto(query)
    if symbol:
        data = fetch_price(symbol)
        print(format_price(data))
    else:
        print(f"❌ '{query}' 인식 불가")
