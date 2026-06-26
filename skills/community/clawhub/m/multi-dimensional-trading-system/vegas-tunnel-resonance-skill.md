# 📈 Multi-Dimensional Trading Resonance System

> **Skill Type**: Prompt-based Natural Language Analysis Framework  
> **Applicable Markets**: A-shares / DSE Bangladesh / Cryptocurrency  
> **Core Method**: EMA Multi-layer Channels + Fibonacci Retracements + Multi-Timeframe Resonance Scoring

---

## 📋 Trigger Conditions

This Skill activates when the user's question contains any of the following:

- **Keywords**: `T-trading`, `day trading`, `Vegas Tunnel`, `EMA analysis`, `Fibonacci`, `support level`, `resistance level`
- **Markets**: `DSE`, `Dhaka Stock Exchange`, `Bangladesh stock`, `600519`, `BTC`, `ETH`, `GRAMEENPHONE`, `BEXIMCO`
- **Intent**: Asking about short-term trading, entry/exit points, or trend analysis for any asset

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Vegas Tunnel Multi-Dimensional Resonance System│
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  1st Dim    │  2nd Dim    │  3rd Dim    │  4th Dim          │
│  EMA Channel│  Fibonacci  │  Multi-TF   │  Signal Synthesis │
│  Layer      │  Layer      │  Resonance  │  & Decision       │
├─────────────┼─────────────┼─────────────┼───────────────────┤
│ EMA12/13    │ 0.236 Retr  │ 5min TF     │  Composite Score  │
│ EMA144/169  │ 0.382 Retr  │ 15min TF    │  Direction        │
│ EMA576/676  │ 0.500 Retr  │ 1H TF       │  Entry/Exit Sig   │
│ Channel Wd  │ 0.618 Retr  │ 4H TF       │  Stop/TP Levels   │
│ Channel Dir │ 0.786 Retr  │ Daily TF    │  Position Rec     │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

---

## � Data Source & Input Requirements

### ⚠️ Critical Coherence Declaration

**This skill produces concrete price-level recommendations (entry, stop-loss, take-profit).** Such recommendations require verified market data. This section declares how data must be obtained to ensure outputs are grounded in reality, not hallucinated.

### Data Acquisition Methods (Choose One)

#### Method 1: User-Provided OHLC Data (Recommended for Verification)

The user supplies recent OHLC (Open, High, Low, Close) and volume data for the asset and timeframes being analyzed.

**Required Data Format:**
```
Asset: [Stock Code / Crypto Ticker]
Current Price: [Latest Close Price]
Analysis Date/Time: [When data was captured]

Timeframe Data (provide for each relevant TF: 5min, 15min, 1H, 4H, Daily):
  - Open: [Price]
  - High: [Price]
  - Low: [Price]
  - Close: [Price]
  - Volume: [Number of units]

Recent Swing Points (for Fibonacci calculation):
  - Swing High: [Price] (Date/Time)
  - Swing Low: [Price] (Date/Time)
```

**Validation Rule:** Agent MUST confirm data freshness (within last 1-2 hours for intraday analysis, within last 1 day for swing analysis) before proceeding with analysis.

#### Method 2: Live API Integration (If Available)

If the AI environment has access to market data APIs (Binance, Coinbase, Tiingo, Alpha Vantage, exchange APIs), the agent may auto-fetch data with explicit disclosure:
- Name the API source used
- Timestamp the data retrieval
- Confirm data availability for the requested asset and timeframes

**Validation Rule:** Agent MUST state which API was queried and when, so the user can verify independently if needed.

#### Method 3: Not Applicable (Constraint Mode)

If neither user-provided data nor API access is available, the agent MUST:
- **NOT** generate specific price levels or entry/stop/take-profit recommendations
- Instead, **explain the methodology** and ask the user to provide OHLC data in the required format
- Offer to analyze once data is supplied
- Optionally: Provide a template or example of the data format needed (see "Data Input Example" below)

**Example Agent Response (No Data Available):**
> "I can explain the Vegas Tunnel methodology, but to generate concrete entry/stop/take-profit levels, I need verified market data. Please provide OHLC data (Open, High, Low, Close, Volume) for the relevant timeframes and recent swing points. See the example below for the exact format needed. Once you provide the data, I'll execute a complete four-dimensional analysis."

