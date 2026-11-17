"""Dividend income visualization: stacked bar of net income + tax per symbol.

Net income and withholding tax are stacked so the chart shows both the income
kept and the tax lost per holding. Builder is pure — rendering to HTML/PNG is
done by ib_common.charts.render in the report layer.
"""
from __future__ import annotations
import plotly.graph_objects as go
from ib_common.schema import Dividend
from .dividend_analysis import income_by_symbol


def build_chart(dividends: list[Dividend]) -> go.Figure:
    """Stacked bar per symbol: net income (bottom) + withholding tax (top)."""
    inc = income_by_symbol(dividends)
    symbols = list(inc.keys())
    net = [inc[s]["net"] for s in symbols]
    tax = [inc[s]["tax"] for s in symbols]
    fig = go.Figure(data=[
        go.Bar(name="Net income", x=symbols, y=net),
        go.Bar(name="Withholding tax", x=symbols, y=tax),
    ])
    fig.update_layout(barmode="stack", title="Dividend income by symbol (net + tax)")
    return fig
