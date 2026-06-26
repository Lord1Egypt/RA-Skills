"""Portfolio state persistence — holdings, performance history."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from mpt_portfolio.utils import get_portfolios_dir


@dataclass
class PortfolioState:
    created_at: str = ""
    last_updated: str = ""
    initial_investment: float = 0.0
    holdings: dict[str, dict] = field(default_factory=dict)
    cash: float = 0.0
    target_weights: dict[str, float] = field(default_factory=dict)
    optimization_method: str = ""
    optimization_date: str = ""
    rebalance_history: list[dict] = field(default_factory=list)
    performance_history: list[dict] = field(default_factory=list)


def _state_path(portfolio_name: str) -> Path:
    return get_portfolios_dir() / portfolio_name / "state.json"


def load_state(portfolio_name: str) -> PortfolioState | None:
    path = _state_path(portfolio_name)
    if not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    return PortfolioState(**{
        k: data.get(k, default)
        for k, default in PortfolioState().__dict__.items()
    })


def save_state(portfolio_name: str, state: PortfolioState) -> Path:
    state.last_updated = datetime.now(timezone.utc).isoformat()
    path = _state_path(portfolio_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(asdict(state), f, indent=2, default=str)
    return path


def initialize_state(
    portfolio_name: str,
    initial_investment: float,
    weights: pd.Series,
    prices: pd.Series,
    optimization_method: str,
) -> PortfolioState:
    """Create initial state: buy shares according to weights and current prices."""
    now = datetime.now(timezone.utc).isoformat()
    holdings = {}
    total_invested = 0.0

    for ticker, weight in weights.items():
        if abs(weight) < 0.001:
            continue
        alloc = initial_investment * weight
        price = prices.get(ticker, 0)
        if price > 0:
            shares = alloc / price
            holdings[ticker] = {"shares": round(shares, 6), "cost_basis": round(price, 4)}
            total_invested += shares * price

    cash = initial_investment - total_invested

    state = PortfolioState(
        created_at=now,
        last_updated=now,
        initial_investment=initial_investment,
        holdings=holdings,
        cash=round(cash, 2),
        target_weights={k: round(float(v), 6) for k, v in weights.items() if abs(v) > 0.001},
        optimization_method=optimization_method,
        optimization_date=now,
        rebalance_history=[],
        performance_history=[{
            "date": now[:10],
            "portfolio_value": round(initial_investment, 2),
        }],
    )

    save_state(portfolio_name, state)
    return state


def compute_current_value(
    state: PortfolioState,
    current_prices: pd.Series,
) -> tuple[float, pd.Series]:
    """Compute total portfolio value and current weights."""
    values = {}
    for ticker, holding in state.holdings.items():
        price = current_prices.get(ticker, 0)
        values[ticker] = holding["shares"] * price

    total = sum(values.values()) + state.cash
    if total <= 0:
        weights = pd.Series(0.0, index=list(state.holdings.keys()))
    else:
        weights = pd.Series({t: v / total for t, v in values.items()})

    return total, weights


def update_performance_history(
    portfolio_name: str,
    current_prices: pd.Series,
    benchmark_price: float | None = None,
) -> None:
    """Append today's snapshot to performance history."""
    state = load_state(portfolio_name)
    if state is None:
        return

    total_value, _ = compute_current_value(state, current_prices)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    entry = {"date": today, "portfolio_value": round(total_value, 2)}
    if benchmark_price is not None:
        entry["benchmark_price"] = round(benchmark_price, 4)

    # Avoid duplicate entries for same date
    if state.performance_history and state.performance_history[-1].get("date") == today:
        state.performance_history[-1] = entry
    else:
        state.performance_history.append(entry)

    save_state(portfolio_name, state)