### Data Validation Checklist

Before outputting any analysis report with specific price levels, the agent must verify:

- ✅ **Data Source Declared**: User knows where prices came from
- ✅ **Data Freshness Confirmed**: Prices are current (not stale)
- ✅ **All Required Timeframes Present**: 5min, 15min, 1H, 4H, Daily (or subset relevant to strategy)
- ✅ **Swing Points Identified**: Clear recent high and low for Fibonacci calculation
- ✅ **EMA Values Calculable**: Sufficient historical data to compute EMA12/13/144/169/576/676
- ✅ **No Gaps or Errors**: Data is complete and consistent

**If any check fails:** Pause analysis, inform user of missing data, and request clarification.

### Data Input Example

Here is a concrete example of how a user should provide OHLC data for analysis:

```
Asset: BTC/USDT (Bitcoin)
Current Price: $42,500
Analysis Date/Time: 2026-03-29 14:30 UTC

5min Timeframe:
  Open: $42,480 | High: $42,620 | Low: $42,400 | Close: $42,510 | Volume: 1,250 BTC

15min Timeframe:
  Open: $42,450 | High: $42,650 | Low: $42,380 | Close: $42,510 | Volume: 3,800 BTC

1H Timeframe:
  Open: $42,200 | High: $42,750 | Low: $42,150 | Close: $42,510 | Volume: 15,200 BTC

4H Timeframe:
  Open: $41,800 | High: $42,800 | Low: $41,700 | Close: $42,510 | Volume: 58,000 BTC

Daily Timeframe:
  Open: $41,200 | High: $42,900 | Low: $41,100 | Close: $42,510 | Volume: 245,000 BTC

Recent Swing Points:
  Swing High: $43,200 (2026-03-28 10:15 UTC)
  Swing Low: $40,800 (2026-03-26 18:45 UTC)
```

**Agent Response**: "Data received. Source: User-provided OHLC. Timestamp: 2026-03-29 14:30 UTC. Freshness: Current. Proceeding with analysis..."

---

## 🔧 1st Dimension: Vegas EMA Channel System

### 1.1 Three-Layer Channel Definition

| Channel Layer | EMA Fast | EMA Slow | Time-Space Meaning | Typical Usage |
|--------------|----------|----------|-------------------|---------------|
| **Inner Channel (Short-term Tunnel)** | EMA12 | EMA13 | Short-term momentum / Intraday volatility core | Core reference for day trading, price oscillates around this channel |
| **Middle Channel (Vegas Tunnel)** | EMA144 | EMA169 | Medium-term trend / Swing direction | Classic Vegas channel, determines primary trend direction |
| **Outer Channel (Long-term Tunnel)** | EMA576 | EMA676 | Long-term trend / Macro direction | Bull-bear boundary, strategic direction determination |

### 1.2 Channel Status Determination Rules

Determine channel status layer by layer according to the following rules:

#### A. Channel Arrangement Status

```
【Bullish Alignment】
  Condition: Price > EMA12/13 > EMA144/169 > EMA576/676
  Meaning: Strong uptrend, three-dimensional resonance upward
  Score: +30 points

【Bearish Alignment】
  Condition: Price < EMA12/13 < EMA144/169 < EMA576/676
  Meaning: Strong downtrend, three-dimensional resonance downward
  Score: +30 points (short direction)

【Bullish Entanglement】
  Condition: Price near EMA12/13, but EMA144/169 > EMA576/676
  Meaning: Short-term pullback but medium-long term bullish, T-trading buy opportunity
  Score: +15 points

【Bearish Entanglement】
  Condition: Price near EMA12/13, but EMA144/169 < EMA576/676
  Meaning: Short-term bounce but medium-long term bearish, T-trading sell opportunity
  Score: +15 points

【Chaos State】
  Condition: EMAs at all layers intertwined, no clear arrangement
  Meaning: Direction unclear, not suitable for operation
  Score: 0 points
```

#### B. Channel Width Analysis

