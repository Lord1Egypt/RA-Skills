# Data Sources Reference

How to fetch stock data and news. Primary source is Google Finance; fallback sources listed for each data type.

---

## Google Finance URL Patterns

### Single Stock Quote Page
```
https://www.google.com/finance/quote/{SYMBOL}:{EXCHANGE}
```

Examples:
| Stock | URL |
|-------|-----|
| Apple (US) | `https://www.google.com/finance/quote/AAPL:NASDAQ` |
| Tesla (US) | `https://www.google.com/finance/quote/TSLA:NASDAQ` |
| NVIDIA | `https://www.google.com/finance/quote/NVDA:NASDAQ` |
| Microsoft | `https://www.google.com/finance/quote/MSFT:NASDAQ` |
| Tencent (HK) | `https://www.google.com/finance/quote/0700:HKG` |
| Toyota (JP) | `https://www.google.com/finance/quote/7203:TYO` |
| LVMH (EU) | `https://www.google.com/finance/quote/MC:EPA` |
| Alibaba (HK) | `https://www.google.com/finance/quote/9988:HKG` |
| Alibaba (US ADR) | `https://www.google.com/finance/quote/BABA:NYSE` |

### Exchange Suffix Mapping

| Market | Suffix | Example |
|--------|--------|---------|
| NASDAQ | `NASDAQ` | `AAPL:NASDAQ` |
| NYSE | `NYSE` | `JPM:NYSE` |
| Hong Kong | `HKG` | `0700:HKG` |
| Tokyo | `TYO` | `7203:TYO` |
| London | `LON` | `BP:LON` |
| Paris | `EPA` | `MC:EPA` |
| Frankfurt | `FRA` | `SAP:FRA` |
| Shanghai | `SHA` | `600519:SHA` |
| Shenzhen | `SHE` | `000001:SHE` |
| Korea | `KRX` | `005930:KRX` |
| Toronto | `TSE` | `SHOP:TSE` |
| Australia | `ASX` | `BHP:ASX` |

If the exchange is unknown, try `NYSE` first, then `NASDAQ`.

---

## Extracting Data from Google Finance Page

### Browser Automation Steps

1. Navigate to the quote URL (see above).
2. Wait for the price element to appear (selector: `.YMlKec.fxKbKc` or `[data-last-price]`).
3. Extract the following:

```
Price:         document.querySelector('.YMlKec.fxKbKc')?.innerText
Change %:      document.querySelector('.JwB6zf')?.innerText
               (or the second `.NydbP` span)
Company name:  document.querySelector('.zzDege')?.innerText
```

4. For the stats table (Open, High, Low, Market Cap, P/E, 52-week range):
   - Find all `.gyFHrc` rows
   - Each row has `.mfs7Fc` (label) and `.P6K39c` (value)
   - Build a key-value map from label text → value text

5. For news headlines:
   - Find `.Yfwt5` or `.AoCdqe` elements in the news section
   - Each contains: `.Yfwt5` (title), `.sfyJob` (source + time)

### Parsing Volume

The volume field on Google Finance is formatted as "62.3M" or "1.2B". Parse to a number:
```python
def parse_volume(s):
    s = s.replace(',', '').strip()
    if s.endswith('B'): return float(s[:-1]) * 1_000_000_000
    if s.endswith('M'): return float(s[:-1]) * 1_000_000
    if s.endswith('K'): return float(s[:-1]) * 1_000
    return float(s)
```

Use `{baseDir}/scripts/parse-stock.py` for a complete parser.

---

## Fallback: Yahoo Finance

If Google Finance is rate-limiting or blocking:

```
https://finance.yahoo.com/quote/{SYMBOL}/
```

Yahoo Finance note: Use the `^` prefix for index symbols (e.g., `^GSPC` = S&P 500).

For programmatic fallback, use the Yahoo Finance unofficial API:
```
https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=1d&range=1d
```
Returns JSON with `regularMarketPrice`, `regularMarketChangePercent`, `regularMarketVolume`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`.

Parse with `python3 -c "import sys,json; d=json.load(sys.stdin)['chart']['result'][0]; print(d['meta']['regularMarketPrice'])"`.

---

## Fallback: Stooq (international data)

For international stocks where Yahoo/Google fail:
```
https://stooq.com/q/l/?s={SYMBOL}&f=sd2t2ohlcvn&e=csv
```
Returns CSV: `Symbol,Date,Time,Open,High,Low,Close,Volume,Name`

---

## News Sources

### Google News Search (primary)
```
https://www.google.com/search?q={COMPANY_NAME}+stock&tbm=nws&tbs=qdr:d
```
Replace `{COMPANY_NAME}` with URL-encoded company name (e.g., `Apple+Inc`).

Add `&num=10` for 10 results. Extract `.WlydOe a` for headline titles and `.CEMjEf` for source/time.

### RSS Feeds (fallback)
Common financial RSS feeds for news aggregation:

| Source | RSS URL template |
|--------|-----------------|
| Reuters | `https://feeds.reuters.com/reuters/businessNews` |
| Bloomberg | `https://feeds.bloomberg.com/markets/news.rss` |
| Yahoo Finance | `https://finance.yahoo.com/rss/headline?s={SYMBOL}` |
| Seeking Alpha | `https://seekingalpha.com/symbol/{SYMBOL}.xml` |

Use `curl -s "{url}" | python3 -c "import sys; from xml.etree import ElementTree as ET; root=ET.parse(sys.stdin).getroot(); [print(i.findtext('title'), '|', i.findtext('pubDate')) for i in root.findall('.//item')[:5]]"`

---

## Market Hours by Exchange

| Exchange | Local hours | UTC |
|----------|-------------|-----|
| NYSE/NASDAQ | 09:30–16:00 ET | 14:30–21:00 UTC (EDT) / 15:30–22:00 UTC (EST) |
| Hong Kong (HKG) | 09:30–16:00 HKT | 01:30–08:00 UTC |
| Tokyo (TYO) | 09:00–15:30 JST | 00:00–06:30 UTC |
| London (LON) | 08:00–16:30 GMT | 08:00–16:30 UTC |
| Paris (EPA) | 09:00–17:30 CET | 08:00–16:30 UTC |
| Shanghai (SHA) | 09:30–15:00 CST | 01:30–07:00 UTC |

**Pre/after-market note:** Google Finance shows after-hours prices for US stocks. The change % shown is vs. prior regular close. Include a note like "(after-hours)" when checking outside market hours.

---

## State File Location

Watchlist and snapshot state is stored at:
```
~/.openclaw/workspace/stock-tracker-state.json
```

If the file does not exist, create it with:
```json
{
  "watchlist": [],
  "lastChecked": null,
  "snapshots": {}
}
```

Read/write this file using the `computer-use` or `bash` tool:
```bash
# Read
python3 -c "import json; print(json.dumps(json.load(open('$HOME/.openclaw/workspace/stock-tracker-state.json')), indent=2))"

# Write (after building updated_state dict in python)
python3 {baseDir}/scripts/parse-stock.py --update-state
```

---

## Data Freshness & Caching

- Google Finance prices: 15-min delayed for most non-US exchanges; real-time for major US exchanges.
- Do NOT re-fetch within 10 minutes of a previous check for the same symbol (avoid rate limits).
- Store `lastChecked` timestamp per symbol in state file. Skip fetch if `now - lastChecked < 600s`.
- For cron jobs running every 4 hours, this is never an issue.
