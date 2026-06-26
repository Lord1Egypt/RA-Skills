# Futures — REST API

Assumes `client` is initialized. See SKILL.md.

Futures symbols use exchange-standard formats:
- CME: `ES1!` (S&P 500 front-month), `NQ1!` (Nasdaq front-month), `CL1!` (Crude Oil)
- CBOT: `ZB1!` (30-Year T-Bond), `ZC1!` (Corn)
- NYMEX: `GC1!` (Gold), `SI1!` (Silver)

`!` suffix = continuous/front-month contract. Specific expiries use month codes
(e.g. `ESH25` = March 2025 S&P 500 contract).

---

## Futures Trades

Returns individual trade records for a futures contract.

```python
resp = client.futures.trades(
    ticker="ES1!",
    from_="2024-01-01",
    to="2024-01-31",
    limit=1000,
    order="desc",
)
trades = resp["results"]
# Each trade: price, size, exchange, timestamp (Unix ns)
```

---

## Futures Quotes

Returns bid/ask quotes for a futures contract.

```python
resp = client.futures.quotes(
    ticker="ES1!",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
)
quotes = resp["results"]
# Each quote: bid_price, ask_price, bid_size, ask_size, timestamp
```

---

## Futures OHLCV Aggregates

Returns OHLCV bars for a futures contract.

```python
resp = client.futures.aggregates(
    ticker="ES1!",
    multiplier=1,
    timespan="minute",   # "minute", "hour", "day", "week", "month"
    from_="2024-01-01",
    to="2024-01-31",
    sort="asc",
    limit=50000,
)
bars = resp["results"]
# Each bar: o, h, l, c, v, vw (VWAP), t (timestamp ms), n (transactions)
```

---

## Futures Snapshot

Returns the latest quote, trade, and day bar for a futures contract.

```python
resp = client.futures.snapshot(ticker="ES1!")
snapshot = resp["results"]
# Fields: day (OHLCV), lastQuote, lastTrade, prevDay, todaysChange, todaysChangePerc
```

---

## Futures Contract Details

Returns contract specifications including expiry, exchange, tick size, and multiplier.

```python
resp = client.futures.details(ticker="ES1!")
details = resp["results"]
# Fields: ticker, name, expiration_date, exchange, multiplier, tick_size,
#   currency, asset_class
```

---

## Common Futures Symbols for Reference

| Symbol | Contract |
|---|---|
| `ES1!` | S&P 500 E-mini (CME) |
| `NQ1!` | Nasdaq 100 E-mini (CME) |
| `RTY1!` | Russell 2000 E-mini (CME) |
| `YM1!` | Dow Jones E-mini (CBOT) |
| `CL1!` | Crude Oil WTI (NYMEX) |
| `GC1!` | Gold (COMEX) |
| `SI1!` | Silver (COMEX) |
| `ZB1!` | 30-Year T-Bond (CBOT) |
| `ZN1!` | 10-Year T-Note (CBOT) |
| `6E1!` | Euro FX (CME) |
