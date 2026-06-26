# Live Trading Guide

This guide explains how to connect NautilusTrader to real exchanges and brokers for live trading.

## IMPORTANT: Risk warning

**Live trading involves real financial risk.** Before deploying:

1. **Thoroughly backtest** your strategy with realistic fill models
2. **Paper trade** in Sandbox mode with real market data
3. **Start with small position sizes** when going live
4. **Never run live trading in Jupyter notebooks** — use standalone Python scripts
5. **One TradingNode per process** — do not run multiple nodes in the same process

## Supported exchanges and brokers

### Crypto exchanges (CEX)

| Exchange | Venue ID | Status | Required credentials | Extra features |
|---|---|---|---|---|
| **Binance** | `BINANCE` | stable | `BINANCE_API_KEY`, `BINANCE_API_SECRET` | Spot, USDT Futures, Coin Futures; testnet available |
| **Bybit** | `BYBIT` | stable | `BYBIT_API_KEY`, `BYBIT_API_SECRET` | Spot, Linear, Inverse; testnet available |
| **OKX** | `OKX` | stable | `OKX_API_KEY`, `OKX_API_SECRET`, `OKX_PASSPHRASE` | Spot, Futures, Options; demo mode available |
| **Kraken** | `KRAKEN` | stable | `KRAKEN_API_KEY`, `KRAKEN_API_SECRET` | Spot, Futures |
| **BitMEX** | `BITMEX` | stable | `BITMEX_API_KEY`, `BITMEX_API_SECRET` | Derivatives; testnet available |
| **Deribit** | `DERIBIT` | stable | `DERIBIT_CLIENT_ID`, `DERIBIT_CLIENT_SECRET` | Options, Futures; testnet available |

### Crypto exchanges (DEX)

| Exchange | Venue ID | Status | Required credentials |
|---|---|---|---|
| **dYdX** | `DYDX` | stable | Mnemonic or private key |
| **Hyperliquid** | `HYPERLIQUID` | stable | Private key; testnet available |
| **Polymarket** | `POLYMARKET` | stable | Private key |

### Traditional finance

| Broker/Provider | Venue ID | Status | Required setup |
|---|---|---|---|
| **Interactive Brokers** | `INTERACTIVE_BROKERS` | stable | TWS or IB Gateway running locally, account credentials |
| **AX Exchange** | `AX` | beta | API Key + Secret |

### Data providers (no execution)

| Provider | Venue ID | Status | Usage |
|---|---|---|---|
| **Databento** | `DATABENTO` | stable | US equities, futures, options data (CME, XNAS, etc.) |
| **Tardis** | `TARDIS` | stable | Historical and live crypto data |

## Complete live trading example (Binance Spot)

```python
from decimal import Decimal

from nautilus_trader.adapters.binance import BINANCE
from nautilus_trader.adapters.binance import BinanceAccountType
from nautilus_trader.adapters.binance import BinanceDataClientConfig
from nautilus_trader.adapters.binance import BinanceExecClientConfig
from nautilus_trader.adapters.binance import BinanceLiveDataClientFactory
from nautilus_trader.adapters.binance import BinanceLiveExecClientFactory
from nautilus_trader.config import (
    InstrumentProviderConfig,
    LiveExecEngineConfig,
    LoggingConfig,
    TradingNodeConfig,
)
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.data import BarType
from nautilus_trader.model.identifiers import InstrumentId, TraderId

# -- Your strategy import --
# from my_strategy import MyStrategy, MyStrategyConfig


# 1. Configure the TradingNode
config_node = TradingNodeConfig(
    trader_id=TraderId("LIVE-001"),
    logging=LoggingConfig(
        log_level="INFO",
        log_level_file="DEBUG",   # Detailed logs to file
    ),
    exec_engine=LiveExecEngineConfig(
        reconciliation=True,                # Always enable for live
        reconciliation_lookback_mins=1440,  # 24 hours
    ),
    data_clients={
        BINANCE: BinanceDataClientConfig(
            api_key=None,       # Uses BINANCE_API_KEY env var
            api_secret=None,    # Uses BINANCE_API_SECRET env var
            account_type=BinanceAccountType.SPOT,
            testnet=False,      # PRODUCTION
            instrument_provider=InstrumentProviderConfig(load_all=True),
        ),
    },
    exec_clients={
        BINANCE: BinanceExecClientConfig(
            api_key=None,       # Uses BINANCE_API_KEY env var
            api_secret=None,    # Uses BINANCE_API_SECRET env var
            account_type=BinanceAccountType.SPOT,
            testnet=False,      # PRODUCTION
            instrument_provider=InstrumentProviderConfig(load_all=True),
            max_retries=3,
        ),
    },
    timeout_connection=30.0,
    timeout_reconciliation=10.0,
    timeout_portfolio=10.0,
    timeout_disconnection=10.0,
    timeout_post_stop=5.0,
)

# 2. Create TradingNode
node = TradingNode(config=config_node)

# 3. Configure and add strategy
strategy = MyStrategy(
    MyStrategyConfig(
        instrument_id=InstrumentId.from_str("ETHUSDT.BINANCE"),
        bar_type=BarType.from_str("ETHUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL"),
        trade_size=Decimal("0.05"),
    ),
)
node.trader.add_strategy(strategy)

# 4. Register client factories
node.add_data_client_factory(BINANCE, BinanceLiveDataClientFactory)
node.add_exec_client_factory(BINANCE, BinanceLiveExecClientFactory)
node.build()

# 5. Run (CTRL+C to stop gracefully)
if __name__ == "__main__":
    try:
        node.run()
    finally:
        node.dispose()
```

