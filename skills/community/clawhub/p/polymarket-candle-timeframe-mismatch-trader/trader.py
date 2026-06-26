"""
polymarket-candle-timeframe-mismatch-trader
Multi-timeframe analysis for crypto "Up or Down" markets on Polymarket.
Detects when 5-minute candle consensus diverges from the hourly/30-min market
and trades the convergence.

Core edge: Polymarket lists both hourly and 5-minute interval markets for BTC,
ETH, and SOL. When 4+ of 6 five-minute sub-intervals within an hour show a
clear directional consensus (UP or DOWN), but the hourly market is still
NEUTRAL (0.45-0.55), the 5-min intervals are leading indicators. The hourly
market will converge to match the sub-interval consensus.

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

TRADE_SOURCE = "sdk:polymarket-candle-timeframe-mismatch-trader"
SKILL_SLUG   = "polymarket-candle-timeframe-mismatch-trader"

KEYWORDS = ['Bitcoin Up or Down', 'Ethereum Up or Down', 'Solana Up or Down']

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Skill-specific tunables
MIN_CONSENSUS  = int(os.environ.get(  "SIMMER_MIN_CONSENSUS", "4"))

# Bias thresholds for classifying interval direction
UP_BIAS_THRESHOLD   = 0.55   # p > 0.55 = Up bias
DOWN_BIAS_THRESHOLD = 0.45   # p < 0.45 = Down bias

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_CONSENSUS
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
        MIN_CONSENSUS  = int(os.environ.get(  "SIMMER_MIN_CONSENSUS", str(MIN_CONSENSUS)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date, time from crypto Up/Down questions
# ---------------------------------------------------------------------------

COIN_PATTERNS = {
    "BTC": re.compile(r"(?:Bitcoin|BTC)", re.I),
    "ETH": re.compile(r"(?:Ethereum|ETH)", re.I),
    "SOL": re.compile(r"(?:Solana|SOL)", re.I),
}

# Matches 5-min interval: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
_INTERVAL_RE = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)

# Matches hourly/30-min market: "Bitcoin Up or Down - March 29, 11AM ET" (no sub-interval)
_HOURLY_RE = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}\s*[AP]M)\s*ET",
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


def parse_5min_interval(question: str):
    """
    Parse a 5-min interval question.
    Returns (coin, date_str, start_minutes) or None.
    """
    m = _INTERVAL_RE.search(question)
    if m:
        coin = normalize_coin(m.group(1))
        date_str = m.group(2).strip()
        start_minutes = time_to_minutes(m.group(3).strip())
        return coin, date_str, start_minutes
    return None


def parse_hourly_market(question: str):
    """
    Parse an hourly/30-min market question (no sub-interval range).
    Returns (coin, date_str, start_minutes) or None.
    """
    # Exclude questions that have a time range (those are 5-min intervals)
    if re.search(r"\d{1,2}:\d{2}\s*[AP]M\s*[-\u2013]\s*\d{1,2}:\d{2}\s*[AP]M", question, re.I):
        return None
    m = _HOURLY_RE.search(question)
    if m:
        coin = normalize_coin(m.group(1))
        date_str = m.group(2).strip()
        start_minutes = time_to_minutes(m.group(3).strip())
        return coin, date_str, start_minutes
    return None


def is_crypto_updown_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up or Down market."""
    q = question.lower()
    has_coin = any(w in q for w in ("bitcoin", "btc", "ethereum", "eth", "solana", "sol"))
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


