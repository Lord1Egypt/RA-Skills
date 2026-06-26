"""Risk validator and position sizer for LSE trading.

Validates proposed trades against risk rules and computes position sizing
using half-Kelly criterion and ATR-based stop losses.

Usage:
    uv run scripts/risk.py --action BUY --ticker HSBA.L --price 678.5 --portfolio-value 50000
    uv run scripts/risk.py --check-exposure --portfolio-file data/portfolio.json
"""

import argparse
import json
import math
import sys
from pathlib import Path

from config import RiskParams
from indicators import fetch_ohlcv, compute_indicators


def load_portfolio(portfolio_path: str) -> dict | None:
    """Load portfolio JSON file, returning None if it doesn't exist."""
    path = Path(portfolio_path)
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def compute_kelly_size(
    portfolio_value: float,
    risk_params: RiskParams,
    win_rate: float = 0.55,
    payoff_ratio: float = 2.0,
) -> float:
    """Compute half-Kelly position size as fraction of portfolio.

    Returns the recommended position value (not shares).
    """
    kelly_raw = win_rate - (1 - win_rate) / payoff_ratio
    kelly_raw = max(kelly_raw, 0.0)  # never negative
    kelly_adj = risk_params.kelly_fraction * kelly_raw
    position_value = kelly_adj * portfolio_value
    # Cap at max_position_pct
    max_value = risk_params.max_position_pct * portfolio_value
    return min(position_value, max_value)


def compute_stop_loss(price: float, atr: float, risk_params: RiskParams, action: str) -> float:
    """Compute ATR-based stop loss price."""
    if action == "BUY":
        return price - (atr * risk_params.atr_stop_multiplier)
    else:  # SELL / short
        return price + (atr * risk_params.atr_stop_multiplier)


def get_atr_for_ticker(ticker: str) -> float | None:
    """Fetch current ATR for a ticker. Returns None on failure."""
    try:
        df = fetch_ohlcv(ticker, period="3mo", interval="1d")
        result = compute_indicators(df)
        return result["indicators"]["atr"]
    except Exception:
        return None


def validate_trade(
    action: str,
    ticker: str,
    price: float,
    portfolio_value: float,
    portfolio: dict | None = None,
    risk_params: RiskParams | None = None,
    win_rate: float = 0.55,
    payoff_ratio: float = 2.0,
) -> dict:
    """Validate a proposed trade against risk rules and compute sizing."""
    if risk_params is None:
        risk_params = RiskParams()

    checks = {}

    # Compute Kelly position size
    position_value = compute_kelly_size(portfolio_value, risk_params, win_rate, payoff_ratio)
    position_pct = position_value / portfolio_value * 100
    max_pct = risk_params.max_position_pct * 100

    checks["position_size"] = {
        "pass": position_pct <= max_pct,
        "detail": f"{position_pct:.1f}% < {max_pct:.1f}% max"
        if position_pct <= max_pct
        else f"{position_pct:.1f}% exceeds {max_pct:.1f}% max",
    }

    # Fetch ATR for stop loss
    atr = get_atr_for_ticker(ticker)
    if atr is not None and atr > 0:
        stop_loss_price = compute_stop_loss(price, atr, risk_params, action)
        risk_per_share = abs(price - stop_loss_price)
        shares = math.floor(position_value / price)
        risk_amount = risk_per_share * shares
        risk_pct = risk_amount / portfolio_value * 100
        max_risk_pct = risk_params.max_risk_per_trade * 100

        # If risk exceeds limit, reduce shares
        if risk_pct > max_risk_pct:
            max_risk_amount = risk_params.max_risk_per_trade * portfolio_value
            shares = math.floor(max_risk_amount / risk_per_share)
            position_value = shares * price
            risk_amount = risk_per_share * shares
            risk_pct = risk_amount / portfolio_value * 100

        checks["risk_per_trade"] = {
            "pass": risk_pct <= max_risk_pct,
            "detail": f"{risk_pct:.1f}% < {max_risk_pct:.1f}% max"
            if risk_pct <= max_risk_pct
            else f"{risk_pct:.1f}% exceeds {max_risk_pct:.1f}% max",
        }
    else:
        stop_loss_price = None
        shares = math.floor(position_value / price)
        checks["risk_per_trade"] = {
            "pass": True,
            "detail": "ATR unavailable — skipped risk-per-trade check",
        }

    # Portfolio-dependent checks
    if portfolio is not None:
        positions = portfolio.get("positions", [])

        # Sector exposure
        sector_values: dict[str, float] = {}
        total_value = portfolio.get("total_value", portfolio_value)
        for pos in positions:
            sector = pos.get("sector", "Unknown")
            val = pos.get("market_value", 0)
            sector_values[sector] = sector_values.get(sector, 0) + val

        # Find the sector for the new trade (if provided in portfolio metadata)
        new_sector = portfolio.get("ticker_sectors", {}).get(ticker, "Unknown")
        sector_values[new_sector] = sector_values.get(new_sector, 0) + position_value
        max_sector_pct = risk_params.max_sector_exposure * 100

        sector_exposure_pct = (
            sector_values[new_sector] / total_value * 100 if total_value > 0 else 0
        )
        checks["sector_exposure"] = {
            "pass": sector_exposure_pct <= max_sector_pct,
            "detail": f"{new_sector} at {sector_exposure_pct:.1f}% < {max_sector_pct:.1f}% max"
            if sector_exposure_pct <= max_sector_pct
            else f"{new_sector} at {sector_exposure_pct:.1f}% exceeds {max_sector_pct:.1f}% max",
        }

        # Open positions count
        position_count = len(positions)
        max_positions = risk_params.max_open_positions
        checks["open_positions"] = {
            "pass": position_count < max_positions,
            "detail": f"{position_count} < {max_positions} max"
            if position_count < max_positions
            else f"{position_count} at or exceeds {max_positions} max",
        }

        # Drawdown check
        peak_value = portfolio.get("peak_value", total_value)
        drawdown_pct = (
            (peak_value - total_value) / peak_value * 100 if peak_value > 0 else 0
        )
        max_dd_pct = risk_params.max_drawdown * 100
        checks["drawdown"] = {
            "pass": drawdown_pct <= max_dd_pct,
            "detail": f"{drawdown_pct:.1f}% < {max_dd_pct:.1f}% circuit breaker"
            if drawdown_pct <= max_dd_pct
            else f"{drawdown_pct:.1f}% exceeds {max_dd_pct:.1f}% circuit breaker",
        }
    else:
        checks["sector_exposure"] = {
            "pass": True,
            "detail": "No portfolio file — skipped",
        }
        checks["open_positions"] = {
            "pass": True,
            "detail": "No portfolio file — skipped",
        }
        checks["drawdown"] = {
            "pass": True,
            "detail": "No portfolio file — skipped",
        }

    all_pass = all(c["pass"] for c in checks.values())

    # Compute total cost with SDRT (stamp duty only on buys)
    actual_value = shares * price
    sdrt = actual_value * risk_params.sdrt_rate if action == "BUY" else 0
    total_cost = actual_value + sdrt

    kelly_raw = win_rate - (1 - win_rate) / payoff_ratio
    kelly_used = risk_params.kelly_fraction * max(kelly_raw, 0.0)

    result = {
        "action": action,
        "ticker": ticker,
        "price": price,
        "checks": checks,
        "all_pass": all_pass,
        "recommended_shares": shares,
        "recommended_value": round(actual_value, 2),
        "stop_loss_price": round(stop_loss_price, 2) if stop_loss_price is not None else None,
        "stop_loss_method": f"ATR x {risk_params.atr_stop_multiplier}",
        "total_cost_with_sdrt": round(total_cost, 2),
        "kelly_fraction_used": round(kelly_used, 4),
    }

    return result


