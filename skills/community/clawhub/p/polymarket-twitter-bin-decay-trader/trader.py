"""
polymarket-twitter-bin-decay-trader
Trades post-count bin markets by tracking elapsed time within the market period.
As time passes, bins that are mathematically unreachable (given estimated posts
so far) should be at 0% — trade against "dead" bins that still hold probability.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-twitter-bin-decay-trader"
SKILL_SLUG   = "polymarket-twitter-bin-decay-trader"

KEYWORDS = [
    'Elon Musk', 'elon musk tweet', 'musk tweets',
    'Donald Trump', 'trump post', 'Truth Social',
    'Vitalik', 'vitalik post', 'CZ tweet',
    'tweets', 'posts',
]

PERSONS = {
    'elon musk':        {'key': 'elon',    'daily_rate': 65, 'max_daily': 120},
    'donald trump':     {'key': 'trump',   'daily_rate': 23, 'max_daily': 50},
    'vitalik buterin':  {'key': 'vitalik', 'daily_rate': 8,  'max_daily': 20},
    'cz':               {'key': 'cz',      'daily_rate': 12, 'max_daily': 30},
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
    """Returns (person_info, bin_lower, bin_upper, period_days, start_date, end_date)."""
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


def compute_bin_viability(person: dict, bin_lower: int, bin_upper: int,
                          period_days: int, start: datetime | None) -> tuple[float, str]:
    """
    Estimate whether this bin is still reachable given elapsed time.

    Returns (viability 0.0-1.0, explanation).
    - 1.0 = fully viable (period hasn't started or just started)
    - 0.0 = mathematically dead (impossible to reach this bin)
    """
    if not start:
        return 0.5, "no dates, assume neutral"

    now = datetime.now(timezone.utc)
    end = start + __import__('datetime').timedelta(days=period_days)

    if now < start:
        return 0.5, "period not started"

    if now >= end:
        return 0.5, "period ended"

    elapsed = (now - start).total_seconds()
    total   = (end - start).total_seconds()
    fraction = elapsed / total  # 0.0 to 1.0

    if fraction < 0.15:
        return 0.5, f"only {fraction:.0%} elapsed, too early"

    # Estimate posts so far: fraction * daily_rate * period_days
    estimated_so_far = fraction * person['daily_rate'] * period_days

    # Remaining capacity
    remaining_fraction = 1.0 - fraction
    remaining_days = remaining_fraction * period_days

    # Max posts remaining: max_daily * remaining_days
    max_remaining = person['max_daily'] * remaining_days
    # Min posts remaining: roughly 0.3 * daily_rate * remaining (people don't stop entirely)
    min_remaining = 0.3 * person['daily_rate'] * remaining_days

    max_total = estimated_so_far + max_remaining
    min_total = estimated_so_far + min_remaining

    # Check bin viability
    if bin_lower > max_total:
        return 0.0, f"DEAD: need {bin_lower}, max possible={max_total:.0f} (est_so_far={estimated_so_far:.0f})"

    if bin_upper < min_total:
        return 0.0, f"DEAD: bin_upper={bin_upper} < min_possible={min_total:.0f} (est_so_far={estimated_so_far:.0f})"

    # Partially viable: compute how centered the bin is on the expected trajectory
    expected_total = estimated_so_far + person['daily_rate'] * remaining_days
    bin_mid = (bin_lower + bin_upper) / 2
    deviation = abs(bin_mid - expected_total) / max(expected_total, 1)

    # viability: 1.0 if bin is perfectly aligned, decays with deviation
    viability = max(0.1, 1.0 - deviation * 2)

    return viability, (
        f"est={estimated_so_far:.0f} expect_total={expected_total:.0f} "
        f"bin={bin_lower}-{bin_upper} viability={viability:.1%}"
    )


def compute_signal(market) -> tuple[str | None, float, str]:
    p = market.current_probability
    q = market.question

    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    person, bl, bu, period_days, start, end = parse_post_market(q)
    if not person:
        return None, 0, "Not a post-count bin market"

    viability, explanation = compute_bin_viability(person, bl, bu, period_days, start)

    # Dead bin still priced high → sell NO (fade it)
    if viability < 0.05 and p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * 1.5)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, (
            f"NO DEAD-BIN {p:.0%} viability={viability:.0%} ${size} "
            f"-- {person['key']} {bl}-{bu} | {explanation[:50]}"
        )

    # Highly viable bin priced low → buy YES
    if viability > 0.7 and p <= YES_THRESHOLD:
        bias = min(2.0, viability * 2)
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES VIABLE {p:.0%} edge={edge:.0%} viability={viability:.0%} "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    # Standard threshold signals with viability as bias
    bias = max(0.3, viability)

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} viability={viability:.0%} "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO {p:.0%} edge={edge:.0%} viability={viability:.0%} "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    return None, 0, f"Neutral {p:.1%} (viability={viability:.0%}) | {explanation[:60]}"


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
    safe_print(f"[twitter-bin-decay] mode={mode} max_pos=${MAX_POSITION}")

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[twitter-bin-decay] {len(markets)} post-count bin markets found")

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

    safe_print(f"[twitter-bin-decay] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
