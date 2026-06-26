"""
polymarket-bundle-cross-coin-5min-trader
Trades cross-coin divergence in 5-minute crypto Up/Down bundles on Polymarket.

Core edge: BTC, ETH, SOL, XRP Up/Down markets in the same 5-min window should
be highly correlated (crypto moves together). When one coin diverges from the
group consensus, it is likely to revert. If BTC=Up(60%), ETH=Up(55%),
SOL=Down(40%) in the same window, SOL is the outlier.

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

TRADE_SOURCE = "sdk:polymarket-bundle-cross-coin-5min-trader"
SKILL_SLUG   = "polymarket-bundle-cross-coin-5min-trader"

KEYWORDS = [
    'Bitcoin Up or Down',
    'Ethereum Up or Down',
    'Solana Up or Down',
    'XRP Up or Down',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Minimum deviation from group mean to consider a coin an outlier
MIN_DEVIATION  = float(os.environ.get("SIMMER_MIN_DEVIATION", "0.10"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_DEVIATION
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
        MIN_DEVIATION  = float(os.environ.get("SIMMER_MIN_DEVIATION", str(MIN_DEVIATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date, time_window from question text
# ---------------------------------------------------------------------------

# Matches "Bitcoin Up or Down - March 28, 2026, 10:05 AM ET"
# Also handles "Ethereum Up or Down - Mar 28, 2026, 2:30 PM ET"
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

# Date/time: "March 28, 2026, 10:05 AM ET" or "Mar 28, 2026, 2:30 PM ET"
_DATETIME_PATTERN = re.compile(
    r"(\w+\s+\d{1,2},?\s+\d{4}),?\s+(\d{1,2}:\d{2}\s*[AP]M)\s*ET",
    re.I,
)

# Simpler time-only pattern for normalizing windows
_TIME_PATTERN = re.compile(
    r"(\d{1,2}:\d{2}\s*[AP]M)\s*ET",
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
        # Normalize date to remove extra whitespace
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


def is_crypto_5min_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up/Down 5-min market."""
    if not _COIN_PATTERN.search(question):
        return False
    if not _DATETIME_PATTERN.search(question):
        return False
    return True


# ---------------------------------------------------------------------------
# Group markets by time window and find outliers
# ---------------------------------------------------------------------------

class CoinMarket:
    """One market mapped to a coin in a time window."""
    __slots__ = ("market", "coin", "date_str", "time_window", "price")

    def __init__(self, market, coin: str, date_str: str, time_window: str, price: float):
        self.market = market
        self.coin = coin
        self.date_str = date_str
        self.time_window = time_window
        self.price = price


def group_by_window(markets: list) -> dict[str, list[CoinMarket]]:
    """Group markets into time windows keyed by (date, time_bucket)."""
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


def find_outliers(windows: dict[str, list[CoinMarket]]) -> list[tuple]:
    """
    For each time window with 2+ coins, compute group mean and find outliers.
    An outlier deviates from the group mean by more than MIN_DEVIATION.

    Returns list of (market, side, deviation, reasoning).
    The trade direction pushes the outlier toward the group mean.
    """
    opportunities: list[tuple] = []

    for window_key, coins in windows.items():
        if len(coins) < 2:
            continue

        # Deduplicate by coin (keep first seen)
        seen_coins: dict[str, CoinMarket] = {}
        for cm in coins:
            if cm.coin not in seen_coins:
                seen_coins[cm.coin] = cm

        if len(seen_coins) < 2:
            continue

        coin_list = list(seen_coins.values())
        group_mean = sum(cm.price for cm in coin_list) / len(coin_list)

        for cm in coin_list:
            deviation = cm.price - group_mean

            if abs(deviation) < MIN_DEVIATION:
                continue

            # Coin is above group mean -> expect reversion down -> sell NO (push price down)
            # Coin is below group mean -> expect reversion up -> buy YES (push price up)
            if deviation > 0:
                # Price is too high relative to group -> trade NO
                side = "no"
                reason = (
                    f"NO {cm.coin} Up={cm.price:.0%} vs group_mean={group_mean:.0%} "
                    f"dev={deviation:+.0%} -- {cm.market.question[:55]}"
                )
            else:
                # Price is too low relative to group -> trade YES
                side = "yes"
                reason = (
                    f"YES {cm.coin} Up={cm.price:.0%} vs group_mean={group_mean:.0%} "
                    f"dev={deviation:+.0%} -- {cm.market.question[:55]}"
                )

            opportunities.append((cm.market, side, abs(deviation), reason))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the divergence from group mean.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
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
        return None, 0, "No divergence found"

    _, side, deviation, reason = opportunity
    p = float(p)

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (deviation - MIN_DEVIATION) / max(0.01, YES_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (deviation - MIN_DEVIATION) / max(0.01, 1 - NO_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, reason

    return None, 0, "Unknown side"


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
    Find active crypto 5-min Up/Down markets via keyword search and bulk fetch,
    deduplicated. Uses both find_markets(query=...) and get_markets(limit=200)
    as fallback since find_markets may miss some.
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

    # Bulk fallback -- scan recent/popular markets for crypto Up/Down we may have missed
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
        f"[cross-coin-5min] mode={mode} max_pos=${MAX_POSITION} "
        f"min_deviation={MIN_DEVIATION:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[cross-coin-5min] {len(markets)} candidate markets")

    # Group by time window
    windows = group_by_window(markets)
    safe_print(
        f"[cross-coin-5min] {len(windows)} time windows: "
        + ", ".join(f"{k}({len(v)} coins)" for k, v in windows.items())
    )

    # Log each window's structure
    for window_key, coins in windows.items():
        safe_print(
            f"  [{window_key}] "
            + ", ".join(f"{cm.coin}={cm.price:.0%}" for cm in coins)
        )

    # Find outlier opportunities across all windows
    all_opps: dict[str, tuple] = {}
    outliers = find_outliers(windows)
    for market, side, dev, reason in outliers:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or dev > existing[2]:
            all_opps[mid] = (market, side, dev, reason)

    safe_print(f"[cross-coin-5min] {len(all_opps)} outlier opportunities")

    # Execute trades on best outliers
    placed = 0
    for market_id, opp in sorted(all_opps.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        side, size, reasoning = compute_signal(market, opp)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=market_id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[cross-coin-5min] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades cross-coin divergence in 5-min crypto Up/Down bundles on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
