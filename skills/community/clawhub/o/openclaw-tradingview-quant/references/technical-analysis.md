# Technical Analysis Methodology

> Professional technical analysis scoring model and indicator interpretation

---

## 📊 Comprehensive Scoring Model

### Total Score Composition (100 points)

```
Total Score = Trend Strength(30 points) + Momentum Indicators(25 points) + Pattern Recognition(20 points) + 
              Support Resistance(15 points) + Market Sentiment(10 points)
```

### Rating Standards

| Score Range | Rating | Recommendation |
|------------|--------|---------------|
| 90-100 | ⭐⭐⭐⭐⭐ | Strongly Recommend |
| 80-89 | ⭐⭐⭐⭐ | Recommend |
| 70-79 | ⭐⭐⭐ | Neutral Watch |
| 60-69 | ⭐⭐ | Cautious |
| < 60 | ⭐ | Not Recommend |

---

## 1️⃣ Trend Strength Analysis (30 points)

### 1.1 Multi-Timeframe Moving Average Arrangement (0-15 points)

#### Perfect Bullish Arrangement (15 points)
```
5-day MA > 10-day MA > 20-day MA > 60-day MA
```

#### Scoring Criteria
- 5-day > 10-day > 20-day > 60-day: **15 points** (Perfect bullish)
- 5-day > 10-day > 20-day: **12 points** (Strong bullish)
- 5-day > 10-day: **8 points** (Short-term bullish)
- Moving averages converging: **5 points** (Direction unclear)
- Bearish arrangement: **0 points** (Downward trend)

### 1.2 Price Relative Position (0-10 points)

#### Scoring Criteria
- Price > all moving averages: **10 points** (Strong)
- Price > 60-day MA: **8 points** (Medium-term strong)
- Price > 20-day MA: **5 points** (Short-term strong)
- Price < all moving averages: **0 points** (Weak)

### 1.3 Trend Duration (0-5 points)

#### Scoring Criteria
- Duration > 30 days: **5 points** (Mature trend)
- Duration 20-30 days: **4 points** (Established trend)
- Duration 10-20 days: **3 points** (Early trend)
- Duration < 10 days: **1 point** (Unstable trend)

---

## 2️⃣ Momentum Indicators Analysis (25 points)

### 2.1 RSI Relative Strength Index (0-10 points)

#### Health Scoring
- RSI in 40-60: **10 points** (Most healthy)
- RSI in 30-40 or 60-70: **8 points** (Healthy)
- RSI in 20-30 or 70-80: **5 points** (Caution)
- RSI < 20 or > 80: **2 points** (Overbought/oversold)

#### Trading Signals
```
Buy Signals:
- RSI breaks above 30 from below
- RSI bottom divergence (price makes new low, RSI doesn't make new low)

Sell Signals:
- RSI breaks below 70 from above
- RSI top divergence (price makes new high, RSI doesn't make new high)
```

### 2.2 MACD Indicator (0-10 points)

#### Status Scoring
- Golden cross + DIF > 0 + histogram expanding: **10 points** (Strong buy)
- Golden cross + DIF < 0: **8 points** (Buy signal)
- Golden cross + histogram contracting: **6 points** (Momentum weakening)
- Death cross + DIF > 0: **3 points** (Caution)
- Death cross + DIF < 0: **0 points** (Sell signal)

#### Trading Signals
```
Strong Buy:
- MACD golden cross above 0 axis
- Histogram rapidly expanding

Buy:
- MACD golden cross below 0 axis
- Bottom divergence

Sell:
- MACD death cross below 0 axis
- Top divergence
```

### 2.3 Volume Coordination (0-5 points)

#### Volume-Price Relationship Scoring
- Rise + volume increase: **5 points** (Healthy rise)
- Rise + volume decrease: **3 points** (Insufficient momentum)
- Fall + volume decrease: **2 points** (Selling pressure easing)
- Fall + volume increase: **0 points** (Panic selling)

#### Relative Volume
```
Volume increase: Daily volume > 5-day average × 1.5
Volume decrease: Daily volume < 5-day average × 0.7
```

---

## 3️⃣ Pattern Recognition (20 points)

### 3.1 Classic Patterns (0-15 points)

#### Reversal Patterns
- **Double bottom/double top**: Confidence > 85% → 15 points
- **Head and shoulders bottom/top**: Confidence > 80% → 12 points
- **Rounding bottom/top**: Confidence > 75% → 10 points

#### Consolidation Patterns
- **Ascending triangle**: Confidence > 80% → 12 points
- **Flag consolidation**: Confidence > 75% → 10 points
- **Rectangle consolidation**: Confidence > 70% → 8 points

### 3.2 Candlestick Patterns (0-5 points)

#### Bullish Patterns
- **Hammer**: Appears at support → 5 points
- **Bullish engulfing**: Volume increases → 5 points
- **Morning star**: Three candlestick combination → 5 points

#### Bearish Patterns
- **Shooting star**: Appears at resistance → 0 points
- **Bearish engulfing**: Volume increases → 0 points
- **Evening star**: Three candlestick combination → 0 points

---

## 4️⃣ Support Resistance Analysis (15 points)

### 4.1 Distance from Support Level (0-8 points)

#### Scoring Criteria
```
Distance from support < 3%: 8 points (High safety margin)
Distance from support 3-5%: 6 points (Relatively safe)
Distance from support 5-8%: 4 points (Average)
Distance from support > 8%: 2 points (Higher risk)
```

