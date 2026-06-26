---
name: polymarket-esports-trader
description: Trades esports tournament, game release, and streaming milestone prediction markets on Polymarket. Exploits three stacked edges — game data richness (HLTV Elo, Oracle's Elixir), series format variance reduction (Bo5 vs Bo1), and Asian session timing lag for Korean/Chinese team matches.
metadata:
  author: snetripp
  version: "1.0"
  displayName: Esports & Gaming Trader
  difficulty: intermediate
---

# Esports & Gaming Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `esports_bias()` — three stacked structural edges, no external API required.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Esports markets are mispriced in two directions simultaneously. Data-rich titles (CS2, LoL, Dota 2) have published Elo models, map win rates, and patch-level performance metrics that retail ignores entirely. At the same time, fan-favourite teams (T1/Faker) are systematically overcrowded by fanbases trading loyalty rather than skill assessment. Three structural edges compound cleanly without any API.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Esports Bias

1. Discover active esports and gaming markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `esports_bias()` — three layers: game data quality × series format × Asian session timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Esports Bias (built-in, no API required)

**Layer 1 — Game / Market Type**

| Game / market type | Multiplier | Key data source retail ignores |
|---|---|---|
| T1 / Faker markets | **0.75x** | Fandom overcrowds YES by 10–20% vs Elo model — documented 2023–2025 |
| CS2 / Counter-Strike | **1.20x** | HLTV.org Elo ratings, map win rates, head-to-head history |
| League of Legends (non-T1) | **1.15x** | Oracle's Elixir patch-level stats — meta shifts change team win rates ±15% |
| Dota 2 / The International | **1.15x** | OpenDota comprehensive match stats — consistency rewarded in long series |
| Valorant / VCT | **1.10x** | VLR.gg agent win rates, map pools — growing and increasingly accurate |
| Mobile esports (HoK, PUBG Mobile, MLBB) | **1.15x** | Deep Asian stats with Western info lag |
| Game release date milestone | **1.10x** | Publisher delay history documented — ~70% re-delay rate for prior delayers |
| Twitch / streaming peak viewership | **1.10x** | TwitchTracker daily historical peaks — viewership growth curves trackable |
| Steam concurrent player milestone | **1.10x** | SteamCharts real-time — launch peaks predictable from pre-order velocity |

**The T1 / Faker Rule** — The most precisely documented single-team overcrowding in all of esports. Faker's global fandom spans every region, every language, every platform. The result is systematic YES overpricing on T1 outcomes by 10–20% relative to what HLTV/Oracle's Elixir Elo models imply. T1 are genuinely elite — but the *market price* of T1 wins is almost always too high because the fan base is the dominant pricing force, not analysts. This is not a bet against T1 — it is a sizing discipline: trade T1 markets very conservatively.

**Layer 2 — Series Format: Variance Reduction by Match Length**

This is the cleanest mechanic in the entire trader — no data needed, just understanding how best-of series work:

| Format | Multiplier | Statistical reality |
|---|---|---|
| Bo5 / Grand Final / Championship | **1.20x** | Stronger team wins ~72–78% — retail says "anything can happen" which is statistically false |
| Bo3 / Playoff / Semifinal / Elimination | **1.10x** | Stronger team wins ~65–70% — meaningful variance reduction |
| Bo1 / Group Stage / Swiss / Round Robin | **0.90x** | ~40% upset rate — genuine uncertainty, reduce conviction |

The Grand Final insight: retail treats championship matches as the most uncertain because "the stakes are highest." The opposite is true statistically. Teams playing Bo5 Grand Finals have survived multiple elimination rounds — they are the two best teams in the tournament, playing the format that most reliably selects the winner. This is maximum-edge territory, not minimum.

**Layer 3 — Asian Session Timing**

LoL LCK/LPL, mobile esports, and Dota 2 SEA feature Korean, Chinese, and Southeast Asian teams competing at 01:00–09:00 UTC. Polymarket is US-dominated — match results in these regions take 30–90 minutes to fully reprice when US retail is asleep.

| Condition | Multiplier |
|---|---|
| Asian-dominant game + 01:00–09:00 UTC | **1.15x** — lag window open |
| All other times | **1.00x** |

### Combined Examples

| Market | Type | Format | Timing | Final bias |
|---|---|---|---|---|
| CS2 Bo5 Grand Final | 1.20x | 1.20x | 1.0x | **1.35x cap** |
| T1 Bo3 match | 0.75x | 1.10x | 1.0x | **0.83x** |
| LoL LCK Bo5 at 04:00 UTC | 1.15x | 1.20x | 1.15x | **1.35x cap** |
| Dota 2 Bo1 group stage | 1.15x | 0.90x | 1.0x | **1.04x** |
| Any Bo1 group match | type_mult | **0.90x** | 1.0x | Edge compressed |

### Keywords Monitored

```
esports, League of Legends, CS2, Counter-Strike, Dota 2, Valorant, Fortnite,
World Championship, tournament, Steam, Twitch, game release, PlayStation,
Xbox, Nintendo, gaming revenue, Riot Games, Blizzard, grand final, bracket,
LCK, LPL, LEC, BLAST, ESL, VCT, The International, HLTV, peak viewers,
concurrent players, T1, Faker, NaVi, Vitality, patch
```

### Remix Signal Ideas

- **HLTV.org Elo ratings**: Compare published Elo-implied win probability to Polymarket price for CS2 matchup markets — the gap is consistently 8–15% for non-marquee matches
- **Oracle's Elixir**: LoL team stats by patch — when a meta patch hits 2 days before a tournament, markets haven't adjusted; the data has
- **Liquipedia API**: Real-time bracket data, match results, team stats for 30+ esports titles — feed bracket position into p to trade next-round markets
- **TwitchTracker**: Daily peak viewer history for "will X reach Y viewers" markets — compare trajectory to market price


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `20` | Max USDC per trade — reflects esports market liquidity |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `2` | Min days until resolution — tournaments move fast |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
