"""
polymarket-bundle-btc-5min-streak-trader
Trades BTC "Up or Down" 5-minute interval markets on Polymarket by detecting
streaks of consecutive same-direction intervals and trading mean-reversion
(contrarian) on the NEXT interval.

Core edge: Polymarket lists ~103 live BTC "Up or Down" 5-min interval markets
per day. After 3+ consecutive intervals where the market shows the same
directional bias (Up or Down), retail momentum chasers pile in on the streak
direction for the next interval. Mean-reversion is the statistically dominant
strategy for short-horizon BTC microstructure: 5-min returns are negatively
autocorrelated at lag 1-3 with coefficient ~-0.04 to -0.08, enough to exploit
when the market overweights the streak.

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

TRADE_SOURCE = "sdk:polymarket-bundle-btc-5min-streak-trader"
SKILL_SLUG   = "polymarket-bundle-btc-5min-streak-trader"

KEYWORDS = ['Bitcoin Up or Down', 'BTC Up or Down', 'Bitcoin Up', 'Bitcoin Down']

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Streak-specific tunables
STREAK_LENGTH  = int(os.environ.get(  "SIMMER_STREAK_LENGTH", "3"))

# Bias thresholds for classifying interval direction
UP_BIAS_THRESHOLD   = 0.55   # p > 0.55 = Up bias
DOWN_BIAS_THRESHOLD = 0.45   # p < 0.45 = Down bias

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, STREAK_LENGTH
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
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        STREAK_LENGTH  = int(os.environ.get(  "SIMMER_STREAK_LENGTH", str(STREAK_LENGTH)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract date + time window from 5-min interval questions
# ---------------------------------------------------------------------------

# Matches: "Bitcoin Up or Down - March 28, 11:00AM-11:05AM ET"
_INTERVAL_RE = re.compile(
    r"(?:Bitcoin|BTC)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"                     # "March 28"
    r"(\d{1,2}:\d{2}\s*[AP]M)"                   # "11:00AM" (start)
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",                   # "11:05AM" (end)
    re.I,
)

# Simpler fallback for slightly different formatting
_INTERVAL_RE_ALT = re.compile(
    r"(?:Bitcoin|BTC)\s+(?:Up|Down)"
    r".*?"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)


def parse_interval(question: str) -> tuple[str, str, str] | None:
    """
    Parse a BTC 5-min interval question.
    Returns (date_str, start_time, end_time) or None.
    e.g. ("March 28", "11:00AM", "11:05AM")
    """
    m = _INTERVAL_RE.search(question)
    if not m:
        m = _INTERVAL_RE_ALT.search(question)
    if m:
        return (m.group(1).strip(), m.group(2).strip(), m.group(3).strip())
    return None


def time_sort_key(start_time: str) -> int:
    """Convert a time like '11:00AM' to minutes since midnight for sorting."""
    try:
        t = start_time.upper().replace(" ", "")
        fmt = "%I:%M%p" if ":" in t else "%I%p"
        dt = datetime.strptime(t, fmt)
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def is_btc_5min_market(question: str) -> bool:
    """Return True if the question looks like a BTC 5-min Up or Down market."""
    q = question.lower()
    has_btc = any(w in q for w in ("bitcoin", "btc"))
    has_updown = "up or down" in q or ("up" in q and "down" in q)
    has_time = any(w in q for w in ("am", "pm", "am-", "pm-", ":00", ":05",
                                     ":10", ":15", ":20", ":25", ":30",
                                     ":35", ":40", ":45", ":50", ":55"))
    return has_btc and has_updown and has_time


# ---------------------------------------------------------------------------
# Streak detection and signal
# ---------------------------------------------------------------------------

class IntervalMarket:
    """Parsed 5-min interval market with sorting info."""
    __slots__ = ("market", "date_str", "start_time", "end_time", "sort_key", "p", "bias")

    def __init__(self, market, date_str, start_time, end_time):
        self.market = market
        self.date_str = date_str
        self.start_time = start_time
        self.end_time = end_time
        self.sort_key = time_sort_key(start_time)
        self.p = float(market.current_probability)
        if self.p > UP_BIAS_THRESHOLD:
            self.bias = "up"
        elif self.p < DOWN_BIAS_THRESHOLD:
            self.bias = "down"
        else:
            self.bias = "neutral"


def detect_streaks(intervals: list[IntervalMarket]) -> list[tuple[str, int, IntervalMarket]]:
    """
    Walk sorted intervals and find streaks of STREAK_LENGTH+ same-direction bias.
    Returns list of (streak_direction, streak_len, next_interval_to_trade).
    """
    if len(intervals) < STREAK_LENGTH + 1:
        return []

    sorted_ivs = sorted(intervals, key=lambda iv: iv.sort_key)
    opportunities = []

    for i in range(STREAK_LENGTH, len(sorted_ivs)):
        # Look back STREAK_LENGTH intervals
        window = sorted_ivs[i - STREAK_LENGTH:i]
        biases = [iv.bias for iv in window]

        # All same direction?
        if all(b == "up" for b in biases):
            opportunities.append(("up", STREAK_LENGTH, sorted_ivs[i]))
        elif all(b == "down" for b in biases):
            opportunities.append(("down", STREAK_LENGTH, sorted_ivs[i]))

    return opportunities


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    This is the standard conviction-based signal for individual market evaluation.
    The streak logic in run() determines WHICH markets to pass here and adjusts
    the effective threshold based on streak context.
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


def compute_streak_signal(streak_dir: str, streak_len: int,
                          target: IntervalMarket) -> tuple[str | None, float, str]:
    """
    Mean-reversion signal: after a streak of 'up' intervals, trade the next
    interval as 'down' (buy YES on Down bias = sell NO on Up bias).

    After 3+ consecutive Up-biased intervals (p > 0.55), the next interval
    is contrarian: sell NO (bet on Down / mean-revert).
    After 3+ consecutive Down-biased intervals (p < 0.45), the next interval
    is contrarian: buy YES (bet on Up / mean-revert).

    Conviction scales with streak length beyond minimum.
    """
    m = target.market
    p = target.p
    q = m.question

    # Spread gate
    if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {m.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Mean-reversion: trade OPPOSITE to streak direction
    extra_streak = streak_len - STREAK_LENGTH  # 0 at minimum, grows with longer streaks
    streak_bonus = min(0.3, extra_streak * 0.1)  # up to 0.3 extra conviction

    if streak_dir == "up":
        # Streak was Up -- mean-revert to Down -- sell NO on the next interval
        if p >= NO_THRESHOLD:
            conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) + streak_bonus)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"STREAK-REVERT {streak_len}xUp -> NO {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:55]}"
            )
        # Even if not past NO_THRESHOLD, a strong streak can push us to trade
        if p >= 0.50 and streak_len >= STREAK_LENGTH + 1:
            conviction = min(1.0, streak_bonus + 0.1)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "no", size, (
                f"STREAK-REVERT {streak_len}xUp -> NO {p:.0%} streak-forced "
                f"size=${size} -- {q[:55]}"
            )

    elif streak_dir == "down":
        # Streak was Down -- mean-revert to Up -- buy YES on the next interval
        if p <= YES_THRESHOLD:
            conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD + streak_bonus)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"STREAK-REVERT {streak_len}xDown -> YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:55]}"
            )
        if p <= 0.50 and streak_len >= STREAK_LENGTH + 1:
            conviction = min(1.0, streak_bonus + 0.1)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "yes", size, (
                f"STREAK-REVERT {streak_len}xDown -> YES {p:.0%} streak-forced "
                f"size=${size} -- {q[:55]}"
            )

    return None, 0, (
        f"No streak signal at {p:.1%} after {streak_len}x{streak_dir} "
        f"-- {q[:60]}"
    )


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
    Find active BTC 5-min interval markets via keyword search + bulk fetch fallback,
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
                    if is_btc_5min_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback -- scan recent/popular markets for BTC 5-min we may have missed
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_btc_5min_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[bundle-btc-5min-streak] mode={mode} max_pos=${MAX_POSITION} "
        f"streak_len={STREAK_LENGTH}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-btc-5min-streak] {len(markets)} candidate markets")

    # Parse intervals and group by date
    by_date: dict[str, list[IntervalMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_interval(q)
        if parsed is None:
            continue
        date_str, start_time, end_time = parsed
        iv = IntervalMarket(m, date_str, start_time, end_time)
        by_date.setdefault(date_str, []).append(iv)

    safe_print(f"[bundle-btc-5min-streak] {len(by_date)} dates with parsed intervals")
    for date_str, ivs in by_date.items():
        sorted_ivs = sorted(ivs, key=lambda iv: iv.sort_key)
        safe_print(
            f"  [{date_str}] {len(ivs)} intervals: "
            + ", ".join(f"{iv.start_time}={iv.p:.0%}({iv.bias})" for iv in sorted_ivs[:10])
            + ("..." if len(ivs) > 10 else "")
        )

    # Detect streaks across all dates
    placed = 0
    for date_str, ivs in by_date.items():
        if placed >= MAX_POSITIONS:
            break

        streaks = detect_streaks(ivs)
        if not streaks:
            safe_print(f"  [{date_str}] no streaks of {STREAK_LENGTH}+")
            continue

        for streak_dir, streak_len, target in streaks:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_streak_signal(streak_dir, streak_len, target)
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

    safe_print(f"[bundle-btc-5min-streak] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades BTC 5-min interval streak mean-reversion on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
