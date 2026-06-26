# Polymarket Real-time Query Skill

Query real-time prediction market data from [Polymarket](https://polymarket.com/) — odds, trending markets, sports schedules, live events, and more.

## Features

- **Sports Schedules** — NBA, NFL, MLB, NHL, EPL, La Liga, UCL, MLS, ATP, WTA, UFC, LOL, CS2, F1, PGA, Boxing, Cricket
- **Real-time Odds** — Current prices/probabilities for any market
- **Trending Markets** — Top markets by 24h volume across all categories
- **Live/In-Play** — Currently active sports markets
- **Market Search** — Find markets by keyword across sports, politics, crypto, etc.
- **Event Details** — Full event breakdowns with sub-markets (spreads, O/U, props)
- **Category Browsing** — Sports, politics, crypto, business, entertainment, AI

## Quick Start

### Python (cross-platform)

```bash
python polymarket_query.py trending --limit 10
python polymarket_query.py schedule --sport nba --date 2026-04-12
python polymarket_query.py search Bitcoin
python polymarket_query.py market 540816
```

### PowerShell (Windows)

```powershell
.\polymarket_query.ps1 -Command trending -Limit 10
.\polymarket_query.ps1 -Command schedule -Sport nba -Date 2026-04-12
.\polymarket_query.ps1 -Command search -Keyword "Bitcoin" -Limit 5
.\polymarket_query.ps1 -Command market -Id 540816
```

## Commands

| Command | Parameters | Description |
|---------|-----------|-------------|
| `categories` | — | List all market categories |
| `trending` | `--limit N` | Top trending markets by 24h volume |
| `search` | `<keyword>` `--limit N` | Search markets by keyword |
| `market` | `<market_id>` | Detailed market info with odds |
| `event` | `<event_id>` | Event with all sub-markets |
| `odds` | `<market_id>` | Focused odds for a market |
| `sports` | `--limit N` | Sports markets |
| `politics` | `--limit N` | Politics markets |
| `crypto` | `--limit N` | Crypto markets |
| `category` | `<slug>` `--limit N` | Markets in a category |
| `live` | — | Live/in-play sports markets |
| `schedule` | `--sport X` `--date YYYY-MM-DD` | Sports schedule by sport & date |

## Supported Sports

| Keyword | League | Keyword | League |
|---------|--------|---------|--------|
| `nba` / `basketball` | NBA | `ufc` / `mma` | UFC/MMA |
| `nfl` / `football` | NFL | `cs2` / `csgo` | Counter-Strike 2 |
| `mlb` / `baseball` | MLB | `lol` / `leagueoflegends` | League of Legends |
| `nhl` / `hockey` | NHL | `f1` / `racing` | Formula 1 |
| `epl` / `soccer` | English Premier League | `pga` / `golf` | PGA Golf |
| `laliga` | La Liga | `boxing` | Boxing |
| `ligue1` | Ligue 1 | `cricket` | Cricket |
| `seriea` | Serie A | `mls` | MLS |
| `ucl` / `championsleague` | UEFA Champions League | `atp` / `tennis` | ATP Tennis |
| `bundesliga` | Bundesliga | `wta` | WTA Tennis |

## How It Works

The tool queries Polymarket's public [Gamma API](https://gamma-api.polymarket.com) — no authentication required.

Key technical details:
- The API's `tag` and date-range parameters are unreliable for sport filtering
- Sport events are found by iterating `/events?order=volume24hr` and filtering by slug prefix client-side
- Game events follow the slug pattern `{sport}-{team1}-{team2}-{YYYY-MM-DD}`
- Award/season events follow `{sport}-{descriptor}-{id}`
- Boxing/fighting events use `{sport}-{fighter1}-vs-{fighter2}` pattern
- Team abbreviations may contain digits (e.g., `ucl-liv1-psg1`, `lol-ig1`, `ufc-cur1`)

## File Structure

```
polymarket/
├── SKILL.md                    # Skill definition (description, commands, workflow)
├── README.md                   # This file
├── references/
│   └── api_reference.md        # Polymarket API documentation
└── scripts/
    ├── polymarket_query.py     # Python version (cross-platform)
    └── polymarket_query.ps1    # PowerShell version (Windows)
```

## Requirements

- **Python 3.7+** (for Python version) — no external dependencies
- **PowerShell 5.1+** (for PowerShell version, Windows only)

No API keys or authentication needed — all data comes from Polymarket's public APIs.

## License

MIT
