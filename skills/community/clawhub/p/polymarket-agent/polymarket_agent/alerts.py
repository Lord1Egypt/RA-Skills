"""Whale alerts with deduplication across runs.

Designed to run under `openclaw cron`. Two details make the difference between
a useful alert and spam:

1. **Deduplication by transaction hash.** A cron every 5 min with a 15 min
   window would re-see the same trades three times. The state remembers what
   was already announced.
2. **Explicit silence.** OpenClaw suppresses delivery when the output is
   exactly `NO_REPLY` — so "no whales right now" does not become a
   notification. Without it, an alert every 5 minutes turns into noise and the
   user switches everything off.

The queried window is always larger than the cron interval (deliberate
overlap): trades arrive with a small indexing delay, and it is better to
re-see them and deduplicate than to miss them.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from .paths import app_dir, write_private
from .whales import WhaleTrade, recent_whales

#: Sentinel OpenClaw recognizes to suppress delivery of the cron output.
NO_REPLY = "NO_REPLY"

#: How many hashes to remember. Covers days of alerts without growing unbounded.
MAX_SEEN = 2000

#: Trades seen longer ago than this are forgotten — they have already left any
#: plausible query window, so they cannot produce a repeat alert.
SEEN_TTL_SECONDS = 24 * 60 * 60


def state_path():
    return app_dir() / "alerts.json"


@dataclass
class AlertState:
    seen: Dict[str, float] = field(default_factory=dict)
    last_run: float = 0.0

    @classmethod
    def load(cls) -> "AlertState":
        path = state_path()
        if not path.exists():
            return cls()
        try:
            with open(path, encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return cls()
        if not isinstance(raw, dict):
            return cls()
        seen = raw.get("seen")
        if not isinstance(seen, dict):
            seen = {}
        clean = {
            str(k): float(v)
            for k, v in seen.items()
            if isinstance(v, (int, float))
        }
        return cls(seen=clean, last_run=float(raw.get("last_run") or 0.0))

    def save(self) -> None:
        self._prune()
        write_private(
            state_path(),
            json.dumps({"seen": self.seen, "last_run": self.last_run}, indent=0),
        )

    def _prune(self) -> None:
        cutoff = time.time() - SEEN_TTL_SECONDS
        self.seen = {k: v for k, v in self.seen.items() if v >= cutoff}
        if len(self.seen) > MAX_SEEN:
            newest = sorted(self.seen.items(), key=lambda kv: kv[1], reverse=True)
            self.seen = dict(newest[:MAX_SEEN])

    def is_new(self, trade: WhaleTrade) -> bool:
        return bool(trade.tx_hash) and trade.tx_hash not in self.seen

    def mark(self, trade: WhaleTrade) -> None:
        if trade.tx_hash:
            self.seen[trade.tx_hash] = time.time()


def new_whales(
    min_notional: float = 25_000.0,
    window_seconds: int = 900,
    limit: int = 100,
    persist: bool = True,
) -> List[WhaleTrade]:
    """Whales not yet announced. Marks the returned ones as seen.

    `persist=False` lets you preview without consuming the state (useful for
    the user to test the alert before scheduling it).
    """
    state = AlertState.load()
    trades = recent_whales(
        min_notional=min_notional, window_seconds=window_seconds, limit=limit
    )
    fresh = [t for t in trades if state.is_new(t)]

    if persist:
        for trade in fresh:
            state.mark(trade)
        state.last_run = time.time()
        state.save()

    return fresh


def format_alert(trades: List[WhaleTrade], min_notional: float) -> str:
    """Alert message, or NO_REPLY when there is nothing new."""
    if not trades:
        return NO_REPLY

    total = sum(t.notional_usd for t in trades)
    lines = [
        f"🐋 *{len(trades)} trade(s) above ${min_notional:,.0f}* "
        f"— ${total:,.0f} in total",
        "",
    ]
    for trade in trades[:15]:
        lines.append(
            f"• *${trade.notional_usd:,.0f}* {trade.side} `{trade.outcome}` "
            f"@ ${trade.price:.3f} ({trade.implied_pct:.0f}%)"
        )
        lines.append(f"  {trade.title[:90]}")
        lines.append(f"  by {trade.trader}" + (f" — {trade.url}" if trade.url else ""))
        lines.append("")

    if len(trades) > 15:
        lines.append(f"…and {len(trades) - 15} more trade(s).")

    return "\n".join(lines).rstrip()


def reset_state() -> bool:
    """Forget everything already announced."""
    path = state_path()
    if not path.exists():
        return False
    path.unlink(missing_ok=True)
    return True
