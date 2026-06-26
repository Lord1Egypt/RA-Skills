# Backtesting Guide

This guide explains how to run backtests and generate performance reports with NautilusTrader.

## Two API levels

| API | Entry point | Best for |
|---|---|---|
| **Low-level** | `BacktestEngine` | Data fits in RAM, want fine control |
| **High-level** | `BacktestNode` + config objects | Streaming large datasets, multiple runs |

## Low-level API: BacktestEngine

### Complete example (bar data)

```python
from decimal import Decimal

import pandas as pd

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.test_kit.providers import TestInstrumentProvider

# -- Your strategy import --
# from my_strategy import MyStrategy, MyStrategyConfig

# 1. Configure engine
engine = BacktestEngine(
    config=BacktestEngineConfig(
        logging=LoggingConfig(log_level="INFO"),
    ),
)

# 2. Add venue
SIM = Venue("SIM")
engine.add_venue(
    venue=SIM,
    oms_type=OmsType.NETTING,       # NETTING (one position per instrument) or HEDGING
    account_type=AccountType.MARGIN, # MARGIN or CASH
    base_currency=USD,
    starting_balances=[Money(1_000_000, USD)],
    default_leverage=Decimal(1),
)

# 3. Add instrument
instrument = TestInstrumentProvider.default_fx_ccy("EUR/USD", SIM)
engine.add_instrument(instrument)

# 4. Add data (bars, ticks, or order book data)
# Assuming you have prepared `bars` via a DataWrangler (see data_conversion.md)
engine.add_data(bars)

# 5. Add strategy
strategy = MyStrategy(
    MyStrategyConfig(
        instrument_id=instrument.id,
        bar_type=BarType.from_str("EUR/USD.SIM-1-MINUTE-LAST-EXTERNAL"),
        trade_size=Decimal(100_000),
    ),
)
engine.add_strategy(strategy)

# 6. Run
engine.run()

# 7. Generate reports (see Reports section below)
print(engine.trader.generate_account_report(SIM))
print(engine.trader.generate_positions_report())
print(engine.trader.generate_order_fills_report())

# 8. Clean up
engine.reset()   # Reset for another run (data + instruments persist)
engine.dispose()  # Final cleanup
```

### Complete example (tick data)

```python
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler
from nautilus_trader.test_kit.providers import TestDataProvider, TestInstrumentProvider

# Load test tick data
provider = TestDataProvider()
instrument = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

wrangler = QuoteTickDataWrangler(instrument=instrument)
ticks = wrangler.process(provider.read_csv_ticks("truefx/audusd-ticks.csv"))

engine.add_instrument(instrument)
engine.add_data(ticks)

# Bars will be aggregated INTERNALLY from ticks
strategy_config = MyStrategyConfig(
    instrument_id=instrument.id,
    bar_type=BarType.from_str("AUD/USD.SIM-100-TICK-MID-INTERNAL"),
    trade_size=Decimal(1_000_000),
)
```

### Performance optimization for large datasets

When loading data for multiple instruments:

```python
# BAD: sorts on each call (gets slower as data grows)
engine.add_data(instrument1_bars)
engine.add_data(instrument2_bars)

# GOOD: defer sorting until the end
engine.add_data(instrument1_bars, sort=False)
engine.add_data(instrument2_bars, sort=False)
engine.sort_data()  # Sort once — much faster
```

## High-level API: BacktestNode

Uses `BacktestNode` with configuration objects and data from a `ParquetDataCatalog`.

```python
from decimal import Decimal
from pathlib import Path

from nautilus_trader.backtest.node import (
    BacktestDataConfig,
    BacktestEngineConfig,
    BacktestNode,
    BacktestRunConfig,
    BacktestVenueConfig,
)
from nautilus_trader.config import ImportableStrategyConfig
from nautilus_trader.model import BarType, QuoteTick
from nautilus_trader.persistence.catalog import ParquetDataCatalog

# 1. Set up catalog (must have data written already — see data_conversion.md)
catalog = ParquetDataCatalog(Path("./catalog"))
instrument = catalog.instruments()[0]

# 2. Configure venues
venue_configs = [
    BacktestVenueConfig(
        name="SIM",
        oms_type="NETTING",
        account_type="MARGIN",
        base_currency="USD",
        starting_balances=["1_000_000 USD"],
    ),
]

# 3. Configure data sources
data_configs = [
    BacktestDataConfig(
        catalog_path=str(catalog.path),
        data_cls=QuoteTick,
        instrument_id=instrument.id,
    ),
]

# 4. Configure strategies (using importable config for serialization)
strategies = [
    ImportableStrategyConfig(
        strategy_path="nautilus_trader.examples.strategies.ema_cross:EMACross",
        config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
        config={
            "instrument_id": instrument.id,
            "bar_type": BarType.from_str(f"{instrument.id}-15-MINUTE-BID-INTERNAL"),
            "fast_ema_period": 10,
            "slow_ema_period": 20,
            "trade_size": Decimal(1_000_000),
        },
    ),
]

# 5. Create run config
config = BacktestRunConfig(
    engine=BacktestEngineConfig(strategies=strategies),
    data=data_configs,
    venues=venue_configs,
)

# 6. Run
node = BacktestNode(configs=[config])
results = node.run()

# results is a list of BacktestResult objects
print(results[0])
```

