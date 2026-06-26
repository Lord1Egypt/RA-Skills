"""Walk-forward backtesting engine.

At each rebalance date, re-estimates parameters using only past data (no look-ahead).
Supports: monthly, quarterly, yearly, dynamic (threshold-based), and buy-and-hold.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

from mpt_portfolio.config import Config, ConstraintsConfig
from mpt_portfolio.data import get_risk_free_rate
from mpt_portfolio.metrics import (
    PerformanceMetrics,
    compare_metrics,
    compute_drawdown_series,
    compute_metrics,
    compute_rolling_sharpe,
)
from mpt_portfolio.optimization import (
    OptimizationResult,
    maximize_sharpe,
    minimize_variance,
    optimize,
    risk_parity,
)
from mpt_portfolio.returns import compute_log_returns, get_expected_returns
from mpt_portfolio.risk import get_covariance
from mpt_portfolio.utils import TRADING_DAYS_PER_YEAR

logger = logging.getLogger(__name__)


@dataclass
class RebalanceEvent:
    date: datetime
    old_weights: pd.Series | None
    new_weights: pd.Series
    turnover: float
    transaction_cost: float


@dataclass
class BacktestResult:
    strategy_name: str
    portfolio_values: pd.Series
    daily_returns: pd.Series
    weights_over_time: pd.DataFrame
    rebalance_events: list[RebalanceEvent]
    metrics: PerformanceMetrics
    total_turnover: float
    total_transaction_costs: float


@dataclass
class BacktestComparison:
    results: dict[str, BacktestResult]
    benchmark_result: BacktestResult
    recommended_strategy: str
    recommendation_reason: str


def generate_rebalance_dates(
    start_date: datetime,
    end_date: datetime,
    frequency: str,
    trading_dates: pd.DatetimeIndex,
) -> list[datetime]:
    """Generate rebalance dates aligned to actual trading days."""
    trading_dates = trading_dates[(trading_dates >= start_date) & (trading_dates <= end_date)]

    if frequency == "monthly":
        months = trading_dates.to_period("M").unique()
        dates = []
        for m in months:
            month_dates = trading_dates[(trading_dates.month == m.month) & (trading_dates.year == m.year)]
            if len(month_dates) > 0:
                dates.append(month_dates[0])
        return dates

    elif frequency == "quarterly":
        quarters = trading_dates.to_period("Q").unique()
        dates = []
        for q in quarters:
            q_dates = trading_dates[(trading_dates.quarter == q.quarter) & (trading_dates.year == q.year)]
            if len(q_dates) > 0:
                dates.append(q_dates[0])
        return dates

    elif frequency == "yearly":
        years = trading_dates.year.unique()
        dates = []
        for y in years:
            y_dates = trading_dates[trading_dates.year == y]
            if len(y_dates) > 0:
                dates.append(y_dates[0])
        return dates

    else:
        raise ValueError(f"Unknown rebalance frequency: {frequency}")


def _check_dynamic_rebalance(
    current_weights: pd.Series,
    prices_window: pd.DataFrame,
    method: str,
    expected_returns_method: str,
    covariance_method: str,
    risk_free_rate: float,
    constraints: ConstraintsConfig,
    threshold: float,
) -> tuple[bool, OptimizationResult | None]:
    """Re-run optimizer on current data; trigger if portfolio distance exceeds threshold."""
    result = _run_optimization(
        prices_window, method, expected_returns_method,
        covariance_method, risk_free_rate, constraints,
    )
    if result is None:
        return False, None
    fresh_weights = result.weights.reindex(current_weights.index, fill_value=0.0)
    fresh_weights = fresh_weights / fresh_weights.sum()
    distance = float((current_weights - fresh_weights).abs().sum()) / 2.0
    return distance > threshold, result


def _run_optimization(
    prices_window: pd.DataFrame,
    method: str,
    expected_returns_method: str,
    covariance_method: str,
    risk_free_rate: float,
    constraints: ConstraintsConfig,
) -> OptimizationResult | None:
    """Run optimization on a lookback window of prices. Returns None on failure."""
    try:
        log_returns = compute_log_returns(prices_window)
        if len(log_returns) < 30:
            return None
        mu = get_expected_returns(log_returns, expected_returns_method)
        cov = get_covariance(log_returns, covariance_method)
        result = optimize(mu, cov, risk_free_rate, method, constraints)
        if hasattr(result, "max_sharpe_portfolio"):
            return result.max_sharpe_portfolio
        return result
    except Exception as e:
        logger.warning(f"Optimization failed: {e}")
        return None


def run_backtest(
    prices: pd.DataFrame,
    config: Config,
    strategy: str,
) -> BacktestResult:
    """Run a single backtest for one rebalancing strategy.

    Walk-forward: at each rebalance date, only data up to that date is used.
    Between rebalances, weights drift with market prices.
    """
    asset_tickers = [t for t in config.portfolio.assets if t in prices.columns]
    asset_prices = prices[asset_tickers]
    trading_dates = asset_prices.index
    lookback_days = config.data.lookback_years * TRADING_DAYS_PER_YEAR
    backtest_days = config.backtest.backtest_years * TRADING_DAYS_PER_YEAR
    risk_free_rate = get_risk_free_rate(config.optimization.risk_free_rate)

    # Backtest starts backtest_days from the end (or after minimum lookback)
    target_start_idx = max(lookback_days, len(trading_dates) - backtest_days)
    start_idx = max(60, min(target_start_idx, len(trading_dates) - 1))

    backtest_dates = trading_dates[start_idx:]
    if len(backtest_dates) == 0:
        raise ValueError("Not enough data for backtesting")

    # Generate rebalance dates
    if strategy == "buy_and_hold":
        rebalance_dates_set = {backtest_dates[0]}
    elif strategy == "dynamic":
        rebalance_dates_set = set()  # decided day-by-day
    else:
        rebalance_dates_set = set(generate_rebalance_dates(
            backtest_dates[0], backtest_dates[-1], strategy, backtest_dates,
        ))

    portfolio_value = config.portfolio.initial_investment
    current_weights = None
    target_weights = None
    daily_values = []
    weight_rows = []
    rebalance_events = []
    total_turnover = 0.0
    total_costs = 0.0
    n_assets = len(asset_tickers)
    opt_method = config.optimization.method
    if opt_method == "efficient_frontier":
        opt_method = "max_sharpe"

    for i, date in enumerate(backtest_dates):
        date_ts = pd.Timestamp(date)
        do_rebalance = False
        dynamic_opt_result = None

        if current_weights is None:
            do_rebalance = True
        elif strategy == "dynamic":
            loc = trading_dates.get_loc(date_ts)
            window_start = max(0, loc - lookback_days)
            window_prices = asset_prices.iloc[window_start:loc + 1]
            triggered, dyn_result = _check_dynamic_rebalance(
                current_weights, window_prices, opt_method,
                config.optimization.expected_returns,
                config.optimization.covariance,
                risk_free_rate,
                config.optimization.constraints,
                config.backtest.dynamic_threshold,
            )
            if triggered:
                do_rebalance = True
                dynamic_opt_result = dyn_result
        elif strategy != "buy_and_hold":
            if date_ts in rebalance_dates_set:
                do_rebalance = True

        if do_rebalance:
            if dynamic_opt_result is not None:
                result = dynamic_opt_result
            else:
                loc = trading_dates.get_loc(date_ts)
                window_start = max(0, loc - lookback_days)
                window_prices = asset_prices.iloc[window_start:loc + 1]

                result = _run_optimization(
                    window_prices, opt_method,
                    config.optimization.expected_returns,
                    config.optimization.covariance,
                    risk_free_rate,
                    config.optimization.constraints,
                )

            if result is not None:
                new_weights = result.weights.reindex(asset_tickers, fill_value=0.0)
                new_weights = new_weights / new_weights.sum()  # ensure sum to 1

                if current_weights is not None:
                    turnover = float((new_weights - current_weights).abs().sum()) / 2.0
                    cost = turnover * portfolio_value * config.backtest.transaction_cost
                    portfolio_value -= cost
                    total_turnover += turnover
                    total_costs += cost
                else:
                    turnover = 0.0
                    cost = 0.0

                rebalance_events.append(RebalanceEvent(
                    date=date_ts,
                    old_weights=current_weights.copy() if current_weights is not None else None,
                    new_weights=new_weights.copy(),
                    turnover=turnover,
                    transaction_cost=cost,
                ))
                target_weights = new_weights.copy()
                current_weights = new_weights.copy()

        if current_weights is not None and i > 0:
            prev_date = backtest_dates[i - 1]
            today_prices = asset_prices.loc[date_ts]
            prev_prices = asset_prices.loc[prev_date]
            valid = prev_prices > 0
            asset_returns = pd.Series(1.0, index=asset_tickers)
            asset_returns[valid] = today_prices[valid] / prev_prices[valid]

            weighted_values = current_weights * asset_returns
            day_return = weighted_values.sum()
            portfolio_value *= day_return
            current_weights = weighted_values / weighted_values.sum()

        daily_values.append(portfolio_value)
        weight_rows.append(
            current_weights.copy() if current_weights is not None
            else pd.Series(0.0, index=asset_tickers)
        )

    portfolio_values = pd.Series(daily_values, index=backtest_dates)
    daily_returns = portfolio_values.pct_change().dropna()
    weights_df = pd.DataFrame(weight_rows, index=backtest_dates, columns=asset_tickers)
    metrics = compute_metrics(portfolio_values, risk_free_rate, total_turnover, total_costs)

    return BacktestResult(
        strategy_name=strategy,
        portfolio_values=portfolio_values,
        daily_returns=daily_returns,
        weights_over_time=weights_df,
        rebalance_events=rebalance_events,
        metrics=metrics,
        total_turnover=total_turnover,
        total_transaction_costs=total_costs,
    )


def run_benchmark_backtest(
    prices: pd.DataFrame,
    benchmark_ticker: str,
    start_date,
    risk_free_rate: float,
    initial_investment: float = 100_000,
) -> BacktestResult:
    """Simple buy-and-hold of the benchmark."""
    if benchmark_ticker not in prices.columns:
        raise ValueError(f"Benchmark '{benchmark_ticker}' not in price data")

    bm_prices = prices[benchmark_ticker].dropna()
    bm_prices = bm_prices[bm_prices.index >= start_date]

    if len(bm_prices) == 0:
        raise ValueError(f"No benchmark data from {start_date}")

    portfolio_values = bm_prices / bm_prices.iloc[0] * initial_investment
    daily_returns = portfolio_values.pct_change().dropna()
    metrics = compute_metrics(portfolio_values, risk_free_rate)

    weights_df = pd.DataFrame(
        {benchmark_ticker: 1.0}, index=portfolio_values.index,
    )

    return BacktestResult(
        strategy_name=f"Benchmark ({benchmark_ticker})",
        portfolio_values=portfolio_values,
        daily_returns=daily_returns,
        weights_over_time=weights_df,
        rebalance_events=[],
        metrics=metrics,
        total_turnover=0.0,
        total_transaction_costs=0.0,
    )


def run_all_backtests(
    prices: pd.DataFrame,
    config: Config,
) -> BacktestComparison:
    """Run all configured strategies + buy-and-hold + benchmark. Recommend best."""
    results: dict[str, BacktestResult] = {}

    for strategy in config.backtest.rebalancing_strategies:
        logger.info(f"Running backtest: {strategy}")
        results[strategy] = run_backtest(prices, config, strategy)

    if config.backtest.include_buy_and_hold:
        results["buy_and_hold"] = run_backtest(prices, config, "buy_and_hold")

    # Determine backtest start date for benchmark alignment
    first_result = next(iter(results.values()))
    start_date = first_result.portfolio_values.index[0]
    risk_free_rate = get_risk_free_rate(config.optimization.risk_free_rate)

    benchmark_result = run_benchmark_backtest(
        prices, config.portfolio.benchmark, start_date,
        risk_free_rate, config.portfolio.initial_investment,
    )

    # Recommend: highest Sharpe with max_drawdown < 2x benchmark max_drawdown
    bm_dd = benchmark_result.metrics.max_drawdown
    dd_threshold = max(bm_dd * 2, 0.15)

    candidates = {
        name: r for name, r in results.items()
        if r.metrics.max_drawdown <= dd_threshold
    }

    if candidates:
        best_name = max(candidates, key=lambda n: candidates[n].metrics.sharpe_ratio)
        best = candidates[best_name]
        reason = (
            f"Highest risk-adjusted return (Sharpe {best.metrics.sharpe_ratio:.3f}) "
            f"with acceptable drawdown ({best.metrics.max_drawdown:.2%} vs "
            f"benchmark {bm_dd:.2%})."
        )
    else:
        best_name = min(results, key=lambda n: results[n].metrics.max_drawdown)
        reason = (
            f"All strategies exceeded drawdown threshold. "
            f"Selected lowest drawdown ({results[best_name].metrics.max_drawdown:.2%})."
        )

    return BacktestComparison(
        results=results,
        benchmark_result=benchmark_result,
        recommended_strategy=best_name,
        recommendation_reason=reason,
    )
