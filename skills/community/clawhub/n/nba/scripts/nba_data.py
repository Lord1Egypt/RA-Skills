#!/usr/bin/env python3
"""
NBA Data Fetcher
Fetches today's NBA schedule/scores and standings from NBA CDN & StatMuse.
Usage:
  python nba_data.py scoreboard       # today's games + live scores
  python nba_data.py standings        # current season standings
  python nba_data.py all              # both
"""

import sys
import json
import urllib.request
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/html, */*",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())

def fetch_text(url):
    req = urllib.request.Request(url, headers={**HEADERS, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def get_scoreboard():
    """Fetch today's NBA scoreboard from NBA CDN live data."""
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    try:
        data = fetch_json(url)
        sb = data["scoreboard"]
        game_date = sb.get("gameDate", "Unknown")
        games = sb.get("games", [])

        print(f"\n🏀 NBA Schedule — {game_date}\n{'='*50}")
        if not games:
            print("  No games scheduled today.")
            return

        for g in games:
            status_text = g.get("gameStatusText", "")
            home = g["homeTeam"]
            away = g["awayTeam"]
            ht = f"{home['teamCity']} {home['teamName']} ({home['wins']}-{home['losses']})"
            at = f"{away['teamCity']} {away['teamName']} ({away['wins']}-{away['losses']})"
            status = g.get("gameStatus", 1)

            # Game time (ET)
            game_time_utc = g.get("gameTimeUTC", "")
            try:
                gt = datetime.fromisoformat(g.get("gameEt", "").replace("Z", "+00:00"))
                time_str = gt.strftime("%I:%M %p ET")
            except Exception:
                time_str = ""

            if status == 1:
                # Upcoming
                print(f"\n  🕐 {at} @ {ht}")
                print(f"     Tip-off: {time_str}")
            elif status == 2:
                # Live
                hs = home.get("score", 0)
                as_ = away.get("score", 0)
                period = g.get("period", 0)
                clock_raw = g.get("gameClock", "")
                # Parse clock e.g. PT04M17.00S
                clock_str = status_text
                print(f"\n  🔴 LIVE  {at} {as_} @ {ht} {hs}  [{clock_str}]")
                # Leaders
                hl = g.get("gameLeaders", {}).get("homeLeaders", {})
                al = g.get("gameLeaders", {}).get("awayLeaders", {})
                if hl.get("name"):
                    print(f"     🏠 {hl['name']}: {hl['points']}pts {hl['rebounds']}reb {hl['assists']}ast")
                if al.get("name"):
                    print(f"     ✈️  {al['name']}: {al['points']}pts {al['rebounds']}reb {al['assists']}ast")
            else:
                # Final
                hs = home.get("score", 0)
                as_ = away.get("score", 0)
                winner = ht if hs > as_ else at
                print(f"\n  ✅ FINAL  {at} {as_} @ {ht} {hs}")
                hl = g.get("gameLeaders", {}).get("homeLeaders", {})
                al = g.get("gameLeaders", {}).get("awayLeaders", {})
                if hl.get("name"):
                    print(f"     🏠 {hl['name']}: {hl['points']}pts {hl['rebounds']}reb {hl['assists']}ast")
                if al.get("name"):
                    print(f"     ✈️  {al['name']}: {al['points']}pts {al['rebounds']}reb {al['assists']}ast")

        print()
    except Exception as e:
        print(f"  ❌ Error fetching scoreboard: {e}")
        print("  Fallback: https://www.nba.com/schedule")

def get_standings():
    """Fetch NBA standings from StatMuse (natural language query)."""
    # StatMuse natural language queries return readable summaries
    queries = [
        ("Eastern Conference", "https://www.statmuse.com/nba/ask/nba-2025-26-eastern-conference-standings"),
        ("Western Conference", "https://www.statmuse.com/nba/ask/nba-2025-26-western-conference-standings"),
    ]
    print(f"\n📊 NBA Standings 2025-26\n{'='*50}")
    for label, url in queries:
        try:
            import re
            html = fetch_text(url)
            # Extract readable text from StatMuse response
            # StatMuse renders standings as table rows in HTML
            # Look for team records pattern
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
            if rows:
                print(f"\n{label}:")
                for row in rows[:16]:  # max 15 teams per conference + header
                    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                    clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                    clean = [c for c in clean if c]
                    if len(clean) >= 4:
                        print(f"  {' | '.join(clean[:6])}")
            else:
                # Fallback: try meta description or og:description
                meta = re.search(r'<meta\s+(?:name="description"|property="og:description")\s+content="([^"]+)"', html)
                if meta:
                    print(f"\n{label}:\n  {meta.group(1)}")
                else:
                    print(f"\n{label}: See https://www.statmuse.com/nba/ask/nba-standings-today")
        except Exception as e:
            print(f"\n{label}: ❌ Error — {e}")

    print(f"\n  Full standings: https://www.statmuse.com/nba/ask/nba-2025-26-standings")
    print(f"  More detail:   https://www.nba.com/standings\n")

def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if cmd in ("scoreboard", "schedule", "scores", "games"):
        get_scoreboard()
    elif cmd in ("standings", "stand"):
        get_standings()
    else:
        get_scoreboard()
        get_standings()

if __name__ == "__main__":
    main()
