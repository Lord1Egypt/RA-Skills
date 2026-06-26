# LEAN Data Download — Expanding the Universe

## Current State

After initial setup, you'll have ~160 symbols in `$LEAN_ROOT/Data/equity/usa/daily/`.
For pattern-scanning strategies, you may need 500+ liquid US equities.

## Method 1: QuantConnect Data Library (Recommended)

QuantConnect provides free data for backtesting via their API.

```bash
# Install lean CLI
pip install lean

# Login (requires free QuantConnect account)
lean login

# Download specific symbols
lean data download --dataset "US Equity Security Master"
lean data download --dataset "US Equities" --resolution daily --start 20200101
```

## Method 2: LEAN ToolBox — Coarse Universe Generator

LEAN includes a ToolBox for generating coarse universe files from existing data:

```bash
export PATH="$PATH:$DOTNET_ROOT"
cd "$LEAN_ROOT"
dotnet run --project ToolBox -- --app=CoarseUniverseGenerator \
  --source-dir=Data/equity/usa/daily \
  --destination-dir=Data/equity/usa/fundamental/coarse
```

## Method 3: Manual Data Preparation

For custom data sources (yfinance, Alpha Vantage, etc.):

### Data Format (Daily)

File: `$LEAN_ROOT/Data/equity/usa/daily/{ticker}.zip` containing `{ticker}.csv`

CSV format (no header):
```
YYYYMMDD HH:MM,Open,High,Low,Close,Volume
```

**Important:** Prices are scaled by 10000 (integer format).
- Real price $150.25 → stored as 1502500
- Real price $3.50 → stored as 35000

### Conversion Script

```python
#!/usr/bin/env python3
"""Convert yfinance data to LEAN format."""
import yfinance as yf
import zipfile
import io

def download_to_lean(ticker, start="2020-01-01", end="2026-03-01"):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    
    lines = []
    for date, row in df.iterrows():
        date_str = date.strftime("%Y%m%d 00:00")
        o = int(row["Open"] * 10000)
        h = int(row["High"] * 10000)
        l = int(row["Low"] * 10000)
        c = int(row["Close"] * 10000)
        v = int(row["Volume"])
        lines.append(f"{date_str},{o},{h},{l},{c},{v}")
    
    csv_content = "\n".join(lines)
    zip_path = f"Data/equity/usa/daily/{ticker.lower()}.zip"
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{ticker.lower()}.csv", csv_content)
    
    print(f"Wrote {len(lines)} bars to {zip_path}")
```

### Map Files

For proper symbol resolution, LEAN needs map files at:
`$LEAN_ROOT/Data/equity/usa/map_files/{ticker}.csv`

Format:
```
YYYYMMDD,ticker,market,security_type
20200101,AAPL,usa,Equity
```

For simple backtests without delistings/splits, a single-row map file works.

## Method 4: Batch Download Script

Use the included `download_us_universe.py` script:

1. Gets S&P 500 constituent list (~160 symbols)
2. Downloads daily OHLCV via yfinance
3. Converts to LEAN format
4. Generates map files

Usage:
```bash
pip install yfinance pandas
python3 download_us_universe.py --symbols sp500 --start 2020-01-01 --data-dir "$LEAN_ROOT/Data"
```
