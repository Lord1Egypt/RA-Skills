---
name: meme-signal-evaluator
description: |
  6-dimensional scoring engine for meme tokens with automated paper trading simulation.
  Use this skill when users ask to evaluate/score meme tokens, set up buy/sell strategies,
  run paper trading simulations, or build a systematic meme token trading pipeline.
  Combines Smart Money, Social, Trend, Inflow, KOL/Whale, and Hype dimensions.
metadata:
  author: ls569333469
  version: "1.0"
---

# Meme Signal Evaluator

## Overview

A systematic scoring engine that evaluates meme tokens across 6 dimensions, matches them against configurable trading strategies, and simulates paper trades. Designed to turn raw market data into actionable buy/sell signals.

## Use Cases

1. **Token Scoring**: Evaluate any meme token with a 0-100 composite score
2. **Strategy Matching**: Define multiple strategies with different thresholds and entry modes
3. **Paper Trading**: Simulate buy/sell with configurable take-profit and stop-loss
4. **Watchlist Management**: Lifecycle tracking (watching → buy_signal → bought → sold/dismissed)
5. **Performance Tracking**: Win rate, average P&L, and per-strategy statistics

---

## 6-Dimension Scoring Algorithm

Each dimension scores 0-100 independently. Final score = weighted sum + negative penalty.

### Dimension 1: Smart Money (SM) Score

**Weight**: 20% (default, configurable)

**Data Sources**:
- Smart Money trading signals (buy direction, 24h window)
- Smart Money inflow data
- Token Dynamic API `smartMoneyHolders` field

**Scoring Logic**:
```
SM buy signal count:
  ≥5 SM addresses buying → 80pts
  ≥3 SM addresses buying → 60pts
  ≥1 SM address buying  → 40pts

SM inflow amount:
  >$50K inflow → +20pts
  >$10K inflow → +10pts

Dynamic SM holders (fallback when no signals):
  ≥5 holders → 60pts
  ≥3 holders → 45pts
  ≥1 holder  → 25pts

Cap: 100
```

### Dimension 2: Social Score

**Weight**: 10% (default)

**Data Sources**:
- Social Hype Leaderboard ranking
- Topic Rush association
- Unified Rank presence

**Scoring Logic**:
```
Social Hype ranking:
  Top 10  → 90pts
  Top 30  → 70pts
  Listed   → 40pts
  Positive sentiment → +10pts

Topic Rush association:
  Found in trending topic → +25pts
  Topic net inflow >$10K  → +10pts

Fallback: present in Unified Rank → 30pts

Cap: 100
```

### Dimension 3: Trend Score

**Weight**: 20% (default)

**Data Source**: Token Dynamic API real-time price changes

**Scoring Logic**:
```
1h price change:
  >20% → +40pts (strong trend)
  >10% → +30pts
  >5%  → +20pts
  >0%  → +10pts

5m momentum:
  >5%  → +20pts
  >2%  → +10pts

4h trend confirmation:
  >10% → +15pts
  >5%  → +8pts

Multi-timeframe resonance (5m+1h+4h all positive): +10pts
1h drop <-10%: -20pts penalty

Cap: 100
```

### Dimension 4: Inflow/Volume Score

**Weight**: 20% (default)

**Data Source**: Token Dynamic API volume data

**Scoring Logic**:
```
5m volume:
  >$100K → 60pts
  >$50K  → 45pts
  >$10K  → 30pts
  >$5K   → 15pts

Buy/sell ratio (24h):
  Buy% ≥60% → +20pts (strong buy pressure)
  Buy% ≥55% → +10pts

1h volume:
  >$500K → +15pts
  >$100K → +8pts

Cap: 100
```

### Dimension 5: KOL/Whale Score

**Weight**: 15% (default)

**Data Source**: Token Dynamic API holder data

**Scoring Logic**:
```
KOL holders:
  ≥10 → 50pts
  ≥5  → 35pts
  ≥2  → 20pts

Pro holders:
  ≥5  → +25pts
  ≥2  → +15pts
  ≥1  → +8pts

KOL holding percentage:
  >5% → +15pts

Cap: 100
```

### Dimension 6: Hype Score

