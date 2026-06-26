"""
polymarket-twitter-cadence-model-trader
Trades Twitter/X and Truth Social post-count bin markets using a Poisson
statistical model to predict the most likely bins.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from math import lgamma, exp, log
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-twitter-cadence-model-trader"
SKILL_SLUG   = "polymarket-twitter-cadence-model-trader"

KEYWORDS = [
    'Elon Musk', 'elon musk tweet', 'musk tweets',
    'Donald Trump', 'trump post', 'Truth Social',
    'Vitalik', 'vitalik post', 'CZ tweet',
    'tweets', 'posts',
]

# --- Person baselines (historical daily posting rates) -----------------------
PERSONS = {
    'elon musk':        {'key': 'elon',    'daily_rate': 65, 'weekend_factor': 0.70},
    'donald trump':     {'key': 'trump',   'daily_rate': 23, 'weekend_factor': 0.80},
    'vitalik buterin':  {'key': 'vitalik', 'daily_rate': 8,  'weekend_factor': 0.90},
    'cz':               {'key': 'cz',      'daily_rate': 12, 'weekend_factor': 0.85},
}

MONTH_MAP = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
}

# Risk parameters
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


# ── Market discovery ─────────────────────────────────────────────────────────

POST_FILTER = re.compile(
    r'(tweet|tweets|post|posts|truth social)', re.IGNORECASE
)
BIN_PATTERN = re.compile(r'(\d+)\s*[-\u2013]\s*(\d+)')
DATE_PATTERN = re.compile(
    r'(\w+)\s+(\d{1,2})\s+to\s+(\w+)\s+(\d{1,2}),?\s*(\d{4})',
    re.IGNORECASE,
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
    # Fallback: scan all account markets
    try:
        for m in client.get_markets(limit=200):
            q = getattr(m, 'question', '')
            if m.id not in seen and POST_FILTER.search(q) and BIN_PATTERN.search(q):
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] {e}")
    return unique


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_post_market(question: str):
    """Returns (person_info, bin_lower, bin_upper, period_days) or Nones."""
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
        m1n = MONTH_MAP.get(m1.lower(), 1)
        m2n = MONTH_MAP.get(m2.lower(), m1n)
        try:
            start = datetime(int(year), m1n, int(d1), tzinfo=timezone.utc)
            end   = datetime(int(year), m2n, int(d2), tzinfo=timezone.utc)
            period_days = max(1, (end - start).days + 1)
        except Exception:
            period_days = 3
    else:
        period_days = 3

    return person_info, bin_lower, bin_upper, period_days


# ── Poisson model ────────────────────────────────────────────────────────────

def poisson_log_pmf(k: int, lam: float) -> float:
    """Log P(X = k) for Poisson(lam)."""
    if lam <= 0:
        return -999.0
    return k * log(lam) - lam - lgamma(k + 1)


def poisson_bin_prob(lower: int, upper: int, lam: float) -> float:
    """P(lower <= X <= upper) using log-space summation for numerical stability."""
    log_probs = [poisson_log_pmf(k, lam) for k in range(lower, upper + 1)]
    if not log_probs:
        return 0.0
    max_lp = max(log_probs)
    return exp(max_lp) * sum(exp(lp - max_lp) for lp in log_probs)


# ── Signal ───────────────────────────────────────────────────────────────────

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Poisson cadence model: compute P(bin) from person's daily rate x period days,
    compare to market price, trade when model diverges from market.
    """
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

    lam = person['daily_rate'] * period_days
    model_p = poisson_bin_prob(bl, bu, lam)

    # Model bias: how much our model agrees with the threshold signal
    # >1 means model reinforces the signal, <1 means model contradicts it
    if p <= YES_THRESHOLD:
        # We'd buy YES — does our model agree this bin is underpriced?
        if model_p <= p * 0.5:
            return None, 0, f"Model disagrees: model={model_p:.1%} < mkt={p:.1%}, skip YES"
        bias = min(2.0, max(0.5, model_p / max(p, 0.01)))
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = model_p - p
        return "yes", size, (
            f"YES model={model_p:.0%} mkt={p:.0%} edge={edge:+.0%} "
            f"lam={lam:.0f} bias={bias:.1f}x ${size} -- {q[:55]}"
        )

    if p >= NO_THRESHOLD:
        # We'd sell NO — does our model agree this bin is overpriced?
        if model_p >= p * 1.5:
            return None, 0, f"Model disagrees: model={model_p:.1%} > mkt={p:.1%}, skip NO"
        bias = min(2.0, max(0.5, max(p, 0.01) / max(model_p, 0.01)))
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - model_p
        return "no", size, (
            f"NO model={model_p:.0%} mkt={p:.0%} edge={edge:+.0%} "
            f"lam={lam:.0f} bias={bias:.1f}x ${size} -- {q[:55]}"
        )

    return None, 0, f"Neutral {p:.1%} (model={model_p:.1%}, lam={lam:.0f})"


# ── Context check ────────────────────────────────────────────────────────────

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


# ── Main loop ────────────────────────────────────────────────────────────────

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[twitter-cadence-model] mode={mode} max_pos=${MAX_POSITION}")

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[twitter-cadence-model] {len(markets)} post-count bin markets found")

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

    safe_print(f"[twitter-cadence-model] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
