"""
polymarket-candle-harami-trader
Detects harami (inside bar) candlestick patterns on Polymarket crypto 5-minute
interval markets. A harami forms when a small-range interval (near 50%) appears
after a large-range interval (far from 50%), signalling indecision after a strong
move -- often followed by reversal.

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

TRADE_SOURCE = "sdk:polymarket-candle-harami-trader"
SKILL_SLUG   = "polymarket-candle-harami-trader"

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

# Harami-specific tunables
HARAMI_LARGE   = float(os.environ.get("SIMMER_HARAMI_LARGE",  "0.10"))
HARAMI_SMALL   = float(os.environ.get("SIMMER_HARAMI_SMALL",  "0.02"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, HARAMI_LARGE, HARAMI_SMALL
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
        HARAMI_LARGE   = float(os.environ.get("SIMMER_HARAMI_LARGE",  str(HARAMI_LARGE)))
        HARAMI_SMALL   = float(os.environ.get("SIMMER_HARAMI_SMALL",  str(HARAMI_SMALL)))
    return _client


# ---------------------------------------------------------------------------
# Parsing: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
# ---------------------------------------------------------------------------
_INTERVAL_RE = re.compile(
    r"^(BTC|Bitcoin|ETH|Ethereum|SOL|Solana|XRP)\s+Up or Down\s*[-\u2013]\s*"
    r"(.+?),\s*(\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*[-\u2013]\s*(\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*ET$",
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
    Return (coin, date_str, start_minutes) or None.
    coin is normalised to BTC/ETH/SOL/XRP.
    """
    m = _INTERVAL_RE.match(question.strip())
    if not m:
        return None
    coin_raw, date_str, start, _end = m.groups()
    coin = _COIN_NORM.get(coin_raw.lower(), coin_raw.upper())
    return coin, date_str.strip(), _time_to_minutes(start.strip())


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM', '10:50AM', '1:05PM' to minutes since midnight."""
    t = t.upper().strip()
    am_pm = None
    if t.endswith("AM"):
        am_pm = "AM"
        t = t[:-2].strip()
    elif t.endswith("PM"):
        am_pm = "PM"
        t = t[:-2].strip()
    parts = t.split(":")
    h, m = int(parts[0]), int(parts[1])
    if am_pm == "PM" and h != 12:
        h += 12
    elif am_pm == "AM" and h == 12:
        h = 0
    return h * 60 + m


# ---------------------------------------------------------------------------
# Harami pattern detection
# ---------------------------------------------------------------------------

def _is_large(p: float) -> bool:
    """Large candle: far from 0.5 (distance > HARAMI_LARGE)."""
    return abs(p - 0.5) > HARAMI_LARGE


def _is_small(p: float) -> bool:
    """Small candle: near 0.5 (distance <= HARAMI_SMALL)."""
    return abs(p - 0.5) <= HARAMI_SMALL


def detect_harami(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort by time.
    Find consecutive pairs where interval N is large and N+1 is small (harami).
    Return list of (confirmation_market, harami_direction) for interval N+2.
    harami_direction is 'bullish' (large DOWN -> small -> expect reversal UP)
    or 'bearish' (large UP -> small -> expect reversal DOWN).
    """
    groups: dict[tuple[str, str], list] = {}
    for m in markets:
        parsed = parse_interval(getattr(m, "question", ""))
        if not parsed:
            continue
        coin, date_str, start_min = parsed
        key = (coin, date_str)
        groups.setdefault(key, []).append((start_min, m))

    for key in groups:
        groups[key].sort(key=lambda x: x[0])

    harami_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        if n < 3:
            continue

        for i in range(n - 2):
            _, m_large = intervals[i]
            _, m_small = intervals[i + 1]
            _, m_confirm = intervals[i + 2]

            p_large = m_large.current_probability
            p_small = m_small.current_probability

            if not _is_large(p_large) or not _is_small(p_small):
                continue

            # Determine harami direction
            if p_large < 0.40:
                # Large DOWN candle followed by small neutral -> bullish harami
                # Check if confirmation hasn't already moved UP (still tradeable)
                p_confirm = m_confirm.current_probability
                if p_confirm <= 0.55:
                    harami_targets.append((m_confirm, "bullish", p_large, p_small))
            elif p_large > 0.60:
                # Large UP candle followed by small neutral -> bearish harami
                p_confirm = m_confirm.current_probability
                if p_confirm >= 0.45:
                    harami_targets.append((m_confirm, "bearish", p_large, p_small))

    return harami_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, harami_dir: str, p_large: float, p_small: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md:
    - Bullish harami (large DOWN -> small) -> expect reversal UP -> buy YES if p <= YES_THRESHOLD
    - Bearish harami (large UP -> small) -> expect reversal DOWN -> sell NO if p >= NO_THRESHOLD
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

    if harami_dir == "bullish":
        # Large DOWN then small neutral -> expect reversal UP -> buy YES
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"HARAMI-BULL large={p_large:.0%} small={p_small:.0%} "
                f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Bullish harami but confirm already repriced ({p:.0%} > "
            f"YES_THRESHOLD={YES_THRESHOLD:.0%}) -- {q[:60]}"
        )

    if harami_dir == "bearish":
        # Large UP then small neutral -> expect reversal DOWN -> sell NO
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"HARAMI-BEAR large={p_large:.0%} small={p_small:.0%} "
                f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Bearish harami but confirm already repriced ({p:.0%} < "
            f"NO_THRESHOLD={NO_THRESHOLD:.0%}) -- {q[:60]}"
        )

    return None, 0, f"Unknown harami direction: {harami_dir}"


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
        f"[candle-harami] mode={mode} max_pos=${MAX_POSITION} "
        f"harami_large={HARAMI_LARGE} harami_small={HARAMI_SMALL} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-harami] {len(markets)} candidate interval markets")

    harami_targets = detect_harami(markets)
    safe_print(f"[candle-harami] {len(harami_targets)} harami patterns detected")

    placed = 0
    for m, harami_dir, p_large, p_small in harami_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, harami_dir, p_large, p_small)
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

    safe_print(f"[candle-harami] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Detects harami candlestick patterns on Polymarket crypto 5-min interval markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
