# Crypto — REST API

Assumes `client` is initialized. See SKILL.md.

Crypto symbols use a `X:` prefix followed by the pair:
- `X:BTCUSD` — Bitcoin / US Dollar
- `X:ETHUSD` — Ethereum / US Dollar
- `X:SOLUSD` — Solana / US Dollar

---

## Crypto Trades

Returns individual trade records for a crypto pair.

```python
resp = client.crypto.trades(
    ticker="X:BTCUSD",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
    order="desc",
)
trades = resp["results"]
# Each trade: price, size, exchange, conditions, timestamp (Unix ns)
```

---

## Crypto Quotes

Returns bid/ask quotes for a crypto pair.

```python
resp = client.crypto.quotes(
    ticker="X:BTCUSD",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
)
quotes = resp["results"]
# Each quote: bid_price, ask_price, bid_size, ask_size, exchange, timestamp
```

---

## Crypto OHLCV Aggregates

Returns OHLCV bars for a crypto pair.

```python
resp = client.crypto.aggregates(
    ticker="X:BTCUSD",
    multiplier=1,
    timespan="minute",   # "minute", "hour", "day", "week", "month"
    from_="2024-01-01",
    to="2024-01-31",
    adjusted=False,      # no adjustment needed for crypto
    sort="asc",
    limit=50000,
)
bars = resp["results"]
# Each bar: o, h, l, c, v, vw (VWAP), t (timestamp ms), n (transactions)
```

---

## Crypto Snapshot

Returns the latest trade, day bar, and summary for a pair or list of pairs.

```python
# Single pair
resp = client.crypto.snapshot(ticker="X:BTCUSD")

# Multiple pairs
resp = client.crypto.snapshots(tickers=["X:BTCUSD", "X:ETHUSD", "X:SOLUSD"])
snapshot = resp["results"]
# Fields: day (OHLCV), lastTrade, prevDay, todaysChange, todaysChangePerc
```

---

## Crypto Pair Details

Returns metadata about a trading pair including the base and quote currency.

```python
resp = client.crypto.details(ticker="X:BTCUSD")
details = resp["results"]
# Fields: base_currency_name, base_currency_symbol,
#   currency_name, currency_symbol (quote), market
```

---

## Notes

- Crypto trades 24/7 — no market hours restrictions
- Prices are aggregated across multiple exchanges (Coinbase, Binance, Kraken, etc.)
- For real-time crypto streaming, see `references/websocket.md`
- Crypto is not available in Flat Files on all plans — check your subscription
