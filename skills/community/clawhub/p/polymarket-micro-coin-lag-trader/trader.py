"""
polymarket-micro-coin-lag-trader
Micro-trades altcoin 5-min Up/Down markets when BTC leads with a strong
directional signal and altcoins (ETH, SOL, XRP) haven't caught up yet.

Core edge: BTC moves first in crypto. When BTC's current 5-min interval shows
strong directional bias (>60% Up or >60% Down), altcoins in the same or next
interval typically follow 1-2 intervals later. This lag creates a window where
altcoin prices haven't yet absorbed BTC's move.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-micro-coin-lag-trader"
SKILL_SLUG   = "polymarket-micro-coin-lag-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'BTC Up or Down',
    'Ethereum Up or Down', 'ETH Up or Down',
    'Solana Up or Down', 'SOL Up or Down',
    'XRP Up or Down',
]

# MICRO risk parameters -- small size, wide thresholds, high position count.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "10"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "15"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "2"))

# Lead-lag specific: BTC must show strong directional bias to trigger.
LEAD_THRESHOLD = float(os.environ.get("SIMMER_LEAD_THRESHOLD", "0.60"))

_client: SimmerClient | None = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date, time_window from question text
# ---------------------------------------------------------------------------

_COIN_MAP = {
    "bitcoin": "BTC",
    "btc": "BTC",
    "ethereum": "ETH",
    "eth": "ETH",
    "solana": "SOL",
    "sol": "SOL",
    "xrp": "XRP",
}

_COIN_PATTERN = re.compile(
    r"(bitcoin|btc|ethereum|eth|solana|sol|xrp)\s+up\s+or\s+down",
    re.I,
)

# Date/time: "April 4, 10:45AM-10:50AM ET" or "March 28, 2026, 10:05 AM ET"
_DATETIME_PATTERN = re.compile(
    r"(\w+\s+\d{1,2})(?:,?\s+\d{4})?,?\s+(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)


def parse_coin(question: str) -> str | None:
    """Extract normalized coin ticker from question."""
    m = _COIN_PATTERN.search(question)
    if m:
        raw = m.group(1).lower()
        return _COIN_MAP.get(raw)
    return None


def parse_time_window(question: str) -> tuple[str, str] | None:
    """Extract (date_str, time_str) from question for grouping."""
    m = _DATETIME_PATTERN.search(question)
    if m:
        date_str = re.sub(r",", "", m.group(1)).strip().lower()
        time_str = m.group(2).strip().upper()
        date_str = re.sub(r"\s+", " ", date_str)
        return date_str, time_str
    return None


def normalize_time_to_5min(time_str: str) -> str:
    """Normalize a time like '10:07 AM' to the nearest 5-min bucket '10:05 AM'."""
    m = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)", time_str, re.I)
    if not m:
        return time_str
    hour = int(m.group(1))
    minute = int(m.group(2))
    ampm = m.group(3).upper()
    bucket = (minute // 5) * 5
    return f"{hour}:{bucket:02d} {ampm}"


def time_str_to_minutes(time_str: str) -> int | None:
    """Convert '10:05 AM' to minutes since midnight for ordering."""
    m = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)", time_str, re.I)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2))
    ampm = m.group(3).upper()
    if ampm == "PM" and hour != 12:
        hour += 12
    elif ampm == "AM" and hour == 12:
        hour = 0
    return hour * 60 + minute


def is_crypto_5min_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up/Down 5-min market."""
    if not _COIN_PATTERN.search(question):
        return False
    if not _DATETIME_PATTERN.search(question):
        return False
    return True


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class CoinMarket:
    """One market mapped to a coin in a time window."""
    __slots__ = ("market", "coin", "date_str", "time_bucket", "price")

    def __init__(self, market, coin: str, date_str: str, time_bucket: str, price: float):
        self.market = market
        self.coin = coin
        self.date_str = date_str
        self.time_bucket = time_bucket
        self.price = price


