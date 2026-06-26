#!/usr/bin/env bash
# Judgment Enhancement Engine - One-click Setup
# Platforms: Linux / macOS / Windows (Git Bash / WSL)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_PY="$DIR/engine.py"

echo "=== Judgment Enhancement Engine Setup ==="

# 1. Check Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[ERROR] Python not found. Please install Python 3.8+"
    exit 1
fi

echo "[1/3] Python version: $($PYTHON --version 2>&1)"

# 2. Verify engine
echo "[2/3] Verifying engine..."
cd "$DIR"
$PYTHON -c "
import sys
sys.path.insert(0, '.')
from engine import JudgmentEnhancementEngine

class WM:
    def get_possible_outcomes(self, s, a):
        return [('next', 1.0, 1)]
    def is_terminal(self, s):
        return s == 'done'
    def get_legal_actions(self, s):
        return ['go']

class OF:
    def evaluate(self, s):
        return 1.0

e = JudgmentEnhancementEngine(WM(), OF(), lookahead_depth=1)
r = e.enhance_judgment('start')
assert r.best_action is not None, 'Judgment not working'
print(f'Engine verified OK - action={r.best_action} confidence={r.confidence:.2f}')
"

# 3. Run built-in demo
echo "[3/3] Running built-in demo..."
$PYTHON "$ENGINE_PY"

echo ""
echo "=== Setup Complete ==="
echo "Quick start:  python \"$ENGINE_PY\""
echo "API mode:     from engine import JudgmentEnhancementEngine"
