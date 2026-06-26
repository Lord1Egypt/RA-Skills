<!--
v4.x adaptation note: this is a feature-catalog doc carried forward
from v2.6. The financial-analysis surface is unchanged in v4.x —
only the invocation surface differs. Replace any v2.x slash-command
syntax (e.g. `/portfolio holdings`) with the equivalent v4.x MCP tool
call (e.g. `portfolio_holdings`) or a natural-language query through
`portfolio_ask` (e.g. "Show me my holdings"). Numerical results,
methodology, and data-source rules are identical.
-->

# InvestorClaw Capabilities

v4.1.x | Financial Analysis + Data Connectivity | For portfolio owners, advisors, and developers

## InvestorClaw Architecture

InvestorClaw combines three coordinated systems. It uses a deterministic portfolio analysis engine, an LLM synthesis layer, and a data connectivity scaffold.

These systems stay separate by design. The LLM does not perform portfolio math.

```text
┌─────────────────────────────────────────────────────────────┐
│ CONVERSATIONAL LAYER (Agent + Natural Language)             │
│ - Interprets "How am I doing?" → routes to performance()    │
│ - Synthesizes JSON results into advisor-grade narratives    │
│ - Answers follow-up questions ("What does Sharpe mean?")    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ COMPUTATION LAYER (Deterministic Python Pipelines)          │
│ - Fetches live prices (Finnhub, Massive, yfinance)          │
│ - Calculates Sharpe, beta, duration, YTM (no LLM math)      │
│ - Runs Modern Portfolio Theory optimization                 │
│ - Outputs compact JSON (270 positions = 2K tokens)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ DATA LAYER (Pluggable Connectors)                           │
│ - CSV/Excel/PDF import (broker statements)                  │
│ - Real-time market data (5 provider integrations)           │
│ - Analyst ratings, news sentiment, Treasury benchmarks      │
│ - FRED economic data, yfinance fallback (unlimited)         │
└─────────────────────────────────────────────────────────────┘
```

## Financial Analysis

### Holdings Analysis

InvestorClaw builds a live snapshot of your portfolio. It includes real-time pricing and sector breakdowns.

User query: "What's in my portfolio?"

InvestorClaw output:

```json
{
  "timestamp": "2026-04-19T14:32:00Z",
  "total_value": 1250000,
  "positions": [
    {
      "ticker": "AAPL",
      "shares": 100,
      "price": 215.50,
      "market_value": 21550,
      "weight_pct": 1.72,
      "sector": "Technology",
      "asset_class": "US Equity"
    }
    // ... 49 more positions
  ],
  "concentration": {
    "hhi_score": 0.087,
    "risk_classification": "Moderate Concentration",
    "top_10_weight_pct": 42.3
  },
  "sector_allocation": {
    "Technology": 28.5,
    "Healthcare": 18.2,
    "Financials": 15.1,
    // ...
  }
}
```

| Detail | Value |
|---|---|
| Data sources | Finnhub (real-time) → Massive → Alpha Vantage → yfinance (fallback) |
| API keys required | None (yfinance fallback included) |
| Latency | <2 seconds (cached after first fetch) |

### Performance Analysis

InvestorClaw measures risk-adjusted returns against benchmarks.

User query: "How am I doing? Am I beating the S&P 500?"

InvestorClaw output:

```json
{
  "returns": {
    "ytd_return_pct": 8.2,
    "one_year_return_pct": 12.5,
    "inception_return_pct": 45.3
  },
  "risk_metrics": {
    "volatility_annual_pct": 9.8,
    "sharpe_ratio": 1.28,
    "sortino_ratio": 1.92,
    "max_drawdown_pct": -12.4,
    "beta_vs_sp500": 0.95,
    "correlation_vs_sp500": 0.87
  },
  "benchmark_comparison": {
    "sp500_ytd_return_pct": 6.1,
    "portfolio_outperformance_bps": 210,  // 2.1% ahead
    "jensen_alpha": 0.042
  }
}
```

| Detail | Value |
|---|---|
| Calculations | All deterministic (no LLM math) |
| Benchmarks | S&P 500, Russell 2000, MSCI EAFE, etc. |
| Time periods | YTD, 1Y, 3Y, 5Y, inception |
| Data sources | yfinance (historical prices) + FRED (risk-free rate) |

### Bond Analytics

InvestorClaw analyzes fixed-income holdings. It reports duration and yield risk.

User query: "Show my bond exposure. What are the durations?"

InvestorClaw output:

