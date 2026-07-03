---
name: kalshi-fifa-soccer-trader
description: Trade Kalshi soccer markets using EA FC OVR rating disparity and a bivariate Poisson model. Finds edge on match winner, total goals (over/under), and goal spread markets. Use when the user wants to trade soccer markets on Kalshi, automate soccer bets using FIFA ratings, or find mispriced soccer outcomes.
category: world-cup
tags:
  - world-cup
  - kalshi
  - soccer
  - poisson
  - wc2026
metadata:
  author: Simmer (@simmer_markets)
  version: "0.1.0"
  displayName: Kalshi FIFA Soccer Trader
  difficulty: intermediate
  primaryEnv: SIMMER_API_KEY
  envVars:
    - name: SIMMER_API_KEY
      required: true
      description: "Your Simmer SDK API key — get from simmer.markets/dashboard"
    - name: SOLANA_PRIVATE_KEY
      required: true
      description: "Solana wallet private key (base58) for signing DFlow trades. Kalshi has no managed-wallet mode — self-custody only. Never commit."
---
# Kalshi FIFA Soccer Trader

Trade soccer markets on Kalshi using EA FC OVR rating disparity as the signal, executed via DFlow on Solana.

> 🚨 **Framework, not a production trading system.** Read [DISCLAIMER.md](./DISCLAIMER.md) before connecting a wallet with real funds.

> **This is a template.** The default signal is EA FC OVR disparity fed through a bivariate Poisson goal model. Remix it: swap in Elo ratings, add in-play context, or filter by tournament. The skill handles market discovery, model scoring, de-vigging, and trade execution. Your alpha is the input.

> **Defaults: dry-run mode, max $5 USDC per trade, minimum 6% EV edge required.** Pass `--live` to enable real trades; set `SIMMER_SOCCER_MAX_POSITION_USD` and `SIMMER_SOCCER_ENTRY_EDGE` to adjust.

> **Powered by DFlow.** Kalshi trades execute via DFlow's Solana-based prediction market infrastructure. KYC through Proof is required for buys.

## When to Use This Skill

Use when the user wants to:
- Trade Kalshi soccer match winner, total goals, or goal spread markets
- Use EA FC OVR ratings to find pricing edges against the market
- Automate position management across multiple upcoming soccer matches
- Backtest or dry-run the Poisson goal model against live Kalshi prices

## Strategy

EA FC OVR disparity → bivariate Poisson → probability grid → de-vig vs Kalshi prices → EV-positive trades.

**Three market types handled:**
- **Match winner** — P(home win) / P(draw) / P(away win) vs the YES/NO price
- **Total goals** — P(total goals > line) vs the over market price
- **Goal spread** — P(home wins by ≥ N goals) vs the spread market price

**Model in brief:**
1. Look up both teams' EA FC OVR in `ratings.json` (top ~200 clubs + all national teams)
2. Convert OVR disparity → expected goals per team (λ_home, λ_away) via log-linear model with home advantage
3. Build a 10×10 joint Poisson goal grid
4. Sum grid cells to get probabilities for each market type
5. De-vig the Kalshi YES/NO prices to implied probability
6. Edge = model probability − implied probability
7. Trade when edge > threshold and safeguards pass

## Setup

1. **Install the Simmer SDK**
   ```bash
   pip install simmer-sdk
   ```

2. **Set your Simmer API key**
   ```bash
   export SIMMER_API_KEY=...   # simmer.markets/dashboard → SDK tab
   ```

3. **Set your Solana private key** (live trading only)
   ```bash
   export SOLANA_PRIVATE_KEY=<base58-encoded-secret-key>
   ```

