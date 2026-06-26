"""Chart generation — matplotlib only."""

from __future__ import annotations

import base64
import io
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter


def chart_efficient_frontier(
    frontier_returns: np.ndarray,
    frontier_volatilities: np.ndarray,
    min_var: dict | None = None,
    max_sharpe: dict | None = None,
    individual_assets: dict[str, tuple[float, float]] | None = None,
    risk_free_rate: float = 0.0,
) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(frontier_volatilities, frontier_returns, color="royalblue", linewidth=2,
            label="Efficient Frontier")

    if min_var:
        ax.scatter(min_var["volatility"], min_var["return"], marker="*", s=300,
                   color="green", zorder=5, label="Min Variance")
        ax.annotate("Min Var", (min_var["volatility"], min_var["return"]),
                    textcoords="offset points", xytext=(8, 8), fontsize=9)

    if max_sharpe:
        ax.scatter(max_sharpe["volatility"], max_sharpe["return"], marker="*", s=300,
                   color="red", zorder=5, label="Max Sharpe")
        ax.annotate("Max Sharpe", (max_sharpe["volatility"], max_sharpe["return"]),
                    textcoords="offset points", xytext=(8, 8), fontsize=9)

    if min_var and max_sharpe and risk_free_rate > 0:
        cal_x = np.linspace(0, max(frontier_volatilities) * 1.2, 50)
        slope = (max_sharpe["return"] - risk_free_rate) / max_sharpe["volatility"]
        cal_y = risk_free_rate + slope * cal_x
        ax.plot(cal_x, cal_y, color="gray", linestyle="--", label="Capital Allocation Line")

    if individual_assets:
        vols = [v[0] for v in individual_assets.values()]
        rets = [v[1] for v in individual_assets.values()]
        ax.scatter(vols, rets, color="gray", s=40, zorder=4)
        for ticker, (v, r) in individual_assets.items():
            ax.annotate(ticker, (v, r), textcoords="offset points",
                        xytext=(0, 6), fontsize=8, ha="center")

    ax.set_title("Efficient Frontier")
    ax.set_xlabel("Annualized Volatility")
    ax.set_ylabel("Annualized Expected Return")
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def chart_correlation_heatmap(corr_matrix: pd.DataFrame) -> Figure:
    labels = corr_matrix.columns.tolist()
    z = corr_matrix.values
    n = len(labels)

    fig, ax = plt.subplots(figsize=(max(6, n * 0.8), max(5, n * 0.7)))
    im = ax.imshow(z, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)

    for i in range(n):
        for j in range(n):
            color = "white" if abs(z[i][j]) > 0.6 else "black"
            ax.text(j, i, f"{z[i][j]:.2f}", ha="center", va="center",
                    fontsize=8, color=color)

    fig.colorbar(im, ax=ax, label="Correlation", shrink=0.8)
    ax.set_title("Asset Correlation Matrix")
    fig.tight_layout()
    return fig


def chart_weights_pie(weights: pd.Series, title: str = "Portfolio Weights") -> Figure:
    w = weights[weights.abs() > 0.005].sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        w.values, labels=w.index, autopct="%1.1f%%",
        pctdistance=0.82, wedgeprops=dict(width=0.35, edgecolor="white"),
        textprops=dict(fontsize=10),
    )
    for t in autotexts:
        t.set_fontsize(8)
    ax.set_title(title, fontsize=14, pad=20)
    fig.tight_layout()
    return fig


def chart_equity_curves(
    curves: dict[str, pd.Series],
    benchmark: pd.Series | None = None,
    benchmark_ticker: str = "Benchmark",
    live_start_date: datetime | None = None,
) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 7))

    for name, series in curves.items():
        normalized = series / series.iloc[0]
        ax.plot(normalized.index, normalized.values, linewidth=1.5, label=name)

    if benchmark is not None:
        normalized = benchmark / benchmark.iloc[0]
        ax.plot(normalized.index, normalized.values, color="black",
                linestyle="--", linewidth=1.5, label=f"Benchmark ({benchmark_ticker})")

    if live_start_date is not None:
        ax.axvline(x=live_start_date, color="gray", linestyle=":", linewidth=1.5, alpha=0.7)
        ymin, ymax = ax.get_ylim()
        ax.annotate("Live Start", xy=(live_start_date, ymax),
                    xytext=(10, -15), textcoords="offset points",
                    fontsize=9, color="gray", fontstyle="italic")

    title = "Portfolio Performance: Backtest vs Live" if live_start_date else "Portfolio Equity Curves"
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of $1")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def chart_drawdown(drawdown_series: dict[str, pd.Series]) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 5))

    for name, dd in drawdown_series.items():
        ax.fill_between(dd.index, 0, -dd.values, alpha=0.4, label=name)

    ax.set_title("Drawdown")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def chart_rolling_sharpe(
    rolling_sharpes: dict[str, pd.Series],
    window_label: str = "63-day",
) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 5))

    for name, rs in rolling_sharpes.items():
        ax.plot(rs.index, rs.values, linewidth=1.2, label=name)

    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_title(f"Rolling Sharpe Ratio ({window_label})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sharpe Ratio")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def chart_performance_dashboard(
    equity_curves: dict[str, pd.Series],
    drawdowns: dict[str, pd.Series],
    rolling_sharpes: dict[str, pd.Series],
    benchmark: pd.Series | None = None,
    benchmark_ticker: str = "Benchmark",
) -> Figure:
    fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)

    for name, series in equity_curves.items():
        normalized = series / series.iloc[0]
        axes[0].plot(normalized.index, normalized.values, linewidth=1.2, label=name)
    if benchmark is not None:
        normalized = benchmark / benchmark.iloc[0]
        axes[0].plot(normalized.index, normalized.values, color="black",
                     linestyle="--", linewidth=1.2, label=f"Benchmark ({benchmark_ticker})")
    axes[0].set_title("Equity Curves")
    axes[0].set_ylabel("Growth of $1")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    for name, dd in drawdowns.items():
        axes[1].fill_between(dd.index, 0, -dd.values, alpha=0.4, label=name)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown")
    axes[1].yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
    axes[1].grid(True, alpha=0.3)

    for name, rs in rolling_sharpes.items():
        axes[2].plot(rs.index, rs.values, linewidth=1.0, label=name)
    axes[2].axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    axes[2].set_title("Rolling Sharpe Ratio")
    axes[2].set_ylabel("Sharpe Ratio")
    axes[2].set_xlabel("Date")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("Performance Dashboard", fontsize=16, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def export_chart_png(fig: Figure, filepath: Path, width: int = 1200, height: int = 700) -> Path:
    """Export matplotlib figure to PNG."""
    dpi = 100
    fig.set_size_inches(width / dpi, height / dpi)
    fig.savefig(str(filepath), dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return filepath


def export_chart_base64(fig: Figure) -> str:
    """Export matplotlib figure as base64-encoded PNG for HTML embedding."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f'<img src="data:image/png;base64,{b64}" style="max-width:100%;">'
