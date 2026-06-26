#!/usr/bin/env python3
"""
Premier League scores via ESPN API
Supports: live scores, final results, goal scorers, bookings
"""
import urllib.request
import json

URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"

def get_team_name(team_id, competitors):
    for c in competitors:
        if c.get("team", {}).get("id") == str(team_id):
            return c.get("team", {}).get("shortDisplayName", "?")
    return "?"

def get_scores():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    
    events = data.get("events", [])
    if not events:
        print("No matches found — check back later")
        return
    
    print(f"Premier League — {len(events)} match(es)\n")
    
    for event in events:
        comp = event.get("competitions", [{}])[0]
        status = comp.get("status", {}).get("type", {})
        status_detail = status.get("shortDetail", "—")
        
        competitors = comp.get("competitors", [])
        teams = {}
        for c in competitors:
            hb = c.get("homeAway", "away")
            name = c.get("team", {}).get("shortDisplayName", "?")
            score = c.get("score", "—")
            teams[hb] = {"name": name, "score": score, "id": c.get("team", {}).get("id")}
        
        home = teams.get("home", {"name": "?", "score": "—", "id": None})
        away = teams.get("away", {"name": "?", "score": "—", "id": None})
        
        # Broadcast
        broadcasts = comp.get("broadcasts", [])
        channel = broadcasts[0]["names"][0] if broadcasts else "—"
        
        print(f"{home['name']} {home['score']} - {away['score']} {away['name']}")
        print(f"  [{status_detail}]  📺 {channel}")
        
        # Goal scorers
        details = comp.get("details", [])
        scorers = [d for d in details if d.get("scoringPlay")]
        if scorers:
            for s in scorers:
                player = s.get("athletesInvolved", [{}])[0]
                pname = player.get("shortName", player.get("displayName", "?"))
                minute = s.get("clock", {}).get("displayValue", "?")
                team_id = s.get("team", {}).get("id")
                team_abbr = get_team_name(team_id, competitors)
                penalty = " (pen)" if s.get("penaltyKick") else ""
                owngoal = " (og)" if s.get("ownGoal") else ""
                print(f"  ⚽ {minute} — {pname} ({team_abbr}){penalty}{owngoal}")
        
        # Bookings
        cards = [d for d in details if d.get("yellowCard") or d.get("redCard")]
        if cards:
            for card in cards:
                player = card.get("athletesInvolved", [{}])[0]
                pname = player.get("shortName", player.get("displayName", "?"))
                minute = card.get("clock", {}).get("displayValue", "?")
                team_id = card.get("team", {}).get("id")
                team_abbr = get_team_name(team_id, competitors)
                card_type = "🟨" if card.get("yellowCard") else "🟥"
                print(f"  {card_type} {minute} — {pname} ({team_abbr})")
        
        print()

if __name__ == "__main__":
    get_scores()
