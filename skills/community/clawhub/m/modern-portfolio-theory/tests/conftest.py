"""Shared test fixtures with deterministic fake data."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.config import (
    BacktestConfig,
    Config,
    ConstraintsConfig,
    DataConfig,
    EmailConfig,
    NotificationEventsConfig,
    OptimizationConfig,
    PortfolioConfig,
    RebalancingConfig,
    ReportsConfig,
)


@pytest.fixture
def sample_prices() -> pd.DataFrame:
    """Deterministic fake price data: 5 assets, ~3 years (756 trading days).

    Uses geometric Brownian motion with fixed seed.
    """
    rng = np.random.default_rng(42)
    n_days = 756
    tickers = ["A", "B", "C", "D", "E"]
    drifts = np.array([0.0003, 0.0005, 0.0001, 0.0004, 0.0002])
    vols = np.array([0.01, 0.02, 0.008, 0.015, 0.012])
    start_prices = np.array([100.0, 50.0, 200.0, 75.0, 150.0])

    dates = pd.bdate_range("2021-01-04", periods=n_days)
    prices = np.zeros((n_days, len(tickers)))
    prices[0] = start_prices

    for t in range(1, n_days):
        shocks = rng.standard_normal(len(tickers))
        prices[t] = prices[t - 1] * np.exp(drifts - 0.5 * vols**2 + vols * shocks)

    return pd.DataFrame(prices, index=dates, columns=tickers)


@pytest.fixture
def sample_returns(sample_prices: pd.DataFrame) -> pd.DataFrame:
    """Log returns from sample prices."""
    return np.log(sample_prices / sample_prices.shift(1)).dropna()


@pytest.fixture
def sample_config() -> Config:
    """Minimal valid Config for testing."""
    return Config(
        portfolio=PortfolioConfig(
            name="test_portfolio",
            initial_investment=100_000,
            assets=["A", "B", "C", "D", "E"],
            benchmark="SPY",
        ),
        data=DataConfig(lookback_years=3, frequency="daily", price_type="adjusted"),
        optimization=OptimizationConfig(
            method="max_sharpe",
            risk_free_rate=0.04,
            expected_returns="mean_historical",
            covariance="ledoit_wolf",
            constraints=ConstraintsConfig(long_only=True, max_weight=0.40, min_weight=0.0),
        ),
        backtest=BacktestConfig(
            rebalancing_strategies=["monthly", "quarterly"],
            dynamic_threshold=0.05,
            transaction_cost=0.001,
            include_buy_and_hold=True,
        ),
        rebalancing=RebalancingConfig(strategy="quarterly"),
        reports=ReportsConfig(formats=["terminal"], charts=[]),
    )


@pytest.fixture
def two_asset_prices() -> pd.DataFrame:
    """Simple 2-asset price data for analytical solution testing."""
    rng = np.random.default_rng(123)
    n_days = 504
    dates = pd.bdate_range("2022-01-03", periods=n_days)

    prices = np.zeros((n_days, 2))
    prices[0] = [100.0, 100.0]
    for t in range(1, n_days):
        prices[t, 0] = prices[t - 1, 0] * np.exp(0.0003 + 0.01 * rng.standard_normal())
        prices[t, 1] = prices[t - 1, 1] * np.exp(0.0002 + 0.015 * rng.standard_normal())

    return pd.DataFrame(prices, index=dates, columns=["X", "Y"])
