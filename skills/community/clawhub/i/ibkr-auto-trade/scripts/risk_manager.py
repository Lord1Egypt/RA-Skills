"""
risk_manager.py — Risk validation, position sizing, and kill switch.

All signals pass through this module before execution.
"""

from __future__ import annotations

from datetime import date
from typing import Tuple

from ib_insync import IB
from loguru import logger

from strategy_engine import Signal


class RiskManager:
    def __init__(self, cfg: dict, ib: IB):
        self.cfg = cfg
        self.ib = ib
        self.risk = cfg["risk"]
        self._kill_switch = False
        self._daily_start_value: float | None = None
        self._today = date.today()
        logger.info("RiskManager initialized.")

    # ── Account ────────────────────────────────────────────────────────────────

    def get_account_value(self) -> float:
        """Fetch Net Liquidation Value from IBKR account summary."""
        try:
            summary = self.ib.accountSummary()
            for item in summary:
                if item.tag == "NetLiquidation" and item.currency == "USD":
                    value = float(item.value)
                    if self._daily_start_value is None or date.today() != self._today:
                        self._daily_start_value = value
                        self._today = date.today()
                    return value
        except Exception as e:
            logger.error(f"Failed to get account value: {e}")
        return 0.0

    # ── Kill Switch ────────────────────────────────────────────────────────────

    def kill_switch_active(self) -> bool:
        if self._kill_switch:
            return True
        if self._daily_start_value is None:
            return False
        current = self.get_account_value()
        if current <= 0:
            return False
        daily_loss_pct = (self._daily_start_value - current) / self._daily_start_value * 100
        if daily_loss_pct >= self.risk["max_daily_loss_pct"]:
            logger.critical(
                f"🛑 Kill switch triggered: daily loss {daily_loss_pct:.2f}% "
                f"exceeds {self.risk['max_daily_loss_pct']}%"
            )
            self._kill_switch = True
            return True
        return False

    def reset_kill_switch(self) -> None:
        """Manually reset kill switch (requires explicit call, not automatic)."""
        self._kill_switch = False
        self._daily_start_value = None
        logger.warning("Kill switch manually reset.")

    # ── Signal Validation ──────────────────────────────────────────────────────

    def validate_signal(self, signal: Signal, open_positions: list) -> Tuple[bool, str]:
        """
        Validate a signal against all risk rules.
        Returns (approved, reason).
        """
        # 1. Kill switch
        if self.kill_switch_active():
            return False, "Kill switch active"

        # 2. Max positions
        if len(open_positions) >= self.risk["max_positions"]:
            return False, f"Max positions ({self.risk['max_positions']}) reached"

        # 3. Stop loss must exist
        if signal.stop_price <= 0:
            return False, "No stop loss defined"

        # 4. Risk/reward check
        if signal.direction == "LONG":
            risk = signal.entry_price - signal.stop_price
            reward = signal.target_price - signal.entry_price
        else:
            risk = signal.stop_price - signal.entry_price
            reward = signal.entry_price - signal.target_price

        if risk <= 0:
            return False, "Invalid risk (stop on wrong side of entry)"

        rr_ratio = reward / risk
        min_rr = self.risk["min_risk_reward_ratio"]
        if rr_ratio < min_rr:
            return False, f"R:R {rr_ratio:.2f} below minimum {min_rr}"

        # 5. Confidence floor
        if signal.confidence < 0.2:
            return False, f"Signal confidence {signal.confidence} too low"

        return True, "OK"

    # ── Position Sizing ────────────────────────────────────────────────────────

    def size_position(self, signal: Signal, account_value: float) -> int:
        """
        Calculate share quantity using fixed fractional risk:
            shares = (account_value * max_risk_pct) / |entry - stop|
        """
        if account_value <= 0:
            return 0

        risk_per_share = abs(signal.entry_price - signal.stop_price)
        if risk_per_share <= 0:
            return 0

        max_risk_dollars = account_value * (self.risk["max_risk_per_trade_pct"] / 100)
        quantity = int(max_risk_dollars / risk_per_share)

        logger.debug(
            f"Position size for {signal.symbol}: "
            f"acct={account_value:.0f}, risk_$={max_risk_dollars:.2f}, "
            f"risk/share={risk_per_share:.4f}, qty={quantity}"
        )
        return max(quantity, 0)

    def get_daily_pnl_pct(self, current_value: float) -> float:
        """Return today's PnL as a percentage (negative = loss)."""
        if self._daily_start_value is None or self._daily_start_value == 0:
            return 0.0
        return (current_value - self._daily_start_value) / self._daily_start_value * 100
