"""
polymarket-macro-weekend-momentum-trader
Trades altcoin (ETH/SOL/XRP) Up/Down markets based on BTC weekend price
threshold momentum drift. BTC leads altcoins by 6-24 hours on weekends
because altcoin market makers are less active.

Core edge: BTC price threshold markets form a "ladder" — if P(BTC above $66k)
rises from 40% to 60% over a few hours, that is a bullish drift signal. Altcoin
Up/Down markets (ETH/SOL/XRP) lag this move because weekend altcoin liquidity is
thin and market makers reprice slowly. By the time altcoins catch up, the drift
is already priced in for BTC but NOT for altcoins.

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

TRADE_SOURCE = "sdk:polymarket-macro-weekend-momentum-trader"
SKILL_SLUG   = "polymarket-macro-weekend-momentum-trader"

KEYWORDS = [
    'bitcoin above', 'btc above', 'BTCUSDT above', 'bitcoin reach', 'btc reach',
    'bitcoin hit', 'btc hit', 'bitcoin price', 'btc price', 'btc threshold',
    'Ethereum Up or Down', 'Solana Up or Down', 'XRP Up or Down',
    'ETH Up or Down', 'SOL Up or Down',
    'ethereum up', 'solana up', 'xrp up',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION      = float(os.environ.get("SIMMER_MAX_POSITION",     "40"))
MIN_VOLUME        = float(os.environ.get("SIMMER_MIN_VOLUME",       "3000"))
MAX_SPREAD        = float(os.environ.get("SIMMER_MAX_SPREAD",       "0.08"))
MIN_DAYS          = int(os.environ.get(  "SIMMER_MIN_DAYS",         "0"))
MAX_POSITIONS     = int(os.environ.get(  "SIMMER_MAX_POSITIONS",    "8"))
YES_THRESHOLD     = float(os.environ.get("SIMMER_YES_THRESHOLD",    "0.38"))
NO_THRESHOLD      = float(os.environ.get("SIMMER_NO_THRESHOLD",     "0.62"))
MIN_TRADE         = float(os.environ.get("SIMMER_MIN_TRADE",        "5"))
# Skill-specific: minimum BTC drift to trigger altcoin trades
DRIFT_THRESHOLD   = float(os.environ.get("SIMMER_DRIFT_THRESHOLD",  "0.08"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, DRIFT_THRESHOLD
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
        DRIFT_THRESHOLD = float(os.environ.get("SIMMER_DRIFT_THRESHOLD", str(DRIFT_THRESHOLD)))
    return _client


# ---------------------------------------------------------------------------
# Market classification helpers
# ---------------------------------------------------------------------------

def _is_btc_threshold_market(question: str) -> bool:
    """Return True if the question is a BTC price threshold market."""
    q = question.lower()
    has_btc   = any(w in q for w in ("bitcoin", "btc", "btcusdt"))
    has_price = any(w in q for w in ("above", "reach", "hit", "exceed", "trade at",
                                      "surpass", "break", "touch", "price"))
    has_level = any(c in q for c in ("usdt", "usd", "$")) or any(
                    w in q for w in ("100k", "110k", "120k", "130k", "140k",
                                      "150k", "160k", "170k", "180k", "200k",
                                      "000 usdt", "000 usd"))
    return has_btc and has_price and has_level


def _is_altcoin_updown_market(question: str) -> bool:
    """Return True if the question is an altcoin Up or Down market."""
    q = question.lower()
    has_alt   = any(w in q for w in ("ethereum", "eth", "solana", "sol", "xrp"))
    has_updown = "up or down" in q or "up/down" in q
    return has_alt and has_updown


def _extract_btc_threshold(question: str) -> float | None:
    """
    Extract the BTC price threshold from a question like
    "Will BTC trade above $66,000?" -> 66000.0
    """
    q = question.lower().replace(",", "")
    # Match patterns like 66000, 66k, $66000, 66000 usdt
    m = re.search(r'(\d{2,3})k\b', q)
    if m:
        return float(m.group(1)) * 1000
    m = re.search(r'\$?(\d{4,6})(?:\s*(?:usdt|usd))?', q)
    if m:
        val = float(m.group(1))
        if val >= 10000:  # reasonable BTC price
            return val
    return None


def _is_weekend_or_monday_early() -> bool:
    """
    Return True if current time is Saturday, Sunday, or Monday before 12:00 UTC.
    This is when BTC-to-altcoin weekend lag is most exploitable.
    """
    now = datetime.now(timezone.utc)
    weekday = now.weekday()  # 0=Mon, 5=Sat, 6=Sun
    if weekday in (5, 6):
        return True
    if weekday == 0 and now.hour < 12:
        return True
    return False


# ---------------------------------------------------------------------------
# BTC weekend drift calculation
# ---------------------------------------------------------------------------

def compute_btc_drift(btc_markets: list) -> tuple[str, float]:
    """
    Calculate BTC "weekend drift" direction from the threshold ladder.

    If higher thresholds are getting more likely (P increases with threshold),
    that is bullish drift. If lower thresholds are getting MORE likely relative
    to higher ones, that is bearish.

    We look at the weighted average probability across the threshold ladder.
    A high weighted average = bullish; low = bearish.

    Returns (direction, drift_magnitude).
    direction: "bullish", "bearish", or "neutral"
    drift_magnitude: 0.0 to 1.0 (how strong the drift is)
    """
    if not btc_markets:
        return "neutral", 0.0

    # Extract (threshold, probability) pairs
    ladder = []
    for m in btc_markets:
        threshold = _extract_btc_threshold(m.question)
        if threshold is not None:
            ladder.append((threshold, float(m.current_probability)))

    if len(ladder) < 2:
        return "neutral", 0.0

    # Sort by threshold ascending
    ladder.sort(key=lambda x: x[0])

    # In a neutral/random market, probabilities should decrease monotonically
    # with higher thresholds. The "drift" measures how much the actual
    # probability curve deviates from this expectation.
    #
    # Bullish drift: higher thresholds have HIGHER probability than expected
    # (the ladder is "flatter" than it should be -- market expects upward move)
    #
    # Bearish drift: lower thresholds have HIGHER probability than expected
    # (the ladder is "steeper" -- market expects downward or sideways)

    # Simple metric: average probability across all thresholds
    avg_p = sum(p for _, p in ladder) / len(ladder)

    # If avg_p > 0.5, the market is broadly bullish (most thresholds likely to hit)
    # If avg_p < 0.5, broadly bearish
    # Drift = distance from 0.5
    drift = avg_p - 0.5

    if drift > DRIFT_THRESHOLD / 2:
        return "bullish", min(1.0, abs(drift) * 2)
    elif drift < -(DRIFT_THRESHOLD / 2):
        return "bearish", min(1.0, abs(drift) * 2)

    # Also check slope: are higher thresholds gaining probability?
    # Compute simple slope across the ladder
    if len(ladder) >= 3:
        low_avg = sum(p for _, p in ladder[:len(ladder)//2]) / max(1, len(ladder)//2)
        high_avg = sum(p for _, p in ladder[len(ladder)//2:]) / max(1, len(ladder) - len(ladder)//2)
        slope_signal = high_avg - low_avg  # positive = bullish (higher thresholds gaining)

        if slope_signal > DRIFT_THRESHOLD:
            return "bullish", min(1.0, slope_signal * 2)
        elif slope_signal < -DRIFT_THRESHOLD:
            return "bearish", min(1.0, abs(slope_signal) * 2)

    return "neutral", abs(drift)


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market, drift_dir: str = "neutral",
                   drift_magnitude: float = 0.0) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md, adjusted by BTC weekend drift
    direction and magnitude. Only trades altcoin Up/Down markets when
    BTC drift is strong enough AND altcoin is still neutral (~50%).
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

    # Must be an altcoin Up/Down market
    if not _is_altcoin_updown_market(q):
        return None, 0, "Not an altcoin Up/Down market"

    # Weekend/Monday gate
    if not _is_weekend_or_monday_early():
        return None, 0, "Not weekend or Monday early -- edge not active"

    # Drift gate
    if drift_dir == "neutral" or drift_magnitude < DRIFT_THRESHOLD:
        return None, 0, (
            f"BTC drift too weak: {drift_dir} mag={drift_magnitude:.2f} "
            f"< {DRIFT_THRESHOLD:.2f}"
        )

    # BTC bullish drift + altcoin still neutral/low -> buy YES on altcoin
    if drift_dir == "bullish" and p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by drift magnitude (stronger drift = more confident)
        conviction = min(1.0, conviction * (1 + drift_magnitude))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} BTC={drift_dir}({drift_magnitude:.2f}) "
            f"size=${size} -- {q[:55]}"
        )

    # BTC bearish drift + altcoin still high -> sell NO on altcoin
    if drift_dir == "bearish" and p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, conviction * (1 + drift_magnitude))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO YES={p:.0%} edge={edge:.0%} BTC={drift_dir}({drift_magnitude:.2f}) "
            f"size=${size} -- {q[:55]}"
        )

    # BTC bullish but altcoin already priced in, or bearish but altcoin already low
    return None, 0, (
        f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands) "
        f"drift={drift_dir}({drift_magnitude:.2f})"
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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """
    Find active BTC threshold and altcoin Up/Down markets via keyword search
    + bulk fetch fallback, deduplicated.
    """
    seen: set[str] = set()
    unique: list = []

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if _is_btc_threshold_market(q) or _is_altcoin_updown_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback -- primary discovery
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if _is_btc_threshold_market(q) or _is_altcoin_updown_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[macro-weekend-momentum] mode={mode} max_pos=${MAX_POSITION} "
        f"drift_threshold={DRIFT_THRESHOLD}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[macro-weekend-momentum] {len(markets)} candidate markets")

    # Separate BTC threshold markets from altcoin Up/Down markets
    btc_markets = []
    alt_markets = []
    for m in markets:
        q = getattr(m, "question", "")
        if _is_btc_threshold_market(q):
            btc_markets.append(m)
        if _is_altcoin_updown_market(q):
            alt_markets.append(m)

    safe_print(
        f"[macro-weekend-momentum] {len(btc_markets)} BTC threshold markets, "
        f"{len(alt_markets)} altcoin Up/Down markets"
    )

    # Compute BTC weekend drift
    drift_dir, drift_mag = compute_btc_drift(btc_markets)
    safe_print(f"[macro-weekend-momentum] BTC drift: {drift_dir} magnitude={drift_mag:.3f}")

    if drift_dir == "neutral" or drift_mag < DRIFT_THRESHOLD:
        safe_print(
            f"[macro-weekend-momentum] BTC drift too weak ({drift_mag:.3f} < "
            f"{DRIFT_THRESHOLD}). No trades."
        )
        return

    # Trade altcoin markets that haven't caught up to BTC drift
    placed = 0
    for m in alt_markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, drift_dir, drift_mag)
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

    safe_print(f"[macro-weekend-momentum] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades altcoin Up/Down markets based on BTC weekend price "
            "threshold momentum drift. Altcoins lag BTC by 6-24 hours on weekends."
        )
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
