"""Tests for data sufficiency check."""

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.data import check_data_sufficiency


class TestDataSufficiency:
    def _make_prices(self, n_days: int, tickers: list[str], gaps: dict | None = None) -> pd.DataFrame:
        """Create fake price data with optional per-ticker gaps at the start."""
        rng = np.random.default_rng(42)
        dates = pd.bdate_range("2015-01-05", periods=n_days)
        data = {}
        for t in tickers:
            prices = 100.0 * np.exp(np.cumsum(rng.standard_normal(n_days) * 0.01))
            if gaps and t in gaps:
                prices[:gaps[t]] = np.nan
            data[t] = prices
        return pd.DataFrame(data, index=dates)

    def test_all_sufficient(self):
        prices = self._make_prices(2520, ["A", "B", "C"])
        report = check_data_sufficiency(prices, lookback_years=5, backtest_years=5)
        assert report.all_sufficient
        assert len(report.insufficient_assets) == 0
        assert all(a.sufficient for a in report.assets)

    def test_one_asset_insufficient(self):
        prices = self._make_prices(2520, ["A", "B", "C"], gaps={"C": 2000})
        report = check_data_sufficiency(prices, lookback_years=5, backtest_years=5)
        assert not report.all_sufficient
        assert "C" in report.insufficient_assets
        assert report.assets[2].ticker == "C"
        assert not report.assets[2].sufficient
        assert report.assets[0].sufficient
        assert report.assets[1].sufficient

    def test_suggested_max_years(self):
        prices = self._make_prices(756, ["A", "B"])
        report = check_data_sufficiency(prices, lookback_years=5, backtest_years=5)
        assert report.suggested_max_years == pytest.approx(756 / 252, abs=0.1)

    def test_effective_common_days_with_gaps(self):
        prices = self._make_prices(1000, ["A", "B"], gaps={"B": 200})
        report = check_data_sufficiency(prices, lookback_years=2, backtest_years=1)
        assert report.effective_common_days == 800
        assert report.assets[0].available_days == 1000
        assert report.assets[1].available_days == 800

    def test_all_sufficient_small_requirement(self):
        prices = self._make_prices(756, ["A", "B"])
        report = check_data_sufficiency(prices, lookback_years=2, backtest_years=1)
        assert report.all_sufficient
