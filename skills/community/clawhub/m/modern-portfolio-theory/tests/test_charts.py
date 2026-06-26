"""Tests for charts.py — matplotlib chart generation."""

from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from matplotlib.figure import Figure

from mpt_portfolio.charts import (
    chart_correlation_heatmap,
    chart_drawdown,
    chart_efficient_frontier,
    chart_equity_curves,
    chart_rolling_sharpe,
    chart_weights_pie,
    export_chart_base64,
    export_chart_png,
)


class TestCharts:
    def test_efficient_frontier(self):
        fig = chart_efficient_frontier(
            np.array([0.05, 0.08, 0.10]),
            np.array([0.10, 0.12, 0.18]),
            min_var={"return": 0.05, "volatility": 0.10},
            max_sharpe={"return": 0.10, "volatility": 0.15},
        )
        assert isinstance(fig, Figure)

    def test_efficient_frontier_with_assets(self):
        fig = chart_efficient_frontier(
            np.array([0.05, 0.08, 0.10]),
            np.array([0.10, 0.12, 0.18]),
            individual_assets={"A": (0.15, 0.08), "B": (0.20, 0.12)},
            risk_free_rate=0.04,
        )
        assert isinstance(fig, Figure)

    def test_correlation_heatmap(self):
        corr = pd.DataFrame(
            [[1.0, 0.5], [0.5, 1.0]], index=["A", "B"], columns=["A", "B"],
        )
        fig = chart_correlation_heatmap(corr)
        assert isinstance(fig, Figure)

    def test_weights_pie(self):
        w = pd.Series({"A": 0.4, "B": 0.35, "C": 0.25})
        fig = chart_weights_pie(w)
        assert isinstance(fig, Figure)

    def test_equity_curves(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        curves = {"Strategy1": pd.Series(np.linspace(100, 120, 100), index=dates)}
        fig = chart_equity_curves(curves)
        assert isinstance(fig, Figure)

    def test_drawdown(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        dd = {"S1": pd.Series(np.random.default_rng(42).uniform(0, 0.1, 100), index=dates)}
        fig = chart_drawdown(dd)
        assert isinstance(fig, Figure)

    def test_rolling_sharpe(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        rs = {"S1": pd.Series(np.random.default_rng(42).uniform(-1, 2, 100), index=dates)}
        fig = chart_rolling_sharpe(rs)
        assert isinstance(fig, Figure)

    def test_weights_pie_filters_small(self):
        w = pd.Series({"A": 0.50, "B": 0.49, "C": 0.004, "D": 0.006})
        fig = chart_weights_pie(w)
        assert isinstance(fig, Figure)

    def test_export_chart_base64(self):
        fig = chart_weights_pie(pd.Series({"A": 0.6, "B": 0.4}))
        html = export_chart_base64(fig)
        assert html.startswith('<img src="data:image/png;base64,')
        assert html.endswith('">')

    def test_equity_curves_with_benchmark_ticker(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        curves = {"Strategy1": pd.Series(np.linspace(100, 120, 100), index=dates)}
        benchmark = pd.Series(np.linspace(100, 115, 100), index=dates)
        fig = chart_equity_curves(curves, benchmark=benchmark, benchmark_ticker="QQQ")
        assert isinstance(fig, Figure)

    def test_equity_curves_with_live_start_date(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        curves = {"Strategy1": pd.Series(np.linspace(100, 120, 100), index=dates)}
        live_date = datetime(2023, 3, 1)
        fig = chart_equity_curves(curves, live_start_date=live_date)
        assert isinstance(fig, Figure)

    def test_equity_curves_backward_compatible(self):
        dates = pd.bdate_range("2023-01-03", periods=100)
        curves = {"S1": pd.Series(np.linspace(100, 120, 100), index=dates)}
        fig = chart_equity_curves(curves)
        assert isinstance(fig, Figure)

    def test_export_chart_png(self, tmp_path):
        fig = chart_weights_pie(pd.Series({"A": 0.6, "B": 0.4}))
        path = export_chart_png(fig, tmp_path / "test.png")
        assert path.exists()
        assert path.stat().st_size > 0
