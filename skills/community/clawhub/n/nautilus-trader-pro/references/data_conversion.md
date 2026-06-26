# Data Conversion Guide

This guide explains how to convert external data sources into formats that NautilusTrader can use
for backtesting and live trading.

## Conversion pipeline overview

```
Raw data (CSV, API, database)
    ↓
DataLoader → pd.DataFrame (with specific column schema)
    ↓
DataWrangler → list[NautilusObject]  (QuoteTick, TradeTick, Bar, etc.)
    ↓
Option A: Add directly to BacktestEngine  →  engine.add_data(data)
Option B: Write to ParquetDataCatalog     →  catalog.write_data(data)
```

## Available data wranglers

Each wrangler expects a specific DataFrame schema. All wranglers are in
`nautilus_trader.persistence.wranglers`.

### QuoteTickDataWrangler

Converts bid/ask quote data. DataFrame must have a **DatetimeIndex** (UTC) and these columns:

| Column | Type | Description |
|---|---|---|
| `bid_price` | float | Best bid price |
| `ask_price` | float | Best ask price |
| `bid_size` | float | Best bid size (optional, defaults to 0) |
| `ask_size` | float | Best ask size (optional, defaults to 0) |

```python
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler

wrangler = QuoteTickDataWrangler(instrument=instrument)
ticks = wrangler.process(df)  # Returns list[QuoteTick]
```

### TradeTickDataWrangler

Converts trade/execution data. DataFrame must have a **DatetimeIndex** (UTC) and these columns:

| Column | Type | Description |
|---|---|---|
| `price` | float | Trade price |
| `quantity` | float | Trade size |
| `aggressor_side` | str | "BUY" or "SELL" (trade initiator) |
| `trade_id` | str | Unique trade identifier |

```python
from nautilus_trader.persistence.wranglers import TradeTickDataWrangler

wrangler = TradeTickDataWrangler(instrument=instrument)
ticks = wrangler.process(df)  # Returns list[TradeTick]
```

### BarDataWrangler

Converts OHLCV bar/candle data. DataFrame must have a **DatetimeIndex** (UTC) and these columns:

| Column | Type | Description |
|---|---|---|
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | float | Traded volume (optional, defaults to 0) |

```python
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.model.data import BarType

bar_type = BarType.from_str("EUR/USD.SIM-1-MINUTE-LAST-EXTERNAL")
wrangler = BarDataWrangler(bar_type=bar_type, instrument=instrument)
bars = wrangler.process(df)  # Returns list[Bar]
```

### OrderBookDeltaDataWrangler

Converts order book update data. DataFrame must have specific columns — see
`docs/concepts/data.md` in the repository for the full schema.

```python
from nautilus_trader.persistence.wranglers import OrderBookDeltaDataWrangler

wrangler = OrderBookDeltaDataWrangler(instrument=instrument)
deltas = wrangler.process(df)  # Returns list[OrderBookDelta]
```

## Creating instruments

Before wrangling data, you need an instrument definition. You can create instruments in two ways:

### Using TestInstrumentProvider (for common instruments)

```python
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue

SIM = Venue("SIM")

# Forex
EURUSD = TestInstrumentProvider.default_fx_ccy("EUR/USD", SIM)
AUDUSD = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

# Crypto
BTCUSDT = TestInstrumentProvider.btcusdt_binance()
ETHUSDT = TestInstrumentProvider.ethusdt_binance()

# Equity
AAPL = TestInstrumentProvider.aapl_equity()
```

### Creating instruments manually

For instruments not in the test provider, create them manually:

```python
from nautilus_trader.model.instruments import CurrencyPair, Equity, CryptoPerpetual
from nautilus_trader.model.identifiers import InstrumentId, Symbol, Venue
from nautilus_trader.model.objects import Price, Quantity, Money, Currency
from nautilus_trader.model.currencies import USD, CNY

# Example: Custom equity
instrument = Equity(
    instrument_id=InstrumentId(Symbol("CUSTOM"), Venue("SIM")),
    raw_symbol=Symbol("CUSTOM"),
    currency=USD,
    price_precision=2,
    price_increment=Price.from_str("0.01"),
    lot_size=Quantity.from_int(1),
    ts_event=0,
    ts_init=0,
)
```

