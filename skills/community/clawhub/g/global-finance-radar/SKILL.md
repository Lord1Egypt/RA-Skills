---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_d51ea8035d8011f1abc85254006c9bbf
    ReservedCode1: eweTRVNvKzEj+4a88iwRnnTcZuOLXXyzRJRKY4o6B6q4Euis5ndvJfOu27ehWLDnwFhYKmf+zbxJU2WcI6VDb+68bYRjFyIMGZNV27K+KgwNlZtH3M35hSrTe516/rcgiM0l62TapAlBQkJFTZNCkZbuLG1YNVxhja/QXvNmFqr0ZRgsM2bWPrM8Zq4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_d51ea8035d8011f1abc85254006c9bbf
    ReservedCode2: eweTRVNvKzEj+4a88iwRnnTcZuOLXXyzRJRKY4o6B6q4Euis5ndvJfOu27ehWLDnwFhYKmf+zbxJU2WcI6VDb+68bYRjFyIMGZNV27K+KgwNlZtH3M35hSrTe516/rcgiM0l62TapAlBQkJFTZNCkZbuLG1YNVxhja/QXvNmFqr0ZRgsM2bWPrM8Zq4=
---



# Global Finance Radar

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Central Bank Policy Monitor | Bank(s) + time horizon | Current rate, forward guidance, dot-plot/rate-path, meeting calendar, market-implied probabilities |
| 2 | Macroeconomic Dashboard | Country(ies) + indicators | GDP growth, CPI, unemployment, PMI, trade balance, debt/GDP, FX reserves — with trend arrows |
| 3 | Cross-Asset Market Brief | Asset class(es) + region | Price action, YTD performance, volatility, fund flows, positioning, key catalysts |
| 4 | Yield Curve & Recession Signal | Country | 2s10s spread, 3m10y spread, near-term forward spread, historical recession lead time, probability estimate |
| 5 | Currency Fair-Value Analysis | Currency pair | PPP estimate, REER deviation, Big Mac Index, FEER, carry-to-risk ratio, positioning (CFTC COT) |
| 6 | Equity Valuation Scanner | Index / sector / stock | PE (trailing/forward), EV/EBITDA, PEG, dividend yield, vs. 5Y avg, vs. peers, DuPont decomposition |
| 7 | Commodity Supply-Demand Outlook | Commodity | Inventory levels, production forecasts, demand drivers, cost curve, geopolitical risk overlay |
| 8 | Crypto Market Intelligence | Token / sector | On-chain metrics (active addresses, TVL, hash rate), regulatory developments, institutional flow, correlation to risk assets |
| 9 | Fixed Income Relative Value | Bond / maturity range | Yield, duration, convexity, OAS (credit), breakeven inflation (TIPS), cross-market spread |
| 10 | Global Risk Matrix | Time horizon | VIX/VSTOXX, CDS spreads, EMBI spread, financial conditions indices, geopolitical risk index, tail-risk scenario |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify query → asset class(es) + geography + time horizon + analysis type
  │
  ├─ [Step 2] Source selection:
  │   └─ Macro: IMF, World Bank, OECD, Trading Economics
  │   └─ Central banks: Fed (FRED), ECB (SDW), BIS
  │   └─ Markets: Investing.com, Yahoo Finance, CoinGecko
  │   └─ Commodities: WGC, OPEC MOMR
  │
  ├─ [Step 3] Data retrieval + cross-validation (≥2 sources for key metrics)
  │
  ├─ [Step 4] Apply relevant framework (DCF, DuPont, PPP, yield curve model)
  │
  ├─ [Step 5] Generate structured output with data vintage, source URLs
  │
  └─ [Step 6] Risk disclosure: flag data gaps, model limitations, non-investment-advice disclaimer
```

## Output Formats

### Central Bank Policy Snapshot
| Bank | Current Rate | Last Change | Next Meeting | Market-Implied Path | Hawkish/Dovish Bias |
|------|-------------|-------------|--------------|---------------------|---------------------|
| Fed | X.XX% | ±XXbp (Date) | Date | CME FedWatch probabilities | ... |
| ECB | X.XX% | ... | ... | ... | ... |

### Macro Dashboard
| Indicator | US | EU | CN | JP | IN | Trend |
|-----------|----|----|----|----|----|-------|
| GDP Growth (YoY%) | | | | | | ↑↓→ |
| CPI (YoY%) | | | | | | |
| Unemployment (%) | | | | | | |
| Mfg PMI | | | | | | |
| 10Y Yield (%) | | | | | | |

### Currency Fair-Value Table
| Pair | Spot | PPP Fair Value | Misvaluation % | REER Deviation | Carry (1Y) | Signal |
|------|------|---------------|----------------|----------------|------------|--------|
| EUR/USD | | | | | | Over/Under/Fair |

## Usage Guidelines

1. **Always cite data vintage** — stale data misleads; flag any indicator >30 days old
2. **Cross-validate** — use ≥2 sources for critical metrics (GDP, CPI, rates)
3. **Model transparency** — disclose methodology (e.g., "PPP based on OECD 2020 benchmark, extrapolated with CPI differentials")
4. **Non-investment-advice disclaimer** — mandatory on all outputs involving price forecasts or valuation signals
5. **Multi-language** — search and summarize across English, Chinese, Japanese, German, French, Spanish
6. **Forward-looking statements** — clearly distinguish between historical data, consensus forecasts, and model-generated projections

## Examples

### Example 1: Central Bank Divergence
**User**: "Compare Fed vs ECB vs BoJ policy outlook for H2 2026"
**Output**: Rate path table with market-implied probabilities; divergence chart narrative; FX implications (EUR/USD, USD/JPY).

### Example 2: Recession Check
**User**: "What's the recession probability for the US right now?"
**Output**: Yield curve spreads (2s10s, 3m10y, near-term forward), Sahm Rule indicator, LEI trend, consensus probability from surveys, historical context.

### Example 3: Commodity Outlook
**User**: "Gold price outlook for next 6 months"
**Output**: Real yield correlation, central bank buying trends, ETF flows, technical levels, geopolitical risk premium, consensus range.

---

**Data Base**: `references/finance_sources.json` — 12 data sources, 8 central banks, 9 economic indicators, 5 asset classes, 6 valuation frameworks.
**Last Updated**: June 2026
**Free Tier**: Available. This skill aggregates public financial data; no proprietary terminal data accessed.
*（内容由AI生成，仅供参考）*