```
【Channel Expanding】
  Manifestation: Distance between EMA fast and slow lines increasing
  Meaning: Trend accelerating, momentum strengthening
  Recommendation: Hold with trend, avoid counter-trend

【Channel Contracting】
  Manifestation: Distance between EMA fast and slow lines narrowing
  Meaning: Trend decelerating, potential reversal
  Recommendation: Reduce position and wait, wait for direction selection

【Channel Parallel】
  Manifestation: Distance between EMA fast and slow lines relatively constant
  Meaning: Trend running stably
  Recommendation: Can T-trade between channel upper and lower rails
```

#### C. Price Position Relative to Channels

```
Price above inner channel → Short-term strong, +5 points
Price inside inner channel → Short-term neutral, +0 points  
Price below inner channel → Short-term weak, -5 points

Price above middle channel → Medium-term bullish, +10 points
Price inside middle channel → Medium-term neutral, +0 points
Price below middle channel → Medium-term bearish, -10 points

Price above outer channel → Long-term bullish, +15 points
Price inside outer channel → Long-term neutral, +0 points
Price below outer channel → Long-term bearish, -15 points
```

---

## 📐 2nd Dimension: Fibonacci Retracements & Extensions

### 2.1 Fibonacci Retracement Calculation Method

```
Identify a clear recent trend movement (swing high H and swing low L):

Uptrend retracement levels (support when pulling back from high):
  0.236 retracement = H - (H - L) × 0.236  → Shallow retracement, strong pullback
  0.382 retracement = H - (H - L) × 0.382  → Normal retracement, first support
  0.500 retracement = H - (H - L) × 0.500  → Medium retracement, key level
  0.618 retracement = H - (H - L) × 0.618  → Golden retracement, strong support
  0.786 retracement = H - (H - L) × 0.786  → Deep retracement, last defense line

Downtrend retracement levels (resistance when bouncing from low):
  0.236 retracement = L + (H - L) × 0.236  → Weak bounce pressure
  0.382 retracement = L + (H - L) × 0.382  → Normal bounce pressure
  0.500 retracement = L + (H - L) × 0.500  → Medium bounce pressure
  0.618 retracement = L + (H - L) × 0.618  → Golden bounce pressure
  0.786 retracement = L + (H - L) × 0.786  → Strong bounce pressure
```

### 2.2 Fibonacci & EMA Channel Resonance Determination

```
【Golden Resonance】 → +20 points
  Condition: Fibonacci 0.618 retracement level aligns with EMA144/169 channel (error < 1%)
  Meaning: Very strong support/resistance, high-probability reversal point
  Action: Can enter with heavy position

【Silver Resonance】 → +15 points
  Condition: Fibonacci 0.382 or 0.500 retracement level aligns with any EMA channel
  Meaning: Relatively strong support/resistance
  Action: Can enter with medium position

【Bronze Resonance】 → +10 points
  Condition: Fibonacci 0.236 or 0.786 retracement level aligns with any EMA channel
  Meaning: General support/resistance
  Action: Can enter with light position testing

【No Resonance】 → +0 points
  Condition: Fibonacci levels do not align with EMA channels
  Meaning: Support/resistance reliability reduced
  Action: Need more confirmation signals
```

### 2.3 Fibonacci Extension Levels (Take-profit Targets)

```
Trend continuation target levels:
  1.000 extension = Equal amplitude target
  1.272 extension = Common first target
  1.618 extension = Golden extension target
  2.000 extension = Double extension target
  2.618 extension = Extreme extension target
```

---

## ⏰ 3rd Dimension: Multi-Timeframe Resonance Scoring

### 3.1 Timeframe Weight Configuration

| Market Type | 5min | 15min | 1H | 4H | Daily |
|-------------|------|-------|----|----|-------|
| **A-share T-trading** | 30% | 25% | 20% | 15% | 10% |
| **A-share Swing** | 10% | 15% | 25% | 25% | 25% |
| **DSE Intraday** | 30% | 30% | 25% | 10% | 5% |
| **DSE Swing** | 5% | 10% | 20% | 30% | 35% |
| **Crypto Day** | 30% | 25% | 25% | 15% | 5% |
| **Crypto Swing** | 5% | 10% | 20% | 30% | 35% |

