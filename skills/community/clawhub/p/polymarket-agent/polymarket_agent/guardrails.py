"""Deterministic guard-rails between the AI and real money.

AUDIT FIX (Medium — "Autonomous Decision Making", 97%): v1.0.2 had a
`poly auto true` that disabled all confirmation, with no value cap, no expiry
and no trail. A prompt injected into a news article read by the agent could,
in principle, become a market order.

Principle: **the model proposes, the code disposes.** Nothing here depends on
the LLM behaving well. Every order passes through `evaluate_order`, which only
returns `allowed=True` if ALL limits are satisfied.

Layers, in the order they block:
  1. Kill switch (HALT file) — blocks everything, always.
  2. Numeric sanity (price in range, size > 0, no NaN/inf).
  3. Per-order cap (`max_position_usd`).
  4. Bankroll-fraction cap (`max_bankroll_pct`).
  5. Daily-spend cap (`max_daily_spend_usd`, from the journal).
  6. Open-order cap (`max_open_orders`).
  7. Human confirmation — waived only under VALID, non-expired autonomous mode.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import List, Optional

from . import journal
from .config import Settings
from .paths import halt_path

DAY_SECONDS = 24 * 60 * 60


@dataclass
class Decision:
    """The guard-rails' verdict on a proposed order."""

    allowed: bool
    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    requires_confirmation: bool = True
    notional: float = 0.0

    def blocked_summary(self) -> str:
        return "; ".join(self.reasons) or "blocked"


def halt_active() -> bool:
    return halt_path().exists()


def engage_halt(reason: str = "") -> None:
    """Kill switch. A file — works even with the process dead, and the user
    can trigger it by hand without depending on the skill."""
    from .paths import write_private

    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    write_private(halt_path(), f"{stamp}\n{reason}\n")
    journal.record(journal.Entry(kind="halt", status="engaged", detail=reason))


def release_halt() -> bool:
    path = halt_path()
    if not path.exists():
        return False
    path.unlink(missing_ok=True)
    journal.record(journal.Entry(kind="halt", status="released"))
    return True


def autonomous_active(settings: Settings) -> bool:
    """Autonomous mode only counts if enabled AND within its validity window.

    The expiry is mandatory: an autonomous mode left on and forgotten is
    exactly the scenario the audit flags as unsupervised financial loss.
    """
    if not settings.autonomous_mode:
        return False
    if settings.autonomous_expires_at <= 0:
        return False
    return time.time() < settings.autonomous_expires_at


def _finite(value: float) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def evaluate_order(
    side: str,
    price: float,
    size: float,
    settings: Settings,
    balance_usd: Optional[float] = None,
    open_orders: Optional[int] = None,
) -> Decision:
    """Apply every limit. Sends nothing — only decides.

    `open_orders` should come from the EXCHANGE when there is network; the
    journal is the offline fallback (see `journal.open_order_count`).
    """
    reasons: List[str] = []
    warnings: List[str] = []

    # 1. Kill switch
    if halt_active():
        reasons.append(
            f"kill switch active ({halt_path()}) — clear it with `poly resume` to resume trading"
        )

    # 2. Numeric sanity
    side_upper = (side or "").strip().upper()
    if side_upper not in {"BUY", "SELL"}:
        reasons.append(f"invalid side: {side!r} (use BUY or SELL)")

    if not _finite(price) or not _finite(size):
        reasons.append("price/size are not numeric")
        return Decision(False, reasons, warnings, True, 0.0)

    if not (settings.min_price <= price <= settings.max_price):
        reasons.append(
            f"price {price} outside the allowed range "
            f"[{settings.min_price}, {settings.max_price}]"
        )
    if size <= 0:
        reasons.append(f"size must be positive (got {size})")

    notional = round(price * size, 6)

    # 3. Per-order cap
    if notional > settings.max_position_usd:
        reasons.append(
            f"notional ${notional:.2f} exceeds the per-order cap "
            f"${settings.max_position_usd:.2f} (`poly config --key max_position_usd`)"
        )

    # 4. Bankroll fraction — only applies to buys (a sell doesn't consume balance).
    if side_upper == "BUY" and balance_usd is not None and balance_usd > 0:
        pct = (notional / balance_usd) * 100
        if pct > settings.max_bankroll_pct:
            reasons.append(
                f"order uses {pct:.1f}% of balance (${balance_usd:.2f}), above the "
                f"{settings.max_bankroll_pct:.1f}% limit"
            )
    elif side_upper == "BUY" and balance_usd is None:
        warnings.append("balance unavailable — bankroll % limit could not be checked")

    # 5. Daily spend
    if side_upper == "BUY":
        spent = journal.spend_since(DAY_SECONDS)
        if spent + notional > settings.max_daily_spend_usd:
            reasons.append(
                f"daily spend would breach the cap: ${spent:.2f} already spent in the last "
                f"24h + ${notional:.2f} > ${settings.max_daily_spend_usd:.2f}"
            )
        elif spent > 0:
            warnings.append(
                f"spend in the last 24h: ${spent:.2f} of ${settings.max_daily_spend_usd:.2f}"
            )

    # 6. Open orders
    live_orders = (
        open_orders if open_orders is not None else journal.open_order_count()
    )
    if live_orders >= settings.max_open_orders:
        reasons.append(
            f"{live_orders} open orders — cap is {settings.max_open_orders} "
            "(cancel one with `poly cancel` or raise `max_open_orders`)"
        )

    # 7. Human confirmation
    autonomous = autonomous_active(settings)
    requires_confirmation = not autonomous
    if settings.autonomous_mode and not autonomous:
        warnings.append(
            "autonomous mode was on but EXPIRED — human confirmation is required again"
        )
    if autonomous:
        remaining = settings.autonomous_expires_at - time.time()
        warnings.append(
            f"autonomous mode active for {remaining / 60:.0f} more min — "
            "orders within the limits go through unattended"
        )

    # Low liquidity is a warning, not a block (the agent decides this with the user).
    if settings.dry_run:
        warnings.append("DRY-RUN is on: the order will be validated and journaled, but NOT sent")

    return Decision(
        allowed=not reasons,
        reasons=reasons,
        warnings=warnings,
        requires_confirmation=requires_confirmation,
        notional=notional,
    )


def enable_autonomous(settings: Settings, hours: float) -> Settings:
    """Enable autonomous mode with a mandatory expiry (max 24h per call)."""
    hours = max(0.25, min(float(hours), 24.0))
    settings.autonomous_mode = True
    settings.autonomous_expires_at = time.time() + hours * 3600
    journal.record(
        journal.Entry(
            kind="autonomous",
            status="enabled",
            detail=f"expires in {hours:.2f}h; per-order cap ${settings.max_position_usd:.2f}; "
            f"daily cap ${settings.max_daily_spend_usd:.2f}",
        )
    )
    return settings


def disable_autonomous(settings: Settings) -> Settings:
    settings.autonomous_mode = False
    settings.autonomous_expires_at = 0.0
    journal.record(journal.Entry(kind="autonomous", status="disabled"))
    return settings
