"""Expected return estimation — pure math, no I/O.

Formulas:
  - Log returns:          r_t = ln(P_t / P_{t-1})
  - Annualized mean:      mu = mean(r_daily) * 252
  - Exp-weighted mean:    mu = ewm(r_daily, span).mean()[-1] * 252
  - Black-Litterman:      mu_BL = [(tau*Sigma)^-1 + P^T Omega^-1 P]^-1
                                  * [(tau*Sigma)^-1 pi + P^T Omega^-1 Q]
      where pi = delta * Sigma * w_mkt  (equilibrium excess returns)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from mpt_portfolio.utils import TRADING_DAYS_PER_YEAR


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Daily log returns: ln(P_t / P_{t-1}). First row is dropped."""
    return np.log(prices / prices.shift(1)).dropna()


def annualize_returns(
    daily_returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """Annualized mean return per asset: mu_i = mean(r_i) * trading_days."""
    return daily_returns.mean() * trading_days


def exp_weighted_returns(
    daily_returns: pd.DataFrame,
    span: int = 60,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """Exponentially-weighted annualized mean return.

    Recent data gets higher weight, addressing the criticism that
    historical means are stale estimates of future returns.
    """
    ew = daily_returns.ewm(span=span).mean()
    return ew.iloc[-1] * trading_days


def equilibrium_returns(
    cov_matrix: pd.DataFrame,
    market_weights: pd.Series,
    risk_aversion: float = 2.5,
    risk_free_rate: float = 0.05,
) -> pd.Series:
    """Implied equilibrium excess returns (Black-Litterman prior).

    pi = delta * Sigma * w_mkt
    """
    pi = risk_aversion * cov_matrix.values @ market_weights.values
    return pd.Series(pi, index=cov_matrix.index) + risk_free_rate


def black_litterman_returns(
    cov_matrix: pd.DataFrame,
    market_weights: pd.Series,
    P: np.ndarray,
    Q: np.ndarray,
    omega: np.ndarray | None = None,
    tau: float = 0.05,
    risk_aversion: float = 2.5,
    risk_free_rate: float = 0.05,
) -> pd.Series:
    """Black-Litterman posterior expected returns.

    Args:
        cov_matrix: Annualized covariance matrix (n x n).
        market_weights: Market-cap weights for each asset.
        P: Pick matrix (k x n) where k = number of views.
        Q: View vector (k,) of expected excess returns for each view.
        omega: Uncertainty matrix (k x k). If None, uses tau * P @ Sigma @ P^T.
        tau: Scaling factor for covariance uncertainty (typically 0.025-0.05).
        risk_aversion: Market risk aversion coefficient.
        risk_free_rate: Annual risk-free rate.

    Returns:
        Posterior expected returns (annualized, n-vector).
    """
    sigma = cov_matrix.values
    n = sigma.shape[0]
    k = P.shape[0]
    Q = np.asarray(Q).flatten()

    pi = risk_aversion * sigma @ market_weights.values

    tau_sigma = tau * sigma
    tau_sigma_inv = np.linalg.inv(tau_sigma)

    if omega is None:
        omega = tau * P @ sigma @ P.T
    omega_inv = np.linalg.inv(omega)

    # Posterior precision and mean
    precision = tau_sigma_inv + P.T @ omega_inv @ P
    mean_part = tau_sigma_inv @ pi + P.T @ omega_inv @ Q
    mu_bl = np.linalg.solve(precision, mean_part)

    return pd.Series(mu_bl + risk_free_rate, index=cov_matrix.index)


def get_expected_returns(
    daily_returns: pd.DataFrame,
    method: str,
    cov_matrix: pd.DataFrame | None = None,
    **kwargs,
) -> pd.Series:
    """Dispatch to the configured expected returns method."""
    if method == "mean_historical":
        return annualize_returns(daily_returns, **{
            k: v for k, v in kwargs.items() if k == "trading_days"
        })
    elif method == "exp_weighted":
        return exp_weighted_returns(daily_returns, **{
            k: v for k, v in kwargs.items() if k in ("span", "trading_days")
        })
    elif method == "black_litterman":
        if cov_matrix is None:
            raise ValueError("black_litterman requires cov_matrix")
        required = {"market_weights", "P", "Q"}
        missing = required - set(kwargs.keys())
        if missing:
            raise ValueError(f"black_litterman requires kwargs: {missing}")
        return black_litterman_returns(
            cov_matrix=cov_matrix,
            market_weights=kwargs["market_weights"],
            P=kwargs["P"],
            Q=kwargs["Q"],
            omega=kwargs.get("omega"),
            tau=kwargs.get("tau", 0.05),
            risk_aversion=kwargs.get("risk_aversion", 2.5),
            risk_free_rate=kwargs.get("risk_free_rate", 0.05),
        )
    else:
        raise ValueError(f"Unknown expected returns method: {method}")
