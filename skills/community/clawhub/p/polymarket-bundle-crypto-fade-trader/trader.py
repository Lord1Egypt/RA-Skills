"""
polymarket-bundle-crypto-fade-trader
Fades strong directional crypto moves on Polymarket 5-minute interval markets.
After 3+ consecutive high-conviction same-direction intervals (>58%), the next
interval tends to mean-revert. Targets BTC, ETH, and SOL "Up or Down" bundles.

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

TRADE_SOURCE = "sdk:polymarket-bundle-crypto-fade-trader"
SKILL_SLUG   = "polymarket-bundle-crypto-fade-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'BTC Up or Down',
    'Ethereum Up or Down', 'Solana Up or Down',
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

# Fade-specific tunables
FADE_THRESHOLD = float(os.environ.get("SIMMER_FADE_THRESHOLD", "0.58"))
FADE_LENGTH    = int(os.environ.get(  "SIMMER_FADE_LENGTH",    "3"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, FADE_THRESHOLD, FADE_LENGTH
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
        FADE_THRESHOLD = float(os.environ.get("SIMMER_FADE_THRESHOLD", str(FADE_THRESHOLD)))
        FADE_LENGTH    = int(os.environ.get(  "SIMMER_FADE_LENGTH",    str(FADE_LENGTH)))
    return _client


# ---------------------------------------------------------------------------
# Parsing: "BTC Up or Down - Mar 28, 2026, 14:00-14:05 ET"
# ---------------------------------------------------------------------------
_INTERVAL_RE = re.compile(
    r"^(BTC|Bitcoin|ETH|Ethereum|SOL|Solana)\s+Up or Down\s*[-\u2013]\s*"
    r"(.+?),\s*(\d{1,2}:\d{2})\s*[-\u2013]\s*(\d{1,2}:\d{2})\s*ET$",
    re.IGNORECASE,
)

_COIN_NORM = {
    "btc": "BTC", "bitcoin": "BTC",
    "eth": "ETH", "ethereum": "ETH",
    "sol": "SOL", "solana": "SOL",
}


def parse_interval(question: str):
    """
    Return (coin, date_str, start_time, end_time) or None.
    coin is normalised to BTC/ETH/SOL.
    """
    m = _INTERVAL_RE.match(question.strip())
    if not m:
        return None
    coin_raw, date_str, start, end = m.groups()
    coin = _COIN_NORM.get(coin_raw.lower(), coin_raw.upper())
    return coin, date_str.strip(), start.strip(), end.strip()


def time_key(start_time: str) -> int:
    """Convert HH:MM to minutes since midnight for sorting."""
    parts = start_time.split(":")
    return int(parts[0]) * 60 + int(parts[1])


# ---------------------------------------------------------------------------
# Grouping and fade detection
# ---------------------------------------------------------------------------

def detect_fades(markets: list) -> list:
    """
    Group interval markets by (coin, date). Sort each group by time.
    Detect FADE_LENGTH+ consecutive strong same-direction intervals.
    Return list of (market, fade_direction, streak_length) for the NEXT
    interval after a detected strong move.
    """
    # Parse and group
    groups: dict[tuple[str, str], list] = {}
    for m in markets:
        parsed = parse_interval(getattr(m, "question", ""))
        if not parsed:
            continue
        coin, date_str, start, end = parsed
        key = (coin, date_str)
        groups.setdefault(key, []).append((time_key(start), start, end, m))

    # Sort each group by time
    for key in groups:
        groups[key].sort(key=lambda x: x[0])

    fade_targets = []

    for (coin, date_str), intervals in groups.items():
        n = len(intervals)
        if n < FADE_LENGTH + 1:
            continue

        for i in range(FADE_LENGTH, n):
            # Check if the preceding FADE_LENGTH intervals are all strong
            # in the same direction
            streak_up = 0
            streak_down = 0

            for j in range(i - FADE_LENGTH, i):
                _, _, _, mkt = intervals[j]
                p = mkt.current_probability
                if p >= FADE_THRESHOLD:
                    streak_up += 1
                elif p <= (1 - FADE_THRESHOLD):
                    streak_down += 1

            # Full streak of strong-up intervals
            if streak_up == FADE_LENGTH:
                _, _, _, next_mkt = intervals[i]
                fade_targets.append((next_mkt, "up", FADE_LENGTH))

            # Full streak of strong-down intervals
            elif streak_down == FADE_LENGTH:
                _, _, _, next_mkt = intervals[i]
                fade_targets.append((next_mkt, "down", FADE_LENGTH))

    return fade_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, fade_direction: str, streak_len: int) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Fades strong directional moves:
    - After strong-UP streak -> expect mean reversion DOWN -> buy NO if p >= NO_THRESHOLD
      (i.e. the next interval is still priced Up, so we fade it)
    - After strong-DOWN streak -> expect mean reversion UP -> buy YES if p <= YES_THRESHOLD
      (i.e. the next interval is still priced Down, so we fade it)
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

    if fade_direction == "up":
        # Strong-up streak detected. Fade: the next interval should mean-revert down.
        # If next interval is STILL priced high (Up-biased), sell NO.
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"FADE-UP streak={streak_len} NO YES={p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Fade-up but next interval already repriced ({p:.0%} < "
            f"NO_THRESHOLD={NO_THRESHOLD:.0%}) -- {q[:60]}"
        )

    if fade_direction == "down":
        # Strong-down streak detected. Fade: the next interval should mean-revert up.
        # If next interval is STILL priced low (Down-biased), buy YES.
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"FADE-DOWN streak={streak_len} YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:60]}"
            )
        return None, 0, (
            f"Fade-down but next interval already repriced ({p:.0%} > "
            f"YES_THRESHOLD={YES_THRESHOLD:.0%}) -- {q[:60]}"
        )

    return None, 0, f"Unknown fade direction: {fade_direction}"


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
        f"[crypto-fade] mode={mode} max_pos=${MAX_POSITION} "
        f"fade_thresh={FADE_THRESHOLD} fade_len={FADE_LENGTH} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[crypto-fade] {len(markets)} candidate interval markets")

    fade_targets = detect_fades(markets)
    safe_print(f"[crypto-fade] {len(fade_targets)} fade opportunities detected")

    placed = 0
    for m, fade_dir, streak_len in fade_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, fade_dir, streak_len)
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

    safe_print(f"[crypto-fade] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Fades strong directional crypto moves on Polymarket 5-min interval markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