```json
{
  "bonds": [
    {
      "ticker": "VBTLX",
      "isin": "...",
      "position_value": 125000,
      "ytm_pct": 4.2,
      "duration_years": 6.8,
      "modified_duration": 6.5,
      "convexity": 52.1,
      "credit_quality": "A+",
      "maturity_years": 8.5
    }
  ],
  "portfolio_bond_metrics": {
    "total_bond_value": 250000,
    "bond_weight_pct": 20,
    "average_ytm_pct": 4.05,
    "portfolio_duration_years": 5.2,
    "interest_rate_sensitivity": "For every 1% rate rise, portfolio loses 5.2%"
  },
  "fred_benchmarks": {
    "10y_treasury_ytm_pct": 4.35,
    "portfolio_vs_10y_spread_bps": -30,  // 0.3% cheaper
    "3m_tbill_ytm_pct": 5.5
  }
}
```

| Detail | Value |
|---|---|
| Calculations | Newton-Raphson YTM solver, Macaulay/modified duration, convexity (all Python math) |
| Data sources | Bond details from fund fact sheets + FRED Treasury yields |
| Coverage | US Treasuries, corporates, municipals (via isin lookups) |

### Portfolio Optimization

InvestorClaw suggests rebalancing with Modern Portfolio Theory.

User query: "How should I rebalance? What's the optimal allocation?"

InvestorClaw output:

```json
{
  "optimization_method": "Sharpe Ratio Maximization",
  "efficient_frontier": {
    "optimal_weights": {
      "US_Equity": 0.60,
      "International_Equity": 0.15,
      "Bonds": 0.20,
      "Cash": 0.05
    },
    "expected_return_pct": 7.2,
    "expected_volatility_pct": 8.1,
    "optimal_sharpe_ratio": 0.89
  },
  "current_vs_optimal": {
    "current_weights": { /* ... */ },
    "rebalancing_trades": [
      { "action": "BUY", "ticker": "VTI", "shares": 150, "rationale": "Increase US equity to 60%" },
      { "action": "SELL", "ticker": "AAPL", "shares": 50, "rationale": "Reduce concentration" }
    ],
    "estimated_tax_impact": -$1500
  },
  "efficient_frontier_chart": "SVG plot showing risk/return tradeoff"
}
```

Supported methods:

- Sharpe ratio maximization: Highest risk-adjusted return.
- Min-volatility: Lowest portfolio variance.
- Black-Litterman: Incorporates your return views + market expectations.
- Discrete allocation: Suggests share counts (not just percentages).

Visualization: SVG efficient frontier chart showing risk/return curve.

### Analyst Consensus and News

InvestorClaw surfaces Wall Street opinions and news sentiment for your holdings.

User query: "What does Wall Street think? Any analyst upgrades?"

InvestorClaw output:

```json
{
  "analyst_data": [
    {
      "ticker": "MSFT",
      "current_price": 415.20,
      "analyst_target_price": 475.00,
      "upside_pct": 14.4,
      "consensus_rating": "BUY",
      "ratings_breakdown": {
        "buy": 22,
        "hold": 5,
        "sell": 1
      },
      "target_price_range": [420, 520],
      "recent_upgrades": [
        { "date": "2026-04-15", "analyst": "Goldman Sachs", "from": "Hold", "to": "Buy" }
      ]
    }
  ],
  "portfolio_news": [
    {
      "date": "2026-04-18",
      "headline": "Microsoft announces $10B AI infrastructure investment",
      "tickers": ["MSFT"],
      "sentiment": "positive",
      "relevance_score": 0.92
    }
  ]
}
```

Data sources:

- Analyst ratings: Finnhub (14K+ analysts, live updates)
- News: NewsAPI (100K+ sources), yfinance
- Sentiment: NLP tagging (positive/neutral/negative)

### End-of-Day Reports

InvestorClaw generates a synthesized portfolio narrative and performance summary.

User query: "Generate an EOD report"

InvestorClaw output:

```text
PORTFOLIO DAILY SUMMARY — 2026-04-19
═════════════════════════════════════════════════════════

Performance Today
─────────────────
Portfolio: +1.2% ($15,000 gain)
S&P 500:   +0.8%
Outperformance: +40 bps ✓

Key Movements
─────────────
📈 Technology sector +2.1% (your weight: 28.5%)
📈 NVIDIA +4.2%, Microsoft +2.8%
📉 Utilities -0.5% (your weight: 8.2%)

Risk Indicators
───────────────
Portfolio volatility: 9.8% (annualized)
Max drawdown (YTD): -12.4%
Sharpe ratio: 1.28 (above benchmark 0.92)

Analyst Activity
────────────────
1 upgrade (Goldman Sachs upgrades MSFT to Buy)
No downgrades today

Bond Market
───────────
10Y Treasury: 4.35% (+2 bps)
Your portfolio duration: 5.2 years
Interest rate sensitivity: -5.2% per 1% rate rise

⚠️  DISCLAIMER: This is educational analysis, not investment advice.
Consult a qualified financial professional before making decisions.

═════════════════════════════════════════════════════════
Generated by InvestorClaw v2.2.2
```

