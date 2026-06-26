#!/usr/bin/env python3
"""
Live Sports Score Arbitrage — Exploits price lag between ESPN and Polymarket.

Uses Gaussian win-probability models for NBA/NFL/NHL and Poisson for soccer.
Trades when calculated probability diverges >10% from Polymarket price.

Author: Mibayy
"""

import argparse
import json
import logging
import math
import os
import sys
from datetime import datetime, timezone

import requests
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_SLUG = "polymarket-sports-live"
TRADE_SOURCE = "sdk:polymarket-sports-live"

_client = None
def get_client():
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=os.environ.get("TRADING_VENUE", "sim")
        )
    return _client


def check_context(client, market_id, my_probability=None):
    """Check market context before trading (flip-flop, slippage, edge)."""
    try:
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        ctx = client.get_market_context(market_id, **params)
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning")
        if flip_flop and "SEVERE" in flip_flop:
            return False, f"flip-flop: {flip_flop}"
        slippage = ctx.get("slippage", {})
        if slippage.get("slippage_pct", 0) > 0.15:
            return False, "slippage too high"
        edge = ctx.get("edge_analysis", {})
        if edge.get("recommendation") == "HOLD":
            return False, "edge below threshold"
        return True, "ok"
    except Exception:
        return True, "context unavailable"


DIVERGENCE_THRESHOLD = float(os.environ.get('SPORTS_DIVERGENCE_THRESHOLD', '0.10'))
TRADE_SIZE_USD = float(os.environ.get('SPORTS_TRADE_SIZE', '20.0'))

# ESPN API endpoints
ESPN_ENDPOINTS = {
    "nba": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
    "nfl": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "nhl": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
    "soccer_epl": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard",
    "soccer_mls": "https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard",
}

# Sport-specific model parameters
SPORT_CONFIG = {
    "nba": {"sigma": 12.5, "total_minutes": 48.0, "model": "gaussian"},
    "nfl": {"sigma": 13.5, "total_minutes": 60.0, "model": "gaussian"},
    "nhl": {"sigma": 1.5, "total_minutes": 60.0, "model": "gaussian"},
    "soccer_epl": {"lambda_per_90": 1.35, "total_minutes": 90.0, "model": "poisson"},
    "soccer_mls": {"lambda_per_90": 1.35, "total_minutes": 90.0, "model": "poisson"},
}

log = logging.getLogger(SKILL_SLUG)


# ---------------------------------------------------------------------------
# Probability models
# ---------------------------------------------------------------------------
def phi(x: float) -> float:
    """Standard normal CDF approximation."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def gaussian_win_prob(lead: float, minutes_remaining: float, total_minutes: float, sigma: float) -> float:
    """
    Gaussian model: P(team_ahead wins) = Phi(lead / (sigma * sqrt(t_rem / T)))
    """
    if minutes_remaining <= 0:
        return 1.0 if lead > 0 else (0.0 if lead < 0 else 0.5)

    t_frac = minutes_remaining / total_minutes
    if t_frac > 1.0:
        t_frac = 1.0

    denom = sigma * math.sqrt(t_frac)
    if denom < 0.001:
        return 1.0 if lead > 0 else 0.0

    return phi(lead / denom)


def poisson_pmf(k: int, lam: float) -> float:
    """Poisson probability mass function."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def poisson_win_prob(
    home_goals: int, away_goals: int,
    minutes_remaining: float, total_minutes: float,
    lambda_per_90: float,
) -> float:
    """
    Poisson model for soccer: calculate P(home wins) from current score
    and expected remaining goals.
    """
    if minutes_remaining <= 0:
        if home_goals > away_goals:
            return 1.0
        elif home_goals < away_goals:
            return 0.0
        return 0.5

    remaining_frac = minutes_remaining / total_minutes
    lam_remaining = lambda_per_90 * remaining_frac

    # Sum over possible remaining goals (cap at 8 each for speed)
    max_goals = 8
    p_home_win = 0.0
    p_draw = 0.0

    for h_add in range(max_goals + 1):
        for a_add in range(max_goals + 1):
            p = poisson_pmf(h_add, lam_remaining) * poisson_pmf(a_add, lam_remaining)
            final_h = home_goals + h_add
            final_a = away_goals + a_add
            if final_h > final_a:
                p_home_win += p
            elif final_h == final_a:
                p_draw += p

    return p_home_win + p_draw * 0.5  # half credit for draw