4. **Complete KYC** (required for buys on Kalshi)
   - Verify at [dflow.net/proof](https://dflow.net/proof)
   - Check status: `curl "https://api.simmer.markets/api/proof/status?wallet=YOUR_SOLANA_ADDRESS"`

5. **Fund wallet**
   - SOL on Solana mainnet for gas (~0.05 SOL)
   - USDC on Solana mainnet for capital

6. **Import soccer markets** (first run)
   ```bash
   python soccer_trader.py --import-markets
   ```

7. **Dry run first — always**
   ```bash
   python soccer_trader.py
   ```

## Configuration

| Setting | Env var | Default | Description |
|---------|---------|---------|-------------|
| Entry edge | `SIMMER_SOCCER_ENTRY_EDGE` | 0.06 | Min EV edge to trade (6%) |
| Exit threshold | `SIMMER_SOCCER_EXIT_THRESHOLD` | 0.90 | Sell when implied prob reaches this |
| Max position | `SIMMER_SOCCER_MAX_POSITION_USD` | 5.00 | Max USDC per trade |
| Max trades/run | `SIMMER_SOCCER_MAX_TRADES_PER_RUN` | 5 | Cap per scan cycle |
| Market types | `SIMMER_SOCCER_MARKET_TYPES` | winner,totals,spread | Which market types to trade (comma-sep) |
| Min liquidity | `SIMMER_SOCCER_MIN_LIQUIDITY` | 500 | Skip markets with liquidity below this USD |
| Slippage max | `SIMMER_SOCCER_SLIPPAGE_MAX` | 0.10 | Skip if estimated slippage > 10% |
| Smart sizing % | `SIMMER_SOCCER_SIZING_PCT` | 0.04 | % of balance per trade (with --smart-sizing) |
| Home advantage | `SIMMER_SOCCER_HOME_BOOST` | 0.12 | Log-scale home goal boost (0 = neutral venue) |

## Quick Commands

```bash
# Status + open positions
python scripts/status.py

# Positions only
python scripts/status.py --positions

# Full P&L
python scripts/status.py --pnl
```

## Running the Skill

```bash
# Dry run (default) — shows edge but no trades
python soccer_trader.py

# Live trading
python soccer_trader.py --live

# Smart position sizing from portfolio balance
python soccer_trader.py --live --smart-sizing

# Only trade match winner markets
python soccer_trader.py --live --market-types winner

# Only totals and spread
python soccer_trader.py --live --market-types totals,spread

# Import new Kalshi soccer markets
python soccer_trader.py --import-markets

# Show current model config and ratings loaded
python soccer_trader.py --config

# Quiet — only print on trades/errors (ideal for cron)
python soccer_trader.py --live --smart-sizing --quiet

# Manage open positions (exit anything above threshold)
python soccer_trader.py --live --manage-positions
```

## How It Works

Each cycle:
1. Fetch active soccer markets from Simmer API (filtered by `import_source=kalshi` + soccer keywords)
2. Parse team names and market type from each market's title/question
3. Look up EA FC OVR for each team from `ratings.json` (fuzzy match on team aliases)
4. Compute λ_home and λ_away from OVR disparity
5. Build 10×10 Poisson goal grid
6. Derive model probability for the market's YES outcome
7. De-vig Kalshi YES/NO prices to implied fair probability
8. Edge = model_prob − implied_prob
9. **Safeguards**: check time-to-resolution, slippage, flip-flop, liquidity
10. Buy YES if edge > entry threshold (or NO if negative edge is large enough)
11. Tag every trade with `signal_data` (OVRs, λs, model prob, edge, market type) for backtesting

## Ratings

Team OVR ratings live in `ratings.json`. The skill uses a three-layer hierarchy to compute each team's effective OVR:

1. **Formation-aware** (`lineup_intel.py`) — picks the best XI for a given formation (default 4-3-3) by position group, then adjusts for confirmed absences from `lineup_cache.json`
2. **`top11_avg_ovr`** — average OVR of the best 11 players (fallback if no player data)
3. **`ovr`** — composite team OVR including bench (last resort)

Fields per team:
| Field | Description |
|-------|-------------|
| `ovr` | Composite team OVR (bench included) |
| `att` / `mid` / `def` | Positional ratings |
| `top11_avg_ovr` | Average OVR of the best 11 players |
| `players` | List of `{name, ovr, position}` — used by lineup intel |
| `aliases` | Fuzzy-match list for Kalshi market title parsing |

## Lineup Intelligence

`lineup_intel.py` adds formation-aware OVR and injury signal detection on top of the static ratings.

```bash
# Step 1 (run once, or to refresh): load official WC 2026 squads from Wikipedia
python3 scripts/fetch_wc_squads.py              # all 48 WC teams
python3 scripts/fetch_wc_squads.py Spain France # specific teams only
python3 scripts/fetch_wc_squads.py --dry-run Spain  # preview without writing

# Step 2 (optional): augment with recent match lineup data from TheSportsDB
python3 scripts/fetch_lineups.py Sweden Tunisia
python3 scripts/fetch_lineups.py --all          # all teams in ratings.json
python3 scripts/fetch_lineups.py --demo Spain "Cape Verde"   # prediction demo

# Cached output: lineup_cache.json
```

**What it does:**
- **`fetch_wc_squads.py`** — fetches all 48 official WC 2026 squad lists from Wikipedia (no API key, no rate limits). Populates `lineup_cache.json` with the full 26-man roster per team. Run this first so injury signals only fire for players genuinely excluded from the squad.
- **`fetch_lineups.py`** — pulls last 5 matches per team from TheSportsDB and merges confirmed match starters into the existing squad cache (Wikipedia squad data is preserved, not replaced).
- Builds a formation XI (default 4-3-3) from `ratings.json` player data by position group
- Flags top-5 players not seen in the official squad as possible injury/exclusion
- Warns when lineup data is stale (> 90 days since last match)
- OVR is transparently adjusted in `lineup_intel.py` — no changes needed in trading logic

**Injury flag example:**
```
❓ V. Gyöker... (OVR 82) — not confirmed in last 1 lineup(s); possible injury/rest
⚠  Most recent data is 174d old (Tunisia 3-1 Uganda)
```

> **Recommended workflow:** run `fetch_wc_squads.py` once before a tournament to seed accurate squad data, then `fetch_lineups.py` before individual matches for recent form signals. TheSportsDB free tier returns only ~3 starters per match — use it as a supplement to the Wikipedia squad, not a replacement.

**Refresh from SoFIFA** (Chrome must be closed due to profile lock):
```bash
# 1. Quit Chrome (Cmd+Q on macOS)
# 2. Scrape EA FC 26 ratings for all 48 WC 2026 teams
node scripts/scrape_sofifa.mjs

# 3. Merge scraped data into ratings.json
python3 scripts/merge_sofifa.py

# 4. Re-open Chrome
```

**Add a missing team manually:**
```json
{
  "name": "Team Name",
  "ovr": 83,
  "att": 83, "mid": 82, "def": 81,
  "top11_avg_ovr": 84,
  "aliases": ["alternate name", "abbreviation", "country code"]
}
```

If a team can't be matched, the market is skipped with a warning. Add the team name (or an alias) to `ratings.json` to include it.

## Safeguards

- **Time decay**: Skip markets resolving in < 3 hours (spreads/winner) or < 1 hour (totals — goals can come late)
- **Slippage**: Skip if estimated market slippage > 10%
- **Flip-flop**: Skip if you've reversed direction on this market recently
- **Liquidity**: Skip if market liquidity < min threshold
- **Both teams unknown**: Skip if either team not found in ratings

Disable with `--no-safeguards` (not recommended).

## Troubleshooting

**"Team not found in ratings: [name]"**
- The market title's team name didn't fuzzy-match any entry in `ratings.json`
- Add the team or alias: edit `ratings.json` and add the name to its `aliases` list

**"No soccer markets found"**
- Run `python soccer_trader.py --import-markets` to discover and import Kalshi soccer markets
- Check that Kalshi has active soccer markets (tournament may be between matches)

**"KYC verification required"**
- Complete at [dflow.net/proof](https://dflow.net/proof)

**"SOLANA_PRIVATE_KEY not set"**
- Only needed for `--live`. Dry-run works without it.

**"Insufficient SOL for transaction fees"**
- Fund Solana wallet with at least 0.05 SOL

**Kalshi maintenance window**
- Kalshi's clearinghouse has weekly maintenance Thursdays 3:00–5:00 AM ET — trades during this window will fail
