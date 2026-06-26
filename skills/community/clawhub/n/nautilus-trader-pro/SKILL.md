---
name: nautilus-trader
version: 1.0.0
description: How to use the NautilusTrader algorithmic trading platform for data conversion, strategy development, backtesting, paper trading (sandbox), and live trading. Use this skill whenever the user wants to build or run a quantitative trading strategy with nautilus_trader, convert market data for backtesting, set up a backtest engine, run a sandbox/paper-trading session, connect to a live exchange or broker, or generate performance reports and tearsheets. Also use it when the user mentions NautilusTrader, trading strategies, backtesting frameworks, or connecting to exchanges like Binance, Bybit, Interactive Brokers, etc.
---

# NautilusTrader Skill

This skill teaches you how to use the **NautilusTrader** open-source algorithmic trading platform.
NautilusTrader is a Rust-native, high-performance trading system with Python bindings (via PyO3).
It works as both a backtesting engine and a live trading system — the same strategy code runs in
both environments with zero changes.

## Prerequisites — check before ANY task

Before doing any work, you MUST verify the environment is ready. Follow these steps in order:

### Step 1: Check if nautilus_trader exists in the workspace

Look for a `nautilus_trader/` directory in the user's workspace that contains `pyproject.toml`
and a `nautilus_trader/` Python package subdirectory. Run:

```bash
ls pyproject.toml nautilus_trader/__init__.py 2>/dev/null
```

If both files exist, the project is present — skip to Step 3.

### Step 2: Clone the repository (only if Step 1 failed)

If the project is not found in the workspace, clone it:

```bash
git clone https://github.com/nautechsystems/nautilus_trader.git
cd nautilus_trader
```

### Step 3: Check if the Python environment is set up

Check if a virtual environment exists and nautilus_trader is installed:

```bash
python -c "import nautilus_trader; print(nautilus_trader.__version__)" 2>/dev/null
```

If this succeeds, the environment is ready — proceed to the user's task.

### Step 4: Set up the environment (only if Step 3 failed)

NautilusTrader requires Python 3.12+ and the Rust toolchain. Install in this order:

#### 4a. Install system prerequisites

```bash
# macOS (Rust + clang are typically available, just ensure Rust is installed)
curl https://sh.rustup.rs -sSf | sh -s -- -y
source $HOME/.cargo/env

# Linux (Ubuntu)
curl https://sh.rustup.rs -sSf | sh -s -- -y
source $HOME/.cargo/env
sudo apt-get install -y clang
```

Verify: `rustc --version` and `clang --version`

#### 4b. Install uv (if not already available)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 4c. Install nautilus_trader

There are two installation approaches:

**Option A: Install from PyPI (recommended for users who just want to USE the framework)**

```bash
uv venv --python 3.12
source .venv/bin/activate   # Linux/macOS
uv pip install nautilus_trader
uv pip install "nautilus_trader[visualization]"  # Optional: for tearsheet reports
```

**Option B: Install from source (recommended when working inside the cloned repository)**

```bash
cd nautilus_trader
uv sync --all-extras
```

This creates a virtual environment, installs all dependencies, and builds the Cython/Rust
extensions. It takes several minutes on first build.

For faster development iteration, use:
```bash
make build-debug    # Debug build (faster compilation, slower runtime)
make install        # Release build (slower compilation, faster runtime)
```

#### 4d. Set environment variables (source builds only, Linux/macOS)

```bash
export PYO3_PYTHON=$(pwd)/.venv/bin/python

# Linux only:
export LD_LIBRARY_PATH="$(python -c 'import sys; print(sys.base_prefix)')/lib:$LD_LIBRARY_PATH"
```

#### 4e. Verify installation

```bash
python -c "import nautilus_trader; print(f'NautilusTrader {nautilus_trader.__version__} installed successfully')"
```

### Optional dependencies

