# Entry Patterns (Proven)

## Pattern 1: EMA Crossover + Confirmation
```pine
emaFast = ta.ema(close, 9)
emaSlow = ta.ema(close, 21)
bullCross = ta.crossover(emaFast, emaSlow)
bearCross = ta.crossunder(emaFast, emaSlow)

if bullCross and rsi > 50 and volume > ta.sma(volume, 20)
    strategy.entry("Long", strategy.long)
```

## Pattern 2: Pullback to EMA
```pine
pullbackToEMA = low <= ema21 and close > ema21  // Touch & bounce
if pullbackToEMA and close > ema50 and rsi > 50
    strategy.entry("Long", strategy.long)
```

## Pattern 3: Breakout + Retest
```pine
var float breakoutLevel = na
if close > swingHigh and close[1] <= swingHigh[1]
    breakoutLevel := swingHigh

retest = low <= breakoutLevel * 1.002 and close > breakoutLevel
```

## Pattern 4: Liquidity Sweep + Reversal
```pine
if bearSweep and close > open and close > low + (high - low) * 0.5
    strategy.entry("Long", strategy.long)  // Sweep + bullish candle
```

## Pattern 5: FVG Fill + Bounce
```pine
if bullFVG and low <= fvgTop and close > fvgBottom
    strategy.entry("Long", strategy.long)
```

## Pattern 6: Three EMA Alignment
```pine
ema9 = ta.ema(close, 9)
ema21 = ta.ema(close, 21)
ema50 = ta.ema(close, 50)

bullAlign = ema9 > ema21 and ema21 > ema50 and close > ema9
bearAlign = ema9 < ema21 and ema21 < ema50 and close < ema9
```

## Pattern 7: VWAP + Trend Combo
```pine
vwap = ta.vwap(hlc3)
ema50 = ta.ema(close, 50)

longVWAP = close > vwap and close > ema50 and rsi > 50
shortVWAP = close < vwap and close < ema50 and rsi < 50
```

## Pattern 8: Opening Range Breakout
```pine
var float orbHigh = na
var float orbLow = na
var bool orbSet = false

if hour == 9 and minute == 15  // 15 min after open
    orbHigh := high
    orbLow := low
    orbSet := true

orbLong = orbSet and close > orbHigh and barstate.isconfirmed
```

## Pattern 9: RSI Divergence
```pine
// Price makes lower low but RSI makes higher low = bullish divergence
priceLL = close < ta.lowest(close, 20)
rsiHL = rsi > ta.valuewhen(close < ta.lowest(close, 20)[1], rsi, 1)

bullDiv = priceLL and rsiHL
```

## Pattern 10: Bollinger Band Squeeze Breakout
```pine
bbWidth = (bbUpper - bbLower) / bbBasis * 100
bbSqueeze = bbWidth < ta.sma(bbWidth, 20) * 0.75
squeezeRelease = bbSqueeze[1] and not bbSqueeze

if squeezeRelease and close > bbUpper
    strategy.entry("Long", strategy.long)
```
