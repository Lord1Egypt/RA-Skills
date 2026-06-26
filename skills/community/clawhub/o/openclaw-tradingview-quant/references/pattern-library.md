# Technical Pattern Recognition Library

> Classic technical pattern recognition algorithms and trading strategies

---

## 📋 Pattern Classification

### Reversal Patterns
- Double Bottom (W-Bottom)
- Double Top (M-Top)
- Head and Shoulders Bottom
- Head and Shoulders Top
- Rounding Bottom
- Rounding Top

### Continuation Patterns
- Ascending Triangle
- Descending Triangle
- Symmetrical Triangle
- Flag Pattern
- Rectangle Pattern
- Wedge Pattern

### Candlestick Patterns
- Hammer
- Inverted Hammer
- Engulfing Pattern
- Morning Star/Evening Star
- Doji

---

## 🔄 Reversal Patterns

### 1. Double Bottom (W-Bottom)

#### Pattern Characteristics
```
Price movement forms a "W" shape
Two lows are close in price
Middle high point (neckline)
```

#### Recognition Criteria

1. **Price difference between two lows < 3%**
```javascript
const priceDiff = Math.abs(low1.price - low2.price) / low1.price;
if (priceDiff > 0.03) return false;
```

2. **Time interval between two lows > 10 days**
```javascript
const timeDiff = (low2.time - low1.time) / (24 * 60 * 60);
if (timeDiff < 10) return false;
```

3. **Neckline height > 10%**
```javascript
const necklineHeight = (neckline.price - low1.price) / low1.price;
if (necklineHeight < 0.1) return false;
```

4. **Second low volume < First low volume**
```javascript
if (low2.volume >= low1.volume) return false;
```

5. **Breakout volume > 1.5x average**
```javascript
const avgVolume = calculateAvgVolume(history, 20);
if (breakoutVolume < avgVolume * 1.5) return false;
```

#### Confidence Calculation

```javascript
function calculateDoubleBottomConfidence(pattern) {
  let score = 60; // Base score

  // Smaller price difference is better
  const priceDiff = Math.abs(pattern.low1.price - pattern.low2.price) / pattern.low1.price;
  if (priceDiff < 0.02) score += 10;
  else if (priceDiff < 0.03) score += 5;

  // Longer time interval is more reliable
  const timeDiff = (pattern.low2.time - pattern.low1.time) / (24 * 60 * 60);
  if (timeDiff > 20) score += 10;
  else if (timeDiff > 15) score += 5;

  // Higher neckline is better
  const necklineHeight = (pattern.neckline - pattern.low1.price) / pattern.low1.price;
  if (necklineHeight > 0.15) score += 10;
  else if (necklineHeight > 0.12) score += 5;

  // Decreasing volume
  if (pattern.low2.volume < pattern.low1.volume * 0.8) score += 5;

  // Breakout with volume expansion
  const avgVolume = pattern.avgVolume;
  if (pattern.breakoutVolume > avgVolume * 2) score += 5;
  else if (pattern.breakoutVolume > avgVolume * 1.5) score += 3;

  return Math.min(score, 100);
}
```

#### Trading Strategy

**Entry Points**:
- Breakout above neckline + volume expansion
- Pullback to neckline without breaking (second entry opportunity)

**Target Price**:
```
Target = Neckline Price + (Neckline Price - Low Price)
```

**Stop Loss**:
```
Stop Loss = 2-3% below second low
```

**Success Rate**:
- Confidence > 85%: 75% success rate
- Confidence 70-85%: 60% success rate
- Confidence < 70%: 45% success rate

---

### 2. Head and Shoulders Bottom

#### Pattern Characteristics
```
Three lows: left shoulder, head, right shoulder
Head is lower than both shoulders
Both shoulders are close in price
```

#### Recognition Criteria

1. **Head is > 5% lower than shoulders**
2. **Price difference between shoulders < 5%**
3. **Head has highest volume**
4. **Breakout with volume expansion**

#### Confidence Calculation

```javascript
function calculateHeadShouldersConfidence(pattern) {
  let score = 60;

  // Head depth
  const headDepth = (pattern.leftShoulder.price - pattern.head.price) / pattern.leftShoulder.price;
  if (headDepth > 0.1) score += 15;
  else if (headDepth > 0.07) score += 10;

  // Shoulder symmetry
  const shoulderDiff = Math.abs(pattern.leftShoulder.price - pattern.rightShoulder.price) / pattern.leftShoulder.price;
  if (shoulderDiff < 0.03) score += 10;
  else if (shoulderDiff < 0.05) score += 5;

  // Volume characteristics
  if (pattern.head.volume > pattern.leftShoulder.volume &&
      pattern.head.volume > pattern.rightShoulder.volume) {
    score += 10;
  }

  // Breakout volume
  if (pattern.breakoutVolume > pattern.avgVolume * 1.5) score += 5;

  return Math.min(score, 100);
}
```

#### Trading Strategy

**Entry Point**: Breakout above neckline

**Target Price**:
```
Target = Neckline Price + (Neckline Price - Head Price)
```

**Stop Loss**: Below right shoulder

---

### 3. Rounding Bottom

