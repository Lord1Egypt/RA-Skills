"""
polymarket-macro-sentiment-divergence-trader
Detects macro sentiment divergence across Polymarket prediction markets.
When "positive" categories (entertainment, sports winners, tech milestones, crypto UP)
and "negative" categories (geopolitical escalation, catastrophe, disease outbreaks,
crypto DOWN) are BOTH priced high simultaneously, that is logically inconsistent.
The world cannot be both great and terrible at the same time. Trades the stale side
of the divergence.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-sentiment-divergence-trader"
SKILL_SLUG   = "polymarket-macro-sentiment-divergence-trader"

# ---------------------------------------------------------------------------
# Sentiment classification keywords
# ---------------------------------------------------------------------------
POSITIVE_KEYWORDS = [
    # Sports favorites winning
    'win', 'champion', 'victory', 'gold medal', 'world series', 'super bowl',
    'finals', 'playoff', 'title', 'mvp', 'grand slam',
    # Tech milestones
    'launch', 'release', 'milestone', 'breakthrough', 'ipo', 'market cap',
    'trillion', 'adoption', 'approve', 'fda approval', 'spacex',
    # Entertainment / positive events
    'box office', 'oscar', 'grammy', 'emmy', 'concert', 'festival',
    'record sales', 'streaming record', 'subscriber',
    # Crypto UP
    'bitcoin above', 'btc above', 'eth above', 'ethereum above',
    'crypto above', 'bitcoin up', 'btc up', 'new all-time high',
]

NEGATIVE_KEYWORDS = [
    # Geopolitical escalation
    'war', 'invasion', 'conflict', 'sanctions', 'military', 'nuclear',
    'escalation', 'troops', 'missile', 'strike', 'ceasefire fail',
    'nato', 'annex', 'blockade',
    # Catastrophe / disaster
    'hurricane', 'earthquake', 'tsunami', 'wildfire', 'flood', 'famine',
    'drought', 'pandemic', 'epidemic', 'outbreak', 'disease', 'virus',
    'bird flu', 'avian flu', 'covid', 'monkeypox', 'ebola',
    # Economic doom
    'recession', 'crash', 'collapse', 'default', 'bankruptcy', 'bank failure',
    'debt ceiling', 'shutdown', 'layoffs',
    # Crypto DOWN
    'bitcoin below', 'btc below', 'eth below', 'ethereum below',
    'crypto below', 'bitcoin down', 'btc down',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Divergence-specific tunables
DIVERGENCE_THRESHOLD = float(os.environ.get("SIMMER_DIVERGENCE_THRESHOLD", "0.15"))
MIN_BUCKET_SIZE      = int(os.environ.get("SIMMER_MIN_BUCKET_SIZE", "3"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global DIVERGENCE_THRESHOLD, MIN_BUCKET_SIZE
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
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        DIVERGENCE_THRESHOLD = float(os.environ.get("SIMMER_DIVERGENCE_THRESHOLD", str(DIVERGENCE_THRESHOLD)))
        MIN_BUCKET_SIZE      = int(os.environ.get("SIMMER_MIN_BUCKET_SIZE", str(MIN_BUCKET_SIZE)))
    return _client


# ---------------------------------------------------------------------------
# Sentiment classification
# ---------------------------------------------------------------------------

def _classify_sentiment(question: str) -> str | None:
    """
    Classify a market question as 'positive', 'negative', or None (unclassified).
    Matches against keyword lists. Returns the first match found.
    """
    q = question.lower()
    for kw in POSITIVE_KEYWORDS:
        if kw in q:
            return "positive"
    for kw in NEGATIVE_KEYWORDS:
        if kw in q:
            return "negative"
    return None


def _estimate_recency(market) -> float:
    """
    Estimate how 'recent' a market's price movement is.
    Uses distance from 50% as a proxy -- markets that have moved further
    from 50% have had more recent directional movement.
    Returns a value 0.0-1.0 where 1.0 = maximum movement.
    """
    p = market.current_probability
    return abs(p - 0.5) * 2.0  # 0 at 50%, 1.0 at 0% or 100%


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """
    Discover markets using get_markets(limit=200) as PRIMARY discovery,
    with keyword search as secondary fallback for coverage.
    """
    seen, unique = set(), []

    # 1. Primary: broad scan
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[primary] get_markets: {e}")

    # 2. Secondary: targeted keyword search for deeper coverage
    search_terms = [
        'war', 'hurricane', 'bitcoin', 'champion', 'launch',
        'recession', 'pandemic', 'super bowl', 'milestone', 'crash',
    ]
    for kw in search_terms:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


# ---------------------------------------------------------------------------
# Divergence analysis
# ---------------------------------------------------------------------------

def analyze_divergence(markets: list) -> tuple[float, float, float, list, list]:
    """
    Classify all markets, compute positive_index and negative_index,
    and return the divergence score.

    Returns: (divergence, positive_index, negative_index,
              positive_markets, negative_markets)
    """
    positive_markets = []
    negative_markets = []

    for m in markets:
        q = getattr(m, "question", "")
        sentiment = _classify_sentiment(q)
        if sentiment == "positive":
            positive_markets.append(m)
        elif sentiment == "negative":
            negative_markets.append(m)

    if not positive_markets or not negative_markets:
        return 0.0, 0.0, 0.0, positive_markets, negative_markets

    positive_index = sum(m.current_probability for m in positive_markets) / len(positive_markets)
    negative_index = sum(m.current_probability for m in negative_markets) / len(negative_markets)

    # Divergence: if both indices > 0.5, the world is supposedly both great AND terrible
    divergence = positive_index + negative_index - 1.0

    return divergence, positive_index, negative_index, positive_markets, negative_markets


def identify_stale_side(positive_markets: list, negative_markets: list) -> str:
    """
    Determine which side is 'stale' (less recently moved).
    The side with LESS recent movement is the one that hasn't repriced
    to new information -- that's the side we trade against.

    Returns 'positive' or 'negative' -- indicating which side is stale.
    """
    pos_recency = sum(_estimate_recency(m) for m in positive_markets) / max(1, len(positive_markets))
    neg_recency = sum(_estimate_recency(m) for m in negative_markets) / max(1, len(negative_markets))

    # The side with LESS movement is stale -- trade against it
    if pos_recency <= neg_recency:
        return "positive"  # Positive side is stale -> trade against positive sentiment
    else:
        return "negative"  # Negative side is stale -> trade against negative sentiment


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, stale_side: str, divergence: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    When divergence is detected:
    - If the POSITIVE side is stale, positive markets are overpriced -> sell NO on high ones
    - If the NEGATIVE side is stale, negative markets are overpriced -> sell NO on high ones
    We trade AGAINST the stale side: the stale side hasn't repriced to new info,
    so its high probability is the mispricing.
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
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    # Trading against the stale side: these markets are overpriced (too high)
    # So we look for p >= NO_THRESHOLD to sell NO (betting the price comes down)
    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # Boost conviction by divergence magnitude
        div_boost = min(1.5, 1.0 + divergence)
        conviction = min(1.0, conviction * div_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"DIVERGENCE stale={stale_side} div={divergence:.2f} "
            f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:55]}"
        )

    # Also: if stale side has markets priced LOW, they might be underpriced
    # (the positive side is stale = negative info arrived, but positive markets
    #  haven't fallen yet. However some stale-side markets near the floor
    #  might be bargains if the divergence resolves in the stale side's favour)
    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        div_boost = min(1.5, 1.0 + divergence)
        conviction = min(1.0, conviction * div_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"DIVERGENCE stale={stale_side} div={divergence:.2f} "
            f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:55]}"
        )

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


# ---------------------------------------------------------------------------
# Safeguards
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[sentiment-div] mode={mode} max_pos=${MAX_POSITION} "
        f"div_thresh={DIVERGENCE_THRESHOLD} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[sentiment-div] {len(markets)} total markets scanned")

    divergence, pos_idx, neg_idx, pos_mkts, neg_mkts = analyze_divergence(markets)
    safe_print(
        f"[sentiment-div] positive_index={pos_idx:.2f} ({len(pos_mkts)} mkts) "
        f"negative_index={neg_idx:.2f} ({len(neg_mkts)} mkts) "
        f"divergence={divergence:.3f}"
    )

    if len(pos_mkts) < MIN_BUCKET_SIZE or len(neg_mkts) < MIN_BUCKET_SIZE:
        safe_print(
            f"[sentiment-div] insufficient markets: pos={len(pos_mkts)} neg={len(neg_mkts)} "
            f"(need {MIN_BUCKET_SIZE} each). Done."
        )
        return

    if divergence < DIVERGENCE_THRESHOLD:
        safe_print(
            f"[sentiment-div] divergence {divergence:.3f} < threshold {DIVERGENCE_THRESHOLD}. "
            f"No macro inconsistency detected. Done."
        )
        return

    stale_side = identify_stale_side(pos_mkts, neg_mkts)
    safe_print(f"[sentiment-div] stale side = {stale_side} -- trading AGAINST it")

    # Trade against the stale side
    targets = pos_mkts if stale_side == "positive" else neg_mkts

    placed = 0
    for m in targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, stale_side, divergence)
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
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[sentiment-div] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Detects macro sentiment divergence across Polymarket prediction markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
