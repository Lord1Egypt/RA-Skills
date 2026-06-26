"""
polymarket-candle-volume-spike-trader
Cross-coin volume spike detection for crypto "Up or Down" markets on Polymarket.
When multiple coins (BTC, ETH, SOL, XRP) ALL show strong same-direction candles
in the same time window, it confirms cross-market conviction. Coins that haven't
caught up in the next interval are traded.

Core edge: A single coin showing 58% directional bias in a 5-min window might be
noise. But when 3+ coins simultaneously show 58%+ bias in the same direction,
it reflects a genuine cross-market move driven by macro catalysts (rate decisions,
whale liquidations, exchange outages). The next interval for lagging coins should
continue that direction.

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

TRADE_SOURCE = "sdk:polymarket-candle-volume-spike-trader"
SKILL_SLUG   = "polymarket-candle-volume-spike-trader"

KEYWORDS = ['Bitcoin Up or Down', 'Ethereum Up or Down', 'Solana Up or Down', 'XRP Up or Down']

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION      = float(os.environ.get("SIMMER_MAX_POSITION",     "40"))
MIN_VOLUME        = float(os.environ.get("SIMMER_MIN_VOLUME",       "3000"))
MAX_SPREAD        = float(os.environ.get("SIMMER_MAX_SPREAD",       "0.08"))
MIN_DAYS          = int(os.environ.get(  "SIMMER_MIN_DAYS",         "0"))
MAX_POSITIONS     = int(os.environ.get(  "SIMMER_MAX_POSITIONS",    "8"))
YES_THRESHOLD     = float(os.environ.get("SIMMER_YES_THRESHOLD",    "0.38"))
NO_THRESHOLD      = float(os.environ.get("SIMMER_NO_THRESHOLD",     "0.62"))
MIN_TRADE         = float(os.environ.get("SIMMER_MIN_TRADE",        "5"))
# Skill-specific tunables
SPIKE_THRESHOLD   = float(os.environ.get("SIMMER_SPIKE_THRESHOLD",  "0.58"))
MIN_COINS         = int(os.environ.get(  "SIMMER_MIN_COINS",        "3"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, SPIKE_THRESHOLD, MIN_COINS
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
        MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    str(MAX_POSITION)))
        MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      str(MIN_VOLUME)))
        MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      str(MAX_SPREAD)))
        MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        str(MIN_DAYS)))
        MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   str(MAX_POSITIONS)))
        YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   str(YES_THRESHOLD)))
        NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    str(NO_THRESHOLD)))
        MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       str(MIN_TRADE)))
        SPIKE_THRESHOLD = float(os.environ.get("SIMMER_SPIKE_THRESHOLD", str(SPIKE_THRESHOLD)))
        MIN_COINS       = int(os.environ.get(  "SIMMER_MIN_COINS",       str(MIN_COINS)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date, time from crypto Up/Down questions
# ---------------------------------------------------------------------------

# Matches: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
_INTERVAL_RE = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL|XRP)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)


def normalize_coin(raw: str) -> str:
    """Normalize coin name to ticker."""
    r = raw.upper().strip()
    if r in ("BITCOIN", "BTC"):
        return "BTC"
    if r in ("ETHEREUM", "ETH"):
        return "ETH"
    if r in ("SOLANA", "SOL"):
        return "SOL"
    if r == "XRP":
        return "XRP"
    return r


def time_to_minutes(time_str: str) -> int:
    """Convert a time like '11:00AM' or '11AM' to minutes since midnight."""
    try:
        t = time_str.upper().replace(" ", "")
        fmt = "%I:%M%p" if ":" in t else "%I%p"
        dt = datetime.strptime(t, fmt)
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def parse_interval(question: str):
    """
    Parse a crypto 5-min interval question.
    Returns (coin, date_str, start_minutes) or None.
    """
    m = _INTERVAL_RE.search(question)
    if m:
        coin = normalize_coin(m.group(1))
        date_str = m.group(2).strip()
        start_minutes = time_to_minutes(m.group(3).strip())
        return coin, date_str, start_minutes
    return None


def is_crypto_updown_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up or Down market."""
    q = question.lower()
    has_coin = any(w in q for w in ("bitcoin", "btc", "ethereum", "eth",
                                     "solana", "sol", "xrp"))
    has_updown = "up or down" in q
    has_time = any(w in q for w in ("am", "pm"))
    return has_coin and has_updown and has_time


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based sizing per CLAUDE.md.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


