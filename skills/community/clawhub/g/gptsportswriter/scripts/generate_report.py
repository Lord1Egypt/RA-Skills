#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(__file__))
FETCH_SCRIPT = os.path.join(ROOT, "scripts", "fetch_odds.py")
ASKNEWS_SCRIPT = os.path.join(ROOT, "scripts", "fetch_asknews.py")
FREE_CONTEXT_SCRIPT = os.path.join(ROOT, "scripts", "fetch_free_context.py")
FREE_ODDS_SCRIPT = os.path.join(ROOT, "scripts", "fetch_free_odds.py")
EXTRACT_COVERS_MLB_SCRIPT = os.path.join(ROOT, "scripts", "extract_covers_mlb.py")
EXTRACT_COVERS_MLB_LINES_SCRIPT = os.path.join(ROOT, "scripts", "extract_covers_mlb_lines.py")
MLB_WEATHER_SCRIPT = os.path.join(ROOT, "scripts", "fetch_mlb_weather.py")
MIN_PICK_SCORE = 1.18


def american_to_implied(price: int) -> float:
    if price is None:
        return 0.0
    if price > 0:
        return 100.0 / (price + 100.0)
    return (-price) / ((-price) + 100.0)


def best_price_score(price: int) -> float:
    implied = american_to_implied(price)
    score = 1.0 - implied
    if price < -220:
        score -= 0.30
    elif price < -180:
        score -= 0.15
    elif price > 180:
        score -= 0.12
    return score


def classify_confidence(score: float) -> str:
    if score >= 1.55:
        return "High"
    if score >= 1.22:
        return "Medium"
    return "Low"


def run_fetch(sports: List[str], mode: str) -> Dict[str, Any]:
    cmd = [sys.executable, FETCH_SCRIPT, "--mode", mode, "--sports", *sports]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True, env=os.environ.copy())
    return json.loads(proc.stdout)


def run_asknews(query: str, n_articles: int = 2) -> List[Dict[str, Any]]:
    try:
        cmd = [sys.executable, ASKNEWS_SCRIPT, query, "--n-articles", str(n_articles)]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, env=os.environ.copy())
        data = json.loads(proc.stdout)
        return data.get("articles", []) or []
    except Exception:
        return []