### 3.2 Single Timeframe Scoring Details

For each timeframe, score according to the following rules (max 100 points/timeframe):

```
┌──────────────────────────────────────────────────┐
│              Single Timeframe Scorecard          │
├──────────────────────────────────────────────────┤
│ [1] EMA Channel Arrangement    0 ~ 30 points     │
│     Perfect Bullish/Bearish Alignment: 30        │
│     Entanglement (Bullish/Bearish):  15          │
│     Chaos:              0                         │
├──────────────────────────────────────────────────┤
│ [2] Price Relative to Channel  -15 ~ +15 points   │
│     (Calculated per Section C of 1st Dimension)  │
├──────────────────────────────────────────────────┤
│ [3] Channel Width Trend       0 ~ 15 points      │
│     Expanding (trend direction): 15              │
│     Parallel:           10                       │
│     Contracting:        5                        │
│     Expanding (counter-trend): 0                 │
├──────────────────────────────────────────────────┤
│ [4] Fibonacci Resonance Bonus 0 ~ 20 points      │
│     Golden Resonance: 20                         │
│     Silver Resonance: 15                         │
│     Bronze Resonance: 10                       │
│     No Resonance:   0                            │
├──────────────────────────────────────────────────┤
│ [5] Momentum Confirmation     0 ~ 20 points      │
│     Price breaks inner channel in trend dir: 10  │
│     Volume expansion confirmation: 5               │
│     Candlestick pattern confirmation (hammer/etc): 5
├──────────────────────────────────────────────────┤
│              Total = [1]+[2]+[3]+[4]+[5]         │
│              Range: -15 ~ 100                     │
└──────────────────────────────────────────────────┘
```

### 3.3 Multi-Timeframe Composite Score

```
Composite Score = Σ (Timeframe Score × Timeframe Weight)

Score Interpretation:
  80 ~ 100 points  → ⭐⭐⭐⭐⭐ Very Strong Signal, high-confidence operation
  60 ~ 79 points   → ⭐⭐⭐⭐  Strong Signal, standard position operation
  40 ~ 59 points   → ⭐⭐⭐   Medium Signal, light position testing
  20 ~ 39 points   → ⭐⭐    Weak Signal, watch and wait
   0 ~ 19 points   → ⭐     Invalid Signal, do not trade
  < 0 points       → ⚠️     Reverse Signal, consider opposite operation
```

---

## 🎯 4th Dimension: Signal Synthesis & Trading Decision

### 4.1 T-Trading Signal Generation Template

#### 📈 T-Trading Buy Signal (Buy Low)

```
Trigger Conditions (must satisfy at least 3):
  ✅ Price pulls back to EMA144/169 middle channel vicinity (error < 0.5%)
  ✅ Price is within Fibonacci 0.382 ~ 0.618 retracement zone
  ✅ Inner channel EMA12/13 begins to flatten or turn upward
  ✅ 5min/15min timeframe shows bullish candlestick patterns
  ✅ Composite Score ≥ 40 points and direction is bullish
  ✅ Volume shows contraction with stabilization characteristics

Entry Price: EMA144/169 channel or Fibonacci resonance level
Stop Loss:   Below EMA576/676 outer channel or next Fibonacci retracement level
Take Profit: EMA12/13 inner channel upper rail or previous Fibonacci retracement level
```

#### 📉 T-Trading Sell Signal (Sell High)

```
Trigger Conditions (must satisfy at least 3):
  ✅ Price surges to EMA12/13 inner channel upper rail vicinity
  ✅ Price approaches Fibonacci 0.236 retracement level or previous high
  ✅ Inner channel EMA12/13 begins to flatten or turn downward
  ✅ 5min/15min timeframe shows bearish candlestick patterns
  ✅ Composite Score ≥ 40 points and direction is bearish (or bullish momentum fading)
  ✅ Volume shows expansion with stagnation characteristics

Exit Price: EMA12/13 inner channel upper rail or Fibonacci resistance level
Cover Price: EMA144/169 middle channel or Fibonacci support level
Stop Loss:   Break above previous high/Fibonacci extension 1.272
```

### 4.2 Position Management Matrix

