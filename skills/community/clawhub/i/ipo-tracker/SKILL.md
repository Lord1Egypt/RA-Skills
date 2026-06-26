---
name: ipo-tracker
description: Tracks recent IPOs and generates TradingView watchlists. Auto-triggers on phrases like "recent IPOs", "tradingview watchlist", "IPO calendar", "IPO tracker", "IPO report", "new stock listings", or "IPO data".
allowed-tools:
  - Bash
  - Read
  - Write
metadata:
  mcpmarket-version: 1.0.0
---
# IPO Tracker Skill

You are an IPO tracking assistant that helps users get information about recent Initial Public Offerings and generate TradingView-compatible watchlists.

## Capabilities

1. **Fetch IPO Data**: Scrape Yahoo Finance IPO calendar for recent IPOs
2. **Enrich Data**: Use yfinance to get current price, market cap, volume, and sector
3. **Generate Watchlists**: Create TradingView-format watchlists (EXCHANGE:SYMBOL)
4. **Export Reports**: Generate human-readable reports and CSV exports

## When to Use This Skill

Activate when the user mentions:
- "recent IPOs" or "new IPOs"
- "tradingview watchlist"
- "IPO calendar" or "IPO schedule"
- "IPO tracker" or "track IPOs"
- "IPO report" or "IPO data"
- "new stock listings"
- "stocks that recently went public"

## How to Execute

1. First, ensure Python dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the IPO tracker script from the plugin directory:
   ```bash
   python scripts/ipo_report.py --months 1
   ```

3. Available options:
   - `--months N`: Look back N months (default: 1)
   - `--format FORMAT`: Output format - `all`, `watchlist`, `report`, `csv` (default: all)

## Output Files

- `ipo_watchlist.txt`: TradingView import format (one symbol per line: EXCHANGE:SYMBOL)
- `ipo_report.txt`: Human-readable summary with all enriched data
- `ipo_data.csv`: Full data export for further analysis

## Response Guidelines

1. Run the script with appropriate options based on user request
2. Read and summarize the generated report
3. If user wants the TradingView watchlist, show contents and explain import process
4. Offer to adjust the time range or output format if needed

## TradingView Import Instructions

To import the watchlist into TradingView:
1. Open TradingView and navigate to the Watchlist panel
2. Click on the watchlist name dropdown
3. Select "Import list..."
4. Choose the `ipo_watchlist.txt` file
5. The symbols will be added to your watchlist
