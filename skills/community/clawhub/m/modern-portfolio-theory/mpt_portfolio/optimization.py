"""Portfolio optimization — pure math, no I/O.

Optimization problems:
  1. Global Minimum Variance: min w^T Sigma w, s.t. sum(w)=1, bounds
  2. Max Sharpe Ratio:        max (w^T mu - Rf) / sqrt(w^T Sigma w)
  3. Efficient Frontier:      for range of target returns, solve min variance
  4. Risk Parity:             equalize RC_i = w_i * (Sigma w)_i / sigma_p
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from mpt_portfolio.config import ConstraintsConfig


@dataclass
class OptimizationResult:
    weights: pd.Series
    expected_return: float
    volatility: float
    sharpe_ratio: float
    method: str


@dataclass
class EfficientFrontierResult:
    frontier_returns: np.ndarray
    frontier_volatilities: np.ndarray
    frontier_weights: list[pd.Series]
    min_variance_portfolio: OptimizationResult
    max_sharpe_portfolio: OptimizationResult


class OptimizationError(Exception):
    pass


def portfolio_return(weights: np.ndarray, expected_returns: np.ndarray) -> float:
    return float(weights @ expected_returns)


def portfolio_volatility(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    return float(np.sqrt(weights @ cov_matrix @ weights))


def portfolio_sharpe(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float,
) -> float:
    ret = portfolio_return(weights, expected_returns)
    vol = portfolio_volatility(weights, cov_matrix)
    if vol == 0:
        return 0.0
    return (ret - risk_free_rate) / vol


def _build_bounds(n: int, constraints: ConstraintsConfig) -> list[tuple[float, float]]:
    if constraints.long_only:
        lo = max(constraints.min_weight, 0.0)
    else:
        lo = constraints.min_weight
    return [(lo, constraints.max_weight) for _ in range(n)]


def _sum_to_one_constraint():
    return {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}


def _clamp_weights(raw_weights: np.ndarray, constraints: ConstraintsConfig) -> np.ndarray:
    if constraints.long_only:
        lo = max(constraints.min_weight, 0.0)
    else:
        lo = constraints.min_weight
    hi = constraints.max_weight
    w = np.clip(raw_weights, lo, hi)
    total = w.sum()
    if total <= 0:
        return w
    w = w / total
    # Redistribute excess from capped assets to uncapped ones
    for _ in range(50):
        capped = w > hi
        if not capped.any():
            break
        excess = (w[capped] - hi).sum()
        w[capped] = hi
        free = ~capped
        if not free.any() or w[free].sum() == 0:
            break
        w[free] += excess * (w[free] / w[free].sum())
    return w


def minimize_variance(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
    constraints: ConstraintsConfig,
) -> OptimizationResult:
    """Find the Global Minimum Variance Portfolio."""
    n = len(expected_returns)
    mu = expected_returns.values
    sigma = cov_matrix.values
    x0 = np.ones(n) / n
    bounds = _build_bounds(n, constraints)

    result = minimize(
        fun=lambda w: w @ sigma @ w,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[_sum_to_one_constraint()],
        options={"ftol": 1e-12, "maxiter": 1000},
    )

    if not result.success:
        result = minimize(
            fun=lambda w: w @ sigma @ w,
            x0=x0,
            method="trust-constr",
            bounds=bounds,
            constraints=[_sum_to_one_constraint()],
        )
        if not result.success:
            raise OptimizationError(f"Minimum variance optimization failed: {result.message}")

    w = _clamp_weights(result.x, constraints)
    ret = portfolio_return(w, mu)
    vol = portfolio_volatility(w, sigma)
    sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0.0
    weights = pd.Series(w, index=expected_returns.index)

    return OptimizationResult(
        weights=weights,
        expected_return=ret,
        volatility=vol,
        sharpe_ratio=sharpe,
        method="min_variance",
    )


def maximize_sharpe(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
    constraints: ConstraintsConfig,
) -> OptimizationResult:
    """Find the Maximum Sharpe Ratio (Tangency) Portfolio."""
    n = len(expected_returns)
    mu = expected_returns.values
    sigma = cov_matrix.values
    x0 = np.ones(n) / n
    bounds = _build_bounds(n, constraints)

    def neg_sharpe(w):
        ret = w @ mu
        vol = np.sqrt(w @ sigma @ w)
        if vol < 1e-12:
            return 1e10
        return -(ret - risk_free_rate) / vol

    result = minimize(
        fun=neg_sharpe,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[_sum_to_one_constraint()],
        options={"ftol": 1e-12, "maxiter": 1000},
    )

    if not result.success:
        result = minimize(
            fun=neg_sharpe,
            x0=x0,
            method="trust-constr",
            bounds=bounds,
            constraints=[_sum_to_one_constraint()],
        )
        if not result.success:
            raise OptimizationError(f"Max Sharpe optimization failed: {result.message}")

    w = _clamp_weights(result.x, constraints)
    ret = portfolio_return(w, mu)
    vol = portfolio_volatility(w, sigma)
    sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0.0
    weights = pd.Series(w, index=expected_returns.index)

    return OptimizationResult(
        weights=weights,
        expected_return=ret,
        volatility=vol,
        sharpe_ratio=sharpe,
        method="max_sharpe",
    )


def _minimize_for_target_return(
    target_return: float,
    mu: np.ndarray,
    sigma: np.ndarray,
    bounds: list[tuple[float, float]],
    n: int,
    constraints: ConstraintsConfig | None = None,
) -> np.ndarray | None:
    """Solve: min w^T Sigma w, s.t. w^T mu = target, sum(w) = 1, bounds."""
    x0 = np.ones(n) / n
    cons = [
        _sum_to_one_constraint(),
        {"type": "eq", "fun": lambda w: w @ mu - target_return},
    ]
    result = minimize(
        fun=lambda w: w @ sigma @ w,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if result.success:
        if constraints is not None:
            return _clamp_weights(result.x, constraints)
        return result.x
    return None


def efficient_frontier(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
    constraints: ConstraintsConfig,
    n_points: int = 100,
) -> EfficientFrontierResult:
    """Compute the efficient frontier with min-variance and max-Sharpe portfolios."""
    min_var = minimize_variance(expected_returns, cov_matrix, risk_free_rate, constraints)
    max_sharpe = maximize_sharpe(expected_returns, cov_matrix, risk_free_rate, constraints)

    n = len(expected_returns)
    mu = expected_returns.values
    sigma = cov_matrix.values
    bounds = _build_bounds(n, constraints)

    # Max feasible return: put max_weight in highest-return assets
    sorted_idx = np.argsort(mu)[::-1]
    max_weights = np.zeros(n)
    remaining = 1.0
    for i in sorted_idx:
        alloc = min(constraints.max_weight, remaining)
        max_weights[i] = alloc
        remaining -= alloc
        if remaining <= 1e-10:
            break
    max_return = portfolio_return(max_weights, mu)
    min_return = min_var.expected_return

    target_returns = np.linspace(min_return, max_return, n_points)
    frontier_ret = []
    frontier_vol = []
    frontier_w = []

    for target in target_returns:
        w = _minimize_for_target_return(target, mu, sigma, bounds, n, constraints)
        if w is not None:
            frontier_ret.append(portfolio_return(w, mu))
            frontier_vol.append(portfolio_volatility(w, sigma))
            frontier_w.append(pd.Series(w, index=expected_returns.index))

    return EfficientFrontierResult(
        frontier_returns=np.array(frontier_ret),
        frontier_volatilities=np.array(frontier_vol),
        frontier_weights=frontier_w,
        min_variance_portfolio=min_var,
        max_sharpe_portfolio=max_sharpe,
    )


def risk_parity(
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
    expected_returns: pd.Series | None = None,
    constraints: ConstraintsConfig | None = None,
) -> OptimizationResult:
    """Equal Risk Contribution portfolio.

    Each asset contributes equally to total portfolio risk:
    RC_i = w_i * (Sigma w)_i / sigma_p = sigma_p / n
    """
    sigma = cov_matrix.values
    n = sigma.shape[0]
    x0 = np.ones(n) / n

    def risk_contribution_objective(w):
        port_vol = np.sqrt(w @ sigma @ w)
        if port_vol < 1e-12:
            return 1e10
        marginal = sigma @ w
        rc = w * marginal / port_vol
        target_rc = port_vol / n
        return float(np.sum((rc - target_rc) ** 2))

    if constraints is not None:
        bounds = _build_bounds(n, constraints)
    else:
        bounds = [(0.0, 1.0) for _ in range(n)]
    result = minimize(
        fun=risk_contribution_objective,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[_sum_to_one_constraint()],
        options={"ftol": 1e-15, "maxiter": 2000},
    )

    if not result.success:
        raise OptimizationError(f"Risk parity optimization failed: {result.message}")

    if constraints is not None:
        w = _clamp_weights(result.x, constraints)
    else:
        w = result.x
    weights = pd.Series(w, index=cov_matrix.index)

    if expected_returns is not None:
        mu = expected_returns.values
        ret = portfolio_return(w, mu)
    else:
        ret = 0.0

    vol = portfolio_volatility(w, sigma)
    sharpe = (ret - risk_free_rate) / vol if vol > 0 and expected_returns is not None else 0.0

    return OptimizationResult(
        weights=weights,
        expected_return=ret,
        volatility=vol,
        sharpe_ratio=sharpe,
        method="risk_parity",
    )


def optimize(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
    method: str,
    constraints: ConstraintsConfig | None = None,
    n_points: int = 100,
) -> OptimizationResult | EfficientFrontierResult:
    """Top-level dispatcher."""
    if constraints is None:
        constraints = ConstraintsConfig()

    if method == "min_variance":
        return minimize_variance(expected_returns, cov_matrix, risk_free_rate, constraints)
    elif method == "max_sharpe":
        return maximize_sharpe(expected_returns, cov_matrix, risk_free_rate, constraints)
    elif method == "efficient_frontier":
        return efficient_frontier(
            expected_returns, cov_matrix, risk_free_rate, constraints, n_points
        )
    elif method == "risk_parity":
        return risk_parity(cov_matrix, risk_free_rate, expected_returns, constraints)
    else:
        raise ValueError(f"Unknown optimization method: {method}")
