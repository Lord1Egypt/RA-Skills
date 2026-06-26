"""
polymarket-micro-session-edge-trader
Trades session-transition mean-reversion in 5-minute crypto "Up or Down"
markets on Polymarket.

Core edge: Trading session transitions (US open 9:30 AM ET, Asian session
~8 PM ET, European open ~3 AM ET) create volatility bursts in crypto 5-min
markets. The first 2 intervals after a session open tend to be directional,
then the 3rd interval REVERTS. This skill detects the burst pattern and
fades the move on the next interval.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from datetime import datetime, timezone, timedelta

from simmer_sdk import SimmerClient

SKILL_SLUG   = "polymarket-micro-session-edge-trader"
TRADE_SOURCE = "sdk:polymarket-micro-session-edge-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'BTC Up or Down',
    'Ethereum Up or Down', 'ETH Up or Down',
    'Solana Up or Down', 'SOL Up or Down',
    'XRP Up or Down',
]

# --- MICRO risk parameters ---------------------------------------------------
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "10"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "2"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS",  "15"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))

# Session windows (minutes since midnight, ET)
# US_OPEN:   9:30-10:00 ET  (first 6 five-minute intervals after NYSE open)
# ASIA_OPEN: 20:00-20:30 ET (Asian session start)
# EU_OPEN:   3:00-3:30 ET   (European session start)
SESSION_WINDOWS = [
    ("US_OPEN",   9 * 60 + 30, 10 * 60),      # 570-600
    ("ASIA_OPEN", 20 * 60,     20 * 60 + 30),  # 1200-1230
    ("EU_OPEN",   3 * 60,      3 * 60 + 30),   # 180-210
]

# ET offset from UTC (assume EDT = UTC-4; good enough for trading heuristic)
ET_OFFSET = timedelta(hours=-4)

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except (BrokenPipeError, OSError):
        sys.stdout = open(os.devnull, "w")


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_TRADE, MAX_SPREAD, MIN_DAYS
    global MAX_POSITIONS, YES_THRESHOLD, NO_THRESHOLD, MIN_VOLUME

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
            pass
        MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS",  str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
    return _client


# ---------------------------------------------------------------------------
# Asset and time parsing
# ---------------------------------------------------------------------------

_ASSETS = {
    "bitcoin": "BTC", "btc": "BTC",
    "ethereum": "ETH", "eth": "ETH", "ether": "ETH",
    "solana": "SOL", "sol": "SOL",
    "xrp": "XRP", "ripple": "XRP",
}

# Matches: "April 4, 9:30AM-9:35AM ET" or "April 4, 9:30 AM - 9:35 AM ET"
_WINDOW_PATTERN = re.compile(
    r"((?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2})"                              # date: "April 4"
    r",?\s*"
    r"(\d{1,2}:\d{2}\s*(?:AM|PM))"             # start time: "9:30AM"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*(?:AM|PM))",            # end time: "9:35AM"
    re.I,
)

_UP_DOWN_PATTERN = re.compile(r"\b(up|down)\b.*\bor\b.*\b(up|down)\b", re.I)

# Month name -> number
_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


def parse_asset(question: str) -> str | None:
    q = question.lower()
    for keyword, asset in _ASSETS.items():
        if keyword in q:
            return asset
    return None


def _time_str_to_minutes(t: str) -> int:
    """Convert '9:30AM' or '8:00 PM' to minutes since midnight."""
    t = t.strip().upper().replace(" ", "")
    m = re.match(r"(\d{1,2}):(\d{2})(AM|PM)", t)
    if not m:
        return -1
    hour, minute, ampm = int(m.group(1)), int(m.group(2)), m.group(3)
    if ampm == "AM" and hour == 12:
        hour = 0
    elif ampm == "PM" and hour != 12:
        hour += 12
    return hour * 60 + minute


def parse_date_str(date_str: str) -> str | None:
    """'April 4' -> 'april 4' normalized key."""
    date_str = date_str.strip().lower()
    parts = date_str.split()
    if len(parts) == 2 and parts[0] in _MONTHS:
        return date_str
    return None


def parse_window_details(question: str):
    """
    Extract (date_key, start_minutes, end_minutes) from a question.
    Returns None if unparseable.
    """
    m = _WINDOW_PATTERN.search(question)
    if not m:
        return None
    date_key = parse_date_str(m.group(1))
    if not date_key:
        return None
    start_min = _time_str_to_minutes(m.group(2))
    end_min = _time_str_to_minutes(m.group(3))
    if start_min < 0 or end_min < 0:
        return None
    return (date_key, start_min, end_min)


def is_up_or_down(question: str) -> bool:
    return bool(_UP_DOWN_PATTERN.search(question))


def infer_direction(question: str, probability: float) -> str:
    """YES = Up in standard Polymarket 'Up or Down' markets."""
    return "up" if probability >= 0.50 else "down"


# ---------------------------------------------------------------------------
# Session detection and burst analysis
# ---------------------------------------------------------------------------

class IntervalInfo:
    """One parsed 5-min interval market."""
    __slots__ = ("market", "asset", "date_key", "start_min", "end_min",
                 "probability", "direction")

    def __init__(self, market, asset, date_key, start_min, end_min, probability, direction):
        self.market = market
        self.asset = asset
        self.date_key = date_key
        self.start_min = start_min
        self.end_min = end_min
        self.probability = probability
        self.direction = direction


def get_current_et_minutes() -> tuple[str, int]:
    """Return (date_key like 'april 4', minutes_since_midnight) in ET."""
    now_utc = datetime.now(timezone.utc)
    now_et = now_utc + ET_OFFSET
    month_name = now_et.strftime("%B").lower()
    date_key = f"{month_name} {now_et.day}"
    minutes = now_et.hour * 60 + now_et.minute
    return date_key, minutes


def find_session_window(start_min: int) -> str | None:
    """Return session name if this interval's start falls in a session window."""
    for name, win_start, win_end in SESSION_WINDOWS:
        if win_start <= start_min < win_end:
            return name
    return None


