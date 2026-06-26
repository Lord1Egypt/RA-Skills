# KlickAnalytics CLI — Full Command Reference

All commands follow: `ka [command] -s [SYMBOL] [flags]`

> **Built by KlickAnalytics.com** — developed by an ex-Bloomberg team of professionals
> with deep expertise in market data, terminal design, and institutional-grade analytics.

> **The command list is ever-growing.** New analytics functions are added regularly.
> Run `ka help` to always see the latest available commands, or check the changelog at
> https://www.klickanalytics.com/cli_changelog

---

## help

Show usage instructions for any command.

```bash
ka help
ka help profile
ka help prices
```

---

## profile

Company background, sector, market, and business description.

```bash
ka profile -s AAPL
ka profile -s TSLA
```

**Typical output fields:** `symbol`, `companyName`, `exchange`, `sector`, `industry`,
`description`, `ceo`, `country`, `employees`, `website`, `mktCap`

---

## quote

Real-time (or most recent) market quote.

```bash
ka quote -s AAPL
ka quote -s SPY -datatype json
```

**Typical output fields:** `symbol`, `price`, `changesPercentage`, `change`, `dayLow`,
`dayHigh`, `yearLow`, `yearHigh`, `volume`, `avgVolume`, `marketCap`, `pe`, `eps`,
`sharesOutstanding`, `timestamp`

---

## prices

Historical OHLCV (Open, High, Low, Close, Volume) price data.

```bash
ka prices -s AAPL
ka prices -s AMZN -sd 2025-01-01 -ed 2025-12-31
ka prices -s MSFT -limit 60
```

**Flags:** `-s`, `-sd`, `-ed`, `-limit`
**Typical output fields:** `date`, `open`, `high`, `low`, `close`, `adjClose`, `volume`,
`unadjustedVolume`, `change`, `changePercent`, `vwap`

---

## earnings

Historical earnings per share (EPS) actuals vs. estimates.

```bash
ka earnings -s MSFT
ka earnings -s NVDA -limit 8
```

**Typical output fields:** `date`, `symbol`, `eps`, `epsEstimated`, `revenue`,
`revenueEstimated`, `fiscalDateEnding`, `updatedFromDate`

---

## dividends

Dividend payment history.

```bash
ka dividends -s AAPL
ka dividends -s JNJ -limit 20
```

**Typical output fields:** `date`, `label`, `adjDividend`, `dividend`, `recordDate`,
`paymentDate`, `declarationDate`

---

## splits

Stock split history.

```bash
ka splits -s TSLA
ka splits -s AAPL
```

**Typical output fields:** `date`, `label`, `numerator`, `denominator`

---

## peers

Comparable companies in the same sector/industry.

```bash
ka peers -s MSFT
ka peers -s NVDA
```

**Typical output:** Array of ticker symbols, e.g. `["MSFT", "GOOG", "META", "AAPL", ...]`

---

## news-summary

AI-generated summary of the latest news for a symbol.

```bash
ka news-summary -s MSFT
ka news-summary -s TSLA
```

**Typical output fields:** `symbol`, `summary`, `sentiment`, `articles` (list of sources)

---

## earnings-moves

Historical price movement around past earnings announcements.

```bash
ka earnings-moves -s MSFT
ka earnings-moves -s NVDA -lookback 10
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `date`, `move_pct`, `direction`, `eps_surprise`, `beat_miss`,
`pre_move`, `post_move`, `avg_move`, `pct_positive`

---

## volatility

Historical volatility (rolling standard deviation of returns).

```bash
ka volatility -s MSFT -sd 2025-01-01 -ed 2025-12-31
ka volatility -s SPY -lookback 252
```

**Flags:** `-s`, `-sd`, `-ed`, `-lookback`
**Typical output fields:** `date`, `volatility`, `annualized_vol`, `period`

---

## seasonality

Monthly return patterns based on historical data.

```bash
ka seasonality -s MSFT
ka seasonality -s SPY -lookback 100
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `month`, `avg_return`, `positive_pct`, `count`, `best_year`,
`worst_year`

---

## quantstats

Risk-adjusted performance analytics (Sharpe, Sortino, max drawdown, CAGR).

```bash
ka quantstats -s MSFT -limit 252
ka quantstats -s AAPL -limit 504
```

**Flags:** `-s`, `-limit`
**Typical output fields:** `sharpe`, `sortino`, `max_drawdown`, `cagr`, `volatility`,
`win_rate`, `avg_gain`, `avg_loss`, `best_day`, `worst_day`, `total_return`

---

## price-dist

Price return distribution (histogram buckets, skewness, kurtosis).

