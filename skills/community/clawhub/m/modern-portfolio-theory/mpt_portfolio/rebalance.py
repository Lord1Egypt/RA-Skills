"""Rebalancing logic — drift detection, order generation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd

from mpt_portfolio.config import Config
from mpt_portfolio.data import get_risk_free_rate
from mpt_portfolio.optimization import optimize
from mpt_portfolio.returns import compute_log_returns, get_expected_returns
from mpt_portfolio.risk import get_covariance
from mpt_portfolio.tracker import (
    PortfolioState,
    compute_current_value,
    load_state,
    save_state,
)


@dataclass
class TradeOrder:
    ticker: str
    action: str  # BUY or SELL
    shares: float
    shares_rounded: int
    dollar_amount: float
    current_weight: float
    target_weight: float
    weight_change: float


@dataclass
class RebalanceCheck:
    needs_rebalance: bool
    reason: str
    max_drift: float
    max_drift_asset: str
    current_weights: pd.Series
    target_weights: pd.Series
    orders: list[TradeOrder]
    estimated_cost: float


def generate_orders(
    current_weights: pd.Series,
    target_weights: pd.Series,
    total_portfolio_value: float,
    current_prices: pd.Series,
    transaction_cost_rate: float,
) -> list[TradeOrder]:
    """Calculate shares to buy/sell for each asset."""
    orders = []
    all_tickers = set(current_weights.index) | set(target_weights.index)

    for ticker in sorted(all_tickers):
        cw = current_weights.get(ticker, 0.0)
        tw = target_weights.get(ticker, 0.0)
        delta_weight = tw - cw

        if abs(delta_weight) < 0.001:
            continue

        delta_value = delta_weight * total_portfolio_value
        price = current_prices.get(ticker, 0)
        if price <= 0:
            continue

        shares = delta_value / price
        action = "BUY" if delta_value > 0 else "SELL"

        orders.append(TradeOrder(
            ticker=ticker,
            action=action,
            shares=abs(shares),
            shares_rounded=int(abs(shares)),
            dollar_amount=delta_value,
            current_weight=cw,
            target_weight=tw,
            weight_change=delta_weight,
        ))

    return orders


def check_rebalance(
    portfolio_name: str,
    config: Config,
    prices: pd.DataFrame,
) -> RebalanceCheck:
    """Check if rebalancing is needed and generate orders if so."""
    state = load_state(portfolio_name)
    if state is None:
        return RebalanceCheck(
            needs_rebalance=False, reason="No portfolio state found.",
            max_drift=0.0, max_drift_asset="N/A",
            current_weights=pd.Series(dtype=float),
            target_weights=pd.Series(dtype=float),
            orders=[], estimated_cost=0.0,
        )

    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    latest_prices = prices[asset_tickers].iloc[-1]
    total_value, current_weights = compute_current_value(state, latest_prices)

    # Re-optimize with latest data to get fresh target weights
    risk_free_rate = get_risk_free_rate(config.optimization.risk_free_rate)
    log_returns = compute_log_returns(prices[asset_tickers])
    mu = get_expected_returns(log_returns, config.optimization.expected_returns)
    cov = get_covariance(log_returns, config.optimization.covariance)

    opt_method = config.optimization.method
    if opt_method == "efficient_frontier":
        opt_method = "max_sharpe"

    result = optimize(mu, cov, risk_free_rate, opt_method, config.optimization.constraints)
    if hasattr(result, "max_sharpe_portfolio"):
        result = result.max_sharpe_portfolio

    target_weights = result.weights.reindex(asset_tickers, fill_value=0.0)
    target_weights = target_weights / target_weights.sum()

    # Compute drift
    aligned_current = current_weights.reindex(target_weights.index, fill_value=0.0)
    drifts = (aligned_current - target_weights).abs()
    max_drift = float(drifts.max())
    max_drift_asset = str(drifts.idxmax())

    # Decide if rebalance needed based on strategy
    strategy = config.rebalancing.strategy
    threshold = config.backtest.dynamic_threshold

    if strategy == "dynamic" or strategy == "recommended":
        needs_rebalance = max_drift > threshold
        reason = f"Weight drift {max_drift:.2%} exceeds threshold {threshold:.2%}" if needs_rebalance else "Within threshold"
    else:
        needs_rebalance = max_drift > threshold
        reason = f"Weight drift {max_drift:.2%} exceeds threshold {threshold:.2%}" if needs_rebalance else "Within threshold"

    orders = []
    estimated_cost = 0.0
    if needs_rebalance:
        orders = generate_orders(
            aligned_current, target_weights, total_value,
            latest_prices, config.backtest.transaction_cost,
        )
        turnover = sum(abs(o.weight_change) for o in orders) / 2.0
        estimated_cost = turnover * total_value * config.backtest.transaction_cost

    return RebalanceCheck(
        needs_rebalance=needs_rebalance,
        reason=reason,
        max_drift=max_drift,
        max_drift_asset=max_drift_asset,
        current_weights=aligned_current,
        target_weights=target_weights,
        orders=orders,
        estimated_cost=estimated_cost,
    )


def apply_rebalance(
    portfolio_name: str,
    orders: list[TradeOrder],
    target_weights: pd.Series,
    current_prices: pd.Series,
    optimization_method: str,
    estimated_cost: float,
) -> None:
    """Update state.json with new holdings after rebalance."""
    state = load_state(portfolio_name)
    if state is None:
        return

    total_value, _ = compute_current_value(state, current_prices)
    total_value -= estimated_cost
    state.cash = 0.0

    new_holdings = {}
    for ticker, weight in target_weights.items():
        if abs(weight) < 0.001:
            continue
        price = current_prices.get(ticker, 0)
        if price <= 0:
            continue
        alloc = total_value * weight
        shares = alloc / price
        new_holdings[ticker] = {
            "shares": round(shares, 6),
            "cost_basis": round(price, 4),
        }

    invested = sum(
        h["shares"] * current_prices.get(t, 0)
        for t, h in new_holdings.items()
    )
    state.holdings = new_holdings
    state.cash = round(total_value - invested, 2)
    state.target_weights = {k: round(float(v), 6) for k, v in target_weights.items() if abs(v) > 0.001}
    state.optimization_method = optimization_method
    state.optimization_date = datetime.now(timezone.utc).isoformat()

    state.rebalance_history.append({
        "date": datetime.now(timezone.utc).isoformat(),
        "strategy": optimization_method,
        "turnover": round(sum(abs(o.weight_change) for o in orders) / 2.0, 4),
        "transaction_cost": round(estimated_cost, 2),
        "orders": [
            {"ticker": o.ticker, "action": o.action, "shares": o.shares_rounded, "amount": round(o.dollar_amount, 2)}
            for o in orders
        ],
    })

    save_state(portfolio_name, state)
