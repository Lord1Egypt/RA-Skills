"""
polymarket-whale-scanner-trader
Fetches top-performing Polymarket traders from the public predicting.top
leaderboard API, scores them by SmartScore metrics (winRate, sharpeRatio,
profitFactor), and trades the markets where the highest-rated whales have
high-conviction positions. Builds a whale consensus map and only trades
when whale direction aligns with the conviction-based signal.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
import json
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-whale-scanner-trader"
SKILL_SLUG   = "polymarket-whale-scanner-trader"

# Broad keywords for market discovery
KEYWORDS = [
    "crypto", "bitcoin", "ethereum", "trump", "biden", "election",
    "president", "fed", "inflation", "recession", "war", "nato",
    "ai", "openai", "sports", "nba", "nfl", "soccer", "ufc",
    "climate", "hurricane", "pandemic", "supreme court", "congress",
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
MIN_SMART_SCORE    = float(os.environ.get("SIMMER_MIN_SMART_SCORE",    "70"))
MIN_WIN_RATE       = float(os.environ.get("SIMMER_MIN_WIN_RATE",       "0.55"))
LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", "20"))

_client: SimmerClient | None = None

# Public APIs
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API = "https://data-api.polymarket.com"


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
    global MIN_SMART_SCORE, MIN_WIN_RATE, LEADERBOARD_LIMIT
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
        except (AttributeError, Exception):
            pass  # apply_skill_config only available in Simmer runtime
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        MIN_SMART_SCORE    = float(os.environ.get("SIMMER_MIN_SMART_SCORE",    str(MIN_SMART_SCORE)))
        MIN_WIN_RATE       = float(os.environ.get("SIMMER_MIN_WIN_RATE",       str(MIN_WIN_RATE)))
        LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# Leaderboard and whale activity
# ---------------------------------------------------------------------------

def fetch_leaderboard(limit=20):
    """Fetch top traders from predicting.top"""
    req = Request(LEADERBOARD_URL, headers={"User-Agent": "SimmerSDK/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        # data is a list of trader objects with: wallet, name, stats.pnl, smartScore.score, smartScore.winRate, etc.
        traders = data if isinstance(data, list) else data.get("traders", data.get("data", []))
        return traders[:limit]
    except Exception as e:
        safe_print(f"[leaderboard] fetch error: {e}")
        return []


def score_trader(trader):
    """Extract SmartScore metrics, return (wallet, score, win_rate, tier)"""
    ss = trader.get("smartScore", {})
    score = ss.get("score", 0)
    win_rate = ss.get("winRate", 0)
    tier = ss.get("tier", "Unknown")
    wallet = trader.get("wallet", "")
    return wallet, score, win_rate, tier


def fetch_wallet_activity(wallet, limit=50):
    """Fetch recent trades for a wallet from Polymarket data API (public, no auth)"""
    url = f"{DATA_API}/activity?user={wallet.lower()}&limit={limit}"
    req = Request(url, headers={"User-Agent": "SimmerSDK/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        safe_print(f"[activity] {wallet[:10]}...: {e}")
        return []


def extract_whale_markets(activities):
    """
    Extract market IDs and directions from whale activity.
    Returns list of (market_title_fragment, side, size).
    """
    positions = {}
    for a in activities:
        action = a.get("action", a.get("side", "")).lower()
        title = a.get("title", "")
        size = float(a.get("usdcSize", a.get("size", 0)))
        outcome = a.get("outcome", "").lower()
        if "buy" in action and outcome in ("yes", "no"):
            key = title[:60]
            if key not in positions:
                positions[key] = {"yes_size": 0, "no_size": 0}
            positions[key][f"{outcome}_size"] += size
    # Return net direction per market
    result = []
    for title, sizes in positions.items():
        if sizes["yes_size"] > sizes["no_size"]:
            result.append((title, "yes", sizes["yes_size"]))
        elif sizes["no_size"] > sizes["yes_size"]:
            result.append((title, "no", sizes["no_size"]))
    return sorted(result, key=lambda x: x[2], reverse=True)


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
    Discover markets via keyword search with bulk fallback.
    Returns deduplicated list of all found markets.
    """
    seen: set[str] = set()
    unique: list = []

    # Keyword search across broad categories
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] '{kw}': {e}")

    # Fallback: bulk fetch if keyword search found few
    if len(unique) < 20:
        try:
            for m in client.get_markets(limit=200):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[bulk-fetch] {e}")

    return unique


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[whale-scanner] mode={mode} max_pos=${MAX_POSITION} "
        f"min_score={MIN_SMART_SCORE} min_wr={MIN_WIN_RATE}"
    )

    client = get_client(live=live)

    # Step 1: Fetch leaderboard and filter by SmartScore + win rate
    safe_print(f"[whale-scanner] fetching top {LEADERBOARD_LIMIT} traders from leaderboard...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    safe_print(f"[whale-scanner] {len(traders)} traders fetched")

    qualifying_whales = []
    for t in traders:
        wallet, score, win_rate, tier = score_trader(t)
        if not wallet:
            continue
        if score < MIN_SMART_SCORE:
            safe_print(f"  [skip] {wallet[:10]}... score={score:.0f} < {MIN_SMART_SCORE:.0f}")
            continue
        if win_rate < MIN_WIN_RATE:
            safe_print(f"  [skip] {wallet[:10]}... wr={win_rate:.0%} < {MIN_WIN_RATE:.0%}")
            continue
        name = t.get("name", wallet[:12])
        safe_print(f"  [whale] {name} score={score:.0f} wr={win_rate:.0%} tier={tier}")
        qualifying_whales.append((wallet, score, win_rate, tier, name))

    if not qualifying_whales:
        safe_print("[whale-scanner] no qualifying whales found. done.")
        return

    # Step 2: For each qualifying whale, fetch activity and extract positions
    # Build whale consensus: keyword -> {yes_votes, no_votes, total_size, titles}
    whale_consensus: dict[str, dict] = {}

    for wallet, score, win_rate, tier, name in qualifying_whales:
        activities = fetch_wallet_activity(wallet)
        if not activities:
            safe_print(f"  [activity] {name}: no recent activity")
            continue

        whale_markets = extract_whale_markets(activities)
        safe_print(f"  [activity] {name}: {len(whale_markets)} net positions from {len(activities)} trades")

        for title_fragment, side, usd_size in whale_markets[:10]:  # Top 10 positions per whale
            # Use the title fragment as consensus key
            key = title_fragment.strip().lower()
            if not key:
                continue
            if key not in whale_consensus:
                whale_consensus[key] = {
                    "yes_votes": 0,
                    "no_votes": 0,
                    "total_size": 0,
                    "titles": set(),
                    "whales": [],
                }
            if side == "yes":
                whale_consensus[key]["yes_votes"] += 1
            else:
                whale_consensus[key]["no_votes"] += 1
            whale_consensus[key]["total_size"] += usd_size
            whale_consensus[key]["titles"].add(title_fragment)
            whale_consensus[key]["whales"].append(name)

    safe_print(f"[whale-scanner] {len(whale_consensus)} unique market positions across whales")

    if not whale_consensus:
        safe_print("[whale-scanner] no whale positions found. done.")
        return

    # Step 3: Discover Simmer markets
    markets = find_markets(client)
    safe_print(f"[whale-scanner] {len(markets)} Simmer markets discovered")

    # Build a lookup: lowercase question fragment -> market object
    market_lookup: dict[str, list] = {}
    for m in markets:
        q = getattr(m, "question", "")
        if q:
            market_lookup.setdefault(q.lower(), []).append(m)

    # Step 4: Match whale consensus to Simmer markets and trade
    placed = 0

    # Sort consensus by total_size descending (strongest whale conviction first)
    sorted_consensus = sorted(
        whale_consensus.items(),
        key=lambda x: x[1]["total_size"],
        reverse=True,
    )

    for consensus_key, info in sorted_consensus:
        if placed >= MAX_POSITIONS:
            break

        yes_votes = info["yes_votes"]
        no_votes = info["no_votes"]
        total_size = info["total_size"]
        whales = info["whales"]

        # Determine whale direction
        if yes_votes > no_votes:
            whale_side = "yes"
        elif no_votes > yes_votes:
            whale_side = "no"
        else:
            safe_print(f"  [skip] split consensus on: {consensus_key[:60]}")
            continue

        # Find matching Simmer market by substring matching
        matched_market = None
        for q_lower, mlist in market_lookup.items():
            # Check if any words from consensus key appear in market question
            consensus_words = [w for w in consensus_key.split() if len(w) > 3]
            if not consensus_words:
                continue
            matches = sum(1 for w in consensus_words if w in q_lower)
            if matches >= max(2, len(consensus_words) // 2):
                matched_market = mlist[0]
                break

        if not matched_market:
            safe_print(f"  [no-match] {consensus_key[:60]} -- no Simmer market found")
            continue

        # Step 5: Run compute_signal -- only trade if whale direction aligns
        side, size, reasoning = compute_signal(matched_market)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        if side != whale_side:
            safe_print(
                f"  [skip] signal={side} but whales={whale_side} on "
                f"{matched_market.question[:50]} -- no alignment"
            )
            continue

        # Whale-aligned trade: boost reasoning with whale info
        whale_names = ", ".join(set(whales))[:60]
        whale_reasoning = (
            f"WHALE-ALIGNED {reasoning} | "
            f"whales={yes_votes}Y/{no_votes}N ${total_size:.0f} by [{whale_names}]"
        )

        # Step 6: Context check
        ok, why = context_ok(client, matched_market.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        # Step 7: Execute trade
        try:
            r = client.trade(
                market_id=matched_market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=whale_reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {whale_reasoning[:120]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {matched_market.id}: {e}")

    safe_print(f"[whale-scanner] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Whale scanner trader -- follows top Polymarket whales by SmartScore."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
