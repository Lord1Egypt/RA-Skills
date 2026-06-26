"""
polymarket-macro-asymmetric-longshot-trader
Systematically finds markets with huge asymmetric payoff -- markets priced at
2-10% where cross-category macro analysis suggests the REAL probability is
15-30%. A $5 bet at 5% returns $100 if right. The key: use CROSS-CATEGORY
macro signals to identify which longshots have hidden support.

Core edge: Most longshot bettors pick them randomly ("wouldn't it be cool if").
This trader uses RELATED markets in OTHER categories to identify which longshots
are systematically underpriced. If "BTC above $70k" is at 8% but BTC momentum
markets are trending up, the 70k threshold is underpriced. If "measles > 2000"
is at 5% but "measles > 1000" is already at 70%, the 2000 level is underpriced.

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

TRADE_SOURCE = "sdk:polymarket-macro-asymmetric-longshot-trader"
SKILL_SLUG   = "polymarket-macro-asymmetric-longshot-trader"

KEYWORDS = [
    'bitcoin above', 'btc above', 'ethereum above', 'eth above',
    'solana above', 'sol above', 'xrp above', 'crypto price',
    'measles', 'bird flu', 'avian flu', 'pandemic', 'outbreak',
    'war', 'invasion', 'escalation', 'sanctions', 'nuclear',
    'tariff', 'trade war', 'embargo', 'coup', 'resign',
    'impeach', 'default', 'recession', 'rate cut', 'rate hike',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",       "40"))
MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",         "3000"))
MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",         "0.10"))
MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",           "1"))
MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      "10"))
YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",      "0.38"))
NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",       "0.62"))
MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",          "5"))
# Skill-specific tunables
LONGSHOT_CEILING   = float(os.environ.get("SIMMER_LONGSHOT_CEILING",   "0.10"))
MIN_SUPPORT        = float(os.environ.get("SIMMER_MIN_SUPPORT",        "0.40"))
# Longshot sizing cap: max 30% of MAX_POSITION (these are high-risk bets)
LONGSHOT_SIZE_CAP  = float(os.environ.get("SIMMER_LONGSHOT_SIZE_CAP",  "0.30"))

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
    global LONGSHOT_CEILING, MIN_SUPPORT, LONGSHOT_SIZE_CAP
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
        LONGSHOT_CEILING  = float(os.environ.get("SIMMER_LONGSHOT_CEILING",  str(LONGSHOT_CEILING)))
        MIN_SUPPORT       = float(os.environ.get("SIMMER_MIN_SUPPORT",       str(MIN_SUPPORT)))
        LONGSHOT_SIZE_CAP = float(os.environ.get("SIMMER_LONGSHOT_SIZE_CAP", str(LONGSHOT_SIZE_CAP)))
    return _client


# ---------------------------------------------------------------------------
# Market category classification
# ---------------------------------------------------------------------------

_CRYPTO_RE = re.compile(
    r'(bitcoin|btc|ethereum|eth|solana|sol|xrp|crypto|btcusdt)',
    re.I,
)
_HEALTH_RE = re.compile(
    r'(measles|bird flu|avian|h5n1|pandemic|outbreak|cases|deaths|who\b|cdc)',
    re.I,
)
_GEOPOLITICS_RE = re.compile(
    r'(war|invasion|escalat|sanction|nuclear|nato|missile|troops|attack|military)',
    re.I,
)
_ECONOMIC_RE = re.compile(
    r'(tariff|trade war|embargo|recession|default|rate cut|rate hike|gdp|inflation|fed\b)',
    re.I,
)
_POLITICAL_RE = re.compile(
    r'(coup|resign|impeach|election|vote|president|prime minister|parliament)',
    re.I,
)

# Threshold pattern: "above 70k", "above $70,000", "above 2000", "> 1500"
_THRESHOLD_RE = re.compile(
    r'(?:above|over|exceed|surpass|reach|hit|>)\s*\$?(\d[\d,]*\.?\d*)\s*(?:k|K|usdt|usd)?',
    re.I,
)


def classify_market(question: str) -> str:
    """Classify a market into a category for macro support scoring."""
    q = question.lower()
    if _CRYPTO_RE.search(q):
        return "crypto"
    if _HEALTH_RE.search(q):
        return "health"
    if _GEOPOLITICS_RE.search(q):
        return "geopolitics"
    if _ECONOMIC_RE.search(q):
        return "economic"
    if _POLITICAL_RE.search(q):
        return "political"
    return "other"


def extract_threshold(question: str) -> float | None:
    """Extract a numeric threshold from a question."""
    m = _THRESHOLD_RE.search(question)
    if m:
        val_str = m.group(1).replace(",", "")
        try:
            val = float(val_str)
            # Check for "k" suffix
            after = question[m.end():m.end()+2].lower()
            if after.startswith("k"):
                val *= 1000
            return val
        except ValueError:
            pass
    return None


def is_longshot(p: float) -> bool:
    """Return True if the probability qualifies as a longshot."""
    return 0.02 <= p <= LONGSHOT_CEILING


# ---------------------------------------------------------------------------
# Cross-category macro support scoring
# ---------------------------------------------------------------------------

def compute_macro_support(market, all_markets: list) -> tuple[float, str]:
    """
    Compute a macro support score (0.0 to 1.0) for a longshot market by
    checking related markets in other categories.

    Returns (score, explanation).
    """
    q = market.question.lower()
    p = float(market.current_probability)
    category = classify_market(market.question)

    # --- Crypto longshots: check if lower thresholds are already likely ---
    if category == "crypto":
        threshold = extract_threshold(market.question)
        if threshold is not None:
            # Find related crypto markets with LOWER thresholds
            related_probs = []
            for other in all_markets:
                if other.id == market.id:
                    continue
                oq = other.question.lower()
                if not _CRYPTO_RE.search(oq):
                    continue
                other_thresh = extract_threshold(other.question)
                if other_thresh is not None and other_thresh < threshold:
                    related_probs.append(float(other.current_probability))

            if related_probs:
                # If lower thresholds are very likely, this higher threshold
                # is underpriced. Score = average of lower threshold probs.
                avg_lower = sum(related_probs) / len(related_probs)
                # Scale: if avg_lower > 0.6, strong support
                score = min(1.0, avg_lower * 1.2)
                return score, (
                    f"crypto-ladder: {len(related_probs)} lower thresholds "
                    f"avg={avg_lower:.0%}"
                )

        # Fallback: check if any crypto "up" or momentum markets are bullish
        bullish_count = 0
        for other in all_markets:
            oq = other.question.lower()
            if _CRYPTO_RE.search(oq) and other.id != market.id:
                op = float(other.current_probability)
                if op > 0.60 and any(w in oq for w in ("up", "above", "bull", "rise")):
                    bullish_count += 1
        if bullish_count >= 2:
            score = min(1.0, 0.3 + bullish_count * 0.15)
            return score, f"crypto-momentum: {bullish_count} bullish markets"

    # --- Health longshots: check escalation ladder ---
    if category == "health":
        threshold = extract_threshold(market.question)
        if threshold is not None:
            related_probs = []
            for other in all_markets:
                if other.id == market.id:
                    continue
                oq = other.question.lower()
                if not _HEALTH_RE.search(oq):
                    continue
                other_thresh = extract_threshold(other.question)
                if other_thresh is not None and other_thresh < threshold:
                    related_probs.append(float(other.current_probability))

            if related_probs:
                avg_lower = sum(related_probs) / len(related_probs)
                score = min(1.0, avg_lower * 1.3)
                return score, (
                    f"health-escalation: {len(related_probs)} lower thresholds "
                    f"avg={avg_lower:.0%}"
                )

        # Fallback: check if related health markets are heating up
        heating = 0
        for other in all_markets:
            if other.id == market.id:
                continue
            oq = other.question.lower()
            if _HEALTH_RE.search(oq) and float(other.current_probability) > 0.50:
                heating += 1
        if heating >= 2:
            score = min(1.0, 0.25 + heating * 0.15)
            return score, f"health-heating: {heating} related markets >50%"

    # --- Geopolitics longshots: check escalation markets ---
    if category == "geopolitics":
        escalation_count = 0
        escalation_avg = 0.0
        for other in all_markets:
            if other.id == market.id:
                continue
            oq = other.question.lower()
            if _GEOPOLITICS_RE.search(oq):
                op = float(other.current_probability)
                if op > 0.40:
                    escalation_count += 1
                    escalation_avg += op

        if escalation_count >= 2:
            escalation_avg /= escalation_count
            score = min(1.0, escalation_avg * 1.2)
            return score, (
                f"geopolitics-escalation: {escalation_count} related markets "
                f"avg={escalation_avg:.0%}"
            )

    # --- Economic longshots: check related macro signals ---
    if category == "economic":
        related_heat = 0
        for other in all_markets:
            if other.id == market.id:
                continue
            oq = other.question.lower()
            if _ECONOMIC_RE.search(oq) and float(other.current_probability) > 0.45:
                related_heat += 1
        if related_heat >= 2:
            score = min(1.0, 0.30 + related_heat * 0.12)
            return score, f"economic-heat: {related_heat} related markets >45%"

    # --- Political longshots: check related political markets ---
    if category == "political":
        related_heat = 0
        for other in all_markets:
            if other.id == market.id:
                continue
            oq = other.question.lower()
            if _POLITICAL_RE.search(oq) and float(other.current_probability) > 0.45:
                related_heat += 1
        if related_heat >= 2:
            score = min(1.0, 0.30 + related_heat * 0.12)
            return score, f"political-heat: {related_heat} related markets >45%"

    return 0.0, "no macro support found"


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market, all_markets: list) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Only trades longshots (p between
    0.02 and LONGSHOT_CEILING) that have cross-category macro support above
    MIN_SUPPORT. Position sizes are capped at LONGSHOT_SIZE_CAP * MAX_POSITION
    because these are high-risk, high-reward bets.
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

    # Longshot gate: only trade markets priced between 2% and LONGSHOT_CEILING
    if not is_longshot(p):
        return None, 0, f"Not a longshot: p={p:.1%} (need {0.02:.0%}-{LONGSHOT_CEILING:.0%})"

    # Compute macro support score
    support_score, support_reason = compute_macro_support(market, all_markets)

    if support_score < MIN_SUPPORT:
        return None, 0, (
            f"Weak macro support: {support_score:.2f} < {MIN_SUPPORT:.2f} "
            f"({support_reason}) -- {q[:50]}"
        )

    # Longshot = always buy YES (we are betting the unlikely event happens)
    # Conviction scales with how far below the ceiling AND macro support
    conviction = ((LONGSHOT_CEILING - p) / LONGSHOT_CEILING) * support_score
    conviction = min(1.0, conviction)

    # Cap position size for longshots (high risk)
    max_longshot_size = LONGSHOT_SIZE_CAP * MAX_POSITION
    size = max(MIN_TRADE, round(conviction * max_longshot_size, 2))

    payoff_mult = (1.0 / p) if p > 0 else 0
    edge_reason = (
        f"YES {p:.0%} support={support_score:.2f} "
        f"payoff={payoff_mult:.0f}x size=${size} "
        f"({support_reason}) -- {q[:45]}"
    )
    return "yes", size, edge_reason


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
    Find active markets across all categories via keyword search + bulk fetch
    fallback, deduplicated.
    """
    seen: set[str] = set()
    unique: list = []

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback -- primary discovery
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                seen.add(market_id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[asymmetric-longshot] mode={mode} max_pos=${MAX_POSITION} "
        f"ceiling={LONGSHOT_CEILING:.0%} min_support={MIN_SUPPORT:.2f} "
        f"size_cap={LONGSHOT_SIZE_CAP:.0%}"
    )

    client = get_client(live=live)
    all_markets = find_markets(client)
    safe_print(f"[asymmetric-longshot] {len(all_markets)} total markets discovered")

    # Find longshots
    longshots = [
        m for m in all_markets
        if is_longshot(float(m.current_probability))
    ]
    safe_print(f"[asymmetric-longshot] {len(longshots)} longshot candidates (p={0.02:.0%}-{LONGSHOT_CEILING:.0%})")

    # Score and trade
    placed = 0
    scored: list[tuple[float, object, str, float, str]] = []

    for m in longshots:
        side, size, reasoning = compute_signal(m, all_markets)
        if side:
            # Extract support score for sorting
            support_score, _ = compute_macro_support(m, all_markets)
            scored.append((support_score, m, side, size, reasoning))
        else:
            safe_print(f"  [skip] {reasoning}")

    # Sort by macro support score descending (best supported longshots first)
    scored.sort(key=lambda x: x[0], reverse=True)
    safe_print(f"[asymmetric-longshot] {len(scored)} longshots with macro support >= {MIN_SUPPORT:.2f}")

    for support_score, m, side, size, reasoning in scored:
        if placed >= MAX_POSITIONS:
            break

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

    safe_print(f"[asymmetric-longshot] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Finds asymmetric longshot markets (2-10% probability) with cross-category "
            "macro support. Small bets, huge potential payoff."
        )
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
