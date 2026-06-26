---
description: Smart stock screening workflow - Filter quality targets based on multi-factor model
---

# Smart Stock Screening Workflow

Based on multi-factor model, filter quality targets from the market that meet technical and fundamental conditions, providing comprehensive scoring and buy recommendations.

## Execution Steps

### Step 1: Understand Screening Criteria

Extract from user input:
- **Market scope**: Country/region (determine market_code), asset type
- **Technical conditions**: Trend direction, RSI range, MACD status, volume
- **Fundamental conditions**: PE, PB, ROE, market cap, dividend yield, etc.
- **Sorting preference**: Change percentage, market cap, volume, etc.

### Step 2: Get Metadata (Metadata First)

```
tradingview_get_metadata(type='markets')  # Get market_code
tradingview_get_metadata(type='tabs', asset_type='stocks')  # Get available tabs
```

### Step 3: Get Candidate Pool

Choose appropriate tab and columnset based on screening direction:

```
# Technical screening - Use technical-related tabs
tradingview_get_leaderboard(
  asset_type='stocks', tab='gainers',  # or active/unusual-volume/best-performing
  market_code='china', columnset='overview', count=100
)

# Fundamental data - Switch columnset
tradingview_get_leaderboard(
  asset_type='stocks', tab='all-stocks',
  market_code='china', columnset='valuation', count=100
)

# Profitability
tradingview_get_leaderboard(
  asset_type='stocks', tab='all-stocks',
  market_code='china', columnset='profitability', count=100
)
```

### Step 4: Technical Screening

For Top 20-30 in candidate pool, call individually:

```
tradingview_get_ta(symbol, include_indicators=true)
```

Screening criteria (see `references/technical-analysis.md` scoring model):
- TA multi-timeframe signal is Buy
- RSI in healthy range 30-70
- MACD golden cross or DIF > 0
- ADX > 25 (trend exists)

### Step 5: K-line Data Verification

For Top 10 that pass technical screening, get K-line confirmation:

```
tradingview_get_price(symbol, timeframe='D', range=60)
```

Verify:
- Moving average arrangement (bullish/bearish)
- Volume coordination (volume increase on rise)
- Distance from support level

### Step 6: Comprehensive Scoring and Ranking

Calculate total score (100-point system) according to `references/technical-analysis.md` scoring model:
- Trend strength 30 points
- Momentum indicators 25 points
- Pattern recognition 20 points
- Support resistance 15 points
- Market sentiment 10 points

### Step 7: Generate Detailed Report

```markdown
# Smart Stock Screening Results - [Market/Sector]

## Screening Criteria
- [List technical and fundamental conditions]

## Qualified Stocks (Total N stocks)

### 1. [Stock Name] (Code) ⭐⭐⭐⭐⭐
**Comprehensive Score**: XX/100
- Technical: RSI=XX, MACD=XX, Trend=XX
- Fundamental: PE=XX, ROE=XX%
- Buy Recommendation: ¥XX-XX
- Stop Loss: ¥XX
- Target Price: ¥XX
```

## Example

**User**: "Help me select strong stocks from China A-shares"

**Execution**:
1. `get_metadata(type='markets')` → china
2. `get_leaderboard(tab='gainers', market_code='china', count=100)` → Gainers
3. `get_leaderboard(tab='gainers', market_code='china', columnset='valuation')` → Valuation
4. Top 20 individual `get_ta(include_indicators=true)` → Technical screening
5. Top 10 `get_price(timeframe='D', range=60)` → K-line verification
6. Comprehensive scoring → Output Top 10 report
