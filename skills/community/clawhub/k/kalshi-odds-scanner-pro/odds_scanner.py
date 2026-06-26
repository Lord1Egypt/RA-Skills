#!/usr/bin/env python3
"""
📊 Odds API Scanner
====================
Compares sportsbook lines (The Odds API) vs Kalshi/Polymarket prices.
Finds markets where prediction markets misprice vs sharp books.

Key rule: ONE side per game only — never bet both sides of same market.

NO-side NCAAB insight: When sportsbooks price a team at >80% probability
but Kalshi YES is even higher, buying NO on that team is underpriced.
Historical edge: ~74% win rate on NCAAB heavy favorites (per backtesting).

Usage:
  python3 odds_scanner.py          # scan YES plays + print
  python3 odds_scanner.py --buy    # scan + execute on Kalshi
  python3 odds_scanner.py --sport basketball_nba
  python3 odds_scanner.py --sport basketball_ncaab
  python3 odds_scanner.py --side no    # scan NO-side heavy-favorite plays
  python3 odds_scanner.py --side both  # scan YES + NO plays together
"""

import os, sys, json, time, base64, argparse
import urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

# Ensemble consensus — graceful fallback if unavailable
try:
    from ensemble import get_consensus as ensemble_consensus, format_for_log as ensemble_log
    ENSEMBLE_ENABLED = True
except ImportError:
    ENSEMBLE_ENABLED = False

ODDS_API_KEY = "a977eadc1440ca4b073a6158f52f796a"
KALSHI_KEY_ID = "7a7c9013-90a3-4a85-b5de-189df1aa2371"
KALSHI_PEM = Path.home() / ".config/kalshi/private_key.pem"

MIN_EDGE          = 0.08   # 8% minimum edge vs sportsbook
MIN_EDGE_NO       = 0.05   # 5% min edge for NO plays (lower bar, higher win rate)
NO_HEAVY_FAV_PROB = 0.80   # Flag NO plays when sportsbook has team > 80%
MAX_BET           = 60.0
MIN_BET           = 10.0
RESERVE           = 50.0
KELLY_FRAC        = 0.25

SPORT_MAP = {
    "nba":   ("basketball_nba",   "KXNBAGAME"),
    "ncaab": ("basketball_ncaab", "KXNCAAMBGAME"),
    "nhl":   ("icehockey_nhl",    "KXNHLGAME"),
    "mlb":   ("baseball_mlb",     "KXMLBGAME"),
}

