# Risk Management System

> Professional position management, stop loss/take profit, and portfolio risk control methods

---

## 📊 Three Pillars of Risk Management

1. **Position Management** - Control single trade risk
2. **Stop Loss/Take Profit** - Protect profits, limit losses
3. **Portfolio Management** - Diversify risk, optimize returns

---

## 1️⃣ Position Management

### 1.1 Kelly Criterion

#### Formula
```
Optimal Position = (Win Rate × Profit/Loss Ratio - Loss Rate) / Profit/Loss Ratio

Where:
- Win Rate = Winning Trades / Total Trades
- Loss Rate = 1 - Win Rate
- Profit/Loss Ratio = Average Profit / Average Loss
```

#### Example Calculation
```javascript
function calculateKellyPosition(winRate, profitLossRatio) {
  const loseRate = 1 - winRate;
  const kellyPercent = (winRate * profitLossRatio - loseRate) / profitLossRatio;

  // Use half Kelly for conservative approach
  const conservativeKelly = kellyPercent * 0.5;

  return Math.max(0, Math.min(conservativeKelly, 0.25)); // Max 25%
}

// Example
const winRate = 0.6;        // 60% win rate
const plRatio = 2;          // 2:1 profit/loss ratio
const position = calculateKellyPosition(winRate, plRatio);
// Result: (0.6 × 2 - 0.4) / 2 = 0.4 → Half Kelly = 0.2 (20%)
```

#### Practical Application Recommendations
```
Theoretical Kelly Position × 0.5 = Actual Position (conservative)
Single stock max position: 20%
Single sector max position: 40%
Total position control: Adjust based on market environment
```

---

### 1.2 Fixed Percentage Method

#### Method
```
Position = Total Capital × Fixed Percentage
```

#### Risk Level Classification

| Risk Level | Single Position | Target Audience |
|-----------|----------------|-----------------|
| Conservative | 5-10% | Risk averse |
| Balanced | 10-15% | General investors |
| Aggressive | 15-20% | Risk seekers |
| Extreme | >20% | Professional traders |

---

### 1.3 Volatility Adjustment Method

#### Formula
```
Adjusted Position = Base Position × (Standard Volatility / Actual Volatility)

Standard Volatility = 30%
```

#### Implementation
```javascript
function adjustPositionByVolatility(basePosition, volatility) {
  const standardVol = 0.30;  // 30% standard volatility
  const adjustment = standardVol / volatility;

  return basePosition * Math.min(adjustment, 1.5); // Max 1.5x amplification
}

// Example
const basePosition = 0.15;  // 15% base position
const volatility = 0.45;    // 45% volatility (high volatility)
const adjusted = adjustPositionByVolatility(basePosition, volatility);
// Result: 0.15 × (0.30 / 0.45) = 0.10 (10%)
```

---

### 1.4 Pyramid Position Building

#### Normal Pyramid (Recommended)
```
First batch: 50% position - Buy at support level
Second batch: 30% position - Add after 5% profit
Third batch: 20% position - Add after 10% profit
```

**Advantages**:
- Controlled risk
- Lower cost
- Suitable for trend trading

**Example**:
```javascript
function pyramidBuying(capital, currentPrice, entryPrice, position) {
  const profit = (currentPrice - entryPrice) / entryPrice;

  if (position === 0) {
    // First batch: 50%
    return { amount: capital * 0.5, reason: 'Initial position' };
  } else if (position === 1 && profit >= 0.05) {
    // Second batch: 30%
    return { amount: capital * 0.3, reason: 'Add at 5% profit' };
  } else if (position === 2 && profit >= 0.10) {
    // Third batch: 20%
    return { amount: capital * 0.2, reason: 'Add at 10% profit' };
  }

  return { amount: 0, reason: 'No addition' };
}
```

#### Inverted Pyramid (Not Recommended)
```
First batch: 20% position
Second batch: 30% position
Third batch: 50% position
```

**Disadvantages**:
- Excessive risk
- Higher cost
- Easy to get trapped

---

### 1.5 Staged Position Building

#### Three-Part Method
```
First batch: 33% - Buy at support level
Second batch: 33% - Buy at resistance breakout
Third batch: 34% - Buy after trend confirmation
```

#### Five-Part Method (More Conservative)
```
Each batch: 20%
Buy in 5 batches
Interval: Adjust based on market conditions
```