## Venue configuration

### OMS types

| Type | Behavior | Use for |
|---|---|---|
| `NETTING` | One position per instrument, fills net against each other | Forex, crypto futures |
| `HEDGING` | Separate position per order, allows simultaneous long/short | Some brokers, CFDs |

### Account types

| Type | Description |
|---|---|
| `CASH` | Cannot go negative, no leverage |
| `MARGIN` | Supports leverage and margin requirements |

### Book types (controls execution simulation fidelity)

| Type | Description | Data required |
|---|---|---|
| `L1_MBP` (default) | Top-of-book only | Quotes, trades, or bars |
| `L2_MBP` | Full price-level depth | OrderBookDelta data |
| `L3_MBO` | Individual order tracking | OrderBookDelta data |

### Fill models

Customize order fill simulation:

```python
from nautilus_trader.backtest.models import FillModel

fill_model = FillModel(
    prob_fill_on_limit=0.2,   # 20% chance resting limit fills
    prob_slippage=0.5,        # 50% chance of 1-tick slippage
    random_seed=42,           # For reproducibility
)

engine.add_venue(
    venue=SIM,
    oms_type=OmsType.NETTING,
    account_type=AccountType.MARGIN,
    starting_balances=[Money(1_000_000, USD)],
    fill_model=fill_model,
)
```

## Reports and analysis

### Built-in reports

After `engine.run()`, generate pandas DataFrame reports:

```python
# Account balance over time
account_report = engine.trader.generate_account_report(SIM)

# All orders with status, fill info
orders_report = engine.trader.generate_orders_report()

# Filled orders only
order_fills = engine.trader.generate_order_fills_report()

# Positions with PnL
positions_report = engine.trader.generate_positions_report()

# Individual fill events
fills_report = engine.trader.generate_fills_report()
```

### Performance statistics

```python
portfolio = engine.portfolio

# PnL stats (per currency)
stats_pnls = portfolio.analyzer.get_performance_stats_pnls()

# Returns stats (Sharpe, Sortino, max drawdown, etc.)
stats_returns = portfolio.analyzer.get_performance_stats_returns()

# General stats (win rate, profit factor, avg trade, etc.)
stats_general = portfolio.analyzer.get_performance_stats_general()
```

### Tearsheet visualization

Generate an interactive HTML performance report:

```python
from nautilus_trader.analysis import create_tearsheet

# After engine.run()
create_tearsheet(
    engine=engine,
    output_path="tearsheet.html",
)
```

This creates an HTML file with:
- Equity curve
- Drawdown chart
- Monthly returns heatmap
- Returns distribution
- Rolling Sharpe ratio
- Performance statistics tables

Requires: `pip install "nautilus_trader[visualization]"`

### Custom tearsheet configuration

```python
from nautilus_trader.analysis import (
    TearsheetConfig,
    TearsheetEquityChart,
    TearsheetDrawdownChart,
    TearsheetStatsTableChart,
    TearsheetRunInfoChart,
)

config = TearsheetConfig(
    charts=[
        TearsheetRunInfoChart(),
        TearsheetStatsTableChart(),
        TearsheetEquityChart(),
        TearsheetDrawdownChart(),
    ],
    theme="nautilus_dark",  # or "plotly_white", "nautilus", "plotly_dark"
    height=2000,
)

create_tearsheet(engine=engine, output_path="custom.html", config=config)
```

### Bars with fills chart (standalone)

```python
from nautilus_trader.analysis import create_bars_with_fills

fig = create_bars_with_fills(
    engine=engine,
    bar_type=BarType.from_str("EUR/USD.SIM-1-MINUTE-LAST-EXTERNAL"),
    title="EUR/USD - Entry/Exit Analysis",
)
fig.write_html("bars_with_fills.html")
```

## Multiple backtest runs

### With BacktestEngine (parameter optimization)

```python
# Data and instruments persist across resets
engine.add_venue(...)
engine.add_instrument(instrument)
engine.add_data(data)

# Run with parameter set 1
engine.add_strategy(strategy_v1)
engine.run()
results_v1 = engine.trader.generate_positions_report()

# Reset (clears strategy, orders, positions — keeps data)
engine.reset()

# Run with parameter set 2
engine.add_strategy(strategy_v2)
engine.run()
results_v2 = engine.trader.generate_positions_report()
```

### With BacktestNode (multiple configs)

```python
configs = [
    BacktestRunConfig(engine=engine_config1, data=data_configs, venues=venue_configs),
    BacktestRunConfig(engine=engine_config2, data=data_configs, venues=venue_configs),
]
node = BacktestNode(configs=configs)
results = node.run()  # Returns list of results
```

## Key tips

- **Register indicators before requesting data** — otherwise they miss historical bars
- **Use `EXTERNAL` for pre-aggregated bars** (e.g., from CSV), `INTERNAL` when Nautilus
  should aggregate from ticks
- **Start with bar data** for faster iteration, then move to tick/orderbook data for
  higher fidelity when the strategy looks promising
- **Refer to `examples/backtest/`** in the repository for many working examples
  covering FX, crypto, equities, and order book strategies
