"""Covariance estimation — pure math, no I/O.

Formulas:
  - Sample covariance (annualized): Sigma = cov(r_daily) * 252
  - Ledoit-Wolf shrinkage:          Sigma_LW = alpha*F + (1-alpha)*S
      where F = shrinkage target, S = sample cov, alpha = optimal intensity
  - Correlation matrix:             Corr_ij = Sigma_ij / sqrt(Sigma_ii * Sigma_jj)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from mpt_portfolio.utils import TRADING_DAYS_PER_YEAR


def sample_covariance(
    daily_returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.DataFrame:
    """Annualized sample covariance matrix."""
    return daily_returns.cov() * trading_days


def _ledoit_wolf_shrinkage(X: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit-Wolf (2004) shrinkage toward scaled identity.

    Parameters: X — (n_samples, n_features) centered data matrix.
    Returns: (shrunk_covariance, shrinkage_intensity).
    """
    n, p = X.shape
    S = X.T @ X / n
    mu = np.trace(S) / p

    delta = np.sum((S - mu * np.eye(p)) ** 2) / p
    if delta == 0:
        return S, 0.0

    X2 = X ** 2
    phi = np.sum(X2.T @ X2 / n - S ** 2) / (n * p)

    shrinkage = max(0.0, min(1.0, phi / delta))
    shrunk = (1.0 - shrinkage) * S + shrinkage * mu * np.eye(p)
    return shrunk, shrinkage


def ledoit_wolf_covariance(
    daily_returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.DataFrame:
    """Ledoit-Wolf shrinkage covariance estimator (annualized)."""
    X = daily_returns.values
    X_centered = X - X.mean(axis=0)
    shrunk_cov, _ = _ledoit_wolf_shrinkage(X_centered)
    cov = shrunk_cov * trading_days
    return pd.DataFrame(cov, index=daily_returns.columns, columns=daily_returns.columns)


def correlation_matrix(cov_matrix: pd.DataFrame) -> pd.DataFrame:
    """Convert covariance matrix to correlation matrix."""
    std = np.sqrt(np.diag(cov_matrix.values))
    outer = np.outer(std, std)
    outer[outer == 0] = 1.0
    corr = cov_matrix.values / outer
    np.fill_diagonal(corr, 1.0)
    return pd.DataFrame(corr, index=cov_matrix.index, columns=cov_matrix.columns)


def get_covariance(
    daily_returns: pd.DataFrame,
    method: str,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.DataFrame:
    """Dispatch to the configured covariance method."""
    if method == "sample":
        return sample_covariance(daily_returns, trading_days)
    elif method == "ledoit_wolf":
        return ledoit_wolf_covariance(daily_returns, trading_days)
    else:
        raise ValueError(f"Unknown covariance method: {method}")
