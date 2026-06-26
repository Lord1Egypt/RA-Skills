"""
轻量级技术分析 — 纯 Python，不依赖 TA-Lib / pandas / numpy
只计算 Skill 需要的核心指标
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Optional


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 基础指标
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def sma(values: list[float], period: int) -> list[float | None]:
    """简单移动平均线"""
    result: list[float | None] = [None] * len(values)
    for i in range(period - 1, len(values)):
        result[i] = sum(values[i - period + 1 : i + 1]) / period
    return result


def ema(values: list[float], period: int) -> list[float | None]:
    """指数移动平均线"""
    result: list[float | None] = [None] * len(values)
    if len(values) < period:
        return result
    result[period - 1] = sum(values[:period]) / period
    m = 2 / (period + 1)
    for i in range(period, len(values)):
        prev = result[i - 1]
        if prev is not None:
            result[i] = (values[i] - prev) * m + prev
    return result


def rsi(closes: list[float], period: int = 14) -> list[float | None]:
    """RSI 指标"""
    result: list[float | None] = [None] * len(closes)
    if len(closes) < period + 1:
        return result
    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    ag = sum(gains[:period]) / period
    al = sum(losses[:period]) / period
    result[period] = 100.0 if al == 0 else round(100 - 100 / (1 + ag / al), 2)
    for i in range(period, len(gains)):
        ag = (ag * (period - 1) + gains[i]) / period
        al = (al * (period - 1) + losses[i]) / period
        result[i + 1] = 100.0 if al == 0 else round(100 - 100 / (1 + ag / al), 2)
    return result


def macd(
    closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9
) -> dict:
    """MACD 指标"""
    ef = ema(closes, fast)
    es = ema(closes, slow)
    ml: list[float | None] = [None] * len(closes)
    for i in range(len(closes)):
        if ef[i] is not None and es[i] is not None:
            ml[i] = round(ef[i] - es[i], 6)
    mv = [v for v in ml if v is not None]
    sl_raw = ema(mv, signal) if len(mv) >= signal else []
    sl: list[float | None] = [None] * len(closes)
    off = len(closes) - len(mv)
    for i, v in enumerate(sl_raw):
        sl[off + i] = round(v, 6) if v is not None else None
    hist: list[float | None] = [None] * len(closes)
    for i in range(len(closes)):
        if ml[i] is not None and sl[i] is not None:
            hist[i] = round(ml[i] - sl[i], 6)
    return {"macd": ml, "signal": sl, "histogram": hist}


def bollinger_bands(
    closes: list[float], period: int = 20, std_dev: float = 2.0
) -> dict:
    """布林带"""
    mid = sma(closes, period)
    upper: list[float | None] = [None] * len(closes)
    lower: list[float | None] = [None] * len(closes)
    for i in range(period - 1, len(closes)):
        if mid[i] is None:
            continue
        w = closes[i - period + 1 : i + 1]
        std = (sum((x - mid[i]) ** 2 for x in w) / period) ** 0.5
        upper[i] = round(mid[i] + std_dev * std, 2)
        lower[i] = round(mid[i] - std_dev * std, 2)
    return {"upper": upper, "middle": mid, "lower": lower}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 趋势分析引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TREND_MAP: dict[str, dict] = {
    "strong_up": {"label": "强势上涨", "emoji": "🚀🚀"},
    "up": {"label": "上涨趋势", "emoji": "🚀"},
    "oscillate_to_up": {"label": "震荡转上涨", "emoji": "📈"},
    "oscillate": {"label": "横盘震荡", "emoji": "➡️"},
    "oscillate_to_down": {"label": "震荡转下跌", "emoji": "📉"},
    "down": {"label": "下跌趋势", "emoji": "💀"},
    "strong_down": {"label": "强势下跌", "emoji": "💀💀"},
}


def analyze_trend(klines: list[dict], timeframe: str) -> dict:
    """
    分析单一周期的趋势

    Args:
        klines: K 线列表，每个元素含 open/high/low/close/volume
        timeframe: 1h / 4h / 1d / 1w

    Returns:
        趋势分析结果字典
    """
    if not klines or len(klines) < 30:
        return {"error": "数据不足，需要至少30根K线"}

    closes = [k["close"] for k in klines]
    highs = [k["high"] for k in klines]
    lows = [k["low"] for k in klines]
    volumes = [k["volume"] for k in klines]
    price = closes[-1]
    idx = len(closes) - 1
    prev = idx - 1

    # 计算指标
    ma7_v = sma(closes, 7)
    ma25_v = sma(closes, 25)
    ma99_v = sma(closes, 99) if len(closes) >= 99 else [None] * len(closes)
    rsi_v = rsi(closes, 14)
    macd_d = macd(closes)
    bb = bollinger_bands(closes)
    vol_ma = sma(volumes, 20)

    # ── 评分 (-100 ~ 100) ────────────────────────────────
    score = 0.0

    # 1) 均线排列 (权重 30)
    if ma7_v[idx] and ma25_v[idx]:
        if ma99_v[idx]:
            if ma7_v[idx] > ma25_v[idx] > ma99_v[idx]:
                score += 30
            elif ma7_v[idx] < ma25_v[idx] < ma99_v[idx]:
                score -= 30
            elif ma7_v[idx] > ma25_v[idx]:
                score += 15
            else:
                score -= 15
        else:
            score += 20 if ma7_v[idx] > ma25_v[idx] else -20

    # 2) RSI (权重 20)
    rv = rsi_v[idx]
    if rv is not None:
        if rv > 70:
            score += 12
        elif rv > 55:
            score += 20
        elif rv > 45:
            pass
        elif rv > 30:
            score -= 20
        else:
            score -= 12

    # 3) MACD (权重 25)
    mh = macd_d["histogram"]
    if mh[idx] is not None and mh[prev] is not None:
        if mh[prev] <= 0 < mh[idx]:
            score += 25  # 金叉
        elif mh[prev] >= 0 > mh[idx]:
            score -= 25  # 死叉
        elif mh[idx] > 0:
            score += 10
        else:
            score -= 10

    # 4) 价格动量 (权重 25)
    rec = closes[-10:]
    if len(rec) >= 10:
        n = len(rec)
        xm = (n - 1) / 2
        ym = sum(rec) / n
        num = sum((i - xm) * (rec[i] - ym) for i in range(n))
        den = sum((i - xm) ** 2 for i in range(n))
        if den:
            slope_pct = (num / den) / ym * 100
            score += max(-25, min(25, slope_pct * 8))

    # ── 映射趋势 ─────────────────────────────────────────
    if score >= 55:
        st = "strong_up"
    elif score >= 25:
        st = "up"
    elif score >= 8:
        st = "oscillate_to_up"
    elif score >= -8:
        st = "oscillate"
    elif score >= -25:
        st = "oscillate_to_down"
    elif score >= -55:
        st = "down"
    else:
        st = "strong_down"

    info = TREND_MAP[st]

    # ── 支撑阻力 ─────────────────────────────────────────
    resistance: list[float] = []
    support: list[float] = []

    if bb["upper"][idx]:
        resistance.append(round(bb["upper"][idx], 2))
    if bb["lower"][idx]:
        support.append(round(bb["lower"][idx], 2))
    for mv in [ma7_v[idx], ma25_v[idx], ma99_v[idx]]:
        if mv is None:
            continue
        if mv > price * 1.001:
            resistance.append(round(mv, 2))
        elif mv < price * 0.999:
            support.append(round(mv, 2))
    for h in sorted(highs[-50:], reverse=True)[:3]:
        if h > price * 1.001:
            resistance.append(round(h, 2))
    for lo in sorted(lows[-50:])[:3]:
        if lo < price * 0.999:
            support.append(round(lo, 2))

    resistance = sorted(set(resistance))[:3]
    support = sorted(set(support), reverse=True)[:3]
    while len(resistance) < 3:
        resistance.append(
            round((resistance[-1] if resistance else price) * 1.025, 2)
        )
    while len(support) < 3:
        support.append(
            round((support[-1] if support else price) * 0.975, 2)
        )

    # ── 变盘价格 & 时间 ──────────────────────────────────
    atr_vals: list[float] = []
    for i in range(1, min(15, len(klines))):
        tr = max(
            highs[-i] - lows[-i],
            abs(highs[-i] - closes[-i - 1]),
            abs(lows[-i] - closes[-i - 1]),
        )
        atr_vals.append(tr)
    atr14 = sum(atr_vals) / len(atr_vals) if atr_vals else price * 0.02
    pivot_price = round(
        price - atr14 * 1.5 if score > 0 else price + atr14 * 1.5, 2
    )
    tf_h = {"1h": 3, "4h": 12, "1d": 48, "1w": 168}
    pivot_time = (
        datetime.now() + timedelta(hours=tf_h.get(timeframe, 12))
    ).strftime("%m-%d %H:%M")

    # ── 置信度 ────────────────────────────────────────────
    conf = 50.0 + min(abs(score), 30)
    if vol_ma[idx] and volumes[-1] > vol_ma[idx] * 1.3:
        conf += 10
    if mh[idx] is not None and mh[prev] is not None:
        if (mh[prev] <= 0 < mh[idx]) or (mh[prev] >= 0 > mh[idx]):
            conf += 8
    conf = min(conf, 92)

    return {
        "timeframe": timeframe,
        "trend_status": st,
        "trend_label": info["label"],
        "trend_emoji": info["emoji"],
        "pivot_price": pivot_price,
        "pivot_time": pivot_time,
        "resistance": resistance,
        "support": support,
        "current_price": price,
        "rsi_14": rv,
        "macd_signal": "金叉" if (mh[idx] and mh[idx] > 0) else "死叉",
        "score": round(score, 1),
        "confidence": round(conf, 1),
    }
