"""
polymarket-global-elections-trader
Trades Polymarket prediction markets on elections, referendums, and democratic events
worldwide — outside the US (which is heavily covered). Focuses on EU, Latin America,
Asia, and Africa.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-global-elections-trader"
SKILL_SLUG   = "polymarket-global-elections-trader"

KEYWORDS = [
    'election', 'referendum', 'vote', 'prime minister', 'chancellor', 'president',
    'Germany election', 'France election', 'Brazil election', 'India election',
    'UK election', 'Japan election', 'South Korea', 'Taiwan election',
    'snap election', 'coalition', 'majority', 'parliament', 'polling',
    'exit poll', 'incumbent', 'runoff', 'second round', 'Bundestag',
    'Riksdag', 'Assemblée', 'Duma', 'Diet', 'Congress', 'Lok Sabha',
    'confidence vote', 'no confidence', 'hung parliament', 'minority government',
    'proportional representation', 'first past the post',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "10000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "5"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by electoral system type and
# regional information lag.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

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


def election_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.35) combining two structural edges
    unique to global election markets:

    1. ELECTORAL SYSTEM TYPE — HOW PREDICTABLE IS THIS OUTCOME?
       Electoral systems have radically different outcome distributions. Retail
       on Polymarket trades all elections as if they were US presidential races
       (two candidates, coin flip). They aren't. Understanding the system is
       the core alpha in this domain.

       Two-party / FPTP "will X win" (UK, Australia, Canada)  → 1.20x
         First-past-the-post systems amplify polling leads into landslide
         probabilities. A party with a 5% polling lead has ~80-85% win probability,
         not 55%. Retail systematically underestimates this amplification because
         they anchor to the raw poll margin, not the seat-translation model.
         UK constituency-level polling (Electoral Calculus) makes this trackable.

       Runoff / second-round election (France, Brazil, many) → 1.15x
         After the first round, the runoff polling is dramatically more accurate
         than first-round polling. Head-to-head matchup polling post-round-1
         typically has <3% error. Retail treats runoffs with the same uncertainty
         as first rounds — a significant mispricing. Markets on "who wins the
         runoff" immediately after round-1 results are underpriced on the leading
         candidate.

       Referendum (binary yes/no) (Brexit, IndyRef, etc.)    → 1.10x
         Cleaner resolution criteria than multi-candidate races. Well-polled in
         most democratic countries. Retail overcomplicates these.

       Snap election / early dissolution                      → 0.85x
         Called with little notice — no steady polling baseline, high news-driven
         volatility. The incumbent calling the snap usually has a structural
         advantage that retail underestimates, but the timing uncertainty
         dominates. Trade cautiously.

       Coalition formation / government composition           → 0.80x
         Who forms the coalition after an election is driven by multi-party
         negotiation dynamics that are genuinely unpredictable — party veto
         players, policy distance, personal relationships. Polling tells you
         who won seats, not who governs. Trade with significant caution.

       No-confidence vote / leadership challenge              → 0.80x
         Parliamentary arithmetic matters but so does timing of defections,
         backbench rebellions, and party discipline. Hard to model without
         real-time whip counts.

       PR system "will X win an outright majority"            → 0.70x
         The sharpest dampening in this category. In proportional representation
         systems (Germany, Netherlands, Sweden, Norway, Spain, Israel), a single
         party winning an outright majority of seats is extremely rare — typically
         <5% base rate. Retail prices these markets at 15-30% because they project
         US presidential race logic onto parliamentary systems. It almost never
         happens. Every "will X win a majority in the Bundestag/Riksdag/Knesset"
         question is a structural NO unless polling shows >45% for one party.

    2. REGIONAL INFORMATION LAG — THE POLYMARKET BLINDSPOT
       Polymarket is overwhelmingly US-English-speaking. Non-English-language
       polling updates reach Polymarket traders with a systematic lag of 12–48h.
       Local-language polling aggregators update daily; Polymarket prices don't.
       This is the most exploitable structural gap in election markets.

       German / French / Dutch / Scandinavian elections      → 1.20x
         Wahlrecht.de (Germany), Politico Europe, Votecompass — daily polling
         aggregators in German/French/Dutch that US retail doesn't monitor.
         The lag between a 3-point swing in Wahlrecht and Polymarket repricing
         is 12-36 hours. This is the richest information lag in the category.

       Brazilian / Latin American elections                  → 1.15x
         DataFolha and Quaest (Brazil) publish daily tracking polls in
         Portuguese. CIEP (Mexico), CNC (Argentina) similarly. High-quality
         polling that US retail rarely reads. Runoff races especially.

       South / Southeast Asian elections                     → 1.15x
         India (CSDS, ABP-CVoter), Indonesia (LSI, Indikator), Philippines
         (Pulse Asia) publish local-language tracking. Indian exit polls in
         particular are released in local languages hours before English
         coverage catches up. Enormous audience + lag = large edge.

       UK / Australian / Canadian elections (English)        → 1.05x
         Well-covered in English but less so than US elections. Electoral
         Calculus (UK) and YouGov MRP models give structural edges that
         Polymarket retail underweights.

       Sub-Saharan Africa / fragile democracies              → 0.75x
         Low polling quality (sample sizes, access), high institutional
         volatility. Election outcomes regularly include coup risk, result
         disputes, and logistical delays that make clean resolution uncertain.
         Trade very conservatively — resolution risk is material.

    Combined and capped at 1.35x.
    German FPTP (UK-style): 1.20 × 1.20 = 1.35x cap.
    PR majority question in Germany: 0.70 × 1.20 = 0.84x — correctly skeptical.
    Brazilian runoff: 1.15 × 1.15 = 1.32x — strong, data-backed edge.
    """
    q = question.lower()

    # Factor 1: electoral system type
    if any(w in q for w in ("first past the post", "fptp", "constituency",
                             "seats in parliament", "parliamentary majority",
                             "wins the election", "general election",
                             "wins a majority", "wins the seat")):
        # Disambiguate: FPTP vs PR majority
        if any(w in q for w in ("germany", "bundestag", "netherlands", "sweden",
                                 "riksdag", "norway", "spain", "israel", "knesset",
                                 "proportional", "list seat", "coalition required")):
            system_mult = 0.70  # PR system — majority is near-impossible
        else:
            system_mult = 1.20  # FPTP — polling leads amplify strongly into wins

    elif any(w in q for w in ("runoff", "second round", "second-round",
                               "tour de scrutin", "segundo turno",
                               "ballotage", "deux tours")):
        system_mult = 1.15  # Post-round-1 runoff polling very accurate (<3% error)

    elif any(w in q for w in ("referendum", "plebiscite", "ballot measure",
                               "popular vote on", "vote on independence",
                               "vote on membership", "vote on joining")):
        system_mult = 1.10  # Binary, well-polled, clean resolution criteria

    elif any(w in q for w in ("snap election", "early election", "dissolve parliament",
                               "dissolution", "called early", "called snap")):
        system_mult = 0.85  # No steady polling baseline — volatile

    elif any(w in q for w in ("coalition", "form government", "coalition government",
                               "govern with", "coalition partner", "junior partner",
                               "governing coalition")):
        system_mult = 0.80  # Post-election negotiation — genuinely unpredictable

    elif any(w in q for w in ("no confidence", "confidence vote", "leadership challenge",
                               "leadership contest", "oust", "remove prime minister",
                               "resign", "step down")):
        system_mult = 0.80  # Parliamentary arithmetic + timing of defections

    elif any(w in q for w in ("bundestag majority", "riksdag majority", "knesset majority",
                               "win majority in", "absolute majority", "supermajority",
                               "two-thirds majority")):
        system_mult = 0.70  # PR majority — structurally rare regardless of wording

    else:
        system_mult = 1.0

    # Factor 2: regional information lag
    if any(w in q for w in ("germany", "german", "bundestag", "france", "french",
                             "assemblée", "netherlands", "dutch", "sweden", "swedish",
                             "riksdag", "norway", "denmark", "finland", "austria",
                             "belgium", "switzerland", "spain", "italy", "poland",
                             "chancellor", "président", "premier ministre")):
        region_mult = 1.20  # Wahlrecht.de / Politico Europe — daily lag vs Polymarket

    elif any(w in q for w in ("brazil", "brazilian", "mexico", "mexican",
                               "argentina", "colombia", "chile", "peru",
                               "venezuela", "ecuador", "latin america",
                               "segundo turno", "datafolha", "quaest")):
        region_mult = 1.15  # DataFolha/Quaest/CIEP daily — English lag substantial

    elif any(w in q for w in ("india", "indian", "lok sabha", "indonesia",
                               "indonesian", "philippines", "philippine",
                               "bangladesh", "pakistan", "sri lanka",
                               "south korea", "taiwan", "japan", "japanese")):
        region_mult = 1.15  # Local-language polls + exit polls hours ahead of English

    elif any(w in q for w in ("uk", "united kingdom", "britain", "british",
                               "australia", "australian", "canada", "canadian",
                               "new zealand")):
        region_mult = 1.05  # English-language but less Polymarket attention than US

    elif any(w in q for w in ("africa", "nigeria", "kenya", "ghana", "senegal",
                               "ethiopia", "zimbabwe", "congo", "cameroon",
                               "mali", "burkina", "guinea", "sudan")):
        region_mult = 0.75  # Low polling quality + institutional volatility + coup risk

    else:
        region_mult = 1.0

    return min(1.35, system_mult * region_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with electoral system type and regional lag adjustment:
    - Base conviction scales linearly with distance from threshold
    - election_bias() corrects for two orthogonal edges: system type predictability
      (FPTP amplification 1.20x vs PR majority impossibility 0.70x) and regional
      information lag (German/French/Scandinavian elections lag Polymarket 12-36h)
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Wahlrecht.de / Politico Europe polling averages into p to trade
    the gap between daily aggregator updates and Polymarket's stale prices directly.
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

    bias = election_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by election bias
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
    print(f"[polymarket-global-elections-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-global-elections-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-global-elections-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on elections, referendums, and democratic events worldwide.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
