# Known Use Cases (KUC)

Total: **73**

## `KUC-101`
**Source**: `docs/getting_started/backtest_high_level.py`

Users need to run backtests using a config-driven approach with the BacktestNode, enabling reproducible production workflows that can transition to live trading.

## `KUC-102`
**Source**: `docs/getting_started/backtest_low_level.py`

Users need fine-grained control over backtesting components including custom execution algorithms like TWAP for sophisticated order execution simulation.

## `KUC-103`
**Source**: `docs/getting_started/quickstart.py`

New users need a minimal example to run their first backtest quickly, demonstrating the core strategy and market data handling pattern.

## `KUC-104`
**Source**: `docs/how_to/data_catalog_databento.py`

Users need to efficiently store and query historical market data from Databento using Nautilus Parquet data catalog for backtests and research.

## `KUC-105`
**Source**: `docs/how_to/loading_external_data.py`

Users with historical CSV data from external vendors need to load it into the Parquet data catalog for backtesting with BacktestNode.

## `KUC-106`
**Source**: `docs/tutorials/backtest_fx_bars.py`

Users need to backtest FX strategies with realistic rollover interest simulation and probabilistic fill modeling for USD/JPY.

## `KUC-107`
**Source**: `docs/tutorials/backtest_orderbook_binance.py`

Users need to backtest order book imbalance strategies using Binance exchange depth data for high-frequency trading signal generation.

## `KUC-108`
**Source**: `docs/tutorials/backtest_orderbook_bybit.py`

Users need to backtest order book imbalance strategies using Bybit exchange depth data for high-frequency trading signal generation.

## `KUC-109`
**Source**: `examples/backtest/architect_ax_book_imbalance.py`

Users need to backtest an order book imbalance strategy using Archax exchange data loaded from Databento for crypto perpetual contracts.

## `KUC-110`
**Source**: `examples/backtest/architect_ax_mean_reversion.py`

Users need to backtest a mean reversion strategy using Bollinger Bands indicators on Archax exchange crypto perpetuals.

## `KUC-111`
**Source**: `examples/backtest/betfair_backtest_orderbook_imbalance.py`

Users need to backtest order book imbalance strategies on Betfair sports betting exchange using NautilusTrader.

## `KUC-112`
**Source**: `examples/backtest/bitmex_grid_market_maker.py`

Users need to backtest a grid market making strategy on BitMEX using Tardis quote data for XBTUSD perpetual.

## `KUC-113`
**Source**: `examples/backtest/crypto_ema_cross_ethusdt_trade_ticks.py`

Users need to backtest an EMA crossover strategy with TWAP execution algorithm on Binance ETHUSDT using trade tick data.

## `KUC-114`
**Source**: `examples/backtest/crypto_ema_cross_ethusdt_trailing_stop.py`

Users need to backtest an EMA crossover strategy with trailing stop protection on Binance ETHUSDT trade tick data.

## `KUC-115`
**Source**: `examples/backtest/crypto_ema_cross_with_binance_provider.py`

Users need to backtest an EMA cross with trailing stop strategy using Binance futures instrument provider for real instrument data.

## `KUC-116`
**Source**: `examples/backtest/crypto_orderbook_imbalance.py`

Users need to backtest an order book imbalance strategy on Binance BTCUSDT using order book delta data for high-frequency signals.

## `KUC-117`
**Source**: `examples/backtest/databento_cme_quoter.py`

Users need to backtest a simple quoter strategy that provides liquidity on CME futures markets using Databento historical data.

## `KUC-118`
**Source**: `examples/backtest/databento_ema_cross_long_only_aapl_bars.py`

Users need to backtest a long-only EMA crossover strategy on AAPL equity bars using Databento market data.

## `KUC-119`
**Source**: `examples/backtest/databento_ema_cross_long_only_spy_trades.py`

Users need to backtest a long-only EMA crossover strategy on SPY ETF trade tick data using Databento.

## `KUC-120`
**Source**: `examples/backtest/databento_ema_cross_long_only_tsla_trades.py`

Users need to backtest a long-only EMA crossover strategy on TSLA equity trade tick data using Databento.

## `KUC-121`
**Source**: `examples/backtest/example_01_load_bars_from_custom_csv/run_example.py`

Users need to load custom bar data from CSV files into NautilusTrader for backtesting with their own historical data.

## `KUC-122`
**Source**: `examples/backtest/example_02_use_clock_timer/run_example.py`

Users need to understand how to implement timer-based logic in their strategies for scheduled actions independent of market data.

## `KUC-123`
**Source**: `examples/backtest/example_03_bar_aggregation/run_example.py`

Users need to learn how to aggregate raw tick data into different bar resolutions within their strategies.

