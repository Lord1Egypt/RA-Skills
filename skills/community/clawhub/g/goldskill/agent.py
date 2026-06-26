#!/usr/bin/env python3
"""
GoldSkill v3.2 — OpenClaw Skill 版本
国际期货量化分析系统
"""

import json
import math
import os
import time
import asyncio
import concurrent.futures
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

SYMBOLS = {
    "XAUUSD":  {"yf": "GC=F",  "stooq": "xauusd", "name": "黄金",    "unit": "USD/oz",    "dec": 2},
    "XAGUSD":  {"yf": "SI=F",  "stooq": "xagusd", "name": "白银",    "unit": "USD/oz",    "dec": 3},
    "CRUDEOIL":{"yf": "CL=F",  "stooq": "cl.f",   "name": "WTI原油", "unit": "USD/bbl",   "dec": 2},
    "NATGAS":  {"yf": "NG=F",  "stooq": "ng.f",   "name": "天然气",  "unit": "USD/MMBtu", "dec": 3},
    "COPPER":  {"yf": "HG=F",  "stooq": "hg.f",   "name": "沪铜",    "unit": "USD/lb",    "dec": 4},
}

COMMODITY_KEYWORDS = {
    "XAUUSD": [
        "gold price","gold futures","spot gold","xau/usd","xauusd","gold rally","gold slump",
        "gold hits","gold rises","gold falls","gold drops","gold surges","gold plunges",
        "comex gold","lbma gold","gold fix","troy ounce","gold per ounce",
        "gold demand","gold supply","gold reserve","central bank gold","gold buying",
        "gold etf","gld etf","gold inflow","gold outflow","gold holdings",
        "gold mining","gold output","gold production","gold ore","barrick","newmont","agnico",
        "safe haven","haven demand","inflation hedge","real yield","dollar gold",
        "fed gold","rate gold","treasury gold","geopolitical gold",
        "黄金","金价","现货金","期货金","黄金期货","黄金价格","黄金上涨","黄金下跌",
        "黄金储备","央行购金","黄金需求","黄金ETF","黄金矿","贵金属","避险黄金",
        "纽约黄金","伦敦金","黄金止损","黄金突破",
    ],
    "XAGUSD": [
        "silver price","silver futures","spot silver","xag/usd","xagusd",
        "silver rally","silver slump","silver hits","silver rises","silver falls",
        "comex silver","silver fix","silver per ounce","gold silver ratio",
        "silver demand","silver supply","silver mining","silver output","silver production",
        "silver etf","slv etf","silver inflow","silver investment","silver coin",
        "solar silver","photovoltaic silver","industrial silver","silver deficit","silver surplus",
        "first majestic","pan american silver","wheaton precious",
        "白银","银价","现货白银","白银期货","白银价格","白银上涨","白银下跌",
        "白银需求","白银供应","工业用银","光伏用银","白银ETF","白银矿","金银比",
    ],
    "CRUDEOIL": [
        "crude oil","crude price","oil price","wti crude","brent crude","wti futures","brent futures",
        "oil rally","oil slump","oil hits","oil rises","oil falls","oil surges","oil plunges",
        "barrel price","nymex crude","ice brent","oil fix",
        "opec","opec+","opec cut","opec hike","production cut","output cut","production quota",
        "oil supply","oil demand","oil inventory","oil stockpile","crude inventory",
        "eia crude","api crude","cushing","strategic petroleum reserve","spr release",
        "refinery","refining margin","crack spread","gasoline supply","diesel supply",
        "saudi aramco","saudi oil","russia oil","iran oil","iraq oil","venezuela oil",
        "libya oil","nigeria oil","uae oil","shale oil","permian","bakken","eagle ford",
        "exxon","chevron","bp","shell","totalenergies","conocophillips",
        "原油","油价","布伦特","WTI","石油","欧佩克","减产","增产","原油库存","炼油",
        "汽油","柴油","油价上涨","油价下跌","页岩油","石油储备","沙特石油","俄罗斯石油",
        "能源价格","石油需求","石油供应","原油期货",
    ],
    "NATGAS": [
        "natural gas","natgas","gas price","henry hub","ttf gas","nbp gas",
        "gas futures","gas rally","gas slump","gas hits","gas rises","gas falls",
        "nymex gas","ice gas","gas per mmbtu","gas per therm",
        "gas supply","gas demand","gas storage","gas inventory","gas stockpile",
        "eia gas","gas injection","gas withdrawal","gas deficit","gas surplus",
        "gas production","shale gas","gas output","gas field","gas well",
        "lng","liquefied natural gas","lng export","lng import","lng terminal",
        "lng price","lng cargo","lng tanker","lng facility","lng plant",
        "pipeline gas","gas pipeline","nord stream","gazprom","sabine pass",
        "gas power","gas electricity","power generation gas","gas turbine",
        "heating demand","gas heating","winter demand","summer cooling",
        "cheniere","sempra","qatar gas","australia lng","us lng",
        "天然气","气价","液化天然气","LNG","天然气价格","天然气上涨","天然气下跌",
        "天然气库存","天然气需求","天然气供应","天然气期货","页岩气","管道气",
        "天然气出口","天然气进口","亨利港","欧洲天然气","天然气发电","冬季用气",
    ],
    "COPPER": [
        "copper price","copper futures","copper rally","copper slump",
        "copper hits","copper rises","copper falls","copper surges","copper plunges",
        "lme copper","comex copper","shfe copper","copper fix","copper per pound","copper per tonne",
        "copper demand","copper supply","copper inventory","copper stockpile","copper warehouse",
        "copper deficit","copper surplus","copper production","copper output","copper smelter",
        "copper cathode","copper ore","copper concentrate","copper refining",
        "codelco","freeport","glencore","bhp copper","rio tinto copper","antofagasta",
        "chile copper","peru copper","zambia copper","congo copper","indonesia copper",
        "escondida","grasberg","cobre panama",
        "ev copper","electric vehicle copper","renewable copper","solar copper","wind copper",
        "grid copper","power cable copper","construction copper","china copper demand",
        "铜","铜价","伦铜","沪铜","纽铜","铜期货","铜价上涨","铜价下跌",
        "铜需求","铜供应","铜库存","铜矿","精铜","废铜","铜精矿","铜冶炼",
        "智利铜","秘鲁铜","新能源用铜","电动车用铜","电网用铜","有色金属",
    ],
}

