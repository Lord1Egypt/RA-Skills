"""
polymarket-candle-doji-breakout-trader
Detects doji patterns (48-52% probability) in crypto 5-minute interval markets
on Polymarket and trades the post-doji breakout in the direction of the pre-doji
trend. In candlestick analysis, a doji after a directional trend signals
indecision before a breakout -- the next interval tends to continue the prior
trend direction.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-candle-doji-breakout-trader"
SKILL_SLUG   = "polymarket-candle-doji-breakout-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'Ethereum Up or Down',
    'Solana Up or Down', 'XRP Up or Down',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Doji-specific tunables
DOJI_RANGE     = float(os.environ.get("SIMMER_DOJI_RANGE",    "0.02"))
TREND_LENGTH   = int(os.environ.get(  "SIMMER_TREND_LENGTH",  "3"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, DOJI_RANGE, TREND_LENGTH
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
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        DOJI_RANGE     = float(os.environ.get("SIMMER_DOJI_RANGE",    str(DOJI_RANGE)))
        TREND_LENGTH   = int(os.environ.get(  "SIMMER_TREND_LENGTH",  str(TREND_LENGTH)))
    return _client


# ---------------------------------------------------------------------------
# Parsing: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
#          "Ethereum Up or Down - March 28, 11AM ET"
# ---------------------------------------------------------------------------
_INTERVAL_RE = re.compile(
    r"^(BTC|Bitcoin|ETH|Ethereum|SOL|Solana|XRP)\s+Up or Down\s*[-\u2013]\s*"
    r"(.+?),?\s*"
    r"(\d{1,2}(?::\d{2})?\s*[AP]M)"
    r"(?:\s*[-\u2013]\s*(\d{1,2}(?::\d{2})?\s*[AP]M))?"
    r"\s*ET$",
    re.IGNORECASE,
)

_COIN_NORM = {
    "btc": "BTC", "bitcoin": "BTC",
    "eth": "ETH", "ethereum": "ETH",
    "sol": "SOL", "solana": "SOL",
    "xrp": "XRP",
}


def _parse_time_minutes(t: str) -> int:
    """Convert '10:50AM' or '11AM' to minutes since midnight."""
    t = t.upper().replace(" ", "")
    try:
        fmt = "%I:%M%p" if ":" in t else "%I%p"
        dt = datetime.strptime(t, fmt)
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def parse_interval(question: str):
    """
    Return (coin, date_str, start_minutes, end_minutes) or None.
    coin is normalised to BTC/ETH/SOL/XRP.
    """
    m = _INTERVAL_RE.match(question.strip())
    if not m:
        return None
    coin_raw, date_str, start_str, end_str = m.groups()
    coin = _COIN_NORM.get(coin_raw.lower(), coin_raw.upper())
    start_min = _parse_time_minutes(start_str)
    end_min = _parse_time_minutes(end_str) if end_str else start_min + 5
    return coin, date_str.strip(), start_min, end_min


# ---------------------------------------------------------------------------
# Doji detection and trend analysis
# ---------------------------------------------------------------------------

def classify_interval(p: float) -> str:
    """Classify an interval as UP, DOWN, or NEUTRAL."""
    if p > 0.55:
        return "UP"
    if p < 0.45:
        return "DOWN"
    return "NEUTRAL"


def is_doji(p: float) -> bool:
    """Check if an interval is in the doji zone (48-52% by default)."""
    return (0.50 - DOJI_RANGE) <= p <= (0.50 + DOJI_RANGE)


def detect_doji_breakouts(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort each group by time.
    Find doji intervals with a clear pre-doji trend. Return list of
    (market, trend_direction) for the NEXT interval after a doji.
    """
    groups: dict[tuple[str, str], list] = {}
    for m in markets:
        parsed = parse_interval(getattr(m, "question", ""))
        if not parsed:
            continue
        coin, date_str, start_min, end_min = parsed
        key = (coin, date_str)
        groups.setdefault(key, []).append((start_min, end_min, m))

    for key in groups:
        groups[key].sort(key=lambda x: x[0])

    breakout_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        # Need at least TREND_LENGTH intervals + doji + post-doji target
        if n < TREND_LENGTH + 2:
            continue

        for i in range(TREND_LENGTH, n - 1):
            _, _, doji_mkt = intervals[i]
            p_doji = doji_mkt.current_probability

            if not is_doji(p_doji):
                continue

            # Check pre-doji trend: TREND_LENGTH intervals before the doji
            directions = []
            for j in range(i - TREND_LENGTH, i):
                _, _, prev_mkt = intervals[j]
                directions.append(classify_interval(prev_mkt.current_probability))

            # All must be the same direction (UP or DOWN, not NEUTRAL)
            if len(set(directions)) == 1 and directions[0] != "NEUTRAL":
                trend_dir = directions[0]  # "UP" or "DOWN"
                _, _, post_doji_mkt = intervals[i + 1]
                breakout_targets.append((post_doji_mkt, trend_dir))

    return breakout_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, trend_direction: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Trades the post-doji breakout:
    - Pre-doji trend = UP and post-doji priced < 0.50 -> buy YES (breakout not priced in)
    - Pre-doji trend = DOWN and post-doji priced > 0.50 -> buy NO (breakout not priced in)
    """
    p = market.current_probability
    q = getattr(market, "question", "")

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    if trend_direction == "UP":
        # Pre-doji trend was UP. Expect breakout UP. If post-doji is still
        # priced below 0.50, the market hasn't priced in the breakout -> buy YES.
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"DOJI-BREAK-UP YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Doji-break-up but post-doji already priced in ({p:.0%} > "
            f"YES_THRESHOLD={YES_THRESHOLD:.0%}) -- {q[:60]}"
        )

    if trend_direction == "DOWN":
        # Pre-doji trend was DOWN. Expect breakout DOWN. If post-doji is still
        # priced above 0.50, the market hasn't priced in the breakout -> buy NO.
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"DOJI-BREAK-DN NO YES={p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Doji-break-down but post-doji already priced in ({p:.0%} < "
            f"NO_THRESHOLD={NO_THRESHOLD:.0%}) -- {q[:60]}"
        )

    return None, 0, f"Unknown trend direction: {trend_direction}"


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """Find active crypto interval markets via keyword search + get_markets fallback."""
    seen, unique = set(), []

    # 1. Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # 2. Fallback: scan broad market list for interval matches
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            q = getattr(m, "question", "")
            if mid and mid not in seen and _INTERVAL_RE.match(q.strip()):
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] get_markets: {e}")

    return unique


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


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[doji-breakout] mode={mode} max_pos=${MAX_POSITION} "
        f"doji_range={DOJI_RANGE} trend_len={TREND_LENGTH} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[doji-breakout] {len(markets)} candidate interval markets")

    breakout_targets = detect_doji_breakouts(markets)
    safe_print(f"[doji-breakout] {len(breakout_targets)} doji breakout opportunities detected")

    placed = 0
    for m, trend_dir in breakout_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, trend_dir)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=m.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[doji-breakout] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades post-doji breakouts in crypto 5-min interval markets on Polymarket."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
