"""
polymarket-twitter-cross-contagion-trader
Trades post-count bin markets by detecting cross-person contagion: when one
public figure posts heavily, correlated figures tend to increase their rate too.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-twitter-cross-contagion-trader"
SKILL_SLUG   = "polymarket-twitter-cross-contagion-trader"

KEYWORDS = [
    'Elon Musk', 'elon musk tweet', 'musk tweets',
    'Donald Trump', 'trump post', 'Truth Social',
    'Vitalik', 'vitalik post', 'CZ tweet',
    'tweets', 'posts',
]

PERSONS = {
    'elon musk':        {'key': 'elon',    'daily_rate': 65},
    'donald trump':     {'key': 'trump',   'daily_rate': 23},
    'vitalik buterin':  {'key': 'vitalik', 'daily_rate': 8},
    'cz':               {'key': 'cz',      'daily_rate': 12},
}

# Cross-person contagion coefficients: when person A is hot, person B's rate
# increases by beta * A's excess.  Elon <-> Trump is strongest (political overlap).
CONTAGION = {
    ('elon', 'trump'):   0.15,
    ('trump', 'elon'):   0.12,
    ('elon', 'vitalik'): 0.08,
    ('vitalik', 'elon'): 0.06,
    ('elon', 'cz'):      0.05,
    ('cz', 'elon'):      0.04,
    ('trump', 'vitalik'):0.03,
    ('trump', 'cz'):     0.02,
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
        return None, None, None, None
    rm = BIN_PATTERN.search(question)
    if not rm:
        return None, None, None, None
    bin_lower, bin_upper = int(rm.group(1)), int(rm.group(2))
    dm = DATE_PATTERN.search(question)
    if dm:
        m1, d1, m2, d2, year = dm.groups()
        try:
            start = datetime(int(year), MONTH_MAP.get(m1.lower(), 1), int(d1), tzinfo=timezone.utc)
            end   = datetime(int(year), MONTH_MAP.get(m2.lower(), 1), int(d2), tzinfo=timezone.utc)
            period_days = max(1, (end - start).days + 1)
        except Exception:
            period_days = 3
    else:
        period_days = 3
    return person_info, bin_lower, bin_upper, period_days


def detect_contagion(markets: list) -> dict[str, float]:
    """
    Scan all markets, detect which persons are in a 'hot' state (market prices
    shifted toward higher bins), and compute contagion boost for other persons.

    Returns {person_key: contagion_boost_multiplier}.
    """
    # Group markets by person, compute weighted average bin midpoint
    person_signals: dict[str, list] = defaultdict(list)
    for m in markets:
        person, bl, bu, days = parse_post_market(getattr(m, 'question', ''))
        if not person:
            continue
        p = m.current_probability
        midpoint = (bl + bu) / 2
        expected = person['daily_rate'] * days
        # deviation: how far this bin's midpoint is from expected, weighted by market prob
        deviation = (midpoint - expected) / max(expected, 1) * p
        person_signals[person['key']].append(deviation)

    # Compute each person's aggregate "hotness" (positive = posting more than expected)
    person_heat: dict[str, float] = {}
    for key, devs in person_signals.items():
        if devs:
            person_heat[key] = sum(devs) / len(devs)
        else:
            person_heat[key] = 0.0

    # Apply contagion coefficients
    boosts: dict[str, float] = defaultdict(lambda: 1.0)
    for (source, target), beta in CONTAGION.items():
        heat = person_heat.get(source, 0.0)
        if heat > 0.05:  # source person is hotter than usual
            boost = 1.0 + beta * heat * 10  # scale to meaningful range
            boosts[target] = max(boosts[target], boost)
            safe_print(f"  [contagion] {source} heat={heat:.2f} -> {target} boost={boost:.2f}x")

    return dict(boosts)


def compute_signal(market, contagion_boosts: dict[str, float]) -> tuple[str | None, float, str]:
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

    person, bl, bu, period_days = parse_post_market(q)
    if not person:
        return None, 0, "Not a post-count bin market"

    boost = contagion_boosts.get(person['key'], 1.0)

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} contagion={boost:.2f}x ${size} "
            f"-- {person['key']} {bl}-{bu} -- {q[:50]}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO {p:.0%} edge={edge:.0%} contagion={boost:.2f}x ${size} "
            f"-- {person['key']} {bl}-{bu} -- {q[:50]}"
        )

    return None, 0, f"Neutral {p:.1%} (contagion={boost:.2f}x)"


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
    safe_print(f"[twitter-cross-contagion] mode={mode} max_pos=${MAX_POSITION}")

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[twitter-cross-contagion] {len(markets)} post-count bin markets found")

    # Phase 1: detect cross-person contagion from market price distribution
    contagion_boosts = detect_contagion(markets)

    # Phase 2: trade with contagion-adjusted conviction
    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break
        side, size, reasoning = compute_signal(m, contagion_boosts)
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

    safe_print(f"[twitter-cross-contagion] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