def build_intervals(markets: list) -> list[IntervalInfo]:
    """Parse all markets into IntervalInfo objects."""
    intervals = []
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue
        p = float(p)
        if not is_up_or_down(q):
            continue
        asset = parse_asset(q)
        details = parse_window_details(q)
        if not asset or not details:
            continue
        date_key, start_min, end_min = details
        direction = infer_direction(q, p)
        intervals.append(IntervalInfo(m, asset, date_key, start_min, end_min, p, direction))
    return intervals


def detect_burst_fades(intervals: list[IntervalInfo]) -> list[tuple]:
    """
    For each (coin, date), sort intervals by time, identify session windows,
    detect burst patterns (2 consecutive same-direction intervals in a window),
    and return fade targets.

    Returns list of (market, fade_side, burst_avg_p, reasoning).
    """
    # Group by (asset, date_key)
    groups: dict[tuple[str, str], list[IntervalInfo]] = {}
    for iv in intervals:
        key = (iv.asset, iv.date_key)
        groups.setdefault(key, []).append(iv)

    # Current ET time for filtering
    today_key, now_min = get_current_et_minutes()

    fades = []
    for (asset, date_key), ivs in groups.items():
        ivs.sort(key=lambda x: x.start_min)

        # For each session window, find intervals that fall in it
        for session_name, win_start, win_end in SESSION_WINDOWS:
            # Intervals whose start_min falls in [win_start, win_end)
            window_ivs = [iv for iv in ivs if win_start <= iv.start_min < win_end]
            if len(window_ivs) < 2:
                continue

            # Check first 2 intervals for directional burst
            iv1, iv2 = window_ivs[0], window_ivs[1]
            if iv1.direction != iv2.direction:
                # No confirmed burst -- directions disagree
                continue

            burst_dir = iv1.direction
            burst_avg_p = (iv1.probability + iv2.probability) / 2.0

            # Find the fade target: 3rd interval in window, or first after window
            fade_target = None
            if len(window_ivs) >= 3:
                fade_target = window_ivs[2]
            else:
                # Look for the next interval after the window ends
                for iv in ivs:
                    if iv.start_min >= win_end:
                        fade_target = iv
                        break

            if fade_target is None:
                continue

            # Only trade intervals whose end_time hasn't passed
            if date_key == today_key and fade_target.end_min <= now_min:
                continue

            # Determine fade side: opposite of burst
            if burst_dir == "up":
                fade_side = "no"  # fade up-burst -> bet Down
            else:
                fade_side = "yes"  # fade down-burst -> bet Up

            reasoning = (
                f"SESSION-FADE {session_name}: {asset} burst={burst_dir.upper()} "
                f"(avg {burst_avg_p:.0%}) -> fade to {fade_side.upper()} "
                f"@ {fade_target.probability:.0%} — "
                f"{fade_target.market.question[:70]}"
            )

            fades.append((fade_target.market, fade_side, burst_avg_p, reasoning))

    return fades


