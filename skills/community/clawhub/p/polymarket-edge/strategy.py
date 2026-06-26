"""
BTC 5-Minute Auto-Trading Strategy for Polymarket
──────────────────────────────────────────────────
Logic overview:
  1. Fetch active BTC price markets (e.g. "Will BTC be above $X by date?").
  2. Pull 5-minute price history for YES token.
  3. Compute momentum (EMA crossover) and mean-reversion signals.
  4. Generate a trade signal: BUY_YES / BUY_NO / HOLD.
  5. Optionally place the order if live trading is enabled.

Signal rules (tunable via config):
  - EMA(5) crosses above EMA(20)  → BUY_YES  (momentum bullish)
  - EMA(5) crosses below EMA(20)  → BUY_NO   (momentum bearish)
  - YES price < 0.15              → too cheap / skip (low confidence)
  - YES price > 0.85              → too expensive / skip
  - Spread > 0.05                 → illiquid / skip
"""
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from polymarket_client import (
    Market,
    get_active_btc_markets,
    get_order_book,
    get_price_history,
    get_midpoint,
    get_spread,
    place_limit_order,
)

log = logging.getLogger("strategy")

# ── Config ────────────────────────────────────────────────────────────────────

@dataclass
class StrategyConfig:
    ema_fast: int   = 5       # Fast EMA period
    ema_slow: int   = 20      # Slow EMA period
    interval: str   = "5m"    # Candle interval
    fidelity: int   = 60      # Number of candles to fetch
    min_price: float = 0.15   # Skip YES tokens priced below this
    max_price: float = 0.85   # Skip YES tokens priced above this
    max_spread: float = 0.05  # Skip illiquid markets
    order_size: float = 5.0   # USDC per trade
    auto_trade: bool = False   # Set True to place real orders


DEFAULT_CONFIG = StrategyConfig()


# ── EMA ───────────────────────────────────────────────────────────────────────

def ema(prices: list[float], period: int) -> list[float]:
    """Compute exponential moving average."""
    if len(prices) < period:
        return []
    k = 2 / (period + 1)
    ema_values = [sum(prices[:period]) / period]
    for p in prices[period:]:
        ema_values.append(p * k + ema_values[-1] * (1 - k))
    return ema_values


def crossover_signal(fast: list[float], slow: list[float]) -> str:
    """
    Returns:
      'BUY_YES'  — fast crossed above slow on the last two candles
      'BUY_NO'   — fast crossed below slow on the last two candles
      'HOLD'     — no crossover
    """
    if len(fast) < 2 or len(slow) < 2:
        return "HOLD"
    # Align lengths (slow EMA is shorter due to warm-up)
    min_len = min(len(fast), len(slow))
    f, s = fast[-min_len:], slow[-min_len:]
    prev_above = f[-2] > s[-2]
    curr_above = f[-1] > s[-1]
    if not prev_above and curr_above:
        return "BUY_YES"
    if prev_above and not curr_above:
        return "BUY_NO"
    return "HOLD"


# ── Signal generation ─────────────────────────────────────────────────────────

@dataclass
class TradeSignal:
    market_id: str
    question: str
    yes_token_id: str
    no_token_id: str
    action: str           # BUY_YES | BUY_NO | HOLD | SKIP
    yes_price: float
    no_price: float
    spread: float
    ema_fast_last: float
    ema_slow_last: float
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


