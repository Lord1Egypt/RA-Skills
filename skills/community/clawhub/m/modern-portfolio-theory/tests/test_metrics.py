"""Tests for metrics.py — known-answer performance calculations."""

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.metrics import (
    compute_drawdown_series,
    compute_metrics,
    compute_rolling_sharpe,
    compare_metrics,
)


@pytest.fixture
def simple_portfolio():
    """Portfolio that goes 100 -> 120 linearly over 252 days."""
    dates = pd.bdate_range("2023-01-03", periods=252)
    values = np.linspace(100, 120, 252)
    return pd.Series(values, index=dates)


@pytest.fixture
def drawdown_portfolio():
    """Portfolio: 100 -> 150 -> 90 -> 130."""
    dates = pd.bdate_range("2023-01-03", periods=4)
    values = [100, 150, 90, 130]
    return pd.Series(values, index=dates)


class TestComputeMetrics:
    def test_total_return(self, simple_portfolio):
        m = compute_metrics(simple_portfolio, 0.04)
        assert abs(m.total_return - 0.20) < 0.01

    def test_positive_cagr(self, simple_portfolio):
        m = compute_metrics(simple_portfolio, 0.04)
        assert m.cagr > 0

    def test_positive_volatility(self, simple_portfolio):
        m = compute_metrics(simple_portfolio, 0.04)
        assert m.annualized_volatility > 0

    def test_win_rate_bounds(self, simple_portfolio):
        m = compute_metrics(simple_portfolio, 0.04)
        assert 0 <= m.win_rate <= 1

    def test_empty_series(self):
        s = pd.Series([100.0], index=pd.bdate_range("2023-01-03", periods=1))
        m = compute_metrics(s, 0.04)
        assert m.total_return == 0.0


class TestDrawdown:
    def test_max_drawdown(self, drawdown_portfolio):
        dd = compute_drawdown_series(drawdown_portfolio)
        expected_max = (150 - 90) / 150
        assert abs(dd.max() - expected_max) < 1e-10

    def test_zero_at_start(self, drawdown_portfolio):
        dd = compute_drawdown_series(drawdown_portfolio)
        assert dd.iloc[0] == 0.0

    def test_non_negative(self, simple_portfolio):
        dd = compute_drawdown_series(simple_portfolio)
        assert (dd >= -1e-10).all()


class TestRollingSharpe:
    def test_returns_series(self, simple_portfolio):
        daily_returns = simple_portfolio.pct_change().dropna()
        rs = compute_rolling_sharpe(daily_returns, 0.04, window=63)
        assert isinstance(rs, pd.Series)
        assert len(rs) > 0

    def test_window_effect(self, simple_portfolio):
        daily_returns = simple_portfolio.pct_change().dropna()
        rs_short = compute_rolling_sharpe(daily_returns, 0.04, window=21)
        rs_long = compute_rolling_sharpe(daily_returns, 0.04, window=63)
        assert len(rs_short) > len(rs_long)


class TestCompareMetrics:
    def test_dataframe_output(self, simple_portfolio):
        m1 = compute_metrics(simple_portfolio, 0.04)
        m2 = compute_metrics(simple_portfolio * 1.1, 0.04)
        df = compare_metrics({"A": m1, "B": m2})
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "Sharpe" in df.columns
