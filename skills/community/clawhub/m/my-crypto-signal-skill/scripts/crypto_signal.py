#!/usr/bin/env python3
"""
crypto_signal.py — Crypto signal pipeline, all-in-one.

Usage:
  python3 crypto_signal.py run     BTCUSDT          # full pipeline (recommended)
  python3 crypto_signal.py fetch   BTCUSDT          # fetch market data only
  python3 crypto_signal.py news    BTCUSDT          # fetch news only
  python3 crypto_signal.py signal  BTCUSDT          # generate signal (auto-fetches if needed)
  python3 crypto_signal.py verify  signals/xxx.json # verify a pending signal
  python3 crypto_signal.py report                   # knowledge base summary
  python3 crypto_signal.py schedule BTCUSDT         # run adaptive news scheduler (loop)

All paths are resolved relative to this file's location — run from any directory.
Credentials: ~/.openclaw/credentials/crypto-signal.json  or env vars (see below).
"""

import json
import os
import sys
import time
import uuid
import argparse
import urllib.request
import urllib.parse
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Path anchoring: all persistent data lives next to this script ─
_HERE    = Path(__file__).resolve().parent
_ROOT    = _HERE.parent                          # skill root
_DATA    = _ROOT / "data"
_SIGNALS = _ROOT / "signals"
_RECORDS = _ROOT / "records"

BINANCE_BASE     = "https://api.binance.com/api/v3"
CRYPTOPANIC_BASE = "https://cryptopanic.com/api/v1/posts/"
NEWSAPI_BASE     = "https://newsapi.org/v2/everything"

# ════════════════════════════════════════════════════════════════════
#  CREDENTIALS & PROXY
# ════════════════════════════════════════════════════════════════════

_CREDENTIALS_PATH = Path.home() / ".openclaw" / "credentials" / "crypto-signal.json"

_CREDS_TEMPLATE = {
    "News_apiKey": "YOUR_NEWSAPI_KEY",
    "CP_apiKey":   "YOUR_CRYPTOPANIC_KEY",
    "Bian_apiKey": "YOUR_BINANCE_API_KEY",
    "proxy":       "",
}

_ENV_MAP = {
    "News_apiKey": "NEWSAPI_KEY",
    "CP_apiKey":   "CRYPTOPANIC_KEY",
    "Bian_apiKey": "BINANCE_API_KEY",
}

_creds_cache: dict | None = None
_opener_cache: urllib.request.OpenerDirector | None = None


def _load_creds() -> dict:
    global _creds_cache
    if _creds_cache is not None:
        return _creds_cache

    # 1. Try env vars first
    from_env = {k: os.environ[v] for k, v in _ENV_MAP.items() if v in os.environ}
    if "News_apiKey" in from_env:
        _creds_cache = from_env
        return _creds_cache

    # 2. Fall back to credentials file
    if not _CREDENTIALS_PATH.exists():
        _CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CREDENTIALS_PATH.write_text(json.dumps(_CREDS_TEMPLATE, indent=2))
        _CREDENTIALS_PATH.chmod(0o600)
        _die(
            f"Credentials file not found — template created at:\n"
            f"  {_CREDENTIALS_PATH}\n\n"
            f"Option A (recommended) — set env vars:\n"
            f"  export NEWSAPI_KEY=your_key\n"
            f"  export HTTPS_PROXY=http://127.0.0.1:7890   # if behind proxy\n\n"
            f"Option B — fill in the file above, then re-run."
        )

    creds = json.loads(_CREDENTIALS_PATH.read_text())
    if creds.get("News_apiKey", "").startswith("YOUR_"):
        _die(f"News_apiKey is required. Edit {_CREDENTIALS_PATH} or set NEWSAPI_KEY env var.")

    _creds_cache = creds
    return _creds_cache


def _resolve_proxy() -> str | None:
    """Read proxy from env vars first, then credentials file. Never raises."""
    # 1. env vars (standard)
    proxy = (
        os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or
        os.environ.get("HTTP_PROXY")  or os.environ.get("http_proxy")
    )
    if proxy:
        return proxy
    # 2. credentials file (optional field)
    try:
        creds = _load_creds()
        return creds.get("proxy", "").strip() or None
    except SystemExit:
        return None


