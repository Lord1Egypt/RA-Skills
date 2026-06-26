# Stock Analysis Framework

This file defines the scoring rules and thresholds used to generate BUY / HOLD / SELL signals.

---

## Scoring Model

Each stock receives a score from **-10 to +10**. Positive = bullish, Negative = bearish.

| Score range | Signal |
|-------------|--------|
| +4 to +10   | 🟢 BUY |
| -3 to +3    | 🟡 HOLD |
| -4 to -10   | 🔴 SELL |

Confidence level:
- |score| ≥ 7 → **HIGH**
- |score| 4–6 → **MEDIUM**
- |score| 1–3 → **LOW**

---

## Factor Scoring Rules

Apply each rule that can be evaluated from available data. Skip rules with missing data (don't penalize for missing data).

### Price Momentum (max ±4 pts)

| Condition | Score |
|-----------|-------|
| Today's change > +3% | +2 |
| Today's change +1% to +3% | +1 |
| Today's change -1% to +1% | 0 |
| Today's change -1% to -3% | -1 |
| Today's change < -3% | -2 |
| Price in upper 25% of 52-week range | +1 |
| Price in upper 10% of 52-week range (near high) | -1 (overbought) |
| Price in lower 25% of 52-week range | -1 |
| Price in lower 10% of 52-week range (near low) | +1 (oversold bounce potential) |

**52-week position formula:**
```
position = (current_price - week52_low) / (week52_high - week52_low)
```
- position > 0.75 → "upper 25%"
- position > 0.90 → "upper 10%"
- position < 0.25 → "lower 25%"
- position < 0.10 → "lower 10%"

### Volume Signal (max ±2 pts)

| Condition | Score |
|-----------|-------|
| Current volume > 2× 30-day avg AND price up | +2 (strong buying) |
| Current volume > 1.5× avg AND price up | +1 |
| Current volume < 0.5× avg | -1 (low conviction) |
| Current volume > 2× avg AND price down | -2 (strong selling) |
| Current volume > 1.5× avg AND price down | -1 |

### Valuation (max ±2 pts)

Use P/E ratio vs. sector benchmark. If sector unknown, use S&P 500 average (~22×).

| Condition | Score |
|-----------|-------|
| P/E < 0.7× sector avg (undervalued) | +2 |
| P/E 0.7–1.0× sector avg | +1 |
| P/E 1.0–1.5× sector avg | 0 |
| P/E 1.5–2.0× sector avg (elevated) | -1 |
| P/E > 2.0× sector avg (very high) | -2 |
| P/E negative (loss-making) | -1 |
| No P/E available | 0 (skip) |

**Sector P/E benchmarks (2026 estimates):**
| Sector | Approx P/E |
|--------|-----------|
| Technology | 28× |
| Consumer Discretionary | 24× |
| Healthcare | 20× |
| Financials | 14× |
| Energy | 12× |
| Utilities | 16× |
| Industrials | 20× |
| Default (unknown) | 22× |

### News Sentiment (max ±3 pts)

Analyze the top 5–8 headlines fetched. Score by counting positive vs. negative signals:

**Positive keywords (+0.5 pt each, max +3):**
`beat`, `record`, `growth`, `partnership`, `raised guidance`, `buyback`, `dividend`, `acquisition` (as acquirer), `approved`, `launched`, `upgrade`, `exceeded`, `strong demand`

**Negative keywords (-0.5 pt each, max -3):**
`miss`, `cut guidance`, `layoffs`, `recall`, `investigation`, `SEC`, `lawsuit`, `fine`, `downgrade`, `loss`, `bankruptcy`, `resigned`, `delay`, `tariff`, `ban`

**High-impact overrides (apply once each):**
| Trigger | Override score |
|---------|----------------|
| Headline contains "earnings beat" or "beat estimates" | force +2 |
| Headline contains "earnings miss" or "missed estimates" | force -2 |
| Headline contains "merger" or "acquisition" of this company | +3 (M&A premium) |
| Headline contains "bankruptcy" or "chapter 11" | force -5 |
| Headline contains "CEO resign" or "CFO resign" | -2 |
| Headline contains "stock split" | +1 |
| Headline contains "FDA approved" (pharma) | +3 |
| Headline contains "FDA rejected" (pharma) | -4 |

**Calculation:**
```
news_score = clamp(positive_count * 0.5 - negative_count * 0.5, -3, +3)
Apply overrides on top (cap total at ±3).
```

---

## Composite Score Calculation

```python
total = momentum_score + volume_score + valuation_score + news_score
total = clamp(total, -10, +10)

if total >= 4:   signal = "BUY"
elif total <= -4: signal = "SELL"
else:            signal = "HOLD"

abs_score = abs(total)
if abs_score >= 7:  confidence = "HIGH"
elif abs_score >= 4: confidence = "MEDIUM"
else:               confidence = "LOW"
```

---

## Risk Modifiers (Add to Recommendation Text Only)

These don't change the score but must appear in the recommendation text if applicable:

| Condition | Warning text |
|-----------|-------------|
| Earnings in next 7 days | ⚠️ Earnings upcoming — elevated volatility expected |
| Price up >10% in 5 days | ⚠️ Short-term overbought — wait for pullback |
| Price down >15% in 5 days | ⚠️ Sharp recent drop — confirm trend before buying |
| Volume spike with no news | ⚠️ Unusual volume without clear catalyst |
| Market cap < $2B (small cap) | ⚠️ Small-cap stock — higher volatility and risk |

---

## Stop-Loss & Target Guidance

Include in BUY recommendations:

```
Stop-loss: current_price × 0.95   (5% below entry)
Target 1:  current_price × 1.08   (8% above entry)
Target 2:  52-week high × 1.02    (break above resistance)
```

Include in SELL recommendations:
```
Cover target: current_price × 0.92  (8% below current)
```

---

## Example Scorecard Output

```
──────────────────────────────────────────
📈 AAPL (Apple Inc.) — NASDAQ
──────────────────────────────────────────
Price:       $182.30   (+1.4% today)
52-week:     $143.90 – $199.62  (position: 72%)
Volume:      62.3M  (1.3× avg)

Scoring:
  Momentum     +1  (change +1.4%, position 72%)
  Volume       +1  (1.3× avg, price up)
  Valuation    -1  (P/E 28.5, sector avg 28×)
  News         +2  (3 positive / 1 negative headlines)
  ──────────────
  Total score  +3  → 🟡 HOLD  [Confidence: LOW]

Top headlines:
  ✅ "Apple beats Q2 revenue estimates by 4%" — Reuters (3h)
  ✅ "iPhone 17 demand stronger than expected" — Bloomberg (6h)
  ⚠️  "EU antitrust probe expanded to App Store" — FT (8h)

Recommendation:
  HOLD current position. Positive earnings momentum offset by
  regulatory headwinds. Consider adding on dips to $175.
  Stop-loss: $173.18  |  Target: $196.88

──────────────────────────────────────────
⚠️ This is not financial advice.
──────────────────────────────────────────
```

---

## Disclaimer

This framework applies simple heuristics to publicly available data. It does not account for macroeconomic conditions, insider information, options positioning, or sector rotation. Always consult a licensed financial advisor before making investment decisions.
