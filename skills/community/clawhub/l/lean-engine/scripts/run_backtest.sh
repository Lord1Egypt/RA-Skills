#!/bin/bash
# run_backtest.sh — Configure and run a LEAN backtest
#
# Usage:
#   ./run_backtest.sh <AlgoClassName> <AlgoFile.py>
#   ./run_backtest.sh SecondWavePortfolio SecondWavePortfolio.py
#
# Requires: LEAN_ROOT env var pointing to cloned LEAN repository
# The .py file must exist in $LEAN_ROOT/Algorithm.Python/
# Results go to $LEAN_ROOT/Results/
#
# SAFETY: This script does NOT modify your original config.json.
# It creates a temporary config copy (config.backtest.json) for each run.
# Your original config (including any IB credentials) is never touched.

set -e

ALGO_CLASS="${1:?Usage: $0 <AlgoClassName> <AlgoFile.py>}"
ALGO_FILE="${2:?Usage: $0 <AlgoClassName> <AlgoFile.py>}"

: "${LEAN_ROOT:?Error: LEAN_ROOT not set. Export it to your LEAN repository path.}"

ALGO_DIR="$LEAN_ROOT/Algorithm.Python"
LAUNCHER="$LEAN_ROOT/Launcher/bin/Debug"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Locate source config (read-only — never modified)
if [ -f "$LAUNCHER/config.json" ]; then
    SOURCE_CONFIG="$LAUNCHER/config.json"
else
    SOURCE_CONFIG="$LEAN_ROOT/Launcher/config.json"
fi

# Output config is a separate file — original is never touched
BACKTEST_CONFIG="$LAUNCHER/config.backtest.json"

# Ensure dotnet is in PATH
export PATH="$PATH:${DOTNET_ROOT:-$HOME/.dotnet}"

# LEAN's pythonnet requires the Python shared library path
if [ -z "$PYTHONNET_PYDLL" ]; then
    if [ -f "$LEAN_ROOT/.libs/libpython3.11.so.1.0" ]; then
        export PYTHONNET_PYDLL="$LEAN_ROOT/.libs/libpython3.11.so.1.0"
    else
        echo "⚠️  PYTHONNET_PYDLL not set. LEAN may fail to load Python algorithms."
        echo "   Set it to your Python shared library, e.g.:"
        echo "   export PYTHONNET_PYDLL=\"\$LEAN_ROOT/.libs/libpython3.11.so.1.0\""
    fi
fi

# Verify algorithm file exists
if [ ! -f "$ALGO_DIR/$ALGO_FILE" ]; then
    echo "❌ Algorithm not found: $ALGO_DIR/$ALGO_FILE"
    echo "   Place your .py file there first."
    exit 1
fi

# Verify LEAN is built
if [ ! -f "$LAUNCHER/QuantConnect.Lean.Launcher.dll" ]; then
    echo "❌ LEAN not built. Run: cd $LEAN_ROOT && dotnet build QuantConnect.Lean.sln -c Debug"
    exit 1
fi

# Create backtest config from source (source is NOT modified)
python3 "$SCRIPT_DIR/configure_algo.py" "$SOURCE_CONFIG" "$BACKTEST_CONFIG" "$ALGO_CLASS" "$ALGO_FILE"

# Temporarily swap config for the run, then restore
# LEAN reads config.json from its working directory
cp "$SOURCE_CONFIG" "$SOURCE_CONFIG.pre-backtest"
cp "$BACKTEST_CONFIG" "$SOURCE_CONFIG"

cleanup() {
    # Restore original config after run
    if [ -f "$SOURCE_CONFIG.pre-backtest" ]; then
        cp "$SOURCE_CONFIG.pre-backtest" "$SOURCE_CONFIG"
        rm -f "$SOURCE_CONFIG.pre-backtest"
    fi
}
trap cleanup EXIT

# Run the backtest
echo ""
echo "🚀 Starting LEAN backtest..."
echo "═══════════════════════════════════════════"
cd "$LAUNCHER"
dotnet QuantConnect.Lean.Launcher.dll

echo ""
echo "═══════════════════════════════════════════"
echo "✅ Backtest complete. Results:"
ls -la "$LEAN_ROOT/Results/" 2>/dev/null || echo "   (check $LAUNCHER for output)"
