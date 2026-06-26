"""
polymarket-bundle-crypto-hourly-trader
Trades crypto hourly Up/Down markets when sub-interval consensus disagrees
with the hourly price on Polymarket.

Core edge: BTC/ETH/SOL 5-min interval markets within the same hour must be
consistent with the hourly Up/Down market. If 4 of 6 five-minute intervals
show "Up" bias (>55%), the hourly market should also show Up bias. When it
doesn't, the hourly is mispriced.

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

TRADE_SOURCE = "sdk:polymarket-bundle-crypto-hourly-trader"
SKILL_SLUG   = "polymarket-bundle-crypto-hourly-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'Ethereum Up or Down', 'Solana Up or Down',
    'BTC Up', 'ETH Up', 'SOL Up',
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
# Minimum sub-intervals needed to form consensus
MIN_SUB_INTERVALS = int(os.environ.get("SIMMER_MIN_SUB_INTERVALS", "3"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_SUB_INTERVALS
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
        MAX_POSITION      = float(os.environ.get("SIMMER_MAX_POSITION",      str(MAX_POSITION)))
        MIN_VOLUME        = float(os.environ.get("SIMMER_MIN_VOLUME",        str(MIN_VOLUME)))
        MAX_SPREAD        = float(os.environ.get("SIMMER_MAX_SPREAD",        str(MAX_SPREAD)))
        MIN_DAYS          = int(os.environ.get(  "SIMMER_MIN_DAYS",          str(MIN_DAYS)))
        MAX_POSITIONS     = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     str(MAX_POSITIONS)))
        YES_THRESHOLD     = float(os.environ.get("SIMMER_YES_THRESHOLD",     str(YES_THRESHOLD)))
        NO_THRESHOLD      = float(os.environ.get("SIMMER_NO_THRESHOLD",      str(NO_THRESHOLD)))
        MIN_TRADE         = float(os.environ.get("SIMMER_MIN_TRADE",         str(MIN_TRADE)))
        MIN_SUB_INTERVALS = int(os.environ.get(  "SIMMER_MIN_SUB_INTERVALS", str(MIN_SUB_INTERVALS)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing — extract (coin, date_str, start_time, end_time, is_hourly)
# ---------------------------------------------------------------------------

# Coin aliases
_COIN_MAP = {
    "bitcoin": "btc", "btc": "btc",
    "ethereum": "eth", "eth": "eth",
    "solana": "sol", "sol": "sol",
}

# Matches "Bitcoin Up or Down - March 28, 11:00AM-11:05AM ET"
_SUB_INTERVAL = re.compile(
    r"(bitcoin|ethereum|solana|btc|eth|sol)\s+up\s+or\s+down\s*[-:]\s*"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}:\d{2}\s*[APap][Mm])\s*[-\u2013]\s*(\d{1,2}:\d{2}\s*[APap][Mm])",
    re.I,
)

# Matches "Bitcoin Up or Down - March 28, 11AM ET" (hourly, no sub-interval)
_HOURLY = re.compile(
    r"(bitcoin|ethereum|solana|btc|eth|sol)\s+up\s+or\s+down\s*[-:]\s*"
    r"(\w+\s+\d{1,2}),?\s*"
    r"(\d{1,2}\s*[APap][Mm])\s*(?:ET|EST|EDT)",
    re.I,
)

# Crypto filter — must mention a known coin and Up or Down
_CRYPTO_UP_DOWN = re.compile(
    r"(bitcoin|ethereum|solana|btc|eth|sol)\s+up\s+or\s+down",
    re.I,
)

# Non-crypto noise
_NON_CRYPTO = re.compile(
    r"election|president|congress|senate|weather|temperature|"
    r"counter[\s-]?strike|cs2|dota|overwatch|esport",
    re.I,
)


def normalize_coin(raw: str) -> str:
    """Map coin name/ticker to normalized 3-letter code."""
    return _COIN_MAP.get(raw.lower(), raw.lower())


def parse_hour_from_time(time_str: str) -> int:
    """Extract the hour (0-23) from a time string like '11:00AM' or '2PM'."""
    time_str = time_str.strip().upper()
    m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM)", time_str)
    if not m:
        return -1
    hour = int(m.group(1))
    ampm = m.group(3)
    if ampm == "PM" and hour != 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0
    return hour


def parse_market(question: str):
    """
    Parse a crypto Up/Down market question.
    Returns (coin, date_str, hour, is_hourly) or None.
    """
    if _NON_CRYPTO.search(question):
        return None
    if not _CRYPTO_UP_DOWN.search(question):
        return None

    # Try sub-interval first
    m = _SUB_INTERVAL.search(question)
    if m:
        coin = normalize_coin(m.group(1))
        date_str = m.group(2).strip()
        start_hour = parse_hour_from_time(m.group(3))
        return (coin, date_str, start_hour, False)

    # Try hourly
    m = _HOURLY.search(question)
    if m:
        coin = normalize_coin(m.group(1))
        date_str = m.group(2).strip()
        hour = parse_hour_from_time(m.group(3))
        return (coin, date_str, hour, True)

    return None


def is_crypto_hourly_market(question: str) -> bool:
    """Return True if the question looks like a crypto Up/Down market."""
    if _NON_CRYPTO.search(question):
        return False
    return bool(_CRYPTO_UP_DOWN.search(question))


# ---------------------------------------------------------------------------
# Bundle construction and consensus detection
# ---------------------------------------------------------------------------

class HourBundle:
    """Groups an hourly market with its sub-interval markets."""
    __slots__ = ("coin", "date_str", "hour", "hourly_market", "sub_markets")

    def __init__(self, coin: str, date_str: str, hour: int):
        self.coin = coin
        self.date_str = date_str
        self.hour = hour
        self.hourly_market = None
        self.sub_markets: list = []

    @property
    def key(self) -> str:
        return f"{self.coin}|{self.date_str}|{self.hour}"


def build_bundles(markets: list) -> dict[str, HourBundle]:
    """Group crypto Up/Down markets into hourly bundles."""
    bundles: dict[str, HourBundle] = {}

    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        parsed = parse_market(q)
        if not parsed:
            continue

        coin, date_str, hour, is_hourly = parsed
        if hour < 0:
            continue

        key = f"{coin}|{date_str}|{hour}"
        if key not in bundles:
            bundles[key] = HourBundle(coin, date_str, hour)

        bundle = bundles[key]
        if is_hourly:
            bundle.hourly_market = m
        else:
            bundle.sub_markets.append(m)

    return bundles


def find_opportunities(bundles: dict[str, HourBundle]) -> list[tuple]:
    """
    For each hourly bundle with enough sub-intervals, check if sub-interval
    consensus disagrees with the hourly market price.

    Returns list of (hourly_market, side, edge, reasoning).
    """
    opportunities: list[tuple] = []

    for key, bundle in bundles.items():
        if bundle.hourly_market is None:
            continue
        if len(bundle.sub_markets) < MIN_SUB_INTERVALS:
            continue

        hourly_p = float(getattr(bundle.hourly_market, "current_probability", 0))

        # Count sub-intervals with Up bias (p > 0.55) vs Down bias (p < 0.45)
        up_count = 0
        down_count = 0
        for sub in bundle.sub_markets:
            sub_p = float(getattr(sub, "current_probability", 0.5))
            if sub_p > 0.55:
                up_count += 1
            elif sub_p < 0.45:
                down_count += 1

        total_subs = len(bundle.sub_markets)

        # Majority sub-intervals are Up but hourly is low
        if up_count > total_subs / 2 and hourly_p < 0.45:
            edge = 0.45 - hourly_p
            reason = (
                f"Sub consensus UP ({up_count}/{total_subs} subs >55%) but "
                f"hourly={hourly_p:.1%} -- {bundle.coin.upper()} {bundle.date_str} {bundle.hour}h"
            )
            opportunities.append((bundle.hourly_market, "yes", edge, reason))

        # Majority sub-intervals are Down but hourly is high
        elif down_count > total_subs / 2 and hourly_p > 0.55:
            edge = hourly_p - 0.55
            reason = (
                f"Sub consensus DOWN ({down_count}/{total_subs} subs <45%) but "
                f"hourly={hourly_p:.1%} -- {bundle.coin.upper()} {bundle.date_str} {bundle.hour}h"
            )
            opportunities.append((bundle.hourly_market, "no", edge, reason))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
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
        return None, 0, "No bundle disagreement found"

    _, side, edge, reason = opportunity
    p = float(p)

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
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
    Find active crypto Up/Down markets via keyword search and bulk fetch,
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
                    if is_crypto_hourly_market(q):
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
                if is_crypto_hourly_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[bundle-crypto-hourly] mode={mode} max_pos=${MAX_POSITION} min_subs={MIN_SUB_INTERVALS}")

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-crypto-hourly] {len(markets)} candidate markets")

    # Build hourly bundles
    bundles = build_bundles(markets)
    safe_print(f"[bundle-crypto-hourly] {len(bundles)} bundles: "
               + ", ".join(
                   f"{k}(hourly={'Y' if b.hourly_market else 'N'}, {len(b.sub_markets)} subs)"
                   for k, b in bundles.items()
               ))

    # Log each bundle
    for key, bundle in bundles.items():
        hourly_p = "N/A"
        if bundle.hourly_market:
            hourly_p = f"{float(getattr(bundle.hourly_market, 'current_probability', 0)):.1%}"
        sub_prices = ", ".join(
            f"{float(getattr(s, 'current_probability', 0)):.1%}"
            for s in bundle.sub_markets
        )
        safe_print(f"  [{key}] hourly={hourly_p} subs=[{sub_prices}]")

    # Find opportunities
    opps = find_opportunities(bundles)
    safe_print(f"[bundle-crypto-hourly] {len(opps)} opportunities found")

    # Execute trades
    placed = 0
    for opp in sorted(opps, key=lambda x: -x[2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        market_id = getattr(market, "id", None)
        if not market_id:
            continue

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

    safe_print(f"[bundle-crypto-hourly] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades crypto hourly Up/Down markets when sub-interval consensus disagrees on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
