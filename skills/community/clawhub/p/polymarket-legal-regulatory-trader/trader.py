"""
polymarket-legal-regulatory-trader
Trades legal and regulatory prediction markets: court rulings, antitrust cases, SEC actions, EU fines, and DOJ investigations.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-legal-regulatory-trader"
SKILL_SLUG   = "polymarket-legal-regulatory-trader"

KEYWORDS = [
    'Supreme Court', 'SCOTUS', 'lawsuit', 'antitrust', 'SEC', 'DOJ',
    'EU fine', 'GDPR', 'regulation', 'court ruling', 'verdict',
    'Apple', 'Google', 'Meta', 'Microsoft', 'Amazon',
    'FTC', 'merger blocked', 'acquisition blocked', 'appeal',
    'settlement', 'class action', 'patent', 'trial', 'indicted',
    'Binance', 'Coinbase', 'crypto regulation', 'CFTC',
    'Wells Notice', 'EU competition', 'Phase 2', 'DG Comp',
    'plea deal', 'conviction',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "8000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.1"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "5"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by documented legal base rates.
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


def precedent_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.80–1.35) based on documented
    legal and regulatory institutional base rates.

    Most Polymarket retail participants don't read court filings or
    understand regulatory procedure. They treat legal outcomes as coin
    flips. This bias encodes well-documented historical statistics
    directly into conviction sizing — no API required.

    Action type                         Historical rate              Multiplier
    ──────────────────────────────────  ───────────────────────────  ──────────
    DOJ criminal conviction post-indict ~97% plea/conviction rate    1.35x
    Class action settlement             ~90%+ settle before trial    1.25x
    SEC enforcement (post-Wells Notice) ~85% result in formal action 1.20x
    EU Phase 2 antitrust outcome        ~80%+ conditions or fine     1.20x
    SCOTUS reversal (cert granted)      ~70% reverse lower court     1.15x
    Crypto enforcement post-charges     High after formal charges    1.15x
    Big tech merger blocked (FTC/DOJ)   ~40-60%, rising trend        1.10x
    Regulatory approval / clearance     Harder to time — be cautious 0.80x
    """
    q = question.lower()

    # DOJ criminal conviction after indictment — ~97% plea/conviction rate
    # Retail consistently prices this as 50/50. It almost never is.
    if any(w in q for w in ("convicted", "guilty", "plea deal", "plead guilty",
                             "criminal conviction", "indicted", "doj criminal")):
        return 1.35

    # Class action — ~90%+ settle before reaching trial
    if any(w in q for w in ("class action", "settle", "settlement")):
        return 1.25

    # SEC enforcement after Wells Notice — ~85% result in formal action
    if any(w in q for w in ("sec enforcement", "sec charges", "sec action",
                             "sec fine", "wells notice", "sec investigation")):
        return 1.20

    # EU antitrust Phase 2 — almost always results in conditions/fine (~80%+)
    # Phase 2 timelines are almost exactly 13 months — procedurally clockwork
    if any(w in q for w in ("eu fine", "european commission", "eu antitrust",
                             "dg comp", "phase 2", "gdpr fine", "eu competition")):
        return 1.20

    # SCOTUS — ~70% reverse lower court when cert is granted
    # SCOTUS takes only ~1-2% of cases; granting cert signals intent to correct
    if any(w in q for w in ("supreme court", "scotus", "certiorari")):
        return 1.15

    # Crypto enforcement — high conviction probability once formal charges filed
    if any(w in q for w in ("binance", "coinbase sec", "crypto enforcement",
                             "cftc enforcement", "crypto charges")):
        return 1.15

    # Big tech merger blocked — FTC/DOJ increasingly aggressive (~40-60% now)
    if any(w in q for w in ("merger blocked", "acquisition blocked", "ftc block",
                             "doj block", "antitrust block", "merger challenge")):
        return 1.10

    # Regulatory approval / clearance — harder to time, be conservative
    if any(w in q for w in ("approved", "cleared", "regulatory approval",
                             "merger approved", "merger cleared")):
        return 0.80

    return 1.0  # general legal market — no documented base rate to apply


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with legal precedent adjustment:
    - Base conviction scales linearly with distance from threshold
    - precedent_bias() encodes documented institutional base rates —
      DOJ ~97% conviction, class actions ~90% settle, SCOTUS ~70% reverse
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed CourtListener docket filing velocity or SEC EDGAR
    enforcement release dates into p to trade the divergence between
    procedural timelines and naive market pricing.
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

    bias = precedent_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by precedent bias
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
    print(f"[polymarket-legal-regulatory-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-legal-regulatory-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-legal-regulatory-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades legal and regulatory prediction markets: court rulings, antitrust cases, SEC actions, EU fines, and DOJ investigations.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
