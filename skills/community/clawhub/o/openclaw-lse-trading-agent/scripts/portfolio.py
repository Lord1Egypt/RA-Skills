"""Portfolio tracker with CRUD operations and live price fetching.

Manages a local JSON portfolio file with positions, cash tracking,
and live P&L calculations via yfinance.

Usage:
    uv run scripts/portfolio.py --init 50000
    uv run scripts/portfolio.py --show
    uv run scripts/portfolio.py --add HSBA.L 100 678.5
    uv run scripts/portfolio.py --remove HSBA.L
    uv run scripts/portfolio.py --summary
    uv run scripts/portfolio.py --show --file path/to/portfolio.json
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import yfinance as yf

from config import RiskParams
from ftse350 import get_sector

RISK = RiskParams()
DEFAULT_PORTFOLIO = Path(__file__).resolve().parent.parent / "data" / "portfolio.json"


def _load(path: Path) -> dict:
    """Load portfolio from JSON file."""
    if not path.exists():
        print(json.dumps({"error": f"Portfolio file not found: {path}"}))
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def _save(data: dict, path: Path) -> None:
    """Save portfolio to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _normalize_ticker(ticker: str) -> str:
    """Append .L suffix if missing."""
    return ticker if "." in ticker else f"{ticker}.L"


def _fetch_price(ticker: str) -> float | None:
    """Fetch the latest price for a ticker via yfinance."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if hist.empty:
            return None
        return float(hist["Close"].iloc[-1])
    except Exception:
        return None


def init_portfolio(capital: float, path: Path) -> None:
    """Create a new portfolio with the given starting capital."""
    data = {
        "created": str(date.today()),
        "initial_capital": capital,
        "cash": capital,
        "positions": [],
    }
    _save(data, path)
    print(json.dumps(data, indent=2))


def show_portfolio(path: Path) -> None:
    """Show all positions with live prices and P&L."""
    data = _load(path)
    positions = data["positions"]
    cash = data["cash"]

    enriched = []
    total_invested = 0.0
    total_market_value = 0.0
    total_pnl = 0.0

    for pos in positions:
        ticker = pos["ticker"]
        shares = pos["shares"]
        entry_price = pos["entry_price"]

        current_price = _fetch_price(ticker)
        if current_price is None:
            current_price = entry_price  # fallback if fetch fails

        cost_basis = shares * entry_price
        market_value = shares * current_price
        pnl = market_value - cost_basis
        pnl_pct = (pnl / cost_basis * 100) if cost_basis != 0 else 0.0

        total_invested += cost_basis
        total_market_value += market_value
        total_pnl += pnl

        enriched.append({
            "ticker": ticker,
            "shares": shares,
            "entry_price": entry_price,
            "current_price": round(current_price, 2),
            "entry_date": pos["entry_date"],
            "sector": pos["sector"],
            "market_value": round(market_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 2),
        })

    total_value = cash + total_market_value
    unrealized_pnl_pct = (total_pnl / total_invested * 100) if total_invested != 0 else 0.0

    # Sector exposure as % of total portfolio value
    sector_values: dict[str, float] = {}
    for p in enriched:
        sector_values[p["sector"]] = sector_values.get(p["sector"], 0.0) + p["market_value"]
    sector_exposure = {
        s: round(v / total_value * 100, 2) if total_value else 0.0
        for s, v in sorted(sector_values.items())
    }

    result = {
        "total_value": round(total_value, 2),
        "cash": round(cash, 2),
        "invested": round(total_market_value, 2),
        "unrealized_pnl": round(total_pnl, 2),
        "unrealized_pnl_pct": round(unrealized_pnl_pct, 2),
        "positions": enriched,
        "sector_exposure": sector_exposure,
        "position_count": len(enriched),
    }
    print(json.dumps(result, indent=2))


def add_position(ticker: str, shares: int, price: float, path: Path) -> None:
    """Add a position to the portfolio."""
    ticker = _normalize_ticker(ticker)
    data = _load(path)

    sector = get_sector(ticker)
    if sector is None:
        print(json.dumps({"error": f"Ticker {ticker} not found in FTSE 350 list"}))
        sys.exit(1)

    # Cost includes SDRT (stamp duty)
    total_cost = shares * price * (1 + RISK.sdrt_rate)

    if total_cost > data["cash"]:
        print(json.dumps({
            "error": "Insufficient cash",
            "required": round(total_cost, 2),
            "available": round(data["cash"], 2),
        }))
        sys.exit(1)

    data["cash"] -= total_cost
    data["positions"].append({
        "ticker": ticker,
        "shares": shares,
        "entry_price": price,
        "entry_date": str(date.today()),
        "sector": sector,
    })

    _save(data, path)
    print(json.dumps({
        "action": "added",
        "ticker": ticker,
        "shares": shares,
        "entry_price": price,
        "cost_with_sdrt": round(total_cost, 2),
        "remaining_cash": round(data["cash"], 2),
        "sector": sector,
    }, indent=2))


def remove_position(ticker: str, path: Path) -> None:
    """Remove a position (sell all shares) from the portfolio."""
    ticker = _normalize_ticker(ticker)
    data = _load(path)

    # Find the position
    pos_idx = None
    for i, pos in enumerate(data["positions"]):
        if pos["ticker"] == ticker:
            pos_idx = i
            break

    if pos_idx is None:
        print(json.dumps({"error": f"Position {ticker} not found in portfolio"}))
        sys.exit(1)

    pos = data["positions"][pos_idx]
    current_price = _fetch_price(ticker)
    if current_price is None:
        print(json.dumps({"error": f"Could not fetch price for {ticker}"}))
        sys.exit(1)

    # Proceeds after slippage deduction
    proceeds = pos["shares"] * current_price * (1 - RISK.estimated_slippage)
    cost_basis = pos["shares"] * pos["entry_price"]
    realized_pnl = proceeds - cost_basis

    data["cash"] += proceeds
    data["positions"].pop(pos_idx)

    _save(data, path)
    print(json.dumps({
        "action": "removed",
        "ticker": ticker,
        "shares": pos["shares"],
        "sell_price": round(current_price, 2),
        "proceeds_after_slippage": round(proceeds, 2),
        "realized_pnl": round(realized_pnl, 2),
        "cash": round(data["cash"], 2),
    }, indent=2))


def summary(path: Path) -> None:
    """Print a quick one-line summary of the portfolio."""
    data = _load(path)
    positions = data["positions"]
    cash = data["cash"]

    total_market_value = 0.0
    total_cost = 0.0
    for pos in positions:
        current_price = _fetch_price(pos["ticker"])
        if current_price is None:
            current_price = pos["entry_price"]
        total_market_value += pos["shares"] * current_price
        total_cost += pos["shares"] * pos["entry_price"]

    total_value = cash + total_market_value
    pnl = total_market_value - total_cost
    pnl_pct = (pnl / total_cost * 100) if total_cost != 0 else 0.0

    print(
        f"Total: {total_value:,.2f} | "
        f"Cash: {cash:,.2f} | "
        f"Invested: {total_market_value:,.2f} | "
        f"P&L: {pnl:+,.2f} ({pnl_pct:+.2f}%) | "
        f"Positions: {len(positions)}"
    )


def main():
    parser = argparse.ArgumentParser(description="Portfolio tracker for LSE Trading Agent")
    parser.add_argument("--file", type=Path, default=DEFAULT_PORTFOLIO, help="Portfolio JSON file path")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", type=float, metavar="CAPITAL", help="Create new portfolio with starting capital")
    group.add_argument("--show", action="store_true", help="Show positions with live prices and P&L")
    group.add_argument("--add", nargs=3, metavar=("TICKER", "SHARES", "PRICE"), help="Add a position")
    group.add_argument("--remove", metavar="TICKER", help="Remove a position (sell all)")
    group.add_argument("--summary", action="store_true", help="Quick one-line summary")

    args = parser.parse_args()
    path = args.file

    if args.init is not None:
        init_portfolio(args.init, path)
    elif args.show:
        show_portfolio(path)
    elif args.add:
        ticker, shares_str, price_str = args.add
        add_position(ticker, int(shares_str), float(price_str), path)
    elif args.remove:
        remove_position(args.remove, path)
    elif args.summary:
        summary(path)


if __name__ == "__main__":
    main()