---

## 2️⃣ Stop Loss Strategies

### 2.1 Fixed Percentage Stop Loss

#### Standards
```
Conservative: -5%
Balanced: -7%
Aggressive: -10%
```

#### Implementation
```javascript
function calculateFixedStopLoss(entryPrice, riskLevel = 'balanced') {
  const stopLossPercent = {
    conservative: 0.05,
    balanced: 0.07,
    aggressive: 0.10
  };

  const percent = stopLossPercent[riskLevel] || 0.07;
  return entryPrice * (1 - percent);
}
```

---

### 2.2 Technical Stop Loss

#### Methods

**1. Support Level Stop Loss**
```
Stop Loss = Support Level × 0.98 (2% below support)
```

**2. Moving Average Stop Loss**
```
Short-term: Break below 5-day MA
Medium-term: Break below 20-day MA
Long-term: Break below 60-day MA
```

**3. Pattern Stop Loss**
```
Double Bottom: Below second low
Triangle: Below lower boundary
Head and Shoulders: Below right shoulder
```

#### Implementation
```javascript
function calculateTechnicalStopLoss(currentPrice, support, ma20, pattern) {
  const stops = [];

  // Support level stop loss
  if (support) {
    stops.push({
      price: support * 0.98,
      type: 'support',
      distance: (currentPrice - support * 0.98) / currentPrice
    });
  }

  // Moving average stop loss
  if (ma20) {
    stops.push({
      price: ma20,
      type: 'ma20',
      distance: (currentPrice - ma20) / currentPrice
    });
  }

  // Pattern stop loss
  if (pattern && pattern.stopLoss) {
    stops.push({
      price: pattern.stopLoss,
      type: 'pattern',
      distance: (currentPrice - pattern.stopLoss) / currentPrice
    });
  }

  // Choose nearest stop loss (minimum risk)
  return stops.sort((a, b) => b.price - a.price)[0];
}
```

---

### 2.3 Time-Based Stop Loss

#### Rules
```
Hold 30 days without profit → Consider exit
Hold 60 days without reaching target → Forced exit
```

#### Reasons
- Low capital efficiency
- High opportunity cost
- Possible misjudgment

---

### 2.4 Trailing Stop Loss

#### Strategy
```javascript
function calculateTrailingStop(entryPrice, currentPrice, highestPrice) {
  const profit = (currentPrice - entryPrice) / entryPrice;

  if (profit < 0.05) {
    // Profit < 5%: Stop at cost
    return entryPrice;
  } else if (profit < 0.10) {
    // Profit 5-10%: Stop at cost + 3%
    return entryPrice * 1.03;
  } else if (profit < 0.20) {
    // Profit 10-20%: Stop at cost + 5%
    return entryPrice * 1.05;
  } else {
    // Profit > 20%: Stop at highest - 10%
    return highestPrice * 0.90;
  }
}
```

---

## 3️⃣ Take Profit Strategies

### 3.1 Staged Take Profit

#### Strategy
```
10% profit: Sell 30%
20% profit: Sell 30%
30% profit: Sell 40%
```

#### Advantages
- Lock in partial profits
- Preserve upside potential
- Reduce psychological pressure

#### Implementation
```javascript
function calculatePartialTakeProfit(entryPrice, currentPrice, remainingPosition) {
  const profit = (currentPrice - entryPrice) / entryPrice;

  if (profit >= 0.30 && remainingPosition > 0.4) {
    return { sell: 0.4, reason: '30% profit, sell 40%' };
  } else if (profit >= 0.20 && remainingPosition > 0.7) {
    return { sell: 0.3, reason: '20% profit, sell 30%' };
  } else if (profit >= 0.10 && remainingPosition === 1.0) {
    return { sell: 0.3, reason: '10% profit, sell 30%' };
  }

  return { sell: 0, reason: 'Hold' };
}
```

---

### 3.2 Trailing Take Profit

#### Strategy
```
After profit > 15%
Exit on 5% drawback
```

#### Implementation
```javascript
function calculateTrailingTakeProfit(entryPrice, currentPrice, highestPrice) {
  const profit = (currentPrice - entryPrice) / entryPrice;

  if (profit < 0.15) {
    return { action: 'hold', reason: 'Profit below 15%' };
  }

  const drawdown = (highestPrice - currentPrice) / highestPrice;

  if (drawdown >= 0.05) {
    return { action: 'sell', reason: '5% drawback, trailing take profit' };
  }

  return { action: 'hold', reason: 'Continue holding' };
}
```

