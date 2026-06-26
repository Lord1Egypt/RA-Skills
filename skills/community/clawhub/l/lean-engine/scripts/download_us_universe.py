#!/usr/bin/env python3
"""
download_us_universe.py
Download US equity daily data and convert to LEAN format.

Usage:
  python3 download_us_universe.py --symbols sp500 --start 2020-01-01
  python3 download_us_universe.py --symbols AAPL,MSFT,GOOGL --start 2023-01-01
  python3 download_us_universe.py --symbols sp500 --start 2020-01-01 --data-dir /path/to/lean/Data

Requires: pip install yfinance pandas

If --data-dir is not specified, uses $LEAN_ROOT/Data (env var).
"""

import argparse
import os
import zipfile
import sys
from datetime import datetime

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Missing dependencies. Install with: pip install yfinance pandas")
    sys.exit(1)


# S&P 500 — top ~100 by market cap (expand as needed)
SP500_TOP = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "BRK-B", "TSLA", "UNH", "LLY",
    "JPM", "V", "XOM", "JNJ", "PG", "MA", "AVGO", "HD", "MRK", "COST",
    "ABBV", "CVX", "PEP", "KO", "ADBE", "CRM", "WMT", "MCD", "BAC", "CSCO",
    "ACN", "TMO", "ABT", "NFLX", "LIN", "AMD", "DHR", "ORCL", "CMCSA", "TXN",
    "PM", "DIS", "VZ", "NEE", "WFC", "INTC", "RTX", "BMY", "UPS", "QCOM",
    "HON", "COP", "AMGN", "SPGI", "LOW", "IBM", "GE", "CAT", "BA", "INTU",
    "DE", "MDLZ", "ISRG", "PLD", "SYK", "GILD", "BKNG", "AXP", "GS", "AMAT",
    "BLK", "ADI", "VRTX", "TJX", "REGN", "MMC", "LMT", "SBUX", "CVS", "SCHW",
    "EOG", "NOW", "MO", "SO", "CI", "PGR", "CB", "ZTS", "BDX", "CME",
    "DUK", "SLB", "CL", "NOC", "FI", "ICE", "ITW", "SHW", "MCK", "APD",
    # Additional liquid names
    "PANW", "CRWD", "SNOW", "DDOG", "ZS", "NET", "PLTR", "COIN", "MARA", "RIOT",
    "SQ", "SHOP", "ROKU", "SNAP", "PINS", "UBER", "LYFT", "DASH", "ABNB", "RBLX",
    "SOFI", "HOOD", "RIVN", "LCID", "NIO", "XPEV", "LI", "F", "GM", "TM",
    "MRVL", "MU", "LRCX", "KLAC", "SNPS", "CDNS", "ASML", "TSM", "ON", "SWKS",
    "ENPH", "SEDG", "FSLR", "RUN", "PLUG", "CHPT", "BLNK", "QS", "STEM", "BE",
]

# ETFs for benchmarking
ETFS = ["SPY", "QQQ", "IWM", "DIA", "XLF", "XLK", "XLE", "XLV", "XLI", "XLY"]


def get_default_data_dir():
    """Get default data directory from LEAN_ROOT env var."""
    lean_root = os.environ.get("LEAN_ROOT")
    if lean_root:
        return os.path.join(lean_root, "Data")
    return None


def get_symbols(mode: str) -> list:
    """Get symbol list based on mode."""
    if mode == "sp500":
        return SP500_TOP + ETFS
    elif mode == "etfs":
        return ETFS
    else:
        return [s.strip().upper() for s in mode.split(",")]


def to_lean_csv(df: pd.DataFrame, ticker: str) -> str:
    """Convert yfinance DataFrame to LEAN daily CSV format."""
    # yfinance returns MultiIndex columns: (Price, Ticker) — flatten
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel("Ticker", axis=1)

    lines = []
    for date, row in df.iterrows():
        date_str = date.strftime("%Y%m%d 00:00")
        o = int(round(float(row["Open"]) * 10000))
        h = int(round(float(row["High"]) * 10000))
        l = int(round(float(row["Low"]) * 10000))
        c = int(round(float(row["Close"]) * 10000))
        v = int(float(row["Volume"]))
        if v > 0 and c > 0:
            lines.append(f"{date_str},{o},{h},{l},{c},{v}")
    return "\n".join(lines)


def write_lean_zip(ticker: str, csv_content: str, data_dir: str):
    """Write LEAN-format zip file."""
    daily_dir = os.path.join(data_dir, "equity", "usa", "daily")
    os.makedirs(daily_dir, exist_ok=True)

    clean_ticker = ticker.lower().replace("-", "")
    zip_path = os.path.join(daily_dir, f"{clean_ticker}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{clean_ticker}.csv", csv_content)

    return zip_path


def write_map_file(ticker: str, start_date: str, data_dir: str):
    """Write minimal map file for symbol resolution."""
    map_dir = os.path.join(data_dir, "equity", "usa", "map_files")
    os.makedirs(map_dir, exist_ok=True)

    clean_ticker = ticker.lower().replace("-", "")
    map_path = os.path.join(map_dir, f"{clean_ticker}.csv")

    date_str = start_date.replace("-", "")
    with open(map_path, "w") as f:
        f.write(f"{date_str},{clean_ticker},usa,Equity\n")
        f.write(f"20500101,{clean_ticker},usa,Equity\n")  # far future end date

    return map_path


def main():
    default_data_dir = get_default_data_dir()

    ap = argparse.ArgumentParser(description="Download US equity data for LEAN")
    ap.add_argument("--symbols", default="sp500",
                    help="'sp500', 'etfs', or comma-separated tickers")
    ap.add_argument("--start", default="2020-01-01", help="Start date YYYY-MM-DD")
    ap.add_argument("--end", default=None, help="End date YYYY-MM-DD (default: today)")
    ap.add_argument("--data-dir", default=default_data_dir,
                    help="LEAN Data directory (default: $LEAN_ROOT/Data)")
    ap.add_argument("--batch-size", type=int, default=20,
                    help="Download batch size")
    args = ap.parse_args()

    if not args.data_dir:
        print("Error: --data-dir not specified and LEAN_ROOT env var not set.")
        print("Set LEAN_ROOT or pass --data-dir explicitly.")
        sys.exit(1)

    symbols = get_symbols(args.symbols)
    end = args.end or datetime.now().strftime("%Y-%m-%d")

    print(f"Downloading {len(symbols)} symbols: {args.start} to {end}")
    print(f"Output: {args.data_dir}/equity/usa/daily/")

    success = 0
    failed = []

    for i in range(0, len(symbols), args.batch_size):
        batch = symbols[i:i + args.batch_size]
        print(f"\nBatch {i // args.batch_size + 1}: {', '.join(batch)}")

        for ticker in batch:
            try:
                df = yf.download(ticker, start=args.start, end=end,
                                 auto_adjust=True, progress=False)
                if df.empty or len(df) < 10:
                    print(f"  SKIP {ticker} (insufficient data)")
                    failed.append(ticker)
                    continue

                csv_content = to_lean_csv(df, ticker)
                zip_path = write_lean_zip(ticker, csv_content, args.data_dir)
                write_map_file(ticker, args.start, args.data_dir)

                print(f"  OK   {ticker} ({len(df)} bars) → {os.path.basename(zip_path)}")
                success += 1

            except Exception as e:
                print(f"  FAIL {ticker}: {e}")
                failed.append(ticker)

    print(f"\n{'='*50}")
    print(f"Done: {success}/{len(symbols)} symbols downloaded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"Data at: {args.data_dir}/equity/usa/daily/")


if __name__ == "__main__":
    main()