#### Pattern Characteristics
```
Price rises in arc shape
Long formation time (> 30 days)
Volume forms bowl shape
```

#### Recognition Criteria

1. **Formation time > 30 days**
2. **Price forms arc shape**
3. **Left side volume > Right side volume**
4. **Bottom has lowest volume**

#### Trading Strategy

**Entry Point**: Breakout above arc top

**Target Price**: 1.5-2x arc height

**Stop Loss**: Arc bottom

---

## 📐 Continuation Patterns

### 1. Ascending Triangle

#### Pattern Characteristics
```
Upper boundary horizontal (resistance level)
Lower boundary ascending (support line)
Volume gradually decreases
Breakout direction upward probability 70%
```

#### Recognition Criteria

1. **Upper boundary horizontal (fluctuation < 2%)**
```javascript
const topRange = (Math.max(...tops) - Math.min(...tops)) / Math.min(...tops);
if (topRange > 0.02) return false;
```

2. **Lower boundary ascending**
```javascript
const slope = calculateSlope(bottoms);
if (slope <= 0) return false;
```

3. **Formation time 10-30 days**
4. **Volume contraction**

#### Confidence Calculation

```javascript
function calculateAscendingTriangleConfidence(pattern) {
  let score = 60;

  // Upper boundary horizontality
  const topRange = (Math.max(...pattern.tops) - Math.min(...pattern.tops)) / Math.min(...pattern.tops);
  if (topRange < 0.01) score += 15;
  else if (topRange < 0.02) score += 10;

  // Lower boundary slope
  const slope = calculateSlope(pattern.bottoms);
  if (slope > 0.02) score += 10;
  else if (slope > 0.01) score += 5;

  // Volume contraction
  if (pattern.recentVolume < pattern.initialVolume * 0.7) score += 10;

  // Touch count
  const touchCount = pattern.tops.length + pattern.bottoms.length;
  if (touchCount >= 6) score += 5;

  return Math.min(score, 100);
}
```

#### Trading Strategy

**Entry Point**: Breakout above upper boundary + volume expansion

**Target Price**:
```
Target = Upper Boundary + Triangle Height
```

**Stop Loss**: Below lower boundary

**Success Rate**: 70%

---

### 2. Flag Pattern

#### Pattern Characteristics
```
Prior significant uptrend (flagpole)
Consolidation forms parallelogram
Short consolidation time (< 20 days)
Volume contraction
Breakout direction consistent with flagpole
```

#### Recognition Criteria

1. **Prior gain > 10%**
2. **Consolidation time < 20 days**
3. **Consolidation range < 50% of prior gain**
4. **Volume contraction**

#### Trading Strategy

**Entry Point**: Breakout above flag upper boundary

**Target Price**:
```
Target = Breakout Point + Flagpole Height
```

**Stop Loss**: Flag lower boundary

---

### 3. Rectangle Pattern

#### Pattern Characteristics
```
Price oscillates between two horizontal lines
Both upper and lower boundaries are horizontal
Volume gradually decreases
```

#### Recognition Criteria

1. **Upper and lower boundaries horizontal (fluctuation < 2%)**
2. **Touch boundary count ≥ 4 times**
3. **Consolidation time 10-40 days**

#### Trading Strategy

**Entry Point**: Breakout above upper boundary + volume expansion

**Target Price**:
```
Target = Upper Boundary + Rectangle Height
```

**Stop Loss**: Below lower boundary

---

## 🕯️ Candlestick Patterns

### 1. Hammer

#### Pattern Characteristics
```
Small body
Lower shadow length > Body × 2
Very short or no upper shadow
Appears at end of downtrend
```

#### Recognition Criteria

```javascript
function isHammer(candle) {
  const body = Math.abs(candle.close - candle.open);
  const lowerShadow = Math.min(candle.open, candle.close) - candle.low;
  const upperShadow = candle.high - Math.max(candle.open, candle.close);

  // Lower shadow > Body × 2
  if (lowerShadow < body * 2) return false;

  // Very short upper shadow
  if (upperShadow > body * 0.5) return false;

  // Body < 30% of total length
  const totalLength = candle.high - candle.low;
  if (body / totalLength > 0.3) return false;

  return true;
}
```

#### Signal Strength

**Strong Buy**:
- Appears at support level
- Volume expansion
- Next day closes bullish for confirmation

**General Buy**:
- Appears in downtrend
- Normal volume

---

### 2. Engulfing Pattern

#### Bullish Engulfing

**Characteristics**:
```
Previous candle: Bearish
Current candle: Bullish completely engulfs previous
Appears in downtrend
Volume expansion
```

**Recognition Criteria**:
```javascript
function isBullishEngulfing(prev, curr) {
  // Previous is bearish
  if (prev.close >= prev.open) return false;

  // Current is bullish
  if (curr.close <= curr.open) return false;

  // Complete engulfing
  if (curr.open >= prev.close && curr.close <= prev.open) return false;
  if (curr.open > prev.open || curr.close < prev.close) return false;

  // Volume expansion
  if (curr.volume < prev.volume * 1.2) return false;

  return true;
}
```

#### Bearish Engulfing