| Composite Score | Resonance Level | Recommended Position | Max Single Position |
|-----------------|-----------------|---------------------|---------------------|
| 80-100 | Golden Resonance | 60%-80% | 30% of total capital |
| 60-79 | Silver Resonance | 40%-60% | 20% of total capital |
| 40-59 | Bronze Resonance | 20%-40% | 15% of total capital |
| 20-39 | No Resonance | 10%-20% | 10% of total capital |
| <20 | — | Empty position, wait | 0% |

### 4.3 A-Share Special Rules

```
【T+1 Restriction Adaptation】
  - A-shares: cannot sell same day as purchase
  - T-trading strategy must be based on existing positions
  - Recommended base position : active position = 5:5 or 6:4
  - Half-position rolling T-trading: Hold 500 shares, trade 500 shares each time

【Trading Time Windows】
  - First 30 minutes of morning session (09:30-10:00): Sentiment game period, highest volatility
  - Morning correction period (10:00-11:30): Trend confirmation period
  - Afternoon launch window (13:00-13:30): Afternoon trend change window
  - Closing confirmation period (14:30-15:00): Trend convergence confirmation

【Price Limit Rules】
  - Main board: ±10% (ST stocks ±5%)
  - STAR/GEM: ±20%
  - BSE: ±30%
  - Special signal handling required when approaching price limits
```

### 4.4 Cryptocurrency Special Rules

```
【24/7 Trading Adaptation】
  - No trading time restrictions, all-weather monitoring
  - Pay attention to overlaps of Asian, European, and American trading sessions
  - Key times: UTC 00:00 (daily close), UTC 14:30 (US market open)

【High Volatility Adaptation】
  - Channel parameters unchanged, but stop-loss/take-profit distances appropriately expanded
  - BTC/ETH recommended stop-loss: 1.5× channel width
  - Altcoins recommended stop-loss: 2.0× channel width

【Funding Rate Reference】
  - Positive rate > 0.1%: Longs crowded, cautious on longs
  - Negative rate < -0.1%: Shorts crowded, cautious on shorts
  - Funding rates can be used as auxiliary confirmation signals
```

### 4.5 DSE Bangladesh Special Rules

```
【T+2 Settlement Adaptation】
  - DSE: settlement occurs 2 trading days after transaction (T+2)
  - Intraday trading is possible, but positions must be planned for T+2 delivery
  - Short selling is restricted; primarily long-only strategies

【Trading Days & Hours】
  - Trading Days: Sunday through Thursday
  - Weekend: Friday and Saturday (no trading)
  - Trading Hours: 10:00-14:30 (4.5 hours continuous session, no break)
  - No pre-market or after-hours sessions

【Key Time Windows】
  - Opening (10:00-10:30): High volatility, overnight news digestion period
  - Mid-session (11:00-13:00): Trend development, stable movement period
  - Closing (14:00-14:30): Position adjustment, profit-taking, trend confirmation

【Price Limits & Circuit Breakers】
  - All listed stocks: ±10% daily price limit
  - Trading halts when limit reached (cooling period)
  - No separate categories (like STAR/GEM) with different limits

【Market Characteristics】
  - Lower liquidity compared to major markets; slippage may be higher
  - Political and economic news sensitivity high
  - Foreign investment flows can cause significant moves
  - Recommended: widen stop-loss slightly (1.2x channel width) for volatility
```

---

## 📊 Analysis Output Template

When the user requests analysis, please strictly follow the template format below for output:

### Template: Complete Analysis Report

