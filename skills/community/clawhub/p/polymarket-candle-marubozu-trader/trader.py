"""
polymarket-candle-marubozu-trader
Trades marubozu continuation signals on Polymarket 5-minute crypto interval markets.
A marubozu is an interval with extreme conviction (>65% or <35%) -- full body, no wick.
The NEXT interval should follow the same direction because extreme conviction reflects
new information. Targets BTC, ETH, SOL, and XRP "Up or Down" bundles.

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

TRADE_SOURCE = "sdk:polymarket-candle-marubozu-trader"
SKILL_SLUG   = "polymarket-candle-marubozu-trader"

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

# Marubozu-specific tunables
MARU_THRESHOLD = float(os.environ.get("SIMMER_MARU_THRESHOLD", "0.65"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MARU_THRESHOLD
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
        MARU_THRESHOLD = float(os.environ.get("SIMMER_MARU_THRESHOLD", str(MARU_THRESHOLD)))
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
# Grouping and marubozu detection
# ---------------------------------------------------------------------------

def detect_marubozu(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort each group by time.
    Find marubozu intervals (extreme conviction) and check whether the
    NEXT interval has continuation priced in yet.
    Return list of (next_market, maru_direction, maru_strength).
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

    maru_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        if n < 2:
            continue

        for i in range(n - 1):
            _, maru_mkt = intervals[i]
            _, next_mkt = intervals[i + 1]
            p_maru = maru_mkt.current_probability
            p_next = next_mkt.current_probability

            # Bullish marubozu: p > MARU_THRESHOLD
            if p_maru > MARU_THRESHOLD:
                strength = (p_maru - MARU_THRESHOLD) / (1 - MARU_THRESHOLD)
                # Continuation not yet priced: next interval below 0.55
                if p_next < 0.55:
                    maru_targets.append((next_mkt, "bullish", strength))

            # Bearish marubozu: p < (1 - MARU_THRESHOLD)
            elif p_maru < (1 - MARU_THRESHOLD):
                strength = ((1 - MARU_THRESHOLD) - p_maru) / (1 - MARU_THRESHOLD)
                # Continuation not yet priced: next interval above 0.45
                if p_next > 0.45:
                    maru_targets.append((next_mkt, "bearish", strength))

    return maru_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, maru_direction: str, maru_strength: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Marubozu continuation signals:
    - bullish marubozu: prior interval had extreme UP conviction -> buy YES on next
    - bearish marubozu: prior interval had extreme DOWN conviction -> buy NO on next
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

    if maru_direction == "bullish":
        # Bullish marubozu detected on prior interval. Buy YES on next if underpriced.
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"MARU-BULL str={maru_strength:.0%} YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Maru-bull but next p={p:.0%} > YES_THRESHOLD={YES_THRESHOLD:.0%} -- {q[:60]}"
        )

    if maru_direction == "bearish":
        # Bearish marubozu detected on prior interval. Buy NO on next if overpriced.
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"MARU-BEAR str={maru_strength:.0%} NO YES={p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Maru-bear but next p={p:.0%} < NO_THRESHOLD={NO_THRESHOLD:.0%} -- {q[:60]}"
        )

    return None, 0, f"Unknown marubozu direction: {maru_direction}"


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
        f"[candle-marubozu] mode={mode} max_pos=${MAX_POSITION} "
        f"maru_thresh={MARU_THRESHOLD} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-marubozu] {len(markets)} candidate interval markets")

    maru_targets = detect_marubozu(markets)
    safe_print(f"[candle-marubozu] {len(maru_targets)} marubozu continuation opportunities detected")

    placed = 0
    for m, maru_dir, maru_str in maru_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, maru_dir, maru_str)
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

    safe_print(f"[candle-marubozu] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades marubozu continuation signals on Polymarket 5-min crypto interval markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