def compute_mismatch_signal(hourly_market, consensus_dir: str,
                            consensus_count: int) -> tuple[str | None, float, str]:
    """
    Timeframe mismatch signal: hourly market is NEUTRAL but 5-min consensus
    is clearly directional. Trade the hourly to converge.

    consensus_dir: "up" or "down"
    consensus_count: how many of the sub-intervals agree
    """
    m = hourly_market
    p = float(m.current_probability)
    q = m.question

    # Spread gate
    if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {m.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Only trade if hourly is in the NEUTRAL zone (0.45-0.55)
    if p < DOWN_BIAS_THRESHOLD or p > UP_BIAS_THRESHOLD:
        return None, 0, f"Hourly not neutral ({p:.1%}), no mismatch"

    # Conviction scales with how many sub-intervals agree (4/6 = 0.33, 5/6 = 0.67, 6/6 = 1.0)
    base_conviction = (consensus_count - MIN_CONSENSUS) / (6 - MIN_CONSENSUS) if 6 > MIN_CONSENSUS else 0.5
    conviction = min(1.0, 0.33 + base_conviction * 0.67)

    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    if consensus_dir == "up":
        # 5-min says UP, hourly is neutral -> buy YES on hourly
        return "yes", size, (
            f"TF-MISMATCH {consensus_count}/6 5min=UP hourly={p:.0%} "
            f"size=${size} -- {q[:55]}"
        )
    elif consensus_dir == "down":
        # 5-min says DOWN, hourly is neutral -> buy NO on hourly
        return "no", size, (
            f"TF-MISMATCH {consensus_count}/6 5min=DOWN hourly={p:.0%} "
            f"size=${size} -- {q[:55]}"
        )

    return None, 0, f"No mismatch signal -- {q[:60]}"


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
        f"[candle-timeframe-mismatch] mode={mode} max_pos=${MAX_POSITION} "
        f"min_consensus={MIN_CONSENSUS}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[candle-timeframe-mismatch] {len(markets)} candidate markets")

    # Separate hourly markets from 5-min interval markets
    # Key: (coin, date_str, hour_start_minutes) -> list of 5-min markets
    fivemin_by_hour: dict[tuple[str, str, int], list] = {}
    hourly_markets: dict[tuple[str, str, int], object] = {}

    for m in markets:
        q = getattr(m, "question", "")

        # Try hourly first (must exclude 5-min ranges)
        hourly = parse_hourly_market(q)
        if hourly:
            coin, date_str, start_min = hourly
            key = (coin, date_str, start_min)
            hourly_markets[key] = m
            continue

        # Try 5-min interval
        interval = parse_5min_interval(q)
        if interval:
            coin, date_str, start_min = interval
            # Map to the containing hour (floor to nearest 60 min)
            hour_start = (start_min // 60) * 60
            key = (coin, date_str, hour_start)
            fivemin_by_hour.setdefault(key, []).append((start_min, m))

    safe_print(
        f"[candle-timeframe-mismatch] {len(hourly_markets)} hourly markets, "
        f"{len(fivemin_by_hour)} hour-groups of 5-min intervals"
    )

    # Find mismatches: hourly market is neutral, but 5-min sub-intervals have consensus
    placed = 0
    for key, hourly_m in hourly_markets.items():
        if placed >= MAX_POSITIONS:
            break

        coin, date_str, hour_start = key
        sub_intervals = fivemin_by_hour.get(key, [])

        if len(sub_intervals) < MIN_CONSENSUS:
            safe_print(
                f"  [{coin} {date_str} {hour_start//60}h] "
                f"only {len(sub_intervals)} sub-intervals, need {MIN_CONSENSUS}"
            )
            continue

        # Sort by time and classify direction
        sorted_subs = sorted(sub_intervals, key=lambda x: x[0])
        up_count = 0
        down_count = 0
        for _, sub_m in sorted_subs:
            p = float(sub_m.current_probability)
            if p > UP_BIAS_THRESHOLD:
                up_count += 1
            elif p < DOWN_BIAS_THRESHOLD:
                down_count += 1

        # Determine consensus
        consensus_dir = None
        consensus_count = 0
        if up_count >= MIN_CONSENSUS:
            consensus_dir = "up"
            consensus_count = up_count
        elif down_count >= MIN_CONSENSUS:
            consensus_dir = "down"
            consensus_count = down_count

        if not consensus_dir:
            safe_print(
                f"  [{coin} {date_str} {hour_start//60}h] "
                f"no consensus (up={up_count}, down={down_count}, need {MIN_CONSENSUS})"
            )
            continue

        # Check if hourly market is neutral (mismatch exists)
        hourly_p = float(hourly_m.current_probability)
        safe_print(
            f"  [{coin} {date_str} {hour_start//60}h] "
            f"5min consensus={consensus_dir}({consensus_count}/{len(sorted_subs)}) "
            f"hourly={hourly_p:.0%}"
        )

        side, size, reasoning = compute_mismatch_signal(
            hourly_m, consensus_dir, consensus_count
        )
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, hourly_m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=hourly_m.id,
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
            safe_print(f"  [error] {hourly_m.id}: {e}")

    safe_print(f"[candle-timeframe-mismatch] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades crypto timeframe mismatch on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
