"""Tests for risk.py — covariance estimation."""

import numpy as np
import pandas as pd
import pytest

from mpt_portfolio.risk import (
    correlation_matrix,
    get_covariance,
    ledoit_wolf_covariance,
    sample_covariance,
)


class TestSampleCovariance:
    def test_shape(self, sample_returns):
        cov = sample_covariance(sample_returns)
        n = sample_returns.shape[1]
        assert cov.shape == (n, n)

    def test_symmetric(self, sample_returns):
        cov = sample_covariance(sample_returns)
        np.testing.assert_allclose(cov.values, cov.values.T, atol=1e-12)

    def test_positive_semidefinite(self, sample_returns):
        cov = sample_covariance(sample_returns)
        eigenvalues = np.linalg.eigvalsh(cov.values)
        assert (eigenvalues >= -1e-10).all()

    def test_annualized(self, sample_returns):
        cov = sample_covariance(sample_returns, trading_days=252)
        daily_cov = sample_returns.cov()
        np.testing.assert_allclose(cov.values, daily_cov.values * 252, rtol=1e-10)


class TestLedoitWolfCovariance:
    def test_shape(self, sample_returns):
        cov = ledoit_wolf_covariance(sample_returns)
        n = sample_returns.shape[1]
        assert cov.shape == (n, n)

    def test_symmetric(self, sample_returns):
        cov = ledoit_wolf_covariance(sample_returns)
        np.testing.assert_allclose(cov.values, cov.values.T, atol=1e-12)

    def test_positive_definite(self, sample_returns):
        cov = ledoit_wolf_covariance(sample_returns)
        eigenvalues = np.linalg.eigvalsh(cov.values)
        assert (eigenvalues > 0).all()

    def test_different_from_sample(self, sample_returns):
        sample = sample_covariance(sample_returns)
        lw = ledoit_wolf_covariance(sample_returns)
        assert not np.allclose(sample.values, lw.values)


class TestCorrelationMatrix:
    def test_diagonal_ones(self, sample_returns):
        cov = sample_covariance(sample_returns)
        corr = correlation_matrix(cov)
        np.testing.assert_allclose(np.diag(corr.values), 1.0, atol=1e-10)

    def test_range(self, sample_returns):
        cov = sample_covariance(sample_returns)
        corr = correlation_matrix(cov)
        assert (corr.values >= -1.0 - 1e-10).all()
        assert (corr.values <= 1.0 + 1e-10).all()


class TestGetCovariance:
    def test_sample(self, sample_returns):
        cov = get_covariance(sample_returns, "sample")
        expected = sample_covariance(sample_returns)
        pd.testing.assert_frame_equal(cov, expected)

    def test_ledoit_wolf(self, sample_returns):
        cov = get_covariance(sample_returns, "ledoit_wolf")
        assert cov.shape == (sample_returns.shape[1], sample_returns.shape[1])

    def test_unknown(self, sample_returns):
        with pytest.raises(ValueError, match="Unknown"):
            get_covariance(sample_returns, "invalid")
