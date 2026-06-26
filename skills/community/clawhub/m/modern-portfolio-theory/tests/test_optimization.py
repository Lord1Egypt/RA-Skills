"""Tests for optimization.py — weight constraints, math correctness."""

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.config import ConstraintsConfig
from mpt_portfolio.optimization import (
    EfficientFrontierResult,
    _clamp_weights,
    efficient_frontier,
    maximize_sharpe,
    minimize_variance,
    optimize,
    portfolio_return,
    portfolio_sharpe,
    portfolio_volatility,
    risk_parity,
)
from mpt_portfolio.returns import annualize_returns, compute_log_returns
from mpt_portfolio.risk import ledoit_wolf_covariance


@pytest.fixture
def opt_inputs(sample_returns):
    mu = annualize_returns(sample_returns)
    cov = ledoit_wolf_covariance(sample_returns)
    return mu, cov


class TestPortfolioFunctions:
    def test_portfolio_return(self):
        w = np.array([0.6, 0.4])
        mu = np.array([0.10, 0.20])
        assert abs(portfolio_return(w, mu) - 0.14) < 1e-10

    def test_portfolio_volatility(self):
        w = np.array([1.0, 0.0])
        cov = np.array([[0.04, 0.01], [0.01, 0.09]])
        assert abs(portfolio_volatility(w, cov) - 0.20) < 1e-10

    def test_portfolio_sharpe(self):
        w = np.array([0.5, 0.5])
        mu = np.array([0.10, 0.10])
        cov = np.array([[0.04, 0.0], [0.0, 0.04]])
        rf = 0.02
        vol = portfolio_volatility(w, cov)
        expected_sharpe = (0.10 - 0.02) / vol
        assert abs(portfolio_sharpe(w, mu, cov, rf) - expected_sharpe) < 1e-10


class TestMinimizeVariance:
    def test_weights_sum_to_one(self, opt_inputs):
        mu, cov = opt_inputs
        result = minimize_variance(mu, cov, 0.04, ConstraintsConfig())
        assert abs(result.weights.sum() - 1.0) < 1e-6

    def test_long_only(self, opt_inputs):
        mu, cov = opt_inputs
        result = minimize_variance(mu, cov, 0.04, ConstraintsConfig(long_only=True))
        assert (result.weights >= -1e-6).all()

    def test_max_weight_respected(self, opt_inputs):
        mu, cov = opt_inputs
        result = minimize_variance(mu, cov, 0.04, ConstraintsConfig(max_weight=0.30))
        assert (result.weights <= 0.30 + 1e-10).all()

    def test_returns_result(self, opt_inputs):
        mu, cov = opt_inputs
        result = minimize_variance(mu, cov, 0.04, ConstraintsConfig())
        assert result.method == "min_variance"
        assert result.volatility > 0
        assert isinstance(result.weights, pd.Series)


class TestMaximizeSharpe:
    def test_weights_sum_to_one(self, opt_inputs):
        mu, cov = opt_inputs
        result = maximize_sharpe(mu, cov, 0.04, ConstraintsConfig())
        assert abs(result.weights.sum() - 1.0) < 1e-6

    def test_higher_sharpe_than_min_var(self, opt_inputs):
        mu, cov = opt_inputs
        constraints = ConstraintsConfig()
        mv = minimize_variance(mu, cov, 0.04, constraints)
        ms = maximize_sharpe(mu, cov, 0.04, constraints)
        assert ms.sharpe_ratio >= mv.sharpe_ratio - 0.01

    def test_max_weight_respected(self, opt_inputs):
        mu, cov = opt_inputs
        result = maximize_sharpe(mu, cov, 0.04, ConstraintsConfig(max_weight=0.25))
        assert (result.weights <= 0.25 + 1e-10).all()


class TestEfficientFrontier:
    def test_returns_correct_type(self, opt_inputs):
        mu, cov = opt_inputs
        result = efficient_frontier(mu, cov, 0.04, ConstraintsConfig(), n_points=20)
        assert isinstance(result, EfficientFrontierResult)

    def test_multiple_points(self, opt_inputs):
        mu, cov = opt_inputs
        result = efficient_frontier(mu, cov, 0.04, ConstraintsConfig(), n_points=20)
        assert len(result.frontier_returns) >= 5

    def test_increasing_returns(self, opt_inputs):
        mu, cov = opt_inputs
        result = efficient_frontier(mu, cov, 0.04, ConstraintsConfig(), n_points=20)
        diffs = np.diff(result.frontier_returns)
        assert (diffs >= -1e-6).all()

    def test_contains_special_portfolios(self, opt_inputs):
        mu, cov = opt_inputs
        result = efficient_frontier(mu, cov, 0.04, ConstraintsConfig(), n_points=20)
        assert result.min_variance_portfolio is not None
        assert result.max_sharpe_portfolio is not None


class TestRiskParity:
    def test_weights_sum_to_one(self, opt_inputs):
        mu, cov = opt_inputs
        result = risk_parity(cov, 0.04, mu)
        assert abs(result.weights.sum() - 1.0) < 1e-6

    def test_positive_weights(self, opt_inputs):
        mu, cov = opt_inputs
        result = risk_parity(cov, 0.04, mu)
        assert (result.weights >= -1e-6).all()

    def test_roughly_equal_risk_contribution(self, opt_inputs):
        mu, cov = opt_inputs
        result = risk_parity(cov, 0.04, mu)
        w = result.weights.values
        sigma = cov.values
        vol = np.sqrt(w @ sigma @ w)
        marginal = sigma @ w
        rc = w * marginal / vol
        target = vol / len(w)
        assert np.allclose(rc, target, atol=0.005)


class TestOptimizeDispatcher:
    def test_max_sharpe(self, opt_inputs):
        mu, cov = opt_inputs
        result = optimize(mu, cov, 0.04, "max_sharpe")
        assert result.method == "max_sharpe"

    def test_efficient_frontier(self, opt_inputs):
        mu, cov = opt_inputs
        result = optimize(mu, cov, 0.04, "efficient_frontier")
        assert isinstance(result, EfficientFrontierResult)

    def test_unknown_method(self, opt_inputs):
        mu, cov = opt_inputs
        with pytest.raises(ValueError):
            optimize(mu, cov, 0.04, "unknown")


class TestClampWeights:
    def test_clips_above_max(self):
        w = np.array([0.5, 0.3, 0.2])
        c = ConstraintsConfig(max_weight=0.40, long_only=True)
        result = _clamp_weights(w, c)
        assert (result <= 0.40 + 1e-12).all()
        assert abs(result.sum() - 1.0) < 1e-10

    def test_clips_negative_when_long_only(self):
        w = np.array([-0.1, 0.6, 0.5])
        c = ConstraintsConfig(max_weight=1.0, long_only=True)
        result = _clamp_weights(w, c)
        assert (result >= -1e-12).all()
        assert abs(result.sum() - 1.0) < 1e-10

    def test_preserves_valid_weights(self):
        w = np.array([0.3, 0.3, 0.4])
        c = ConstraintsConfig(max_weight=0.40, long_only=True)
        result = _clamp_weights(w, c)
        assert abs(result.sum() - 1.0) < 1e-10
        assert np.allclose(result, w, atol=1e-10)

    def test_renormalizes_to_one(self):
        w = np.array([0.6, 0.6, 0.1])
        c = ConstraintsConfig(max_weight=0.50, long_only=True)
        result = _clamp_weights(w, c)
        assert abs(result.sum() - 1.0) < 1e-10