| Detail | Value |
|---|---|
| Output format | HTML (email-ready) or text |
| Refresh | On-demand (not scheduled) |

## Data Connectivity

### Market Data Providers

InvestorClaw uses 5 independent data sources. It fails over automatically when a provider is unavailable.

| Provider | Latency | Coverage | Strengths | Requires API Key |
|---|---|---|---|---|
| Finnhub | <100ms | 200K+ tickers | Real-time, analyst data, news | Yes (free tier: 60/min) |
| Massive | 200-500ms | 50K+ tickers | High-quality, real-time | Yes (enterprise) |
| Alpha Vantage | 1-2s | US equities | Reliable, free tier available | Yes (5/min free) |
| yfinance | 2-5s | Unlimited | Free, no limits, complete fallback | No |
| FRED (Federal Reserve) | 200ms | 500K+ economic series | Treasury yields, benchmarks | Yes (free, unlimited) |

Failover order:

1. Try Finnhub (real-time, <100ms).
2. If rate-limited or down, try Massive.
3. If unavailable, use Alpha Vantage.
4. If still no response, fall back to yfinance (always works).
5. For Treasury data, use FRED; fall back to yfinance.

> [!NOTE]
> InvestorClaw provides zero-config fallback to yfinance. Users still get live data with no API keys.

### Portfolio Data Import

InvestorClaw imports portfolio data from multiple formats.

Supported formats:

- CSV (preferred): Schwab, Fidelity, Vanguard, UBS, E*TRADE export formats
- Excel (.xls, .xlsx): Auto-detected columns (Symbol, Shares, Price, Cost Basis)
- PDF: Broker statements (tabular data extraction)
- JSON: FINOS CDM standard (machine-generated)

InvestorClaw detects formats automatically.

```python
import_format = sniff_format(file_path)
# Detects CSV dialect, Excel sheet structure, PDF tables
# Maps "CUSIP" → "cusip", "Num Shares" → "shares", etc.
```

Example CSV (Schwab export):

```csv
Symbol,Quantity,Price ($),Position Value ($)
AAPL,100,215.50,21550
MSFT,50,415.20,20760
VTI,75,265.30,19897
```

InvestorClaw auto-maps column names to the internal CDM schema.

### Real-Time Price Updates

InvestorClaw supports three update modes.

#### On-demand

Use this mode to fetch the latest prices immediately.

```bash
portfolio_holdings --refresh
# Fetches latest prices immediately
```

#### Cached

Use this mode to reuse prices from the last fetch.

```bash
portfolio_holdings
# Uses cached prices from last fetch (faster, cheaper on API quota)
```

#### Scheduled

Use this mode for background refreshes.

- Zeroclaw daemon can refresh every N minutes.
- Useful for dashboards.
- Not required for CLI.

### News and Sentiment Aggregation

InvestorClaw aggregates news and correlates it to your holdings.

Data sources:

- NewsAPI: 100K+ publishers (Bloomberg, Reuters, WSJ, etc.)
- yfinance: Yahoo Finance news feed

Correlation logic:

```python
def portfolio_news_feed():
  news_items = fetch_news_all_tickers()
  # Filter to portfolio holdings only
  # Tag with sentiment (positive/negative/neutral)
  # Score by relevance (0.0–1.0)
  return sorted(news_items, key=lambda x: x.relevance_score, reverse=True)
```

Example:

```json
{
  "headline": "Microsoft announces $10B AI infrastructure investment",
  "source": "Bloomberg",
  "date": "2026-04-18",
  "tickers": ["MSFT"],
  "sentiment": "positive",
  "relevance_score": 0.92,  // high relevance to your MSFT position
  "url": "https://..."
}
```

### FRED Economic Data Integration

InvestorClaw uses FRED data for benchmarks and macro context.

Treasury benchmarks:

```json
{
  "fred_data": {
    "10y_treasury_yield": 4.35,
    "3m_tbill_yield": 5.50,
    "2y_treasury_yield": 4.80,
    "fed_funds_rate": 5.50,
    "unemployment_rate": 3.8,
    "inflation_cpi": 3.2
  }
}
```

Used for:

- Bond yield comparisons (is your 4.0% bond attractive vs. 4.35% Treasury?)
- Risk-free rate (Sharpe ratio calculations)
- Macroeconomic context (recession risk, inflation expectations)

## Dashboard Portal

InvestorClaw v4.x ships a web-based dashboard portal at
`http://localhost:18092`. It is the human-facing surface, separate
from the MCP-HTTP agent surface on port 18090.

### 17 tabs

| Tab | What it shows |
|---|---|
| **Overview** | Portfolio summary card + Regenerate sweep button |
| **Holdings** | Positions, values, weights, account breakdown |
| **Performance** | Returns, Sharpe, Sortino, max drawdown, beta, VaR |
| **WhatChanged** | Delta snapshot vs. prior run |
| **Scenarios** | Rate-shock, drawdown, and correlation-break what-if |
| **Bonds** | YTM, duration, convexity, FRED yield-curve overlay |
| **Optimize** | MPT: Sharpe-max, min-vol, target-return frontiers |
| **Cashflow** | Projected dividends and bond coupons |
| **Peer** | Peer and benchmark comparison |
| **Analyst** | Analyst consensus ratings per holding |
| **News** | News correlation for held positions |
| **Markets** | Market-wide news and macro data |
| **Lookup** | Ticker / account lookup |
| **Synthesis** | LLM-synthesized portfolio narrative |
| **Reports** | Browse and download EOD and advisor reports |
| **Settings** | API keys, portfolio upload form, preferences |
| **About** | Version, license, attribution |

All 30 natural-language queries in the agentic COBOL test suite map
to one of these 17 tabs — coverage is complete.

### Regenerate button

The **Regenerate** button on the Overview tab fires a full background
sweep: `setup → refresh → 12 section analyzers`. Use it to rebuild the
entire cache after uploading a new portfolio or at the start of a session.

### Portfolio file upload

The Settings tab includes a web upload form that accepts `.csv`,
`.tsv`, `.xls`, `.xlsx`, `.pdf`, `.json`, `.ofx`, and `.qfx` files.
The form sanitizes the filename, writes the file to `/data/portfolios/`
inside the container, and queues a refresh automatically. This is the
simplest path for non-technical users.

### API key configuration

All 8 provider keys are configurable via the Settings tab without a
shell or container restart:

| Key | Provider |
|---|---|
| `TOGETHER_API_KEY` | Together AI (narrative synthesis) |
| `OPENAI_API_KEY` | OpenAI (alternative narrative provider) |
| `FINNHUB_KEY` | Finnhub (real-time quotes + analyst ratings) |
| `FRED_API_KEY` | FRED (Treasury yields + macro indicators) |
| `NEWSAPI_KEY` | NewsAPI (per-symbol + market news) |
| `ALPHA_VANTAGE_KEY` | Alpha Vantage (quote fallback) |
| `MASSIVE_API_KEY` | Massive via Massive (high-scale, 200+ symbols) |
| `MARKETAUX_API_KEY` | MarketAux (alternative news source) |

Keys can also be set via the `portfolio_keys_set` MCP tool from your
agent.

## Configuration and Deployment

### API Key Management

InvestorClaw checks API keys in a fixed order.

#### 1. Shell environment variables

This source has the highest priority.

```bash
export FINNHUB_KEY="pk_live_xxx"
export NEWSAPI_KEY="xxx"
investorclaw holdings  # Uses FINNHUB_KEY
```

#### 2. `.env` file

InvestorClaw checks your home directory next.

```bash
~/.investorclaw/.env
FINNHUB_KEY=pk_live_xxx
NEWSAPI_KEY=xxx
FRED_API_KEY=xxx
```

#### 3. Setup wizard config

InvestorClaw can collect keys during first-run setup.

```bash
investorclaw setup
# Prompts for optional API keys, saves to ~/.investorclaw/config.toml
```

#### 4. Fallback

InvestorClaw still works with no keys.

```bash
# Uses yfinance (unlimited, free, no registration)
investorclaw holdings
```

> [!NOTE]
> InvestorClaw works without any API keys. Users can add keys later to unlock real-time data.

### Deployment Modes

InvestorClaw supports three deployment modes.

#### Single-Investor

This is the default mode.

- Personal laptop, iPad, or home server
- Portfolio CSV in `~/portfolios/`
- Results saved to `~/portfolio_reports/`
- No cloud connectivity required

#### FA Professional

This mode targets advisors.

- Multi-client support
- Compliance-grade audit logs
- Custom branding
- Runs on dedicated server or cloud

#### Zeroclaw

This mode targets edge and Raspberry Pi deployments.

- Lightweight Python runtime on Raspberry Pi
- Offline-capable (yfinance caching)
- Paired with central agent (192.0.2.56)
- No cloud calls unless explicitly configured