---

### 3.3 Target Price Take Profit

#### Strategy
```
First target: Sell 50%
Second target: Sell 30%
Third target: Sell 20%
```

#### Target Price Calculation
```javascript
function calculateTargetPrices(entryPrice, pattern, resistance) {
  const targets = [];

  // Pattern-based target
  if (pattern && pattern.target) {
    targets.push({
      price: pattern.target,
      type: 'pattern',
      sellPercent: 0.5
    });
  }

  // Resistance-based target
  if (resistance) {
    targets.push({
      price: resistance,
      type: 'resistance',
      sellPercent: 0.3
    });
  }

  // Risk-reward ratio target
  const riskRewardTarget = entryPrice * 1.20; // 20% target
  targets.push({
    price: riskRewardTarget,
    type: 'risk_reward',
    sellPercent: 0.2
  });

  return targets.sort((a, b) => a.price - b.price);
}
```

---

## 4️⃣ Risk Assessment

### 4.1 Individual Stock Risk Assessment

#### Volatility Risk
```javascript
function calculateVolatility(priceHistory) {
  const returns = [];
  for (let i = 1; i < priceHistory.length; i++) {
    const ret = (priceHistory[i].close - priceHistory[i-1].close) / priceHistory[i-1].close;
    returns.push(ret);
  }

  const mean = returns.reduce((a, b) => a + b) / returns.length;
  const variance = returns.reduce((sum, ret) =>
    sum + Math.pow(ret - mean, 2), 0) / returns.length;

  const dailyVol = Math.sqrt(variance);
  const annualVol = dailyVol * Math.sqrt(252);

  return {
    daily: dailyVol,
    annual: annualVol,
    level: annualVol < 0.2 ? 'low' : annualVol < 0.4 ? 'medium' : 'high'
  };
}
```

#### Risk Levels
```
Low risk: Annual volatility < 20%
Medium risk: Annual volatility 20-40%
High risk: Annual volatility > 40%
```

---

#### Liquidity Risk
```
Good: Daily trading volume > ¥100M
Fair: Daily trading volume ¥50M-100M
Poor: Daily trading volume < ¥50M
```

---

#### Beta Coefficient
```
Low risk: Beta < 0.8
Medium risk: Beta 0.8-1.2
High risk: Beta > 1.2
```

---

### 4.2 Portfolio Risk Assessment

#### Diversification Check
```javascript
function checkDiversification(portfolio) {
  const checks = {
    stockCount: portfolio.length >= 5 && portfolio.length <= 10,
    sectorCount: new Set(portfolio.map(p => p.sector)).size >= 3,
    singleStockMax: Math.max(...portfolio.map(p => p.weight)) <= 0.20,
    sectorMax: checkSectorConcentration(portfolio) <= 0.40
  };

  return {
    score: Object.values(checks).filter(Boolean).length / 4,
    checks
  };
}
```

#### Correlation Check
```javascript
function calculateCorrelation(returns1, returns2) {
  const n = returns1.length;
  const mean1 = returns1.reduce((a, b) => a + b) / n;
  const mean2 = returns2.reduce((a, b) => a + b) / n;

  let numerator = 0;
  let denom1 = 0;
  let denom2 = 0;

  for (let i = 0; i < n; i++) {
    const diff1 = returns1[i] - mean1;
    const diff2 = returns2[i] - mean2;
    numerator += diff1 * diff2;
    denom1 += diff1 * diff1;
    denom2 += diff2 * diff2;
  }

  return numerator / Math.sqrt(denom1 * denom2);
}

// Correlation standards
// < 0.3: Low correlation (good)
// 0.3-0.7: Medium correlation (acceptable)
// > 0.7: High correlation (needs adjustment)
```

---

## 5️⃣ Risk-Reward Ratio

### 5.1 Calculation Method

```javascript
function calculateRiskRewardRatio(entryPrice, targetPrice, stopLoss) {
  const potentialProfit = targetPrice - entryPrice;
  const potentialLoss = entryPrice - stopLoss;

  return {
    ratio: potentialProfit / potentialLoss,
    profit: (potentialProfit / entryPrice * 100).toFixed(2) + '%',
    loss: (potentialLoss / entryPrice * 100).toFixed(2) + '%'
  };
}
```

