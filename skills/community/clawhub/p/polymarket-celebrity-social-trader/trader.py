"""
polymarket-celebrity-social-trader
Trades celebrity, influencer, and social media prediction markets — Elon tweets,
viral moments, reality TV, YouTube milestones.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-celebrity-social-trader"
SKILL_SLUG   = "polymarket-celebrity-social-trader"

KEYWORDS = [
    'Elon Musk', 'tweet', 'X post', 'Elon tweets', 'YouTube', 'subscribers',
    'viral', 'TikTok views', 'celebrity', 'divorce', 'relationship', 'beef',
    'reality TV', 'The Bachelor', 'Oscars', 'Golden Globes', 'social media',
    'followers', 'Instagram', 'MrBeast', 'Logan Paul', 'boxing', 'Jake Paul',
    'influencer', 'Taylor Swift', 'Beyoncé', 'Grammy', 'Emmy', 'streaming',
    'Spotify streams', 'chart', 'Billboard', 'feud', 'reconcile', 'breakup',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "20"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, corrected for fan loyalty and market type.
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


def celebrity_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.35) combining two structural edges
    unique to celebrity and social media markets:

    1. MARKET TYPE PREDICTABILITY
       Celebrity markets look chaotic but split cleanly into two camps:
       data-trackable metrics (subscriber counts, tweet rates, fight records)
       and emotionally-driven narratives (fan loyalty, feuds, relationships).
       The data-trackable ones have genuine edges; the emotional ones are traps.

       Subscriber / follower / view milestones    → 1.25x
         Social Blade tracks YouTube, Instagram, TikTok growth with daily
         granularity. A "will MrBeast reach 400M subscribers by X" market
         is highly predictable from the published growth curve. Retail never
         checks Social Blade before trading these.

       Elon Musk / high-volume poster tweet count → 1.20x
         Elon's posting rate has been remarkably consistent (~350–400 posts/week).
         Markets pricing his weekly or monthly tweet count frequently misprice
         based on vibes rather than his documented posting cadence.

       Boxing / MMA / combat sport outcome        → 1.15x
         Professional athletic records, training camp signals, and fight
         history exist as hard data. Retail prices celebrity fame, not skill.
         Jake Paul vs. a professional boxer: the record speaks, retail doesn't
         know how to read it.

       Reality TV voting outcome                  → 1.10x
         Nielsen Social Content Ratings track social engagement (comments,
         shares, sentiment) which correlates strongly with elimination votes.
         Retail prices vibes; social data gives structural edge.

       Megastar fan-favourite markets             → 0.75x
         Markets about Taylor Swift, Beyoncé, BTS, Ariana Grande, etc. are
         dominated by fans trading their *feelings*, not probability. Fan
         bases systematically overprice positive outcomes for their idol.
         Retail conviction here is not information — it is loyalty. Fade it.

       Celebrity beef / feud reconciliation       → 0.75x
         "Will X and Y make up?" — fans desperately want reconciliation and
         bid YES far above base rate. Celebrity feuds historically rarely
         fully reconcile on a Polymarket-resolution timeframe. Fade YES hard.

       Celebrity relationship / breakup / divorce → 0.80x
         TMZ-driven, tabloid-narrative markets. Very noisy signal. Both
         directions are overpriced depending on which fanbase is more active.
         Trade small, both ways are usually mispriced toward drama.

       Awards outcome (Oscars, Grammys, Emmy)     → 0.85x
         The awards circuit is followed intensely by a dedicated, informed
         community (critics, industry watchers). These markets are more
         efficiently priced than most — less structural edge.

    2. WEEKEND REPRICING LAG
       Social media metrics — subscriber counts, Spotify streams, tweet totals
       — update continuously, but Polymarket market makers are least active on
       weekends (Friday evening through Sunday). Social media activity peaks
       on weekends. This creates a lag window: real-world metrics move, markets
       don't reprice until Monday.

       For metric-based questions + weekend (Fri–Sun UTC):    → 1.15x
       Other combinations:                                     → 1.00x

    Combined and capped at 1.35x.
    Celebrity markets are inherently noisier than data-driven domains — the cap
    is intentionally lower than other traders to reflect the higher uncertainty.
    """
    weekday = datetime.now(timezone.utc).weekday()  # 0=Mon … 6=Sun
    q = question.lower()

    # Factor 1: market type predictability
    if any(w in q for w in ("subscriber", "subscribers", "follower", "followers",
                             "youtube subscribers", "tiktok followers", "instagram followers",
                             "twitch followers", "views milestone", "view count",
                             "youtube views", "tiktok views")):
        type_mult = 1.25  # Social Blade daily data — retail never checks before trading

    elif any(w in q for w in ("elon", "musk tweet", "tweet count", "tweets per",
                               "how many tweets", "x posts", "posts per week",
                               "posts per month", "tweet rate")):
        type_mult = 1.20  # Consistent ~350-400/week cadence; markets misprice on vibes

    elif any(w in q for w in ("boxing", "fight", "knockout", "ko", "ufc", "mma",
                               "bout", "round", "jake paul", "logan paul", "paul vs",
                               "vs paul", "combat", "match result")):
        type_mult = 1.15  # Athletic record exists; retail prices fame over skill

    elif any(w in q for w in ("reality tv", "bachelor", "survivor", "big brother",
                               "american idol", "the voice", "dancing with the stars",
                               "voted off", "eliminated", "winner of season",
                               "next rose", "immunity")):
        type_mult = 1.10  # Nielsen Social Ratings correlate with actual vote outcomes

    elif any(w in q for w in ("taylor swift", "beyoncé", "beyonce", "bts", "ariana grande",
                               "selena gomez", "billie eilish", "rihanna", "justin bieber",
                               "harry styles", "sabrina carpenter", "olivia rodrigo",
                               "doja cat", "nicki minaj")):
        type_mult = 0.75  # Fan loyalty overcrowds — retail trades feelings, not probability

    elif any(w in q for w in ("beef", "feud", "reconcile", "make up", "forgive",
                               "squash beef", "end feud", "friends again",
                               "bury the hatchet", "settle beef")):
        type_mult = 0.75  # Fans overprice reconciliation — historical base rate is low

    elif any(w in q for w in ("divorce", "breakup", "break up", "split", "separated",
                               "relationship", "dating", "girlfriend", "boyfriend",
                               "engaged", "engagement", "married", "wedding")):
        type_mult = 0.80  # Tabloid-narrative noise — both sides overpriced by rival fanbases

    elif any(w in q for w in ("oscar", "grammy", "emmy", "bafta", "golden globe",
                               "award", "nomination", "nominated", "wins best")):
        type_mult = 0.85  # Awards circuit is efficiently covered by informed watchers

    else:
        type_mult = 1.0

    # Factor 2: weekend lag for metric-based markets
    # Social media metrics update continuously but Polymarket MMs go quiet Fri-Sun.
    metric_keywords = ("subscriber", "follower", "views", "tweet", "post", "stream",
                       "streams", "chart", "billboard", "spotify", "listener")
    is_weekend = weekday >= 4  # Friday=4, Saturday=5, Sunday=6
    if any(w in q for w in metric_keywords) and is_weekend:
        timing_mult = 1.15  # Real-world metrics move; market repricing slowest on weekends
    else:
        timing_mult = 1.0

    return min(1.35, type_mult * timing_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with fan loyalty correction and market type adjustment:
    - Base conviction scales linearly with distance from threshold
    - celebrity_bias() boosts data-trackable markets (subscriber growth, tweet
      cadence, boxing records) and dampens fan-loyalty overcrowded markets
      (megastars, feuds, relationships) where retail trades emotion not probability
    - Weekend lag multiplier for metric-based questions (Social Blade, Spotify, etc.)
    - Cap at 1.35x — celebrity domain has inherently higher noise than data-driven
      domains; intentionally more conservative than crypto or legal traders
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Social Blade subscriber growth rate into p — compare published
    daily growth trajectory to Polymarket milestone probability to trade the gap.
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

    bias = celebrity_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by celebrity bias
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
    print(f"[polymarket-celebrity-social-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-celebrity-social-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-celebrity-social-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades celebrity, influencer, and social media prediction markets — Elon tweets, viral moments, reality TV, YouTube milestones.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
