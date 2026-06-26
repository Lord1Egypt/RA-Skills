"""
polymarket-candle-cross-asset-divergence-trader
Detects cross-asset divergence in Polymarket crypto 5-minute interval markets.
When normally correlated assets (BTC and ETH/SOL/XRP) show contradictory candle
directions in overlapping time windows, the divergence tends to close. The less
liquid coin converges toward BTC's direction.

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

TRADE_SOURCE = "sdk:polymarket-candle-cross-asset-divergence-trader"
SKILL_SLUG   = "polymarket-candle-cross-asset-divergence-trader"

KEYWORDS = [
    'Bitcoin Up or Down', 'Ethereum Up or Down',
    'Solana Up or Down', 'XRP Up or Down',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Divergence-specific tunables
DIV_THRESHOLD  = float(os.environ.get("SIMMER_DIV_THRESHOLD", "0.08"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, DIV_THRESHOLD
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
        DIV_THRESHOLD  = float(os.environ.get("SIMMER_DIV_THRESHOLD", str(DIV_THRESHOLD)))
    return _client


# ---------------------------------------------------------------------------
# Parsing: "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET"
# ---------------------------------------------------------------------------
_INTERVAL_RE = re.compile(
    r"^(BTC|Bitcoin|ETH|Ethereum|SOL|Solana|XRP)\s+Up or Down\s*[-\u2013]\s*"
    r"(.+?),\s*(\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*[-\u2013]\s*(\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*ET$",
    re.IGNORECASE,
)

_COIN_NORM = {
    "btc": "BTC", "bitcoin": "BTC",
    "eth": "ETH", "ethereum": "ETH",
    "sol": "SOL", "solana": "SOL",
    "xrp": "XRP",
}

# BTC is the leader; these coins are expected to converge toward BTC.
_FOLLOWER_COINS = {"ETH", "SOL", "XRP"}


def parse_interval(question: str):
    """
    Return (coin, date_str, start_minutes) or None.
    coin is normalised to BTC/ETH/SOL/XRP.
    """
    m = _INTERVAL_RE.match(question.strip())
    if not m:
        return None
    coin_raw, date_str, start, _end = m.groups()
    coin = _COIN_NORM.get(coin_raw.lower(), coin_raw.upper())
    return coin, date_str.strip(), _time_to_minutes(start.strip())


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM', '10:50AM', '1:05PM' to minutes since midnight."""
    t = t.upper().strip()
    am_pm = None
    if t.endswith("AM"):
        am_pm = "AM"
        t = t[:-2].strip()
    elif t.endswith("PM"):
        am_pm = "PM"
        t = t[:-2].strip()
    parts = t.split(":")
    h, m = int(parts[0]), int(parts[1])
    if am_pm == "PM" and h != 12:
        h += 12
    elif am_pm == "AM" and h == 12:
        h = 0
    return h * 60 + m


def _candle_direction(p: float) -> str:
    """Classify a market probability into UP / DOWN / NEUTRAL."""
    if p > 0.55:
        return "UP"
    if p < 0.45:
        return "DOWN"
    return "NEUTRAL"


# ---------------------------------------------------------------------------
# Cross-asset divergence detection
# ---------------------------------------------------------------------------

def detect_divergences(markets: list) -> list:
    """
    Group markets by (date, start_minutes) to find overlapping time windows.
    For each window with 2+ coins, compare BTC direction to follower coins.
    Return list of (follower_market, btc_direction, divergence_amount) where
    BTC and the follower show contradictory candle directions.
    """
    # Group by (date, time) -> {coin: market}
    windows: dict[tuple[str, int], dict[str, object]] = {}
    for m in markets:
        parsed = parse_interval(getattr(m, "question", ""))
        if not parsed:
            continue
        coin, date_str, start_min = parsed
        key = (date_str, start_min)
        windows.setdefault(key, {})[coin] = m

    divergence_targets = []

    for (date_str, start_min), coin_map in sorted(windows.items(), key=lambda x: x[0]):
        if "BTC" not in coin_map:
            continue
        if len(coin_map) < 2:
            continue

        btc_market = coin_map["BTC"]
        btc_p = btc_market.current_probability
        btc_dir = _candle_direction(btc_p)

        if btc_dir == "NEUTRAL":
            continue  # No clear BTC signal to diverge from

        for coin in _FOLLOWER_COINS:
            if coin not in coin_map:
                continue
            follower_market = coin_map[coin]
            follower_p = follower_market.current_probability
            follower_dir = _candle_direction(follower_p)

            if follower_dir == "NEUTRAL":
                continue
            if follower_dir == btc_dir:
                continue  # No divergence

            # Divergence detected: BTC and follower point in opposite directions
            divergence = abs(btc_p - follower_p)
            if divergence < DIV_THRESHOLD:
                continue  # Too small to be meaningful

            divergence_targets.append((follower_market, btc_dir, divergence, coin, btc_p, follower_p))

    return divergence_targets


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, btc_dir: str, divergence: float,
                   coin: str, btc_p: float, follower_p: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md. Trades the follower coin toward
    BTC's direction (convergence trade):
    - BTC UP + follower DOWN -> buy YES on follower (expect it to converge UP)
    - BTC DOWN + follower UP -> sell NO on follower (expect it to converge DOWN)
    """
    p = market.current_probability
    q = getattr(market, "question", "")

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

    if btc_dir == "UP":
        # BTC is UP, follower is DOWN -> buy YES on follower to converge UP
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"DIV {coin} vs BTC: BTC={btc_p:.0%}UP {coin}={follower_p:.0%}DOWN "
                f"div={divergence:.0%} YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:50]}"
            )
        return None, 0, (
            f"Divergence but {coin} already repriced ({p:.0%} > "
            f"YES_THRESHOLD={YES_THRESHOLD:.0%}) -- {q[:60]}"
        )

    if btc_dir == "DOWN":
        # BTC is DOWN, follower is UP -> sell NO on follower to converge DOWN
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"DIV {coin} vs BTC: BTC={btc_p:.0%}DOWN {coin}={follower_p:.0%}UP "
                f"div={divergence:.0%} NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:50]}"
            )
        return None, 0, (
            f"Divergence but {coin} already repriced ({p:.0%} < "
            f"NO_THRESHOLD={NO_THRESHOLD:.0%}) -- {q[:60]}"
        )

    return None, 0, f"Unknown BTC direction: {btc_dir}"


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """Find active crypto interval markets via keyword search + get_markets fallback."""
    seen, unique = set(), []

    # 1. Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # 2. Fallback: scan broad market list for interval matches
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            q = getattr(m, "question", "")
            if mid and mid not in seen and _INTERVAL_RE.match(q.strip()):
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] get_markets: {e}")

    return unique


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
        f"[cross-asset-div] mode={mode} max_pos=${MAX_POSITION} "
        f"div_thresh={DIV_THRESHOLD} "
        f"yes_thresh={YES_THRESHOLD} no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[cross-asset-div] {len(markets)} candidate interval markets")

    div_targets = detect_divergences(markets)
    safe_print(f"[cross-asset-div] {len(div_targets)} divergence opportunities detected")

    placed = 0
    for follower_mkt, btc_dir, divergence, coin, btc_p, follower_p in div_targets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(
            follower_mkt, btc_dir, divergence, coin, btc_p, follower_p
        )
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, follower_mkt.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=follower_mkt.id,
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
            safe_print(f"  [error] {follower_mkt.id}: {e}")

    safe_print(f"[cross-asset-div] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Detects cross-asset divergence in Polymarket crypto 5-min interval markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
