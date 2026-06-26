# TradingView API Examples

This directory contains real API request/response examples from TradingView Data API via RapidAPI. These examples serve as reference data for quantitative analysis.

## Files Overview

| File | Description | Size |
|------|-------------|------|
| 01-price-data.txt | OHLCV candlestick data examples | 26K |
| 02-quote-data.txt | Real-time quote data examples | 8K |
| 03-market-search.txt | Market search results examples | 2.8K |
| 04-technical-analysis.txt | Technical analysis indicators examples | 4.2K |
| 05-leaderboards.txt | Market leaderboard examples (stocks, crypto, etc.) | 5.9K |
| 06-news.txt | Financial news examples | 9.6K |
| 07-metadata.txt | API metadata examples (markets, tabs, columnsets) | 3.6K |
| 08-calendar.txt | Calendar events examples (earnings, economic, IPO) | 8K |
| 09-logo.txt | Logo image URL examples | 239B |

## Usage

These examples demonstrate:
- Request format (curl commands with headers and parameters)
- Response structure (JSON format)
- Available data fields
- Parameter options

## Data Format

Each file contains:
```
curl --request GET \
  --url 'https://tradingview-data1.p.rapidapi.com/api/...' \
  --header 'x-rapidapi-host: ...' \
  --header 'x-rapidapi-key: ...'

{
  "success": true,
  "data": { ... }
}
```

## Note

These are example responses for reference. For real-time data access, visit:
- RapidAPI: https://rapidapi.com/hypier/api/tradingview-data1