| Extra | Install command | Purpose |
|---|---|---|
| Visualization | `uv pip install "nautilus_trader[visualization]"` | Plotly tearsheets and charts |
| Interactive Brokers | `uv pip install "nautilus_trader[ib]"` | IB adapter dependencies |
| Docker (for IB Gateway) | `uv pip install "nautilus_trader[docker]"` | Dockerized IB Gateway |
| Betfair | `uv pip install "nautilus_trader[betfair]"` | Betfair adapter |
| Polymarket | `uv pip install "nautilus_trader[polymarket]"` | Polymarket adapter |

## When to read which reference

Based on what the user needs, read the appropriate reference file from the `references/` directory
next to this SKILL.md. Each reference file is self-contained with code templates and explanations.

| User's goal | Reference file to read |
|---|---|
| Convert CSV/external data into Nautilus format | `references/data_conversion.md` |
| Write a trading strategy | `references/strategy_development.md` |
| Run a backtest and generate reports | `references/backtesting.md` |
| Run paper/simulated trading with real market data | `references/paper_trading.md` |
| Connect to a live exchange/broker and trade | `references/live_trading.md` |

Read **only** the reference file(s) relevant to the current task. If a task spans multiple areas
(e.g., "convert data, write a strategy, and backtest it"), read them in the order listed above.

## Project layout

```
nautilus_trader/             # Python package (v1, production)
├── adapters/                # Venue adapters (Binance, Bybit, IB, etc.)
├── backtest/                # BacktestEngine, BacktestNode
├── examples/                # Example strategies and scripts
│   ├── strategies/          # EMACross, MarketMaker, etc.
│   └── algorithms/          # TWAP execution algorithm
├── indicators/              # Technical indicators (EMA, SMA, RSI, ATR, etc.)
├── live/                    # TradingNode for live/sandbox trading
├── model/                   # Domain types: instruments, orders, events, data
├── persistence/             # Data catalog (Parquet), wranglers
├── analysis/                # Reports, tearsheets, visualization
└── trading/                 # Strategy base class

examples/                    # Runnable example scripts
├── backtest/                # Backtest examples (FX, crypto, equities)
├── data_conversion/         # Data conversion examples
├── live/                    # Live trading examples per exchange
└── sandbox/                 # Sandbox (paper trading) examples

docs/concepts/               # Concept guides (data, strategies, backtesting, etc.)
docs/integrations/           # Per-exchange integration guides
```

## Core concepts quick reference

### Data types

NautilusTrader uses these built-in market data types (in descending order of granularity):

| Type | Description |
|---|---|
| `OrderBookDelta` | Individual order book updates (L1/L2/L3) |
| `OrderBookDepth10` | Aggregated order book snapshot (up to 10 levels per side) |
| `QuoteTick` | Best bid/ask prices with sizes (top-of-book) |
| `TradeTick` | A single executed trade |
| `Bar` | OHLCV candle aggregated by time, tick, volume, etc. |

### Instrument types

| Type | Use case |
|---|---|
| `CurrencyPair` | Forex, crypto spot (e.g., EUR/USD, BTC/USDT) |
| `CryptoPerpetual` | Crypto perpetual futures (e.g., BTCUSDT-PERP) |
| `Equity` | Stocks (e.g., AAPL, TSLA) |
| `FuturesContract` | Traditional futures (e.g., ES, IF) |
| `OptionContract` | Options |
| `Cfd` | CFDs |

### BarType string syntax

Standard format: `{instrument_id}-{step}-{aggregation}-{price_type}-{source}`

Examples:
```
EUR/USD.SIM-1-MINUTE-BID-INTERNAL        # 1-min bars from bid quotes, aggregated internally
BTCUSDT-PERP.BINANCE-5-MINUTE-LAST-EXTERNAL  # 5-min bars from exchange
AAPL.XNAS-1-HOUR-LAST-INTERNAL           # 1-hour bars aggregated internally from trades
```

