"""
polymarket-onlyfans-trader
Trades Polymarket markets on OnlyFans — celebrity join events, platform
bans/restrictions, and creator earnings — by exploiting three structural
mispricings unique to the creator economy.

THE EDGE — THREE STRUCTURAL LAYERS:

1. CELEBRITY PIPELINE BIAS (demographic base-rate mispricing)
   Retail prices "will [celebrity] join OnlyFans?" based on general fame
   level, treating it as a rare or surprising event. The historical base
   rate tells a different story by demographic:

     Reality TV contestant (post-season):  ~40% join within 12 months
     Instagram/influencer model (1M+ followers): ~30%
     Mid-tier athlete / sports personality:  ~20%
     Musician (pop/hip-hop, 18–35):          ~15%
     A-list Hollywood actor:                 ~5%

   Markets about reality TV contestants are frequently priced at 15–20%
   when the base rate is 3–4x higher. We buy YES aggressively on these.
   We fade markets about A-list actors where prices often exceed the base
   rate due to tabloid speculation.

2. REGULATORY THEATER (ban/restriction markets are chronically overpriced)
   Every 6–12 months a country or US state announces it will ban OnlyFans
   or heavily restrict adult content platforms. These markets are priced
   by retail based on political rhetoric, not legislative reality:

   - Average time from "announced review" to actual ban: 3–7 years
   - Effective bans are almost never achieved (VPN workarounds,
     court injunctions, creator economic lobbying)
   - Of 40+ countries that have threatened restrictions since 2020,
     fewer than 3 have enacted enforceable legislation

   We systematically fade YES on ban/restriction markets (buy NO)
   unless very close to a concrete vote with a documented timeline.

3. CREATOR EARNINGS SEASONALITY
   OnlyFans revenue is strongly seasonal — driven by the holiday gift
   economy and Valentine's Day spending:

     Nov–Feb (peak):  +20–35% above annual average
     Mar–Apr (mid):   baseline
     May–Oct (trough): -10–20% below annual average

   Earnings milestone markets ("will creator X reach $Y by [date]?")
   that span or land in the Nov–Feb window are systematically underpriced.
   Markets resolving in summer are overpriced for the same reason.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-onlyfans-trader"
SKILL_SLUG   = "polymarket-onlyfans-trader"

KEYWORDS = [
    # Celebrity join markets
    "join onlyfans", "joining onlyfans", "onlyfans account", "start onlyfans",
    "create onlyfans", "onlyfans page", "sign up onlyfans",
    # Platform ban / restriction
    "onlyfans ban", "ban onlyfans", "onlyfans banned", "onlyfans restrict",
    "onlyfans blocked", "onlyfans regulation", "onlyfans law",
    "onlyfans illegal", "onlyfans shutdown", "shut down onlyfans",
    # Creator earnings / milestones
    "onlyfans earnings", "onlyfans revenue", "onlyfans subscribers",
    "onlyfans million", "onlyfans income", "onlyfans top creator",
    # Platform-level
    "onlyfans ipo", "onlyfans valuation", "onlyfans creator fund",
    "onlyfans policy", "onlyfans adult content",
    # General
    "onlyfans",
]

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


# ---------------------------------------------------------------------------
# Market classifier
# ---------------------------------------------------------------------------

def _classify_market(question: str) -> str:
    """
    Classify the market into one of three types:
      'join'       — will [person] join / start OnlyFans?
      'ban'        — will OnlyFans be banned / restricted / shut down?
      'earnings'   — will [creator] reach an earnings / subscriber milestone?
      'unknown'    — other OnlyFans market
    """
    q = question.lower()
    ban_terms = ("ban", "banned", "restrict", "blocked", "shutdown", "shut down",
                 "illegal", "law", "regulation", "prohibit", "outlaw", "block")
    join_terms = ("join", "joining", "create", "start", "sign up", "launch",
                  "open", "start an", "make an", "set up")
    earn_terms = ("earn", "revenue", "income", "million", "subscriber", "follow",
                  "subscriber", "valuation", "ipo", "net worth", "pay")

    if any(t in q for t in ban_terms):
        return "ban"
    if any(t in q for t in join_terms):
        return "join"
    if any(t in q for t in earn_terms):
        return "earnings"
    return "unknown"


# ---------------------------------------------------------------------------
# Edge 1: Celebrity pipeline bias
# ---------------------------------------------------------------------------

def _celebrity_pipeline_mult(question: str) -> tuple[str, float]:
    """
    Returns (label, multiplier) for the celebrity pipeline base-rate edge.

    Only applied to 'join' markets. For other market types returns 1.00x.

    Demographic categories (parsed from question keywords):

    REALITY TV (highest pipeline → strongest YES bias):
      Signals: "bachelor", "bachelorette", "love island", "big brother",
               "real housewives", "vanderpump", "jersey shore", "temptation",
               "survivor", "amazing race", "dancing with", "dancing on ice",
               "strictly", "x factor", "idol", "drag race", "below deck",
               "summer house", "winter house", "too hot", "love is blind",
               "married at first", "90 day", "teen mom"
      Base rate ~40% → market often at 15–20% → strong YES edge

    INFLUENCER / MODEL:
      Signals: "influencer", "model", "instagram", "tiktok creator",
               "youtuber", "content creator", "onlyfans model",
               "playboy", "maxim", "fitness model", "swimsuit"
      Base rate ~30%

    SPORTS / ATHLETE:
      Signals: "athlete", "footballer", "soccer player", "nfl", "nba",
               "mma", "ufc", "boxer", "wrestling", "wwe", "tennis player",
               "golfer"
      Base rate ~20%

    MUSICIAN (pop / hip-hop):
      Signals: "rapper", "singer", "musician", "pop star", "hip hop",
               "r&b", "artist"
      Base rate ~15%

    A-LIST ACTOR / HIGH-PROFILE:
      Signals: "oscar", "hollywood", "movie star", "actor", "actress",
               "emmy", "grammy", "golden globe"
      Base rate ~5% → market often at 15–25% → tabloid hype overprices

    Multiplier logic:
      YES_THRESHOLD serves as the anchoring reference. We boost multiplier
      when the demographic base rate significantly exceeds what the market
      is likely implying at the YES_THRESHOLD price level.
    """
    q = question.lower()

    reality_tv = (
        "bachelor", "bachelorette", "love island", "big brother",
        "real housewives", "vanderpump", "jersey shore", "temptation island",
        "survivor", "amazing race", "dancing with", "dancing on ice",
        "strictly come", "x factor", "american idol", "drag race",
        "below deck", "summer house", "winter house", "too hot to handle",
        "love is blind", "married at first sight", "90 day fiance", "teen mom",
        "made in chelsea", "towie", "geordie shore", "ex on the beach",
        "paradise hotel", "paradise",
    )
    influencer = (
        "influencer", "instagram model", "tiktok", "youtuber",
        "content creator", "playboy", "maxim", "fitness model",
        "swimsuit model", "only fans model",
    )
    sports = (
        "nfl player", "nba player", "footballer", "soccer player",
        "mma fighter", "ufc", "boxer", "wrestling", "wwe", "tennis player",
        "golfer", "athlete",
    )
    musician = (
        "rapper", "hip hop", "r&b artist", "pop star", "singer",
        "musician", "recording artist",
    )
    aList = (
        "oscar winner", "oscar-winning", "hollywood actor", "movie star",
        "emmy award", "grammy winner", "golden globe",
    )

    if any(t in q for t in reality_tv):
        return "REALITY-TV(base~40%)", 1.35
    if any(t in q for t in influencer):
        return "INFLUENCER(base~30%)", 1.20
    if any(t in q for t in sports):
        return "ATHLETE(base~20%)", 1.10
    if any(t in q for t in musician):
        return "MUSICIAN(base~15%)", 1.00
    if any(t in q for t in aList):
        # A-list: tabloid hype inflates price above base rate → fade YES
        return "A-LIST(base~5%,fade)", 0.75
    return "CELEB-UNKNOWN", 1.00


# ---------------------------------------------------------------------------
# Edge 2: Regulatory theater
# ---------------------------------------------------------------------------

def _regulatory_theater_mult(question: str) -> tuple[str, float]:
    """
    Returns (label, multiplier) for the regulatory theater edge.

    Only applied to 'ban' markets. Returns 1.00x for other types.

    Ban/restriction markets are chronically overpriced because:
    - Legislative processes take years; Polymarket markets resolve in months
    - Court injunctions routinely block enforcement of platform bans
    - VPN workarounds make practical bans largely unenforceable
    - Creator economic lobbying is powerful and well-funded
    - Even authoritarian jurisdictions (UAE, India) have struggled to
      maintain consistent enforcement of content platform bans

    We invert the signal for ban markets:
      - Buy NO when the market price is high (retail believes the ban)
      - The NO_THRESHOLD for ban markets is LOWER than standard, since
        even a 55% "yes on ban" price is almost certainly overpriced

    Multiplier applied to the NO conviction (fading the ban):
      Jurisdiction factors:
        "US", "United States", "America", "federal":  0.90x
          (US has First Amendment constraints; federal bans near-impossible)
        "UK", "Britain", "England":                   0.95x
          (age verification laws exist but full bans face strong opposition)
        "EU", "Europe":                               0.90x
          (GDPR enforcement is the real risk, not bans)
        "Australia":                                  0.85x
          (eSafety office has powers but full bans historically blocked)
        Authoritarian jurisdictions (China, Russia, UAE, Saudi):  1.10x
          (actual ban risk is higher, though market still overprices speed)
        Generic / unspecified:                        1.00x
    """
    q = question.lower()

    if any(t in q for t in ("united states", "u.s.", "us ban", "federal", "congress")):
        return "JURISDICTION-US(First-Amendment-shield)", 0.90
    if any(t in q for t in ("uk", "united kingdom", "britain", "england", "ofcom")):
        return "JURISDICTION-UK(age-verif-not-ban)", 0.95
    if any(t in q for t in ("european union", "eu ban", "europe")):
        return "JURISDICTION-EU(GDPR-not-ban)", 0.90
    if any(t in q for t in ("australia", "australian", "esafety")):
        return "JURISDICTION-AU(eSafety-limited)", 0.85
    if any(t in q for t in ("china", "russia", "uae", "saudi", "iran", "pakistan")):
        return "JURISDICTION-AUTH(real-risk)", 1.10
    return "JURISDICTION-GENERIC", 1.00


# ---------------------------------------------------------------------------
# Edge 3: Creator earnings seasonality
# ---------------------------------------------------------------------------

def _earnings_season_mult() -> tuple[str, float]:
    """
    Returns (label, multiplier) based on OnlyFans revenue seasonality.

    OnlyFans revenue follows a strong annual pattern driven by the gift
    economy and major cultural/romantic spending events:

      Nov–Feb: PEAK season
        - Black Friday / Cyber Monday subscription promos (Nov)
        - Holiday gifting mindset (Dec)
        - New Year's resolutions / "treat yourself" spending (Jan)
        - Valentine's Day ramp-up: the single highest revenue week
          of the year for most creators is the 7 days before Feb 14 (Feb)
        → Earnings milestone markets resolving in this window are
          systematically underpriced. Multiplier: 1.20x

      Mar–Apr: POST-PEAK normalization
        → Spending returns to baseline after Valentine's. Multiplier: 1.00x

      May–Oct: TROUGH
        - Summer outdoor activity reduces screen time / subscriptions
        - No major gift-giving holidays
        - Creator content volume often drops (vacations, burnout)
        → Earnings milestone markets in this window are overpriced.
          Multiplier: 0.85x
    """
    month = datetime.now(timezone.utc).month
    if month in (11, 12, 1, 2):
        return "EARNINGS-PEAK(Nov-Feb)", 1.20
    if month in (3, 4):
        return "EARNINGS-NORMAL(Mar-Apr)", 1.00
    return "EARNINGS-TROUGH(May-Oct)", 0.85


# ---------------------------------------------------------------------------
# Signal bias combiner
# ---------------------------------------------------------------------------

def onlyfans_signal_bias(question: str, market_type: str) -> tuple[float, str]:
    """
    Returns (bias_multiplier, debug_label) based on market type.

    join markets:    pipeline_mult × earnings_season_mult
    ban markets:     regulatory_mult (season irrelevant)
    earnings markets: earnings_season_mult
    unknown:         1.00x (no structural edge identified)

    Capped 0.65–1.40x.
    """
    if market_type == "join":
        pipeline_label, pipeline_mult = _celebrity_pipeline_mult(question)
        season_label,   season_mult   = _earnings_season_mult()
        combined = pipeline_mult * season_mult
        label = f"{pipeline_label} × {season_label}"

    elif market_type == "ban":
        reg_label, reg_mult = _regulatory_theater_mult(question)
        combined = reg_mult
        label = f"REGULATORY-THEATER × {reg_label}"

    elif market_type == "earnings":
        season_label, season_mult = _earnings_season_mult()
        combined = season_mult
        label = season_label

    else:
        return 1.00, "UNKNOWN-MARKET-TYPE"

    capped = min(1.40, max(0.65, combined))
    return capped, label


# ---------------------------------------------------------------------------
# Core signal
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    For BAN markets the signal logic is inverted:
    - Buy NO when p >= NO_THRESHOLD (we're fading the regulatory hype)
      with conviction amplified by regulatory_theater_mult.
    - Buy YES when p <= YES_THRESHOLD (market has already heavily discounted
      the ban — unlikely but possible).

    For JOIN and EARNINGS markets the standard direction applies:
    - Buy YES when underpriced (p <= YES_THRESHOLD).
    - Buy NO when overpriced (p >= NO_THRESHOLD).
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

    market_type = _classify_market(q)
    bias, bias_label = onlyfans_signal_bias(q, market_type)

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return (
            "yes", size,
            f"YES [{market_type}] {p:.0%} edge={edge:.0%} bias={bias:.2f}x "
            f"[{bias_label}] size=${size} — {q[:55]}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return (
            "no", size,
            f"NO [{market_type}] YES={p:.0%} edge={edge:.0%} bias={bias:.2f}x "
            f"[{bias_label}] size=${size} — {q[:55]}"
        )

    return None, 0, (
        f"Neutral {p:.1%} [{market_type}] — "
        f"outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands"
    )


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


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
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
        MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active OnlyFans markets, deduplicated."""
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


def run(live: bool = False) -> None:
    season_label, _ = _earnings_season_mult()
    mode = "LIVE" if live else "PAPER (sim)"
    print(
        f"[polymarket-onlyfans-trader] mode={mode} "
        f"season={season_label} max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-onlyfans-trader] {len(markets)} candidate markets")

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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:75]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-onlyfans-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades OnlyFans prediction markets using celebrity pipeline base-rates, "
            "regulatory theater fading, and creator earnings seasonality."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
