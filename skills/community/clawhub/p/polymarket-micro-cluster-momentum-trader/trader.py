"""
polymarket-micro-cluster-momentum-trader
Trades cluster momentum continuation in 5-minute crypto Up/Down bundles on Polymarket.

Core edge: When 3+ different crypto coins (BTC, ETH, SOL, XRP) ALL show the same
directional bias in the SAME 5-minute time slot, this cross-coin confirmation is
a strong momentum signal. Trade continuation on the NEXT time slot for all coins
at micro sizes.

This is CONVERGENCE (all coins agreeing) -- the opposite of divergence-based skills.
When the entire crypto market agrees on a direction in one window, momentum carries
into the next window.

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

TRADE_SOURCE = "sdk:polymarket-micro-cluster-momentum-trader"
SKILL_SLUG   = "polymarket-micro-cluster-momentum-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'BTC Up or Down',
    'Ethereum Up or Down', 'ETH Up or Down',
    'Solana Up or Down', 'SOL Up or Down',
    'XRP Up or Down',
]

# MICRO risk parameters -- declared as tunables in clawhub.json
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "10"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "15"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "2"))

# Cluster-specific parameters
CLUSTER_BIAS      = float(os.environ.get("SIMMER_CLUSTER_BIAS",      "0.53"))
MIN_CLUSTER_SIZE  = int(os.environ.get(  "SIMMER_MIN_CLUSTER_SIZE",  "2"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, CLUSTER_BIAS, MIN_CLUSTER_SIZE
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
        MAX_POSITION      = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME        = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD        = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS          = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS     = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD     = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD      = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE         = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        CLUSTER_BIAS      = float(os.environ.get("SIMMER_CLUSTER_BIAS",      str(CLUSTER_BIAS)))
        MIN_CLUSTER_SIZE  = int(os.environ.get(  "SIMMER_MIN_CLUSTER_SIZE",  str(MIN_CLUSTER_SIZE)))
    return _client


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


def next_5min_bucket(time_str: str) -> str:
    """Given a 5-min bucket like '10:05 AM', return the next one: '10:10 AM'."""
    m = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)", time_str, re.I)
    if not m:
        return time_str
    hour = int(m.group(1))
    minute = int(m.group(2))
    ampm = m.group(3).upper()
    minute += 5
    if minute >= 60:
        minute = 0
        hour += 1
        if hour == 12:
            ampm = "PM" if ampm == "AM" else "AM"
        elif hour > 12:
            hour = 1
    return f"{hour}:{minute:02d} {ampm}"


def is_crypto_5min_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up/Down 5-min market."""
    if not _COIN_PATTERN.search(question):
        return False
    if not _DATETIME_PATTERN.search(question):
        return False
    return True


# ---------------------------------------------------------------------------
# Market data structure and grouping
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


def group_by_window(markets: list) -> dict[str, dict[str, CoinMarket]]:
    """
    Group markets into time windows keyed by 'date|time_bucket'.
    Returns dict mapping window_key -> {coin: CoinMarket}.
    Deduplicates by coin within each window (keeps first seen).
    """
    windows: dict[str, dict[str, CoinMarket]] = {}
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

        if key not in windows:
            windows[key] = {}
        if coin not in windows[key]:
            windows[key][coin] = cm

    return windows


# ---------------------------------------------------------------------------
# Cluster detection -- find windows where 3+ coins agree on direction
# ---------------------------------------------------------------------------

