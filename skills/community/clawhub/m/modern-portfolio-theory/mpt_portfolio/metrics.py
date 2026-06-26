"""Performance metrics — pure math, no I/O.

Metrics:
  - Total return:       (V_final / V_initial) - 1
  - CAGR:               (V_final / V_initial)^(252/n_days) - 1
  - Annualized vol:     std(r_daily) * sqrt(252)
  - Sharpe:             (CAGR - Rf) / vol
  - Sortino:            (CAGR - Rf) / downside_deviation
  - Max drawdown:       max((peak - trough) / peak)
  - Calmar:             CAGR / |max_drawdown|
  - Win rate:           fraction of positive-return days
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

from mpt_portfolio.utils import TRADING_DAYS_PER_YEAR


@dataclass
class PerformanceMetrics:
    total_return: float
    cagr: float
    annualized_volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    max_drawdown_start: datetime | None
    max_drawdown_end: datetime | None
    calmar_ratio: float
    win_rate: float
    total_turnover: float
    total_transaction_costs: float
    best_day: float
    worst_day: float
    avg_daily_return: float


def compute_drawdown_series(portfolio_values: pd.Series) -> pd.Series:
    """Running drawdown: (cummax - value) / cummax."""
    cummax = portfolio_values.cummax()
    drawdown = (cummax - portfolio_values) / cummax
    return drawdown


def compute_metrics(
    portfolio_values: pd.Series,
    risk_free_rate: float,
    total_turnover: float = 0.0,
    total_transaction_costs: float = 0.0,
) -> PerformanceMetrics:
    """Compute all performance metrics from a portfolio value time series."""
    daily_returns = portfolio_values.pct_change().dropna()
    n_days = len(daily_returns)

    if n_days == 0:
        return PerformanceMetrics(
            total_return=0.0, cagr=0.0, annualized_volatility=0.0,
            sharpe_ratio=0.0, sortino_ratio=0.0, max_drawdown=0.0,
            max_drawdown_start=None, max_drawdown_end=None, calmar_ratio=0.0,
            win_rate=0.0, total_turnover=total_turnover,
            total_transaction_costs=total_transaction_costs,
            best_day=0.0, worst_day=0.0, avg_daily_return=0.0,
        )

    v_initial = portfolio_values.iloc[0]
    v_final = portfolio_values.iloc[-1]
    total_return = (v_final / v_initial) - 1.0

    years = n_days / TRADING_DAYS_PER_YEAR
    if years > 0 and v_final > 0 and v_initial > 0:
        cagr = (v_final / v_initial) ** (1.0 / years) - 1.0
    else:
        cagr = 0.0

    ann_vol = float(daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))
    sharpe = (cagr - risk_free_rate) / ann_vol if ann_vol > 0 else 0.0

    # Sortino: only downside deviation
    daily_rf = risk_free_rate / TRADING_DAYS_PER_YEAR
    downside = daily_returns[daily_returns < daily_rf] - daily_rf
    downside_dev = float(np.sqrt((downside ** 2).mean()) * np.sqrt(TRADING_DAYS_PER_YEAR)) if len(downside) > 0 else 0.0
    sortino = (cagr - risk_free_rate) / downside_dev if downside_dev > 0 else 0.0

    # Max drawdown
    dd = compute_drawdown_series(portfolio_values)
    max_dd = float(dd.max())
    if max_dd > 0:
        dd_end_idx = dd.idxmax()
        dd_start_idx = portfolio_values.loc[:dd_end_idx].idxmax()
        dd_start = dd_start_idx if hasattr(dd_start_idx, "to_pydatetime") else None
        dd_end = dd_end_idx if hasattr(dd_end_idx, "to_pydatetime") else None
    else:
        dd_start = None
        dd_end = None

    calmar = cagr / abs(max_dd) if max_dd > 0 else 0.0
    win_rate = float((daily_returns > 0).sum() / n_days)

    return PerformanceMetrics(
        total_return=total_return,
        cagr=cagr,
        annualized_volatility=ann_vol,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        max_drawdown=max_dd,
        max_drawdown_start=dd_start,
        max_drawdown_end=dd_end,
        calmar_ratio=calmar,
        win_rate=win_rate,
        total_turnover=total_turnover,
        total_transaction_costs=total_transaction_costs,
        best_day=float(daily_returns.max()),
        worst_day=float(daily_returns.min()),
        avg_daily_return=float(daily_returns.mean()),
    )


def compute_rolling_sharpe(
    daily_returns: pd.Series,
    risk_free_rate: float,
    window: int = 63,
) -> pd.Series:
    """Rolling annualized Sharpe ratio."""
    daily_rf = risk_free_rate / TRADING_DAYS_PER_YEAR
    excess = daily_returns - daily_rf
    rolling_mean = excess.rolling(window).mean() * TRADING_DAYS_PER_YEAR
    rolling_std = daily_returns.rolling(window).std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    rolling_std = rolling_std.replace(0, np.nan)
    return (rolling_mean / rolling_std).dropna()


def compute_rolling_returns(
    portfolio_values: pd.Series,
    window: int = 252,
) -> pd.Series:
    """Rolling annualized return over trailing window."""
    return (portfolio_values / portfolio_values.shift(window)) ** (TRADING_DAYS_PER_YEAR / window) - 1


def compare_metrics(
    metrics_dict: dict[str, PerformanceMetrics],
) -> pd.DataFrame:
    """Create a comparison table: strategies as rows, metrics as columns."""
    rows = {}
    for name, m in metrics_dict.items():
        rows[name] = {
            "Total Return": f"{m.total_return:.2%}",
            "CAGR": f"{m.cagr:.2%}",
            "Volatility": f"{m.annualized_volatility:.2%}",
            "Sharpe": f"{m.sharpe_ratio:.3f}",
            "Sortino": f"{m.sortino_ratio:.3f}",
            "Max Drawdown": f"{m.max_drawdown:.2%}",
            "Calmar": f"{m.calmar_ratio:.3f}",
            "Win Rate": f"{m.win_rate:.2%}",
            "Turnover": f"{m.total_turnover:.2f}",
            "Costs": f"${m.total_transaction_costs:.2f}",
        }
    return pd.DataFrame(rows).T
