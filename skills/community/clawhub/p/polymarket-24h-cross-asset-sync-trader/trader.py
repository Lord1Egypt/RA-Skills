"""
polymarket-24h-cross-asset-sync-trader
Trades cross-asset correlation divergences in 5-minute crypto "Up or Down"
markets on Polymarket.

Core edge: Polymarket lists 5-minute "Up or Down" markets for BTC, ETH, SOL,
DOGE, XRP, BNB — often in the SAME time window. These assets are highly
correlated (BTC/ETH ~0.85, BTC/SOL ~0.75, etc.). When BTC shows "Up" at 55%
but ETH shows "Down" at 55% in the same 5-min window, that divergence almost
always corrects. Trade the lagging asset toward the leader.

This is analogous to pairs trading in equities: when correlated instruments
diverge, bet on mean-reversion of the spread.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
import statistics
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-24h-cross-asset-sync-trader"
SKILL_SLUG   = "polymarket-24h-cross-asset-sync-trader"

KEYWORDS = [
    "bitcoin", "ethereum", "solana", "dogecoin", "xrp", "bnb",
    "btc up or down", "eth up or down", "sol up or down",
    "doge up or down", "xrp up or down", "bnb up or down",
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "40"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "5000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.08"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "0"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "8"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))
MIN_DIVERGENCE  = float(os.environ.get("SIMMER_MIN_DIVERGENCE",  "0.04"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_DIVERGENCE
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
        MIN_DIVERGENCE  = float(os.environ.get("SIMMER_MIN_DIVERGENCE",  str(MIN_DIVERGENCE)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing — extract asset and time window from question text
# ---------------------------------------------------------------------------

_ASSETS = {
    "bitcoin": "BTC", "btc": "BTC",
    "ethereum": "ETH", "eth": "ETH", "ether": "ETH",
    "solana": "SOL", "sol": "SOL",
    "dogecoin": "DOGE", "doge": "DOGE",
    "xrp": "XRP", "ripple": "XRP",
    "bnb": "BNB", "binance coin": "BNB",
}

# Matches: "March 28, 4:05AM-4:10AM ET" or "March 28, 4:05 AM - 4:10 AM ET"
_WINDOW_PATTERN = re.compile(
    r"((?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2})"                              # date: "March 28"
    r",?\s*"
    r"(\d{1,2}:\d{2}\s*(?:AM|PM))"             # start time: "4:05AM"
    r"\s*[-\u2013]\s*"
    r"(\d{1,2}:\d{2}\s*(?:AM|PM))",            # end time: "4:10AM"
    re.I,
)

# Matches: "Up or Down" direction questions
_UP_DOWN_PATTERN = re.compile(
    r"\b(up|down)\b.*\bor\b.*\b(up|down)\b",
    re.I,
)


def parse_asset(question: str) -> str | None:
    """Extract the crypto asset ticker from a question."""
    q = question.lower()
    for keyword, asset in _ASSETS.items():
        if keyword in q:
            return asset
    return None


def parse_window(question: str) -> str | None:
    """Extract the time window key (date + start-end) from a question."""
    m = _WINDOW_PATTERN.search(question)
    if m:
        date_str = m.group(1).strip().lower()
        start = m.group(2).strip().upper().replace(" ", "")
        end = m.group(3).strip().upper().replace(" ", "")
        return f"{date_str}|{start}-{end}"
    return None


def is_up_or_down(question: str) -> bool:
    """Check if question is an 'Up or Down' market."""
    return bool(_UP_DOWN_PATTERN.search(question))


def infer_direction(question: str, probability: float) -> str:
    """
    For 'Up or Down' markets, determine whether the market leans Up or Down.
    If probability > 0.50, the market favors the 'Up' outcome (YES = Up).
    If probability < 0.50, it favors 'Down'.
    """
    q = question.lower()
    # Most Polymarket "Up or Down" markets: YES = Up, NO = Down
    # If the question is phrased as "X Up or Down", YES generally = Up
    if "up" in q and q.index("up") < q.index("down") if "down" in q else True:
        # YES = Up: high p means market thinks Up
        return "up" if probability >= 0.50 else "down"
    # Fallback: treat YES = Up
    return "up" if probability >= 0.50 else "down"


# ---------------------------------------------------------------------------
# Window grouping and divergence detection
# ---------------------------------------------------------------------------

class WindowEntry:
    """One market in a time window."""
    __slots__ = ("market", "asset", "window_key", "probability", "direction", "up_probability")

    def __init__(self, market, asset, window_key, probability, direction, up_probability):
        self.market = market
        self.asset = asset
        self.window_key = window_key
        self.probability = probability
        self.direction = direction
        self.up_probability = up_probability  # normalized: how much the market thinks "Up"


def build_window_groups(markets: list) -> dict[str, list[WindowEntry]]:
    """Group 'Up or Down' markets by their time window."""
    groups: dict[str, list[WindowEntry]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue
        p = float(p)

        if not is_up_or_down(q):
            continue

        asset = parse_asset(q)
        window_key = parse_window(q)
        if not asset or not window_key:
            continue

        direction = infer_direction(q, p)
        # Normalize to "up probability" for comparison across assets
        up_prob = p if direction == "up" or p >= 0.50 else 1.0 - p

        entry = WindowEntry(m, asset, window_key, p, direction, up_prob)
        groups.setdefault(window_key, []).append(entry)

    return groups


def find_divergences(group: list[WindowEntry]) -> list[tuple]:
    """
    Find the most divergent asset in a time-window group.
    Returns list of (market, implied_side, deviation, reasoning).

    The consensus direction is determined by the group mean of up_probability.
    An asset diverging from this consensus is a trading opportunity.
    """
    if len(group) < 2:
        return []

    # Deduplicate by asset — keep only one market per asset per window
    by_asset: dict[str, WindowEntry] = {}
    for entry in group:
        if entry.asset not in by_asset:
            by_asset[entry.asset] = entry

    if len(by_asset) < 2:
        return []

    entries = list(by_asset.values())
    up_probs = [e.up_probability for e in entries]
    mean_up = statistics.mean(up_probs)

    opportunities = []
    for entry in entries:
        deviation = abs(entry.up_probability - mean_up)
        if deviation < MIN_DIVERGENCE:
            continue

        # Determine which way to trade the outlier: push it toward the consensus
        consensus_dir = "up" if mean_up >= 0.50 else "down"

        if entry.direction != consensus_dir:
            # This asset diverges from consensus — trade it toward consensus
            # If consensus is "up" but this asset says "down" (low p):
            #   We want to buy YES (betting it will go Up like the others)
            # If consensus is "down" but this asset says "up" (high p):
            #   We want to buy NO (betting it will go Down like the others)
            if consensus_dir == "up":
                side = "yes"
                reasoning = (
                    f"SYNC: {entry.asset} says Down ({entry.probability:.0%}) but "
                    f"group mean={mean_up:.0%} Up | dev={deviation:.0%} — "
                    f"{entry.market.question[:60]}"
                )
            else:
                side = "no"
                reasoning = (
                    f"SYNC: {entry.asset} says Up ({entry.probability:.0%}) but "
                    f"group mean={mean_up:.0%} Down | dev={deviation:.0%} — "
                    f"{entry.market.question[:60]}"
                )
            opportunities.append((entry.market, side, deviation, reasoning))
        else:
            # Same direction as consensus but magnitude differs significantly
            if entry.up_probability < mean_up:
                # Under-confident in Up vs consensus → buy YES
                side = "yes"
                reasoning = (
                    f"SYNC: {entry.asset} under-confident Up ({entry.up_probability:.0%} vs "
                    f"mean={mean_up:.0%}) | dev={deviation:.0%} — "
                    f"{entry.market.question[:60]}"
                )
            else:
                # Over-confident in Up vs consensus → sell NO
                side = "no"
                reasoning = (
                    f"SYNC: {entry.asset} over-confident Up ({entry.up_probability:.0%} vs "
                    f"mean={mean_up:.0%}) | dev={deviation:.0%} — "
                    f"{entry.market.question[:60]}"
                )
            opportunities.append((entry.market, side, deviation, reasoning))

    return opportunities


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


def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the cross-asset divergence.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No cross-asset divergence found"

    _, side, deviation, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by divergence magnitude
        div_boost = min(1.0, (deviation - MIN_DIVERGENCE) / max(0.01, YES_THRESHOLD))
        combined = min(1.0, max(conviction, div_boost))
        size = max(MIN_TRADE, round(combined * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # Boost conviction by divergence magnitude
        div_boost = min(1.0, (deviation - MIN_DIVERGENCE) / max(0.01, 1 - NO_THRESHOLD))
        combined = min(1.0, max(conviction, div_boost))
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


def find_markets(client: SimmerClient) -> list:
    """Find active crypto 'Up or Down' markets, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    # Only keep "Up or Down" markets
                    if "up" in q and "down" in q:
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[cross-asset-sync] mode={mode} max_pos=${MAX_POSITION} min_div={MIN_DIVERGENCE:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[cross-asset-sync] {len(markets)} candidate 'Up or Down' markets")

    # Group by time window
    groups = build_window_groups(markets)
    print(f"[cross-asset-sync] {len(groups)} time windows: " +
          ", ".join(f"{k}({len(v)} assets)" for k, v in groups.items()))

    # Log each window's composition
    for window_key, entries in groups.items():
        assets_str = ", ".join(
            f"{e.asset}={'Up' if e.direction == 'up' else 'Down'}@{e.probability:.0%}"
            for e in entries
        )
        print(f"  [{window_key}] {assets_str}")

    # Find divergences across all windows
    all_opps: dict[str, tuple] = {}
    for window_key, entries in groups.items():
        if len(entries) < 2:
            continue
        divergences = find_divergences(entries)
        for market, side, dev, reason in divergences:
            mid = getattr(market, "id", None)
            if not mid:
                continue
            existing = all_opps.get(mid)
            if existing is None or dev > existing[2]:
                all_opps[mid] = (market, side, dev, reason)

    print(f"[cross-asset-sync] {len(all_opps)} divergence opportunities")

    # Execute trades on best divergences
    placed = 0
    for market_id, opp in sorted(all_opps.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        side, size, reasoning = compute_signal(market, opp)
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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {market_id}: {e}")

    print(f"[cross-asset-sync] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades cross-asset correlation divergences in 5-min crypto markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