def _get_opener() -> urllib.request.OpenerDirector:
    global _opener_cache
    if _opener_cache is not None:
        return _opener_cache

    proxy = _resolve_proxy()
    if proxy:
        handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        _opener_cache = urllib.request.build_opener(handler)
    else:
        _opener_cache = urllib.request.build_opener()

    return _opener_cache


def _get(url: str, headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "crypto-signal/1.0"})
    with _get_opener().open(req, timeout=15) as r:
        return r.read()


def _die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


# ════════════════════════════════════════════════════════════════════
#  FETCH — Binance market data + indicators
# ════════════════════════════════════════════════════════════════════

def _sma(closes, period):
    return sum(closes[-period:]) / period if len(closes) >= period else None

def _ema(closes, period):
    if len(closes) < period:
        return None
    k = 2 / (period + 1)
    val = sum(closes[:period]) / period
    for p in closes[period:]:
        val = p * k + val * (1 - k)
    return val

def _rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    deltas = [closes[i+1] - closes[i] for i in range(len(closes) - 1)]
    gains  = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_g  = sum(gains) / period
    avg_l  = sum(losses) / period
    if avg_l == 0:
        return 100.0
    return round(100 - 100 / (1 + avg_g / avg_l), 2)

def _macd(closes):
    e12, e26 = _ema(closes, 12), _ema(closes, 26)
    if e12 is None or e26 is None:
        return None
    return round(e12 - e26, 4)

def _patterns(klines):
    p, c = [], klines
    if len(c) < 3:
        return p
    if (c[-2]["close"] < c[-2]["open"] and c[-1]["close"] > c[-1]["open"] and
            c[-1]["close"] > c[-2]["open"] and c[-1]["open"] < c[-2]["close"]):
        p.append("bullish_engulfing")
    if (c[-2]["close"] > c[-2]["open"] and c[-1]["close"] < c[-1]["open"] and
            c[-1]["close"] < c[-2]["open"] and c[-1]["open"] > c[-2]["close"]):
        p.append("bearish_engulfing")
    body = abs(c[-1]["close"] - c[-1]["open"])
    rng  = c[-1]["high"] - c[-1]["low"]
    if rng > 0 and body / rng < 0.1:
        p.append("doji")
    if len(c) >= 5:
        highs = [k["high"] for k in c[-5:]]
        lows  = [k["low"]  for k in c[-5:]]
        if all(highs[i] < highs[i+1] for i in range(4)): p.append("higher_highs")
        if all(lows[i]  > lows[i+1]  for i in range(4)): p.append("lower_lows")
    return p


TIMEFRAMES = ["3m", "15m", "30m", "1h"]   # micro → macro


def _fetch_one_timeframe(symbol: str, interval: str, limit: int = 100) -> dict:
    """Fetch klines + compute indicators for a single interval."""
    raw = json.loads(_get(
        f"{BINANCE_BASE}/klines?symbol={symbol}&interval={interval}&limit={limit}"
    ))
    klines = [
        {"time":   datetime.fromtimestamp(k[0] / 1000).strftime("%Y-%m-%d %H:%M"),
         "open":   float(k[1]), "high": float(k[2]),
         "low":    float(k[3]), "close": float(k[4]), "volume": float(k[5])}
        for k in raw
    ]
    closes = [k["close"] for k in klines]
    return {
        "interval":   interval,
        "indicators": {
            "rsi_14": _rsi(closes),
            "ma_20":  round(_sma(closes, 20), 4) if _sma(closes, 20) else None,
            "ma_50":  round(_sma(closes, 50), 4) if _sma(closes, 50) else None,
            "ema_12": round(_ema(closes, 12), 4) if _ema(closes, 12) else None,
            "ema_26": round(_ema(closes, 26), 4) if _ema(closes, 26) else None,
            "macd":   _macd(closes),
        },
        "patterns": _patterns(klines),
    }


def cmd_fetch(symbol: str, interval: str | None = None, limit: int = 100,
              output: Path | None = None) -> dict:
    """Fetch all 4 timeframes (3m/15m/30m/1h) in one call.
    If interval is set, only fetch that single timeframe (for manual use).
    """
    intervals = [interval] if interval else TIMEFRAMES

    raw_ticker = json.loads(_get(f"{BINANCE_BASE}/ticker/24hr?symbol={symbol}"))
    ticker = {
        "price":      float(raw_ticker["lastPrice"]),
        "change_pct": float(raw_ticker["priceChangePercent"]),
        "high_24h":   float(raw_ticker["highPrice"]),
        "low_24h":    float(raw_ticker["lowPrice"]),
        "volume_24h": float(raw_ticker["volume"]),
    }

    timeframes = {}
    for iv in intervals:
        timeframes[iv] = _fetch_one_timeframe(symbol, iv, limit)

    result = {
        "symbol":     symbol,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ticker":     ticker,
        "timeframes": timeframes,
    }

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2))

    return result