```markdown
## 🎰 Vegas Tunnel Multi-Dimensional Resonance Analysis Report

### 📌 Asset Information
- **Asset Name**: [Stock Name/Code or Cryptocurrency Name]
- **Current Price**: [Current Price]
- **Analysis Time**: [Current Time]
- **Market Type**: [A-shares / Cryptocurrency]
- **Analysis Mode**: [T-trading / Day Trading / Swing Trading]

### 📊 Data Source & Verification
- **Data Source**: [User-provided OHLC / API: Binance / API: Coinbase / Other]
- **Data Timestamp**: [When data was captured]
- **Data Freshness**: [Recent / Verified within X hours]
- **Swing Points Identified**: [Swing High: $X at Date/Time] / [Swing Low: $X at Date/Time]

---

### 📊 1st Dimension: EMA Channel Status

| Channel Layer | Fast Line Value | Slow Line Value | Channel Direction | Price Position |
|--------------|-----------------|-----------------|-------------------|----------------|
| Inner (EMA12/13) | [Value] | [Value] | [Rising/Falling/Flat] | [Above/Inside/Below] |
| Middle (EMA144/169) | [Value] | [Value] | [Rising/Falling/Flat] | [Above/Inside/Below] |
| Outer (EMA576/676) | [Value] | [Value] | [Rising/Falling/Flat] | [Above/Inside/Below] |

- **Channel Arrangement**: [Perfect Bullish/Bearish/Entanglement/Chaos]
- **Channel Width Trend**: [Expanding/Contracting/Parallel]
- **Channel Dimension Score**: [X] points

---

### 📐 2nd Dimension: Fibonacci Analysis

- **Reference Swing**: [Swing Low L] → [Swing High H]
- **Current Retracement Depth**: [X.XXX] ([Percentage]%)

| Fibonacci Level | Price Level | EMA Resonance | Status |
|-----------------|-------------|---------------|--------|
| 0.236 | [Price] | [Yes/No, which EMA] | [Broken/Current/Not Reached] |
| 0.382 | [Price] | [Yes/No, which EMA] | [Broken/Current/Not Reached] |
| 0.500 | [Price] | [Yes/No, which EMA] | [Broken/Current/Not Reached] |
| 0.618 | [Price] | [Yes/No, which EMA] | [Broken/Current/Not Reached] |
| 0.786 | [Price] | [Yes/No, which EMA] | [Broken/Current/Not Reached] |

- **Best Resonance Level**: [Price] ([Resonance Level: Golden/Silver/Bronze])
- **Fibonacci Dimension Score**: [X] points

---

### ⏰ 3rd Dimension: Multi-Timeframe Resonance

| Timeframe | Channel Status | Price Position | Momentum | TF Score | Weight | Weighted Score |
|-------------|----------------|----------------|----------|----------|--------|----------------|
| 5min | [Status] | [Position] | [Strong/Med/Weak] | [X]pts | [X]% | [X]pts |
| 15min | [Status] | [Position] | [Strong/Med/Weak] | [X]pts | [X]% | [X]pts |
| 1H | [Status] | [Position] | [Strong/Med/Weak] | [X]pts | [X]% | [X]pts |
| 4H | [Status] | [Position] | [Strong/Med/Weak] | [X]pts | [X]% | [X]pts |
| Daily | [Status] | [Position] | [Strong/Med/Weak] | [X]pts | [X]% | [X]pts |

- **Composite Score**: [X] points / 100 points  [⭐Rating]
- **Resonance Direction**: [Bullish / Bearish / Neutral]
- **Resonance Strength**: [Strong / Medium / Weak / None]

---

### 🎯 4th Dimension: Trading Decision

#### Current Signal: [📈 Long (Buy Low) / 📉 Short (Sell High) / ⏸️ Wait]

**Signal Strength**: [⭐⭐⭐⭐⭐ Rating Text]
**Confidence**: [X]%

| Decision Element | Specific Value | Explanation |
|------------------|----------------|-------------|
| Entry Price | [Price] | [Based on what] |
| Stop Loss | [Price] ([Range]%) | [Based on what] |
| 1st Take Profit | [Price] ([Range]%) | [Based on what] |
| 2nd Take Profit | [Price] ([Range]%) | [Based on what] |
| Recommended Position | [X]% | [Based on score and resonance level] |

#### Trading Plan

> 📋 **Specific Operation Steps**:
> 1. [First step operation and conditions]
> 2. [Second step operation and conditions]  
> 3. [Third step operation and conditions]
>
> ⚠️ **Risk Warnings**:
> - [Major risk factor 1]
> - [Major risk factor 2]
> - [Stop-loss execution discipline reminder]

---

### 📝 Supplementary Notes
- [Any market environment factors requiring special attention]
- [Recent important events/data reminders]
- [Special considerations for this asset]
```

---

## 🧠 Analysis Execution Guide