def compute_spike_signal(market, spike_dir: str,
                         spike_coins: int) -> tuple[str | None, float, str]:
    """
    Volume spike signal: cross-market conviction confirmed, trade a lagging coin
    in the next interval to catch up.

    spike_dir: "up" or "down"
    spike_coins: how many coins confirmed the spike
    """
    m = market
    p = float(m.current_probability)
    q = m.question

    # Spread gate
    if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {m.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # This coin hasn't caught up yet -- it's in the neutral/weak zone
    # Conviction scales with how many coins confirmed the spike
    base_conviction = (spike_coins - MIN_COINS) / (4 - MIN_COINS) if 4 > MIN_COINS else 0.5
    conviction = min(1.0, 0.4 + base_conviction * 0.6)

    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    if spike_dir == "up":
        # Cross-market UP spike, this coin is lagging -> buy YES
        return "yes", size, (
            f"SPIKE {spike_coins} coins UP, lagging={p:.0%} "
            f"size=${size} -- {q[:55]}"
        )
    elif spike_dir == "down":
        # Cross-market DOWN spike, this coin is lagging -> buy NO
        return "no", size, (
            f"SPIKE {spike_coins} coins DOWN, lagging={p:.0%} "
            f"size=${size} -- {q[:55]}"
        )

    return None, 0, f"No spike signal -- {q[:60]}"


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
    Find active crypto Up/Down markets via keyword search + bulk fetch fallback,
    deduplicated.
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
                    if is_crypto_updown_market(q):
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
                if is_crypto_updown_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[candle-volume-spike] mode={mode} max_pos=${MAX_POSITION} "
        f"spike_threshold={SPIKE_THRESHOLD} min_coins={MIN_COINS}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-volume-spike] {len(markets)} candidate markets")

    # Parse all intervals and group by (date, time_window)
    # Key: (date_str, start_minutes) -> dict of coin -> market
    by_window: dict[tuple[str, int], dict[str, object]] = {}

    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_interval(q)
        if parsed is None:
            continue
        coin, date_str, start_min = parsed
        key = (date_str, start_min)
        by_window.setdefault(key, {})[coin] = m

    # Sort windows by time
    sorted_windows = sorted(by_window.keys(), key=lambda k: k[1])
    safe_print(f"[candle-volume-spike] {len(sorted_windows)} time windows across all dates")

    # Detect volume spikes: windows where MIN_COINS+ coins show strong same-direction
    spikes: list[tuple[str, int, str, int, dict[str, object]]] = []  # (date, time, dir, count, coins)

    for date_str, start_min in sorted_windows:
        coins_in_window = by_window[(date_str, start_min)]
        if len(coins_in_window) < MIN_COINS:
            continue

        up_coins = []
        down_coins = []
        for coin, m in coins_in_window.items():
            p = float(m.current_probability)
            if p > SPIKE_THRESHOLD:
                up_coins.append(coin)
            elif p < (1 - SPIKE_THRESHOLD):
                down_coins.append(coin)

        if len(up_coins) >= MIN_COINS:
            spikes.append((date_str, start_min, "up", len(up_coins), coins_in_window))
            safe_print(
                f"  [spike] {date_str} {start_min//60}:{start_min%60:02d} "
                f"UP confirmed by {len(up_coins)} coins: {up_coins}"
            )
        elif len(down_coins) >= MIN_COINS:
            spikes.append((date_str, start_min, "down", len(down_coins), coins_in_window))
            safe_print(
                f"  [spike] {date_str} {start_min//60}:{start_min%60:02d} "
                f"DOWN confirmed by {len(down_coins)} coins: {down_coins}"
            )

    safe_print(f"[candle-volume-spike] {len(spikes)} volume spikes detected")

    # For each spike, find the NEXT time window and trade lagging coins
    placed = 0
    for date_str, spike_time, spike_dir, spike_count, spike_coins in spikes:
        if placed >= MAX_POSITIONS:
            break

        # Find the next 5-min window (spike_time + 5 minutes)
        next_time = spike_time + 5
        next_key = (date_str, next_time)
        next_window = by_window.get(next_key, {})

        if not next_window:
            safe_print(
                f"  [{date_str} {spike_time//60}:{spike_time%60:02d}] "
                f"no next window at +5min"
            )
            continue

        # Find coins in the next window that haven't caught up
        for coin, m in next_window.items():
            if placed >= MAX_POSITIONS:
                break

            p = float(m.current_probability)

            # Check if this coin is lagging (not yet showing strong direction)
            if spike_dir == "up" and p < SPIKE_THRESHOLD:
                # Coin hasn't caught up to the UP spike
                safe_print(
                    f"  [{coin} {date_str} +5min] lagging at {p:.0%}, "
                    f"spike was UP({spike_count} coins)"
                )
            elif spike_dir == "down" and p > (1 - SPIKE_THRESHOLD):
                # Coin hasn't caught up to the DOWN spike
                safe_print(
                    f"  [{coin} {date_str} +5min] lagging at {p:.0%}, "
                    f"spike was DOWN({spike_count} coins)"
                )
            else:
                # Already caught up or wrong direction
                continue

            side, size, reasoning = compute_spike_signal(m, spike_dir, spike_count)
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
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[candle-volume-spike] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades cross-coin volume spikes on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
