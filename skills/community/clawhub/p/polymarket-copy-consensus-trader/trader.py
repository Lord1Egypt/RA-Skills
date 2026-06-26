"""
polymarket-copy-consensus-trader
Only trades Polymarket markets where 3+ tracked whale wallets independently
agree on direction. Fetches the public leaderboard to identify top wallets,
pulls each wallet's recent activity from the Polymarket data API, then builds
a consensus map aggregating net positions across all wallets per market.

Core edge: A single whale can be wrong or manipulating. When multiple
independent smart-money wallets all bet the same direction on the same market,
the probability of all of them being wrong drops sharply. This consensus
filter eliminates noisy single-wallet signals and focuses capital on the
highest-conviction setups. Conviction-boosted sizing scales with the number
of agreeing whales beyond the minimum threshold.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import argparse
import json
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-copy-consensus-trader"
SKILL_SLUG   = "polymarket-copy-consensus-trader"

# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# ---------------------------------------------------------------------------
# Risk parameters -- declared as tunables in clawhub.json
# ---------------------------------------------------------------------------
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "50"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "5000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.08"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "5"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "8"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))

# ---------------------------------------------------------------------------
# Skill-specific parameters
# ---------------------------------------------------------------------------
MIN_CONSENSUS      = int(os.environ.get(  "SIMMER_MIN_CONSENSUS",      "3"))
CONSENSUS_BOOST    = float(os.environ.get("SIMMER_CONSENSUS_BOOST",    "0.20"))
LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", "20"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Flush-safe print for cron/daemon environments (handles Windows cp1252)."""
    try:
        print(*args, **kwargs, flush=True)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        print(text.encode("ascii", "replace").decode(), flush=True)


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global MIN_CONSENSUS, CONSENSUS_BOOST, LEADERBOARD_LIMIT
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
        MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",       str(MAX_POSITION)))
        MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",         str(MIN_VOLUME)))
        MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",         str(MAX_SPREAD)))
        MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",           str(MIN_DAYS)))
        MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      str(MAX_POSITIONS)))
        YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",      str(YES_THRESHOLD)))
        NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",       str(NO_THRESHOLD)))
        MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",          str(MIN_TRADE)))
        MIN_CONSENSUS      = int(os.environ.get(  "SIMMER_MIN_CONSENSUS",      str(MIN_CONSENSUS)))
        CONSENSUS_BOOST    = float(os.environ.get("SIMMER_CONSENSUS_BOOST",    str(CONSENSUS_BOOST)))
        LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",  str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: int = 15) -> dict | list | None:
    """Simple stdlib JSON GET request."""
    try:
        req = Request(url, headers={"User-Agent": "simmer-consensus-trader/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as exc:
        safe_print(f"  [WARN] HTTP GET failed: {url} -> {exc}")
        return None


# ---------------------------------------------------------------------------
# Leaderboard fetching
# ---------------------------------------------------------------------------

def fetch_leaderboard(limit: int = 20) -> list[dict]:
    """Fetch top traders from predicting.top leaderboard API."""
    url = f"{LEADERBOARD_URL}?limit={limit}"
    data = _http_get_json(url)
    if data is None:
        safe_print("  [WARN] Leaderboard fetch returned None, using empty list")
        return []
    # API may return {"traders": [...]} or a raw list
    if isinstance(data, dict):
        traders = data.get("traders", data.get("data", data.get("results", [])))
    elif isinstance(data, list):
        traders = data
    else:
        traders = []
    safe_print(f"  Fetched {len(traders)} traders from leaderboard")
    return traders[:limit]


# ---------------------------------------------------------------------------
# Wallet activity fetching
# ---------------------------------------------------------------------------

def fetch_wallet_activity(wallet: str, limit: int = 80) -> list[dict]:
    """Fetch recent trades for a wallet from Polymarket data API (public, no auth)."""
    url = f"{DATA_API}/activity?user={wallet.lower()}&limit={limit}"
    data = _http_get_json(url, timeout=20)
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("history", data.get("data", []))


# ---------------------------------------------------------------------------
# Consensus map building
# ---------------------------------------------------------------------------

def build_consensus_map(all_wallet_activities: dict[str, list[dict]]) -> dict[str, dict]:
    """Build consensus map from all wallet activities.

    For each wallet's activities, extract net YES vs NO per market title.
    Aggregate across wallets:
        market_title -> {
            yes_wallets: set(), no_wallets: set(),
            yes_volume: float, no_volume: float
        }

    Returns the consensus map.
    """
    consensus: dict[str, dict] = {}

    for wallet, activities in all_wallet_activities.items():
        if not activities:
            continue

        # Per-wallet: aggregate net position per market
        wallet_positions: dict[str, dict] = {}
        for act in activities:
            action = act.get("action", act.get("side", "")).lower()
            title = act.get("title", act.get("question", ""))
            outcome = act.get("outcome", act.get("asset", "")).lower()
            size = float(act.get("usdcSize", act.get("size", act.get("amount", 0))))

            if not title or outcome not in ("yes", "no"):
                continue
            if "buy" not in action and "long" not in action:
                continue

            key = title.strip()[:80]
            if key not in wallet_positions:
                wallet_positions[key] = {"yes_vol": 0.0, "no_vol": 0.0}
            wallet_positions[key][f"{outcome}_vol"] += size

        # Determine net direction per market for this wallet
        for market_title, vols in wallet_positions.items():
            if vols["yes_vol"] <= 0 and vols["no_vol"] <= 0:
                continue

            norm_key = market_title.strip().lower()
            if norm_key not in consensus:
                consensus[norm_key] = {
                    "yes_wallets": set(),
                    "no_wallets": set(),
                    "yes_volume": 0.0,
                    "no_volume": 0.0,
                    "display_title": market_title,
                }

            if vols["yes_vol"] > vols["no_vol"]:
                consensus[norm_key]["yes_wallets"].add(wallet)
                consensus[norm_key]["yes_volume"] += vols["yes_vol"]
            elif vols["no_vol"] > vols["yes_vol"]:
                consensus[norm_key]["no_wallets"].add(wallet)
                consensus[norm_key]["no_volume"] += vols["no_vol"]

    return consensus


# ---------------------------------------------------------------------------
# Consensus signal extraction
# ---------------------------------------------------------------------------

def find_consensus_signals(
    consensus_map: dict[str, dict],
    min_consensus: int,
) -> list[tuple[str, str, int, float, int]]:
    """Filter consensus map to markets with strong multi-wallet agreement.

    Returns list of (market_keyword, consensus_side, wallet_count, total_volume, opposing_count)
    sorted by wallet_count desc, then volume desc.
    """
    signals = []

    for norm_key, info in consensus_map.items():
        yes_count = len(info["yes_wallets"])
        no_count = len(info["no_wallets"])
        majority_count = max(yes_count, no_count)
        minority_count = min(yes_count, no_count)

        if majority_count < min_consensus:
            continue

        # Clean consensus: no opposition or opposition < consensus / 2
        if minority_count > 0 and minority_count >= majority_count / 2:
            continue

        if yes_count >= no_count:
            consensus_side = "yes"
            wallet_count = yes_count
            total_volume = info["yes_volume"]
            opposing = no_count
        else:
            consensus_side = "no"
            wallet_count = no_count
            total_volume = info["no_volume"]
            opposing = yes_count

        display = info.get("display_title", norm_key)
        signals.append((display, consensus_side, wallet_count, total_volume, opposing))

    # Sort by wallet_count desc, then volume desc
    signals.sort(key=lambda x: (x[2], x[3]), reverse=True)
    return signals


# ---------------------------------------------------------------------------
# Market matching
# ---------------------------------------------------------------------------

def find_matching_market(client: SimmerClient, keyword: str):
    """Search simmer markets with progressive keyword matching.

    Tries the full keyword first, then progressively shorter fragments.
    Returns the first matching market or None.
    """
    words = keyword.split()

    # Try full phrase, then progressively shorter
    for length in range(len(words), max(1, len(words) // 3) - 1, -1):
        query = " ".join(words[:length])
        if len(query) < 4:
            continue
        try:
            results = client.find_markets(query)
            if results:
                # Pick the best match: prefer exact substring match in question
                for m in results:
                    q_lower = getattr(m, "question", "").lower()
                    if query.lower() in q_lower:
                        vol = getattr(m, "volume", 0) or 0
                        if float(vol) >= MIN_VOLUME:
                            return m
                # Fallback: return first with sufficient volume
                for m in results:
                    vol = getattr(m, "volume", 0) or 0
                    if float(vol) >= MIN_VOLUME:
                        return m
        except Exception as exc:
            safe_print(f"  [search] '{query[:30]}': {exc}")

    return None


# ---------------------------------------------------------------------------
# Signal logic (standard per CLAUDE.md)
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """Standard conviction-based signal per CLAUDE.md.

    Returns (side, size, reasoning) or (None, 0, skip_reason).
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


# ---------------------------------------------------------------------------
# Consensus-boosted signal
# ---------------------------------------------------------------------------

def compute_consensus_signal(
    market,
    consensus_side: str,
    wallet_count: int,
    min_consensus: int,
) -> tuple[str | None, float, str]:
    """Compute conviction-boosted signal when consensus aligns with market signal.

    Only trades if consensus_side matches compute_signal direction.
    Extra whales beyond min_consensus boost conviction.

    Returns (side, size, reasoning) or (None, 0, skip_reason).
    """
    side, base_size, reasoning = compute_signal(market)

    if side is None:
        return None, 0, reasoning

    if side != consensus_side:
        return None, 0, (
            f"Signal={side} but consensus={consensus_side} "
            f"({wallet_count} wallets) -- no alignment"
        )

    p = market.current_probability

    # Recompute base conviction
    if side == "yes":
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    else:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)

    # Consensus boost: extra whales beyond minimum
    extra_whales = wallet_count - min_consensus
    boost = min(0.5, extra_whales * CONSENSUS_BOOST)
    conviction = min(1.0, base_conviction * (1 + boost))
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    q = market.question
    consensus_reasoning = (
        f"CONSENSUS {side.upper()} {p:.0%} "
        f"wallets={wallet_count} boost={boost:.0%} "
        f"conviction={conviction:.0%} size=${size} -- {q[:60]}"
    )
    return side, size, consensus_reasoning


# ---------------------------------------------------------------------------
# Context check -- prevent flip-flop / slippage
# ---------------------------------------------------------------------------

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
    except Exception as exc:
        safe_print(f"  [ctx] {market_id}: {exc}")
    return True, "ok"


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"\n{'='*65}")
    safe_print(f"  Copy Consensus Trader [{mode}]")
    safe_print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    safe_print(f"  min_consensus={MIN_CONSENSUS} boost={CONSENSUS_BOOST} "
               f"max_pos=${MAX_POSITION}")
    safe_print(f"{'='*65}")

    client = get_client(live)

    # ----- Step 1: Fetch leaderboard -----
    safe_print(f"\n[1/5] Fetching top {LEADERBOARD_LIMIT} wallets from leaderboard...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    if not traders:
        safe_print("  No traders found on leaderboard. Exiting.")
        return

    # Extract wallet addresses
    wallets = []
    for t in traders:
        wallet = (
            t.get("address")
            or t.get("wallet")
            or t.get("id", "")
        )
        if wallet:
            wallets.append(str(wallet))

    if not wallets:
        safe_print("  No wallet addresses extracted. Exiting.")
        return

    safe_print(f"  Tracking {len(wallets)} wallets")

    # ----- Step 2: Fetch activity per wallet -----
    safe_print(f"\n[2/5] Fetching recent activity per wallet...")
    all_activities: dict[str, list[dict]] = {}
    for i, wallet in enumerate(wallets):
        safe_print(f"  [{i+1}/{len(wallets)}] {wallet[:12]}...", end=" ")
        activities = fetch_wallet_activity(wallet, limit=80)
        all_activities[wallet] = activities
        safe_print(f"{len(activities)} trades")

    # ----- Step 3: Build consensus map -----
    safe_print(f"\n[3/5] Building consensus map...")
    consensus_map = build_consensus_map(all_activities)
    safe_print(f"  {len(consensus_map)} unique markets tracked across all wallets")

    # ----- Step 4: Find consensus signals -----
    safe_print(f"\n[4/5] Finding consensus signals (min {MIN_CONSENSUS} wallets)...")
    signals = find_consensus_signals(consensus_map, MIN_CONSENSUS)
    safe_print(f"  {len(signals)} markets with {MIN_CONSENSUS}+ wallet consensus")

    if not signals:
        safe_print("\n  No consensus signals found. Done.")
        return

    # Print consensus dashboard
    safe_print(f"\n{'='*65}")
    safe_print(f"  CONSENSUS DASHBOARD ({len(signals)} signals)")
    safe_print(f"{'='*65}")
    safe_print(f"  {'Market':<40} | {'Dir':>3} | {'Wlt':>3} | {'Volume':>10} | {'Opp':>3}")
    safe_print(f"  {'-'*40}-+-{'-'*3}-+-{'-'*3}-+-{'-'*10}-+-{'-'*3}")
    for title, side, wcount, vol, opp in signals:
        safe_print(
            f"  {title[:40]:<40} | {side.upper():>3} | {wcount:>3} | "
            f"${vol:>9.0f} | {opp:>3}"
        )

    # ----- Step 5: Trade consensus signals -----
    safe_print(f"\n[5/5] Trading consensus signals...")
    placed = 0
    skipped = 0

    for title, consensus_side, wallet_count, total_volume, opposing in signals:
        if placed >= MAX_POSITIONS:
            safe_print(f"  [GATE] Max positions ({MAX_POSITIONS}) reached, stopping")
            break

        # Find matching Simmer market
        m = find_matching_market(client, title)
        if not m:
            safe_print(f"  [no-match] {title[:50]} -- no Simmer market found")
            skipped += 1
            continue

        # Compute consensus-boosted signal
        side, size, reasoning = compute_consensus_signal(
            m, consensus_side, wallet_count, MIN_CONSENSUS
        )
        if side is None:
            safe_print(f"  [skip] {reasoning}")
            skipped += 1
            continue

        # Context check
        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            skipped += 1
            continue

        # Execute trade
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
        except Exception as exc:
            safe_print(f"  [error] {m.id}: {exc}")
            skipped += 1

    # Summary
    safe_print(f"\n{'='*65}")
    safe_print(f"  SUMMARY")
    safe_print(f"{'='*65}")
    safe_print(f"  Wallets tracked:       {len(wallets)}")
    safe_print(f"  Markets in consensus:  {len(signals)}")
    safe_print(f"  Trades placed:         {placed}")
    safe_print(f"  Trades skipped:        {skipped}")
    safe_print(f"{'='*65}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Copy Consensus Trader -- trades only when 3+ whale wallets agree."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