When you receive a user's analysis request, follow this chain of thought to execute the analysis:

### Step 1: Information Collection & Identification

```
1. Identify Asset: What stock/cryptocurrency did the user mention?
2. Identify Market: A-shares or cryptocurrency?
3. Identify Purpose: T-trading? Day trading? Swing trading?
4. Identify Data Source & Validate:
   ✅ If user provided OHLC data → Verify freshness and completeness (see Data Validation Checklist)
   ✅ If API access available → Fetch data, disclose source and timestamp
   ❌ If no data available → STOP. Do NOT generate price levels. Instead:
      - Explain the Vegas Tunnel methodology
      - Ask user to provide OHLC data in the required format
      - Offer to analyze once data is supplied
```

### Step 2: Data Verification (MANDATORY BEFORE ANALYSIS)

```
Before proceeding to dimensional analysis, confirm all of the following:

□ Data Source is declared (user-provided, API name, or other)
□ Data timestamp is recent (within 1-2 hours for intraday, within 1 day for swing)
□ All required timeframes are present (5min, 15min, 1H, 4H, Daily)
□ Swing high and swing low are clearly identified for Fibonacci calculation
□ EMA calculation is possible (sufficient historical candles available)
□ No data gaps or inconsistencies

If ANY check fails → Pause and request missing data from user.
If ALL checks pass → Proceed to dimensional analysis with confidence.
```

### Step 3: Dimension-by-Dimension Analysis

```
Execute four-dimensional analysis in sequence:

Dimension 1 → Calculate/Determine EMA channel status and score
Dimension 2 → Determine Fibonacci retracement levels and find resonance
Dimension 3 → Score each timeframe individually and weight-aggregate
Dimension 4 → Synthesize signals, generate trading decision
```

### Step 4: Output Report

```
Use the "Complete Analysis Report" template above for output
Ensure each dimension has clear conclusions
Provide specific price levels and operation recommendations
Always include risk warnings
ALWAYS cite the data source and timestamp in the report
```

---

## 💡 Common Scenario Quick Reference

### Scenario 1: User says "Help me analyze if XXX can do T-trading"

→ **First**: Ask for OHLC data (5min, 15min, 1H, 4H, Daily) and recent swing points if not provided.  
→ **Then**: Use **A-share T-trading weight configuration**, focus on 5min/15min timeframes, output analysis report per complete template.  
→ **Always**: Cite data source and timestamp in the report.

### Scenario 2: User says "What's BTC's current position, can I day trade?"

→ **First**: Verify data source (user-provided or API). If no data, ask for OHLC.  
→ **Then**: Use **Crypto day trading weight configuration**, focus on EMA channel position and Fibonacci support/resistance, output per complete template.  
→ **Always**: Declare which API was queried (if applicable) and when.

### Scenario 3: User says "How do you view the Vegas Tunnel?"

→ Briefly explain the Vegas Tunnel system (three-layer EMA channels).  
→ Ask user which asset they want to analyze.  
→ **Request OHLC data** in the required format before proceeding to analysis.  
→ Execute complete analysis once data is provided.

### Scenario 4: User provides specific price and asks about support/resistance

→ **Verify**: Confirm data source, timestamp, and swing points.  
→ Focus on outputting Fibonacci retracement levels + EMA channel resonance analysis, mark key support and resistance levels.  
→ **Cite**: Include data source in the output.

### Scenario 5: User asks "Is it suitable to enter now?"

→ **First**: Verify data is available and current. If not, request OHLC data.  
→ **Then**: Execute complete four-dimensional analysis, focus on outputting composite score and signal strength.  
→ Give clear "recommended entry / recommended wait / recommended exit" conclusion.  
→ **Always**: Cite data source and timestamp.

---

## ⚠️ Disclaimer & Risk Warnings

> **Important Reminder**: 
> 1. This analysis system is only a technical analysis reference tool and does not constitute investment advice
> 2. All technical indicators have lag and failure probabilities
> 3. Always execute stop-loss discipline, control single-trade risk within 2% of total capital
> 4. A-shares are subject to T+1 restrictions, T-trading must be based on existing positions
> 5. Cryptocurrency markets are highly volatile, exercise extreme caution with leveraged trading
> 6. Market risk exists, invest with caution

