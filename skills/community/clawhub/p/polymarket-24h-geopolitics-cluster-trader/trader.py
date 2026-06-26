"""
polymarket-24h-geopolitics-cluster-trader
Trades logical inconsistencies in geopolitical event clusters on Polymarket.

Core edge: Geopolitical markets form logical clusters where probabilities must
satisfy consistency constraints. For example:
- Strike-count markets are cumulative: P(strike 7) <= P(strike 6) always
- Daily military action across regions should correlate (escalation chains)
- Prerequisite events constrain downstream markets (Iran action -> Israel response)

When these constraints are violated, the mispriced market reverts. This skill
detects the violation and trades the correction, sizing by conviction.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-24h-geopolitics-cluster-trader"
SKILL_SLUG   = "polymarket-24h-geopolitics-cluster-trader"

KEYWORDS = [
    "Israel", "military", "strike", "Iran", "Gaza",
    "Lebanon", "war", "ceasefire",
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "35"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "5000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.08"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "0"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "8"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))
MIN_VIOLATION   = float(os.environ.get("SIMMER_MIN_VIOLATION",   "0.04"))

_client: SimmerClient | None = None


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_VIOLATION
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
        MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    str(MAX_POSITION)))
        MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      str(MIN_VOLUME)))
        MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      str(MAX_SPREAD)))
        MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        str(MIN_DAYS)))
        MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   str(MAX_POSITIONS)))
        YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   str(YES_THRESHOLD)))
        NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    str(NO_THRESHOLD)))
        MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       str(MIN_TRADE)))
        MIN_VIOLATION   = float(os.environ.get("SIMMER_MIN_VIOLATION",   str(MIN_VIOLATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing — extract event type, region, threshold from question text
# ---------------------------------------------------------------------------

# Matches: "Will Israel strike 6 countries in 2026?"
_STRIKE_COUNT_PATTERN = re.compile(
    r"(?:Israel|IDF)\s+(?:strike|attack|bomb)\s+(\d+)\s+(?:countries|nations|targets)",
    re.I,
)

# Matches: "Will Israel take military action in Gaza on March 21?"
# Also handles: "Will Iran conduct a military action against Israel on March 23, 2026?"
_DAILY_ACTION_PATTERN = re.compile(
    r"(?:Israel|IDF|Iran|Hezbollah|Hamas)\s+(?:take\s+|conduct\s+(?:a\s+)?)?(?:military\s+action|strike|attack|bomb)"
    r"(?:\s+(?:in|on|against)\s+)?"
    r"(Gaza|Lebanon|Syria|Iran|Yemen|West\s*Bank|Israel|Iraq)"
    r"(?:\s+on\s+)?"
    r"((?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2})?",
    re.I,
)

# Matches: "Will Iran conduct military action against Israel?"
_BILATERAL_PATTERN = re.compile(
    r"(Iran|Israel|Hezbollah|Hamas|Turkey|Saudi\s*Arabia)"
    r".*(?:military\s+action|strike|attack|war|invasion)"
    r".*(?:against|on|in)\s+"
    r"(Iran|Israel|Gaza|Lebanon|Syria|Yemen|West\s*Bank|Iraq)",
    re.I,
)

# Ceasefire patterns
_CEASEFIRE_PATTERN = re.compile(
    r"ceasefire.*?(Gaza|Lebanon|Israel|Iran|Syria|Yemen|Ukraine|Russia)",
    re.I,
)


class ParsedMarket:
    """Structured representation of a geopolitical market."""
    __slots__ = (
        "market", "cluster_type", "region", "actor", "threshold",
        "date_str", "probability",
    )

    def __init__(self, market, cluster_type, region, actor, threshold,
                 date_str, probability):
        self.market = market
        self.cluster_type = cluster_type   # "strike_count", "daily_action", "bilateral", "ceasefire"
        self.region = region               # normalized region/target
        self.actor = actor                 # "Israel", "Iran", etc.
        self.threshold = threshold         # numeric threshold for strike-count markets
        self.date_str = date_str           # date string for daily markets
        self.probability = probability


def normalize_region(r: str) -> str:
    """Normalize region strings for grouping."""
    if not r:
        return ""
    r = r.strip().lower().replace(" ", "")
    mapping = {
        "westbank": "west_bank",
        "gaza": "gaza",
        "lebanon": "lebanon",
        "syria": "syria",
        "iran": "iran",
        "yemen": "yemen",
        "israel": "israel",
        "iraq": "iraq",
    }
    return mapping.get(r, r)


def parse_market(market) -> ParsedMarket | None:
    """Parse a geopolitical market question into a structured form."""
    q = getattr(market, "question", "")
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None
    p = float(p)

    # Try strike-count pattern first
    m = _STRIKE_COUNT_PATTERN.search(q)
    if m:
        threshold = int(m.group(1))
        return ParsedMarket(
            market=market, cluster_type="strike_count",
            region="multi", actor="Israel", threshold=threshold,
            date_str=None, probability=p,
        )

    # Try daily military action pattern
    m = _DAILY_ACTION_PATTERN.search(q)
    if m:
        region = normalize_region(m.group(1))
        date_str = m.group(2).strip().lower() if m.group(2) else None
        # Extract actor
        actor_match = re.search(r"(Israel|IDF|Iran|Hezbollah|Hamas)", q, re.I)
        actor = actor_match.group(1) if actor_match else "unknown"
        return ParsedMarket(
            market=market, cluster_type="daily_action",
            region=region, actor=actor, threshold=None,
            date_str=date_str, probability=p,
        )

    # Try bilateral pattern
    m = _BILATERAL_PATTERN.search(q)
    if m:
        actor = m.group(1).strip()
        target = normalize_region(m.group(2))
        return ParsedMarket(
            market=market, cluster_type="bilateral",
            region=target, actor=actor, threshold=None,
            date_str=None, probability=p,
        )

    # Try ceasefire pattern
    m = _CEASEFIRE_PATTERN.search(q)
    if m:
        region = normalize_region(m.group(1))
        return ParsedMarket(
            market=market, cluster_type="ceasefire",
            region=region, actor="ceasefire", threshold=None,
            date_str=None, probability=p,
        )

    return None


# ---------------------------------------------------------------------------
# Cluster grouping and consistency checks
# ---------------------------------------------------------------------------

def group_by_cluster(parsed: list[ParsedMarket]) -> dict[str, list[ParsedMarket]]:
    """Group parsed markets into logical clusters."""
    clusters: dict[str, list[ParsedMarket]] = {}
    for pm in parsed:
        if pm.cluster_type == "strike_count":
            key = f"strike_count|{pm.actor}"
        elif pm.cluster_type == "daily_action":
            key = f"daily_action|{pm.date_str or 'undated'}"
        elif pm.cluster_type == "bilateral":
            key = f"bilateral|{pm.actor}|{pm.region}"
        elif pm.cluster_type == "ceasefire":
            key = f"ceasefire|{pm.region}"
        else:
            continue
        clusters.setdefault(key, []).append(pm)
    return clusters


def check_strike_count_monotonicity(cluster: list[ParsedMarket]) -> list[tuple]:
    """
    Strike-count markets must be monotonically decreasing:
    P(strike 7) <= P(strike 6) <= P(strike 5) ...

    Striking N countries requires striking N-1 first, so the higher
    threshold must always have lower or equal probability.

    Returns list of (overpriced_market, underpriced_market, violation_size).
    """
    # Sort by threshold ascending
    by_threshold = sorted(
        [pm for pm in cluster if pm.threshold is not None],
        key=lambda pm: pm.threshold,
    )
    if len(by_threshold) < 2:
        return []

    violations = []
    for i in range(len(by_threshold) - 1):
        lower = by_threshold[i]      # e.g., strike 5 countries
        higher = by_threshold[i + 1]  # e.g., strike 6 countries

        # P(higher threshold) should be <= P(lower threshold)
        if higher.probability > lower.probability + MIN_VIOLATION:
            violation = higher.probability - lower.probability
            violations.append((higher, lower, violation))

    return violations


def check_daily_action_correlation(cluster: list[ParsedMarket]) -> list[tuple]:
    """
    Daily military action markets for different regions on the same date
    should correlate — escalation in one area increases probability in others.

    If one region has very high probability (resolved YES / near certain) but a
    correlated region shows very low probability, and another shows much lower,
    detect the inconsistency.

    Returns list of (candidate_market, reference_market, violation_size).
    """
    if len(cluster) < 2:
        return []

    # Group by region
    by_region: dict[str, ParsedMarket] = {}
    for pm in cluster:
        if pm.region not in by_region:
            by_region[pm.region] = pm

    if len(by_region) < 2:
        return []

    # Find the highest-probability market as the "anchor"
    sorted_by_prob = sorted(by_region.values(), key=lambda pm: pm.probability, reverse=True)
    anchor = sorted_by_prob[0]

    violations = []
    for pm in sorted_by_prob[1:]:
        # Large gap between anchor and another region may indicate a tradeable
        # inconsistency — the low-prob market may be underpriced given escalation
        gap = anchor.probability - pm.probability
        if gap >= MIN_VIOLATION and pm.probability <= YES_THRESHOLD:
            violations.append((pm, anchor, gap))

    return violations


def check_prerequisite_chain(
    bilateral_clusters: dict[str, list[ParsedMarket]],
    strike_clusters: dict[str, list[ParsedMarket]],
) -> list[tuple]:
    """
    Prerequisite events constrain downstream markets. For example:
    - If "Iran military action against Israel" is at 8%, then Israel-strike
      markets that implicitly require Iranian escalation should not price
      higher scenarios too high.

    Returns list of (overpriced_market, constraint_market, violation_size).
    """
    violations = []

    # Find Iran -> Israel bilateral probability
    iran_israel_prob = None
    iran_israel_market = None
    for key, cluster in bilateral_clusters.items():
        if "iran" in key.lower() and "israel" in key.lower():
            for pm in cluster:
                if iran_israel_prob is None or pm.probability > iran_israel_prob:
                    iran_israel_prob = pm.probability
                    iran_israel_market = pm

    if iran_israel_prob is None or iran_israel_market is None:
        return violations

    # High strike counts implicitly require broader escalation
    # If P(Iran action) is low, very high strike counts should be even lower
    for _key, cluster in strike_clusters.items():
        for pm in cluster:
            if pm.threshold is not None and pm.threshold >= 6:
                # P(strike 6+) should not greatly exceed P(Iran action)
                # because striking 6+ countries likely involves Iranian theater
                if pm.probability > iran_israel_prob + MIN_VIOLATION:
                    violation = pm.probability - iran_israel_prob
                    violations.append((pm, iran_israel_market, violation))

    return violations


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def valid_market(market) -> tuple[bool, str]:
    """Check spread and days-to-resolution gates."""
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return False, "missing probability"

    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return False, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return False, f"Only {days} days to resolve"
        except Exception:
            pass

    return True, "ok"


def compute_signal(market, side_hint: str, violation: float, reason: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    side_hint: "yes" if market is underpriced, "no" if overpriced.
    violation: magnitude of the logical inconsistency.
    Conviction scales with both the violation size and the threshold distance.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    p = float(getattr(market, "current_probability", 0))

    if side_hint == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by violation magnitude
        viol_boost = min(1.0, (violation - MIN_VIOLATION) / max(0.01, YES_THRESHOLD))
        combined = min(1.0, max(conviction, viol_boost))
        size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
        return "yes", size, reason

    if side_hint == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        viol_boost = min(1.0, (violation - MIN_VIOLATION) / max(0.01, 1 - NO_THRESHOLD))
        combined = min(1.0, max(conviction, viol_boost))
        size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
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
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


_GEO_FILTER = re.compile(
    r"(israel|iran|gaza|lebanon|military|strike.*countr|ceasefire|war\b|invasion)",
    re.I,
)


def find_markets(client: SimmerClient) -> list:
    """Find active geopolitical markets, deduplicated.
    Filters out non-geopolitical matches (e.g. esports with 'strike' in name)."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                q = getattr(m, "question", "")
                if market_id and market_id not in seen and _GEO_FILTER.search(q):
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[geopolitics-cluster] mode={mode} max_pos=${MAX_POSITION} min_viol={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[geopolitics-cluster] {len(markets)} candidate geopolitical markets")

    # Parse all markets — log raw questions for debugging
    parsed: list[ParsedMarket] = []
    for m in markets:
        q = getattr(m, "question", "")
        pm = parse_market(m)
        if pm:
            safe_print(f"  [parsed] {pm.cluster_type}: {q[:90]}")
            parsed.append(pm)
        else:
            safe_print(f"  [no-parse] {q[:90]}")

    print(f"[geopolitics-cluster] {len(parsed)} parseable markets")

    # Group into clusters
    clusters = group_by_cluster(parsed)
    print(f"[geopolitics-cluster] {len(clusters)} clusters: " +
          ", ".join(f"{k}({len(v)})" for k, v in clusters.items()))

    # Log each cluster
    for key, members in clusters.items():
        entries_str = ", ".join(
            f"{pm.region or pm.actor}@{pm.probability:.0%}"
            + (f"[t={pm.threshold}]" if pm.threshold is not None else "")
            for pm in members
        )
        safe_print(f"  [{key}] {entries_str}")

    # Separate cluster types for different checks
    strike_clusters = {k: v for k, v in clusters.items() if k.startswith("strike_count")}
    daily_clusters = {k: v for k, v in clusters.items() if k.startswith("daily_action")}
    bilateral_clusters = {k: v for k, v in clusters.items() if k.startswith("bilateral")}

    # Collect all trading opportunities: market_id -> (market, side, violation, reason)
    all_opps: dict[str, tuple] = {}

    # 1. Strike-count monotonicity violations
    for key, cluster in strike_clusters.items():
        violations = check_strike_count_monotonicity(cluster)
        for overpriced, underpriced, viol in violations:
            # Sell the overpriced higher-threshold market (NO)
            mid = getattr(overpriced.market, "id", None)
            if mid:
                reason = (
                    f"MONO: P(strike {overpriced.threshold})={overpriced.probability:.0%} > "
                    f"P(strike {underpriced.threshold})={underpriced.probability:.0%} "
                    f"viol={viol:.0%} — {getattr(overpriced.market, 'question', '')[:60]}"
                )
                existing = all_opps.get(mid)
                if existing is None or viol > existing[2]:
                    all_opps[mid] = (overpriced.market, "no", viol, reason)

            # Buy the underpriced lower-threshold market (YES)
            mid2 = getattr(underpriced.market, "id", None)
            if mid2:
                reason2 = (
                    f"MONO: P(strike {underpriced.threshold})={underpriced.probability:.0%} "
                    f"underpriced vs P(strike {overpriced.threshold})={overpriced.probability:.0%} "
                    f"viol={viol:.0%} — {getattr(underpriced.market, 'question', '')[:60]}"
                )
                existing2 = all_opps.get(mid2)
                if existing2 is None or viol > existing2[2]:
                    all_opps[mid2] = (underpriced.market, "yes", viol, reason2)

    # 2. Daily military action correlation violations
    for key, cluster in daily_clusters.items():
        violations = check_daily_action_correlation(cluster)
        for candidate, anchor, viol in violations:
            mid = getattr(candidate.market, "id", None)
            if mid:
                reason = (
                    f"CORR: {candidate.region}@{candidate.probability:.0%} underpriced vs "
                    f"{anchor.region}@{anchor.probability:.0%} on {candidate.date_str or 'same date'} "
                    f"gap={viol:.0%} — {getattr(candidate.market, 'question', '')[:60]}"
                )
                existing = all_opps.get(mid)
                if existing is None or viol > existing[2]:
                    all_opps[mid] = (candidate.market, "yes", viol, reason)

    # 3. Prerequisite chain violations
    prereq_violations = check_prerequisite_chain(bilateral_clusters, strike_clusters)
    for overpriced, constraint, viol in prereq_violations:
        mid = getattr(overpriced.market, "id", None)
        if mid:
            reason = (
                f"PREREQ: P(strike {overpriced.threshold})={overpriced.probability:.0%} > "
                f"P({constraint.actor}->{constraint.region})={constraint.probability:.0%} "
                f"viol={viol:.0%} — {getattr(overpriced.market, 'question', '')[:60]}"
            )
            existing = all_opps.get(mid)
            if existing is None or viol > existing[2]:
                all_opps[mid] = (overpriced.market, "no", viol, reason)

    print(f"[geopolitics-cluster] {len(all_opps)} violation opportunities")

    # Execute trades on best violations
    placed = 0
    for market_id, opp in sorted(all_opps.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market, side_hint, violation, reason = opp
        side, size, reasoning = compute_signal(market, side_hint, violation, reason)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            print(f"  [skip] {why}")
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
            print(f"  [error] {market_id}: {e}")

    print(f"[geopolitics-cluster] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades geopolitical cluster inconsistencies on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
