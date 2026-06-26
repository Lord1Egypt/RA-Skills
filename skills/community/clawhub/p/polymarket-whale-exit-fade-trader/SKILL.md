---
name: polymarket-whale-exit-fade-trader
description: Detects when multiple whale wallets exit positions simultaneously, causing market overshooting. Fades the panic by buying the dip after whale dumps, exploiting retail panic-selling that pushes prices below fair value.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Whale Exit Fade Trader
  difficulty: advanced
---

# Whale Exit Fade Trader

## Strategy

This skill monitors the top Polymarket wallets (via the predicting.top leaderboard) for coordinated exit events -- when multiple whales sell the same market within a configurable time window. When whale exits are detected, the skill fades the resulting panic by buying the dip.

### Why it works

Whale exits create a predictable cascade:

1. **Whale sells** -- large position unwind pushes price down.
2. **Retail panic** -- smaller traders see the drop and panic-sell, amplifying the move.
3. **Overshoot** -- the combined selling pushes the market below fair value.
4. **Reversion** -- once the panic subsides, the market recovers toward its fundamental value.

The edge comes from distinguishing between "whales exiting for portfolio reasons" (liquidity, rebalancing, profit-taking) versus "whales exiting on new information." In most cases, coordinated whale exits are portfolio-driven, not information-driven, making the overshoot a reliable fade opportunity.

## Signal Logic

### Exit Detection

1. Fetch top N wallets from the predicting.top leaderboard.
2. Pull recent activity for each wallet from the Polymarket data API.
3. Filter for SELL actions within the lookback window (default 24h).
4. Group sells by market title and outcome (YES/NO).
5. Flag markets where >= `MIN_EXIT_WHALES` distinct wallets sold >= `MIN_EXIT_VOLUME` USD.

### Fade Direction

- If whales **sold YES** and the market price dropped below `YES_THRESHOLD` -> **buy YES** (fade the dump).
- If whales **sold NO** and the market price rose above `NO_THRESHOLD` -> **buy NO** (fade the pump).

### Conviction Sizing

Base conviction comes from threshold distance (per CLAUDE.md standard):

- YES: `(YES_THRESHOLD - p) / YES_THRESHOLD`
- NO: `(p - NO_THRESHOLD) / (1 - NO_THRESHOLD)`

Enhanced by an **exit intensity multiplier**:

```
exit_mult = 1 + min(0.5, (exit_whale_count - 1) * 0.15 + min(0.2, exit_volume / 5000))
conviction = min(1.0, base_conviction * exit_mult)
size = max(MIN_TRADE, conviction * MAX_POSITION)
```

More whales exiting and higher exit volume increase the fade conviction, capped at 1.0.

## Edge Thesis

| Factor | Why it creates edge |
|---|---|
| Whale exit cascade | Large sells trigger retail panic, overshooting fair value |
| Information asymmetry | Most whale exits are portfolio-driven, not info-driven |
| Behavioral bias | Retail overreacts to visible whale selling |
| Mean reversion | Markets recover once panic selling exhausts itself |
| Multi-whale confirmation | Requiring 2+ whales selling filters noise from single-wallet rebalancing |

## Safety

| Safeguard | Description |
|---|---|
| Paper mode default | All trades are simulated unless `--live` is passed |
| Spread gate | Skips markets with bid-ask spread > `MAX_SPREAD` |
| Days gate | Skips markets resolving within `MIN_DAYS` |
| Position limit | Maximum `MAX_POSITIONS` trades per run |
| Flip-flop check | SDK context check prevents rapid reversals |
| Slippage check | Skips markets with > 15% expected slippage |
| Min exit whales | Requires multiple whales exiting, not just one |
| Min exit volume | Filters out trivially small exits |
| Conviction sizing | Position size scales with edge, never flat |

## Tunables

| Variable | Default | Description |
|---|---|---|
| `SIMMER_MAX_POSITION` | 40 | Max trade size (USD) |
| `SIMMER_MIN_TRADE` | 5 | Min trade size floor (USD) |
| `SIMMER_MIN_VOLUME` | 5000 | Min market volume (USD) |
| `SIMMER_MAX_SPREAD` | 0.12 | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | 5 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 6 | Max open positions per run |
| `SIMMER_YES_THRESHOLD` | 0.38 | Buy YES below this probability |
| `SIMMER_NO_THRESHOLD` | 0.62 | Buy NO above this probability |
| `SIMMER_EXIT_LOOKBACK_HOURS` | 24 | Window for exit detection (hours) |
| `SIMMER_MIN_EXIT_WHALES` | 2 | Min distinct whales selling for signal |
| `SIMMER_MIN_EXIT_VOLUME` | 500 | Min USD volume of whale exits |
| `SIMMER_LEADERBOARD_LIMIT` | 20 | Number of top wallets to scan |

## Remix Ideas

- **Time decay**: Weight recent exits higher than older ones within the window.
- **SmartScore filter**: Only track exits from whales above a SmartScore threshold.
- **Volume ratio**: Compare exit volume to market daily volume for relative sizing.
- **Multi-timeframe**: Run with 6h, 24h, and 48h lookbacks and only trade when all align.
- **Exit velocity**: Track how fast whales are exiting (sells per hour) for urgency signal.
- **Cross-market**: If whales exit multiple related markets, increase conviction on all.

## Dependency

- `simmer-sdk` (pip install simmer-sdk)
- `SIMMER_API_KEY` environment variable
- Public APIs: predicting.top (leaderboard), data-api.polymarket.com (activity)