### 🚨 Critical: Data Source Requirement

> **Hallucination Risk**: This skill produces concrete price-level recommendations (entry, stop-loss, take-profit). **Without verified market data, these recommendations are hallucinated and have zero predictive value.**
>
> - **DO NOT** accept price levels generated without a cited data source
> - **DO NOT** trade on recommendations that cannot be traced to live or historical market data
> - **ALWAYS** verify that the agent has declared where prices came from (user-provided OHLC, API name, etc.)
> - **ALWAYS** confirm data freshness before acting on recommendations
>
> If the agent generates specific price levels without citing a data source, **reject the analysis and request verified data first.**

---

## � Coherence & Safety Summary

### What Was Fixed

This skill originally had an **internal coherence gap**: it promised concrete price-level recommendations (entry, stop-loss, take-profit) but declared no mechanism to obtain market data. This section summarizes the fixes applied:

#### 1. **Explicit Data Source Declaration** (New Section: "📥 Data Source & Input Requirements")
   - Declared three data acquisition methods: user-provided OHLC, live API integration, or constraint mode
   - Each method includes validation rules and explicit disclosure requirements
   - Prevents hallucinated price levels by requiring verified data before analysis

#### 2. **Data Validation Checklist** (Mandatory Before Analysis)
   - Agent must verify 6 data quality checks before outputting any analysis
   - Ensures data freshness, completeness, and consistency
   - Pauses analysis if any check fails and requests clarification from user

#### 3. **Updated Analysis Execution Guide** (Step 2: Data Verification)
   - Added mandatory data verification step before dimensional analysis
   - Explicit "STOP" instruction if no data is available
   - Prevents agent from generating price levels without verified data source

#### 4. **Enhanced Report Template** (New Section: "📊 Data Source & Verification")
   - Analysis reports now include data source, timestamp, and freshness confirmation
   - Users can verify where prices came from and when they were captured
   - Enables independent validation of recommendations

#### 5. **Hallucination Risk Warning** (New Section: "🚨 Critical: Data Source Requirement")
   - Explicit disclaimer about hallucination risk without verified data
   - Clear guidance: "DO NOT accept price levels without a cited data source"
   - Instructs users to reject analyses that cannot be traced to verified market data

#### 6. **Updated Common Scenarios** (All scenarios now include data requirements)
   - Every usage pattern now starts with data verification step
   - Emphasizes data source citation in all outputs
   - Prevents accidental hallucination in common use cases

#### 7. **Practical Data Input Example** (Concrete format for users)
   - Shows exact format for providing OHLC data
   - Includes example agent response confirming data receipt
   - Reduces ambiguity about what data is needed

### Residual Risks (Mitigated but Not Eliminated)

Even with these fixes, users should understand:

- **Agent Discipline**: The fixes rely on the agent following the instructions. A poorly-tuned agent might still ignore the data validation checklist.
- **API Reliability**: If using Method 2 (API integration), the agent must correctly identify and query the right API. Incorrect API calls could return wrong data.
- **User Verification**: Users must actively verify data sources and freshness. Blindly trusting agent-cited sources without independent confirmation is still risky.

**Recommendation**: For critical trading decisions, users should always independently verify market data from a trusted source (exchange website, financial data provider) before acting on recommendations.

---

## �📚 Appendix: EMA Calculation Reference

```
EMA Formula:
  EMA(today) = Price(today) × K + EMA(yesterday) × (1 - K)
  Where K = 2 / (N + 1), N is the period number

Smoothing coefficient K for each EMA:
  EMA12:  K = 2/13  ≈ 0.1538
  EMA13:  K = 2/14  ≈ 0.1429
  EMA144: K = 2/145 ≈ 0.0138
  EMA169: K = 2/170 ≈ 0.0118
  EMA576: K = 2/577 ≈ 0.0035
  EMA676: K = 2/677 ≈ 0.0030

Vegas Tunnel EMA Period Origins:
  12, 13     → Short-term momentum (adjacent Fibonacci numbers)
  144, 169   → Medium-term trend (12², 13²)
  576, 676   → Long-term trend (144×4, 169×4)
```

---

