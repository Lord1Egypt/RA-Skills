"""Tests for rebalance.py — order generation."""

import pandas as pd
import pytest

from mpt_portfolio.rebalance import generate_orders, TradeOrder


class TestGenerateOrders:
    def test_basic_rebalance(self):
        current = pd.Series({"A": 0.6, "B": 0.4})
        target = pd.Series({"A": 0.5, "B": 0.5})
        prices = pd.Series({"A": 100.0, "B": 50.0})
        orders = generate_orders(current, target, 100_000, prices, 0.001)
        assert len(orders) == 2
        sell = [o for o in orders if o.action == "SELL"]
        buy = [o for o in orders if o.action == "BUY"]
        assert len(sell) == 1
        assert len(buy) == 1
        assert sell[0].ticker == "A"
        assert buy[0].ticker == "B"

    def test_no_orders_when_aligned(self):
        current = pd.Series({"A": 0.5, "B": 0.5})
        target = pd.Series({"A": 0.5, "B": 0.5})
        prices = pd.Series({"A": 100.0, "B": 50.0})
        orders = generate_orders(current, target, 100_000, prices, 0.001)
        assert len(orders) == 0

    def test_dollar_amounts_net_to_zero(self):
        current = pd.Series({"A": 0.7, "B": 0.2, "C": 0.1})
        target = pd.Series({"A": 0.4, "B": 0.3, "C": 0.3})
        prices = pd.Series({"A": 100.0, "B": 50.0, "C": 25.0})
        orders = generate_orders(current, target, 100_000, prices, 0.001)
        total_dollars = sum(o.dollar_amount for o in orders)
        assert abs(total_dollars) < 0.01

    def test_new_asset_added(self):
        current = pd.Series({"A": 1.0})
        target = pd.Series({"A": 0.5, "B": 0.5})
        prices = pd.Series({"A": 100.0, "B": 50.0})
        orders = generate_orders(current, target, 100_000, prices, 0.001)
        buy = [o for o in orders if o.action == "BUY"]
        assert any(o.ticker == "B" for o in buy)

    def test_shares_calculation(self):
        current = pd.Series({"A": 0.0})
        target = pd.Series({"A": 1.0})
        prices = pd.Series({"A": 50.0})
        orders = generate_orders(current, target, 10_000, prices, 0.0)
        assert len(orders) == 1
        assert abs(orders[0].shares - 200.0) < 0.01  # $10,000 / $50 = 200 shares
