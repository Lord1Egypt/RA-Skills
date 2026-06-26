---
name: lean
description: Run QuantConnect LEAN backtests and manage US equity algorithm development. Use when asked to backtest a trading strategy, run a LEAN algorithm, analyze backtest results, download market data, or deploy to Interactive Brokers TWS. Covers algorithm creation, data management, config editing, and result analysis.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["dotnet"], "anyBins": ["python3", "python"], "env": ["LEAN_ROOT", "DOTNET_ROOT", "PYTHONNET_PYDLL"] },
        "install":
          [
            {
              "id": "dotnet",
              "kind": "download",
              "url": "https://dotnet.microsoft.com/download/dotnet/8.0",
              "label": "Install .NET 8 SDK"
            }
          ]
      }
  }
---

# LEAN Engine — QuantConnect Algorithmic Trading

## Prerequisites & Setup

### Required Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `LEAN_ROOT` | Path to cloned LEAN repository | `/home/user/lean` |
| `DOTNET_ROOT` | Path to .NET SDK installation | `/home/user/.dotnet` |
| `PYTHONNET_PYDLL` | Path to Python shared library (required by LEAN's pythonnet) | `$LEAN_ROOT/.libs/libpython3.11.so.1.0` |

All three must be set before using this skill. Add to your shell profile:
```bash
export LEAN_ROOT="$HOME/lean"
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$PATH:$DOTNET_ROOT"
export PYTHONNET_PYDLL="$LEAN_ROOT/.libs/libpython3.11.so.1.0"
```

> **Note:** LEAN bundles its own Python shared library in `$LEAN_ROOT/.libs/`. If you built LEAN from source, the library should be there after `dotnet build`. If not, install `libpython3.11-dev` and point `PYTHONNET_PYDLL` to your system's `libpython3.11.so`.

### First-Time Setup

1. **Install .NET 8 SDK:**
   ```bash
   # Linux/macOS
   wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
   chmod +x dotnet-install.sh
   ./dotnet-install.sh --channel 8.0
   export DOTNET_ROOT="$HOME/.dotnet"
   export PATH="$PATH:$DOTNET_ROOT"
   ```

2. **Clone and build LEAN:**
   ```bash
   git clone https://github.com/QuantConnect/Lean.git "$LEAN_ROOT"
   cd "$LEAN_ROOT"
   dotnet build QuantConnect.Lean.sln -c Debug
   ```

3. **Download initial market data:**
   ```bash
   pip install yfinance pandas
   python3 {baseDir}/scripts/download_us_universe.py --symbols sp500 --start 2020-01-01 --data-dir "$LEAN_ROOT/Data"
   ```

4. **Verify setup:**
   ```bash
   ls "$LEAN_ROOT/Data/equity/usa/daily/"  # Should list .zip files
   ls "$LEAN_ROOT/Launcher/bin/Debug/"      # Should contain QuantConnect.Lean.Launcher.dll
   ```

## Environment

- **LEAN source:** `$LEAN_ROOT/`
- **Launcher (pre-built):** `$LEAN_ROOT/Launcher/bin/Debug/`
- **Config:** `$LEAN_ROOT/Launcher/config.json`
- **Python algos:** `$LEAN_ROOT/Algorithm.Python/`
- **Market data:** `$LEAN_ROOT/Data/`
- **dotnet:** `$DOTNET_ROOT/dotnet` (add to PATH: `export PATH="$PATH:$DOTNET_ROOT"`)

## Quick Reference

### Run a Backtest

1. Place algorithm in `$LEAN_ROOT/Algorithm.Python/YourAlgo.py`
2. Edit config to point to it:
   ```bash
   # Update config.json — set these fields:
   # "algorithm-type-name": "YourClassName"
   # "algorithm-language": "Python"
   # "algorithm-location": "../../../Algorithm.Python/YourAlgo.py"
   ```
3. Run:
   ```bash
   export PATH="$PATH:$DOTNET_ROOT"
   cd "$LEAN_ROOT/Launcher/bin/Debug"
   dotnet QuantConnect.Lean.Launcher.dll
   ```
4. Results appear in stdout + `$LEAN_ROOT/Results/`

**Or use the helper script:**
```bash
bash {baseDir}/scripts/run_backtest.sh YourClassName YourAlgo.py
```

### Config Editing

Edit `$LEAN_ROOT/Launcher/config.json` with these key fields:

| Field | Purpose | Example |
|-------|---------|---------|
| `algorithm-type-name` | Python class name | `"MyStrategy"` |
| `algorithm-language` | Language | `"Python"` |
| `algorithm-location` | Path to .py file | `"../../../Algorithm.Python/MyStrategy.py"` |
| `data-folder` | Market data path | `"../Data/"` |
| `environment` | Mode | `"backtesting"` or `"live-interactive"` |

For IB live trading, set environment to `"live-interactive"` and configure the
`ib-*` fields (account, username, password, host, port, trading-mode).

### Data Management

**Check available data:**
```bash
ls "$LEAN_ROOT/Data/equity/usa/daily/"
```

**Data format:** ZIP files containing CSV. Each line:
`YYYYMMDD HH:MM,Open*10000,High*10000,Low*10000,Close*10000,Volume`

Prices are stored as integers (multiply by 10000). LEAN handles conversion internally.

**Download more data:**
```bash
python3 {baseDir}/scripts/download_us_universe.py --symbols sp500 --data-dir "$LEAN_ROOT/Data"
```

See `{baseDir}/references/data-download.md` for additional methods to expand the universe.

### Writing Algorithms

LEAN Python algorithms inherit from `QCAlgorithm`:

```python
from AlgorithmImports import *

class MyAlgo(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2024, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100_000)
        self.AddEquity("SPY", Resolution.Daily)
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage,
                               AccountType.Margin)

    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.SetHoldings("SPY", 1.0)
```

Key API patterns:
- `self.History(symbol, periods, resolution)` — get historical bars
- `self.SetHoldings(symbol, weight)` — target portfolio weight
- `self.Liquidate(symbol)` — close position
- `self.AddUniverse(coarse_fn, fine_fn)` — dynamic universe selection
- `self.Schedule.On(date_rule, time_rule, action)` — scheduled events
- `self.Debug(msg)` — log output

### Analyzing Results

After a backtest run, check:
```bash
ls "$LEAN_ROOT/Results/"
# Key files: *-log.txt, *-order-log.txt, *.json (statistics)
```

### Rebuild LEAN (if source changes)

```bash
export PATH="$PATH:$DOTNET_ROOT"
cd "$LEAN_ROOT"
dotnet build QuantConnect.Lean.sln -c Debug
```

## Security Notes

### Config.json Safety
The `run_backtest.sh` script does **NOT** modify your original `config.json`. Instead, it:
1. Reads the original config as a template (read-only)
2. Creates a separate `config.backtest.json` with only algorithm fields changed (class name, file path, language, environment=backtesting)
3. Temporarily swaps it in for the LEAN run, then restores the original via a `trap` cleanup handler

The `configure_algo.py` helper performs the field substitution in an isolated output file. Your original config — including any Interactive Brokers credentials for live trading — is never modified.

**Modified fields (in the temp copy only):**
- `algorithm-type-name` — set to the requested class name
- `algorithm-language` — set to `Python`
- `algorithm-location` — set to the requested .py file path
- `environment` — set to `backtesting`

### Network Access
The setup instructions involve network downloads:
- `git clone` from GitHub (QuantConnect/Lean repository)
- `dotnet build` may restore NuGet packages
- `pip install yfinance pandas` installs Python packages from PyPI
- `download_us_universe.py` fetches market data from Yahoo Finance

All downloads are from well-known public sources. For maximum isolation, run setup in a container or VM.

### Environment Variables
This skill requires the following environment variables at runtime:
- `LEAN_ROOT` — path to your cloned LEAN repository
- `DOTNET_ROOT` — path to your .NET SDK installation
- `PYTHONNET_PYDLL` — path to Python shared library (auto-detected from `$LEAN_ROOT/.libs/` if not set)

These are declared in the skill metadata and must be set before use.

## Troubleshooting

- **"No data files found"** → Check `data-folder` in config.json points to correct path
- **Python import errors** → LEAN bundles its own Python; check `python-venv` config if using custom packages
- **Slow backtest** → Reduce universe size or date range; check Resolution (Minute >> Daily)
- **IB connection issues** → Verify TWS/Gateway is running, port matches config (default 4002 for Gateway)
- **`LEAN_ROOT` not set** → Add `export LEAN_ROOT="$HOME/lean"` to your shell profile
- **dotnet not found** → Add `export PATH="$PATH:$DOTNET_ROOT"` to your shell profile
- **`Runtime.PythonDLL was not set`** → Set `PYTHONNET_PYDLL` to the Python shared library path (see env var table above)