def check_exposure(portfolio_path: str, risk_params: RiskParams | None = None) -> dict:
    """Check portfolio exposure against risk limits."""
    if risk_params is None:
        risk_params = RiskParams()

    portfolio = load_portfolio(portfolio_path)
    if portfolio is None:
        return {"error": f"Portfolio file not found: {portfolio_path}"}

    positions = portfolio.get("positions", [])
    total_value = portfolio.get("total_value", 0)
    peak_value = portfolio.get("peak_value", total_value)

    # Sector exposure breakdown
    sector_values: dict[str, float] = {}
    for pos in positions:
        sector = pos.get("sector", "Unknown")
        val = pos.get("market_value", 0)
        sector_values[sector] = sector_values.get(sector, 0) + val

    sector_exposure = {
        sector: round(val / total_value * 100, 1) if total_value > 0 else 0
        for sector, val in sector_values.items()
    }

    max_sector_pct = risk_params.max_sector_exposure * 100
    sectors_over_limit = [
        sector for sector, pct in sector_exposure.items() if pct > max_sector_pct
    ]

    drawdown_pct = (peak_value - total_value) / peak_value * 100 if peak_value > 0 else 0

    return {
        "sector_exposure": sector_exposure,
        "sectors_over_limit": sectors_over_limit,
        "position_count": len(positions),
        "max_positions": risk_params.max_open_positions,
        "estimated_drawdown_pct": round(drawdown_pct, 1),
        "circuit_breaker_triggered": drawdown_pct > risk_params.max_drawdown * 100,
    }


def main():
    parser = argparse.ArgumentParser(description="Risk validator and position sizer for LSE trading")

    # Mode 1: Trade validation
    parser.add_argument("--action", choices=["BUY", "SELL"], help="Trade action")
    parser.add_argument("--ticker", help="Yahoo Finance ticker (e.g., HSBA.L)")
    parser.add_argument("--price", type=float, help="Entry price")
    parser.add_argument("--portfolio-value", type=float, help="Total portfolio value")
    parser.add_argument("--win-rate", type=float, default=0.55, help="Estimated win rate")
    parser.add_argument("--payoff-ratio", type=float, default=2.0, help="Reward-to-risk ratio")

    # Mode 2: Exposure check
    parser.add_argument("--check-exposure", action="store_true", help="Check portfolio exposure")

    # Shared
    parser.add_argument("--portfolio-file", help="Path to portfolio JSON file")

    args = parser.parse_args()

    if args.check_exposure:
        if not args.portfolio_file:
            print(json.dumps({"error": "--portfolio-file required with --check-exposure"}))
            sys.exit(1)
        result = check_exposure(args.portfolio_file)
        print(json.dumps(result, indent=2))
    elif args.action and args.ticker and args.price and args.portfolio_value:
        ticker = args.ticker if "." in args.ticker else f"{args.ticker}.L"
        portfolio = load_portfolio(args.portfolio_file) if args.portfolio_file else None
        result = validate_trade(
            action=args.action,
            ticker=ticker,
            price=args.price,
            portfolio_value=args.portfolio_value,
            portfolio=portfolio,
            win_rate=args.win_rate,
            payoff_ratio=args.payoff_ratio,
        )
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
