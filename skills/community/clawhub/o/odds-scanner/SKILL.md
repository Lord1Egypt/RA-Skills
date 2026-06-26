---
name: odds-scanner
description: "Fetch live sports betting odds from 20+ sportsbooks and compare lines. Supports NFL, NBA, MLB, NHL, soccer, and 30+ sports. Use when asked about odds, lines, spreads, totals, or sportsbook comparison."
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["curl", "jq"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# Sports Odds Scanner

Fetch and compare live betting odds from 20+ sportsbooks via The Odds API.

## When to Use

Use this skill when the user asks about:
- Current odds, lines, spreads, or totals for any sport
- Comparing sportsbook lines for a specific game
- Finding the best available line
- Which sportsbooks have the sharpest odds
- Vig or hold percentage for a market

## Sport Keys

Common sport keys for the API:

| Sport | Key |
|-------|-----|
| NFL | americanfootball_nfl |
| NCAA Football | americanfootball_ncaaf |
| NBA | basketball_nba |
| NCAA Basketball | basketball_ncaab |
| MLB | baseball_mlb |
| NHL | icehockey_nhl |
| EPL | soccer_epl |
| MLS | soccer_usa_mls |
| La Liga | soccer_spain_la_liga |
| Champions League | soccer_uefa_champions_league |
| UFC/MMA | mma_mixed_martial_arts |
| FIFA World Cup | soccer_fifa_world_cup |

For the full list, run the "List active sports" command below.

## Operations

### 1. List Active Sports

Show which sports currently have odds:

```bash
curl -s "https://api.the-odds-api.com/v4/sports?apiKey=$ODDS_API_KEY" \
  | jq '[.[] | select(.active==true) | {key, title, description}]'

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-odds-scanner-skill/](https://agentbets.ai/guides/openclaw-odds-scanner-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