## End-to-End Example

InvestorClaw can process a full portfolio workflow in about 3 seconds.

User asks: "I just got my Schwab export. How's my portfolio doing compared to the market?"

InvestorClaw workflow:

1. Data import (CSV parser)
   - Reads `~/portfolios/schwab_2026_04_19.csv`
   - Maps columns: Symbol → ticker, Quantity → shares, etc.
   - Validates 50 holdings found
2. Price fetch (data layer)
   - Tries Finnhub for each ticker (100ms each, cached after 5 min)
   - Falls back to yfinance if rate-limited
   - Builds holdings JSON
3. Analysis (computation layer)
   - Calculates concentration (HHI score)
   - Sector breakdown
   - Beta vs. S&P 500
   - Sharpe ratio vs. benchmark
4. Synthesis (conversational layer)
   - Agent receives compact JSON (holdings + metrics)
   - Constructs response: "Your portfolio is up 8.2% YTD, beating the S&P by 2.1%. Your tech weight (28.5%) is driving outperformance, but concentration risk is moderate (HHI=0.087)."
5. Guardrails (always on)
   - Agent appends: "⚠️ This is educational analysis, not investment advice. Consult a qualified financial professional."

| Detail | Value |
|---|---|
| Total time | ~3 seconds (2.5s for price fetches, 0.5s for calculation) |
| Data sent to cloud | Only the API calls to Finnhub/yfinance/FRED (ticker symbols only, no account details) |
| Sensitive data handling | Portfolio holdings never leave your machine |

## Product Comparison

This table shows what InvestorClaw is and is not.

| Capability | InvestorClaw | Robinhood | Schwab | ChatGPT |
|---|---|---|---|---|
| Live prices | ✅ (Finnhub/yfinance) | ✅ (in-house) | ✅ (in-house) | ❌ (stale) |
| Portfolio analysis | ✅ (deterministic math) | ⚠️ (basic) | ✅ (full) | ❌ (generic) |
| Optimization | ✅ (MPT) | ❌ | ⚠️ (limited) | ❌ |
| Execute trades | ❌ | ✅ | ✅ | ❌ |
| Fiduciary advice | ❌ | ❌ | ✅ (FA mode) | ❌ |
| Natural language Q&A | ✅ | ❌ | ❌ | ✅ (but no data) |
| Local/offline capable | ✅ | ❌ | ❌ | ❌ |
| Custom data sources | ✅ (plugin architecture) | ❌ | ❌ | ❌ |

## Data Flow

InvestorClaw routes data through a fixed pipeline.

```text
User: "How am I doing?"
  ↓
Agent (conversational): Routes → performance() command
  ↓
Command layer: Executes performance.py
  ↓
  ├─ Data layer: fetch_prices() → Finnhub/yfinance
  ├─ Data layer: fetch_historical() → yfinance
  ├─ Data layer: fetch_benchmarks() → FRED
  ↓
Computation layer: Calculate Sharpe, beta, alpha
  ↓
Output: performance.json (compact, ~500 bytes)
  ↓
Agent (synthesis): Reads JSON, generates response
  ↓
"Your portfolio is up 8.2% YTD, beating the S&P by 2.1%.
 Sharpe ratio of 1.28 suggests good risk-adjusted returns.
 Your tech weight (28.5%) is driving outperformance...
 ⚠️ This is educational analysis, not investment advice."
```

## Privacy and Security

InvestorClaw keeps portfolio analysis local by default.

- No cloud by default: All portfolio math runs locally
- Minimal data transmission: Only ticker symbols sent to data providers (no holdings, no values)
- Encryption: Optional encryption for sensitive config files
- Audit logs: Compliance-grade logging (FA mode)
- FINOS CDM: Industry-standard, privacy-respecting schema

## Further Reading

- [COMMANDS.md](COMMANDS.md): All 15 commands with usage examples
- [CONFIGURATION.md](CONFIGURATION.md): API keys, environment variables, advanced setup
- [FEATURES.md](FEATURES.md): What InvestorClaw does and doesn't do
- [MODELS.md](MODELS.md): Sharpe ratio, beta, YTM, duration formulas
- [DEPLOYMENT.md](DEPLOYMENT.md): Production setup, scaling, multi-user

## Summary

InvestorClaw is a three-layer deterministic + LLM system. The LLM never touches portfolio math.

InvestorClaw encrypts data locally. It produces results that are compact enough to fit in a conversational context window.

InvestorClaw works without any API keys because it can fall back to yfinance. It scales from a laptop to a $10B advisory firm.