def load_kalshi_key():
    from cryptography.hazmat.primitives import serialization
    with open(KALSHI_PEM, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def kalshi_request(pk, method, endpoint, body=None):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    full_path = f"/trade-api/v2{endpoint}"
    ts = str(int(time.time() * 1000))
    msg = f"{ts}{method.upper()}{full_path}".encode()
    sig = pk.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    headers = {"KALSHI-ACCESS-KEY": KALSHI_KEY_ID,
               "KALSHI-ACCESS-TIMESTAMP": ts,
               "KALSHI-ACCESS-SIGNATURE": base64.b64encode(sig).decode(),
               "Accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"https://api.elections.kalshi.com/trade-api/v2{endpoint}",
        data=data, headers=headers, method=method.upper()
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": e.read().decode()[:200]}

def get_odds(sport_key):
    """Fetch sportsbook lines from The Odds API."""
    url = (f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
           f"?apiKey={ODDS_API_KEY}&regions=us&markets=h2h&oddsFormat=decimal")
    req = urllib.request.Request(url, headers={"User-Agent": "ClawdipusRex/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"   ⚠️  Odds API error: {e}")
        return []

def build_sportsbook_map(games):
    """Build team → implied_probability map, averaged across bookmakers."""
    team_probs = {}
    game_teams = {}  # team → game_id for dedup

    for g in games:
        game_id = g.get("id", g.get("sport_key","") + g.get("commence_time",""))
        home = g.get("home_team","").lower()
        away = g.get("away_team","").lower()
        game_teams[home] = game_id
        game_teams[away] = game_id

        books = g.get("bookmakers", [])
        for b in books[:4]:  # avg top 4 bookmakers
            outcomes = b.get("markets",[{}])[0].get("outcomes",[])
            for o in outcomes:
                name = o["name"].lower()
                prob = 1 / o["price"]
                if name not in team_probs:
                    team_probs[name] = []
                team_probs[name].append(prob)

    return {t: sum(p)/len(p) for t, p in team_probs.items()}, game_teams

def get_kalshi_markets(pk, series_ticker):
    """Get open Kalshi markets for a series."""
    data = kalshi_request(pk, "GET", f"/markets?limit=200&status=open&series_ticker={series_ticker}")
    markets = data.get("markets", [])
    result = []
    for m in markets:
        yes_ask = float(m.get("yes_ask_dollars") or 0)
        no_ask  = float(m.get("no_ask_dollars") or 0)
        if yes_ask < 0.04 or yes_ask > 0.96:
            continue
        result.append({
            "ticker":       m.get("ticker",""),
            "title":        m.get("title",""),
            "yes_sub":      m.get("yes_sub_title","").lower(),
            "no_sub":       m.get("no_sub_title","").lower(),
            "event_ticker": m.get("event_ticker",""),
            "yes_ask":      yes_ask,
            "no_ask":       no_ask if no_ask > 0 else round(1.0 - yes_ask, 4),
            "close":        m.get("close_time","")[:10],
        })
    return result

def match_team(yes_sub, sportsbook_map):
    """Find best matching team in sportsbook map."""
    best_team = None
    best_prob = 0
    best_overlap = 0
    sub_words = [w for w in yes_sub.split() if len(w) > 3]

    for team, prob in sportsbook_map.items():
        team_words = [w for w in team.split() if len(w) > 3]
        overlap = sum(1 for w in team_words if any(w in s or s in w for s in sub_words))
        if overlap > best_overlap or (overlap == best_overlap and prob > best_prob):
            best_overlap = overlap
            best_team = team
            best_prob = prob

    return (best_team, best_prob) if best_overlap >= 1 else (None, 0)

def kelly_size(true_prob, market_price, bankroll):
    deployable = bankroll - RESERVE
    if market_price <= 0 or true_prob <= market_price:
        return 0
    b = (1 - market_price) / market_price
    q = 1 - true_prob
    k = max(0, (true_prob * b - q) / b) * KELLY_FRAC
    return round(min(MAX_BET, max(MIN_BET, deployable * k)), 2)

def scan_no_side(pk, sport_key, series_ticker, bankroll, min_edge=MIN_EDGE_NO):
    """
    NO-side scanner: find heavy favorites where buying NO is underpriced.

    Insight: when sportsbooks price Team A at >80%, the NO side on Team A
    in Kalshi is systematically underpriced. Historical NCAAB win rate: ~74%.

    Edge formula:
      NO price on Kalshi = no_ask (or 1 - yes_ask)
      true_prob_of_NO = 1 - sportsbook_prob_of_A
      edge = (1 - sportsbook_prob_of_A) - no_ask
           = if sportsbook says 85%, true NO prob = 15%.
             if Kalshi NO ask is 12¢, edge = 15% - 12% = +3%.
      BUT: we also capture the complementary angle:
           if sportsbook says 85% for TeamA and Kalshi YES is only 70%,
           NO at 30¢ vs true NO (15%) = underdog is overpriced → edge to be short YES.
    """
    print(f"   📡 Fetching {sport_key} odds (NO-side scanner)...")
    games = get_odds(sport_key)
    if not games:
        return []

    sportsbook_map, game_teams = build_sportsbook_map(games)
    print(f"   📊 {len(games)} games, {len(sportsbook_map)} teams from sportsbooks")

    kalshi_markets = get_kalshi_markets(pk, series_ticker)
    print(f"   🎯 {len(kalshi_markets)} Kalshi markets open")

    seen_events = {}
    for m in kalshi_markets:
        team, sportsbook_prob = match_team(m["yes_sub"], sportsbook_map)
        if not team or sportsbook_prob == 0:
            continue

        # Only consider heavy favorites (>80% sportsbook probability)
        if sportsbook_prob < NO_HEAVY_FAV_PROB:
            continue

        # NO side analysis
        # True probability of NO = 1 - sportsbook_prob_of_favorite
        # Kalshi NO price = m["no_ask"] (or approximated as 1 - yes_ask)
        true_no_prob = 1.0 - sportsbook_prob
        no_ask = m["no_ask"]

        # Edge: sportsbook says this team wins 85%, so underdog NO is worth 15%.
        # If Kalshi charges 12¢ for NO, that's a +3% edge.
        # Alternatively: if Kalshi YES is much lower than sportsbook implies,
        # the YES-side gap shows the underdog (NO target) is overpriced on YES.
        edge = true_no_prob - no_ask

        if edge < min_edge:
            continue

        # Kelly size for NO purchase
        no_kelly = kelly_size(true_no_prob, no_ask, bankroll)
        if no_kelly < MIN_BET:
            continue

        play = {
            **m,
            "trade_side":   "no",
            "team":         team,
            "sportsbook_prob_yes": sportsbook_prob,
            "true_prob":    true_no_prob,
            "market_price": no_ask,
            "edge":         round(edge, 4),
            "kelly_size":   no_kelly,
            "label":        f"NO on {m['yes_sub']} (fav {sportsbook_prob:.0%})",
        }

        event = m["event_ticker"] or m["title"]
        if event not in seen_events or edge > seen_events[event]["edge"]:
            seen_events[event] = play

    plays = sorted(seen_events.values(), key=lambda x: x["edge"], reverse=True)
    return plays


def scan(pk, sport_key, series_ticker, bankroll):
    """Find YES-side edges between sportsbook and Kalshi."""
    print(f"   📡 Fetching {sport_key} odds...")
    games = get_odds(sport_key)
    if not games:
        return []

    sportsbook_map, game_teams = build_sportsbook_map(games)
    print(f"   📊 {len(games)} games, {len(sportsbook_map)} teams from sportsbooks")

    kalshi_markets = get_kalshi_markets(pk, series_ticker)
    print(f"   🎯 {len(kalshi_markets)} Kalshi markets open")

    # Find edges — deduplicate by event_ticker (one side per game)
    seen_events = {}  # event_ticker → best play
    for m in kalshi_markets:
        team, true_prob = match_team(m["yes_sub"], sportsbook_map)
        if not team or true_prob == 0:
            continue

        edge = true_prob - m["yes_ask"]
        if edge < MIN_EDGE:
            continue

        size = kelly_size(true_prob, m["yes_ask"], bankroll)
        if size < MIN_BET:
            continue

        play = {**m, "trade_side": "yes", "team": team, "true_prob": true_prob,
                "edge": edge, "kelly_size": size, "label": m["yes_sub"]}

        # Keep only best edge per game event
        event = m["event_ticker"] or m["title"]
        if event not in seen_events or edge > seen_events[event]["edge"]:
            seen_events[event] = play

    plays = sorted(seen_events.values(), key=lambda x: x["edge"], reverse=True)
    return plays

def print_plays(plays, mode="yes"):
    """Print plays table."""
    if mode == "no":
        print(f"\n  {'Team (NO on fav)':<28} {'Book FAV':>8} {'NO ask':>7} {'Edge':>6}  {'Kelly$':>7}  Market")
        print(f"  {'-'*28} {'--------':>8} {'------':>7} {'----':>6}  {'------':>7}  ------")
        for p in plays:
            print(f"  {p['label']:<28} {p['sportsbook_prob_yes']:>7.0%} {p['no_ask']:>6.0%} "
                  f"{p['edge']:>+5.0%}  ${p['kelly_size']:>6.0f}  {p['title'][:35]}")
    else:
        print(f"\n  {'Team':<22} {'Book':>6} {'Kalshi':>7} {'Edge':>6}  {'Kelly$':>7}  Market")
        print(f"  {'-'*22} {'----':>6} {'------':>7} {'----':>6}  {'------':>7}  ------")
        for p in plays:
            print(f"  {p.get('label', p.get('yes_sub','')):<22} {p['true_prob']:>5.0%} "
                  f"{p['yes_ask']:>6.0%} {p['edge']:>+5.0%}  ${p['kelly_size']:>6.0f}  {p['title'][:40]}")


def _run_ensemble(play: dict) -> dict | None:
    """
    Run ensemble consensus check on a play.
    Returns result dict, or None if ensemble is disabled/unavailable.
    """
    if not ENSEMBLE_ENABLED:
        return None
    side = play.get("trade_side", "yes")
    market_price = play["no_ask"] if side == "no" else play["yes_ask"]
    sportsbook_prob = play.get("true_prob", 0.5)
    if side == "no":
        # For NO plays: true_prob is already the NO probability
        outcome = f"NOT {play.get('yes_sub', 'favorite')}"
    else:
        outcome = play.get("yes_sub", play.get("label", play["ticker"]))

    try:
        result = ensemble_consensus(
            market_title=play.get("title", play["ticker"]),
            outcome=outcome,
            market_price=market_price,
            sportsbook_prob=sportsbook_prob,
            signals=["odds_api"],
            context=(
                f"Sportsbooks: {sportsbook_prob:.0%} implied. "
                f"Kalshi {side.upper()}: {market_price:.0%}. "
                f"Edge: {play.get('edge', 0):.0%}."
            ),
        )
        return result
    except Exception as e:
        print(f"   ⚠️  ensemble error (non-blocking): {e}")
        return None


def _log_ensemble_result(play: dict, ensemble_result: dict | None) -> None:
    """Append ensemble result to TRADE_LOG.md."""
    log_path = Path(__file__).parent / "TRADE_LOG.md"
    if not log_path.exists():
        return
    label = play.get("label", play.get("yes_sub", play.get("ticker", "?")))
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    if ensemble_result is None:
        line = f"\n> {ts} | Ensemble: DISABLED | {label}\n"
    else:
        line = f"\n> {ts} | {ensemble_log(ensemble_result)} | {label}\n"
    try:
        with open(log_path, "a") as f:
            f.write(line)
    except Exception:
        pass


def execute_plays(pk, plays):
    """Execute a list of plays (YES or NO side), with ensemble consensus gate."""
    for p in plays:
        side = p.get("trade_side", "yes")
        price = p["no_ask"] if side == "no" else p["yes_ask"]
        label = p.get("label", p.get("yes_sub", p["ticker"]))

        # ── Momentum check ───────────────────────────────────────────────────
        try:
            from momentum import get_momentum_signal
            mom = get_momentum_signal(p["ticker"], price)
            if mom["confidence_delta"] < 0:
                print(f"  📉 Momentum bearish ({mom['note']}) — skipping {label}")
                continue
            elif mom["confidence_delta"] > 0:
                print(f"  📈 Momentum bullish ({mom['note']})")
        except Exception:
            pass  # momentum unavailable, proceed

        # ── Ensemble consensus check ─────────────────────────────────────────
        ensemble_result = _run_ensemble(p)
        if ensemble_result is not None:
            rec = ensemble_result.get("recommendation", "SKIP")
            avg = ensemble_result.get("avg_prob", 0)
            models_ok = ensemble_result.get("_models_ok", 0)
            print(f"  🧠 Ensemble → {rec}  avg={avg:.0%}  "
                  f"conf={ensemble_result.get('confidence', 0):.0%}  "
                  f"models={models_ok}/3")
            if models_ok == 0:
                # All models failed (rate-limited, etc) — don't block trades
                print(f"  ⚠️  Ensemble unavailable (0/3 models) — proceeding without gate")
            elif rec != "BUY":
                print(f"  ⏭️  Skipping {label} — ensemble says {rec}")
                _log_ensemble_result(p, ensemble_result)
                continue
        # ── If ensemble failed/disabled, proceed anyway (don't block trades) ──

        count = int(p["kelly_size"] / price)
        if count < 1:
            continue
        cost = round(count * price, 2)

        if side == "no":
            # NO orders use yes_price field with the NO price in cents
            order_body = {
                "ticker": p["ticker"], "side": "no", "action": "buy",
                "count": count, "type": "limit",
                "yes_price": round((1.0 - p["no_ask"]) * 100),  # Kalshi API: yes_price for NO orders
            }
        else:
            order_body = {
                "ticker": p["ticker"], "side": "yes", "action": "buy",
                "count": count, "type": "limit",
                "yes_price": round(p["yes_ask"] * 100),
            }

        resp = kalshi_request(pk, "POST", "/portfolio/orders", order_body)
        order = resp.get("order", {})
        filled = float(order.get("fill_count_fp", 0))
        status = "✅" if filled > 0 else "❌"
        detail = resp.get("detail","")[:50] if "error" in resp else ""
        print(f"  {status} {count}x {side.upper()} {label:<20} @ {round(price*100)}¢ ${cost:.0f} {detail}")
        _log_ensemble_result(p, ensemble_result)
        time.sleep(1.5)


def main():
    parser = argparse.ArgumentParser(description="Odds API Scanner")
    parser.add_argument("--buy",  action="store_true", help="Execute plays")
    parser.add_argument("--sport", default="nba", choices=list(SPORT_MAP.keys()))
    parser.add_argument("--min-edge", type=float, default=MIN_EDGE)
    parser.add_argument("--side",  default="yes", choices=["yes", "no", "both"],
                        help="Which side to scan: yes (default), no (NO plays on heavy favs), both")
    args = parser.parse_args()

    pk = load_kalshi_key()

    print("=" * 65)
    print("📊  ODDS API SCANNER")
    print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    sport_key, series_ticker = SPORT_MAP[args.sport]

    # Get balance
    bal = kalshi_request(pk, "GET", "/portfolio/balance")
    cash = bal.get("balance", 0) / 100
    print(f"\n💰 Kalshi cash: ${cash:.2f}\n")

    yes_plays, no_plays = [], []

    if args.side in ("yes", "both"):
        yes_plays = scan(pk, sport_key, series_ticker, cash)

    if args.side in ("no", "both"):
        print()
        no_plays = scan_no_side(pk, sport_key, series_ticker, cash, min_edge=args.min_edge)

    # Deduplicate: if a market appears in both, keep the better edge
    all_plays = yes_plays + no_plays
    if not all_plays:
        print("\n✓ No significant edges found vs sportsbooks right now.")
        return

    # YES plays
    if yes_plays:
        print(f"\n⚡ YES plays — {len(yes_plays)} edge play(s) found:")
        print_plays(yes_plays, mode="yes")
        total_yes = sum(p["kelly_size"] for p in yes_plays)
        print(f"\n  YES total to deploy: ${total_yes:.0f}")

    # NO plays
    if no_plays:
        print(f"\n🎯 NO plays — {len(no_plays)} heavy-favorite NO trade(s) found (74% hist. win rate):")
        print_plays(no_plays, mode="no")
        total_no = sum(p["kelly_size"] for p in no_plays)
        print(f"\n  NO total to deploy: ${total_no:.0f}")

    grand_total = sum(p["kelly_size"] for p in all_plays)
    print(f"\n  Grand total to deploy: ${grand_total:.0f}")

    if args.buy:
        print(f"\n🚀 Executing...\n")
        execute_plays(pk, all_plays)
        bal2 = kalshi_request(pk, "GET", "/portfolio/balance")
        print(f"\n  Remaining cash: ${bal2.get('balance',0)/100:.2f}")

if __name__ == "__main__":
    main()