## Exchange-specific configuration

### Binance Futures

```python
from nautilus_trader.adapters.binance import BinanceAccountType

# USDT-margined futures
data_config = BinanceDataClientConfig(
    account_type=BinanceAccountType.USDT_FUTURES,
    testnet=False,
    instrument_provider=InstrumentProviderConfig(load_all=True),
)

exec_config = BinanceExecClientConfig(
    account_type=BinanceAccountType.USDT_FUTURES,
    testnet=False,
    instrument_provider=InstrumentProviderConfig(load_all=True),
)

# Instrument ID format: "BTCUSDT-PERP.BINANCE"
```

### Bybit

```python
from nautilus_trader.adapters.bybit import BYBIT
from nautilus_trader.adapters.bybit import BybitDataClientConfig
from nautilus_trader.adapters.bybit import BybitExecClientConfig
from nautilus_trader.adapters.bybit import BybitLiveDataClientFactory
from nautilus_trader.adapters.bybit import BybitLiveExecClientFactory
from nautilus_trader.adapters.bybit import BybitProductType

data_config = BybitDataClientConfig(
    product_types=[BybitProductType.LINEAR],
    testnet=False,
    instrument_provider=InstrumentProviderConfig(load_all=True),
)

exec_config = BybitExecClientConfig(
    product_types=[BybitProductType.LINEAR],
    testnet=False,
    instrument_provider=InstrumentProviderConfig(load_all=True),
)
```

### Interactive Brokers

Requires TWS or IB Gateway running locally:

```python
from nautilus_trader.adapters.interactive_brokers.common import IB
from nautilus_trader.adapters.interactive_brokers.config import (
    InteractiveBrokersDataClientConfig,
    InteractiveBrokersExecClientConfig,
)
from nautilus_trader.adapters.interactive_brokers.factories import (
    InteractiveBrokersLiveDataClientFactory,
    InteractiveBrokersLiveExecClientFactory,
)

data_config = InteractiveBrokersDataClientConfig(
    ibg_host="127.0.0.1",
    ibg_port=7497,       # TWS live: 7496, paper: 7497; Gateway live: 4001, paper: 4002
    ibg_client_id=1,
    instrument_provider=InstrumentProviderConfig(load_all=False),
)

exec_config = InteractiveBrokersExecClientConfig(
    ibg_host="127.0.0.1",
    ibg_port=7497,
    ibg_client_id=1,
    instrument_provider=InstrumentProviderConfig(load_all=False),
    account_id="YOUR_ACCOUNT_ID",  # e.g., "DU12345" for paper
)
```

**IB Prerequisites:**
- Install TWS (Trader Workstation) or IB Gateway
- Enable API access in TWS/Gateway settings
- Configure allowed IP addresses
- For paper trading: use port 7497 (TWS) or 4002 (Gateway)
- For live trading: use port 7496 (TWS) or 4001 (Gateway)

See `docs/integrations/ib.md` for the complete IB integration guide.

## Multi-venue configuration

