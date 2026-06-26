#!/usr/bin/env python3
"""
Position Sizer - Calculates optimal position size based on confidence and risk.
Usage: python position_sizer.py [confidence] [account_balance] [stop_loss_pct]
"""
import sys
import json

def kelly_criterion(win_rate, avg_win, avg_loss):
    """Calculate Kelly position size fraction."""
    if avg_loss == 0 or win_rate <= 0 or win_rate >= 1:
        return 0.10  # conservative default
    b = avg_win / avg_loss
    p = win_rate
    q = 1 - p
    kelly = (b * p - q) / b
    return max(0.01, min(kelly, 0.20))  # cap at 20%

def calc_position_size(confidence, balance, stop_loss_pct, win_rate=0.55, avg_win_pct=3.0, avg_loss_pct=2.0):
    """
    Calculate position size in quote currency (e.g., USDT for BTC/USDT).

    Args:
        confidence: 0-100, trading-judge confidence
        balance: account balance in quote currency
        stop_loss_pct: stop loss as percentage (e.g., 3.0 for 3%)
        win_rate: historical win rate (default 0.55)
        avg_win_pct: average win percentage
        avg_loss_pct: average loss percentage

    Returns: {size_btc, size_usdt, risk_amount, risk_pct}
    """
    confidence_frac = confidence / 100.0

    # Kelly-based size
    kelly = kelly_criterion(win_rate, avg_win_pct, avg_loss_pct)

    # Confidence multiplier (low confidence = smaller size)
    confidence_multiplier = (confidence_frac ** 0.5)  # sqrt scaling

    # Risk fraction (account for stop loss distance)
    risk_fraction = kelly * confidence_multiplier

    # Cap at 20% of balance per trade
    max_fraction = 0.20
    risk_fraction = min(risk_fraction, max_fraction)

    # Calculate position
    position_value = balance * risk_fraction
    risk_amount = position_value * (stop_loss_pct / 100.0)
    risk_pct = risk_fraction * 100

    # Size in base currency (assuming BTCUSDT pair)
    btc_price = 67000  # fallback estimate
    size_btc = position_value / btc_price

    return {
        "position_value_usdt": round(position_value, 2),
        "position_size_btc": round(size_btc, 4),
        "risk_amount_usdt": round(risk_amount, 2),
        "risk_pct_of_balance": round(risk_pct, 2),
        "kelly_fraction": round(risk_fraction, 4),
        "confidence_adjusted": confidence_frac,
        "signal_strength": "STRONG" if confidence > 70 else "MODERATE" if confidence > 40 else "WEAK"
    }

if __name__ == "__main__":
    try:
        confidence = float(sys.argv[1]) if len(sys.argv) > 1 else 65
        balance = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
        stop_loss = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0

        result = calc_position_size(confidence, balance, stop_loss)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
