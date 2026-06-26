"""
polymarket-twitter-weekend-drift-trader
Exploits systematic weekday/weekend posting rate differences in post-count
bin markets.  Weekend posting rates are 20-30% lower for most public figures,
but markets are often set on Friday reflecting weekday cadence.

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

TRADE_SOURCE = "sdk:polymarket-twitter-weekend-drift-trader"
SKILL_SLUG   = "polymarket-twitter-weekend-drift-trader"

KEYWORDS = [
    'Elon Musk', 'elon musk tweet', 'musk tweets',
    'Donald Trump', 'trump post', 'Truth Social',
    'Vitalik', 'vitalik post', 'CZ tweet',
    'tweets', 'posts',
]

PERSONS = {
    'elon musk':        {'key': 'elon',    'weekday_rate': 72, 'weekend_rate': 50},
    'donald trump':     {'key': 'trump',   'weekday_rate': 25, 'weekend_rate': 20},
    'vitalik buterin':  {'key': 'vitalik', 'weekday_rate': 9,  'weekend_rate': 7},
    'cz':               {'key': 'cz',      'weekday_rate': 14, 'weekend_rate': 10},
}

MONTH_MAP = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
}

MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
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
    return _client


POST_FILTER = re.compile(r'(tweet|tweets|post|posts|truth social)', re.IGNORECASE)
BIN_PATTERN = re.compile(r'(\d+)\s*[-\u2013]\s*(\d+)')
DATE_PATTERN = re.compile(
    r'(\w+)\s+(\d{1,2})\s+to\s+(\w+)\s+(\d{1,2}),?\s*(\d{4})', re.IGNORECASE,
)


def find_markets(client: SimmerClient) -> list:
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                q = getattr(m, 'question', '')
                if m.id not in seen and POST_FILTER.search(q) and BIN_PATTERN.search(q):
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    try:
        for m in client.get_markets(limit=200):
            q = getattr(m, 'question', '')
            if m.id not in seen and POST_FILTER.search(q) and BIN_PATTERN.search(q):
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] {e}")
    return unique


def parse_post_market(question: str):
    q = question.lower()
    person_info = None
    for name, info in PERSONS.items():
        if name in q:
            person_info = info
            break
    if not person_info:
        return None, None, None, None, None, None
    rm = BIN_PATTERN.search(question)
    if not rm:
        return None, None, None, None, None, None
    bin_lower, bin_upper = int(rm.group(1)), int(rm.group(2))
    dm = DATE_PATTERN.search(question)
    start_date, end_date = None, None
    period_days = 3
    if dm:
        m1, d1, m2, d2, year = dm.groups()
        try:
            start_date = datetime(int(year), MONTH_MAP.get(m1.lower(), 1), int(d1), tzinfo=timezone.utc)
            end_date   = datetime(int(year), MONTH_MAP.get(m2.lower(), 1), int(d2), tzinfo=timezone.utc)
            period_days = max(1, (end_date - start_date).days + 1)
        except Exception:
            pass
    return person_info, bin_lower, bin_upper, period_days, start_date, end_date


def count_weekend_weekday(start: datetime, days: int) -> tuple[int, int]:
    """Count how many weekend days (Sat=5, Sun=6) vs weekdays in the period."""
    weekend, weekday = 0, 0
    for i in range(days):
        d = start + timedelta(days=i)
        if d.weekday() >= 5:
            weekend += 1
        else:
            weekday += 1
    return weekday, weekend


def weekend_adjusted_lambda(person: dict, start: datetime | None, period_days: int) -> tuple[float, float]:
    """
    Returns (naive_lambda, adjusted_lambda).
    naive = flat daily rate * days (what the market probably assumes).
    adjusted = weekday_rate * weekdays + weekend_rate * weekends.
    """
    avg_rate = (person['weekday_rate'] * 5 + person['weekend_rate'] * 2) / 7
    naive_lam = avg_rate * period_days

    if start:
        weekdays, weekends = count_weekend_weekday(start, period_days)
        adj_lam = person['weekday_rate'] * weekdays + person['weekend_rate'] * weekends
    else:
        adj_lam = naive_lam  # can't compute without dates

    return naive_lam, adj_lam


def compute_signal(market) -> tuple[str | None, float, str]:
    p = market.current_probability
    q = market.question

    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days_left = (resolves - datetime.now(timezone.utc)).days
            if days_left < MIN_DAYS:
                return None, 0, f"Only {days_left} days left"
        except Exception:
            pass

    person, bl, bu, period_days, start, end = parse_post_market(q)
    if not person:
        return None, 0, "Not a post-count bin market"

    naive_lam, adj_lam = weekend_adjusted_lambda(person, start, period_days)
    bin_mid = (bl + bu) / 2

    # The weekend drift: if adjusted lambda is lower than naive, lower bins are
    # underpriced and higher bins are overpriced (and vice versa)
    drift = adj_lam - naive_lam  # negative = fewer posts expected than market thinks
    drift_pct = drift / max(naive_lam, 1)

    # Determine if this bin benefits from the drift
    if abs(drift_pct) < 0.02:
        return None, 0, f"Minimal drift {drift_pct:+.1%} for {person['key']} ({naive_lam:.0f}->{adj_lam:.0f})"

    # Lower bins benefit from negative drift (fewer posts expected)
    # Higher bins benefit from positive drift (more posts expected)
    bin_aligns_with_drift = (
        (drift < 0 and bin_mid < naive_lam) or  # fewer posts, lower bin
        (drift > 0 and bin_mid > naive_lam)      # more posts, higher bin
    )

    bias = 1.0 + abs(drift_pct) * 3 if bin_aligns_with_drift else max(0.4, 1.0 - abs(drift_pct) * 3)

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} drift={drift_pct:+.0%} "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO {p:.0%} edge={edge:.0%} drift={drift_pct:+.0%} "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    return None, 0, f"Neutral {p:.1%} (drift={drift_pct:+.1%}, bias={bias:.1f}x)"


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            return False, f"Flip-flop: {ctx['discipline'].get('flip_flop_reason', 'reversal')}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[twitter-weekend-drift] mode={mode} max_pos=${MAX_POSITION}")

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[twitter-weekend-drift] {len(markets)} post-count bin markets found")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break
        side, size, reasoning = compute_signal(m)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue
        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue
        try:
            r = client.trade(
                market_id=m.id, side=side, amount=size,
                source=TRADE_SOURCE, skill_slug=SKILL_SLUG, reasoning=reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[twitter-weekend-drift] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