### 4.2 Breaking Resistance Level (0-7 points)

#### Scoring Criteria
```
Effective break above resistance + volume increase: 7 points (Strong)
Break above resistance but volume decrease: 4 points (To be confirmed)
Approaching resistance without break: 2 points (Wait)
Far from resistance: 0 points (Limited space)
```

### 4.3 Support Resistance Calculation Methods

#### 1. Historical High-Low Method
```javascript
// Find important high-low points in recent 60 days
function findSupportResistance(priceHistory) {
  const highs = findLocalHighs(priceHistory);
  const lows = findLocalLows(priceHistory);
  
  // Support: Recent important low points
  const support = Math.max(...lows.slice(-3));
  
  // Resistance: Recent important high points
  const resistance = Math.min(...highs.slice(-3));
  
  return { support, resistance };
}
```

#### 2. Moving Average Support Method
```
Short-term support: 20-day MA
Medium-term support: 60-day MA
Long-term support: 120-day MA
```

#### 3. Fibonacci Retracement Method
```
From high point retracement:
- 0.382 retracement level (Shallow retracement)
- 0.5 retracement level (Moderate retracement)
- 0.618 retracement level (Deep retracement)

From low point rebound:
- 1.382 target level
- 1.618 target level
- 2.0 target level
```

---

## 5️⃣ Market Sentiment Analysis (10 points)

### 5.1 Relative Strength (0-5 points)

#### Scoring Criteria
```
Outperform market > 10%: 5 points (Strong)
Outperform market 5-10%: 4 points (Strong)
Outperform market 0-5%: 3 points (Slightly strong)
Underperform market 0-5%: 2 points (Slightly weak)
Underperform market > 5%: 0 points (Weak)
```

### 5.2 Sector Linkage (0-5 points)

#### Scoring Criteria
```
Sector leader + strong sector: 5 points
Sector follower + strong sector: 4 points
Sector leader + average sector: 3 points
Sector follower + average sector: 2 points
Sector laggard: 0 points
```

---

## 📈 Practical Application Examples

### Example 1: Strong Stock Scoring

```
Stock: Puyuan Information (688118)
Current Price: ¥35.50

【Trend Strength】30 points → 28 points
- Moving average arrangement: 5-day>10-day>20-day>60-day(15 points)
- Price position: Above all moving averages (10 points)
- Duration: 25 days (3 points)

【Momentum Indicators】25 points → 23 points
- RSI(14): 65.3 (8 points)
- MACD: Golden cross+DIF>0+increasing (10 points)
- Volume: Volume increase on rise (5 points)

【Pattern Recognition】20 points → 18 points
- Ascending triangle: Confidence 85% (12 points)
- Bullish engulfing: Appeared yesterday (5 points)
- Pattern completeness: 90% (1 point)

【Support Resistance】15 points → 13 points
- Distance from support: 6% (4 points)
- Break above resistance: Effective break + volume increase (7 points)
- Space assessment: Good (2 points)

【Market Sentiment】10 points → 8 points
- Relative strength: Outperform market 8% (4 points)
- Sector linkage: Sector leader + strong sector (4 points)

Total Score: 90 points ⭐⭐⭐⭐⭐
Rating: Strongly Recommend
```

### Example 2: Weak Stock Scoring

```
Stock: XXX (000000)
Current Price: ¥10.50

【Trend Strength】30 points → 8 points
- Moving average arrangement: Bearish arrangement (0 points)
- Price position: Below all moving averages (0 points)
- Duration: Falling for 15 days (0 points)
- Adjustment points: 8 points (Signs of rebound)

【Momentum Indicators】25 points → 10 points
- RSI(14): 25.3 (5 points - Oversold)
- MACD: Death cross+DIF<0 (0 points)
- Volume: Volume decrease on fall (5 points - Selling pressure easing)

【Pattern Recognition】20 points → 5 points
- Descending channel (0 points)
- Bearish patterns (0 points)
- Possible bottom: 5 points (RSI oversold)

【Support Resistance】15 points → 6 points
- Distance from support: 2% (6 points - Close to support)
- Resistance level: Far away (0 points)

【Market Sentiment】10 points → 0 points
- Relative strength: Underperform market 12% (0 points)
- Sector linkage: Sector laggard (0 points)

Total Score: 29 points ⭐
Rating: Not Recommend (But possible oversold rebound)
```

---

## 🎯 Usage Recommendations

### 1. Comprehensive Judgment
- Don't look at single indicators only
- Combine multiple dimensions for comprehensive scoring
- Pay attention to scoring change trends

### 2. Dynamic Adjustment
- Update scores daily
- Track scoring changes
- Adjust strategies promptly

### 3. Risk Control
- Set stop losses even for high-score stocks
- Low-score stocks may have oversold rebounds
- Strictly execute risk management

### 4. Market Environment
- Bull market: Consider above 70 points
- Sideways market: Above 80 points
- Bear market: Above 90 points or oversold rebounds

---

## 📚 Advanced Learning

### Recommended Reading
1. 《Japanese Candlestick Charting Techniques》- Steve Nison
2. 《Reminiscences of a Stock Operator》- Edwin Lefèvre
3. 《The Turtle Trading Rules》- Curtis Faith
4. 《Technical Analysis of the Financial Markets》- Martin J. Pring

### Practical Suggestions
1. Build your own scoring model
2. Backtest historical data validation
3. Keep trading logs
4. Continuously optimize and improve
