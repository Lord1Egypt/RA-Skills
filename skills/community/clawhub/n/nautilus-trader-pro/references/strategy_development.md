# Strategy Development Guide

This guide explains how to write trading strategies with NautilusTrader.

## Strategy architecture

A strategy consists of two parts:

1. **StrategyConfig** — Configuration class (optional but recommended). Defines parameters.
2. **Strategy** — The strategy class. Inherits from `Strategy` and implements event handlers.

The same strategy code runs identically in backtest, sandbox, and live modes.

## Minimal strategy template

```python
from decimal import Decimal

from nautilus_trader.config import StrategyConfig
from nautilus_trader.indicators import ExponentialMovingAverage
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.trading.strategy import Strategy


class MyStrategyConfig(StrategyConfig, frozen=True):
    """
    Configuration for MyStrategy.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument to trade.
    bar_type : BarType
        The bar type to use for signals.
    trade_size : Decimal
        The position size per trade.
    fast_ema_period : int
        Fast EMA period.
    slow_ema_period : int
        Slow EMA period.

    """
    instrument_id: InstrumentId
    bar_type: BarType
    trade_size: Decimal
    fast_ema_period: int = 10
    slow_ema_period: int = 20


class MyStrategy(Strategy):
    def __init__(self, config: MyStrategyConfig) -> None:
        super().__init__(config)
        # Create indicators
        self.fast_ema = ExponentialMovingAverage(config.fast_ema_period)
        self.slow_ema = ExponentialMovingAverage(config.slow_ema_period)

    def on_start(self) -> None:
        """Called when the strategy starts. Set up subscriptions and state."""
        # Validate instrument exists
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if self.instrument is None:
            self.log.error(f"Could not find instrument {self.config.instrument_id}")
            self.stop()
            return

        # Register indicators for automatic updates
        self.register_indicator_for_bars(self.config.bar_type, self.fast_ema)
        self.register_indicator_for_bars(self.config.bar_type, self.slow_ema)

        # Request historical data (to warm up indicators)
        self.request_bars(self.config.bar_type)

        # Subscribe to live data
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar) -> None:
        """Called on each new bar. Implement trading logic here."""
        # Wait for indicators to warm up
        if not self.indicators_initialized():
            self.log.info(
                f"Waiting for indicators to warm up "
                f"[{self.cache.bar_count(self.config.bar_type)}]",
            )
            return

        # === YOUR TRADING LOGIC HERE ===
        # BUY signal: fast EMA crosses above slow EMA
        if self.fast_ema.value >= self.slow_ema.value:
            if self.portfolio.is_flat(self.config.instrument_id):
                self.buy()
            elif self.portfolio.is_net_short(self.config.instrument_id):
                self.close_all_positions(self.config.instrument_id)
                self.buy()

        # SELL signal: fast EMA crosses below slow EMA
        elif self.fast_ema.value < self.slow_ema.value:
            if self.portfolio.is_flat(self.config.instrument_id):
                self.sell()
            elif self.portfolio.is_net_long(self.config.instrument_id):
                self.close_all_positions(self.config.instrument_id)
                self.sell()

    def buy(self) -> None:
        order = self.order_factory.market(
            instrument_id=self.config.instrument_id,
            order_side=OrderSide.BUY,
            quantity=self.instrument.make_qty(self.config.trade_size),
        )
        self.submit_order(order)

    def sell(self) -> None:
        order = self.order_factory.market(
            instrument_id=self.config.instrument_id,
            order_side=OrderSide.SELL,
            quantity=self.instrument.make_qty(self.config.trade_size),
        )
        self.submit_order(order)

    def on_stop(self) -> None:
        """Called when the strategy stops. Clean up."""
        self.cancel_all_orders(self.config.instrument_id)
        self.close_all_positions(self.config.instrument_id)
        self.unsubscribe_bars(self.config.bar_type)

    def on_reset(self) -> None:
        """Called on strategy reset. Reset indicators."""
        self.fast_ema.reset()
        self.slow_ema.reset()
```

## Strategy lifecycle handlers

These are called by the Nautilus engine at specific lifecycle events:

| Handler | When it's called | Typical use |
|---|---|---|
| `on_start()` | Strategy starts | Subscribe to data, initialize state |
| `on_stop()` | Strategy stops | Cancel orders, close positions |
| `on_resume()` | Strategy resumes | Re-subscribe after a pause |
| `on_reset()` | Strategy resets | Reset indicators and custom state |
| `on_dispose()` | Strategy is destroyed | Release resources |

## Data handlers

These are called when market data arrives:

| Handler | Data type | Use case |
|---|---|---|
| `on_bar(bar: Bar)` | Bar/candle data | Most common — time-based strategies |
| `on_quote_tick(tick: QuoteTick)` | Bid/ask quotes | Spread-based strategies, HFT |
| `on_trade_tick(tick: TradeTick)` | Individual trades | Volume-based strategies |
| `on_order_book(book: OrderBook)` | Full order book | Market-making, order flow |
| `on_order_book_deltas(deltas)` | Book updates | Incremental book processing |
| `on_data(data: Data)` | Custom data types | User-defined signals |
| `on_historical_data(data: Data)` | Historical response | Processing requested history |

## Order management

### Order types

Create orders via `self.order_factory`:

