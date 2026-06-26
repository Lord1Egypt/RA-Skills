#!/usr/bin/env python3
"""
Compute trading signal from technical features.
Input (stdin JSON):
  {
    "features_1h": {...},    ← primary timeframe (from compute_features)
    "features_4h": {...},    ← higher timeframe context
    "features_5m": {...},    ← entry timing (optional)
    "allow_short": bool,
    "position": null | {"side": "BUY"|"SELL", "quantity": float, ...}
  }

Output:
  {
    "signal": "long"|"short"|"wait"|"hold"|"close",
    "reason": str,
    "confidence": float   ← 0.0–1.0
  }
"""
import json
import sys


def score_long(f1h: dict, f4h: dict, f5m: dict | None) -> tuple[float, list[str]]:
    """Score a long setup. Returns (score 0-1, reasons)."""
    score = 0.0
    reasons = []
    total = 0

    # 4H trend alignment (weight 2)
    if f4h.get("trend") == "up":
        score += 2
        reasons.append("4H_trend_up")
    total += 2

    # 1H trend (weight 2)
    if f1h.get("trend") == "up":
        score += 2
        reasons.append("1H_trend_up")
    total += 2

    # 1H momentum / RSI (weight 1.5) — RSI 45–68 is ideal for longs
    rsi = f1h.get("rsi14")
    if rsi is not None:
        if 45 <= rsi <= 68:
            score += 1.5
            reasons.append(f"RSI_long_zone:{rsi:.1f}")
        elif rsi > 75:
            reasons.append(f"RSI_overbought:{rsi:.1f}")
    total += 1.5

    # MACD bullish (weight 1)
    macd = f1h.get("macd")
    macd_sig = f1h.get("macd_signal")
    if macd is not None and macd_sig is not None and macd > macd_sig:
        score += 1
        reasons.append("MACD_bullish")
    total += 1

    # 5M timing (weight 0.5) — if available
    if f5m:
        if f5m.get("trend") == "up" or f5m.get("momentum") == "up":
            score += 0.5
            reasons.append("5M_timing_up")
    total += 0.5

    # Volume confirmation (weight 1)
    vol_ratio = f1h.get("volume_ratio", 0)
    if vol_ratio >= 0.8:
        score += 1
        reasons.append(f"volume_ok:{vol_ratio:.2f}")
    total += 1

    # Price above EMA20 (weight 1)
    price = f1h.get("last_price", 0)
    ema20 = f1h.get("ema20")
    if ema20 and price > ema20:
        score += 1
        reasons.append("price_above_ema20")
    total += 1

    # Funding rate — negative funding favours longs (shorts pay longs) (weight 0.5)
    funding = f1h.get("funding_rate")
    if funding is not None:
        if funding < -0.0001:
            score += 0.5
            reasons.append(f"funding_favours_long:{funding:.6f}")
        elif funding > 0.001:
            reasons.append(f"funding_expensive_for_long:{funding:.6f}")
    total += 0.5

    return score / total if total > 0 else 0.0, reasons


