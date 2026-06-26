# Options — REST API

Assumes `client` is initialized. See SKILL.md.

Options symbols follow OCC format: `O:AAPL261218C00240000`
= `O:` prefix + underlying + expiry (YYMMDD) + type (C/P) + strike * 1000 (8 digits)

---

## Options Chain

Returns all option contracts for an underlying ticker, with filtering.

```python
resp = client.options.chain(
    underlying_ticker="AAPL",
    expiration_date="2026-12-18",       # optional filter by expiry
    expiration_date_gte="2026-01-01",   # optional range filter
    expiration_date_lte="2026-12-31",
    contract_type="call",               # "call" or "put"
    strike_price_gte=200,               # optional strike range
    strike_price_lte=300,
    limit=250,
    order="asc",
    sort="strike_price",
)
contracts = resp["results"]
# Each contract: ticker (OCC symbol), underlying_ticker, expiration_date,
#   strike_price, contract_type, shares_per_contract, primary_exchange,
#   exercise_style ("american" or "european")
```

---

## Options Quotes

Returns bid/ask quotes for a specific option contract.

```python
resp = client.options.quotes(
    option_ticker="O:AAPL261218C00240000",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
)
quotes = resp["results"]
# Each quote: bid_price, ask_price, bid_size, ask_size, bid_exchange, ask_exchange, timestamp
```

---

## Options Trades

Returns individual trade records for a specific option contract.

```python
resp = client.options.trades(
    option_ticker="O:AAPL261218C00240000",
    from_="2024-01-01",
    to="2024-01-02",
    limit=1000,
)
trades = resp["results"]
# Each trade: price, size, exchange, conditions, timestamp
```

---

## Options OHLCV Aggregates

Returns OHLCV bars for a specific option contract.

```python
resp = client.options.aggregates(
    option_ticker="O:AAPL261218C00240000",
    multiplier=1,
    timespan="day",   # "minute", "hour", "day"
    from_="2024-01-01",
    to="2024-12-31",
    adjusted=True,
    sort="asc",
    limit=5000,
)
bars = resp["results"]
# Each bar: o, h, l, c, v, vw (VWAP), t (timestamp ms), n (transactions)
```

---

## Options Snapshot (Latest Data + Greeks)

Returns the latest quote, trade, day bar, and Greeks for a contract or full chain.

```python
# Single contract
resp = client.options.snapshot(option_ticker="O:AAPL261218C00240000")
snapshot = resp["results"]
# Includes: day (OHLCV), lastQuote, lastTrade, details (contract info),
#   greeks (delta, gamma, theta, vega), implied_volatility, open_interest

# Full chain snapshot for underlying
resp = client.options.chain_snapshot(underlying_ticker="AAPL")
chain = resp["results"]  # list of snapshots for all contracts
```

### Greeks fields
| Field | Description |
|---|---|
| `delta` | Rate of change of option price vs underlying price |
| `gamma` | Rate of change of delta |
| `theta` | Time decay per day |
| `vega` | Sensitivity to implied volatility |
| `implied_volatility` | IV as a decimal (e.g. 0.30 = 30%) |
| `open_interest` | Number of open contracts |

---

## Options Contract Details

Returns static details for a specific option contract.

```python
resp = client.options.details(option_ticker="O:AAPL261218C00240000")
details = resp["results"]
# Fields: ticker, underlying_ticker, expiration_date, strike_price,
#   contract_type, exercise_style, shares_per_contract, primary_exchange
```