Connect to multiple exchanges simultaneously:

```python
config_node = TradingNodeConfig(
    data_clients={
        "BINANCE_SPOT": BinanceDataClientConfig(
            account_type=BinanceAccountType.SPOT,
        ),
        "BINANCE_FUTURES": BinanceDataClientConfig(
            account_type=BinanceAccountType.USDT_FUTURES,
        ),
    },
    exec_clients={
        "BINANCE_SPOT": BinanceExecClientConfig(
            account_type=BinanceAccountType.SPOT,
        ),
        "BINANCE_FUTURES": BinanceExecClientConfig(
            account_type=BinanceAccountType.USDT_FUTURES,
        ),
    },
)
```

## Execution reconciliation

Reconciliation aligns the engine's internal state with the exchange's actual state at startup.
It recovers missed order events, fills, and position changes.

**Always enable reconciliation for live trading:**

```python
LiveExecEngineConfig(
    reconciliation=True,
    reconciliation_lookback_mins=1440,  # Look back 24 hours
)
```

Key settings:

| Setting | Default | Description |
|---|---|---|
| `reconciliation` | True | Enable startup reconciliation |
| `reconciliation_lookback_mins` | None (max) | How far back to check |
| `inflight_check_interval_ms` | 2000 | Monitor unconfirmed orders |
| `open_check_interval_secs` | None | Periodic open order verification |

## Environment variables

Most adapters read credentials from environment variables. Set them before running:

```bash
# Binance
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"

# Binance testnet
export BINANCE_FUTURES_TESTNET_API_KEY="your_testnet_key"
export BINANCE_FUTURES_TESTNET_API_SECRET="your_testnet_secret"

# Bybit
export BYBIT_API_KEY="your_key"
export BYBIT_API_SECRET="your_secret"

# OKX
export OKX_API_KEY="your_key"
export OKX_API_SECRET="your_secret"
export OKX_PASSPHRASE="your_passphrase"
```

## Strategy considerations for live trading

### Strategy must not block the event loop

All strategy callbacks (`on_bar`, `on_quote_tick`, etc.) run on the main event loop thread.
They must return quickly. Move heavy computation to a background thread:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class MyStrategy(Strategy):
    def __init__(self, config):
        super().__init__(config)
        self._executor = ThreadPoolExecutor(max_workers=1)

    def on_bar(self, bar: Bar) -> None:
        # Quick calculations are OK here
        if self.should_compute_signal():
            # Offload heavy work
            loop = asyncio.get_event_loop()
            loop.run_in_executor(self._executor, self._heavy_computation, bar)

    def _heavy_computation(self, bar):
        # ML inference, complex calculations, etc.
        pass
```

### Graceful shutdown

```python
if __name__ == "__main__":
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.stop()
        finally:
            node.dispose()
```

### Managing stop behavior

Configure automatic position closing on stop:

```python
config = MyStrategyConfig(
    manage_stop=True,    # Performs market_exit() before stopping
    close_positions_on_stop=True,
)
```

## Testing progression

Recommended path from development to production:

1. **Backtest** with historical data → validate strategy logic
2. **Backtest** with realistic fill model → assess execution sensitivity
3. **Sandbox** with testnet data → verify live data handling
4. **Sandbox** with production data → confirm real market behavior
5. **Live** with testnet/paper account → test exchange connectivity
6. **Live** with small real capital → gradual scale-up

## Detailed integration guides

For exchange-specific details (instrument formats, API limits, supported features),
read the per-exchange guide in `docs/integrations/`:

| Exchange | Guide file |
|---|---|
| Binance | `docs/integrations/binance.md` |
| Bybit | `docs/integrations/bybit.md` |
| OKX | `docs/integrations/okx.md` |
| Kraken | `docs/integrations/kraken.md` |
| BitMEX | `docs/integrations/bitmex.md` |
| Deribit | `docs/integrations/deribit.md` |
| dYdX | `docs/integrations/dydx.md` |
| Hyperliquid | `docs/integrations/hyperliquid.md` |
| Interactive Brokers | `docs/integrations/ib.md` |
| Polymarket | `docs/integrations/polymarket.md` |
| Databento | `docs/integrations/databento.md` |
| Tardis | `docs/integrations/tardis.md` |

Also see `examples/live/` in the repository for per-exchange runnable examples.
