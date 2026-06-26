# Paper Trading (Sandbox) Guide

This guide explains how to run paper trading using NautilusTrader's Sandbox mode, which
uses **real-time market data** from a live exchange but executes orders through a **local
simulated exchange**.

## What is Sandbox mode?

Sandbox mode combines:
- **Live data client** → real market data from an exchange (prices, order books, bars)
- **Sandbox execution client** → local simulated exchange (no real orders sent)

This lets you test strategies against real market conditions without risking capital.

## How Sandbox differs from Backtest and Live

| Aspect | Backtest | Sandbox | Live |
|---|---|---|---|
| Data source | Historical files | Live exchange feeds | Live exchange feeds |
| Order execution | Simulated (BacktestEngine) | Simulated (SandboxExecClient) | Real exchange |
| Market impact | None | None | Real |
| Account balance | Simulated | Simulated (configurable) | Real |
| Running mode | Finite (data exhaustion) | Continuous | Continuous |

## Complete Sandbox example (Binance Futures)

```python
import asyncio
from decimal import Decimal

from nautilus_trader.adapters.binance import BINANCE, BINANCE_VENUE
from nautilus_trader.adapters.binance import BinanceAccountType
from nautilus_trader.adapters.binance import BinanceDataClientConfig
from nautilus_trader.adapters.binance.factories import BinanceLiveDataClientFactory
from nautilus_trader.adapters.sandbox.config import SandboxExecutionClientConfig
from nautilus_trader.adapters.sandbox.factory import SandboxLiveExecClientFactory
from nautilus_trader.config import (
    CacheConfig,
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


async def main():
    # 1. Configure the TradingNode
    config_node = TradingNodeConfig(
        trader_id=TraderId("SANDBOX-001"),
        logging=LoggingConfig(
            log_level="INFO",
            log_colors=True,
            use_pyo3=True,
        ),
        exec_engine=LiveExecEngineConfig(
            reconciliation=True,
            reconciliation_lookback_mins=1440,
            filter_position_reports=True,
        ),
        cache=CacheConfig(
            timestamps_as_iso8601=True,
            flush_on_start=False,
        ),
        # DATA: Real market data from Binance testnet
        data_clients={
            BINANCE: BinanceDataClientConfig(
                api_key=None,       # Uses BINANCE_API_KEY env var
                api_secret=None,    # Uses BINANCE_API_SECRET env var
                account_type=BinanceAccountType.USDT_FUTURES,
                testnet=True,       # Use testnet for safety
                instrument_provider=InstrumentProviderConfig(load_all=True),
            ),
        },
        # EXECUTION: Local sandbox (no real orders)
        exec_clients={
            BINANCE: SandboxExecutionClientConfig(
                venue=BINANCE_VENUE,
                starting_balances=["10_000 USDT", "10 ETH"],
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
            instrument_id=InstrumentId.from_str("ETHUSDT-PERP.BINANCE"),
            bar_type=BarType.from_str("ETHUSDT-PERP.BINANCE-1-MINUTE-LAST-EXTERNAL"),
            trade_size=Decimal("0.010"),
        ),
    )
    node.trader.add_strategy(strategy)

    # 4. Register client factories
    node.add_data_client_factory(BINANCE, BinanceLiveDataClientFactory)
    node.add_exec_client_factory(BINANCE, SandboxLiveExecClientFactory)
    node.build()

    # 5. Run (CTRL+C to stop)
    try:
        await node.run_async()
    finally:
        await node.stop_async()
        await asyncio.sleep(1)
        node.dispose()


if __name__ == "__main__":
    asyncio.run(main())
```

## Key configuration details

### SandboxExecutionClientConfig

```python
from nautilus_trader.adapters.sandbox.config import SandboxExecutionClientConfig

SandboxExecutionClientConfig(
    venue=BINANCE_VENUE,                        # Venue to simulate
    starting_balances=["10_000 USDT", "10 ETH"],  # Initial balances
)
```

- `venue`: The venue identifier (must match data client venue)
- `starting_balances`: List of starting balances as `"{amount} {currency}"` strings

### Using testnet data

For Binance, set `testnet=True` in the data client config to use testnet data feeds.
This avoids needing production API credentials for paper trading.

Required environment variables (for Binance testnet):
```bash
export BINANCE_FUTURES_TESTNET_API_KEY="your_testnet_key"
export BINANCE_FUTURES_TESTNET_API_SECRET="your_testnet_secret"
```

Get testnet keys from: https://testnet.binancefuture.com

### Client factory pairing

The key to Sandbox mode is using **mismatched** factories:

```python
# Data: real exchange data factory
node.add_data_client_factory(BINANCE, BinanceLiveDataClientFactory)

# Execution: sandbox simulated factory (NOT BinanceLiveExecClientFactory)
node.add_exec_client_factory(BINANCE, SandboxLiveExecClientFactory)
```

## Sandbox with other exchanges

### Bybit

```python
from nautilus_trader.adapters.bybit import BYBIT, BYBIT_VENUE
from nautilus_trader.adapters.bybit import BybitDataClientConfig
from nautilus_trader.adapters.bybit.factories import BybitLiveDataClientFactory

config_node = TradingNodeConfig(
    data_clients={
        BYBIT: BybitDataClientConfig(
            testnet=True,
            instrument_provider=InstrumentProviderConfig(load_all=True),
        ),
    },
    exec_clients={
        BYBIT: SandboxExecutionClientConfig(
            venue=BYBIT_VENUE,
            starting_balances=["10_000 USDT"],
        ),
    },
    ...
)

node.add_data_client_factory(BYBIT, BybitLiveDataClientFactory)
node.add_exec_client_factory(BYBIT, SandboxLiveExecClientFactory)
```

### Interactive Brokers

```python
from nautilus_trader.adapters.interactive_brokers.common import IB
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersDataClientConfig
from nautilus_trader.adapters.interactive_brokers.factories import (
    InteractiveBrokersLiveDataClientFactory,
)

config_node = TradingNodeConfig(
    data_clients={
        IB: InteractiveBrokersDataClientConfig(
            ibg_host="127.0.0.1",
            ibg_port=4002,  # Paper trading port
            ibg_client_id=1,
            instrument_provider=InstrumentProviderConfig(load_all=False),
        ),
    },
    exec_clients={
        IB: SandboxExecutionClientConfig(
            venue=IB,
            starting_balances=["100_000 USD"],
        ),
    },
    ...
)

node.add_data_client_factory("IB", InteractiveBrokersLiveDataClientFactory)
node.add_exec_client_factory("IB", SandboxLiveExecClientFactory)
```

## Monitoring and results

During a sandbox session, you can monitor:

1. **Logs**: Strategy logs, order events, fill events appear in console
2. **Cache**: Access orders, positions, and account data via `node.trader.cache`

After stopping the node, you can generate reports the same way as backtesting:

```python
# These work the same as in backtesting
orders_report = node.trader.generate_orders_report()
positions_report = node.trader.generate_positions_report()
```

## Key tips

- **Always test with testnet first** before connecting to production data feeds
- **The same strategy file** used in backtesting works in Sandbox — only the config changes
- **Look at `examples/sandbox/`** in the repository for per-exchange sandbox examples
- **Sandbox mode has the same matching engine** as backtesting (L1 by default), so fills
  are simulated locally based on market data
- **Network errors in data feeds** will affect sandbox just like live trading — this is
  actually useful for testing strategy resilience