# ---------------------------------------------------------------------------
# ESPN data parsing
# ---------------------------------------------------------------------------
def fetch_live_games(sport: str) -> list:
    """Fetch live games from ESPN."""
    url = ESPN_ENDPOINTS.get(sport)
    if not url:
        return []

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.debug("ESPN fetch failed for %s: %s", sport, e)
        return []

    games = []
    events = data.get("events", [])

    for event in events:
        status = event.get("status", {})
        state = status.get("type", {}).get("state", "")

        if state != "in":  # only live games
            continue

        competitions = event.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue

        # Parse scores and teams
        home = away = None
        for c in competitors:
            info = {
                "team": c.get("team", {}).get("displayName", "Unknown"),
                "abbr": c.get("team", {}).get("abbreviation", "UNK"),
                "score": int(c.get("score", "0")),
            }
            if c.get("homeAway") == "home":
                home = info
            else:
                away = info

        if not home or not away:
            continue

        # Parse clock / period
        clock_str = status.get("displayClock", "0:00")
        period = int(status.get("period", 1))

        minutes_elapsed = parse_elapsed(sport, clock_str, period)
        config = SPORT_CONFIG.get(sport, {})
        total = config.get("total_minutes", 48.0)
        minutes_remaining = max(0, total - minutes_elapsed)

        games.append({
            "event_id": event.get("id", ""),
            "name": event.get("name", f"{away['team']} @ {home['team']}"),
            "home": home,
            "away": away,
            "minutes_remaining": minutes_remaining,
            "total_minutes": total,
            "sport": sport,
        })

    return games


def parse_elapsed(sport: str, clock_str: str, period: int) -> float:
    """Parse elapsed minutes from ESPN clock data."""
    try:
        parts = clock_str.replace(" ", "").split(":")
        if len(parts) == 2:
            mins, secs = float(parts[0]), float(parts[1])
        else:
            mins, secs = 0, 0
    except (ValueError, IndexError):
        mins, secs = 0, 0

    clock_mins = mins + secs / 60.0

    if sport == "nba":
        # 4 quarters × 12 min; clock counts down
        elapsed_in_period = 12.0 - clock_mins
        return (period - 1) * 12.0 + elapsed_in_period
    elif sport == "nfl":
        elapsed_in_period = 15.0 - clock_mins
        return (period - 1) * 15.0 + elapsed_in_period
    elif sport == "nhl":
        elapsed_in_period = 20.0 - clock_mins
        return (period - 1) * 20.0 + elapsed_in_period
    elif sport.startswith("soccer"):
        # Soccer clock counts up; period = half
        return clock_mins + (45.0 if period >= 2 else 0)

    return clock_mins


# ---------------------------------------------------------------------------
# Market matching
# ---------------------------------------------------------------------------
def find_matching_market(client: SimmerClient, game: dict) -> dict | None:
    """Find a Polymarket market matching this game."""
    home_team = game["home"]["team"]
    away_team = game["away"]["team"]

    # Search by team names
    for query in [home_team, away_team, game["home"]["abbr"]]:
        try:
            markets = client.find_markets(query=query)
        except Exception:
            markets = []

        for m in (markets or []):
            q = m.get("question", "").lower()
            if (home_team.lower() in q or away_team.lower() in q or
                game["home"]["abbr"].lower() in q):
                return m

    return None


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def calculate_fair_prob(game: dict) -> dict:
    """Calculate fair probability using sport-specific model."""
    sport = game["sport"]
    config = SPORT_CONFIG[sport]
    home_score = game["home"]["score"]
    away_score = game["away"]["score"]
    t_rem = game["minutes_remaining"]
    total = game["total_minutes"]

    if config["model"] == "gaussian":
        lead = home_score - away_score
        p_home = gaussian_win_prob(lead, t_rem, total, config["sigma"])
    else:
        p_home = poisson_win_prob(
            home_score, away_score, t_rem, total, config["lambda_per_90"]
        )

    return {
        "p_home_win": p_home,
        "p_away_win": 1.0 - p_home,
        "lead": home_score - away_score,
        "minutes_remaining": t_rem,
    }


