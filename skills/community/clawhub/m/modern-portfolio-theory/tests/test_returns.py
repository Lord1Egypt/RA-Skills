"""Tests for returns.py — return calculation correctness."""

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.returns import (
    annualize_returns,
    compute_log_returns,
    exp_weighted_returns,
    get_expected_returns,
)


class TestComputeLogReturns:
    def test_basic(self, sample_prices):
        returns = compute_log_returns(sample_prices)
        assert len(returns) == len(sample_prices) - 1
        assert list(returns.columns) == list(sample_prices.columns)

    def test_no_nans(self, sample_prices):
        returns = compute_log_returns(sample_prices)
        assert not returns.isna().any().any()

    def test_log_return_formula(self):
        prices = pd.DataFrame({"A": [100.0, 110.0, 105.0]})
        returns = compute_log_returns(prices)
        expected = [np.log(110.0 / 100.0), np.log(105.0 / 110.0)]
        np.testing.assert_allclose(returns["A"].values, expected, rtol=1e-10)


class TestAnnualizeReturns:
    def test_shape(self, sample_returns):
        ann = annualize_returns(sample_returns)
        assert len(ann) == sample_returns.shape[1]

    def test_formula(self, sample_returns):
        ann = annualize_returns(sample_returns)
        manual = sample_returns.mean() * 252
        pd.testing.assert_series_equal(ann, manual)


class TestExpWeightedReturns:
    def test_shape(self, sample_returns):
        ew = exp_weighted_returns(sample_returns)
        assert len(ew) == sample_returns.shape[1]

    def test_different_from_mean(self, sample_returns):
        ew = exp_weighted_returns(sample_returns)
        mean = annualize_returns(sample_returns)
        assert not np.allclose(ew.values, mean.values)


class TestGetExpectedReturns:
    def test_mean_historical(self, sample_returns):
        result = get_expected_returns(sample_returns, "mean_historical")
        expected = annualize_returns(sample_returns)
        pd.testing.assert_series_equal(result, expected)

    def test_exp_weighted(self, sample_returns):
        result = get_expected_returns(sample_returns, "exp_weighted")
        assert len(result) == sample_returns.shape[1]

    def test_unknown_method(self, sample_returns):
        with pytest.raises(ValueError, match="Unknown"):
            get_expected_returns(sample_returns, "invalid_method")