- Price types: `BID`, `ASK`, `MID` (from QuoteTick), `LAST` (from TradeTick)
- Sources: `INTERNAL` (Nautilus aggregates), `EXTERNAL` (exchange/provider provides)

### Key identifiers

- `InstrumentId`: e.g., `"EUR/USD.SIM"`, `"ETHUSDT-PERP.BINANCE"`, `"AAPL.XNAS"`
- `Venue`: e.g., `"SIM"`, `"BINANCE"`, `"INTERACTIVE_BROKERS"`
- `TraderId`: e.g., `"TRADER-001"`
- `StrategyId`: auto-generated as `{ClassName}-{order_id_tag}`

### Environment contexts

NautilusTrader has three operating modes:

| Mode | Data source | Execution | Use case |
|---|---|---|---|
| **Backtest** | Historical data files | Simulated exchange | Strategy research |
| **Sandbox** | Live market feeds | Simulated locally | Paper trading |
| **Live** | Live market feeds | Real exchange | Production trading |

The **same strategy code** runs in all three modes.

### Installation

```bash
pip install nautilus_trader

# With visualization support (Plotly tearsheets)
pip install "nautilus_trader[visualization]"
```

For development in this repository:
```bash
make install          # Release build
make build-debug      # Debug build (faster compilation)
```

## Important conventions

- **Timestamps** are UNIX nanoseconds (`ts_event`, `ts_init`)
- **Prices** use fixed-point arithmetic (`Price`, `Quantity` types) — never raw floats
- **All imports** come from the `nautilus_trader` package
- **Strategy code is identical** across backtest, sandbox, and live — only the engine config changes
- **Do not block the event loop** — strategy callbacks must return quickly
- **One TradingNode per process** — use separate processes for parallel live nodes

## Key source files for reference

When writing code, these files in the repository are the most useful references:

| Purpose | Path |
|---|---|
| EMA Cross strategy (simplest example) | `nautilus_trader/examples/strategies/ema_cross.py` |
| Quickstart backtest | `docs/getting_started/quickstart.py` |
| Loading external CSV data | `docs/how_to/loading_external_data.py` |
| Backtest with ticks | `examples/backtest/fx_ema_cross_audusd_ticks.py` |
| Bar-based backtest | `examples/backtest/fx_ema_cross_bracket_gbpusd_bars_external.py` |
| Sandbox example | `examples/sandbox/binance_futures_testnet_sandbox.py` |
| Live trading example | `examples/live/binance/binance_spot_ema_cross_bracket_algo.py` |
| Data conversion (CN futures) | `examples/data_conversion/if_data_converter.py` |
| Strategy concepts doc | `docs/concepts/strategies.md` |
| Data concepts doc | `docs/concepts/data.md` |
| Backtesting concepts doc | `docs/concepts/backtesting.md` |
| Live trading concepts doc | `docs/concepts/live.md` |
| Reports & analysis doc | `docs/concepts/reports.md` |
| Visualization doc | `docs/concepts/visualization.md` |
| Integration guides (per exchange) | `docs/integrations/*.md` |

## Typical end-to-end workflow

1. **Prepare data** → Read `references/data_conversion.md`
   - Load raw CSV/API data → DataFrame → DataWrangler → Nautilus objects
   - Optionally persist to ParquetDataCatalog

2. **Write strategy** → Read `references/strategy_development.md`
   - Create `StrategyConfig` + `Strategy` subclass
   - Implement `on_start`, `on_bar`/`on_quote_tick`, `on_stop`

3. **Backtest** → Read `references/backtesting.md`
   - Configure `BacktestEngine` or `BacktestNode`
   - Run and generate reports/tearsheets

4. **Paper trade** → Read `references/paper_trading.md`
   - Configure `TradingNode` with Sandbox execution client
   - Use live data feeds with simulated order execution

5. **Go live** → Read `references/live_trading.md`
   - Switch execution client from Sandbox to real exchange adapter
   - Configure reconciliation, risk management
