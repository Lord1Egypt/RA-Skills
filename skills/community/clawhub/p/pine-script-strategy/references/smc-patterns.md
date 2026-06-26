# SMC (Smart Money Concepts) Patterns

## Break of Structure (BOS)
```pine
var float lastSwingHigh = na
var float lastSwingLow = na

pivotH = ta.pivothigh(high, swingLook, swingLook)
pivotL = ta.pivotlow(low, swingLook, swingLook)

if not na(pivotH)
    lastSwingHigh := high[swingLook]
if not na(pivotL)
    lastSwingLow := low[swingLook]

bullBOS = not na(lastSwingHigh) and close > lastSwingHigh
bearBOS = not na(lastSwingLow) and close < lastSwingLow
```

## Change of Character (ChoCH)
```pine
var int lastStructure = 0  // 1=bullish, -1=bearish
var bool choChBull = false
var bool choChBear = false

if bullBOS
    if lastStructure == -1
        choChBull := true
    lastStructure := 1
if bearBOS
    if lastStructure == 1
        choChBear := true
    lastStructure := -1
```

## Fair Value Gaps (FVG)
```pine
bullFVG = low[0] > high[2]   // Gap up
bearFVG = high[0] < low[2]   // Gap down
fvgTop = bullFVG ? low[0] : na
fvgBottom = bullFVG ? high[2] : na
```

## Order Blocks
```pine
bullOB = close[1] < open[1] and close > open and close > high[1]
bearOB = close[1] > open[1] and close < open and close < low[1]
```

## Liquidity Sweeps
```pine
bullSweep = high > lastSwingHigh and close < lastSwingHigh
bearSweep = low < lastSwingLow and close > lastSwingLow
```

## Premium / Discount Zones
```pine
range_ = lastSwingHigh - lastSwingLow
premium = close > lastSwingLow + range_ * 0.75    // Top 25%
discount = close < lastSwingLow + range_ * 0.5    // Bottom 50%
equilibrium = close > lastSwingLow + range_ * 0.45 and close < lastSwingLow + range_ * 0.55
```

## FVG Fill Detection
```pine
// Track unfilled FVGs
var float unfilledFVGTop = na
var float unfilledFVGBot = na

if bullFVG
    unfilledFVGTop := low[0]
    unfilledFVGBot := high[2]

// Price fills the gap
fvgFilled = not na(unfilledFVGTop) and low <= unfilledFVGBot
if fvgFilled
    unfilledFVGTop := na
    unfilledFVGBot := na
```
