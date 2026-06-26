# Kalshi Market Categories & Series Tickers

## API Base
- **Endpoint:** `api.elections.kalshi.com`
- **Auth:** RSA-PSS signature on `timestamp + method + path`

## Sports Series Tickers
| Series | Description | Edge Potential |
|--------|-------------|----------------|
| KXATPMATCH | ATP main draw matches | Low (1-3%) |
| KXATPCHALLENGERMATCH | ATP Challenger matches | HIGH (5-40%) |
| KXNCAAMBGAME | NCAAB men's games | Medium (2-9%) |
| KXNBA / KXNBAGAME | NBA games | None (efficient) |
| KXNHL / KXNHLGAME | NHL games | None (efficient) |
| KXSOCCER | Soccer matches | Low-Medium |
| KXMMA / KXUFCMATCH | MMA/UFC fights | Low |
| KXEPL / KXEPLGAME | EPL matches | Low |

## Weather Series Tickers
| Series | Description |
|--------|-------------|
| KXHIGHNY | NYC daily high temp |
| KXHIGHCHI | Chicago daily high temp |
| KXHIGHAUS | Austin daily high temp |
| KXHIGHMIA | Miami daily high temp |
| KXLOWNY | NYC daily low temp |

## Data Sources for De-Vigging
| Source | Coverage | Cost | Quality |
|--------|----------|------|---------|
| Sofascore | Tennis (all levels) | Free | Excellent for challengers |
| Odds API | Major sports | Free tier (500/mo) | Good for NBA/NHL/NCAAB |
| Pinnacle (via Odds API) | Everything | Via Odds API | Gold standard |
| Brave Search | Sportsbook lines | Free | Good for NCAAB |

## Best Edge Sources (Ranked)
1. ATP Challenger matches vs Sofascore de-vig
2. Small NCAAB conference tournaments vs sportsbook lines  
3. WTA lower-tier matches
4. Soccer qualifying matches
5. Weather (high variance — use with caution)