def score_short(f1h: dict, f4h: dict, f5m: dict | None) -> tuple[float, list[str]]:
    """Score a short setup. Returns (score 0-1, reasons)."""
    score = 0.0
    reasons = []
    total = 0

    # 4H trend down (weight 2)
    if f4h.get("trend") == "down":
        score += 2
        reasons.append("4H_trend_down")
    total += 2

    # 1H trend down (weight 2)
    if f1h.get("trend") == "down":
        score += 2
        reasons.append("1H_trend_down")
    total += 2

    # RSI 32–55 for short entry (weight 1.5)
    rsi = f1h.get("rsi14")
    if rsi is not None:
        if 32 <= rsi <= 55:
            score += 1.5
            reasons.append(f"RSI_short_zone:{rsi:.1f}")
        elif rsi < 25:
            reasons.append(f"RSI_oversold:{rsi:.1f}")
    total += 1.5

    # MACD bearish (weight 1)
    macd = f1h.get("macd")
    macd_sig = f1h.get("macd_signal")
    if macd is not None and macd_sig is not None and macd < macd_sig:
        score += 1
        reasons.append("MACD_bearish")
    total += 1

    # 5M timing (weight 0.5)
    if f5m:
        if f5m.get("trend") == "down" or f5m.get("momentum") == "down":
            score += 0.5
            reasons.append("5M_timing_down")
    total += 0.5

    # Volume (weight 1)
    vol_ratio = f1h.get("volume_ratio", 0)
    if vol_ratio >= 0.8:
        score += 1
        reasons.append(f"volume_ok:{vol_ratio:.2f}")
    total += 1

    # Price below EMA20 (weight 1)
    price = f1h.get("last_price", 0)
    ema20 = f1h.get("ema20")
    if ema20 and price < ema20:
        score += 1
        reasons.append("price_below_ema20")
    total += 1

    # Funding rate — positive funding favours shorts (longs pay shorts) (weight 0.5)
    funding = f1h.get("funding_rate")
    if funding is not None:
        if funding > 0.0001:
            score += 0.5
            reasons.append(f"funding_favours_short:{funding:.6f}")
        elif funding < -0.001:
            reasons.append(f"funding_expensive_for_short:{funding:.6f}")
    total += 0.5

    return score / total if total > 0 else 0.0, reasons


def main() -> int:
    payload = json.load(sys.stdin)
    f1h = payload.get("features_1h") or payload.get("features") or {}
    f4h = payload.get("features_4h") or f1h
    f5m = payload.get("features_5m")
    allow_short = bool(payload.get("allow_short", True))
    position = payload.get("position")

    # If we have an existing position, check hold/close logic
    if position:
        side = position.get("side", "")
        pnl_pct = float(position.get("unrealised_pnl_pct", 0))

        # Close if position is going against trend
        pos_is_long = side.upper() in ("BUY", "LONG")
        current_trend_1h = f1h.get("trend", "neutral")
        current_trend_4h = f4h.get("trend", "neutral")
        rsi_v = f1h.get("rsi14")

        # Hard close signals
        should_close = False
        close_reason = ""

        if pos_is_long and current_trend_1h == "down" and current_trend_4h == "down":
            should_close = True
            close_reason = "trend_reversed_bearish"
        elif not pos_is_long and current_trend_1h == "up" and current_trend_4h == "up":
            should_close = True
            close_reason = "trend_reversed_bullish"
        elif pos_is_long and rsi_v and rsi_v > 78:
            should_close = True
            close_reason = "rsi_overbought_exit"
        elif not pos_is_long and rsi_v and rsi_v < 22:
            should_close = True
            close_reason = "rsi_oversold_exit"

        if should_close:
            print(json.dumps({"signal": "close", "reason": close_reason, "confidence": 0.9}))
            return 0

        print(json.dumps({"signal": "hold", "reason": "position_within_parameters", "confidence": 0.5}))
        return 0

    # No existing position — look for entry
    CONFIDENCE_THRESHOLD = 0.55

    long_score, long_reasons = score_long(f1h, f4h, f5m)
    short_score, short_reasons = score_short(f1h, f4h, f5m)

    # Avoid trading in high volatility unless confidence is high
    if f1h.get("high_volatility") and max(long_score, short_score) < 0.70:
        print(json.dumps({
            "signal": "wait",
            "reason": "high_volatility_low_confidence",
            "confidence": max(long_score, short_score)
        }))
        return 0

    if long_score >= short_score and long_score >= CONFIDENCE_THRESHOLD:
        print(json.dumps({
            "signal": "long",
            "reason": ", ".join(long_reasons),
            "confidence": long_score
        }))
    elif allow_short and short_score > long_score and short_score >= CONFIDENCE_THRESHOLD:
        print(json.dumps({
            "signal": "short",
            "reason": ", ".join(short_reasons),
            "confidence": short_score
        }))
    else:
        best = max(long_score, short_score)
        print(json.dumps({
            "signal": "wait",
            "reason": f"insufficient_confluence (long={long_score:.2f} short={short_score:.2f})",
            "confidence": best
        }))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
