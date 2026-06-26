"""
polymarket-candle-engulfing-reversal-trader
Detects engulfing reversal patterns in crypto 5-minute interval markets on
Polymarket. A bullish engulfing occurs when an interval completely reverses
the prior interval with stronger conviction -- signaling a powerful reversal.
The NEXT interval should continue the reversal direction.

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

TRADE_SOURCE = "sdk:polymarket-candle-engulfing-reversal-trader"
SKILL_SLUG   = "polymarket-candle-engulfing-reversal-trader"

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

# Engulfing-specific tunables
ENGULF_THRESHOLD = float(os.environ.get("SIMMER_ENGULF_THRESHOLD", "0.06"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, ENGULF_THRESHOLD
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
        MAX_POSITION     = float(os.environ.get("SIMMER_MAX_POSITION",    str(MAX_POSITION)))
        MIN_VOLUME       = float(os.environ.get("SIMMER_MIN_VOLUME",      str(MIN_VOLUME)))
        MAX_SPREAD       = float(os.environ.get("SIMMER_MAX_SPREAD",      str(MAX_SPREAD)))
        MIN_DAYS         = int(os.environ.get(  "SIMMER_MIN_DAYS",        str(MIN_DAYS)))
        MAX_POSITIONS    = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   str(MAX_POSITIONS)))
        YES_THRESHOLD    = float(os.environ.get("SIMMER_YES_THRESHOLD",   str(YES_THRESHOLD)))
        NO_THRESHOLD     = float(os.environ.get("SIMMER_NO_THRESHOLD",    str(NO_THRESHOLD)))
        MIN_TRADE        = float(os.environ.get("SIMMER_MIN_TRADE",       str(MIN_TRADE)))
        ENGULF_THRESHOLD = float(os.environ.get("SIMMER_ENGULF_THRESHOLD", str(ENGULF_THRESHOLD)))
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
# Engulfing pattern detection
# ---------------------------------------------------------------------------

def classify_interval(p: float) -> str:
    """Classify an interval as UP, DOWN, or NEUTRAL."""
    if p > 0.55:
        return "UP"
    if p < 0.45:
        return "DOWN"
    return "NEUTRAL"


def detect_engulfing(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort each group by time.
    Find engulfing patterns: consecutive interval pairs where direction
    reverses AND the new interval has stronger conviction. Return list of
    (market, engulfing_type) for the NEXT interval after the engulfing pair.

    Bullish engulfing: prior p < 0.48, current p > 0.55,
                       AND (current - 0.5) > (0.5 - prior)
    Bearish engulfing: prior p > 0.52, current p < 0.45,
                       AND (0.5 - current) > (prior - 0.5)
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

    engulfing_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        if n < 3:
            continue

        for i in range(n - 2):
            _, _, prior_mkt = intervals[i]
            _, _, current_mkt = intervals[i + 1]
            _, _, next_mkt = intervals[i + 2]

            p_prior = prior_mkt.current_probability
            p_current = current_mkt.current_probability

            # Bullish engulfing: DOWN -> UP with stronger UP conviction
            if (p_prior < 0.48 and p_current > 0.55
                    and (p_current - 0.5) > (0.5 - p_prior)
                    and (p_current - 0.5) - (0.5 - p_prior) >= ENGULF_THRESHOLD):
                engulfing_targets.append((next_mkt, "bullish"))

            # Bearish engulfing: UP -> DOWN with stronger DOWN conviction
            elif (p_prior > 0.52 and p_current < 0.45
                    and (0.5 - p_current) > (p_prior - 0.5)
                    and (0.5 - p_current) - (p_prior - 0.5) >= ENGULF_THRESHOLD):
                engulfing_targets.append((next_mkt, "bearish"))

    return engulfing_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, engulfing_type: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Trades the post-engulfing continuation:
    - Bullish engulfing -> next interval should continue UP; if priced <= YES_THRESHOLD, buy YES
    - Bearish engulfing -> next interval should continue DOWN; if priced >= NO_THRESHOLD, buy NO
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

    if engulfing_type == "bullish":
        # Bullish engulfing detected. Next interval should continue UP.
        # If it hasn't moved up yet (still priced low), buy YES.
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"ENGULF-BULL YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Bullish engulfing but next interval already priced in ({p:.0%} > "
            f"YES_THRESHOLD={YES_THRESHOLD:.0%}) -- {q[:60]}"
        )

    if engulfing_type == "bearish":
        # Bearish engulfing detected. Next interval should continue DOWN.
        # If it hasn't moved down yet (still priced high), buy NO.
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"ENGULF-BEAR NO YES={p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Bearish engulfing but next interval already priced in ({p:.0%} < "
            f"NO_THRESHOLD={NO_THRESHOLD:.0%}) -- {q[:60]}"
        )

    return None, 0, f"Unknown engulfing type: {engulfing_type}"


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
        f"[engulfing] mode={mode} max_pos=${MAX_POSITION} "
        f"engulf_thresh={ENGULF_THRESHOLD} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[engulfing] {len(markets)} candidate interval markets")

    engulfing_targets = detect_engulfing(markets)
    safe_print(f"[engulfing] {len(engulfing_targets)} engulfing opportunities detected")

    placed = 0
    for m, eng_type in engulfing_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, eng_type)
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

    safe_print(f"[engulfing] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades engulfing reversal patterns in crypto 5-min interval markets on Polymarket."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