# ════════════════════════════════════════════════════════════════════
#  NEWS — CryptoPanic + NewsAPI sentiment
# ════════════════════════════════════════════════════════════════════

EXTREME_NEGATIVE = [
    "ban", "banned", "illegal", "crackdown", "sec charges", "doj indictment",
    "exchange hack", "exchange insolvent", "exchange collapse", "exit scam",
    "nonfarm payrolls miss", "cpi surge", "inflation spike",
    "emergency rate hike", "bank failure", "systemic risk",
    "war escalation", "sanctions", "nuclear threat",
]
EXTREME_POSITIVE = [
    "etf approved", "legal tender", "strategic bitcoin reserve",
    "rate cut surprise", "nation adopts bitcoin",
    "sec approves", "fed pivot", "quantitative easing",
]
MACRO_BEARISH = [
    "rate hike", "hawkish", "inflation", "recession", "layoffs",
    "gdp miss", "bank run", "credit crunch", "tightening",
    "regulatory crackdown", "tax crypto", "delist",
]
MACRO_BULLISH = [
    "rate cut", "dovish", "fed pivot", "stimulus", "easing",
    "gdp beat", "employment strong", "institutional adoption",
    "etf inflow", "bitcoin reserve", "macro tailwind",
]


def _base_currency(symbol: str) -> str:
    for quote in ("USDT", "BUSD", "BTC", "ETH", "BNB"):
        if symbol.endswith(quote) and len(symbol) > len(quote):
            return symbol[:-len(quote)]
    return symbol


def _fetch_cryptopanic(symbol: str, api_key: str = "") -> list[dict]:
    params = {"currencies": _base_currency(symbol), "filter": "hot", "public": "true"}
    if api_key and not api_key.startswith("YOUR_"):
        params["auth_token"] = api_key
    url = f"{CRYPTOPANIC_BASE}?{urllib.parse.urlencode(params)}"
    try:
        data = json.loads(_get(url))
        return [
            {"title": p.get("title", ""), "source": p.get("source", {}).get("title", ""),
             "url": p.get("url", ""),
             "votes": {"positive": p.get("votes", {}).get("positive", 0),
                       "negative": p.get("votes", {}).get("negative", 0)}}
            for p in data.get("results", [])[:10]
        ]
    except Exception as e:
        print(f"CryptoPanic error: {e}")
        return []


def _score_cryptopanic(news: list[dict]) -> dict:
    pos   = sum(n["votes"]["positive"] for n in news)
    neg   = sum(n["votes"]["negative"] for n in news)
    total = pos + neg
    if total == 0:
        return {"score": 0, "sentiment": "neutral", "pos": 0, "neg": 0, "ratio": 0}
    ratio = (pos - neg) / total
    score = +1 if ratio > 0.4 else (-1 if ratio < -0.4 else 0)
    return {"score": score,
            "sentiment": "bullish" if score > 0 else ("bearish" if score < 0 else "neutral"),
            "pos": pos, "neg": neg, "ratio": round(ratio, 3)}