async def analyze_market(market: Market, cfg: StrategyConfig = DEFAULT_CONFIG) -> TradeSignal:
    """Run the strategy on a single market. Returns a TradeSignal."""
    if len(market.clob_token_ids) < 2:
        return TradeSignal(
            market_id=market.id, question=market.question,
            yes_token_id="", no_token_id="",
            action="SKIP", yes_price=0, no_price=0, spread=0,
            ema_fast_last=0, ema_slow_last=0,
            reason="Market has no tradeable tokens",
        )

    yes_token = market.clob_token_ids[0]
    no_token  = market.clob_token_ids[1]

    # Fetch price + spread in parallel
    mid, spread_val = await asyncio.gather(
        get_midpoint(yes_token),
        get_spread(yes_token),
    )
    if mid is None:
        return TradeSignal(
            market_id=market.id, question=market.question,
            yes_token_id=yes_token, no_token_id=no_token,
            action="SKIP", yes_price=0, no_price=0, spread=0,
            ema_fast_last=0, ema_slow_last=0,
            reason="No midpoint price available",
        )

    yes_price = float(mid)
    no_price  = round(1.0 - yes_price, 4)
    spread    = float(spread_val or 0)

    # Liquidity check
    if spread > cfg.max_spread:
        return TradeSignal(
            market_id=market.id, question=market.question,
            yes_token_id=yes_token, no_token_id=no_token,
            action="SKIP", yes_price=yes_price, no_price=no_price, spread=spread,
            ema_fast_last=0, ema_slow_last=0,
            reason=f"Spread {spread:.3f} exceeds limit {cfg.max_spread}",
        )

    # Price sanity
    if yes_price < cfg.min_price or yes_price > cfg.max_price:
        return TradeSignal(
            market_id=market.id, question=market.question,
            yes_token_id=yes_token, no_token_id=no_token,
            action="SKIP", yes_price=yes_price, no_price=no_price, spread=spread,
            ema_fast_last=0, ema_slow_last=0,
            reason=f"YES price {yes_price:.3f} outside tradeable range [{cfg.min_price}, {cfg.max_price}]",
        )

    # 5-min candle data
    history = await get_price_history(yes_token, interval=cfg.interval, fidelity=cfg.fidelity)
    prices = [float(c.get("p") or c.get("price") or c.get("c") or 0) for c in history if c]
    prices = [p for p in prices if p > 0]

    if len(prices) < cfg.ema_slow + 2:
        return TradeSignal(
            market_id=market.id, question=market.question,
            yes_token_id=yes_token, no_token_id=no_token,
            action="HOLD", yes_price=yes_price, no_price=no_price, spread=spread,
            ema_fast_last=0, ema_slow_last=0,
            reason=f"Not enough history: {len(prices)} candles (need {cfg.ema_slow + 2})",
        )

    fast_ema = ema(prices, cfg.ema_fast)
    slow_ema = ema(prices, cfg.ema_slow)
    signal   = crossover_signal(fast_ema, slow_ema)

    ema_fast_last = fast_ema[-1] if fast_ema else 0
    ema_slow_last = slow_ema[-1] if slow_ema else 0

    reason_map = {
        "BUY_YES": f"EMA({cfg.ema_fast}) {ema_fast_last:.3f} crossed above EMA({cfg.ema_slow}) {ema_slow_last:.3f}",
        "BUY_NO":  f"EMA({cfg.ema_fast}) {ema_fast_last:.3f} crossed below EMA({cfg.ema_slow}) {ema_slow_last:.3f}",
        "HOLD":    f"EMA({cfg.ema_fast})={ema_fast_last:.3f}, EMA({cfg.ema_slow})={ema_slow_last:.3f} — no crossover",
    }

    return TradeSignal(
        market_id=market.id, question=market.question,
        yes_token_id=yes_token, no_token_id=no_token,
        action=signal,
        yes_price=yes_price, no_price=no_price, spread=spread,
        ema_fast_last=ema_fast_last, ema_slow_last=ema_slow_last,
        reason=reason_map.get(signal, "HOLD"),
    )


# ── Auto-trader ───────────────────────────────────────────────────────────────

_running = False
_trade_log: list[dict] = []


async def run_once(cfg: StrategyConfig = DEFAULT_CONFIG) -> list[TradeSignal]:
    """Fetch BTC markets, analyse each, optionally trade. Returns all signals."""
    markets = await get_active_btc_markets(limit=5)
    signals = await asyncio.gather(*[analyze_market(m, cfg) for m in markets])

    for sig in signals:
        entry = {
            "ts": sig.timestamp,
            "market": sig.question[:60],
            "action": sig.action,
            "yes_price": sig.yes_price,
            "reason": sig.reason,
        }
        _trade_log.append(entry)
        if len(_trade_log) > 500:
            _trade_log.pop(0)

        if cfg.auto_trade and sig.action in ("BUY_YES", "BUY_NO"):
            token_id = sig.yes_token_id if sig.action == "BUY_YES" else sig.no_token_id
            buy_price = sig.yes_price if sig.action == "BUY_YES" else sig.no_price
            try:
                order = await place_limit_order(
                    token_id=token_id,
                    side="BUY",
                    price=round(buy_price + 0.01, 2),  # slight premium to fill
                    size=round(cfg.order_size / buy_price, 2),
                )
                entry["order_id"] = order.order_id
                entry["order_status"] = order.status
                log.info("Placed order %s for %s", order.order_id, sig.question[:40])
            except Exception as exc:
                log.warning("Order failed for %s: %s", sig.question[:40], exc)
                entry["order_error"] = str(exc)

    return list(signals)


async def auto_trade_loop(interval_seconds: int = 300, cfg: StrategyConfig = DEFAULT_CONFIG):
    """Run the strategy every `interval_seconds` (default 5 min)."""
    global _running
    _running = True
    log.info("Auto-trader started. Interval: %ds.", interval_seconds)
    while _running:
        try:
            signals = await run_once(cfg)
            actionable = [s for s in signals if s.action not in ("HOLD", "SKIP")]
            log.info("Cycle done. %d signal(s) actionable out of %d markets.", len(actionable), len(signals))
        except Exception as exc:
            log.error("Strategy cycle error: %s", exc)
        await asyncio.sleep(interval_seconds)
    log.info("Auto-trader stopped.")


def stop_auto_trader():
    global _running
    _running = False


def get_trade_log() -> list[dict]:
    return list(reversed(_trade_log))


def is_running() -> bool:
    return _running