# ---------------------------------------------------------------------------
# Conviction-based sizing and signal
# ---------------------------------------------------------------------------

def compute_signal(market, fade_side: str, burst_avg_p: float, reasoning: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) using conviction-based sizing per CLAUDE.md.
    Conviction is boosted by burst strength (how extreme the burst was).
    """
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None, 0, "Missing probability"
    p = float(p)

    # Spread gate
    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    # Burst strength factor: how extreme the burst average was
    # burst_avg_p near 0 or 1 means very strong burst -> higher conviction boost
    # Fade trades use wider thresholds — the market near 50% IS the opportunity
    fade_yes_limit = 0.52  # buy YES up to 52% after down-burst
    fade_no_limit  = 0.48  # sell NO down to 48% after up-burst

    if fade_side == "no":
        # Fading an up-burst: sell NO (bet Down)
        if p < fade_no_limit:
            return None, 0, f"NO blocked at {p:.1%}; fade limit is {fade_no_limit:.0%}"
        conviction = min(1.0, (p - fade_no_limit) / 0.30)
        burst_strength = max(0, (burst_avg_p - 0.55) / 0.45)
        combined = min(1.0, conviction + 0.3 * burst_strength)
        size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
        return "no", size, reasoning

    if fade_side == "yes":
        # Fading a down-burst: buy YES (bet Up)
        if p > fade_yes_limit:
            return None, 0, f"YES blocked at {p:.1%}; fade limit is {fade_yes_limit:.0%}"
        conviction = min(1.0, (fade_yes_limit - p) / 0.30)
        burst_strength = max(0, (0.45 - burst_avg_p) / 0.45)
        combined = min(1.0, conviction + 0.3 * burst_strength)
        size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
        return "yes", size, reasoning

    return None, 0, "Unknown fade side"


# ---------------------------------------------------------------------------
# Context check, market discovery, execution
# ---------------------------------------------------------------------------

def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
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
    """Find active crypto 'Up or Down' markets, deduplicated."""
    seen, unique = set(), []

    # Fast markets first (best source for 5-min intervals)
    try:
        for m in client.get_fast_markets():
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "").lower()
                if "up" in q and "down" in q:
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[fast_markets] {e}")

    # Keyword search fallback
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    if "up" in q and "down" in q:
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[session-edge] mode={mode} max_pos=${MAX_POSITION} "
               f"thresholds={YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[session-edge] {len(markets)} candidate 'Up or Down' markets")

    # Parse all intervals
    intervals = build_intervals(markets)
    safe_print(f"[session-edge] {len(intervals)} parsed intervals")

    # Show current ET time
    today_key, now_min = get_current_et_minutes()
    now_h, now_m = divmod(now_min, 60)
    safe_print(f"[session-edge] current ET: {today_key} {now_h:02d}:{now_m:02d} "
               f"({now_min} min since midnight)")

    # Detect burst-fade opportunities
    fades = detect_burst_fades(intervals)
    safe_print(f"[session-edge] {len(fades)} burst-fade opportunities detected")

    for _, _, _, reason in fades:
        safe_print(f"  [fade] {reason}")

    # Execute trades
    placed = 0
    for market, fade_side, burst_avg_p, reasoning in fades:
        if placed >= MAX_POSITIONS:
            break

        market_id = getattr(market, "id", None)
        if not market_id:
            continue

        side, size, signal_reason = compute_signal(market, fade_side, burst_avg_p, reasoning)
        if not side:
            safe_print(f"  [skip] {signal_reason}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            p = getattr(market, "current_probability", 0)
            sig = {
                "edge": round(abs(p - burst_avg_p), 4),
                "confidence": round(size / MAX_POSITION, 4),
                "signal_source": "session_edge",
                "fade_side": fade_side,
                "burst_avg_p": round(burst_avg_p, 4),
                "target_p": round(p, 4),
            }
            r = client.trade(
                market_id=market_id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=signal_reason,
                signal_data=sig,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} — {signal_reason[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[session-edge] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades session-transition mean-reversion in 5-min crypto markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