```python
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.objects import Price, Quantity

# Market order
order = self.order_factory.market(
    instrument_id=self.config.instrument_id,
    order_side=OrderSide.BUY,
    quantity=self.instrument.make_qty(Decimal("1.0")),
)

# Limit order
order = self.order_factory.limit(
    instrument_id=self.config.instrument_id,
    order_side=OrderSide.BUY,
    quantity=self.instrument.make_qty(Decimal("1.0")),
    price=self.instrument.make_price(50000.00),
    time_in_force=TimeInForce.GTC,
)

# Stop-market order
order = self.order_factory.stop_market(
    instrument_id=self.config.instrument_id,
    order_side=OrderSide.SELL,
    quantity=self.instrument.make_qty(Decimal("1.0")),
    trigger_price=self.instrument.make_price(49000.00),
)

# Submit any order
self.submit_order(order)
```

### Order event handlers

Monitor order lifecycle events:

```python
def on_order_accepted(self, event) -> None: ...
def on_order_rejected(self, event) -> None: ...
def on_order_filled(self, event) -> None: ...
def on_order_canceled(self, event) -> None: ...
def on_order_expired(self, event) -> None: ...
def on_order_event(self, event) -> None: ...  # Catches all order events
```

### Position event handlers

```python
def on_position_opened(self, event) -> None: ...
def on_position_changed(self, event) -> None: ...
def on_position_closed(self, event) -> None: ...
```

### Position management

```python
# Check position state
self.portfolio.is_flat(instrument_id)       # No position
self.portfolio.is_net_long(instrument_id)   # Net long
self.portfolio.is_net_short(instrument_id)  # Net short

# Close positions
self.close_all_positions(instrument_id)

# Cancel orders
self.cancel_all_orders(instrument_id)
self.cancel_order(order)

# Modify existing order
self.modify_order(order, new_quantity)

# Graceful exit (cancel orders + close positions)
self.market_exit()
```

## Indicators

NautilusTrader includes many built-in indicators in `nautilus_trader.indicators`:

| Indicator | Class |
|---|---|
| EMA | `ExponentialMovingAverage(period)` |
| SMA | `SimpleMovingAverage(period)` |
| RSI | `RelativeStrengthIndex(period)` |
| ATR | `AverageTrueRange(period)` |
| Bollinger Bands | `BollingerBands(period, k)` |
| MACD | `MovingAverageConvergenceDivergence(fast, slow, signal)` |

### Registering indicators

```python
# Register for automatic updates with bar data
self.register_indicator_for_bars(bar_type, self.ema)

# Register for automatic updates with quote ticks
self.register_indicator_for_quote_ticks(instrument_id, self.ema)

# Register for automatic updates with trade ticks
self.register_indicator_for_trade_ticks(instrument_id, self.ema)

# Check if all registered indicators are warmed up
if self.indicators_initialized():
    # Safe to use indicator values
    value = self.ema.value
```

## Timers and scheduled actions

```python
import pandas as pd

# Set a one-time alert
self.clock.set_time_alert(
    name="MyAlert",
    alert_time=self.clock.utc_now() + pd.Timedelta(minutes=5),
)

# Set a recurring timer
self.clock.set_timer(
    name="MyTimer",
    interval=pd.Timedelta(minutes=1),
)

# Handle timer events in on_event
def on_event(self, event) -> None:
    if isinstance(event, TimeEvent) and event.name == "MyTimer":
        # Do periodic work
        pass
```

## Cache access

```python
# Get latest data
last_quote = self.cache.quote_tick(instrument_id)
last_trade = self.cache.trade_tick(instrument_id)
last_bar = self.cache.bar(bar_type)

# Get orders and positions
order = self.cache.order(client_order_id)
position = self.cache.position(position_id)

# Get instrument
instrument = self.cache.instrument(instrument_id)
```

## Multiple strategy instances

When running multiple instances of the same strategy (different instruments or parameters),
give each a unique `order_id_tag`:

```python
config1 = MyStrategyConfig(
    instrument_id="EUR/USD.SIM",
    order_id_tag="001",  # Unique tag
    ...
)
config2 = MyStrategyConfig(
    instrument_id="GBP/USD.SIM",
    order_id_tag="002",  # Different tag
    ...
)
```

## Writing more complex strategies

For advanced strategy patterns beyond the simple EMA cross template above, refer to:

| Pattern | Example file |
|---|---|
| Bracket orders (entry + SL + TP) | `nautilus_trader/examples/strategies/ema_cross_bracket.py` |
| Bracket with exec algorithm (TWAP) | `nautilus_trader/examples/strategies/ema_cross_bracket_algo.py` |
| Stop entry orders | `nautilus_trader/examples/strategies/ema_cross_stop_entry.py` |
| Trailing stop loss | `nautilus_trader/examples/strategies/ema_cross_trailing_stop.py` |
| Market making | `nautilus_trader/examples/strategies/volatility_market_maker.py` |
| Order book imbalance | `nautilus_trader/examples/strategies/orderbook_imbalance.py` |
| Hedge mode (dual positions) | `nautilus_trader/examples/strategies/ema_cross_hedge_mode.py` |

For more complex concepts also see:

- **Execution algorithms**: `docs/concepts/execution.md` — TWAP, custom algos
- **Custom data types**: `docs/concepts/custom_data.md` — integrate non-market signals
- **Actors**: `docs/concepts/actors.md` — for non-trading components (data processing, signals)
- **Order types and advanced orders**: `docs/concepts/orders.md`
- **Options and greeks**: `docs/concepts/options.md` and `docs/concepts/greeks.md`
