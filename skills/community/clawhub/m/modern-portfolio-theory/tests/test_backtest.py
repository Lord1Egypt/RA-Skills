"""Tests for backtest.py — walk-forward correctness."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from mpt_portfolio.backtest import (
    generate_rebalance_dates,
    _check_dynamic_rebalance,
)
from mpt_portfolio.config import ConstraintsConfig


class TestGenerateRebalanceDates:
    @pytest.fixture
    def trading_dates(self):
        return pd.bdate_range("2022-01-03", "2023-12-29")

    def test_monthly_count(self, trading_dates):
        dates = generate_rebalance_dates(
            trading_dates[0], trading_dates[-1], "monthly", trading_dates,
        )
        assert 23 <= len(dates) <= 25  # ~24 months

    def test_quarterly_count(self, trading_dates):
        dates = generate_rebalance_dates(
            trading_dates[0], trading_dates[-1], "quarterly", trading_dates,
        )
        assert 7 <= len(dates) <= 9  # ~8 quarters

    def test_yearly_count(self, trading_dates):
        dates = generate_rebalance_dates(
            trading_dates[0], trading_dates[-1], "yearly", trading_dates,
        )
        assert len(dates) == 2

    def test_dates_are_trading_days(self, trading_dates):
        dates = generate_rebalance_dates(
            trading_dates[0], trading_dates[-1], "monthly", trading_dates,
        )
        for d in dates:
            assert d in trading_dates

    def test_invalid_frequency(self, trading_dates):
        with pytest.raises(ValueError):
            generate_rebalance_dates(
                trading_dates[0], trading_dates[-1], "biweekly", trading_dates,
            )


class TestCheckDynamicRebalance:
    """Tests for _check_dynamic_rebalance — compares current weights to fresh optimal."""

    def _mock_opt_result(self, weights_dict):
        result = MagicMock()
        result.weights = pd.Series(weights_dict)
        return result

    def test_no_rebalance_when_close_to_optimal(self):
        current = pd.Series({"A": 0.50, "B": 0.50})
        mock_result = self._mock_opt_result({"A": 0.52, "B": 0.48})
        dummy_prices = pd.DataFrame({"A": [1.0], "B": [1.0]})
        with patch("mpt_portfolio.backtest._run_optimization", return_value=mock_result):
            triggered, result = _check_dynamic_rebalance(
                current, dummy_prices, "max_sharpe", "mean_historical",
                "ledoit_wolf", 0.05, ConstraintsConfig(), 0.05,
            )
        assert not triggered

    def test_rebalance_when_far_from_optimal(self):
        current = pd.Series({"A": 0.30, "B": 0.70})
        mock_result = self._mock_opt_result({"A": 0.60, "B": 0.40})
        dummy_prices = pd.DataFrame({"A": [1.0], "B": [1.0]})
        with patch("mpt_portfolio.backtest._run_optimization", return_value=mock_result):
            triggered, result = _check_dynamic_rebalance(
                current, dummy_prices, "max_sharpe", "mean_historical",
                "ledoit_wolf", 0.05, ConstraintsConfig(), 0.05,
            )
        assert triggered
        assert result is mock_result

    def test_no_rebalance_on_optimization_failure(self):
        current = pd.Series({"A": 0.50, "B": 0.50})
        dummy_prices = pd.DataFrame({"A": [1.0], "B": [1.0]})
        with patch("mpt_portfolio.backtest._run_optimization", return_value=None):
            triggered, result = _check_dynamic_rebalance(
                current, dummy_prices, "max_sharpe", "mean_historical",
                "ledoit_wolf", 0.05, ConstraintsConfig(), 0.05,
            )
        assert not triggered
        assert result is None

    def test_distance_calculation(self):
        """Distance = sum(|current - optimal|) / 2. Here: (|0.4-0.5| + |0.6-0.5|) / 2 = 0.1"""
        current = pd.Series({"A": 0.40, "B": 0.60})
        mock_result = self._mock_opt_result({"A": 0.50, "B": 0.50})
        dummy_prices = pd.DataFrame({"A": [1.0], "B": [1.0]})
        with patch("mpt_portfolio.backtest._run_optimization", return_value=mock_result):
            triggered_low, _ = _check_dynamic_rebalance(
                current, dummy_prices, "max_sharpe", "mean_historical",
                "ledoit_wolf", 0.05, ConstraintsConfig(), 0.09,
            )
            triggered_high, _ = _check_dynamic_rebalance(
                current, dummy_prices, "max_sharpe", "mean_historical",
                "ledoit_wolf", 0.05, ConstraintsConfig(), 0.11,
            )
        assert triggered_low  # distance 0.1 > threshold 0.09
        assert not triggered_high  # distance 0.1 < threshold 0.11
