#!/usr/bin/env python3
"""
Kalshi FIFA Soccer Trader — Simmer SDK skill.
Uses EA FC OVR rating disparity + bivariate Poisson model to find edge
on Kalshi soccer markets: match winner, total goals, and goal spread.
"""

import os
import sys
import re
import json
import math
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Set

try:
    from simmer_sdk.skill import load_config, update_config
except ImportError:
    def load_config(schema, *args, **kwargs):
        out = {}
        for k, v in schema.items():
            env_val = os.environ.get(v["env"])
            out[k] = v["type"](env_val) if env_val else v["default"]
        return out
    def update_config(*args, **kwargs):
        pass

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CONFIG_SCHEMA = {
    "entry_edge":       {"env": "SIMMER_SOCCER_ENTRY_EDGE",        "default": 0.06,  "type": float},
    "exit_threshold":   {"env": "SIMMER_SOCCER_EXIT_THRESHOLD",     "default": 0.90,  "type": float},
    "max_position_usd": {"env": "SIMMER_SOCCER_MAX_POSITION_USD",   "default": 5.00,  "type": float},
    "sizing_pct":       {"env": "SIMMER_SOCCER_SIZING_PCT",         "default": 0.04,  "type": float},
    "max_trades":       {"env": "SIMMER_SOCCER_MAX_TRADES_PER_RUN", "default": 5,     "type": int},
    "market_types":     {"env": "SIMMER_SOCCER_MARKET_TYPES",       "default": "winner,totals,spread", "type": str},
    "min_liquidity":    {"env": "SIMMER_SOCCER_MIN_LIQUIDITY",      "default": 500,   "type": float},
    "slippage_max":     {"env": "SIMMER_SOCCER_SLIPPAGE_MAX",       "default": 0.10,  "type": float},
    "home_boost":       {"env": "SIMMER_SOCCER_HOME_BOOST",         "default": 0.12,  "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-fifa-soccer-trader")

TRADE_SOURCE = "sdk:kalshi-soccer"
SKILL_SLUG = "kalshi-fifa-soccer-trader"
RATINGS_PATH = Path(__file__).parent / "ratings.json"

# ---------------------------------------------------------------------------
# Client (lazy init, mirrors weather_trader pattern)
# ---------------------------------------------------------------------------

_client = None

def get_client(live: bool = False):
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY", "")
        if not api_key:
            print("Error: SIMMER_API_KEY not set. Get yours at simmer.markets/dashboard → SDK tab")
            sys.exit(1)
        _client = SimmerClient(api_key=api_key, venue="kalshi", live=live)
    return _client

# ---------------------------------------------------------------------------
# Bivariate Poisson model
# ---------------------------------------------------------------------------

MAX_GOALS = 10  # 0..9 goals per team in the grid
BASE_GOALS = 1.35  # baseline expected goals per team per game (top-flight average)
ALPHA = 0.022     # OVR-point sensitivity in log-scale

def _poisson_pmf(lam: float, k: int) -> float:
    if lam <= 0 or k < 0:
        return 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def ovr_to_lambdas(home_ovr: int, away_ovr: int, home_boost: float = 0.12) -> tuple:
    """Convert OVR disparity to (lambda_home, lambda_away)."""
    delta = home_ovr - away_ovr
    lam_home = BASE_GOALS * math.exp(ALPHA * delta + home_boost)
    lam_away = BASE_GOALS * math.exp(-ALPHA * delta)
    return round(lam_home, 4), round(lam_away, 4)

def build_goal_grid(lam_home: float, lam_away: float) -> list:
    """Return MAX_GOALS x MAX_GOALS joint probability grid P[i][j] = P(home=i, away=j)."""
    return [
        [_poisson_pmf(lam_home, i) * _poisson_pmf(lam_away, j) for j in range(MAX_GOALS)]
        for i in range(MAX_GOALS)
    ]

def compute_win_probs(grid: list) -> tuple:
    """Return (p_home_win, p_draw, p_away_win)."""
    p_home = p_draw = p_away = 0.0
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            p = grid[i][j]
            if i > j:
                p_home += p
            elif i == j:
                p_draw += p
            else:
                p_away += p
    return p_home, p_draw, p_away

def compute_over_prob(grid: list, line: float) -> float:
    """P(total goals > line). For half-goal lines (2.5, 3.5), returns P(>=ceil(line))."""
    p_over = 0.0
    threshold = math.ceil(line) if line != int(line) else int(line) + 1
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            if (i + j) >= threshold:
                p_over += grid[i][j]
    return p_over

def compute_spread_prob(grid: list, home_margin: int) -> float:
    """P(home wins by >= home_margin goals). home_margin > 0 = home favored."""
    p = 0.0
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            if (i - j) >= home_margin:
                p += grid[i][j]
    return p

# ---------------------------------------------------------------------------
# De-vig
# ---------------------------------------------------------------------------

def devig(price_yes: float, price_no: float) -> tuple:
    """De-vig YES/NO Kalshi prices to fair implied probability. Returns (fair_yes, fair_no)."""
    total = price_yes + price_no
    if total <= 0:
        return None, None
    return price_yes / total, price_no / total

def compute_edge(model_prob: float, fair_implied: float) -> float:
    """EV = model probability - fair implied probability."""
    return round(model_prob - fair_implied, 4)

# ---------------------------------------------------------------------------
# Ratings lookup + lineup intelligence
# ---------------------------------------------------------------------------

_ratings_cache: dict = {}
_ratings_data: list = []  # raw team list for lineup intel

# Lazy import of lineup_intel (optional — degrades gracefully if missing)
try:
    import lineup_intel as _lineup_intel
    _HAS_LINEUP_INTEL = True
except ImportError:
    _HAS_LINEUP_INTEL = False

def load_ratings() -> dict:
    global _ratings_cache, _ratings_data
    if _ratings_cache:
        return _ratings_cache
    if not RATINGS_PATH.exists():
        print(f"Warning: ratings.json not found at {RATINGS_PATH}")
        return {}
    with open(RATINGS_PATH) as f:
        data = json.load(f)
    _ratings_data = data.get("teams", [])
    for team in _ratings_data:
        # Prefer top11_avg_ovr (best starting XI average) over composite team OVR
        effective_ovr = team.get("top11_avg_ovr") or team["ovr"]
        primary = team["name"].lower()
        _ratings_cache[primary] = effective_ovr
        for alias in team.get("aliases", []):
            _ratings_cache[alias.lower()] = effective_ovr
    return _ratings_cache

def _resolve_team_name(cleaned: str) -> Optional[str]:
    """Return the canonical team name from ratings.json matching cleaned input."""
    load_ratings()
    for team in _ratings_data:
        if team["name"].lower() == cleaned:
            return team["name"]
        for alias in team.get("aliases", []):
            if alias.lower() == cleaned:
                return team["name"]
    # substring fallbacks
    for team in _ratings_data:
        if len(team["name"]) >= 4 and team["name"].lower() in cleaned:
            return team["name"]
        for alias in team.get("aliases", []):
            if len(alias) >= 4 and alias.lower() in cleaned:
                return team["name"]
    for team in _ratings_data:
        if len(cleaned) >= 4 and cleaned in team["name"].lower():
            return team["name"]
    return None

def lookup_team(name: str) -> Optional[float]:
    """
    Fuzzy-match a team name to its EA FC OVR (formation-aware if lineup_intel available).
    Returns None if no match.
    """
    ratings = load_ratings()
    cleaned = name.strip().lower()

    # Try lineup-intel first (formation-aware + injury adjustment)
    if _HAS_LINEUP_INTEL:
        canonical = _resolve_team_name(cleaned)
        if canonical:
            try:
                ovr, _signals = _lineup_intel.effective_lineup_ovr(canonical)
                return ovr
            except Exception:
                pass  # fall through to static lookup

    # Static fallback: exact → substring
    if cleaned in ratings:
        return ratings[cleaned]
    for key, ovr in ratings.items():
        if len(key) >= 4 and key in cleaned:
            return ovr
    for key, ovr in ratings.items():
        if len(cleaned) >= 4 and cleaned in key:
            return ovr
    return None

def lookup_team_with_signals(name: str) -> tuple:
    """
    Like lookup_team but also returns injury/lineup signals for logging.
    Returns (ovr, signals_list) where signals_list may be empty.
    """
    ratings = load_ratings()
    cleaned = name.strip().lower()

    if _HAS_LINEUP_INTEL:
        canonical = _resolve_team_name(cleaned)
        if canonical:
            try:
                ovr, signals = _lineup_intel.effective_lineup_ovr(canonical)
                return ovr, signals
            except Exception:
                pass

    if cleaned in ratings:
        return ratings[cleaned], []
    for key, ovr in ratings.items():
        if len(key) >= 4 and key in cleaned:
            return ovr, []
    for key, ovr in ratings.items():
        if len(cleaned) >= 4 and cleaned in key:
            return ovr, []
    return None, [f"⚠  Team not found in ratings: {name}"]

# ---------------------------------------------------------------------------
# Market type parsing
# ---------------------------------------------------------------------------

# Regex patterns to detect market type and extract relevant info from titles/questions
_WINNER_PATTERNS = [
    re.compile(r"will\s+(.+?)\s+(?:beat|defeat|win\s+(?:against|vs\.?|versus))\s+(.+?)[\?]?$", re.I),
    re.compile(r"(.+?)\s+(?:to\s+win|wins)\s+(?:vs\.?|versus|against)\s+(.+?)[\?]?$", re.I),
    re.compile(r"(.+?)\s+vs\.?\s+(.+?)[\s\-–:]+(?:match\s+)?(?:winner|result|moneyline)[\?]?", re.I),
]
_DRAW_PATTERNS = [
    re.compile(r"(.+?)\s+vs\.?\s+(.+?)[\s\-–:]+draw[\?]?", re.I),
    re.compile(r"will\s+(.+?)\s+vs\.?\s+(.+?)\s+end\s+in\s+(?:a\s+)?draw[\?]?", re.I),
]
_TOTALS_PATTERNS = [
    re.compile(r"(?:over|more\s+than)\s+([\d.]+)\s+goals?\s+(?:in\s+)?(.+?)\s+vs\.?\s+(.+?)[\?]?$", re.I),
    re.compile(r"(.+?)\s+vs\.?\s+(.+?)[\s\-–:]+(?:over|under|o/u|total)\s+([\d.]+)[\?]?", re.I),
    re.compile(r"will\s+(?:there\s+be\s+)?(?:more\s+than|over)\s+([\d.]+)\s+goals?\s+in\s+(.+?)\s+vs\.?\s+(.+?)[\?]?$", re.I),
    re.compile(r"total\s+goals\s+(?:over|under)\s+([\d.]+)\s+in\s+(.+?)\s+(?:vs\.?|versus)\s+(.+?)[\?]?$", re.I),
]
_SPREAD_PATTERNS = [
    re.compile(r"will\s+(.+?)\s+(?:win|beat)\s+(?:by|with)\s+(\d+)(?:\+|\s+or\s+more)?\s+(?:goals?)\s+(?:vs\.?|versus|against|in\s+(?:game|match)\s+with)\s+(.+?)[\?]?$", re.I),
    re.compile(r"(.+?)\s+(?:to\s+win|wins)\s+by\s+(\d+)(?:\+|\s+or\s+more)?\s+goals?\s+(?:vs\.?|versus|against)\s+(.+?)[\?]?$", re.I),
    re.compile(r"(.+?)\s+vs\.?\s+(.+?)[\s\-–:]+(?:handicap|spread|margin)[\s\(]+([+\-]?\d+)[\)]?[\?]?", re.I),
]

# Generic "team A vs team B" extractor as fallback
_VS_PATTERN = re.compile(r"(.+?)\s+vs\.?\s+(.+?)(?:\s*[\-–:,\?]|$)", re.I)

def _clean_team(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip(" ?,.-–")

def parse_market(market: dict, allowed_types: Set[str]) -> Optional[dict]:
    """
    Parse a Kalshi market dict and return structured signal info, or None if unrecognized.

    Returns:
        {
            "type": "winner" | "totals" | "spread",
            "home": str,
            "away": str,
            "side": "yes" | "no",    # which side our model probability corresponds to
            "line": float | None,     # for totals (e.g. 2.5) or spread (e.g. 2)
            "yes_price": float,
            "no_price": float,
        }
    """
    title = market.get("question") or market.get("title") or market.get("subtitle") or ""
    yes_price = (market.get("yes_ask") or market.get("yes_bid") or 0) / 100.0
    no_price  = (market.get("no_ask")  or market.get("no_bid")  or 0) / 100.0

    if yes_price <= 0 or no_price <= 0:
        return None

    # --- Draw market --------------------------------------------------
    if "draw" in allowed_types:
        for pat in _DRAW_PATTERNS:
            m = pat.search(title)
            if m:
                home, away = _clean_team(m.group(1)), _clean_team(m.group(2))
                return {"type": "draw", "home": home, "away": away, "side": "yes",
                        "line": None, "yes_price": yes_price, "no_price": no_price}

    # --- Totals -------------------------------------------------------
    if "totals" in allowed_types:
        for pat in _TOTALS_PATTERNS:
            m = pat.search(title)
            if m:
                groups = [g for g in m.groups() if g]
                # Extract the numeric line
                line_candidates = [g for g in groups if re.match(r"[\d.]+$", g)]
                team_candidates = [g for g in groups if not re.match(r"[\d.]+$", g)]
                if line_candidates and len(team_candidates) >= 2:
                    line = float(line_candidates[0])
                    home = _clean_team(team_candidates[0])
                    away = _clean_team(team_candidates[1])
                    return {"type": "totals", "home": home, "away": away, "side": "yes",
                            "line": line, "yes_price": yes_price, "no_price": no_price}

    # --- Spread / handicap --------------------------------------------
    if "spread" in allowed_types:
        for pat in _SPREAD_PATTERNS:
            m = pat.search(title)
            if m:
                groups = [_clean_team(g) for g in m.groups() if g]
                margin_candidates = [g for g in groups if re.match(r"[+\-]?\d+$", g)]
                team_candidates  = [g for g in groups if not re.match(r"[+\-]?\d+$", g)]
                if margin_candidates and len(team_candidates) >= 2:
                    margin = int(margin_candidates[0].lstrip("+"))
                    home = team_candidates[0]
                    away = team_candidates[1]
                    return {"type": "spread", "home": home, "away": away, "side": "yes",
                            "line": margin, "yes_price": yes_price, "no_price": no_price}

    # --- Match winner -------------------------------------------------
    if "winner" in allowed_types:
        for pat in _WINNER_PATTERNS:
            m = pat.search(title)
            if m:
                home, away = _clean_team(m.group(1)), _clean_team(m.group(2))
                return {"type": "winner", "home": home, "away": away, "side": "yes",
                        "line": None, "yes_price": yes_price, "no_price": no_price}
        # Generic vs pattern as last-resort for winner
        m = _VS_PATTERN.search(title)
        kw = title.lower()
        if m and any(w in kw for w in ("win", "beat", "defeat", "result", "moneyline")):
            home, away = _clean_team(m.group(1)), _clean_team(m.group(2))
            return {"type": "winner", "home": home, "away": away, "side": "yes",
                    "line": None, "yes_price": yes_price, "no_price": no_price}

    return None

# ---------------------------------------------------------------------------
# Model probability for a parsed market
# ---------------------------------------------------------------------------

def model_probability(parsed: dict, home_ovr: int, away_ovr: int, home_boost: float) -> Optional[float]:
    """
    Given a parsed market and team OVRs, return the model probability for the YES outcome.
    Returns None if market type is unrecognized.
    """
    lam_home, lam_away = ovr_to_lambdas(home_ovr, away_ovr, home_boost)
    grid = build_goal_grid(lam_home, lam_away)

    mtype = parsed["type"]
    if mtype == "winner":
        p_home, _, _ = compute_win_probs(grid)
        return p_home
    elif mtype == "draw":
        _, p_draw, _ = compute_win_probs(grid)
        return p_draw
    elif mtype == "totals":
        return compute_over_prob(grid, parsed["line"])
    elif mtype == "spread":
        return compute_spread_prob(grid, int(parsed["line"]))
    return None

# ---------------------------------------------------------------------------
# Market discovery and fetching (mirrors weather_trader)
# ---------------------------------------------------------------------------

SOCCER_SEARCH_TERMS = ["soccer", "football", "world cup", "UEFA", "EPL", "MLS", "champions league"]

def discover_and_import_soccer_markets(log=print) -> int:
    """Discover soccer markets on Kalshi and import them into Simmer."""
    client = get_client()
    imported = 0
    seen_urls = set()
    for term in SOCCER_SEARCH_TERMS:
        try:
            results = client.list_importable_markets(q=term, venue="kalshi", min_volume=500, limit=30)
            for m in results:
                url = m.get("url") or m.get("kalshi_url") or ""
                if not url or url in seen_urls:
                    continue
                if "kalshi.com" not in url:
                    continue
                seen_urls.add(url)
                try:
                    result = client.import_kalshi_market(url)
                    status = result.get("status") if isinstance(result, dict) else str(result)
                    if status == "imported":
                        imported += 1
                        log(f"  Imported: {url}")
                    else:
                        log(f"  Already tracked: {url}")
                except Exception as e:
                    log(f"  Import failed for {url}: {e}")
        except Exception as e:
            log(f"  Search failed for '{term}': {e}")
    log(f"Discovery complete. {imported} new markets imported.")
    return imported

def fetch_soccer_markets() -> list:
    """Fetch active Kalshi soccer markets from Simmer API."""
    client = get_client()
    markets = []
    for q in ["soccer", "football goals", "world cup winner"]:
        try:
            result = client._request("GET", "/api/sdk/markets", params={
                "status": "active",
                "import_source": "kalshi",
                "q": q,
                "limit": 100,
            })
            for m in result.get("markets", []):
                if m.get("id") not in {x.get("id") for x in markets}:
                    markets.append(m)
        except Exception as e:
            print(f"  Warning: market fetch failed for '{q}': {e}")
    return markets

# ---------------------------------------------------------------------------
# Safeguards (mirrors weather_trader)
# ---------------------------------------------------------------------------

def _time_to_resolution_hours(market: dict) -> float:
    """Return hours until market resolution, or 999 if unknown."""
    time_str = market.get("time_to_resolution") or market.get("close_time") or ""
    if not time_str:
        return 999.0
    try:
        if "T" in time_str:
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(time_str)
        now = datetime.now(timezone.utc)
        return (dt - now).total_seconds() / 3600.0
    except Exception:
        return 999.0

def check_safeguards(market: dict, parsed: dict, context: dict, cfg: dict) -> tuple:
    """Return (ok: bool, reasons: list[str])."""
    reasons = []

    # Time decay
    hours_left = _time_to_resolution_hours(market)
    min_hours = 1.0 if parsed["type"] == "totals" else 3.0
    if hours_left < min_hours:
        reasons.append(f"Time decay: {hours_left:.1f}h left (min {min_hours}h)")

    # Slippage
    slippage = context.get("slippage") or context.get("market", {}).get("slippage") or 0
    if slippage > cfg["slippage_max"]:
        reasons.append(f"Slippage {slippage:.1%} > max {cfg['slippage_max']:.1%}")

    # Liquidity
    liquidity = (
        context.get("market", {}).get("liquidity")
        or market.get("liquidity")
        or 0
    )
    if cfg["min_liquidity"] > 0 and liquidity < cfg["min_liquidity"]:
        reasons.append(f"Liquidity ${liquidity:.0f} < min ${cfg['min_liquidity']:.0f}")

    # Flip-flop
    flip = (
        context.get("flip_flop_warning")
        or context.get("market", {}).get("flip_flop_warning")
        or False
    )
    if flip:
        reasons.append("Flip-flop warning active")

    return len(reasons) == 0, reasons

# ---------------------------------------------------------------------------
# Trade execution (exact same pattern as weather_trader)
# ---------------------------------------------------------------------------

def get_portfolio() -> dict:
    try:
        return get_client().get_portfolio()
    except Exception:
        return {}

def get_position_size(cfg: dict, smart_sizing: bool = False) -> float:
    if not smart_sizing:
        return cfg["max_position_usd"]
    portfolio = get_portfolio()
    balance = portfolio.get("balance_usd") or portfolio.get("usdc_balance") or 0
    sized = balance * cfg["sizing_pct"]
    return min(sized, cfg["max_position_usd"])

def execute_trade(
    market_id: str,
    side: str,
    amount: float,
    reasoning: str = "",
    signal_data: dict = None,
    live: bool = False,
) -> dict:
    try:
        client = get_client(live)
        if client.live:
            pf = client.preflight(planned_amount=amount, exposure_cap_usd=0, venue=client.venue)
            if not pf.ok_to_trade:
                blockers = ", ".join(pf.blockers)
                return {"error": f"preflight_blocked: {blockers}"}
        result = client.trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
            signal_data=signal_data,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "shares": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}

def execute_sell(market_id: str, shares: float, reasoning: str = "", live: bool = False) -> dict:
    try:
        client = get_client(live)
        if client.live:
            pf = client.preflight(planned_amount=0, exposure_cap_usd=0, venue=client.venue)
            if not pf.ok_to_trade:
                blockers = ", ".join(pf.blockers)
                return {"error": f"preflight_blocked: {blockers}"}
        result = client.trade(
            market_id=market_id,
            side="yes",
            action="sell",
            shares=shares,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_sold": shares,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}

def get_positions(live: bool = False) -> list:
    try:
        client = get_client(live)
        positions = client.get_positions(venue=client.venue)
        from dataclasses import asdict
        return [asdict(p) if hasattr(p, "__dataclass_fields__") else dict(p) for p in positions]
    except Exception:
        return []

# ---------------------------------------------------------------------------
# Main scan loop
# ---------------------------------------------------------------------------

def scan_markets(
    live: bool = False,
    smart_sizing: bool = False,
    quiet: bool = False,
    manage_positions: bool = False,
    no_safeguards: bool = False,
    market_type_filter: set = None,
    log=None,
) -> dict:
    if log is None:
        log = (lambda msg, force=False: None) if quiet else (lambda msg, force=False: print(msg))

    cfg = _config
    allowed_types = market_type_filter or set(cfg["market_types"].split(","))

    log("=" * 60)
    log(f"Kalshi FIFA Soccer Trader  |  {'LIVE' if live else 'DRY RUN'}")
    log(f"Market types: {', '.join(allowed_types)}  |  Entry edge: {cfg['entry_edge']:.0%}")
    log("=" * 60)

    markets = fetch_soccer_markets()
    log(f"Fetched {len(markets)} soccer markets from Simmer API")

    trades_executed = 0
    total_usd_spent = 0.0
    results = []

    # --- Position management pass ---
    if manage_positions:
        positions = get_positions(live)
        log(f"\nManaging {len(positions)} open positions...")
        for pos in positions:
            if pos.get("source") != TRADE_SOURCE:
                continue
            market_id = pos.get("market_id") or pos.get("id")
            current_price = pos.get("current_price") or pos.get("yes_price") or 0
            if current_price >= cfg["exit_threshold"]:
                shares = pos.get("shares") or pos.get("quantity") or 0
                if shares > 0:
                    log(f"  Selling {shares:.1f}sh @ {current_price:.2f} (exit threshold)", force=True)
                    r = execute_sell(market_id, shares, reasoning="exit_threshold", live=live)
                    if r.get("success"):
                        log(f"  ✅ Sold", force=True)
                    else:
                        log(f"  ❌ Sell failed: {r.get('error')}", force=True)

    # --- Entry pass ---
    for market in markets:
        if trades_executed >= cfg["max_trades"]:
            log(f"\nMax trades ({cfg['max_trades']}) reached — stopping.")
            break

        market_id = market.get("id") or market.get("market_id")
        title = market.get("question") or market.get("title") or "(untitled)"

        parsed = parse_market(market, allowed_types)
        if parsed is None:
            continue

        home_name = parsed["home"]
        away_name = parsed["away"]
        home_ovr = lookup_team(home_name)
        away_ovr = lookup_team(away_name)

        if home_ovr is None or away_ovr is None:
            missing = home_name if home_ovr is None else away_name
            log(f"\n  ⚠  Team not found in ratings: '{missing}' — skipping {title[:60]}")
            continue

        lam_home, lam_away = ovr_to_lambdas(home_ovr, away_ovr, cfg["home_boost"])
        grid = build_goal_grid(lam_home, lam_away)

        # Probabilities for this market type
        model_prob = model_probability(parsed, home_ovr, away_ovr, cfg["home_boost"])
        if model_prob is None:
            continue

        yes_price = parsed["yes_price"]
        no_price  = parsed["no_price"]
        fair_yes, fair_no = devig(yes_price, no_price)
        if fair_yes is None:
            continue

        edge_yes = compute_edge(model_prob, fair_yes)
        edge_no  = compute_edge(1.0 - model_prob, fair_no)

        best_edge = edge_yes
        trade_side = "yes"
        if edge_no > edge_yes:
            best_edge = edge_no
            trade_side = "no"

        mtype = parsed["type"]
        line_str = f" (line {parsed['line']})" if parsed["line"] is not None else ""
        log(f"\n{home_name} vs {away_name} — {mtype}{line_str}")
        log(f"  OVR: {home_ovr} vs {away_ovr}  |  λ: {lam_home:.2f} / {lam_away:.2f}")
        log(f"  Model: {model_prob:.1%}  |  Fair YES: {fair_yes:.1%}  |  Edge YES: {edge_yes:+.1%}")
        log(f"  Market price YES/NO: {yes_price:.2f} / {no_price:.2f}")

        if best_edge < cfg["entry_edge"]:
            log(f"  No edge ({best_edge:+.1%} < {cfg['entry_edge']:.0%})")
            continue

        # Safeguards
        if not no_safeguards:
            try:
                client = get_client(live)
                context = client.get_market_context(market_id)
            except Exception:
                context = {}
            ok, reasons = check_safeguards(market, parsed, context, cfg)
            if not ok:
                log(f"  ⛔ Safeguard blocked: {'; '.join(reasons)}")
                continue

        position_size = get_position_size(cfg, smart_sizing)
        reasoning = (
            f"{mtype}{line_str}: {home_name} ({home_ovr} OVR) vs {away_name} ({away_ovr} OVR). "
            f"Model={model_prob:.1%}, fair={fair_yes:.1%}, edge={best_edge:+.1%}."
        )
        signal_data = {
            "market_type": mtype,
            "home_team": home_name,
            "away_team": away_name,
            "home_ovr": home_ovr,
            "away_ovr": away_ovr,
            "lambda_home": lam_home,
            "lambda_away": lam_away,
            "model_prob": round(model_prob, 4),
            "fair_yes": round(fair_yes, 4),
            "edge": round(best_edge, 4),
            "trade_side": trade_side,
            "line": parsed["line"],
            "signal_source": "ea_fc_ovr_poisson",
        }

        log(f"  ✓ Edge {best_edge:+.1%} on {trade_side.upper()} — trading ${position_size:.2f}", force=True)

        result = execute_trade(
            market_id, trade_side, position_size,
            reasoning=reasoning, signal_data=signal_data, live=live,
        )

        if result.get("success"):
            trades_executed += 1
            total_usd_spent += position_size
            shares = result.get("shares_bought") or result.get("shares") or 0
            trade_id = result.get("trade_id")
            sim_tag = "[PAPER] " if result.get("simulated") else ""
            log(f"  ✅ {sim_tag}Bought {shares:.1f}sh @ ${yes_price if trade_side == 'yes' else no_price:.2f}  (trade_id={trade_id})", force=True)
            results.append({"market_id": market_id, "side": trade_side, "amount": position_size, "trade_id": trade_id})
        else:
            log(f"  ❌ Trade failed: {result.get('error')}", force=True)

    log(f"\n{'=' * 60}")
    log(f"Done. {trades_executed} trade(s) executed | ${total_usd_spent:.2f} deployed", force=True)
    return {"trades": trades_executed, "usd_spent": total_usd_spent, "results": results}

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Kalshi FIFA Soccer Trader")
    parser.add_argument("--live",             action="store_true",  help="Execute real trades (default: dry run)")
    parser.add_argument("--smart-sizing",     action="store_true",  help="Size from portfolio balance")
    parser.add_argument("--quiet",            action="store_true",  help="Only print trades/errors")
    parser.add_argument("--import-markets",   action="store_true",  help="Discover and import Kalshi soccer markets")
    parser.add_argument("--manage-positions", action="store_true",  help="Exit positions above threshold, then scan")
    parser.add_argument("--no-safeguards",    action="store_true",  help="Disable all safeguard checks")
    parser.add_argument("--market-types",     type=str,             help="Comma-sep: winner,totals,spread,draw")
    parser.add_argument("--config",           action="store_true",  help="Print current config and loaded ratings count")
    args = parser.parse_args()

    if args.config:
        print("\n--- Config ---")
        for k, v in _config.items():
            print(f"  {k}: {v}")
        ratings = load_ratings()
        unique = len(set(ratings.values()))
        print(f"\nRatings loaded: {len(ratings)} aliases covering {unique} unique OVR values")
        return

    if args.import_markets:
        print("Discovering and importing Kalshi soccer markets...")
        discover_and_import_soccer_markets()
        return

    market_type_filter = None
    if args.market_types:
        market_type_filter = set(t.strip() for t in args.market_types.split(","))

    scan_markets(
        live=args.live,
        smart_sizing=args.smart_sizing,
        quiet=args.quiet,
        manage_positions=args.manage_positions,
        no_safeguards=args.no_safeguards,
        market_type_filter=market_type_filter,
    )

if __name__ == "__main__":
    main()
