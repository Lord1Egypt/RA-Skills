---
name: polymarket-smart-money
description: "Discover, analyze, and filter Polymarket smart money wallets. Use when asked to find profitable traders, analyze wallet addresses, detect market makers or HFT bots, assess copy-trading reliability, run the smart money discovery pipeline, or check if a Polymarket address is suitable for copy trading. Triggers on: find smart money, analyze wallet, discover traders, is this a market maker, copy trading, leaderboard, 聪明钱, 做市商检测, 跟单可靠性."
---

# Polymarket Smart Money Discovery & Analysis

Discover profitable Polymarket traders, filter out market makers and HFT bots, and assess copy-trading reliability.

## Project Location

```
{baseDir}/../../agents/polymarket-bot/PolyAnalysis/
```

Activate the virtualenv before running any script:

```bash
cd {baseDir}/../../agents/polymarket-bot/PolyAnalysis
source .venv/bin/activate
```

## Quick Commands

### Analyze a single wallet

```bash
python analyze.py <address>
python analyze.py <address> --force   # force full refresh
python analyze.py <address> --json    # JSON output
```

The report includes:
- PnL, ROI, win rate
- Entry timing analysis
- Copy trading score (0-100)
- **MM/HFT detection** (MM Score, is_market_maker, is_hft)
- **Copy reliability label** (🟢 高可靠 / 🟡 中可靠 / 🔴 低可靠 / ❌ 不可跟单)

### Discover smart money (batch)

```bash
python analyze.py discover --top-n 10
python analyze.py discover --top-n 20 --min-profit 100000 --min-volume 500000
python analyze.py discover --top-n 10 --output-json --output-file smart_money.json
```

Discovery pipeline:
1. Fetch from Polymarket v1 Leaderboard API (7 strategies)
2. Deduplicate across dimensions
3. Stage 1 pre-filter: PnL/Vol < 3% → exclude (likely market maker)
4. Fetch activity data for remaining addresses
5. Stage 2 deep analysis: MM Score + HFT detection
6. Exclude "❌ 不可跟单" addresses
7. Rank by copy trading score

### Cache management

```bash
python analyze.py cache list
python analyze.py cache stats
python analyze.py cache clear <address>
python analyze.py cache clear --all
```

## Filtering Pipeline

### Stage 1: Pre-filter (from leaderboard data, zero cost)

| Rule | Threshold | Rationale |
|------|-----------|-----------|
| PnL/Vol ratio | < 3% → exclude | Market makers earn tiny spreads on huge volume |
| VOL-only listing | exclude | Only on volume leaderboard, not on any PNL leaderboard |

### Stage 2: Deep analysis (from activity data)

#### MM Score (0-100, weighted)

| Indicator | Weight | Market Maker Signal |
|-----------|--------|-------------------|
| PnL/Vol ratio | 30% | < 1% |
| Decision frequency (positions/day) | 25% | > 50/day |
| Buy/sell balance | 20% | > 0.7 (near 1:1) |
| Avg holding time | 15% | < 1 hour |
| Trade amount uniformity (CV) | 10% | < 0.3 |

MM Score > 50 → flagged as market maker.

**Important**: Decision frequency uses **positions per day**, not trades per day. A directional trader may place hundreds of trades to build one position (dollar-cost averaging). What matters is how many independent position decisions they make.

#### HFT Detection (2 of 3 conditions)

| Condition | Threshold |
|-----------|-----------|
| Decision frequency | > 10 positions/day |
| Median holding time | < 4 hours |
| Median position size | < $50 |

#### Copy Reliability Labels

| Label | Conditions |
|-------|-----------|
| 🟢 高可靠 | Holding > 24h, < 2 positions/day, PnL/Vol > 10% |
| 🟡 中可靠 | Holding 4-24h, < 5 positions/day |
| 🔴 低可靠 | Holding < 4h or > 5 positions/day |
| ❌ 不可跟单 | MM Score > 50 or HFT detected |

## Data Sources

| API | Base URL | Auth | Use |
|-----|----------|------|-----|
| Gamma API | gamma-api.polymarket.com | None | Markets, events, search |
| Data API v1 | data-api.polymarket.com/v1 | None | Leaderboard, positions, trades, PnL |
| CLOB API | clob.polymarket.com | For trading | Orderbook, prices |

### Key endpoints

```
GET /v1/leaderboard?category=OVERALL&timePeriod=ALL&orderBy=PNL&limit=50&offset=0
GET /positions?user={address}
GET /closed-positions?user={address}
GET /activity?user={address}
GET /profit-loss?user={address}
```

## On-Chain Data (Phase 2)

Alchemy RPC configured in `.env`:

```
POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/<key>
```

CTF Exchange contract: `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`

Key event: `OrderFilled` — extract maker/taker addresses and trade amounts from on-chain logs.

Free tier limit: 10 blocks per `eth_getLogs` call.

## Architecture

```
polycopilot/
├── fetcher.py      # Data fetching (incremental + full)
├── processor.py    # Trade processing, MarketReport generation
├── analyzer.py     # Scoring, MM/HFT detection, copy reliability
├── discovery.py    # Multi-source wallet discovery + filtering
└── cache.py        # Disk cache for incremental updates
```

## Interpreting Results

When presenting results to users:

- Always show the **copy reliability label** prominently
- For ❌ addresses, explain why (MM Score, HFT indicators)
- For 🟢 addresses, highlight key strengths (holding time, PnL/Vol efficiency)
- Compare addresses using the copy trading score (0-100, A/B/C/D grades)
- Use Chinese for user-facing output (the user prefers Chinese)
