"""
polymarket-candle-three-soldiers-trader
Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting
"Three White Soldiers" (3 consecutive strong UP intervals) and "Three Black Crows"
(3 consecutive strong DOWN intervals) -- classic candlestick continuation patterns.

Core edge: When three consecutive 5-min intervals all show strong directional bias
(all p>0.57 for soldiers, all p<0.43 for crows), the trend has momentum. If the
NEXT interval hasn't caught up yet (lagging the trend), there's edge in buying the
continuation. Three White Soldiers with next interval < 0.55 = buy YES (trend hasn't
been priced in). Three Black Crows with next interval > 0.45 = buy NO.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-candle-three-soldiers-trader"
SKILL_SLUG   = "polymarket-candle-three-soldiers-trader"

KEYWORDS = ['Bitcoin Up or Down', 'Ethereum Up or Down', 'Solana Up or Down']

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Pattern-specific tunables
SOLDIER_THRESHOLD = float(os.environ.get("SIMMER_SOLDIER_THRESHOLD", "0.57"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, SOLDIER_THRESHOLD
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        if live:
            _client.live = True
        try:
            _client.apply_skill_config(SKILL_SLUG)
        except AttributeError:
            pass  # apply_skill_config only available in Simmer runtime
        MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",       str(MAX_POSITION)))
        MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",         str(MIN_VOLUME)))
        MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",         str(MAX_SPREAD)))
        MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",           str(MIN_DAYS)))
        MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      str(MAX_POSITIONS)))
        YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",      str(YES_THRESHOLD)))
        NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",       str(NO_THRESHOLD)))
        MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",          str(MIN_TRADE)))
        SOLDIER_THRESHOLD  = float(os.environ.get("SIMMER_SOLDIER_THRESHOLD",  str(SOLDIER_THRESHOLD)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date + time window from 5-min interval questions
# ---------------------------------------------------------------------------

_INTERVAL_RE = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"                     # "March 29"
    r"(\d{1,2}:\d{2}\s*[AP]M)"                   # "10:50AM" (start)
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",                   # "10:55AM" (end)
    re.I,
)

_INTERVAL_RE_ALT = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL)\s+(?:Up|Down)"
    r".*?"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)


def parse_interval(question: str) -> tuple[str, str, str, str] | None:
    """
    Parse a crypto 5-min interval question.
    Returns (coin, date_str, start_time, end_time) or None.
    e.g. ("Bitcoin", "March 29", "10:50AM", "10:55AM")
    """
    m = _INTERVAL_RE.search(question)
    if not m:
        m = _INTERVAL_RE_ALT.search(question)
    if m:
        return (m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
    return None


def time_sort_key(start_time: str) -> int:
    """Convert a time like '10:50AM' to minutes since midnight for sorting."""
    try:
        t = start_time.upper().replace(" ", "")
        fmt = "%I:%M%p" if ":" in t else "%I%p"
        dt = datetime.strptime(t, fmt)
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def is_crypto_5min_market(question: str) -> bool:
    """Return True if the question looks like a crypto 5-min Up or Down market."""
    q = question.lower()
    has_coin = any(w in q for w in ("bitcoin", "btc", "ethereum", "eth", "solana", "sol"))
    has_updown = "up or down" in q or ("up" in q and "down" in q)
    has_time = any(w in q for w in ("am", "pm", "am-", "pm-", ":00", ":05",
                                     ":10", ":15", ":20", ":25", ":30",
                                     ":35", ":40", ":45", ":50", ":55"))
    return has_coin and has_updown and has_time


# ---------------------------------------------------------------------------
# Interval data class
# ---------------------------------------------------------------------------

class IntervalMarket:
    """Parsed 5-min interval market with sorting info."""
    __slots__ = ("market", "coin", "date_str", "start_time", "end_time", "sort_key", "p")

    def __init__(self, market, coin, date_str, start_time, end_time):
        self.market = market
        self.coin = coin
        self.date_str = date_str
        self.start_time = start_time
        self.end_time = end_time
        self.sort_key = time_sort_key(start_time)
        self.p = float(market.current_probability)


# ---------------------------------------------------------------------------
# Three Soldiers / Three Crows detection and signal
# ---------------------------------------------------------------------------

def detect_patterns(intervals: list[IntervalMarket]) -> list[tuple[str, IntervalMarket]]:
    """
    Walk sorted intervals and find Three White Soldiers or Three Black Crows patterns.
    Returns list of (pattern_type, next_interval_to_trade).
    pattern_type is "soldiers" or "crows".
    """
    if len(intervals) < 4:
        return []

    sorted_ivs = sorted(intervals, key=lambda iv: iv.sort_key)
    crow_threshold = 1.0 - SOLDIER_THRESHOLD  # e.g. 0.43
    opportunities = []

    for i in range(3, len(sorted_ivs)):
        w = sorted_ivs[i - 3:i]  # three-candle window
        target = sorted_ivs[i]   # next interval

        # Three White Soldiers: all three > SOLDIER_THRESHOLD
        if all(iv.p > SOLDIER_THRESHOLD for iv in w):
            # Next interval hasn't caught up -- still below 0.55
            if target.p < 0.55:
                opportunities.append(("soldiers", target))

        # Three Black Crows: all three < crow_threshold
        elif all(iv.p < crow_threshold for iv in w):
            # Next interval hasn't caught down -- still above 0.45
            if target.p > 0.45:
                opportunities.append(("crows", target))

    return opportunities


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based signal for individual market evaluation.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


def compute_pattern_signal(pattern: str, target: IntervalMarket) -> tuple[str | None, float, str]:
    """
    Continuation signal after Three White Soldiers or Three Black Crows.
    Soldiers (UP trend) + next interval < 0.55 -> buy YES (hasn't caught up).
    Crows (DOWN trend) + next interval > 0.45 -> buy NO (hasn't caught down).
    """
    m = target.market
    p = target.p
    q = m.question

    # Spread gate
    if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {m.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    if pattern == "soldiers":
        # Three soldiers (UP) detected, next interval is lagging below 0.55
        # The lower p is (further from 0.55), the more edge
        lag = 0.55 - p
        conviction = min(1.0, lag / 0.55) if lag > 0 else 0.05
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, (
            f"3-SOLDIERS -> YES {p:.0%} lag={lag:.0%} size=${size} -- {q[:60]}"
        )

    elif pattern == "crows":
        # Three crows (DOWN) detected, next interval is lagging above 0.45
        lag = p - 0.45
        conviction = min(1.0, lag / 0.55) if lag > 0 else 0.05
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, (
            f"3-CROWS -> NO {p:.0%} lag={lag:.0%} size=${size} -- {q[:60]}"
        )

    return None, 0, f"Unknown pattern {pattern} at {p:.1%}"


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    """Check flip-flop and slippage safeguards."""
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            reason = ctx["discipline"].get("flip_flop_reason", "recent reversal")
            return False, f"Flip-flop: {reason}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """
    Find active crypto 5-min interval markets via keyword search + bulk fetch fallback,
    deduplicated.
    """
    seen: set[str] = set()
    unique: list = []

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_crypto_5min_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_crypto_5min_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[candle-three-soldiers] mode={mode} max_pos=${MAX_POSITION} "
        f"soldier_threshold={SOLDIER_THRESHOLD}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-three-soldiers] {len(markets)} candidate markets")

    # Parse intervals and group by (coin, date)
    by_group: dict[str, list[IntervalMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_interval(q)
        if parsed is None:
            continue
        coin, date_str, start_time, end_time = parsed
        iv = IntervalMarket(m, coin, date_str, start_time, end_time)
        key = f"{coin}|{date_str}"
        by_group.setdefault(key, []).append(iv)

    safe_print(f"[candle-three-soldiers] {len(by_group)} coin-date groups with parsed intervals")
    for key, ivs in by_group.items():
        sorted_ivs = sorted(ivs, key=lambda iv: iv.sort_key)
        safe_print(
            f"  [{key}] {len(ivs)} intervals: "
            + ", ".join(f"{iv.start_time}={iv.p:.0%}" for iv in sorted_ivs[:10])
            + ("..." if len(ivs) > 10 else "")
        )

    # Detect patterns across all groups
    placed = 0
    for key, ivs in by_group.items():
        if placed >= MAX_POSITIONS:
            break

        patterns = detect_patterns(ivs)
        if not patterns:
            safe_print(f"  [{key}] no three-soldiers/crows patterns")
            continue

        for pattern, target in patterns:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_pattern_signal(pattern, target)
            if not side:
                safe_print(f"  [skip] {reasoning}")
                continue

            ok, why = context_ok(client, target.market.id)
            if not ok:
                safe_print(f"  [skip] {why}")
                continue

            try:
                r = client.trade(
                    market_id=target.market.id,
                    side=side,
                    amount=size,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {target.market.id}: {e}")

    safe_print(f"[candle-three-soldiers] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades crypto 5-min interval Three Soldiers/Crows patterns on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