**Weight**: 15% (default)

**Data Sources**: Topic Rush data, Meme Exclusive ranking

**Scoring Logic**:
```
Topic Rush (Viral topics):
  Found in viral topic → 70pts
  Topic inflow >$10K   → +15pts

Meme Exclusive ranking:
  Score ≥4.0 → 80pts
  Score ≥3.0 → 60pts
  Score ≥2.0 → 40pts
  Listed     → 20pts

Cap: 100
```

### Negative Signals (Penalty)

Applied after positive scoring. Can reduce total score.

```
Token audit risk (honeypot, rug pull):
  High risk detected  → -30pts + force dismiss

High tax (>10%):
  → -20pts

DEX screener paid without real traction:
  → -10pts
```

### Final Score Calculation

```
rawScore = SM × w_sm + Social × w_social + Trend × w_trend + 
           Inflow × w_inflow + KOL × w_kol + Hype × w_hype

totalScore = max(0, rawScore + negativePenalty)
```

Default weights: SM=20, Social=10, Trend=20, Inflow=20, KOL=15, Hype=15

---

## Strategy Configuration

Multiple strategies can be defined with different entry modes and thresholds.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Strategy name (e.g., `volume_5m_50k`) |
| entryMode | string | Entry trigger (`volume_driven`, `sm_driven`) |
| buyThreshold | number | Minimum total score to trigger buy (e.g., 20, 30, 40) |
| enabled | boolean | Whether strategy is active |
| weightSm/Social/Trend/Inflow/Kol/Hype | number | Dimension weights (should sum to 100) |

### Strategy Matching

When a token's `totalScore` reaches a strategy's `buyThreshold`:
1. Sort matching strategies by threshold (highest first)
2. Pick the first strategy where `totalScore >= buyThreshold`
3. This ensures higher-threshold strategies get priority

---

## Paper Trading Simulation

### Entry Logic
When evaluator sets status to `buy_signal`, paper trader:
1. Records entry price from Token Dynamic API
2. Creates a paper trade record with entry timestamp
3. Sets watchlist status to `bought`

### Exit Logic (checked on each evaluation cycle)
```
Take Profit: price ≥ entry × (1 + takeProfitPct/100)  → sell, mark "tp"
Stop Loss:   price ≤ entry × (1 - stopLossPct/100)    → sell, mark "sl"
Timeout:     holdTime > maxHoldMinutes                  → sell, mark "timeout"
```

Default: Take Profit = 50%, Stop Loss = 20%, Max Hold = 1440 minutes (24h)

### Trade Record Fields

| Field | Description |
|-------|-------------|
| entryPrice | Price at buy |
| exitPrice | Price at sell |
| pnlPercent | (exitPrice - entryPrice) / entryPrice × 100 |
| strategyUsed | Which strategy triggered the buy |
| exitReason | `tp` (take profit) / `sl` (stop loss) / `timeout` |

---

## Pipeline Workflow

The complete pipeline runs on a scheduler (default: every 5 minutes):

```
1. Collect Data    → Run all collectors (unified-rank, meme-rush, smart-money, social-hype)
2. Scan Watchlist  → Filter new tokens into watchlist based on global filters
3. Evaluate        → Score all watching tokens using 6-dimension algorithm
4. Paper Trade     → Execute simulated buys for buy_signal tokens
5. Monitor         → Check existing positions for TP/SL/timeout exits
```

### Global Filters for Watchlist Entry

| Filter | Default | Description |
|--------|---------|-------------|
| minMarketCap | $10K | Minimum market cap |
| maxMarketCap | $50M | Maximum market cap |
| minLiquidity | $5K | Minimum liquidity |
| minHolders | 50 | Minimum holder count |
| minVolume5m | $1K | Minimum 5-minute volume |
| maxTokenAgeHours | 72 | Maximum token age |

---

## Notes

1. All scores are 0-100. Higher = more bullish.
2. Weights are percentages and should sum to 100 for proper normalization.
3. The evaluator fetches fresh Token Dynamic data before each evaluation for accuracy.
4. Strategy matching uses the highest-threshold-first approach for conviction grading.
5. Paper trading tracks simulated P&L for strategy backtesting without risk.