For exchange-specific instruments (crypto, futures), see `docs/concepts/instruments.md`.

## Complete example: CSV bar data to backtest

```python
import pandas as pd
from pathlib import Path
from nautilus_trader.model.data import BarType
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue

# 1. Load raw CSV
df = pd.read_csv("my_data.csv")

# 2. Ensure proper datetime index (UTC)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.set_index("timestamp")

# 3. Rename columns to match schema
df = df.rename(columns={
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
})

# 4. Create instrument
SIM = Venue("SIM")
instrument = TestInstrumentProvider.default_fx_ccy("EUR/USD", SIM)

# 5. Create bar type and wrangle
bar_type = BarType.from_str("EUR/USD.SIM-1-MINUTE-LAST-EXTERNAL")
wrangler = BarDataWrangler(bar_type=bar_type, instrument=instrument)
bars = wrangler.process(df)

# 6. Now use bars:
#    - Add to BacktestEngine: engine.add_data(bars)
#    - Or write to catalog: catalog.write_data(bars)
```

## Complete example: CSV tick data to backtest

```python
import pandas as pd
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue

# 1. Load and prepare DataFrame
df = pd.read_csv("tick_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.set_index("timestamp")

# Ensure columns: bid_price, ask_price, bid_size, ask_size
df = df.rename(columns={
    "Bid": "bid_price",
    "Ask": "ask_price",
    "BidSize": "bid_size",
    "AskSize": "ask_size",
})

# 2. Create instrument and wrangle
SIM = Venue("SIM")
instrument = TestInstrumentProvider.default_fx_ccy("EUR/USD", SIM)
wrangler = QuoteTickDataWrangler(instrument=instrument)
ticks = wrangler.process(df)

# 3. Use: engine.add_data(ticks)
```

## Using the ParquetDataCatalog

The data catalog persists Nautilus data in Parquet format for efficient reuse:

```python
from pathlib import Path
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.model import QuoteTick

# Write data to catalog
catalog = ParquetDataCatalog(Path("./catalog"))
catalog.write_data([instrument])  # Write instrument first
catalog.write_data(ticks)          # Then write data

# Read data back
instruments = catalog.instruments()
ticks = catalog.quote_ticks(instrument_ids=["EUR/USD.SIM"])
bars = catalog.bars(bar_types=["EUR/USD.SIM-1-MINUTE-LAST-EXTERNAL"])
```

The catalog is required when using the high-level `BacktestNode` API (see backtesting guide).

## Crypto exchange data (Binance example)

Binance provides specific loaders for its data formats:

```python
from nautilus_trader.adapters.binance.loaders import BinanceOrderBookDeltaDataLoader
from nautilus_trader.persistence.wranglers import OrderBookDeltaDataWrangler
from nautilus_trader.test_kit.providers import TestInstrumentProvider

# Load raw Binance CSV
df = BinanceOrderBookDeltaDataLoader.load("btcusdt-depth-snap.csv")

# Wrangle
instrument = TestInstrumentProvider.btcusdt_binance()
wrangler = OrderBookDeltaDataWrangler(instrument)
deltas = wrangler.process(df)
```

## Traditional finance data (Databento example)

For US equities/futures data via Databento:

```python
# See docs/how_to/data_catalog_databento.py for the complete workflow
# Key steps:
# 1. Download DBN data via Databento API
# 2. Use DatabentoDataLoader to parse into Nautilus objects
# 3. Write to ParquetDataCatalog
```

See `docs/how_to/data_catalog_databento.py` and `docs/integrations/databento.md` for details.

## Key tips

- **DateTime index must be UTC** — always set `utc=True` when parsing timestamps
- **Column names are case-sensitive** — use lowercase: `open`, `high`, `low`, `close`, `volume`
- **For EXTERNAL bars** — use the `EXTERNAL` aggregation source, meaning the data provider
  already aggregated the bars (most common for downloaded historical data)
- **For INTERNAL bars** — Nautilus will aggregate bars from ticks at runtime
- **Instrument precision matters** — the instrument defines how many decimal places prices
  and quantities can have. Mismatched precision will cause errors
- **Refer to `examples/data_conversion/`** in the repository for real-world conversion examples
  including Chinese futures (IF) data from CSV and ZIP files
