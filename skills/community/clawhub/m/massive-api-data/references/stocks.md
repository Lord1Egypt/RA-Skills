# Stocks — REST API

Assumes `client` is initialized and `MASSIVE_API_KEY` is set. See SKILL.md.

All endpoints support common query parameters:
- `ticker` — stock symbol (e.g. `AAPL`, `MSFT`)
- `from` / `to` — date range in ISO format (`YYYY-MM-DD`)
- `limit` — max results per page (default varies by endpoint)
- `order` — `asc` or `desc`

---

## Trades

Returns individual trade records (price, size, exchange, timestamp).

```python
resp = client.stocks.trades(
    ticker="AAPL",
    from_="2024-01-01",
    to="2024-01-31",
    limit=1000,
    order="desc",
)
trades = resp["results"]
# Each trade: price, size, exchange, conditions, timestamp (Unix ns)
```

---

## Quotes (NBBO)

Returns National Best Bid and Offer quotes.

```python
resp = client.stocks.quotes(
    ticker="AAPL",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
)
quotes = resp["results"]
# Each quote: bid_price, ask_price, bid_size, ask_size, exchange, timestamp
```

---

## OHLCV Aggregates (Minute Bars)

Returns open/high/low/close/volume bars for a given timeframe.

```python
# Minute bars
resp = client.stocks.aggregates(
    ticker="AAPL",
    multiplier=1,
    timespan="minute",   # "minute", "hour", "day", "week", "month", "quarter", "year"
    from_="2024-01-01",
    to="2024-01-31",
    adjusted=True,       # adjust for splits/dividends
    sort="asc",
    limit=50000,
)
bars = resp["results"]
# Each bar: o, h, l, c, v, vw (VWAP), t (timestamp ms), n (transactions)
```

---

## Snapshot (Latest Quote + Trade)

Returns the most recent quote, trade, and day aggregate for a ticker or list of tickers.

```python
# Single ticker
resp = client.stocks.snapshot(ticker="AAPL")

# Multiple tickers
resp = client.stocks.snapshots(tickers=["AAPL", "MSFT", "TSLA"])
snapshot = resp["results"]
# Each snapshot: day (OHLCV), lastQuote, lastTrade, prevDay, todaysChange, todaysChangePerc
```

---

## Dividends

Returns dividend records for a ticker.

```python
resp = client.stocks.dividends(
    ticker="AAPL",
    from_="2023-01-01",
    to="2024-01-01",
)
dividends = resp["results"]
# Each dividend: cash_amount, declaration_date, ex_dividend_date, pay_date, record_date, frequency
```

---

## Stock Splits

```python
resp = client.stocks.splits(ticker="AAPL")
splits = resp["results"]
# Each split: execution_date, split_from, split_to
```

---

## Ticker Details (Fundamentals)

Returns company info, market cap, share count, SIC code, description, and more.

```python
resp = client.stocks.ticker_details(ticker="AAPL")
details = resp["results"]
# Fields: name, market_cap, share_class_shares_outstanding, sic_description,
#   description, homepage_url, list_date, primary_exchange
```

---

## Ticker Search

Search for tickers by keyword.

```python
resp = client.stocks.tickers(
    search="apple",
    market="stocks",   # "stocks", "crypto", "fx", "indices"
    active=True,
    limit=10,
)
tickers = resp["results"]
# Each ticker: ticker, name, market, primary_exchange, currency_name, active
```
