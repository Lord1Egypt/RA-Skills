---
name: polymarket-query
version: 1.5.0
description: >
  This skill should be used when the user wants to query real-time data from Polymarket
  (https://polymarket.com/), including market categories, trending markets, event details,
  market odds/prices, live/in-play sports markets, and search for specific prediction markets
  across all categories such as sports, politics, crypto, business, entertainment, and more.
  It provides access to Polymarket's public Gamma API and CLOB API for real-time odds,
  volumes, and market information.
metadata:
  openclaw:
    slug: polymarket-query
    requires:
      bins:
        - python
    primaryEnv: ""
    homepage: "https://github.com/Amurtiger01/polymarket-skill"
---

# Polymarket Real-time Query Skill

## Purpose

Query real-time prediction market data from Polymarket, including:
- All market categories (Sports, Politics, Crypto, Business, Entertainment, AI, etc.)
- Current odds/prices for any market
- Trending and most actively traded markets
- Live/in-play sports markets
- Search for specific markets by keyword
- Detailed event and market information with sub-markets

## When to Use

Use this skill when the user asks about:
- Polymarket markets, odds, or predictions
- Current betting odds for events (sports, politics, crypto, etc.)
- Live or in-play markets
- Trending prediction markets
- Specific market or event details on Polymarket
- Prediction market probabilities for real-world events

## How to Use

### Primary Tool: Python Query Script

Execute the bundled Python script `scripts/polymarket_query.py` to query Polymarket data:

```bash
python "<skill_dir>/scripts/polymarket_query.py" <command> [options]
```

A PowerShell version (`scripts/polymarket_query.ps1`) is available in the [GitHub repository](https://github.com/Amurtiger01/polymarket-skill) but is not included in the ClawHub package due to file type restrictions.

### Schedule Sport Keywords

When using the `schedule` command, supported sport keywords are:
- `nba`, `basketball` → NBA
- `nfl`, `football` → NFL
- `mlb`, `baseball` → MLB
- `nhl`, `hockey` → NHL
- `soccer`, `epl`, `premierleague` → English Premier League
- `laliga` → La Liga
- `ligue1` → Ligue 1
- `ucl`, `championsleague` → UEFA Champions League
- `mls` → MLS
- `atp`, `tennis` → ATP Tennis
- `wta` → WTA Tennis
- `ufc`, `mma` → UFC/MMA
- `cs2`, `csgo` → Counter-Strike 2
- `lol`, `leagueoflegends` → League of Legends
- `f1`, `racing` → Formula 1
- `pga`, `golf` → PGA Golf
- `boxing` → Boxing
- `cricket` → Cricket

### Available Commands

| Command | Parameters | Description |
|---------|-----------|-------------|
| `categories` | — | List all market categories and sub-categories |
| `trending` | `--limit N` (default 10) | Show top trending markets by 24h volume |
| `search` | `--keyword X` `--limit N` | Search markets by keyword in question/description |
| `market` | `ID` | Get detailed market info with odds, volume, dates |
| `event` | `ID` | Get event with all sub-markets and their odds |
| `odds` | `ID` | Get focused odds/prices for a market |
| `sports` | `--limit N` (default 10) | Show sports markets |
| `politics` | `--limit N` (default 10) | Show politics markets |
| `crypto` | `--limit N` (default 10) | Show crypto markets |
| `category` | `--slug X` `--limit N` | Markets in a specific category slug |
| `live` | — | Show live/in-play sports markets |
| `schedule` | `--sport X` `--date YYYY-MM-DD` | Show sports schedule by sport & date |

### Execution Examples

```bash
# List all categories
python "<skill_dir>/scripts/polymarket_query.py" categories

# Top 10 trending markets
python "<skill_dir>/scripts/polymarket_query.py" trending --limit 10

# Search for Bitcoin markets
python "<skill_dir>/scripts/polymarket_query.py" search --keyword "Bitcoin" --limit 5

# Get market details
python "<skill_dir>/scripts/polymarket_query.py" market 1862566

# Get odds for a specific market
python "<skill_dir>/scripts/polymarket_query.py" odds 1862566

# Get event details with sub-markets
python "<skill_dir>/scripts/polymarket_query.py" event 320112

# Show sports markets
python "<skill_dir>/scripts/polymarket_query.py" sports --limit 15

# Show live/in-play markets
python "<skill_dir>/scripts/polymarket_query.py" live

# Show NBA schedule for a specific date
python "<skill_dir>/scripts/polymarket_query.py" schedule --sport nba --date 2026-04-12

# Show soccer/EPL schedule
python "<skill_dir>/scripts/polymarket_query.py" schedule --sport soccer --date 2026-04-12
```

### Workflow

1. **Identify user intent**: Determine what type of Polymarket data the user wants
2. **Select appropriate command**: Choose the script command that best matches the query
3. **Execute the script**: Run the Python script using `execute_command` tool
4. **Format the response**: Present the results in a clear, readable format to the user in their language

### Common Query Patterns

- "Polymarket上有什么热门的？" → Use `trending` command
- "X的赔率是多少？" → Use `search` to find the market, then `odds` or `market` with the market ID
- "有什么体育比赛市场？" → Use `sports` command
- "有哪些政治预测市场？" → Use `politics` command
- "有什么正在进行的比赛？" → Use `live` command
- "搜索比特币相关市场" → Use `search --keyword "Bitcoin"` command
- "Polymarket有哪些分类？" → Use `categories` command
- "今天NBA有什么比赛？" → Use `schedule --sport nba --date YYYY-MM-DD` command
- "4月12日的足球比赛" → Use `schedule --sport soccer --date 2026-04-12` command

### Understanding Odds

Polymarket uses a price-based system where:
- Price ranges from 0 to 1 (displayed as percentage, e.g., 65%)
- A "Yes" price of 0.65 means the market thinks there's a 65% probability
- Implied odds = 1 / price (e.g., 0.65 → 1.54x)
- For multi-outcome markets (e.g., "Who will win X?"), each option has its own price

### Direct API Fallback

If the script is unavailable or needs adjustment, query the Gamma API directly:

```bash
curl "https://gamma-api.polymarket.com/markets?limit=10&active=true&closed=false&order=volume24hr&ascending=false"
curl "https://gamma-api.polymarket.com/markets/{market_id}"
curl "https://gamma-api.polymarket.com/events/{event_id}"
curl "https://gamma-api.polymarket.com/categories"
```

For detailed API documentation, refer to `references/api_reference.md`.

### Important Notes

- Polymarket is a **prediction market** (not a traditional sportsbook). "Odds" represent probability estimates, not fixed payouts.
- There is no "real-time score" feed in the Polymarket API — for live scores of sports events, consult sports-specific APIs. However, price movements on Polymarket often reflect game progress.
- Market data is updated frequently but may have slight delays (typically seconds to minutes).
- The Python script uses `certifi` for SSL certificate verification if available, otherwise tries system CA bundles. On Windows systems without `certifi`, it falls back to disabling cert verification with a warning. Install `certifi` (`pip install certifi`) for secure connections.
- A PowerShell version is available in the [GitHub repository](https://github.com/Amurtiger01/polymarket-skill) for Windows users who prefer it.
- Category slugs for direct filtering: `sports`, `politics`, `crypto`, `business`, `coronavirus`, `pop-culture`, `science`, `ai`
