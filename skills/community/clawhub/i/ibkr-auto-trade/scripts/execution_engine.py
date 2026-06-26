"""
execution_engine.py — Order placement, modification, cancellation, and position management.

Uses ib_insync. Supports market/limit bracket orders with automatic stop loss.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from ib_insync import (
    IB,
    MarketOrder,
    LimitOrder,
    StopOrder,
    Stock,
    Trade,
    Position,
    util,
)
from loguru import logger

from strategy_engine import Signal


@dataclass
class ExecutedTrade:
    signal: Signal
    ib_trade: Trade
    order_id: int
    bracket_orders: list | None = None


class ExecutionEngine:
    def __init__(self, cfg: dict, ib: IB):
        self.cfg = cfg
        self.ib = ib
        self.exec_cfg = cfg["execution"]
        self.data_cfg = cfg["data"]
        self._placed_signals: set[str] = set()  # Duplicate guard
        logger.info("ExecutionEngine initialized.")

    # ── Market Data ────────────────────────────────────────────────────────────

    def fetch_bars(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch historical bars from IBKR for a symbol."""
        contract = Stock(symbol, "SMART", "USD")
        try:
            self.ib.qualifyContracts(contract)
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime="",
                durationStr=self.data_cfg["duration"],
                barSizeSetting=self.data_cfg["bar_size"],
                whatToShow=self.data_cfg["what_to_show"],
                useRTH=self.data_cfg["use_rth"],
                formatDate=1,
            )
            if not bars:
                logger.warning(f"No bars returned for {symbol}")
                return None
            df = util.df(bars)
            df.columns = [c.lower() for c in df.columns]
            return df
        except Exception as e:
            logger.error(f"fetch_bars({symbol}) failed: {e}")
            return None

    # ── Order Execution ────────────────────────────────────────────────────────

    def execute_trade(self, signal: Signal) -> Optional[ExecutedTrade]:
        """
        Place a bracket order: entry + stop loss + profit target.
        Includes duplicate guard and retry logic.
        """
        # Duplicate guard
        if signal.signal_id in self._placed_signals:
            logger.warning(f"Duplicate signal {signal.signal_id} ignored.")
            return None
        self._placed_signals.add(signal.signal_id)

        contract = Stock(signal.symbol, "SMART", "USD")
        try:
            self.ib.qualifyContracts(contract)
        except Exception as e:
            logger.error(f"Contract qualification failed for {signal.symbol}: {e}")
            return None

        action = "BUY" if signal.direction == "LONG" else "SELL"
        close_action = "SELL" if signal.direction == "LONG" else "BUY"
        qty = signal.quantity
        entry = round(signal.entry_price, 2)
        stop = round(signal.stop_price, 2)
        target = round(signal.target_price, 2)

        use_bracket = self.exec_cfg.get("use_bracket_orders", True)
        order_type = self.exec_cfg.get("order_type", "LMT")

        for attempt in range(1, self.exec_cfg["retry_attempts"] + 1):
            try:
                if use_bracket:
                    # Pre-assign order IDs so parentId is correct before placeOrder
                    parent_id = self.ib.client.getReqId()

                    # Entry order
                    if order_type == "MKT":
                        parent = MarketOrder(action, qty)
                    else:
                        lmt_offset = entry * (self.exec_cfg["limit_offset_pct"] / 100)
                        limit_price = round(
                            entry + lmt_offset if action == "BUY" else entry - lmt_offset, 2
                        )
                        parent = LimitOrder(action, qty, limit_price)

                    parent.orderId = parent_id
                    parent.transmit = False

                    # Profit target (limit)
                    take_profit = LimitOrder(close_action, qty, target)
                    take_profit.orderId = self.ib.client.getReqId()
                    take_profit.parentId = parent_id
                    take_profit.transmit = False

                    # Stop loss
                    stop_loss = StopOrder(close_action, qty, stop)
                    stop_loss.orderId = self.ib.client.getReqId()
                    stop_loss.parentId = parent_id
                    stop_loss.transmit = True  # Transmits all three

                    parent_trade = self.ib.placeOrder(contract, parent)
                    tp_trade = self.ib.placeOrder(contract, take_profit)
                    sl_trade = self.ib.placeOrder(contract, stop_loss)

                    self.ib.sleep(1)

                    logger.info(
                        f"✅ Bracket order placed: {action} {qty}x {signal.symbol} "
                        f"@ {entry} | SL={stop} | TP={target} | "
                        f"parentOrderId={parent_id}"
                    )
                    return ExecutedTrade(
                        signal=signal,
                        ib_trade=parent_trade,
                        order_id=parent_id,
                        bracket_orders=[parent_trade, tp_trade, sl_trade],
                    )
                else:
                    # Simple entry only (stop attached separately)
                    if order_type == "MKT":
                        order = MarketOrder(action, qty)
                    else:
                        order = LimitOrder(action, qty, entry)
                    trade = self.ib.placeOrder(contract, order)
                    self.ib.sleep(1)
                    logger.info(
                        f"✅ Order placed: {action} {qty}x {signal.symbol} @ {entry} "
                        f"orderId={trade.order.orderId}"
                    )
                    return ExecutedTrade(signal=signal, ib_trade=trade, order_id=trade.order.orderId)

            except Exception as e:
                logger.warning(f"Order attempt {attempt} failed for {signal.symbol}: {e}")
                if attempt < self.exec_cfg["retry_attempts"]:
                    time.sleep(self.exec_cfg["retry_delay_sec"])

        logger.error(f"All order attempts failed for {signal.symbol}.")
        return None

    # ── Position Management ────────────────────────────────────────────────────

    def get_positions(self) -> list[Position]:
        """Return all current open positions."""
        try:
            return self.ib.positions()
        except Exception as e:
            logger.error(f"get_positions failed: {e}")
            return []

    def get_open_orders(self) -> list[Trade]:
        """Return all pending open orders."""
        try:
            return self.ib.openTrades()
        except Exception as e:
            logger.error(f"get_open_orders failed: {e}")
            return []

    def close_trade(self, position: Position) -> bool:
        """Market-close an open position."""
        symbol = position.contract.symbol
        qty = abs(int(position.position))
        action = "SELL" if position.position > 0 else "BUY"
        contract = position.contract
        try:
            order = MarketOrder(action, qty)
            trade = self.ib.placeOrder(contract, order)
            self.ib.sleep(1)
            logger.info(f"Closing position: {action} {qty}x {symbol}")
            return True
        except Exception as e:
            logger.error(f"close_trade({symbol}) failed: {e}")
            return False

    def close_all_positions(self) -> None:
        """Emergency close all open positions (shutdown hook)."""
        positions = self.get_positions()
        logger.warning(f"Closing all {len(positions)} positions...")
        for pos in positions:
            self.close_trade(pos)

    def adjust_stop(self, order_id: int, new_stop: float) -> bool:
        """Modify an existing stop loss order to a new price."""
        try:
            trades = self.get_open_orders()
            for trade in trades:
                if trade.order.orderId == order_id and trade.order.orderType == "STP":
                    trade.order.auxPrice = round(new_stop, 2)
                    self.ib.placeOrder(trade.contract, trade.order)
                    logger.info(f"Adjusted stop for orderId={order_id} to {new_stop}")
                    return True
            logger.warning(f"No stop order found with orderId={order_id}")
            return False
        except Exception as e:
            logger.error(f"adjust_stop failed: {e}")
            return False

    def cancel_trade(self, order_id: int) -> bool:
        """Cancel a pending order by ID."""
        try:
            trades = self.get_open_orders()
            for trade in trades:
                if trade.order.orderId == order_id:
                    self.ib.cancelOrder(trade.order)
                    self.ib.sleep(1)
                    logger.info(f"Cancelled order {order_id}")
                    return True
            logger.warning(f"Order {order_id} not found in open orders.")
            return False
        except Exception as e:
            logger.error(f"cancel_trade({order_id}) failed: {e}")
            return False

    # ── Position Monitoring ────────────────────────────────────────────────────

    def monitor_positions(self, positions: list[Position], perf_tracker) -> None:
        """
        Monitor open positions for exit conditions.
        Called each loop iteration. Marks closed trades in perf_tracker.
        """
        open_orders = self.get_open_orders()
        active_symbols = {t.contract.symbol for t in open_orders}

        for pos in positions:
            symbol = pos.contract.symbol
            if symbol not in active_symbols:
                # Position is open but no child orders — something closed it
                logger.info(f"Position {symbol} appears to have closed (no open orders).")
                perf_tracker.mark_trade_closed(symbol, exit_reason="bracket_fill_or_stop")
