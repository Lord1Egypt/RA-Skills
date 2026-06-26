---
name: japanfinance-agent
description: "Compound MCP agent combining 6 Japan finance data sources — EDINET securities filings (有価証券報告書), TDNET timely disclosures (適時開示), e-Stat government statistics (GDP/CPI/雇用), BOJ central bank data (金利/マネーサプライ), financial news, J-Quants stock prices. Company analysis, macro snapshots, earnings monitoring. Japanese financial data aggregator."
metadata: {"openclaw":{"emoji":"🏯","requires":{"bins":["japanfinance-agent"]},"install":[{"id":"uv","kind":"uv","package":"japanfinance-agent[all]","bins":["japanfinance-agent"],"label":"Install japanfinance-agent with all data sources (uv)"}],"tags":["japan","finance","mcp","agent","edinet","tdnet","estat","boj","stock","compound-analysis"]}}
---

# Japan Finance Agent: Compound Analysis from 6 Data Sources

Combines EDINET, TDNET, e-Stat, BOJ, news, and stock price data into high-value compound analysis tools. Instead of calling each source individually, get comprehensive results in a single request.

## Use Cases

- Comprehensive company analysis (financial statements + disclosures + news + stock price)
- Macro economic snapshots (GDP, CPI, employment + central bank data + news)
- Earnings watchlist monitoring for multiple companies
- Check which data sources are available and connected

## Commands

### Analyze a company
```bash
japanfinance-agent analyze 7203
japanfinance-agent analyze 7203 -e E02144 -p 2025 --json-output
```

### Macro economic snapshot
```bash
japanfinance-agent macro
japanfinance-agent macro -k CPI
```

### Monitor earnings watchlist
```bash
japanfinance-agent monitor 7203 6758 6861
```

### Check data sources
```bash
japanfinance-agent test
```

### Start MCP server
```bash
japanfinance-agent serve
```

## Data Sources

| Source | Data | Auth |
|---|---|---|
| EDINET | Securities filings, XBRL financial statements | API key (free) |
| TDNET | Timely disclosures (earnings, dividends) | None |
| e-Stat | Government statistics (GDP, CPI, employment) | App ID (free) |
| BOJ | Central bank data (rates, money supply) | None |
| News | Financial news (Yahoo, NHK, Reuters) | None |
| J-Quants | Stock prices (OHLCV) | Email + Password |

## Setup

```bash
# Install with all data sources
pip install "japanfinance-agent[all]"

# Or pick specific sources
pip install "japanfinance-agent[edinet,tdnet,news]"
```

Missing packages degrade gracefully — the agent works with whatever sources are available.
