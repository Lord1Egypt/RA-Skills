---
name: infoway-financial-data
description: Real-time financial market data MCP server — stocks, crypto, forex quotes, klines, sector analysis and fundamentals
install: pip install infoway-mcp-server
env:
  INFOWAY_API_KEY:
    description: Infoway API key for authenticating requests
    required: true
---

# Infoway Market Data — 20,000+ Stocks, Crypto & Forex

Real-time financial market data for Claude. Stream live quotes, candlestick/kline charts, market depth, sector heatmaps, and company fundamentals across 20,000+ instruments — US, HK, CN, SG stocks, crypto, and forex.

## Install

```bash
pip install infoway-mcp-server
```

## Required Environment Variables

- `INFOWAY_API_KEY` — Your Infoway API key. Get a free key at [infoway.io](https://infoway.io) (7-day free trial with full access).

## Configuration

```json
{
  "mcpServers": {
    "infoway": {
      "command": "uvx",
      "args": ["infoway-mcp-server"],
      "env": {
        "INFOWAY_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## Tools

### Real-Time Market Data
- `get_realtime_trade` — Get real-time trade data (price, volume, change) for stocks, crypto, or forex
- `get_market_depth` — Get order book / bid-ask depth for given symbols
- `get_kline` — Get candlestick / K-line (OHLCV) data with multiple intervals (1m to yearly)

### Market Overview
- `get_market_temperature` — Market sentiment and heat indicators for HK, US, CN, SG
- `get_market_breadth` — Advance/decline statistics for a market
- `get_global_indexes` — Real-time data for major global indexes (Dow, S&P, Nasdaq, HSI, etc.)
- `get_leading_industries` — Top-performing industry sectors ranked by performance

### Sector / Plate Analysis
- `get_industry_list` — Full list of industry sectors with performance data
- `get_concept_list` — Thematic/concept sectors (AI, EV, Metaverse, etc.)
- `get_plate_members` — All stocks within a specific sector/plate
- `get_plate_heatmap` — Sector heatmap data for market visualization

### Stock Fundamentals
- `get_company_overview` — Company profile, description, CEO, headquarters, key metrics
- `get_stock_valuation` — Valuation ratios: P/E, P/B, EV/EBITDA, dividend yield, market cap
- `get_stock_ratings` — Analyst consensus: buy/sell/hold counts, target price
- `get_stock_panorama` — Comprehensive stock summary with key financial data
- `get_stock_drivers` — Key price drivers and catalysts affecting the stock

### Utilities
- `search_symbols` — Search and list available trading symbols, optionally filtered by market

## Example Prompts

- "What's the current price of Apple and Tesla?"
- "Show me the daily K-line for Bitcoin over the last 30 days"
- "How is the US market doing today? Which sectors are leading?"
- "Give me a full analysis of Tencent including valuation and analyst ratings"
- "Compare the valuation of NVIDIA vs AMD"
- "What are the top concept sectors in the HK market right now?"