## `KUC-124`
**Source**: `examples/backtest/example_04_using_data_catalog/run_example.py`

Users need to use the Parquet data catalog for organizing, storing, and retrieving backtest market data efficiently.

## `KUC-125`
**Source**: `examples/backtest/example_05_using_portfolio/run_example.py`

Users need to understand how to work with the portfolio module to track positions, orders, and manage multi-instrument strategies.

## `KUC-126`
**Source**: `examples/backtest/example_06_using_cache/run_example.py`

Users need to store and retrieve custom data objects in the cache for stateful strategy logic across backtest runs.

## `KUC-127`
**Source**: `examples/backtest/example_07_using_indicators/run_example.py`

Users need to learn how to use built-in technical indicators (MovingAverages, etc.) in their trading strategies.

## `KUC-128`
**Source**: `examples/backtest/example_08_cascaded_indicator/run_example.py`

Users need to implement strategies that chain indicators together, such as EMA of EMA, for more sophisticated signal generation.

## `KUC-129`
**Source**: `examples/backtest/example_09_messaging_with_msgbus/run_example.py`

Users need to implement inter-component communication using the message bus for decoupled strategy architecture.

## `KUC-130`
**Source**: `examples/backtest/example_10_messaging_with_actor_data/run_example.py`

Users need to publish and subscribe to custom data types between actors for building complex multi-component trading systems.

## `KUC-131`
**Source**: `examples/backtest/example_11_messaging_with_actor_signals/run_example.py`

Users need to use the Signal mechanism to emit and receive trading signals between actors for signal-based strategies.

## `KUC-132`
**Source**: `examples/backtest/fx_ema_cross_audusd_bars_from_ticks.py`

Users need to backtest EMA crossover on AUD/USD with rollover interest simulation, building bars from raw tick data.

## `KUC-133`
**Source**: `examples/backtest/fx_ema_cross_audusd_ticks.py`

Users need to backtest EMA crossover on AUD/USD using raw tick data with fill model and rollover interest simulation.

## `KUC-134`
**Source**: `examples/backtest/fx_ema_cross_bracket_gbpusd_bars_external.py`

Users need to backtest EMA crossover with bracket orders (profit target, stop loss) on GBP/USD using external bar data.

## `KUC-135`
**Source**: `examples/backtest/fx_ema_cross_bracket_gbpusd_bars_internal.py`

Users need to backtest EMA crossover with bracket orders on GBP/USD using internally generated bars from quote ticks.

## `KUC-136`
**Source**: `examples/backtest/fx_market_maker_gbpusd_bars.py`

Users need to backtest a volatility-based market making strategy on GBP/USD with dual-sided quotes and rollover interest.

## `KUC-137`
**Source**: `examples/backtest/model_configs_example.py`

Users need to understand how to configure backtests including venues, data sources, fee models, fill models, and latency models.

## `KUC-138`
**Source**: `examples/backtest/notebooks/databento_backtest_with_data_client.py`

Users need to integrate Databento data client with BacktestNode for streaming historical data into backtests.

## `KUC-139`
**Source**: `examples/backtest/notebooks/databento_download.py`

Users need to download and cache historical market data from Databento for offline backtesting and research.

## `KUC-140`
**Source**: `examples/backtest/notebooks/databento_futures_settlement.py`

Users need to backtest futures trading strategies that handle contract settlement and expiry correctly using Databento data.

## `KUC-141`
**Source**: `examples/backtest/notebooks/databento_option_exercise.py`

Users need to backtest options strategies including exercise and assignment mechanics using Databento market data.

## `KUC-142`
**Source**: `examples/backtest/notebooks/databento_option_greeks.py`

Users need to analyze option Greeks (delta, gamma, vega, theta) and create performance tearsheets for options strategies.

## `KUC-143`
**Source**: `examples/backtest/notebooks/databento_test_order_book_deltas.py`

Users need to test order book delta data handling from Databento for high-frequency and microstructure strategies.

## `KUC-144`
**Source**: `examples/backtest/notebooks/databento_test_request_bars.py`

Users need to request and process OHLCV bar data from Databento for backtesting bar-based strategies.

## `KUC-145`
**Source**: `examples/backtest/polymarket_simple_quoter.py`

Users need to backtest a quoter strategy on Polymarket prediction market using historical trade data from their APIs.

## `KUC-146`
**Source**: `examples/backtest/synthetic_data_pnl_test.py`

Users need to test P&L calculations and portfolio accounting using synthetic futures contract data with proper settlement.

## `KUC-147`
**Source**: `examples/live/architect_ax/ax_book_imbalance.py`

Users need to run an order book imbalance strategy live on Archax exchange for real-time crypto perpetual trading.

