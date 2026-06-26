# Known Use Cases (KUC)

Total: **14**

## `KUC-101`
**Source**: `scripts/v2_funding_rate_arb.py`

Exploits funding rate differences between perpetual exchanges (e.g., Hyperliquid and Binance) to generate risk-adjusted returns using leverage.

## `KUC-102`
**Source**: `scripts/log_price_example.py`

Demonstrates how to retrieve and log market prices (best bid, best ask, mid price) from multiple exchanges for monitoring purposes.

## `KUC-103`
**Source**: `scripts/xrpl_liquidity_example.py`

Provides liquidity on XRPL (Ripple Ledger) decentralized exchange when price crosses user-defined target levels.

## `KUC-104`
**Source**: `scripts/download_order_book_and_trades.py`

Collects and exports historical order book snapshots and trade data to CSV files for backtesting and analysis.

## `KUC-105`
**Source**: `scripts/external_events_example.py`

Demonstrates how to use the MQTT external events plugin to subscribe to external topics and receive/process messages.

## `KUC-106`
**Source**: `scripts/amm_data_feed_example.py`

Fetches and displays real-time price data from AMM DEX connectors (Jupiter, Uniswap) via the Gateway for analysis.

## `KUC-107`
**Source**: `scripts/screener_volatility.py`

Scans multiple trading pairs to identify highly volatile instruments using Bollinger Bands width, percentage, and NATR indicators.

## `KUC-108`
**Source**: `scripts/simple_xemm.py`

Places maker orders on one exchange and immediately hedges/hedging filled orders on another exchange to capture spread.

## `KUC-109`
**Source**: `scripts/format_status_example.py`

Demonstrates how to add custom status display formatting to a strategy using format_status method and market status dataframes.

## `KUC-110`
**Source**: `scripts/simple_pmm.py`

Provides liquidity by placing bid and ask orders around the mid price with configurable spreads, refreshing at set intervals.

## `KUC-111`
**Source**: `scripts/v2_with_controllers.py`

Runs a multi-controller strategy with features like cash-out scheduling, dynamic config reloading, and drawdown protection.

## `KUC-112`
**Source**: `scripts/candles_example.py`

Demonstrates how to initialize and consume candles data feeds for multiple trading pairs and timeframes without requiring market trading.

## `KUC-113`
**Source**: `scripts/xrpl_arb_example.py`

Exploits price differences between XRPL decentralized exchange and centralized exchanges for risk-free profit opportunities.

## `KUC-114`
**Source**: `scripts/simple_vwap.py`

Executes large buy or sell orders using Volume Weighted Average Price algorithm, splitting orders to minimize market impact.