def run(live: bool = False, quiet: bool = False):
    """Main scan and trade loop."""
    client = get_client()

    all_games = []
    for sport in ESPN_ENDPOINTS:
        games = fetch_live_games(sport)
        all_games.extend(games)
        log.info("ESPN %s: %d live games", sport, len(games))

    if not all_games:
        log.info("No live games currently")
        return

    trades_made = 0

    for game in all_games:
        fair = calculate_fair_prob(game)
        log.info(
            "%s — %s %d vs %s %d | %.0f min left | P(home)=%.1f%%",
            game["sport"].upper(),
            game["home"]["team"], game["home"]["score"],
            game["away"]["team"], game["away"]["score"],
            fair["minutes_remaining"],
            fair["p_home_win"] * 100,
        )

        # Find matching Polymarket market
        market = find_matching_market(client, game)
        if not market:
            log.debug("No Polymarket market found for %s", game["name"])
            continue

        market_price = float(market.current_probability)
        market_id = market.id
        token_id = market.polymarket_token_id
        if not token_id:
            continue

        # Check divergence
        divergence = fair["p_home_win"] - market_price

        if abs(divergence) < DIVERGENCE_THRESHOLD:
            log.info(
                "  Market %.1f%% vs model %.1f%% — divergence %.1f%% < threshold",
                market_price * 100, fair["p_home_win"] * 100, abs(divergence) * 100,
            )
            continue

        # Trade signal
        if divergence > 0:
            side = "yes"
            desc = "underpriced"
        else:
            side = "no"
            desc = "overpriced"

        reasoning = (
            f"Live score arb ({game['sport']}): {game['home']['team']} "
            f"{game['home']['score']}-{game['away']['score']} {game['away']['team']}, "
            f"{fair['minutes_remaining']:.0f}min left. "
            f"Model P(home)={fair['p_home_win']:.1%} vs market={market_price:.1%}. "
            f"Divergence={abs(divergence):.1%}, market {desc}."
        )

        log.info("  TRADE: %s — %s", side.upper(), reasoning)

        ok, reason = check_context(client, market_id)
        if not ok:
            log.warning("Skipping trade: %s", reason)
            continue

        if live:
            try:
                result = client.trade(
                    market_id=market_id,
                    side=side,
                    amount=TRADE_SIZE_USD,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                log.info("  Trade placed: %s", json.dumps(result, default=str)[:200])
                trades_made += 1
            except Exception as e:
                log.error("  Order failed: %s", e)
        else:
            log.info("  [DRY RUN] Would %s $%.0f", side, TRADE_SIZE_USD)
            trades_made += 1

    if not quiet:
        print(f"\n{'='*60}")
        print(f"Live Sports Scan — {datetime.now(timezone.utc).isoformat()}")
        print(f"Live games found: {len(all_games)}")
        print(f"Trades: {trades_made}")
        print(f"Mode: {'LIVE' if live else 'DRY RUN'}")
        print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Live Sports Score Arbitrage")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--quiet", action="store_true", help="Suppress summary output")
    parser.add_argument("--debug", action="store_true", help="Debug logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else (logging.WARNING if args.quiet else logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")

    if not os.environ.get("SIMMER_API_KEY"):
        log.error("SIMMER_API_KEY not set")
        sys.exit(1)

    try:
        run(live=args.live, quiet=args.quiet)
    except KeyboardInterrupt:
        log.info("Interrupted")
    except Exception as e:
        log.error("Fatal: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