NEWS_SOURCES = [
    {"name": "Google News · 黄金",         "url": "https://news.google.com/rss/search?q=gold+price+futures+XAU&hl=en-US&gl=US&ceid=US:en",                              "agency": "Google News", "country": "US", "symbols_hint": ["XAUUSD"],                              "extract_source": True},
    {"name": "Google News · 白银",         "url": "https://news.google.com/rss/search?q=silver+price+XAG+commodities&hl=en-US&gl=US&ceid=US:en",                        "agency": "Google News", "country": "US", "symbols_hint": ["XAGUSD"],                              "extract_source": True},
    {"name": "Google News · 原油",         "url": "https://news.google.com/rss/search?q=crude+oil+WTI+Brent+OPEC&hl=en-US&gl=US&ceid=US:en",                            "agency": "Google News", "country": "US", "symbols_hint": ["CRUDEOIL"],                            "extract_source": True},
    {"name": "Google News · 天然气",       "url": "https://news.google.com/rss/search?q=natural+gas+LNG+Henry+Hub+price&hl=en-US&gl=US&ceid=US:en",                     "agency": "Google News", "country": "US", "symbols_hint": ["NATGAS"],                              "extract_source": True},
    {"name": "Google News · 铜",           "url": "https://news.google.com/rss/search?q=copper+price+LME+COMEX+mining&hl=en-US&gl=US&ceid=US:en",                       "agency": "Google News", "country": "US", "symbols_hint": ["COPPER"],                              "extract_source": True},
    {"name": "Google News · 路透社大宗商品","url": "https://news.google.com/rss/search?q=site:reuters.com+commodities+gold+oil+copper&hl=en-US&gl=US&ceid=US:en",        "agency": "Reuters",     "country": "UK", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL","NATGAS","COPPER"], "extract_source": True},
    {"name": "Google News · 路透社原油",   "url": "https://news.google.com/rss/search?q=site:reuters.com+crude+oil+OPEC+energy&hl=en-US&gl=US&ceid=US:en",              "agency": "Reuters",     "country": "UK", "symbols_hint": ["CRUDEOIL","NATGAS"],                   "extract_source": True},
    {"name": "Google News · 路透社金属",   "url": "https://news.google.com/rss/search?q=site:reuters.com+gold+silver+copper+metals&hl=en-US&gl=US&ceid=US:en",          "agency": "Reuters",     "country": "UK", "symbols_hint": ["XAUUSD","XAGUSD","COPPER"],            "extract_source": True},
    {"name": "Google News · 彭博社大宗商品","url": "https://news.google.com/rss/search?q=site:bloomberg.com+commodities+gold+oil+metals&hl=en-US&gl=US&ceid=US:en",     "agency": "Bloomberg",   "country": "US", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL","NATGAS","COPPER"], "extract_source": True},
    {"name": "Google News · 彭博社金属",   "url": "https://news.google.com/rss/search?q=site:bloomberg.com+copper+silver+gold+metals&hl=en-US&gl=US&ceid=US:en",        "agency": "Bloomberg",   "country": "US", "symbols_hint": ["COPPER","XAGUSD","XAUUSD"],            "extract_source": True},
    {"name": "Google News · 美联社能源",   "url": "https://news.google.com/rss/search?q=site:apnews.com+energy+oil+gold+commodities&hl=en-US&gl=US&ceid=US:en",         "agency": "AP",          "country": "US", "symbols_hint": ["CRUDEOIL","NATGAS","XAUUSD"],          "extract_source": True},
    {"name": "Google News · 美联社金属",   "url": "https://news.google.com/rss/search?q=site:apnews.com+gold+silver+copper&hl=en-US&gl=US&ceid=US:en",                  "agency": "AP",          "country": "US", "symbols_hint": ["XAUUSD","XAGUSD","COPPER"],            "extract_source": True},
    {"name": "Kitco 黄金新闻",             "url": "https://www.kitco.com/news/rss/kitcogold.rss",                                                                        "agency": "Kitco",       "country": "CA", "symbols_hint": ["XAUUSD","XAGUSD"],                    "encoding": "latin-1"},
    {"name": "Kitco 白银新闻",             "url": "https://www.kitco.com/news/rss/kitcosilver.rss",                                                                      "agency": "Kitco",       "country": "CA", "symbols_hint": ["XAGUSD","XAUUSD"],                    "encoding": "latin-1"},
    {"name": "Kitco 基础金属",             "url": "https://www.kitco.com/news/rss/kitcobase.rss",                                                                        "agency": "Kitco",       "country": "CA", "symbols_hint": ["COPPER","XAGUSD"],                    "encoding": "latin-1"},
    {"name": "Investing.com 大宗商品",     "url": "https://www.investing.com/rss/news_14.rss",                                                                           "agency": "Investing.com","country": "US", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL","NATGAS","COPPER"]},
    {"name": "Investing.com 能源",         "url": "https://www.investing.com/rss/news_25.rss",                                                                           "agency": "Investing.com","country": "US", "symbols_hint": ["CRUDEOIL","NATGAS"]},
    {"name": "EIA 今日能源",               "url": "https://www.eia.gov/rss/todayinenergy.xml",                                                                           "agency": "EIA",         "country": "US", "symbols_hint": ["CRUDEOIL","NATGAS"]},
    {"name": "CNBC 能源",                  "url": "https://www.cnbc.com/id/10000664/device/rss/rss.html",                                                                "agency": "CNBC",        "country": "US", "symbols_hint": ["CRUDEOIL","NATGAS"]},
    {"name": "CNBC 市场",                  "url": "https://www.cnbc.com/id/15839069/device/rss/rss.html",                                                                "agency": "CNBC",        "country": "US", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL","COPPER"]},
    {"name": "FXStreet 大宗商品",          "url": "https://www.fxstreet.com/rss/news/commodity",                                                                         "agency": "FXStreet",    "country": "ES", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL"]},
    {"name": "Rigzone 石油天然气",         "url": "https://www.rigzone.com/news/rss/rigzone_latest.aspx",                                                                "agency": "Rigzone",     "country": "US", "symbols_hint": ["CRUDEOIL","NATGAS"]},
    {"name": "MarketWatch 市场",           "url": "https://feeds.marketwatch.com/marketwatch/marketpulse/",                                                              "agency": "MarketWatch", "country": "US", "symbols_hint": ["XAUUSD","XAGUSD","CRUDEOIL","NATGAS","COPPER"]},
    {"name": "MetalMiner 金属",            "url": "https://agmetalminer.com/feed/",                                                                                      "agency": "MetalMiner",  "country": "US", "symbols_hint": ["COPPER","XAGUSD"]},
]

NEWS_MAX_AGE = 7 * 24 * 3600

def http_get(url, timeout=8, headers=None):
    hdrs = {"User-Agent": "Mozilla/5.0 GoldSkill/3.2"}
    if headers:
        hdrs.update(headers)
    req = Request(url, headers=hdrs)
    with urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

def fetch_price_yahoo(cfg):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{cfg['yf']}?interval=5m&range=1d"
    data = json.loads(http_get(url, timeout=8))
    result = data["chart"]["result"][0]
    meta   = result["meta"]
    quotes = result["indicators"]["quote"][0]
    closes = [c for c in quotes.get("close", []) if c]
    price  = meta.get("regularMarketPrice") or (closes[-1] if closes else None)
    prev   = meta.get("previousClose", price)
    return {
        "source": "Yahoo Finance",
        "price":  round(price, cfg["dec"]),
        "prev":   round(prev,  cfg["dec"]),
        "high":   round(meta.get("regularMarketDayHigh", price), cfg["dec"]),
        "low":    round(meta.get("regularMarketDayLow",  price), cfg["dec"]),
        "volume": int(meta.get("regularMarketVolume", 0)),
        "series": [round(v, cfg["dec"]) for v in closes[-50:]],
    }

def fetch_price_stooq(cfg):
    url = f"https://stooq.com/q/l/?s={cfg['stooq']}&f=sd2t2ohlcv&h&e=csv"
    lines = [l for l in http_get(url, timeout=8).strip().split("\n") if l and not l.startswith("Symbol")]
    if not lines:
        raise ValueError("Stooq: no data")
    p = lines[-1].split(",")
    price = float(p[6])
    return {
        "source": "Stooq",
        "price":  round(price,       cfg["dec"]),
        "prev":   round(float(p[3]), cfg["dec"]),
        "high":   round(float(p[4]), cfg["dec"]),
        "low":    round(float(p[5]), cfg["dec"]),
        "volume": int(float(p[7])) if p[7].strip() else 0,
        "series": [round(price, cfg["dec"])],
    }

def fetch_price_metals_live(cfg):
    if cfg["yf"] not in ("GC=F", "SI=F"):
        raise ValueError("metals.live: only gold/silver")
    data  = json.loads(http_get("https://api.metals.live/v1/spot", timeout=8))
    key   = "gold" if cfg["yf"] == "GC=F" else "silver"
    price = data.get(key)
    if price is None:
        raise ValueError("metals.live: no price")
    return {
        "source": "metals.live",
        "price":  round(price, cfg["dec"]),
        "prev":   round(price * 0.999, cfg["dec"]),
        "high":   round(price * 1.003, cfg["dec"]),
        "low":    round(price * 0.997, cfg["dec"]),
        "volume": 0, "series": [round(price, cfg["dec"])],
    }

PRICE_FETCHERS = [fetch_price_yahoo, fetch_price_stooq, fetch_price_metals_live]

def fetch_price(sym):
    cfg = SYMBOLS[sym]
    errors = []
    for fetcher in PRICE_FETCHERS:
        try:
            r = fetcher(cfg)
            r.update({"symbol": sym, "name": cfg["name"], "unit": cfg["unit"], "dec": cfg["dec"]})
            return r
        except Exception as e:
            errors.append(f"{fetcher.__name__}: {e}")
    raise RuntimeError(f"{sym} 所有价格源失败: {'; '.join(errors)}")

def calc_ema(prices, period):
    if not prices: return 0.0
    k, e = 2.0 / (period + 1), prices[0]
    for p in prices[1:]: e = p * k + e * (1 - k)
    return e

def calc_rsi(prices, period=14):
    if len(prices) < period + 1: return 50.0
    gains, losses = [], []
    for i in range(1, len(prices)):
        d = prices[i] - prices[i-1]
        gains.append(max(d, 0)); losses.append(max(-d, 0))
    ag = sum(gains[:period]) / period
    al = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        ag = (ag * (period-1) + gains[i]) / period
        al = (al * (period-1) + losses[i]) / period
    return round(100 - 100 / (1 + ag / al) if al else 100, 2)

def calc_macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow: return {"macd": 0, "signal": 0, "hist": 0}
    macd = calc_ema(prices, fast) - calc_ema(prices, slow)
    sig  = macd * (2 / (signal + 1))
    return {"macd": round(macd, 4), "signal": round(sig, 4), "hist": round(macd - sig, 4)}

def calc_bb(prices, period=20, std_dev=2):
    sl = prices[-period:] if len(prices) >= period else prices
    mean = sum(sl) / len(sl)
    std  = math.sqrt(sum((p - mean)**2 for p in sl) / len(sl))
    return {"upper": round(mean + std_dev*std, 4), "mid": round(mean, 4), "lower": round(mean - std_dev*std, 4)}

def calc_atr(prices, period=14):
    if len(prices) < 2: return 0.0
    trs = [abs(prices[i] - prices[i-1]) for i in range(max(1, len(prices)-period), len(prices))]
    return round(sum(trs) / len(trs), 4)

def calc_cci(prices, period=14):
    sl = prices[-period:] if len(prices) >= period else prices
    mean = sum(sl) / len(sl)
    mad  = sum(abs(p - mean) for p in sl) / len(sl)
    return round((prices[-1] - mean) / (0.015 * mad) if mad else 0, 2)

def calc_stoch(prices, k_period=14):
    sl = prices[-k_period:] if len(prices) >= k_period else prices
    hi, lo, cl = max(sl), min(sl), prices[-1]
    return round((cl - lo) / (hi - lo) * 100 if hi != lo else 50, 2)

def calc_indicators(pd):
    series = pd.get("series", [])
    if len(series) < 3:
        series = [pd["price"]] * 30
    cur, prev = series[-1], series[-2] if len(series) > 1 else series[-1]
    rsi   = calc_rsi(series)
    macd  = calc_macd(series)
    bb    = calc_bb(series)
    cci   = calc_cci(series)
    stoch = calc_stoch(series)
    atr   = calc_atr(series)
    ema20 = round(calc_ema(series, 20), pd["dec"])
    ema50 = round(calc_ema(series, 50), pd["dec"])

    bull, bear, reasons = 0, 0, []
    if rsi < 30:   bull += 2; reasons.append(f"RSI {rsi} 超卖区 → 反弹信号")
    elif rsi > 70: bear += 2; reasons.append(f"RSI {rsi} 超买区 → 回调风险")
    else:          reasons.append(f"RSI {rsi} 中性")

    if macd["macd"] > macd["signal"]: bull += 1; reasons.append("MACD 金叉 → 多头")
    else:                              bear += 1; reasons.append("MACD 死叉 → 空头")

    if cur > ema20 and cur > ema50:   bull += 2; reasons.append("价格 > EMA20/50 → 上升趋势")
    elif cur < ema20 and cur < ema50: bear += 2; reasons.append("价格 < EMA20/50 → 下降趋势")
    else:                             reasons.append("价格在均线间震荡")

    if cci < -100: bull += 1; reasons.append(f"CCI {cci} 超卖")
    elif cci > 100: bear += 1; reasons.append(f"CCI {cci} 超买")

    if stoch < 20: bull += 1; reasons.append(f"随机指标 {stoch} 超卖")
    elif stoch > 80: bear += 1; reasons.append(f"随机指标 {stoch} 超买")

    if cur > bb["upper"]: bear += 1; reasons.append("价格突破布林上轨 → 过热")
    elif cur < bb["lower"]: bull += 1; reasons.append("价格跌破布林下轨 → 超卖")

    direction = "HOLD"
    conf = 50
    if bull > bear + 1:   direction = "BUY";  conf = min(92, 50 + bull * 7)
    elif bear > bull + 1: direction = "SELL"; conf = min(92, 50 + bear * 7)
    else:                 conf = 40 + abs(bull - bear) * 5

    dec = pd["dec"]
    if direction == "BUY":
        sl_price = round(cur - atr * 1.5, dec);  tp1 = round(cur + atr * 1.5, dec); tp2 = round(cur + atr * 3.0, dec)
    elif direction == "SELL":
        sl_price = round(cur + atr * 1.5, dec);  tp1 = round(cur - atr * 1.5, dec); tp2 = round(cur - atr * 3.0, dec)
    else:
        sl_price = round(cur - atr, dec);         tp1 = round(cur + atr, dec);        tp2 = round(cur + atr * 2, dec)

    chg_pct = round((cur - prev) / prev * 100, 3) if prev else 0
    return {
        "rsi": rsi, "macd": macd, "bb": bb, "cci": cci, "stoch": stoch,
        "atr": atr, "ema20": ema20, "ema50": ema50,
        "direction": direction, "confidence": conf,
        "bull_score": bull, "bear_score": bear, "reasons": reasons,
        "entry": cur, "stop_loss": sl_price, "tp1": tp1, "tp2": tp2,
        "change_pct": chg_pct,
    }

def sentiment_score(text):
    t = text.lower()
    bull_kws = ["surge","soar","rally","breakout","bullish","record high","safe haven","涨","上涨","看涨","利好","反弹"]
    bear_kws = ["crash","plunge","slump","bearish","record low","recession","rate hike","跌","下跌","看跌","利空","暴跌"]
    b = sum(1 for w in bull_kws if w in t)
    s = sum(1 for w in bear_kws if w in t)
    score = round((b - s) / max(b + s, 1), 3)
    return ("bull" if score > 0.15 else "bear" if score < -0.15 else "neu"), score

def rel_symbol(text, hints=None):
    t = text.lower()
    scores = {sym: sum(1 for k in kws if k in t) for sym, kws in COMMODITY_KEYWORDS.items()}
    matched = [(s, c) for s, c in scores.items() if c > 0]
    if matched:
        syms = [s for s, _ in sorted(matched, key=lambda x: -x[1])]
        return syms, scores
    fallback = hints or []
    return fallback, {s: 1 for s in fallback}

def _sanitize_xml(raw_bytes, hint_enc=None):
    for enc in ([hint_enc] if hint_enc else []) + ["utf-8", "latin-1"]:
        try:
            raw = raw_bytes.decode(enc); break
        except Exception: continue
    else:
        raw = raw_bytes.decode("latin-1", errors="replace")
    raw = raw.lstrip('\ufeff\ufffe')
    raw = re.sub(r'<\?xml[^?]*\?>', '<?xml version="1.0" encoding="UTF-8"?>', raw, count=1)
    raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', raw)
    raw = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', raw)
    return raw

def _get_text(el, *tags):
    for tag in tags:
        found = el.find(tag)
        if found is not None:
            txt = (found.text or '').strip() or ''.join(found.itertext()).strip()
            if txt: return txt
    return ''

def _extract_source(title, default):
    m = re.search(r'\s[-–—]\s*([A-Za-z][A-Za-z0-9 .&]+?)\s*$', title)
    if m:
        src = m.group(1).strip()
        mapping = {"Reuters":"Reuters","Bloomberg":"Bloomberg","AP":"AP","CNBC":"CNBC","WSJ":"WSJ","MarketWatch":"MarketWatch","Kitco":"Kitco"}
        for k, v in mapping.items():
            if k.lower() in src.lower():
                return v, title[:title.rfind(m.group(0))].strip()
        if len(src) < 30:
            return src, title[:title.rfind(m.group(0))].strip()
    return default, title

def parse_date(s):
    if not s: return int(time.time())
    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"]:
        try:
            dt = datetime.strptime(s.strip(), fmt)
            return int((dt.replace(tzinfo=timezone.utc) if not dt.tzinfo else dt).timestamp())
        except: continue
    return int(time.time())

def fetch_rss(source):
    uas = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
    ]
    raw_bytes = None
    for ua in uas:
        try:
            req = Request(source["url"], headers={"User-Agent": ua, "Accept": "application/rss+xml,*/*"})
            with urlopen(req, timeout=8) as r:
                raw_bytes = r.read()
            break
        except: time.sleep(0.3)
    if not raw_bytes:
        return []

    raw = _sanitize_xml(raw_bytes, source.get("encoding"))
    try:
        root = ET.fromstring(raw.encode("utf-8"))
    except ET.ParseError:
        try:
            root = ET.fromstring(raw[:raw.rfind(">")+1].encode("utf-8"))
        except: return []

    items = root.findall(".//item") or root.findall("channel/item")
    results = []
    for item in items[:10]:
        title = _get_text(item, "title")
        if not title: continue
        link_el = item.find("link")
        link = (link_el.text or "").strip() if link_el is not None else ""
        desc  = _get_text(item, "description", "summary")
        pub_ts = parse_date(_get_text(item, "pubDate", "published"))
        agency = source["agency"]
        if source.get("extract_source"):
            agency, title = _extract_source(title, agency)
        text = title + " " + desc
        sent, score = sentiment_score(text)
        syms, rel_scores = rel_symbol(text, source.get("symbols_hint", []))
        results.append({
            "title": title[:200], "link": link, "agency": agency,
            "pub_ts": pub_ts,
            "pub_time": datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d %H:%M"),
            "sentiment": sent, "score": score, "symbols": syms,
            "rel_scores": rel_scores,
        })
    return results

def fetch_all_news():
    all_news = []
    def _one(src):
        try: return fetch_rss(src)
        except: return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(_one, s) for s in NEWS_SOURCES]
        for fut in concurrent.futures.as_completed(futs, timeout=60):
            try:
                all_news.extend(fut.result())
            except Exception:
                pass
    cutoff = int(time.time()) - NEWS_MAX_AGE
    seen, unique = set(), []
    for n in all_news:
        if n["pub_ts"] < cutoff:
            continue
        key = n["title"][:60].lower().strip()
        if key and key not in seen:
            seen.add(key); unique.append(n)
    unique.sort(key=lambda x: x["pub_ts"], reverse=True)
    return unique

SENT_ICON = {"bull": "▲", "bear": "▼", "neu": "●"}
SENT_LABEL = {"bull": "看涨", "bear": "看跌", "neu": "中性"}
DIR_ICON = {"BUY": "▲ 做多", "SELL": "▼ 做空", "HOLD": "◆ 观望"}
PRIORITY_AGENCIES = {"Reuters", "Bloomberg", "AP"}

def format_strategy(sym, pd, ind):
    name = pd["name"]
    price = pd["price"]
    chg = ind["change_pct"]
    chg_str = (f"+{chg}%" if chg >= 0 else f"{chg}%")
    direction = ind["direction"]
    conf = ind["confidence"]

    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  {name} ({sym})  {price} {pd['unit']}  {chg_str}")
    lines.append(f"  高: {pd.get('high', '-')}  低: {pd.get('low', '-')}")
    lines.append(f"{'='*60}")
    lines.append(f"  策略信号: {DIR_ICON[direction]}   置信度: {conf}%")
    lines.append(f"  多头得分: {ind['bull_score']}   空头得分: {ind['bear_score']}")
    lines.append(f"  进场价:  {ind['entry']}")
    lines.append(f"  止损:    {ind['stop_loss']}")
    lines.append(f"  目标1:   {ind['tp1']}")
    lines.append(f"  目标2:   {ind['tp2']}")
    lines.append(f"  风险回报: 1 : 1.5 / 1 : 3.0")
    lines.append(f"\n  主要指标:")
    lines.append(f"    RSI={ind['rsi']}  MACD={ind['macd']['macd']}  ATR={ind['atr']}")
    lines.append(f"    CCI={ind['cci']}  随机K={ind['stoch']}  EMA20={ind['ema20']}  EMA50={ind['ema50']}")
    lines.append(f"    布林: 上{ind['bb']['upper']} 中{ind['bb']['mid']} 下{ind['bb']['lower']}")
    lines.append(f"\n  信号依据:")
    for r in ind["reasons"]:
        lines.append(f"    • {r}")
    return "\n".join(lines)

def _news_sort_key(n, sym):
    rel   = n.get("rel_scores", {}).get(sym, 0)
    prio  = 1 if n["agency"] in PRIORITY_AGENCIES else 0
    return (rel, prio, n["pub_ts"])

def format_news(sym, news_list, shown_titles):
    filtered = [n for n in news_list
                if sym in n.get("symbols", []) and n.get("rel_scores", {}).get(sym, 0) >= 2]
    if not filtered:
        return f"\n  暂无 {sym} 相关新闻（7天内）"
    
    filtered.sort(key=lambda n: _news_sort_key(n, sym), reverse=True)
    shown = filtered[:6]
    
    lines = [f"\n  专属新闻（关联度最高 6 条）:"]
    for n in shown:
        shown_titles.add(n["title"][:60].lower())
        icon  = SENT_ICON[n["sentiment"]]
        label = SENT_LABEL[n["sentiment"]]
        star  = "★ " if n["agency"] in PRIORITY_AGENCIES else "   "
        lines.append(f"    {star}{icon} [{label}] {n['title'][:80]}")
        lines.append(f"         来源: {n['agency']}  时间: {n['pub_time']}")
        if n.get("link"):
            lines.append(f"         链接: {n['link'][:100]}")
    return "\n".join(lines)

def format_general_news(news_list, shown_titles):
    general = [
        n for n in news_list
        if n["title"][:60].lower() not in shown_titles
        and sum(n.get("rel_scores", {}).values()) >= 1
    ]
    general.sort(key=lambda n: n["pub_ts"], reverse=True)
    shown = general[:10]
    
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  全球大宗商品综合新闻（最新 {len(shown)} 条）")
    lines.append(f"{'='*60}")
    if not shown:
        lines.append("  暂无更多新闻")
        return "\n".join(lines)
    
    for n in shown:
        icon  = SENT_ICON[n["sentiment"]]
        label = SENT_LABEL[n["sentiment"]]
        star  = "★ " if n["agency"] in PRIORITY_AGENCIES else "   "
        syms_str = " / ".join(n.get("symbols", []))
        lines.append(f"    {star}{icon} [{label}] {n['title'][:80]}")
        lines.append(f"         来源: {n['agency']}  时间: {n['pub_time']}  品种: {syms_str}")
        if n.get("link"):
            lines.append(f"         链接: {n['link'][:100]}")
    return "\n".join(lines)

async def run(skill_input: str, context: dict = None):
    target_symbols = list(SYMBOLS.keys())
    
    if skill_input:
        input_lower = skill_input.lower()
        if "黄金" in input_lower or "gold" in input_lower or "xau" in input_lower:
            target_symbols = ["XAUUSD"]
        elif "白银" in input_lower or "silver" in input_lower or "xag" in input_lower:
            target_symbols = ["XAGUSD"]
        elif "原油" in input_lower or "oil" in input_lower or "brent" in input_lower or "wti" in input_lower:
            target_symbols = ["CRUDEOIL"]
        elif "天然气" in input_lower or "natgas" in input_lower or "lng" in input_lower:
            target_symbols = ["NATGAS"]
        elif "铜" in input_lower or "copper" in input_lower:
            target_symbols = ["COPPER"]
        elif "全部" in input_lower or "all" in input_lower:
            target_symbols = list(SYMBOLS.keys())

    loop = asyncio.get_event_loop()
    
    def fetch_all_prices():
        results = {}
        def _fetch_sym(sym):
            try:
                pd = fetch_price(sym)
                ind = calc_indicators(pd)
                return sym, pd, ind, None
            except Exception as e:
                return sym, None, None, str(e)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            futs = {ex.submit(_fetch_sym, sym): sym for sym in target_symbols}
            for fut in concurrent.futures.as_completed(futs):
                sym, pd, ind, err = fut.result()
                results[sym] = (pd, ind, err)
        return results

    def fetch_news():
        return fetch_all_news()

    price_results = await loop.run_in_executor(None, fetch_all_prices)
    all_news = await loop.run_in_executor(None, fetch_news)

    output = []
    output.append("=" * 60)
    output.append("  GoldSkill v3.2 — 国际期货量化分析系统")
    output.append(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    shown_titles = set()
    for sym in target_symbols:
        pd, ind, err = price_results.get(sym, (None, None, "未获取"))
        if err:
            output.append(f"\n{'='*60}")
            output.append(f"  {SYMBOLS[sym]['name']} ({sym})  获取失败: {err}")
            continue
        output.append(format_strategy(sym, pd, ind))
        output.append(format_news(sym, all_news, shown_titles))

    output.append(format_general_news(all_news, shown_titles))

    output.append(f"\n{'='*60}")
    output.append(f"  分析完成  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)

    return "\n".join(output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        result = asyncio.run(run("测试"))
        print(result)
    else:
        result = asyncio.run(run(""))
        print(result)