def summarize_game_pick(game: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    event = f"{game['away_team']} at {game['home_team']}"
    sport = game.get("sport_key")
    candidates = []

    for team, info in (game.get("best_h2h") or {}).items():
        price = info.get("price")
        if price is None:
            continue
        score = 0.55 + best_price_score(price)
        if sport == "baseball_mlb":
            score += 0.02
            # Prefer modest favorites / near-pick'em MLB prices over blind dog-chasing.
            if -155 <= price <= -105:
                score += 0.28
            elif -104 <= price <= 110:
                score += 0.14
            elif 111 <= price <= 125:
                score += 0.03
            elif 126 <= price <= 150:
                score -= 0.10
            elif price > 150:
                score -= 0.34
        if sport == "icehockey_nhl":
            if -150 <= price <= 130:
                score += 0.16
            elif price > 150:
                score -= 0.18
        if sport == "soccer_epl":
            if -135 <= price <= 160:
                score += 0.18
            elif price > 180:
                score -= 0.14
        if price < -200:
            score -= 0.22
        if price > 160:
            score -= 0.20
        candidates.append({
            "event": event,
            "sport": sport,
            "market": "Moneyline",
            "lean": f"{team} ML",
            "current_odds_range": f"best price {price} at {info.get('book')}",
            "confidence_score": score,
            "line_sensitivity": "Gets worse if the market moves toward expensive favorite pricing or away from plus-money value.",
            "why": "Books are offering a clearly defined best moneyline, and the model prefers prices that are not overly juiced.",
        })

    for team, info in (game.get("spread_ranges") or {}).items():
        points = info.get("points") or []
        prices = info.get("prices") or []
        if not points or not prices:
            continue
        shortest = min(points, key=lambda p: abs(float(p)))
        best_price = max(prices)
        point_val = float(shortest)
        score = 1.00 + (1.0 / (1.0 + abs(point_val))) + (best_price_score(best_price) * 0.25)
        if sport == "basketball_nba":
            score += 0.10
        if sport == "icehockey_nhl":
            score -= 0.10
        if sport == "soccer_epl":
            score -= 0.28
        if abs(point_val) <= 2.5:
            score += 0.24
        elif abs(point_val) >= 6:
            score -= 0.18
        if abs(point_val) == 1.5:
            score -= 0.40
            if sport == "baseball_mlb":
                score -= 0.38
            if sport == "icehockey_nhl":
                score -= 0.35
        if abs(point_val) > 10:
            score -= 0.40
        if best_price > 140:
            score -= 0.15
        candidates.append({
            "event": event,
            "sport": sport,
            "market": "Spread",
            "lean": f"{team} {shortest}",
            "current_odds_range": f"points {', '.join(map(str, points))}; prices {', '.join(map(str, prices))}",
            "confidence_score": score,
            "line_sensitivity": "Best at the shortest number with the least juice; this model strongly prefers short spreads over flashy run lines.",
            "why": "The spread is consistent across books, and the model explicitly prefers tighter, more stable numbers.",
        })

    for side, info in (game.get("total_ranges") or {}).items():
        points = info.get("points") or []
        prices = info.get("prices") or []
        if not points or not prices:
            continue
        point_span = max(points) - min(points) if len(points) > 1 else 0
        best_price = max(prices)
        score = 0.12 + (1.0 / (1.0 + point_span)) + (best_price_score(best_price) * 0.08)
        if point_span == 0:
            score += 0.05
        if max(points) >= 230 or min(points) <= 7:
            score -= 0.08
        if sport == "soccer_epl":
            if max(points) <= 3.5:
                score += 0.10
            score += 0.06
        candidates.append({
            "event": event,
            "sport": sport,
            "market": "Total",
            "lean": f"{side} {min(points)}" if len(set(points)) == 1 else f"{side} {min(points)}-{max(points)}",
            "current_odds_range": f"points {', '.join(map(str, points))}; prices {', '.join(map(str, prices))}",
            "confidence_score": score,
            "line_sensitivity": "Totals are ranked conservatively unless supported by stronger context.",
            "why": "The total is available across books, but totals are intentionally deprioritized unless they look unusually stable.",
        })

    if not candidates:
        return None
    return max(candidates, key=lambda x: x["confidence_score"])


def apply_asknews_context(picks: List[Dict[str, Any]]) -> None:
    for pick in picks[:5]:
        articles = run_asknews(f"{pick['event']} betting preview injuries {pick['lean']}", n_articles=2)
        boost = 0.0
        note = None
        for art in articles:
            blob = ((art.get("summary") or "") + " " + (art.get("title") or art.get("eng_title") or "")).lower()
            if any(k in blob for k in ["out", "questionable", "probable", "injury", "soreness", "knee", "ankle", "calf"]):
                boost += 0.08
                note = "AskNews surfaced same-day injury or availability context."
            if any(k in blob for k in ["preview", "win probability", "favorite", "close game", "toss-up"]):
                boost += 0.05
                note = note or "AskNews surfaced same-day matchup preview context."
        pick["confidence_score"] += boost
        if note:
            pick["why"] += f" {note}"


def build_ranked(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    picks = []
    for sport in data.get("sports", []):
        for game in sport.get("games", []):
            best = summarize_game_pick(game)
            if best:
                picks.append(best)
    picks = sorted(picks, key=lambda x: x["confidence_score"], reverse=True)
    apply_asknews_context(picks)
    picks = sorted(picks, key=lambda x: x["confidence_score"], reverse=True)
    filtered = []
    for p in picks:
        threshold = MIN_PICK_SCORE
        if p.get('sport') == 'baseball_mlb':
            threshold = max(threshold, 1.30)
        if p['confidence_score'] >= threshold:
            filtered.append(p)
    return filtered


def render_free_mode_report(data: Dict[str, Any], sports: List[str]) -> str:
    lines = []
    lines.append("**GPTSportswriter — Best Betting Advice of the Day**")
    lines.append("**Date:** today")
    lines.append("**Mode:** Free fallback")
    lines.append("")
    lines.append("Using free/public sources only for odds context and news context.")
    lines.append("This mode avoids paid APIs, but odds may be less precise or more stale.")
    lines.append("")

    # Special-case MLB free mode with Covers extraction.
    if sports == ['baseball_mlb']:
        try:
            import requests, tempfile
            html = requests.get('https://www.covers.com/sport/baseball/mlb/odds', timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
            with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.html') as f:
                f.write(html)
                odds_page = f.name
            proc = subprocess.run([sys.executable, EXTRACT_COVERS_MLB_SCRIPT, odds_page], capture_output=True, text=True, check=True, env=os.environ.copy())
            events = json.loads(proc.stdout).get('events', [])
            ranked = []
            for ev in events:
                matchup_url = (ev.get('url') or '').replace('#sportsevent', '')
                snapshot_note = 'No line snapshot extracted.'
                ml = None
                ou = None
                if matchup_url:
                    try:
                        page = requests.get(matchup_url, timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
                        with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.html') as mf:
                            mf.write(page)
                            matchup_file = mf.name
                        snap_proc = subprocess.run([sys.executable, EXTRACT_COVERS_MLB_LINES_SCRIPT, matchup_file], capture_output=True, text=True, check=True, env=os.environ.copy())
                        snaps = json.loads(snap_proc.stdout).get('snapshots', [])
                        if snaps:
                            s = snaps[0]
                            ml = s.get('ml')
                            ou = s.get('ou')
                            snapshot_note = f"Snapshot ML {ml} | O/U {ou}"
                    except Exception:
                        pass
                score = 0
                try:
                    if ml is not None:
                        ml_num = int(str(ml))
                        if -145 <= ml_num <= 125:
                            score += 2
                        elif 125 < ml_num <= 150:
                            score += 1
                        elif ml_num > 150:
                            score -= 1
                    if ou and any(x in str(ou).lower() for x in ['7.0','7.5','8.0','8.5']):
                        score += 1
                except Exception:
                    pass
                ranked.append({
                    'event': ev.get('event'),
                    'url': ev.get('url'),
                    'snapshot_note': snapshot_note,
                    'score': score,
                })
            ranked = sorted(ranked, key=lambda x: x['score'], reverse=True)[:3]
            lines.append("**Top Looks Today (free MLB prototype)**")
            if not ranked:
                lines.append("- No MLB events extracted from Covers.")
            for i, ev in enumerate(ranked, 1):
                lines.append(f"{i}. **{ev.get('event')}**")
                lines.append(f"   - **Source:** Covers MLB")
                lines.append(f"   - **Public line snapshot:** {ev.get('snapshot_note')}")
                lines.append(f"   - **Link:** {ev.get('url')}")
                lines.append("")
            lines.append("**Bottom Line**")
            lines.append("- Free MLB mode now uses Covers matchup extraction plus public line snapshots. It is useful for public-source research, but still less precise than live multi-book API odds.")
            return '\n'.join(lines)
        except Exception:
            pass

    hints = []
    odds_hints = []
    try:
        cmd = [sys.executable, FREE_CONTEXT_SCRIPT, "--sports", *sports]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, env=os.environ.copy())
        hints = json.loads(proc.stdout).get("sports", [])
    except Exception:
        hints = []
    try:
        cmd = [sys.executable, FREE_ODDS_SCRIPT, "--sports", *sports]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, env=os.environ.copy())
        odds_hints = json.loads(proc.stdout).get("sports", [])
    except Exception:
        odds_hints = []

    lines.append("**Free-source plan**")
    if hints or odds_hints:
        by_sport = {}
        for item in hints:
            by_sport.setdefault(item.get('sport_key'), {}).update(item)
        for item in odds_hints:
            by_sport.setdefault(item.get('sport_key'), {}).update(item)
        for sport_key, item in by_sport.items():
            lines.append(f"- **{sport_key}**")
            for src in item.get("sources", []):
                lines.append(f"  - Context source: {src}")
            for q in item.get("queries", []):
                lines.append(f"  - Odds search: {q}")
            lines.append(f"  - {item.get('note')}")
    else:
        lines.append("- Covers / OddsShark / Yahoo Sports / AP / ESPN")

    lines.append("")
    lines.append("**Bottom Line**")
    lines.append("- Free mode is enabled. Use public web odds snapshots plus public article context instead of paid feeds.")
    return "\n".join(lines)


def render_report(top: List[Dict[str, Any]], detail: str = 'standard') -> str:
    lines = []
    lines.append("**GPTSportswriter — Best Betting Advice of the Day**")
    lines.append("**Date:** today")
    lines.append("**Scope:** Broad daily slate across in-season sports")
    lines.append("")
    lines.append("**Top Looks Today**")
    if not top:
        lines.append("- No picks cleared the current quality threshold today.")
        lines.append("")
    for i, pick in enumerate(top[:3], 1):
        lines.append(f"{i}. **{pick['event']}**")
        lines.append(f"   - **Market:** {pick['market']}")
        lines.append(f"   - **Lean:** {pick['lean']}")
        lines.append(f"   - **Current odds:** {pick['current_odds_range']}")
        lines.append(f"   - **Why this play:** {pick['why']}")
        lines.append(f"   - **Confidence:** {classify_confidence(pick['confidence_score'])}")
        if detail == 'deep' and pick.get('sport') == 'baseball_mlb':
            articles = run_asknews(f"{pick['event']} probable pitchers weather injuries betting preview", n_articles=1)
            weather_line = None
            try:
                wp = subprocess.run([sys.executable, MLB_WEATHER_SCRIPT, pick['event']], capture_output=True, text=True, check=True, env=os.environ.copy())
                weather_line = json.loads(wp.stdout).get('weather')
            except Exception:
                weather_line = None
            if weather_line:
                lines.append(f"   - **Weather:** {weather_line}")
            if articles:
                art = articles[0]
                summary = (art.get('summary') or '').strip().replace('\n', ' ')
                key_points = art.get('key_points') or []
                lines.append(f"   - **Extra context:** {summary[:260]}")
                if key_points:
                    lines.append(f"   - **Key players / injuries / trend:** {key_points[0]}")
        lines.append("")
    lines.append("**Consensus Signals**")
    lines.append("- Picks are ranked from current market structure first, then boosted by AskNews context when relevant.")
    lines.append("- NBA-style short spreads and sane moneylines are preferred over totals and baseball run lines.")
    lines.append("")
    lines.append("**Watch-Outs**")
    lines.append("- This is still a heuristic model, not a guaranteed edge finder.")
    lines.append("- Injury/news context can help, but late scratches can still flip a bet.")
    lines.append("- Re-run near tipoff/first pitch because lines move.")
    lines.append("")
    lines.append("**Bottom Line**")
    if top:
        best = top[0]
        lines.append(f"- The current top market-backed angle is **{best['lean']}** in **{best['event']}**, based on live odds plus AskNews context.")
    else:
        lines.append("- Nothing cleared the current no-pick threshold, so the board looks weak right now.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Generate a ranked GPTSportswriter report from live odds")
    ap.add_argument("--sports", nargs="*", default=["baseball_mlb", "basketball_nba"])
    ap.add_argument("--mode", default="auto", choices=["auto", "premium", "free"])
    ap.add_argument("--detail", default="standard", choices=["standard", "deep"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    data = run_fetch(args.sports, args.mode)
    free_mode_active = all((s.get('source') == 'free-web-fallback') for s in data.get('sports', []))
    if free_mode_active:
        if args.json:
            print(json.dumps({"mode": "free", "sports": data.get("sports", [])}, indent=2))
        else:
            print(render_free_mode_report(data, args.sports))
        return

    ranked = build_ranked(data)
    if args.json:
        print(json.dumps({"ranked": ranked[:10]}, indent=2))
    else:
        print(render_report(ranked, detail=args.detail))


if __name__ == "__main__":
    main()