### 5.2 Rating Standards

| Risk-Reward Ratio | Rating | Recommendation |
|------------------|--------|----------------|
| > 1:3 | Excellent | Strongly recommended |
| 1:2 - 1:3 | Good | Recommended |
| 1:1.5 - 1:2 | Fair | Acceptable |
| < 1:1.5 | Poor | Not recommended |

### 5.3 Minimum Requirements

```
Risk-Reward Ratio ≥ 1:2
Win Rate ≥ 50%
```

---

## 6️⃣ Capital Management

### 6.1 Total Position Control

#### Market Environment Adjustment
```
Bull market: 70-90%
Sideways market: 50-70%
Bear market: 20-40%
```

#### Implementation
```javascript
function adjustTotalPosition(marketTrend, basePosition) {
  const adjustments = {
    bull: 1.2,      // Bull market amplify 20%
    neutral: 1.0,   // Sideways unchanged
    bear: 0.6       // Bear market reduce 40%
  };

  const adjusted = basePosition * (adjustments[marketTrend] || 1.0);
  return Math.min(adjusted, 0.90); // Max 90%
}
```

---

### 6.2 Cash Reserve

#### Minimum Cash
```
Minimum cash reserve: 10%
```

#### Purpose
- Adding opportunities
- Emergency funds
- Psychological safety cushion

---

### 6.3 Leverage Usage

#### Recommendations
```
Not recommended to use leverage
If necessary: Leverage ≤ 1.5x
```

#### Risks
- Amplified losses
- Forced liquidation
- Psychological pressure

---

## 📊 Practical Examples

### Example 1: Complete Risk Management Process

```
Stock: Primeton (688118)
Capital: ¥100,000
Current Price: ¥35.50

【Step 1: Risk Assessment】
- Volatility: 45.2% (high risk)
- Beta: 2.19 (high risk)
- Liquidity: Good

【Step 2: Position Calculation】
- Base position: 15% (balanced)
- Volatility adjustment: 15% × (30% / 45%) = 10%
- Recommended position: 8-10%

【Step 3: Staged Position Building】
First batch: 5% (¥5,000) - Price ¥35.00-35.50
Second batch: 5% (¥5,000) - Breakout ¥37.00 or pullback to ¥33.50

【Step 4: Stop Loss Setup】
- Technical stop: ¥33.00 (support level)
- Percentage stop: ¥33.00 (-7%)
- Final stop: ¥33.00

【Step 5: Take Profit Setup】
- First target: ¥40.00 (+12.7%) - Sell 50%
- Second target: ¥45.00 (+26.8%) - Sell 30%
- Trailing take profit: After profit > 15%, exit on 5% drawback

【Step 6: Risk-Reward Ratio】
- Potential profit: +12.7% (first target)
- Potential risk: -7%
- Risk-reward ratio: 1:1.8 ✅

【Execution Result】
- Entry price: ¥35.20
- Quantity: 142 shares (¥5,000)
- Stop loss: ¥33.00
- Target: ¥40.00
```

---

## 💡 Risk Management Principles

### 1. Never Go Full Position

**Reasons**:
- Loss of flexibility
- Unable to respond to opportunities
- Enormous psychological pressure

---

### 2. Strictly Execute Stop Loss

**Principles**:
- Stop loss is discipline, not suggestion
- Don't move stop loss (unless upward)
- Don't buy back immediately after stop loss

---

### 3. Protect Profits

**Methods**:
- Move stop loss up after profit
- Staged take profit
- Don't let profits turn into losses

---

### 4. Control Drawdown

**Targets**:
- Single trade max loss: < 2%
- Monthly max drawdown: < 10%
- Annual max drawdown: < 20%

---

### 5. Record and Review

**Content**:
- Record every trade
- Analyze stop loss reasons
- Summarize successes and failures
- Continuously optimize strategies

---

## 📚 Recommended Reading

1. "The Complete TurtleTrader" - Curtis Faith
2. "Trade Your Way to Financial Freedom" - Van K. Tharp
3. "Trading in the Zone" - Mark Douglas
4. "Trader Vic—Methods of a Wall Street Master" - Victor Sperandeo
