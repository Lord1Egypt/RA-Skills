---
description: Symbol search workflow - Quick search and discovery of trading instruments
---

# Symbol Search Workflow

Quickly search and discover trading instruments such as stocks, cryptocurrencies, forex, futures, etc.

## Execution Steps

### Step 1: Parse Search Intent

Extract search keywords and filter conditions from user input:
- Keywords: Stock names, codes, pinyin abbreviations, etc.
- Asset type: Stocks, cryptocurrencies, forex, futures, indices, funds, bonds, options
- Language preference: Chinese or English

### Step 2: Call Search Tool

Call `tradingview_search_market` for instrument search:

```
Parameter description:
- query: Search keywords (required)
- filter: Asset type filter (optional)
  - stock: Stocks
  - crypto: Cryptocurrency
  - forex: Forex
  - futures: Futures
  - index: Indices
  - funds: Funds
  - bond: Bonds
  - options: Options
- lang: Language code (default en)
- limit: Number of results (default 20, max 100)
```

### Step 3: Format Search Results

Organize search results into readable format, including:
- Instrument code (e.g., NASDAQ:AAPL)
- Exchange name
- Full name and description
- Asset type
- Currency code
- Country

### Step 4: Provide Follow-up Action Suggestions

Based on search results, suggest subsequent operations users can perform:
- View real-time quotes
- View technical analysis
- View historical price data
- View related news

## Example Conversations

**User**: "Help me search for Apple company's stock"

**Execution**:
1. Call `tradingview_search_market`, query="AAPL", filter="stock"
2. Return results including NASDAQ:AAPL and other matches
3. Suggest user can view real-time quotes or technical analysis

---

**User**: "Search for Bitcoin-related trading pairs"

**Execution**:
1. Call `tradingview_search_market`, query="BTC", filter="crypto"
2. Return BINANCE:BTCUSDT, COINBASE:BTCUSD and other trading pairs
3. Suggest user select specific trading pair for in-depth analysis