```bash
ka price-dist -s MSFT
ka price-dist -s SPY -lookback 252
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `mean`, `std`, `skewness`, `kurtosis`, `min`, `max`,
`distribution` (array of `{bucket, count, pct}`)

---

## traderstats

Trader-focused statistics: win rate, average gain/loss, streaks.

```bash
ka traderstats -s MSFT
ka traderstats -s NVDA
```

**Typical output fields:** `win_rate`, `loss_rate`, `avg_gain_pct`, `avg_loss_pct`,
`max_win_streak`, `max_loss_streak`, `avg_holding_days`, `profit_factor`

---

## candle_patterns

Detect latest candlestick pattern formations (doji, hammer, engulfing, etc.).

```bash
ka candle_patterns -s MSFT
ka candle_patterns -s SPY
```

**Typical output fields:** `date`, `pattern`, `signal` (`bullish`/`bearish`/`neutral`),
`strength`, `description`

---

## updown

Historical up/down rally streak analysis.

```bash
ka updown -s MSFT
ka updown -s MSFT -lookback 100
ka updown -s MSFT -lookback 100 -min_days 3
```

**Flags:** `-s`, `-lookback`, `-min_days`
**Typical output fields:** `direction`, `length_days`, `start_date`, `end_date`,
`move_pct`, `avg_up_streak`, `avg_down_streak`

---

## fib

Fibonacci retracement and extension levels.

```bash
ka fib -s MSFT
ka fib -s MSFT -lookback 360
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `high`, `low`, `fib_0`, `fib_236`, `fib_382`, `fib_500`,
`fib_618`, `fib_786`, `fib_100`, `current_price`, `nearest_level`

---

## gap-analysis

Historical gap open analysis (gap up / gap down frequency, fill rate).

```bash
ka gap-analysis -s MSFT
ka gap-analysis -s TSLA -lookback 360
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `date`, `gap_pct`, `direction`, `filled`, `days_to_fill`,
`avg_gap_up`, `avg_gap_down`, `fill_rate_up`, `fill_rate_down`

---

## price-actions

Historical price action strategy analysis (breakouts, pullbacks, reversals).

```bash
ka price-actions -s MSFT
ka price-actions -s MSFT -lookback 360
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `strategy`, `signal`, `date`, `entry`, `exit`, `return_pct`,
`win_rate`, `avg_return`

---

## ta

Full technical analysis snapshot (RSI, MACD, Bollinger Bands, moving averages).

```bash
ka ta -s MSFT
ka ta -s NVDA
```

**Typical output fields:** `rsi`, `macd`, `macd_signal`, `macd_hist`, `sma_20`, `sma_50`,
`sma_200`, `ema_12`, `ema_26`, `bb_upper`, `bb_lower`, `bb_mid`, `adx`, `atr`,
`stoch_k`, `stoch_d`

---

## ta-signals

Condensed technical signal pack — bullish/bearish/neutral calls per indicator.

```bash
ka ta-signals -s MSFT
ka ta-signals -s SPY -lookback 360
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `indicator`, `value`, `signal` (`buy`/`sell`/`neutral`),
`strength`, `overall_signal`, `overall_strength`

---

## vol-profile

Detailed volume analysis by price level (volume at price).

```bash
ka vol-profile -s MSFT
ka vol-profile -s SPY -lookback 100
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `price_level`, `volume`, `pct_of_total`, `poc` (point of control),
`value_area_high`, `value_area_low`

---

## vol-unusual

Unusual volume spikes vs. average baseline.

```bash
ka vol-unusual -s MSFT
ka vol-unusual -s NVDA -lookback 100
```

**Flags:** `-s`, `-lookback`
**Typical output fields:** `date`, `volume`, `avg_volume`, `ratio`, `pct_above_avg`,
`price_change_pct`, `catalyst`

---

## bestdays

Best historical trading days by return.

```bash
ka bestdays -s MSFT
ka bestdays -s SPY
```

**Typical output fields:** `date`, `return_pct`, `open`, `close`, `volume`,
`event` (earnings/split/news if detected)

---

## ai-chat

Built-in AI chat interface — ask financial questions in plain English directly from the terminal.

```bash
ka ai-chat -q "What is the technical outlook for MSFT right now?"
ka ai-chat -q "Summarize earnings surprise history for NVDA"
ka ai-chat -q "Which S&P 500 sectors have the strongest momentum this month?"
ka ai-chat -q "Compare MSFT and AAPL volatility over the last 12 months"
ka ai-chat -q "Give me a pre-market briefing for US tech stocks"
```

**Flags:** `-q` (required — your natural language query)
**Output:** Structured analyst-style JSON response, pipeable into agent workflows

---

## Example multi-command workflows

### Pre-earnings research on NVDA
```bash
ka profile -s NVDA          # sector, background
ka earnings -s NVDA         # EPS history
ka earnings-moves -s NVDA   # how it reacts to earnings
ka ta-signals -s NVDA       # current technical setup
ka vol-unusual -s NVDA      # any unusual activity
```

### Daily pre-market scan
```bash
for sym in AAPL MSFT NVDA TSLA AMZN; do
  ka quote -s $sym -datatype json
done
```

### Quant research workflow
```bash
ka quantstats -s SPY -limit 504    # 2yr risk-adjusted stats
ka volatility -s SPY -lookback 252  # rolling volatility
ka seasonality -s SPY               # seasonal bias
ka price-dist -s SPY -lookback 252  # return distribution shape
```