def group_by_window(markets: list) -> dict[str, list[CoinMarket]]:
    """Group markets into time windows keyed by 'date|time_bucket'."""
    windows: dict[str, list[CoinMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        coin = parse_coin(q)
        if coin is None:
            continue

        tw = parse_time_window(q)
        if tw is None:
            continue

        date_str, time_str = tw
        bucket = normalize_time_to_5min(time_str)
        key = f"{date_str}|{bucket}"
        cm = CoinMarket(m, coin, date_str, bucket, float(p))
        windows.setdefault(key, []).append(cm)

    return windows


# ---------------------------------------------------------------------------
# Lead-lag detection
# ---------------------------------------------------------------------------

def find_btc_lead_signals(windows: dict[str, list[CoinMarket]]) -> dict[str, str]:
    """
    Scan all windows for BTC lead signals.
    Returns {window_key: direction} where direction is 'up' or 'down'.
    BTC must show p > LEAD_THRESHOLD (strong Up) or p < (1-LEAD_THRESHOLD) (strong Down).
    """
    signals: dict[str, str] = {}
    for key, coins in windows.items():
        for cm in coins:
            if cm.coin != "BTC":
                continue
            if cm.price > LEAD_THRESHOLD:
                signals[key] = "up"
            elif cm.price < (1 - LEAD_THRESHOLD):
                signals[key] = "down"
    return signals


def get_adjacent_window_key(window_key: str) -> str | None:
    """
    Given a window key 'date|time_bucket', return the key for the next
    5-minute interval. E.g., 'march 28 2026|10:05 AM' -> 'march 28 2026|10:10 AM'.
    """
    parts = window_key.split("|", 1)
    if len(parts) != 2:
        return None
    date_str, time_bucket = parts
    minutes = time_str_to_minutes(time_bucket)
    if minutes is None:
        return None
    next_minutes = minutes + 5
    if next_minutes >= 24 * 60:
        return None  # rolls over to next day, skip
    hour = next_minutes // 60
    minute = next_minutes % 60
    ampm = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    next_bucket = f"{display_hour}:{minute:02d} {ampm}"
    return f"{date_str}|{next_bucket}"


def find_lag_opportunities(
    windows: dict[str, list[CoinMarket]],
    btc_signals: dict[str, str],
) -> list[tuple]:
    """
    For each BTC lead signal, find altcoins in the same or next time slot
    that haven't caught up.

    Returns list of (market, side, conviction, reasoning).
    """
    opportunities: list[tuple] = []

    for btc_key, direction in btc_signals.items():
        # Look at same slot + next slot for lagging altcoins
        check_keys = [btc_key]
        next_key = get_adjacent_window_key(btc_key)
        if next_key:
            check_keys.append(next_key)

        # Get BTC's price for reasoning
        btc_price = None
        for cm in windows.get(btc_key, []):
            if cm.coin == "BTC":
                btc_price = cm.price
                break

        for check_key in check_keys:
            if check_key not in windows:
                continue
            for cm in windows[check_key]:
                if cm.coin == "BTC":
                    continue  # skip BTC itself

                lag_type = "same-slot" if check_key == btc_key else "next-slot"
                min_lag_gap = 0.08  # altcoin must be 8%+ behind BTC

                if direction == "up" and btc_price is not None:
                    # BTC is strong Up -- altcoin lagging if it's below BTC
                    gap = btc_price - cm.price
                    if gap >= min_lag_gap:
                        # Altcoin hasn't caught up -- buy YES
                        conviction = min(1.0, gap / 0.30)  # 30% gap = full conviction
                        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
                        reason = (
                            f"LAG-YES {cm.coin} {cm.price:.0%} lag={lag_type} "
                            f"BTC-Up={btc_price:.0%} gap={gap:.0%} "
                            f"size=${size} -- {cm.market.question[:55]}"
                        )
                        sig = {"edge": round(gap, 4), "confidence": round(conviction, 4),
                               "signal_source": "coin_lag", "lag_type": lag_type,
                               "btc_p": round(btc_price, 4), "alt_p": round(cm.price, 4)}
                        opportunities.append((cm.market, "yes", size, reason, sig))

                elif direction == "down" and btc_price is not None:
                    # BTC is strong Down -- altcoin lagging if it's above BTC
                    gap = cm.price - btc_price
                    if gap >= min_lag_gap:
                        conviction = min(1.0, gap / 0.30)
                        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
                        reason = (
                            f"LAG-NO {cm.coin} Up={cm.price:.0%} lag={lag_type} "
                            f"BTC-Down={btc_price:.0%} gap={gap:.0%} "
                            f"size=${size} -- {cm.market.question[:55]}"
                        )
                        sig = {"edge": round(gap, 4), "confidence": round(conviction, 4),
                               "signal_source": "coin_lag", "lag_type": lag_type,
                               "btc_p": round(btc_price, 4), "alt_p": round(cm.price, 4)}
                        opportunities.append((cm.market, "no", size, reason, sig))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md:
    - YES: conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    - NO:  conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
    - size = max(MIN_TRADE, conviction * MAX_POSITION)
    """
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None, 0, "missing probability"

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

    if not opportunity:
        return None, 0, "No lag opportunity"

    side, size, reason = opportunity[1], opportunity[2], opportunity[3]
    return side, size, reason


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


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, LEAD_THRESHOLD
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
        LEAD_THRESHOLD = float(os.environ.get("SIMMER_LEAD_THRESHOLD", str(LEAD_THRESHOLD)))
    return _client


def find_markets(client: SimmerClient) -> list:
    """
    Find active crypto 5-min Up/Down markets via keyword search and bulk fetch,
    deduplicated.
    """
    seen: set[str] = set()
    unique: list = []

    # Fast markets (best source for 5-min intervals)
    try:
        for m in client.get_fast_markets():
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_crypto_5min_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[fast_markets] {e}")

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
        f"[micro-coin-lag] mode={mode} max_pos=${MAX_POSITION} "
        f"lead_thresh={LEAD_THRESHOLD:.0%} bands={YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[micro-coin-lag] {len(markets)} candidate markets")

    # Group by time window
    windows = group_by_window(markets)
    safe_print(f"[micro-coin-lag] {len(windows)} time windows")

    # Log each window's structure
    for window_key, coins in windows.items():
        safe_print(
            f"  [{window_key}] "
            + ", ".join(f"{cm.coin}={cm.price:.0%}" for cm in coins)
        )

    # Find BTC lead signals
    btc_signals = find_btc_lead_signals(windows)
    safe_print(f"[micro-coin-lag] {len(btc_signals)} BTC lead signals")
    for key, direction in btc_signals.items():
        safe_print(f"  [lead] {key} -> BTC {direction}")

    # Find lagging altcoin opportunities
    lag_opps = find_lag_opportunities(windows, btc_signals)
    safe_print(f"[micro-coin-lag] {len(lag_opps)} lag opportunities")

    # Deduplicate by market id (keep best opportunity per market)
    best_by_market: dict[str, tuple] = {}
    for opp in lag_opps:
        market, side, size, reason, _sig = opp
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = best_by_market.get(mid)
        if existing is None or size > existing[2]:
            best_by_market[mid] = opp

    # Execute trades, largest size first
    placed = 0
    for market_id, opp in sorted(best_by_market.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        sig = opp[4] if len(opp) > 4 else None
        side, size, reasoning = compute_signal(market, opp)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            trade_kwargs = dict(
                market_id=market_id, side=side, amount=size,
                source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            if sig:
                trade_kwargs["signal_data"] = sig
            r = client.trade(**trade_kwargs)
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[micro-coin-lag] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Micro-trades altcoin 5-min Up/Down markets when BTC leads "
            "with a strong directional signal and altcoins lag behind."
        )
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