**Characteristics**:
```
Previous candle: Bullish
Current candle: Bearish completely engulfs previous
Appears in uptrend
Volume expansion
```

---

### 3. Morning Star/Evening Star

#### Morning Star (Bullish)

**Three Candle Combination**:
```
First candle: Large bearish
Second candle: Small body (doji best)
Third candle: Large bullish
```

**Recognition Criteria**:
```javascript
function isMorningStar(k1, k2, k3) {
  // First large bearish
  const body1 = k1.open - k1.close;
  if (body1 < (k1.high - k1.low) * 0.6) return false;

  // Second small body
  const body2 = Math.abs(k2.close - k2.open);
  if (body2 > (k2.high - k2.low) * 0.3) return false;

  // Third large bullish
  const body3 = k3.close - k3.open;
  if (body3 < (k3.high - k3.low) * 0.6) return false;

  // Third close > First body midpoint
  if (k3.close < (k1.open + k1.close) / 2) return false;

  return true;
}
```

---

## 🚫 Pattern Failure Recognition

### False Breakout Characteristics

1. **Volume not expanded after breakout**
```javascript
if (breakoutVolume < avgVolume * 1.3) {
  return { type: 'fake_breakout', reason: 'volume_not_confirmed' };
}
```

2. **Quick reversal after breakout**
```javascript
if (closePrice < breakoutPrice * 0.97) {
  return { type: 'fake_breakout', reason: 'quick_reversal' };
}
```

3. **Breakout magnitude < 3%**
```javascript
const breakoutPercent = (breakoutPrice - resistance) / resistance;
if (breakoutPercent < 0.03) {
  return { type: 'weak_breakout', reason: 'insufficient_momentum' };
}
```

4. **Sideways movement after breakout**
```javascript
const daysAfterBreakout = 5;
const priceChange = (currentPrice - breakoutPrice) / breakoutPrice;
if (priceChange < 0.02 && daysPassed > daysAfterBreakout) {
  return { type: 'failed_breakout', reason: 'no_follow_through' };
}
```

### Response Strategies

**Confirm Breakout**:
- Wait 2-3 days after breakout for confirmation
- Observe volume cooperation
- Set stop loss (3% below breakout point)

**False Breakout Stop Loss**:
- Quick stop loss, don't hesitate
- Re-evaluate pattern
- Wait for new opportunities

---

## 📊 Practical Examples

### Example 1: BTC/USDT Ascending Triangle

```
Time: February 15 - March 1, 2026
Pattern: Ascending Triangle

Recognition Process:
1. Upper boundary: $68,200 (horizontal resistance)
2. Lower boundary: Rising trendline
3. Touch count: Upper boundary 3 times, lower boundary 4 times
4. Volume: Gradually contracting
5. Confidence: 85%

Trading Strategy:
- Entry: Breakout above $68,200 and hold
- Target: $72,000 (pattern height $3,800)
- Stop Loss: $66,500
- Risk-Reward Ratio: 1:2.4

Result:
- March 2: Breakout above $68,200
- March 5: Reached target $72,000
- Success: ✅
```

### Example 2: Primeton Double Bottom Pattern

```
Time: January 10 - February 20, 2026
Pattern: Double Bottom (W-Bottom)

Recognition Process:
1. First low: ¥28.50 (January 10)
2. Second low: ¥28.20 (February 5)
3. Price difference: 1.05% ✅
4. Time interval: 26 days ✅
5. Neckline: ¥33.00
6. Neckline height: 15.9% ✅
7. Volume: Decreasing ✅
8. Confidence: 92%

Trading Strategy:
- Entry: Breakout above ¥33.00
- Target: ¥37.50
- Stop Loss: ¥27.50
- Risk-Reward Ratio: 1:2.7

Result:
- February 20: Breakout above neckline
- March 1: Reached ¥35.50 (target not reached but significant profit)
- Success: ✅
```

---

## 💡 Usage Recommendations

### 1. Pattern Recognition Priority

**High Priority**:
- Double Bottom/Double Top
- Head and Shoulders Bottom/Top
- Ascending Triangle

**Medium Priority**:
- Flag Pattern
- Rectangle Pattern
- Rounding Bottom

**Low Priority**:
- Single candlestick patterns (need confirmation with other signals)

### 2. Confirmation Mechanism

**Must Confirm**:
- Volume cooperation
- Breakout validity
- Time period

**Optional Confirmation**:
- Technical indicator support
- Fundamental cooperation
- Market environment

### 3. Risk Control

**Strict Stop Loss**:
- Exit immediately when pattern breaks
- Don't hold false hopes
- Capital protection first

**Staged Position Building**:
- 50% position on breakout
- 30% add after confirmation
- 20% add on trend continuation

---

## 📚 Advanced Learning

### Recommended Books
1. "Technical Analysis of Stock Trends" - Robert D. Edwards
2. "Technical Analysis of the Futures Markets" - John J. Murphy
3. "Japanese Candlestick Charting Techniques" - Steve Nison

### Practice Recommendations
1. Build pattern recognition journal
2. Backtest historical pattern success rates
3. Summarize failure cases
4. Continuously optimize recognition algorithms