def _fetch_newsapi(symbol: str, api_key: str) -> list[dict]:
    currency = _base_currency(symbol)
    query    = f"({currency} OR bitcoin OR crypto) AND (Fed OR inflation OR regulation OR CPI OR economy)"
    from_dt  = (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S")
    params   = {"q": query, "from": from_dt, "sortBy": "publishedAt",
                "pageSize": "20", "apiKey": api_key, "language": "en"}
    url = f"{NEWSAPI_BASE}?{urllib.parse.urlencode(params)}"
    try:
        data = json.loads(_get(url))
        return [
            {"title": a.get("title", ""), "source": a.get("source", {}).get("name", ""),
             "url": a.get("url", ""), "published": a.get("publishedAt", ""),
             "description": a.get("description", "")}
            for a in data.get("articles", [])[:10] if a.get("title")
        ]
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []


def _score_newsapi(articles: list[dict]) -> dict:
    combined  = " ".join((a["title"] + " " + a.get("description", "")).lower() for a in articles)
    bull_hits = [kw for kw in MACRO_BULLISH if kw in combined]
    bear_hits = [kw for kw in MACRO_BEARISH if kw in combined]
    net       = len(bull_hits) - len(bear_hits)
    if net >= 2:   score, sent = +2, "strongly bullish"
    elif net == 1: score, sent = +1, "mildly bullish"
    elif net == -1:score, sent = -1, "mildly bearish"
    elif net <= -2:score, sent = -2, "strongly bearish"
    else:          score, sent = 0,  "neutral"
    return {"score": score, "sentiment": sent,
            "bullish_kw": bull_hits, "bearish_kw": bear_hits,
            "article_count": len(articles)}


def _check_extreme(headlines: list[str]) -> dict | None:
    combined = " ".join(headlines).lower()
    for kw in EXTREME_NEGATIVE:
        if kw in combined:
            return {"override": "BLOCK", "direction": "SELL",
                    "reason": f"Extreme negative: '{kw}'", "keyword": kw}
    for kw in EXTREME_POSITIVE:
        if kw in combined:
            return {"override": "BOOST", "direction": "BUY",
                    "reason": f"Extreme positive: '{kw}'", "keyword": kw}
    return None


def cmd_news(symbol: str, output: Path | None = None) -> dict:
    creds     = _load_creds()
    cp_news   = _fetch_cryptopanic(symbol, creds.get("CP_apiKey", ""))
    na_news   = _fetch_newsapi(symbol, creds["News_apiKey"])
    cp_score  = _score_cryptopanic(cp_news)
    na_score  = _score_newsapi(na_news)
    extreme   = _check_extreme([n["title"] for n in cp_news + na_news])

    if extreme:
        sentiment_score = -2 if extreme["direction"] == "SELL" else +2
    else:
        sentiment_score = max(-2, min(2, cp_score["score"] + na_score["score"]))

    result = {
        "symbol": symbol, "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cryptopanic": {"score": cp_score},
        "newsapi":     {"score": na_score},
        "extreme_override": extreme, "sentiment_score": sentiment_score,
    }

    if extreme:
        print(f"extreme_override={extreme['direction']} reason={extreme['reason']}")
    print(f"sentiment_score={sentiment_score:+d}")

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    return result


# ════════════════════════════════════════════════════════════════════
#  SIGNAL — scoring + BUY/SELL/HOLD decision
# ════════════════════════════════════════════════════════════════════

def _score_indicators(ind: dict, patterns: list[str]) -> dict:
    votes = {}
    rsi_v = ind.get("rsi_14")
    if rsi_v is not None:
        if rsi_v < 30:   votes["rsi"] = {"vote": +1, "reason": f"RSI={rsi_v} oversold → bullish"}
        elif rsi_v > 70: votes["rsi"] = {"vote": -1, "reason": f"RSI={rsi_v} overbought → bearish"}
        else:            votes["rsi"] = {"vote":  0, "reason": f"RSI={rsi_v} neutral"}

    ma20, ma50, price = ind.get("ma_20"), ind.get("ma_50"), ind.get("_price")
    if ma20 and ma50 and price:
        if price > ma20 > ma50:   votes["ma_cross"] = {"vote": +1, "reason": "Price > MA20 > MA50 → uptrend"}
        elif price < ma20 < ma50: votes["ma_cross"] = {"vote": -1, "reason": "Price < MA20 < MA50 → downtrend"}
        else:                     votes["ma_cross"] = {"vote":  0, "reason": "MA alignment neutral"}

    macd_v = ind.get("macd")
    if macd_v is not None:
        votes["macd"] = {"vote": +1 if macd_v > 0 else -1,
                         "reason": f"MACD={macd_v:.6f} {'positive' if macd_v > 0 else 'negative'} momentum"}

    pattern_map = {
        "bullish_engulfing": (+1, "Bullish engulfing"),
        "bearish_engulfing": (-1, "Bearish engulfing"),
        "higher_highs":      (+1, "Higher highs structure"),
        "lower_lows":        (-1, "Lower lows structure"),
        "doji":              ( 0, "Doji — indecision"),
    }
    for pt in patterns:
        if pt in pattern_map:
            v, reason = pattern_map[pt]
            votes[f"pattern_{pt}"] = {"vote": v, "reason": reason}

    return {"votes": votes, "total_score": sum(v["vote"] for v in votes.values())}


def _apply_news_layer(tech_score: int, news: dict | None) -> dict:
    if news is None:
        return {"final_score": tech_score, "news_applied": False,
                "override": None, "news_summary": "No news — technical only."}

    extreme = news.get("extreme_override")
    if extreme:
        forced = -3 if extreme["direction"] == "SELL" else +3
        return {"final_score": forced, "news_applied": True, "override": extreme,
                "news_summary": f"EXTREME_OVERRIDE: {extreme['reason']}"}

    sentiment = news.get("sentiment_score")
    if sentiment is None:
        sentiment = ((news.get("cryptopanic") or {}).get("score") or {}).get("score", 0)

    combined = max(-4, min(4, tech_score + sentiment))
    macro_s  = ((news.get("newsapi") or {}).get("score") or {}).get("sentiment", "")
    crypto_s = ((news.get("cryptopanic") or {}).get("score") or {}).get("sentiment", "neutral")

    return {"final_score": combined, "news_applied": True, "override": None,
            "tech_score": tech_score, "news_score": sentiment,
            "news_summary": f"Crypto: {crypto_s}. Macro: {macro_s or 'not analyzed'}"}


def _make_signal(final_score: int, symbol: str, price: float) -> dict:
    if final_score >= 2:
        direction, confidence = "BUY",  "HIGH" if final_score >= 3 else "MEDIUM"
        target, stop_loss     = round(price * 1.020, 4), round(price * 0.985, 4)
    elif final_score <= -2:
        direction, confidence = "SELL", "HIGH" if final_score <= -3 else "MEDIUM"
        target, stop_loss     = round(price * 0.980, 4), round(price * 1.015, 4)
    else:
        direction, confidence = "HOLD", "LOW"
        target, stop_loss     = price, None

    return {
        "id":           str(uuid.uuid4())[:8],
        "symbol":       symbol,
        "direction":    direction,
        "confidence":   confidence,
        "entry_price":  price,
        "target_price": target,
        "stop_loss":    stop_loss,
        "verify_at":    (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
        "status":       "PENDING",
        "llm_judgment": None,
    }


def cmd_signal(market: dict, news: dict | None, output_dir: Path) -> dict:
    symbol     = market["symbol"]
    price      = market["ticker"]["price"]
    timeframes = market.get("timeframes", {})

    # Score each available timeframe independently (micro → macro)
    tf_scores = {}
    for iv in TIMEFRAMES:
        if iv not in timeframes:
            continue
        tf = timeframes[iv]
        ind = {**tf["indicators"], "_price": price}
        tf_scores[iv] = _score_indicators(ind, tf.get("patterns", []))

    # Aggregate: weighted average (1h > 30m > 15m > 3m)
    weights   = {"3m": 1, "15m": 2, "30m": 3, "1h": 4}
    total_w   = sum(weights[iv] for iv in tf_scores)
    if total_w:
        raw_tech  = sum(tf_scores[iv]["total_score"] * weights[iv]
                        for iv in tf_scores) / total_w
        tech_score = round(raw_tech)
    else:
        # fallback: use 15m if available, else first available
        fb_iv  = "15m" if "15m" in timeframes else (list(timeframes.keys())[0] if timeframes else None)
        if fb_iv:
            fb     = timeframes[fb_iv]
            ind    = {**fb["indicators"], "_price": price}
            tech_res   = _score_indicators(ind, fb.get("patterns", []))
        else:
            tech_res = {"total_score": 0, "votes": {}}
        tech_score = tech_res["total_score"]
        tf_scores  = {fb_iv or "n/a": tech_res}

    news_r = _apply_news_layer(tech_score, news)
    sig    = _make_signal(news_r["final_score"], symbol, price)
    sig["score"]        = news_r["final_score"]
    sig["tf_scores"]    = {iv: {"score": tf_scores[iv]["total_score"],
                                "votes": tf_scores[iv]["votes"]}
                           for iv in tf_scores}
    sig["news_layer"]   = news_r
    sig["generated_at"] = market["fetched_at"]

    print(f"SIGNAL={sig['direction']} [{sig['confidence']}] score={news_r['final_score']:+d} @ {price}")
    print(f"target={sig['target_price']} stop={sig['stop_loss']} verify_at={sig['verify_at']}")

    # Per-timeframe breakdown (micro → macro)
    for iv in TIMEFRAMES:
        if iv not in tf_scores:
            continue
        s = tf_scores[iv]["total_score"]
        print(f"tf={iv} score={s:+d}")
        for v in tf_scores[iv]["votes"].values():
            print(f"  factor={v['reason']}")

    print(f"news: {news_r['news_summary']}")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{sig['id']}_{symbol}_{sig['direction']}.json"
    out_path.write_text(json.dumps(sig, indent=2))

    return sig


# ════════════════════════════════════════════════════════════════════
#  VERIFY — check signal outcome 30 min later
# ════════════════════════════════════════════════════════════════════

def cmd_verify(signal_path: Path):
    sig = json.loads(signal_path.read_text())

    if sig["status"] != "PENDING":
        print(f"Signal already {sig['status']}, skipping.")
        return

    symbol = sig["symbol"]

    price_data  = json.loads(_get(f"{BINANCE_BASE}/ticker/price?symbol={symbol}"))
    curr_price  = float(price_data["price"])

    entry       = sig["entry_price"]
    target      = sig["target_price"]
    stop        = sig.get("stop_loss")
    direction   = sig["direction"]
    change_pct  = (curr_price - entry) / entry * 100

    if direction == "HOLD":
        result = "HIT" if abs(change_pct) < 1.5 else "MISS"
        note   = f"Price moved {change_pct:+.2f}% ({'stable ✓' if result=='HIT' else 'volatile ✗'})"
    elif direction == "BUY":
        if curr_price >= target:
            result, note = "HIT",     f"Target reached: {curr_price:.4f} ≥ {target} (+{change_pct:.2f}%) ✓"
        elif stop and curr_price <= stop:
            result, note = "MISS",    f"Stop loss hit: {curr_price:.4f} ≤ {stop} ({change_pct:.2f}%) ✗"
        else:
            result = "PARTIAL" if change_pct > 0 else "MISS"
            note   = f"In progress: {curr_price:.4f} ({change_pct:+.2f}%)"
    else:  # SELL
        if curr_price <= target:
            result, note = "HIT",     f"Target reached: {curr_price:.4f} ≤ {target} ({change_pct:.2f}%) ✓"
        elif stop and curr_price >= stop:
            result, note = "MISS",    f"Stop loss hit: {curr_price:.4f} ≥ {stop} ({change_pct:+.2f}%) ✗"
        else:
            result = "PARTIAL" if change_pct < 0 else "MISS"
            note   = f"In progress: {curr_price:.4f} ({change_pct:+.2f}%)"

    verification = {
        "result": result, "note": note,
        "current_price": curr_price, "change_pct": round(change_pct, 4),
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(f"VERIFY={result} entry={entry} target={target} current={curr_price} ({change_pct:+.2f}%) {note}")

    sig["status"]       = result
    sig["verification"] = verification
    signal_path.write_text(json.dumps(sig, indent=2))

    knowledge_file = _RECORDS / "knowledge.jsonl"
    miss_file      = _RECORDS / "misses.jsonl"

    if result in ("HIT", "PARTIAL"):
        _RECORDS.mkdir(parents=True, exist_ok=True)
        entry_rec = {
            "id": sig["id"], "symbol": symbol, "direction": direction,
            "confidence": sig["confidence"], "score": sig.get("score", 0),
            "entry_price": entry, "target_price": target,
            "current_price": curr_price, "change_pct": verification["change_pct"],
            "result": result, "factors": sig.get("factors", {}),
            "llm_judgment": sig.get("llm_judgment"),
            "news_summary": (sig.get("news_layer") or {}).get("news_summary", ""),
            "generated_at": sig["generated_at"], "verified_at": verification["verified_at"],
        }
        with open(knowledge_file, "a") as f:
            f.write(json.dumps(entry_rec) + "\n")
    else:
        _RECORDS.mkdir(parents=True, exist_ok=True)
        with open(miss_file, "a") as f:
            f.write(json.dumps({**sig, **verification}) + "\n")


# ════════════════════════════════════════════════════════════════════
#  REPORT — knowledge base summary
# ════════════════════════════════════════════════════════════════════

def cmd_report():
    def load_jsonl(path):
        if not path.exists():
            return []
        return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

    hits   = load_jsonl(_RECORDS / "knowledge.jsonl")
    misses = load_jsonl(_RECORDS / "misses.jsonl")
    total  = len(hits) + len(misses)

    print("REPORT:")
    print(f"total={total}")
    print(f"hits={len(hits)}")
    print(f"misses={len(misses)}")
    print(f"hit_rate={len(hits)/total*100:.1f}%" if total else "hit_rate=n/a")

    if not hits:
        print("no hits yet")
        return

    for d, c in Counter(h["direction"] for h in hits).items():
        print(f"direction={d} count={c}")

    for sym, c in Counter(h["symbol"] for h in hits).most_common(5):
        print(f"symbol={sym} count={c}")

    fc = Counter()
    for h in hits:
        winning = tuple(sorted(k for k, v in h.get("factors", {}).items() if v.get("vote", 0) != 0))
        fc[winning] += 1
    for combo, count in fc.most_common(5):
        print(f"combo={count}x {'|'.join(combo)}")

    changes = [h["change_pct"] for h in hits if h.get("change_pct") is not None]
    if changes:
        print(f"price_change avg={sum(changes)/len(changes):+.2f}% best={max(changes):+.2f}% worst={min(changes):+.2f}%")

    llm = [h for h in hits if h.get("llm_judgment")]
    if llm:
        print(f"llm_coverage={len(llm)}/{len(hits)}")



# ════════════════════════════════════════════════════════════════════
#  SCHEDULE — adaptive news fetch loop
# ════════════════════════════════════════════════════════════════════

MACRO_WINDOWS = [
    {"name": "NFP/CPI release", "hour": 12, "minute": 30, "duration_min": 60,  "interval_min": 5},
    {"name": "Fed decision",    "hour": 18, "minute":  0, "duration_min": 90,  "interval_min": 5},
    {"name": "Asia open",       "hour":  0, "minute":  0, "duration_min": 30,  "interval_min": 10},
    {"name": "US open",         "hour": 13, "minute": 30, "duration_min": 30,  "interval_min": 10},
]
NORMAL_INTERVAL_MIN = 30
DAILY_LIMIT         = 100
WARN_THRESHOLD      = 80
HARD_STOP           = 95


def _load_budget() -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    p     = _RECORDS / "newsapi_budget.json"
    if p.exists():
        data = json.loads(p.read_text())
        if data.get("date") == today:
            return data
    return {"date": today, "used": 0, "events": []}


def _save_budget(budget: dict):
    _RECORDS.mkdir(parents=True, exist_ok=True)
    (_RECORDS / "newsapi_budget.json").write_text(json.dumps(budget, indent=2))


def _in_macro_window(now: datetime) -> dict | None:
    for w in MACRO_WINDOWS:
        start  = w["hour"] * 60 + w["minute"]
        nowmin = now.hour * 60 + now.minute
        if start <= nowmin < start + w["duration_min"]:
            return {"name": w["name"], "interval_min": w["interval_min"],
                    "remaining_min": w["duration_min"] - (nowmin - start)}
    return None


def cmd_schedule(symbol: str, output_dir: Path, dry_run: bool = False):
    output_dir.mkdir(parents=True, exist_ok=True)

    while True:
        now    = datetime.now(timezone.utc)
        budget = _load_budget()
        used   = budget["used"]

        print(f"schedule time={now.strftime('%H:%M UTC')} budget={used}/{DAILY_LIMIT}")

        if used >= HARD_STOP:
            print("budget=hard_stop sleeping_until=UTC_midnight")
            tomorrow  = (now + timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0)
            time.sleep(int((tomorrow - now).total_seconds()))
            continue

        macro = _in_macro_window(now)
        if macro:
            interval    = macro["interval_min"]
            event_label = macro["name"]
            print(f"window={macro['name']} remaining={macro['remaining_min']}min interval={interval}min")
        else:
            interval    = NORMAL_INTERVAL_MIN
            event_label = "normal"
            print(f"window=normal interval={interval}min")

        ts      = datetime.now().strftime("%Y%m%d_%H%M")
        outfile = output_dir / f"news_{ts}.json"

        if dry_run:
            print(f"dry_run outfile={outfile}")
        else:
            try:
                cmd_news(symbol, output=outfile)
                budget["used"] += 1
                budget["events"].append({"time": now.strftime("%H:%M:%S"), "event": event_label})
                _save_budget(budget)
            except Exception as e:
                print(f"error={e}")

        time.sleep(interval * 60)


# ════════════════════════════════════════════════════════════════════
#  RUN — full pipeline in one shot
# ════════════════════════════════════════════════════════════════════

def cmd_run(symbol: str, skip_news: bool = False):
    symbol = symbol.upper()

    # 1. Fetch
    market_file = _DATA / f"market_{symbol}.json"
    market      = cmd_fetch(symbol, output=market_file)

    # 2. News
    news = None
    if skip_news:
        pass
    else:
        news_file = _DATA / f"news_{symbol}.json"
        try:
            news = cmd_news(symbol, output=news_file)
        except Exception as e:
            print(f"news_failed={e}")

    # 3. Signal
    sig = cmd_signal(market, news, _SIGNALS)

    sig_file = _SIGNALS / f"{sig['id']}_{symbol}_{sig['direction']}.json"
    print(f"verify_cmd: python3 {__file__} verify {sig_file}")


# ════════════════════════════════════════════════════════════════════
#  CLI entry point
# ════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="crypto_signal.py",
        description="Crypto signal pipeline — run from any directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  run      BTCUSDT [--skip-news]                    full pipeline (3m/15m/30m/1h)
  fetch    BTCUSDT [--interval 3m|15m|30m|1h]       single timeframe only
  news     BTCUSDT                                   news sentiment only
  signal   BTCUSDT [--skip-news]                    signal (auto-fetches data)
  verify   signals/xxx.json                          verify a pending signal
  report                                             knowledge base summary
  schedule BTCUSDT [--dry-run]                       adaptive news loop
        """
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # run
    p_run = sub.add_parser("run", help="Full pipeline")
    p_run.add_argument("symbol")
    p_run.add_argument("--skip-news",  action="store_true")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Market data only")
    p_fetch.add_argument("symbol")
    p_fetch.add_argument("--interval", default="15m")
    p_fetch.add_argument("--limit",    default=100, type=int)
    p_fetch.add_argument("--output",   default=None)

    # news
    p_news = sub.add_parser("news", help="News sentiment only")
    p_news.add_argument("symbol")
    p_news.add_argument("--output", default=None)

    # signal
    p_sig = sub.add_parser("signal", help="Generate signal (auto-fetches if needed)")
    p_sig.add_argument("symbol")
    p_sig.add_argument("--skip-news", action="store_true")

    # verify
    p_ver = sub.add_parser("verify", help="Verify a pending signal")
    p_ver.add_argument("signal_json")

    # report
    sub.add_parser("report", help="Knowledge base summary")

    # schedule
    p_sch = sub.add_parser("schedule", help="Adaptive news fetch loop")
    p_sch.add_argument("symbol", default="BTCUSDT", nargs="?")
    p_sch.add_argument("--output-dir", default=None)
    p_sch.add_argument("--dry-run",    action="store_true")

    args = parser.parse_args()

    if args.cmd == "run":
        cmd_run(args.symbol, args.skip_news)

    elif args.cmd == "fetch":
        out = Path(args.output) if args.output else _DATA / f"market_{args.symbol.upper()}.json"
        cmd_fetch(args.symbol.upper(), args.interval, args.limit, out)

    elif args.cmd == "news":
        out = Path(args.output) if args.output else _DATA / f"news_{args.symbol.upper()}.json"
        cmd_news(args.symbol.upper(), out)

    elif args.cmd == "signal":
        symbol      = args.symbol.upper()
        market_file = _DATA / f"market_{symbol}.json"
        if not market_file.exists():
            cmd_fetch(symbol, output=market_file)
        market    = json.loads(market_file.read_text())
        news      = None
        news_file = _DATA / f"news_{symbol}.json"
        if not args.skip_news:
            if news_file.exists():
                news = json.loads(news_file.read_text())
            else:
                try:
                    news = cmd_news(symbol, output=news_file)
                except Exception as e:
                    print(f"news_failed={e}")
        cmd_signal(market, news, _SIGNALS)

    elif args.cmd == "verify":
        cmd_verify(Path(args.signal_json))

    elif args.cmd == "report":
        cmd_report()

    elif args.cmd == "schedule":
        out = Path(args.output_dir) if args.output_dir else _DATA / "news"
        cmd_schedule(args.symbol.upper(), out, args.dry_run)


if __name__ == "__main__":
    main()
