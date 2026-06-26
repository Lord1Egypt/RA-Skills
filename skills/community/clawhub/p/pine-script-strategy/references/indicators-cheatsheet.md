# Indicators Cheat Sheet

## Moving Averages
```pine
ema20 = ta.ema(close, 20)
sma50 = ta.sma(close, 50)
wma20 = ta.wma(close, 20)
vwma20 = ta.vwma(close, 20)
rma14 = ta.rma(close, 14)          // Wilder's (used in RSI/ATR)
alma20 = ta.alma(close, 20, 0.85, 6)
```

## Oscillators
```pine
rsi = ta.rsi(close, 14)
macdLine = ta.ema(close, 12) - ta.ema(close, 26)
signalLine = ta.ema(macdLine, 9)
histogram = macdLine - signalLine

// Stochastic
k = ta.sma(ta.stoch(close, high, low, 14), 3)
d = ta.sma(k, 3)
```

## Volatility
```pine
atr = ta.atr(14)
bbBasis = ta.sma(close, 20)
bbDev = 2.0 * ta.stdev(close, 20)
bbUpper = bbBasis + bbDev
bbLower = bbBasis - bbDev
bbWidth = (bbUpper - bbLower) / bbBasis * 100

// Keltner Channels
kcBasis = ta.ema(close, 20)
kcUpper = kcBasis + ta.atr(10) * 1.5
kcLower = kcBasis - ta.atr(10) * 1.5

// Supertrend
[stLine, stDir] = ta.supertrend(3, 10)  // stDir < 0 = bull, > 0 = bear
```

## Trend Strength
```pine
[diPlus, diMinus, adx] = ta.dmi(14, 14)
// ADX > 25 = strong trend, < 20 = ranging/choppy
```

## Volume
```pine
volAvg = ta.sma(volume, 20)
volSpike = volume > volAvg * 1.5
obv = ta.obv
cmf = ta.cmf(hlc3, 20)
```

## VWAP
```pine
vwap = ta.vwap(hlc3)  // Resets each session
```

## Pivot Points
```pine
pivotHigh = ta.pivothigh(high, 5, 5)
pivotLow = ta.pivotlow(low, 5, 5)
// Returns na when no pivot found
```

## Parabolic SAR
```pine
sar = ta.sar(0.02, 0.02, 0.2)
```

## Linear Regression
```pine
lr = ta.linreg(close, 14, 0)
```

## CCI
```pine
cci = ta.cci(close, 20)
```

## MFI
```pine
mfi = ta.mfi(hlc3, 14)
```
