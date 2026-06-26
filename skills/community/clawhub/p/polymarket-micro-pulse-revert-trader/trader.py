"""
polymarket-micro-pulse-revert-trader
Micro-trading skill that detects extreme probability spikes in 5-minute crypto
interval markets and trades mean-reversion on the NEXT interval.

Core edge: When a 5-min interval shows extreme bias (p > 70% or p < 30%),
retail conviction is overextended. The next interval mean-reverts with
higher probability than continuation. By trading tiny amounts ($2-$10)
across many such pulses, the skill accumulates consistent small profits.

SAFE BY DEFAULT: paper mode unless --live flag is passed.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-micro-pulse-revert-trader"
SKILL_SLUG = "polymarket-micro-pulse-revert-trader"

# Search for ALL crypto 5-min markets (BTC, ETH, SOL, XRP)
KEYWORDS = [
    'Bitcoin Up or Down', 'BTC Up or Down',
    'Ethereum Up or Down', 'ETH Up or Down',
    'Solana Up or Down', 'SOL Up or Down',
    'XRP Up or Down',
]

# MICRO risk parameters -- intentionally small
MAX_POSITION = float(os.environ.get("SIMMER_MAX_POSITION", "10"))
MIN_VOLUME = float(os.environ.get("SIMMER_MIN_VOLUME", "1000"))
MAX_SPREAD = float(os.environ.get("SIMMER_MAX_SPREAD", "0.12"))
MIN_DAYS = int(os.environ.get("SIMMER_MIN_DAYS", "0"))
MAX_POSITIONS = int(os.environ.get("SIMMER_MAX_POSITIONS", "15"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", "0.58"))
MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", "2"))

# Pulse-specific: how extreme must the PREVIOUS interval be to trigger
PULSE_HIGH = float(os.environ.get("SIMMER_PULSE_HIGH", "0.70"))  # p > 70% = extreme Up
PULSE_LOW = float(os.environ.get("SIMMER_PULSE_LOW", "0.30"))    # p < 30% = extreme Down

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, PULSE_HIGH, PULSE_LOW
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
        MAX_POSITION = float(os.environ.get("SIMMER_MAX_POSITION", str(MAX_POSITION)))
        MIN_VOLUME = float(os.environ.get("SIMMER_MIN_VOLUME", str(MIN_VOLUME)))
        MAX_SPREAD = float(os.environ.get("SIMMER_MAX_SPREAD", str(MAX_SPREAD)))
        MIN_DAYS = int(os.environ.get("SIMMER_MIN_DAYS", str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get("SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", str(NO_THRESHOLD)))
        MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", str(MIN_TRADE)))
        PULSE_HIGH = float(os.environ.get("SIMMER_PULSE_HIGH", str(PULSE_HIGH)))
        PULSE_LOW = float(os.environ.get("SIMMER_PULSE_LOW", str(PULSE_LOW)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract coin, date, time window from 5-min interval Qs
# ---------------------------------------------------------------------------

# Matches: "Bitcoin/BTC/Ethereum/ETH/Solana/SOL/XRP Up or Down - March 28, 11:00AM-11:05AM ET"
_INTERVAL_RE = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL|XRP)\s+(?:Up\s+or\s+Down)"
    r"\s*[-\u2013]\s*"
    r"(\w+\s+\d{1,2}),?\s*"                     # "March 28"
    r"(\d{1,2}:\d{2}\s*[AP]M)"                   # "11:00AM" (start)
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",                  # "11:05AM" (end)
    re.I,
)

# Simpler fallback for slightly different formatting
_INTERVAL_RE_ALT = re.compile(
    r"(Bitcoin|BTC|Ethereum|ETH|Solana|SOL|XRP)\s+(?:Up|Down)"
    r".*?"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*[AP]M)",
    re.I,
)

# Map various coin names to canonical symbol
_COIN_MAP = {
    "bitcoin": "BTC", "btc": "BTC",
    "ethereum": "ETH", "eth": "ETH",
    "solana": "SOL", "sol": "SOL",
    "xrp": "XRP",
}


def parse_interval(question: str) -> tuple[str, str, str, str] | None:
    """
    Parse a crypto 5-min interval question.
    Returns (coin, date_str, start_time, end_time) or None.
    e.g. ("BTC", "March 28", "11:00AM", "11:05AM")
    """
    m = _INTERVAL_RE.search(question)
    if not m:
        m = _INTERVAL_RE_ALT.search(question)
    if m:
        coin_raw = m.group(1).strip().lower()
        coin = _COIN_MAP.get(coin_raw, coin_raw.upper())
        return (coin, m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
    return None


def time_sort_key(start_time: str) -> int:
    """Convert a time like '11:00AM' to minutes since midnight for sorting."""
    try:
        t = start_time.upper().replace(" ", "")
        fmt = "%I:%M%p" if ":" in t else "%I%p"
        dt = datetime.strptime(t, fmt)
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def is_crypto_5min_market(question: str) -> bool:
    """Return True if the question looks like a crypto 5-min Up or Down market."""
    q = question.lower()
    has_coin = any(w in q for w in ("bitcoin", "btc", "ethereum", "eth",
                                     "solana", "sol", "xrp"))
    has_updown = "up or down" in q or ("up" in q and "down" in q)
    has_time = any(w in q for w in ("am", "pm", "am-", "pm-", ":00", ":05",
                                     ":10", ":15", ":20", ":25", ":30",
                                     ":35", ":40", ":45", ":50", ":55"))
    return has_coin and has_updown and has_time


# ---------------------------------------------------------------------------
# Interval container and pulse detection
# ---------------------------------------------------------------------------

class IntervalMarket:
    """Parsed 5-min interval market with sorting info."""
    __slots__ = ("market", "coin", "date_str", "start_time", "end_time",
                 "sort_key", "p")

    def __init__(self, market, coin, date_str, start_time, end_time):
        self.market = market
        self.coin = coin
        self.date_str = date_str
        self.start_time = start_time
        self.end_time = end_time
        self.sort_key = time_sort_key(start_time)
        self.p = float(market.current_probability)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) using conviction-based sizing.
    Called on the NEXT interval after a pulse is detected.
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


def compute_pulse_signal(pulse_dir: str, pulse_p: float,
                         target: IntervalMarket) -> tuple[str | None, float, str]:
    """
    Mean-reversion signal after a single extreme pulse.

    If previous interval was extreme Up (p > PULSE_HIGH): trade NEXT as NO
    (mean-revert down). Conviction scales with how extreme the pulse was.

    If previous interval was extreme Down (p < PULSE_LOW): trade NEXT as YES
    (mean-revert up). Conviction scales with how extreme the pulse was.
    """
    m = target.market
    p = target.p
    q = m.question

    # Spread gate
    if m.spread_cents is not None and m.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {m.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    if pulse_dir == "up":
        # Previous was extreme Up -- mean-revert: sell NO on the next interval
        # Pulse conviction: how far above PULSE_HIGH the pulse was
        pulse_conviction = (pulse_p - PULSE_HIGH) / (1 - PULSE_HIGH)
        # Also check standard threshold on target
        if p >= NO_THRESHOLD:
            target_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            combined = min(1.0, (pulse_conviction + target_conviction) / 2)
            size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"PULSE-REVERT Up@{pulse_p:.0%} -> NO {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:55]}"
            )
        # Even if target not past NO_THRESHOLD, strong pulse can force trade
        if p >= 0.48 and pulse_p >= PULSE_HIGH + 0.05:
            size = max(MIN_TRADE, round(pulse_conviction * MAX_POSITION * 0.5, 2))
            size = max(MIN_TRADE, size)
            return "no", size, (
                f"PULSE-REVERT Up@{pulse_p:.0%} -> NO {p:.0%} pulse-forced "
                f"size=${size} -- {q[:55]}"
            )

    elif pulse_dir == "down":
        # Previous was extreme Down -- mean-revert: buy YES on the next interval
        pulse_conviction = (PULSE_LOW - pulse_p) / PULSE_LOW
        if p <= YES_THRESHOLD:
            target_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            combined = min(1.0, (pulse_conviction + target_conviction) / 2)
            size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"PULSE-REVERT Down@{pulse_p:.0%} -> YES {p:.0%} edge={edge:.0%} "
                f"size=${size} -- {q[:55]}"
            )
        if p <= 0.52 and pulse_p <= PULSE_LOW - 0.05:
            size = max(MIN_TRADE, round(pulse_conviction * MAX_POSITION * 0.5, 2))
            size = max(MIN_TRADE, size)
            return "yes", size, (
                f"PULSE-REVERT Down@{pulse_p:.0%} -> YES {p:.0%} pulse-forced "
                f"size=${size} -- {q[:55]}"
            )

    return None, 0, (
        f"No pulse signal at {p:.1%} after {pulse_dir}@{pulse_p:.0%} "
        f"-- {q[:60]}"
    )


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
    Find active crypto 5-min interval markets via keyword search + bulk fetch
    fallback, deduplicated.
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

    # Bulk fallback -- scan recent/popular markets for crypto 5-min we may have missed
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
        f"[micro-pulse-revert] mode={mode} max_pos=${MAX_POSITION} "
        f"pulse_high={PULSE_HIGH:.0%} pulse_low={PULSE_LOW:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[micro-pulse-revert] {len(markets)} candidate markets")

    # Parse intervals and group by (coin, date)
    by_group: dict[tuple[str, str], list[IntervalMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_interval(q)
        if parsed is None:
            continue
        coin, date_str, start_time, end_time = parsed
        iv = IntervalMarket(m, coin, date_str, start_time, end_time)
        by_group.setdefault((coin, date_str), []).append(iv)

    safe_print(
        f"[micro-pulse-revert] {len(by_group)} (coin, date) groups with parsed intervals"
    )

    # Show summary per group
    for (coin, date_str), ivs in sorted(by_group.items()):
        sorted_ivs = sorted(ivs, key=lambda iv: iv.sort_key)
        safe_print(
            f"  [{coin} {date_str}] {len(ivs)} intervals: "
            + ", ".join(
                f"{iv.start_time}={iv.p:.0%}" for iv in sorted_ivs[:8]
            )
            + ("..." if len(ivs) > 8 else "")
        )

    # Detect pulses and trade the next interval
    placed = 0
    pulses_found = 0

    for (coin, date_str), ivs in sorted(by_group.items()):
        if placed >= MAX_POSITIONS:
            break

        sorted_ivs = sorted(ivs, key=lambda iv: iv.sort_key)

        if len(sorted_ivs) < 2:
            continue

        # Walk consecutive pairs: if interval[i] is extreme, trade interval[i+1]
        for i in range(len(sorted_ivs) - 1):
            if placed >= MAX_POSITIONS:
                break

            prev = sorted_ivs[i]
            target = sorted_ivs[i + 1]

            # Check if previous interval is an extreme pulse
            pulse_dir = None
            if prev.p > PULSE_HIGH:
                pulse_dir = "up"
            elif prev.p < PULSE_LOW:
                pulse_dir = "down"

            if pulse_dir is None:
                continue

            pulses_found += 1
            safe_print(
                f"  [PULSE] {coin} {date_str} {prev.start_time} "
                f"p={prev.p:.0%} ({pulse_dir}) -> target {target.start_time} "
                f"p={target.p:.0%}"
            )

            # Compute signal on the target interval
            side, size, reasoning = compute_pulse_signal(
                pulse_dir, prev.p, target
            )
            if not side:
                safe_print(f"  [skip] {reasoning}")
                continue

            ok, why = context_ok(client, target.market.id)
            if not ok:
                safe_print(f"  [skip] {why}")
                continue

            try:
                sig = {
                    "edge": round(abs(prev.p - target.p), 4),
                    "confidence": round(size / MAX_POSITION, 4),
                    "signal_source": "pulse_revert",
                    "pulse_dir": pulse_dir,
                    "pulse_p": round(prev.p, 4),
                    "target_p": round(target.p, 4),
                }
                r = client.trade(
                    market_id=target.market.id,
                    side=side,
                    amount=size,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                    signal_data=sig,
                )
                tag = "(sim)" if r.simulated else "(live)"
                status = "OK" if r.success else f"FAIL:{r.error}"
                safe_print(
                    f"  [trade] {side.upper()} ${size} {tag} {status} "
                    f"-- {reasoning[:100]}"
                )
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {target.market.id}: {e}")

    safe_print(
        f"[micro-pulse-revert] done. {pulses_found} pulses found, "
        f"{placed} orders placed."
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades crypto 5-min pulse mean-reversion on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
