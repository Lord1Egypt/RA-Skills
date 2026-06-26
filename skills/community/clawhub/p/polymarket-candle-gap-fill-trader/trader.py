"""
polymarket-candle-gap-fill-trader
Trades gap-fill reversions on Polymarket 5-minute crypto interval markets.
When consecutive intervals have contradictory strong signals (e.g., interval N
at 62% UP, interval N+1 at 38% DOWN), the outlier tends to revert toward 0.50.
Targets BTC, ETH, SOL, and XRP "Up or Down" bundles.

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

TRADE_SOURCE = "sdk:polymarket-candle-gap-fill-trader"
SKILL_SLUG   = "polymarket-candle-gap-fill-trader"

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

# Gap-fill-specific tunables
GAP_SIZE       = float(os.environ.get("SIMMER_GAP_SIZE",      "0.12"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, GAP_SIZE
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
        GAP_SIZE       = float(os.environ.get("SIMMER_GAP_SIZE",      str(GAP_SIZE)))
    return _client


# ---------------------------------------------------------------------------
# Parsing: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
# ---------------------------------------------------------------------------
_INTERVAL_RE = re.compile(
    r"^(BTC|Bitcoin|ETH|Ethereum|SOL|Solana|XRP)\s+Up or Down\s*[-\u2013]\s*"
    r"(.+?),\s*(\d{1,2}:\d{2}(?:AM|PM)?)\s*[-\u2013]\s*(\d{1,2}:\d{2}(?:AM|PM)?)\s*ET$",
    re.IGNORECASE,
)

_COIN_NORM = {
    "btc": "BTC", "bitcoin": "BTC",
    "eth": "ETH", "ethereum": "ETH",
    "sol": "SOL", "solana": "SOL",
    "xrp": "XRP",
}


def parse_interval(question: str):
    """
    Return (coin, date_str, start_time_minutes) or None.
    coin is normalised to BTC/ETH/SOL/XRP.
    """
    m = _INTERVAL_RE.match(question.strip())
    if not m:
        return None
    coin_raw, date_str, start, _end = m.groups()
    coin = _COIN_NORM.get(coin_raw.lower(), coin_raw.upper())
    return coin, date_str.strip(), time_key(start.strip())


def time_key(start_time: str) -> int:
    """Convert HH:MM or HH:MMAM/PM to minutes since midnight for sorting."""
    t = start_time.upper()
    is_pm = "PM" in t
    is_am = "AM" in t
    t = t.replace("AM", "").replace("PM", "")
    parts = t.split(":")
    h, m = int(parts[0]), int(parts[1])
    if is_pm and h != 12:
        h += 12
    elif is_am and h == 12:
        h = 0
    return h * 60 + m


# ---------------------------------------------------------------------------
# Grouping and gap detection
# ---------------------------------------------------------------------------

def detect_gaps(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort each group by time.
    Detect consecutive pairs where directions are opposite AND the gap
    exceeds GAP_SIZE. Return list of (market, gap_direction, gap_magnitude).
    gap_direction is the direction of the REVERSION we expect on the current interval.
    """
    # Parse and group
    groups: dict[tuple[str, str], list] = {}
    for mkt in markets:
        parsed = parse_interval(getattr(mkt, "question", ""))
        if not parsed:
            continue
        coin, date_str, start_min = parsed
        key = (coin, date_str)
        groups.setdefault(key, []).append((start_min, mkt))

    # Sort each group by time
    for key in groups:
        groups[key].sort(key=lambda x: x[0])

    gap_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        if n < 2:
            continue

        for i in range(1, n):
            _, prior_mkt = intervals[i - 1]
            _, curr_mkt = intervals[i]
            p_prior = prior_mkt.current_probability
            p_curr = curr_mkt.current_probability

            # Determine directions: UP if p>0.55, DOWN if p<0.45
            prior_up = p_prior > 0.55
            prior_down = p_prior < 0.45
            curr_up = p_curr > 0.55
            curr_down = p_curr < 0.45

            # Must be opposite strong signals
            if not ((prior_up and curr_down) or (prior_down and curr_up)):
                continue

            gap = abs(p_curr - p_prior)
            if gap < GAP_SIZE:
                continue

            if prior_up and curr_down:
                # Prior was UP, current is DOWN outlier -> gap fill upward
                gap_targets.append((curr_mkt, "fill_up", gap))
            elif prior_down and curr_up:
                # Prior was DOWN, current is UP outlier -> gap fill downward
                gap_targets.append((curr_mkt, "fill_down", gap))

    return gap_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, gap_direction: str, gap_magnitude: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Fills gaps between consecutive intervals:
    - fill_up: current is DOWN outlier after prior UP -> buy YES (revert upward)
    - fill_down: current is UP outlier after prior DOWN -> buy NO (revert downward)
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

    if gap_direction == "fill_up":
        # Current is DOWN outlier (p<0.45 after prior UP). Gap fill = buy YES.
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"GAP-FILL-UP gap={gap_magnitude:.0%} YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Gap-fill-up but p={p:.0%} > YES_THRESHOLD={YES_THRESHOLD:.0%} -- {q[:60]}"
        )

    if gap_direction == "fill_down":
        # Current is UP outlier (p>0.55 after prior DOWN). Gap fill = buy NO.
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"GAP-FILL-DOWN gap={gap_magnitude:.0%} NO YES={p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Gap-fill-down but p={p:.0%} < NO_THRESHOLD={NO_THRESHOLD:.0%} -- {q[:60]}"
        )

    return None, 0, f"Unknown gap direction: {gap_direction}"


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
        f"[candle-gap-fill] mode={mode} max_pos=${MAX_POSITION} "
        f"gap_size={GAP_SIZE} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-gap-fill] {len(markets)} candidate interval markets")

    gap_targets = detect_gaps(markets)
    safe_print(f"[candle-gap-fill] {len(gap_targets)} gap-fill opportunities detected")

    placed = 0
    for m, gap_dir, gap_mag in gap_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, gap_dir, gap_mag)
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

    safe_print(f"[candle-gap-fill] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades gap-fill reversions on Polymarket 5-min crypto interval markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