## `KUC-148`
**Source**: `examples/live/architect_ax/ax_data_tester.py`

Users need to test and validate market data streaming from Archax exchange before running live strategies.

## `KUC-149`
**Source**: `examples/live/architect_ax/ax_exec_tester.py`

Users need to test order execution and fill simulation on Archax exchange before running production strategies.

## `KUC-150`
**Source**: `examples/live/architect_ax/ax_mean_reversion.py`

Users need to run a Bollinger Bands mean reversion strategy live on Archax exchange for crypto perpetuals.

## `KUC-151`
**Source**: `examples/live/betfair/betfair.py`

Users need to run an order book imbalance strategy live on Betfair sports betting exchange.

## `KUC-152`
**Source**: `examples/live/binance/binance_futures_demo_exec_tester.py`

Users need to test Binance futures execution functionality including order submission and fill confirmation.

## `KUC-153`
**Source**: `examples/live/binance/binance_spot_and_futures_market_maker.py`

Users need to run a volatility market maker strategy simultaneously on Binance spot and futures markets.

## `KUC-154`
**Source**: `examples/live/binance/binance_spot_ema_cross_bracket_algo.py`

Users need to run an EMA crossover strategy with bracket orders and TWAP execution algorithm live on Binance spot.

## `KUC-155`
**Source**: `examples/live/binance/binance_spot_exec_tester.py`

Users need to test order execution functionality on Binance spot market.

## `KUC-156`
**Source**: `examples/live/bybit/bybit_ema_cross.py`

Users need to run an EMA crossover strategy live on Bybit for crypto perpetual trading.

## `KUC-157`
**Source**: `examples/live/bybit/bybit_ema_cross_bracket_algo.py`

Users need to run EMA crossover with bracket orders and TWAP execution algorithm live on Bybit.

## `KUC-158`
**Source**: `examples/live/bybit/bybit_ema_cross_stop_entry.py`

Users need to run EMA crossover strategy with stop entry orders live on Bybit.

## `KUC-159`
**Source**: `examples/live/bybit/bybit_ema_cross_with_trailing_stop.py`

Users need to run EMA crossover with trailing stop protection live on Bybit.

## `KUC-160`
**Source**: `examples/live/bybit/bybit_option_chain.py`

Users need to subscribe to option chain data from Bybit including strikes and expiry for BTC options trading.

## `KUC-161`
**Source**: `examples/live/bybit/bybit_option_greeks.py`

Users need to subscribe to live option Greeks (delta, gamma, vega, theta, IV) from Bybit for options trading.

## `KUC-162`
**Source**: `examples/live/bybit/bybit_options_data_collector.py`

Users need to collect and store historical options market data from Bybit for research and backtesting.

## `KUC-163`
**Source**: `examples/live/databento/databento_data_tester.py`

Users need to test and validate Databento live market data streaming including bars and order book data.

## `KUC-164`
**Source**: `examples/live/deribit/deribit_data_tester.py`

Users need to test market data streaming and options data from Deribit exchange for crypto options trading.

## `KUC-165`
**Source**: `examples/live/dydx/dydx_exec_tester.py`

Users need to test order execution on dYdX v4 including short-term and long-term orders with custom tags.

## `KUC-166`
**Source**: `examples/live/dydx/dydx_market_maker.py`

Users need to run a volatility market maker strategy live on dYdX v4 perpetual markets.

## `KUC-167`
**Source**: `examples/live/hyperliquid/hyperliquid_exec_tester.py`

Users need to test order execution functionality on Hyperliquid exchange for crypto perpetual trading.

## `KUC-168`
**Source**: `examples/live/interactive_brokers/connect_with_dockerized_gateway.py`

Users need to connect NautilusTrader to Interactive Brokers using a dockerized Gateway for traditional asset trading.

## `KUC-169`
**Source**: `examples/live/interactive_brokers/connect_with_tws.py`

Users need to connect NautilusTrader to Interactive Brokers via Trader Workstation (TWS) for trading.

## `KUC-170`
**Source**: `examples/live/interactive_brokers/contract_download.py`

Users need to download contract details from Interactive Brokers including futures and options instruments.

## `KUC-171`
**Source**: `examples/live/interactive_brokers/historical_download.py`

Users need to download historical market data from Interactive Brokers for backtesting and research.

## `KUC-172`
**Source**: `examples/live/interactive_brokers/notebooks/bracket_order_example.py`

Users need to understand how to place bracket orders (with profit target and stop loss) on Interactive Brokers.

## `KUC-173`
**Source**: `examples/live/interactive_brokers/notebooks/oca_group_example.py`

Users need to understand how to use One-Cancels-All (OCA) groups for order management on Interactive Brokers.
