"""
polymarket-science-milestones-trader
Trades Polymarket prediction markets on scientific breakthroughs, Nobel Prizes,
physics discoveries, climate science milestones, and research paper impact.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-science-milestones-trader"
SKILL_SLUG   = "polymarket-science-milestones-trader"

KEYWORDS = [
    'Nobel Prize', 'Nobel', 'physics', 'fusion energy', 'ITER', 'nuclear fusion',
    'dark matter', 'quantum computer', 'quantum computing', 'breakthrough',
    'nature paper', 'CERN', 'James Webb', 'room temperature superconductor',
    'AGI', 'consciousness', 'cancer cure', 'Alzheimer treatment', 'longevity',
    'aging reversal', 'CRISPR', 'gene therapy', 'clinical trial', 'phase 3',
    'replication', 'preprint', 'arXiv', 'peer review', 'superconductor',
    'LK-99', 'qubit', 'quantum supremacy', 'drug approval',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "14"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, corrected for science hype cycles and
# Nobel calendar timing.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Nobel Prize announcement week: first two weeks of October.
# Physics: first Monday of Oct. Chemistry: Tuesday. Physiology/Medicine: Monday.
# Peace: Friday. Economics: Monday of the second week.
# Clarivate Citation Laureates shortlist typically released in late September.
_NOBEL_WEEK_MONTHS   = {10}          # October
_CLARIVATE_MONTH     = 9             # September — shortlist published

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS, YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        # Load tunable overrides set via the Simmer UI (SIMMER_* vars only).
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
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active markets matching strategy keywords, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def science_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.55–1.35) combining two structural edges
    unique to science milestone markets:

    1. SCIENCE CLAIM TYPE — HYPE CYCLE vs REPLICATION REALITY
       Science markets are priced by non-experts following journalist headlines.
       Journalists systematically amplify the most optimistic interpretation of
       scientific results. The research community knows the replication rate,
       timeline track record, and definitional ambiguity behind each claim.
       Retail doesn't. This creates large, consistent mispricings by claim type.

       CRISPR / gene therapy clinical milestone          → 1.15x
         clinicaltrials.gov publishes trial endpoints and expected completion
         dates. CRISPR therapies (Casgevy approved 2023) have defined Phase 3
         paths. Regulatory milestones for gene therapy are trackable — retail
         treats them as sci-fi when the FDA approval process is public record.

       Alzheimer / neurodegeneration specific drug       → 1.10x
         Lecanemab (2023) and Donanemab (2024) set precedent for the amyloid
         hypothesis approval path. Post-Phase 3 Alzheimer drug markets are now
         structured similarly to other FDA approvals. Regulatory calendar is
         public; retail still prices with existential uncertainty.

       Nobel Prize (any field)                           → 1.15x (+ timing below)
         Thomson Reuters / Clarivate Citation Laureates has predicted ~40% of
         Nobel winners in advance using citation impact. Importantly: Nobel
         committees reward work done 10–30 years ago that has been thoroughly
         replicated and transformed a field. Retail chases recent hype; Clarivate
         tracks citation longevity. The information is public every September.

       Dark matter / particle physics detection          → 0.85x
         Rare binary events. Multiple experiments (LZ, XENONnT, PandaX) have
         published sensitivity curves and expected timelines. The science is
         trackable but genuine detections are rare — retail doesn't understand
         that "no signal yet" is itself strong data.

       Quantum computing milestone (specific qubit count) → 0.85x
         IBM, Google, and IonQ publish public roadmaps with qubit targets.
         Markets on specific count thresholds are somewhat trackable. But:
         corporate "quantum supremacy" claims are marketing-contaminated and
         frequently contested — apply skepticism to claims from press releases.

       AGI / artificial general intelligence by date     → 0.70x
         The single most definitionally ambiguous claim in science markets.
         "AGI" has no agreed definition — the resolution criteria are almost
         always vague enough that any outcome can be disputed. Retail overprices
         dramatically based on AI hype cycles. Additionally: every AGI timeline
         prediction since 1956 has been wrong. Trade the historical base rate.

       Longevity / aging reversal / lifespan extension   → 0.70x
         Longevity conference culture creates aggressive retail overcrowding on
         YES for "will human lifespan reach 150 by X" type markets. The gap
         between mouse model results (which dominate longevity press) and human
         clinical validation is 10–15 years minimum. Retail collapses this gap.

       Cancer "cure" or universal treatment              → 0.65x
         The most fundamental category error in science markets. "Cancer" is
         200+ distinct diseases with different mechanisms, genetics, and treatment
         paths. A market asking "will a cure for cancer be found by X" contains
         an incoherent premise that virtually guarantees NO regardless of medical
         progress. Retail prices the headline emotion, not the biology.

       Commercial fusion / grid-connected fusion         → 0.65x
         The canonical "5 years away" joke in physics. NIF achieved ignition
         (Q>1) in December 2022 — a genuine historic milestone. But commercial
         fusion (grid-connected, cost-competitive) is a different problem entirely.
         ITER's completion has been delayed from 2016 → 2020 → 2025 → 2035.
         Every commercial fusion company's timeline has slipped by >50%.
         Markets on fusion electricity "by X" are systematically overpriced.

       Room temperature superconductor claim             → 0.55x
         The lowest confidence category. Every major "room temperature
         superconductor" claim since 1987 has either failed replication or been
         retracted. The 2023 LK-99 episode — global excitement, total replication
         failure within two weeks — is the template. Retail gets euphoric;
         physicists know the replication failure rate is near 100%.
         The prior probability of any specific RT superconductor claim surviving
         peer review and replication is extremely low.

    2. NOBEL CALENDAR TIMING
       Nobel Prize announcements follow a precise, known schedule every October.
       Clarivate Citation Laureates publishes its shortlist in late September.
       Both create specific, exploitable timing windows:

       Nobel market + October (announcement week)       → 1.25x
         The committee meets and announces in real-time. Polymarket takes
         15–30 minutes to fully reprice after each announcement. Pre-announcement,
         Clarivate shortlist provides structural edge retail ignores.

       Nobel market + September (Clarivate month)       → 1.15x
         Clarivate shortlist is public. Markets priced without this data
         can be traded against it — retail doesn't read citation databases.

       Nobel market + other months                      → 1.00x

    Combined and capped at 1.35x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: science claim type
    if any(w in q for w in ("crispr", "gene therapy", "gene editing", "base editing",
                             "prime editing", "casgevy", "gene correction",
                             "gene therapy trial")):
        claim_mult = 1.15  # clinicaltrials.gov trackable — retail treats as sci-fi

    elif any(w in q for w in ("alzheimer", "lecanemab", "donanemab", "amyloid",
                               "tau protein", "neurodegeneration treatment",
                               "parkinson treatment", "dementia drug")):
        claim_mult = 1.10  # Post-Phase 3 FDA path now established; calendar trackable

    elif any(w in q for w in ("nobel prize", "nobel", "nobel laureate",
                               "nobel winner", "fields medal")):
        claim_mult = 1.15  # Clarivate ~40% hit rate; committee prefers verified longevity

    elif any(w in q for w in ("dark matter", "dark energy", "wimp", "axion",
                               "neutron star", "gravitational wave", "ligo",
                               "particle physics", "higgs", "cern")):
        claim_mult = 0.85  # Binary rare event — publishable sensitivity curves exist

    elif any(w in q for w in ("quantum comput", "qubit", "quantum supremacy",
                               "quantum advantage", "fault tolerant",
                               "error correction", "quantum processor")):
        claim_mult = 0.85  # Roadmaps public but corporate claims marketing-contaminated

    elif any(w in q for w in ("agi", "artificial general intelligence",
                               "human-level ai", "superintelligence",
                               "ai consciousness", "sentient ai")):
        claim_mult = 0.70  # No agreed definition; every timeline since 1956 was wrong

    elif any(w in q for w in ("longevity", "lifespan", "aging reversal", "anti-aging",
                               "life extension", "immortality", "senolytics",
                               "yamanaka", "epigenetic reprogramming",
                               "live to 150", "live to 120")):
        claim_mult = 0.70  # Mouse → human gap 10-15 years; conference hype cycles retail

    elif any(w in q for w in ("cancer cure", "cure cancer", "cure for cancer",
                               "universal cancer", "cancer vaccine broad",
                               "end cancer")):
        claim_mult = 0.65  # Category error — 200+ diseases; premise is incoherent

    elif any(w in q for w in ("fusion energy", "fusion power", "fusion electricity",
                               "commercial fusion", "iter complete", "fusion reactor",
                               "fusion plant", "fusion grid", "tokamak power")):
        claim_mult = 0.65  # Canonical "5 years away" — every milestone delayed 5-10 years

    elif any(w in q for w in ("room temperature superconductor", "room-temperature",
                               "ambient superconductor", "lk-99", "superconductor",
                               "superconducting at room")):
        claim_mult = 0.55  # Near-100% replication failure rate; LK-99 is the template

    else:
        claim_mult = 1.0

    # Factor 2: Nobel calendar timing (only applied to Nobel markets)
    is_nobel = any(w in q for w in ("nobel", "nobel prize", "laureate",
                                     "nobel winner", "fields medal"))
    if is_nobel:
        if month in _NOBEL_WEEK_MONTHS:
            timing_mult = 1.25  # Announcement week — Clarivate + real-time repricing edge
        elif month == _CLARIVATE_MONTH:
            timing_mult = 1.15  # Clarivate shortlist published — public data retail ignores
        else:
            timing_mult = 1.00
    else:
        timing_mult = 1.0

    return min(1.35, claim_mult * timing_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with science hype cycle correction and Nobel timing:
    - Base conviction scales linearly with distance from threshold
    - science_bias() corrects for systematic retail overpricing of dramatic claims
      (fusion 0.65x, RT superconductors 0.55x, cancer cure 0.65x) and boosts
      data-trackable milestones (CRISPR/gene therapy 1.15x, Alzheimer drugs 1.10x)
    - Nobel markets boosted during October announcement week (1.25x timing)
      and September Clarivate shortlist month (1.15x)
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Clarivate Citation Laureates shortlist into YES market pricing
    for Nobel markets to trade the gap between citation-data prediction and
    naive retail allocation across candidates.
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

    bias = science_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by science bias
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


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


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    month = datetime.now(timezone.utc).month
    nobel_window = "ANNOUNCEMENT" if month == 10 else ("CLARIVATE" if month == 9 else "off-season")
    print(f"[polymarket-science-milestones-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS} nobel={nobel_window}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-science-milestones-trader] {len(markets)} candidate markets")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            print(f"  [skip] {why}")
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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-science-milestones-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on scientific breakthroughs, Nobel Prizes, physics discoveries, and research milestones.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
