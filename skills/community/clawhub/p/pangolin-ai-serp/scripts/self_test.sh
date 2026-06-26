#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PANGOLIN="$SCRIPT_DIR/pangolin.py"

# Cross-platform Python detection
# On Windows, python3 may exist but exit non-zero; test with --version
if python3 --version &>/dev/null 2>&1; then
  PYTHON="python3"
else
  PYTHON="python"
fi

echo "=== Pangolinfo AI SERP Self-Test ==="

# Test 1: Auth check
echo "[1/2] Testing authentication..."
if $PYTHON "$PANGOLIN" --auth-only; then
  echo "  PASS: Auth OK"
else
  echo "  FAIL: Auth failed (exit code $?)"
  exit 1
fi

# Test 2: Minimal SERP query
echo "[2/2] Testing SERP query..."
if $PYTHON "$PANGOLIN" --q "openclaw" --mode serp 2>/dev/null | $PYTHON -c "import sys,json; d=json.load(sys.stdin); assert d.get('success')==True; print(f'  PASS: Got {d.get(\"results_num\",0)} results')"; then
  :
else
  echo "  FAIL: SERP query failed"
  exit 2
fi

# Error path tests
echo "[E1] Testing missing query error..."
if $PYTHON "$PANGOLIN" 2>/dev/null; then
  echo "  FAIL: Should have errored on missing --q"
  exit 10
else
  echo "  PASS: Correctly rejected missing query"
fi

echo "=== All tests passed ==="
