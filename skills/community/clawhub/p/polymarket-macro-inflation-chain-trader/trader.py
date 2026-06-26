"""
polymarket-macro-inflation-chain-trader
Three-step macro chain reaction trader for Polymarket prediction markets.
Chains commodity pressure -> inflation/rate expectations -> equity impact.
Most traders think in single categories; this skill chains three macro layers
to find mispriced equity-threshold markets when commodity signals diverge.

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

TRADE_SOURCE = "sdk:polymarket-macro-inflation-chain-trader"
SKILL_SLUG   = "polymarket-macro-inflation-chain-trader"

# Classification keywords
COMMODITY_KW = [
    'oil', 'wti', 'crude', 'brent', 'commodity', 'commodities',
    'natural gas', 'copper', 'gold price', 'silver price',
    'oil price', 'barrel', 'opec',
]
MONETARY_KW = [
    'fed', 'federal reserve', 'rate cut', 'rate hike', 'fomc',
    'inflation', 'cpi', 'interest rate', 'monetary policy',
    'powell', 'rate hold', 'basis points', 'hawkish', 'dovish',
]
EQUITY_KW = [
    'nvidia', 'amazon', 's&p', 'sp500', 'nasdaq', 'stock',
    'dow jones', 'apple', 'tesla', 'microsoft', 'google',
    'meta', 'equity', 'market cap', 'ipo', 'earnings',
    'above', 'below', 'stock price',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Skill-specific tunables
COMMODITY_PRESSURE_THRESHOLD = float(os.environ.get("SIMMER_COMMODITY_PRESSURE", "0.50"))
EQUITY_OPTIMISM_HIGH         = float(os.environ.get("SIMMER_EQUITY_OPTIMISM_HIGH", "0.55"))
EQUITY_OPTIMISM_LOW          = float(os.environ.get("SIMMER_EQUITY_OPTIMISM_LOW", "0.40"))
COMMODITY_LOW                = float(os.environ.get("SIMMER_COMMODITY_LOW", "0.30"))

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
    global COMMODITY_PRESSURE_THRESHOLD, EQUITY_OPTIMISM_HIGH, EQUITY_OPTIMISM_LOW, COMMODITY_LOW
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
        COMMODITY_PRESSURE_THRESHOLD = float(os.environ.get("SIMMER_COMMODITY_PRESSURE", str(COMMODITY_PRESSURE_THRESHOLD)))
        EQUITY_OPTIMISM_HIGH = float(os.environ.get("SIMMER_EQUITY_OPTIMISM_HIGH", str(EQUITY_OPTIMISM_HIGH)))
        EQUITY_OPTIMISM_LOW  = float(os.environ.get("SIMMER_EQUITY_OPTIMISM_LOW", str(EQUITY_OPTIMISM_LOW)))
        COMMODITY_LOW        = float(os.environ.get("SIMMER_COMMODITY_LOW", str(COMMODITY_LOW)))
    return _client


# ---------------------------------------------------------------------------
# Market classification
# ---------------------------------------------------------------------------

def classify_market(question: str) -> str | None:
    """Classify a market into 'commodity', 'monetary', 'equity', or None."""
    q = question.lower()
    if any(kw in q for kw in COMMODITY_KW):
        return "commodity"
    if any(kw in q for kw in MONETARY_KW):
        return "monetary"
    if any(kw in q for kw in EQUITY_KW):
        return "equity"
    return None


def is_high_threshold_market(question: str) -> bool:
    """Check if a market asks about a price being ABOVE a threshold (bullish)."""
    q = question.lower()
    return any(w in q for w in ("above", "over", "exceed", "higher than", "reach", "hit"))


def is_rate_hold_or_hike(question: str) -> bool:
    """Check if a monetary market is about holding or hiking rates (hawkish)."""
    q = question.lower()
    if any(w in q for w in ("rate hold", "hold rate", "rate hike", "hike rate", "hawkish", "no cut")):
        return True
    # Inverse: rate cut market -> high prob means dovish, low prob means hawkish
    if any(w in q for w in ("rate cut", "cut rate", "lower rate", "dovish")):
        return False  # This is a cut market, not a hold/hike
    return False


def is_rate_cut_market(question: str) -> bool:
    """Check if a monetary market is specifically about rate cuts."""
    q = question.lower()
    return any(w in q for w in ("rate cut", "cut rate", "lower rate", "dovish"))


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based sizing per CLAUDE.md.
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

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


def compute_chain_signal(market, chain_dir: str,
                         commodity_p: float, equity_p: float) -> tuple[str | None, float, str]:
    """
    Chain-reaction signal for equity markets based on macro divergence.

    chain_dir: "sell_equity" (commodities up, equities haven't corrected)
               or "buy_equity" (commodities down, equities oversold)
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

    if chain_dir == "sell_equity":
        # Commodities are high, equities haven't priced in the pain
        # Sell NO on equity-above-threshold markets (bet they WON'T hit targets)
        if p >= NO_THRESHOLD:
            divergence = commodity_p - (1 - equity_p)
            conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * (1 + divergence))
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "no", size, (
                f"CHAIN-SELL NO p={p:.0%} commodity={commodity_p:.0%} "
                f"equity={equity_p:.0%} size=${size} -- {q[:55]}"
            )
        # Even in the neutral zone, if conviction from the chain is high enough
        if p > 0.50:
            divergence = commodity_p - (1 - equity_p)
            conviction = min(1.0, divergence * 1.5)
            if conviction > 0.2:
                size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
                return "no", size, (
                    f"CHAIN-SELL NO p={p:.0%} commodity={commodity_p:.0%} "
                    f"divergence={divergence:.0%} size=${size} -- {q[:55]}"
                )

    elif chain_dir == "buy_equity":
        # Commodities are low, equities have overreacted downward
        if p <= YES_THRESHOLD:
            relief = (1 - commodity_p) - equity_p
            conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * (1 + relief))
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "yes", size, (
                f"CHAIN-BUY YES p={p:.0%} commodity={commodity_p:.0%} "
                f"equity={equity_p:.0%} size=${size} -- {q[:55]}"
            )
        # Even in the neutral zone, if the overreaction is extreme
        if p < 0.50:
            relief = (1 - commodity_p) - equity_p
            conviction = min(1.0, relief * 1.5)
            if conviction > 0.2:
                size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
                return "yes", size, (
                    f"CHAIN-BUY YES p={p:.0%} commodity={commodity_p:.0%} "
                    f"relief={relief:.0%} size=${size} -- {q[:55]}"
                )

    return None, 0, f"No chain signal at {p:.1%} -- {q[:60]}"


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
    Primary discovery via get_markets(limit=200), then keyword search fallback.
    Deduplicated.
    """
    seen: set[str] = set()
    unique: list = []

    # Primary: bulk fetch
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if classify_market(q) is not None:
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    # Fallback: keyword search for deeper coverage
    all_kw = COMMODITY_KW[:5] + MONETARY_KW[:5] + EQUITY_KW[:5]
    for kw in all_kw:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if classify_market(q) is not None:
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[macro-inflation-chain] mode={mode} max_pos=${MAX_POSITION} "
        f"commodity_threshold={COMMODITY_PRESSURE_THRESHOLD} "
        f"equity_high={EQUITY_OPTIMISM_HIGH} equity_low={EQUITY_OPTIMISM_LOW}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[macro-inflation-chain] {len(markets)} candidate markets")

    # Classify all markets
    commodity_markets = []
    monetary_markets = []
    equity_markets = []

    for m in markets:
        q = getattr(m, "question", "")
        cat = classify_market(q)
        if cat == "commodity":
            commodity_markets.append(m)
        elif cat == "monetary":
            monetary_markets.append(m)
        elif cat == "equity":
            equity_markets.append(m)

    safe_print(
        f"[macro-inflation-chain] classified: "
        f"{len(commodity_markets)} commodity, "
        f"{len(monetary_markets)} monetary, "
        f"{len(equity_markets)} equity"
    )

    # Step 1: Compute commodity_pressure
    # Average probability of commodity-hitting-high-threshold markets
    commodity_probs = []
    for m in commodity_markets:
        q = getattr(m, "question", "")
        p = float(m.current_probability)
        if is_high_threshold_market(q):
            commodity_probs.append(p)
        else:
            # For non-threshold markets, use raw probability
            commodity_probs.append(p)
    commodity_pressure = sum(commodity_probs) / len(commodity_probs) if commodity_probs else 0.5
    safe_print(f"  [chain-1] commodity_pressure={commodity_pressure:.2%} ({len(commodity_probs)} markets)")

    # Step 2: Compute rate_hawkish
    # High = hawkish (rates held/hiked), Low = dovish (rates cut)
    rate_probs = []
    for m in monetary_markets:
        q = getattr(m, "question", "")
        p = float(m.current_probability)
        if is_rate_hold_or_hike(q):
            rate_probs.append(p)  # High P = hawkish
        elif is_rate_cut_market(q):
            rate_probs.append(1 - p)  # High P(cut) = dovish, so invert
        else:
            rate_probs.append(p)
    rate_hawkish = sum(rate_probs) / len(rate_probs) if rate_probs else 0.5
    safe_print(f"  [chain-2] rate_hawkish={rate_hawkish:.2%} ({len(rate_probs)} markets)")

    # Step 3: Compute equity_optimism
    # Average probability of stock-above-threshold markets
    equity_probs = []
    for m in equity_markets:
        q = getattr(m, "question", "")
        p = float(m.current_probability)
        if is_high_threshold_market(q):
            equity_probs.append(p)
        else:
            equity_probs.append(p)
    equity_optimism = sum(equity_probs) / len(equity_probs) if equity_probs else 0.5
    safe_print(f"  [chain-3] equity_optimism={equity_optimism:.2%} ({len(equity_probs)} markets)")

    # Chain logic: determine trade direction
    chain_dir = None
    if commodity_pressure > COMMODITY_PRESSURE_THRESHOLD and equity_optimism > EQUITY_OPTIMISM_HIGH:
        # Equities haven't priced in commodity pressure -> sell equity optimism
        chain_dir = "sell_equity"
        safe_print(
            f"  [chain] SELL signal: commodity={commodity_pressure:.0%}>{COMMODITY_PRESSURE_THRESHOLD:.0%} "
            f"AND equity={equity_optimism:.0%}>{EQUITY_OPTIMISM_HIGH:.0%} -> equities overpriced"
        )
    elif commodity_pressure < COMMODITY_LOW and equity_optimism < EQUITY_OPTIMISM_LOW:
        # Equities overreacted to low commodity pressure -> buy oversold equities
        chain_dir = "buy_equity"
        safe_print(
            f"  [chain] BUY signal: commodity={commodity_pressure:.0%}<{COMMODITY_LOW:.0%} "
            f"AND equity={equity_optimism:.0%}<{EQUITY_OPTIMISM_LOW:.0%} -> equities oversold"
        )
    else:
        safe_print(
            f"  [chain] No chain signal: commodity={commodity_pressure:.0%} "
            f"equity={equity_optimism:.0%} -- no divergence detected"
        )

    if not chain_dir:
        # Fall back to standard conviction-based trading on individual markets
        safe_print("[macro-inflation-chain] No chain signal. Falling back to standard signals.")
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
        safe_print(f"[macro-inflation-chain] done (fallback). {placed} orders placed.")
        return

    # Trade equity markets based on chain signal
    placed = 0
    for m in equity_markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_chain_signal(
            m, chain_dir, commodity_pressure, equity_optimism
        )
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
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:100]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[macro-inflation-chain] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Three-step macro chain reaction trader for Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