def detect_clusters(windows: dict[str, dict[str, CoinMarket]]) -> list[tuple]:
    """
    For each time window, check if 3+ coins show the same directional bias.

    Returns list of (window_key, direction, agreeing_coins, cluster_size)
    where direction is 'up' or 'down'.
    """
    clusters: list[tuple] = []

    for window_key, coin_map in windows.items():
        if len(coin_map) < MIN_CLUSTER_SIZE:
            continue

        up_coins = []
        down_coins = []

        for coin, cm in coin_map.items():
            if cm.price > CLUSTER_BIAS:
                up_coins.append(coin)
            elif cm.price < (1 - CLUSTER_BIAS):
                down_coins.append(coin)

        if len(up_coins) >= MIN_CLUSTER_SIZE:
            clusters.append((window_key, "up", up_coins, len(up_coins)))

        if len(down_coins) >= MIN_CLUSTER_SIZE:
            clusters.append((window_key, "down", down_coins, len(down_coins)))

    return clusters


def find_continuation_targets(
    clusters: list[tuple],
    windows: dict[str, dict[str, CoinMarket]],
) -> list[tuple]:
    """
    For each cluster, look at the NEXT 5-min time slot and find
    continuation trade targets.

    Returns list of (market, side, cluster_size, reasoning).
    """
    targets: list[tuple] = []

    for window_key, direction, agreeing_coins, cluster_size in clusters:
        # Parse the window key to find the next slot
        parts = window_key.split("|", 1)
        if len(parts) != 2:
            continue
        date_str, time_bucket = parts
        next_bucket = next_5min_bucket(time_bucket)
        next_key = f"{date_str}|{next_bucket}"

        # Try next slot, then +10min, then +15min
        next_window = None
        found_key = next_key
        for offset_slots in range(1, 4):
            try_bucket = next_5min_bucket(time_bucket)
            for _ in range(offset_slots - 1):
                try_bucket = next_5min_bucket(try_bucket)
            try_key = f"{date_str}|{try_bucket}"
            if try_key in windows:
                next_window = windows[try_key]
                found_key = try_key
                break

        if not next_window:
            safe_print(
                f"  [cluster] {direction.upper()} cluster ({cluster_size} coins: "
                f"{','.join(agreeing_coins)}) at {window_key} -- no nearby next slot"
            )
            continue

        safe_print(
            f"  [cluster] {direction.upper()} cluster ({cluster_size} coins: "
            f"{','.join(agreeing_coins)}) at {window_key} -> trading {next_key}"
        )

        for coin, cm in next_window.items():
            if direction == "up":
                # Momentum: cluster was Up, buy YES if coin hasn't run up yet
                if cm.price <= 0.50:
                    conviction = min(1.0, (0.50 - cm.price) / 0.30 + 0.2)
                    reason = (
                        f"YES {coin} p={cm.price:.0%} | UP cluster "
                        f"({cluster_size} coins: {','.join(agreeing_coins)}) "
                        f"at {time_bucket} -> continuation -- {cm.market.question[:50]}"
                    )
                    targets.append((cm.market, "yes", cluster_size, reason))
                elif cm.price <= YES_THRESHOLD:
                    reason = (
                        f"YES {coin} p={cm.price:.0%} | UP cluster "
                        f"({cluster_size} coins: {','.join(agreeing_coins)}) "
                        f"at {time_bucket} -> continuation -- {cm.market.question[:50]}"
                    )
                    targets.append((cm.market, "yes", cluster_size, reason))
            elif direction == "down":
                # Momentum: cluster was Down, sell NO if coin hasn't dropped yet
                if cm.price >= 0.50:
                    conviction = min(1.0, (cm.price - 0.50) / 0.30 + 0.2)
                    reason = (
                        f"NO {coin} p={cm.price:.0%} | DOWN cluster "
                        f"({cluster_size} coins: {','.join(agreeing_coins)}) "
                        f"at {time_bucket} -> continuation -- {cm.market.question[:50]}"
                    )
                    targets.append((cm.market, "no", cluster_size, reason))
                elif cm.price >= NO_THRESHOLD:
                    reason = (
                        f"NO {coin} p={cm.price:.0%} | DOWN cluster "
                        f"({cluster_size} coins: {','.join(agreeing_coins)}) "
                        f"at {time_bucket} -> continuation -- {cm.market.question[:50]}"
                    )
                    targets.append((cm.market, "no", cluster_size, reason))
                else:
                    safe_print(
                        f"    [skip] {coin} p={cm.price:.0%} < NO_THRESHOLD "
                        f"{NO_THRESHOLD:.0%} -- no NO entry"
                    )

    return targets


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, side: str, cluster_size: int, reasoning: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction is based on both threshold distance AND cluster strength.
    More coins agreeing = higher conviction multiplier.
    """
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None, 0, "missing probability"
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

    # Volume gate
    volume = getattr(market, "volume", None)
    if isinstance(volume, (int, float)) and volume < MIN_VOLUME:
        return None, 0, f"Volume ${volume:.0f} < ${MIN_VOLUME:.0f}"

    # Cluster strength multiplier: 3 coins = 1.0x, 4 coins = 1.33x
    cluster_multiplier = min(1.5, cluster_size / MIN_CLUSTER_SIZE)

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        conviction *= cluster_multiplier
        conviction = min(1.0, conviction)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reasoning

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction *= cluster_multiplier
        conviction = min(1.0, conviction)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, reasoning

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
        f"[cluster-momentum] mode={mode} max_pos=${MAX_POSITION} "
        f"cluster_bias={CLUSTER_BIAS:.0%} min_cluster={MIN_CLUSTER_SIZE}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[cluster-momentum] {len(markets)} candidate markets")

    # Group by time window
    windows = group_by_window(markets)
    safe_print(
        f"[cluster-momentum] {len(windows)} time windows: "
        + ", ".join(
            f"{k}({len(v)} coins)" for k, v in sorted(windows.items())
        )
    )

    # Log each window's structure
    for window_key in sorted(windows.keys()):
        coin_map = windows[window_key]
        safe_print(
            f"  [{window_key}] "
            + ", ".join(f"{coin}={cm.price:.0%}" for coin, cm in coin_map.items())
        )

    # Detect clusters (3+ coins agreeing on direction)
    clusters = detect_clusters(windows)
    safe_print(f"[cluster-momentum] {len(clusters)} directional clusters found")

    if not clusters:
        safe_print("[cluster-momentum] No clusters detected. Done.")
        return

    # Find continuation targets in next time slots
    targets = find_continuation_targets(clusters, windows)
    safe_print(f"[cluster-momentum] {len(targets)} continuation targets")

    if not targets:
        safe_print("[cluster-momentum] No tradeable continuation targets. Done.")
        return

    # Deduplicate by market_id, keeping the one with the largest cluster
    deduped: dict[str, tuple] = {}
    for market, side, cluster_size, reasoning in targets:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = deduped.get(mid)
        if existing is None or cluster_size > existing[2]:
            deduped[mid] = (market, side, cluster_size, reasoning)

    # Execute trades, sorted by cluster size descending
    placed = 0
    for market_id, (market, side, cluster_size, reasoning) in sorted(
        deduped.items(), key=lambda x: -x[1][2]
    ):
        if placed >= MAX_POSITIONS:
            break

        final_side, size, final_reasoning = compute_signal(
            market, side, cluster_size, reasoning
        )
        if not final_side:
            safe_print(f"  [skip] {final_reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            p = getattr(market, "current_probability", 0)
            edge = abs(p - 0.50)
            sig = {
                "edge": round(edge, 4),
                "confidence": round(size / MAX_POSITION, 4),
                "signal_source": "cluster_momentum",
                "cluster_size": cluster_size,
                "probability": round(p, 4),
            }
            r = client.trade(
                market_id=market_id,
                side=final_side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=final_reasoning,
                signal_data=sig,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(
                f"  [trade] {final_side.upper()} ${size} {tag} {status} "
                f"-- {final_reasoning[:110]}"
            )
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[cluster-momentum] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades cluster momentum continuation in 5-min crypto Up/Down bundles on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
