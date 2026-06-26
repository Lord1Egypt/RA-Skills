"""
polymarket-twitter-sentiment-spike-trader
Detects crisis/news spikes across other Polymarket markets and adjusts expected
posting rates upward — public figures tweet more during geopolitical crises,
crypto volatility, and breaking news.  Trades higher bins when spike detected.

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

TRADE_SOURCE = "sdk:polymarket-twitter-sentiment-spike-trader"
SKILL_SLUG   = "polymarket-twitter-sentiment-spike-trader"

KEYWORDS = [
    'Elon Musk', 'elon musk tweet', 'musk tweets',
    'Donald Trump', 'trump post', 'Truth Social',
    'Vitalik', 'vitalik post', 'CZ tweet',
    'tweets', 'posts',
]

# Crisis-detection keywords: scan non-posting markets for extreme probabilities
CRISIS_KEYWORDS = [
    'war', 'strike', 'military', 'sanction', 'tariff', 'crash', 'ban',
    'bitcoin', 'BTC', 'ethereum', 'impeach', 'resign', 'indictment',
    'recession', 'default', 'shutdown', 'hack', 'breach', 'pandemic',
]

PERSONS = {
    'elon musk':        {'key': 'elon',    'daily_rate': 65, 'crisis_boost': 1.40},
    'donald trump':     {'key': 'trump',   'daily_rate': 23, 'crisis_boost': 1.50},
    'vitalik buterin':  {'key': 'vitalik', 'daily_rate': 8,  'crisis_boost': 1.25},
    'cz':               {'key': 'cz',      'daily_rate': 12, 'crisis_boost': 1.30},
}

# Which crisis topics boost which person's posting rate most
PERSON_CRISIS_AFFINITY = {
    'elon':    ['bitcoin', 'BTC', 'tariff', 'ban', 'hack', 'AI', 'tesla', 'spacex'],
    'trump':   ['war', 'strike', 'military', 'sanction', 'tariff', 'impeach', 'recession', 'shutdown'],
    'vitalik': ['ethereum', 'bitcoin', 'BTC', 'hack', 'breach', 'DeFi', 'regulation'],
    'cz':      ['bitcoin', 'BTC', 'binance', 'SEC', 'regulation', 'hack', 'crash'],
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


def find_all_markets(client: SimmerClient) -> tuple[list, list]:
    """Returns (post_markets, other_markets) for separate processing."""
    seen, post_markets, other_markets = set(), [], []
    # Keyword search for post markets
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                q = getattr(m, 'question', '')
                if m.id not in seen:
                    seen.add(m.id)
                    if POST_FILTER.search(q) and BIN_PATTERN.search(q):
                        post_markets.append(m)
                    else:
                        other_markets.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    # Scan all markets for crisis detection
    try:
        for m in client.get_markets(limit=200):
            q = getattr(m, 'question', '')
            if m.id not in seen:
                seen.add(m.id)
                if POST_FILTER.search(q) and BIN_PATTERN.search(q):
                    post_markets.append(m)
                else:
                    other_markets.append(m)
    except Exception as e:
        safe_print(f"[fallback] {e}")
    return post_markets, other_markets


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


def compute_crisis_level(other_markets: list) -> dict[str, float]:
    """
    Scan non-posting markets for crisis signals.  A market at >85% or <15%
    with crisis-related keywords indicates heightened activity.

    Returns {person_key: crisis_multiplier (1.0 = no crisis, up to person's crisis_boost)}.
    """
    # Count how many crisis-adjacent markets are at extreme probabilities
    person_crisis_scores: dict[str, float] = {info['key']: 0.0 for info in PERSONS.values()}

    for m in other_markets:
        q = getattr(m, 'question', '').lower()
        p = m.current_probability

        # Only care about extreme markets (strong signal either way)
        if 0.15 < p < 0.85:
            continue

        extremity = max(p, 1 - p)  # how extreme (0.85-1.0)

        for person_key, affinity_words in PERSON_CRISIS_AFFINITY.items():
            if any(word.lower() in q for word in affinity_words):
                person_crisis_scores[person_key] += extremity - 0.80

    # Convert scores to multipliers
    result = {}
    for name, info in PERSONS.items():
        key = info['key']
        score = person_crisis_scores.get(key, 0.0)
        if score > 0:
            # Scale: score of 0.5 gives full crisis_boost, linear below
            multiplier = 1.0 + (info['crisis_boost'] - 1.0) * min(1.0, score / 0.5)
            safe_print(f"  [crisis] {key}: score={score:.2f} -> {multiplier:.2f}x boost")
        else:
            multiplier = 1.0
        result[key] = multiplier

    return result


def compute_signal(market, crisis_multipliers: dict[str, float]) -> tuple[str | None, float, str]:
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

    crisis_mult = crisis_multipliers.get(person['key'], 1.0)
    expected = person['daily_rate'] * period_days
    crisis_expected = expected * crisis_mult
    bin_mid = (bl + bu) / 2

    # During crisis: higher bins become more likely, lower bins less likely
    # Boost conviction for bins aligned with crisis direction
    if crisis_mult > 1.05:
        if bin_mid > expected:
            # Higher bin + crisis = underpriced (more posts expected)
            bias = crisis_mult
        else:
            # Lower bin + crisis = overpriced (fewer posts than this bin unlikely)
            bias = max(0.4, 2.0 - crisis_mult)
    else:
        bias = 1.0  # no crisis signal

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} crisis={crisis_mult:.2f}x "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO {p:.0%} edge={edge:.0%} crisis={crisis_mult:.2f}x "
            f"bias={bias:.1f}x ${size} -- {person['key']} {bl}-{bu}"
        )

    return None, 0, f"Neutral {p:.1%} (crisis={crisis_mult:.2f}x, bias={bias:.1f}x)"


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
    safe_print(f"[twitter-sentiment-spike] mode={mode} max_pos=${MAX_POSITION}")

    client = get_client(live=live)
    post_markets, other_markets = find_all_markets(client)
    safe_print(f"[twitter-sentiment-spike] {len(post_markets)} post-count bins, {len(other_markets)} context markets")

    # Phase 1: compute crisis level from other markets
    crisis_multipliers = compute_crisis_level(other_markets)

    # Phase 2: trade post-count markets with crisis-adjusted conviction
    placed = 0
    for m in post_markets:
        if placed >= MAX_POSITIONS:
            break
        side, size, reasoning = compute_signal(m, crisis_multipliers)
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

    safe_print(f"[twitter-sentiment-spike] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
