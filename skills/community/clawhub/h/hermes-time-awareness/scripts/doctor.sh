#!/usr/bin/env bash
# Health check for hermes-time-awareness plugin.
# Usage: bash scripts/doctor.sh
set -euo pipefail

echo "hermes-time-awareness doctor"
echo ""

ERRORS=0

# 1. Check Python
if command -v python3 >/dev/null 2>&1; then
  PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
  PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
  if [[ "$PY_MAJOR" -ge 3 && "$PY_MINOR" -ge 9 ]]; then
    echo "  ✓ Python $PY_VER"
  else
    echo "  ✗ Python $PY_VER (need 3.9+)"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "  ✗ Python 3 not found"
  ERRORS=$((ERRORS + 1))
fi

# 2. Check plugin directory
PLUGIN_DIR="$HOME/.hermes/plugins/hermes-time-awareness"
if [[ -d "$PLUGIN_DIR" ]]; then
  echo "  ✓ Plugin directory exists"
else
  echo "  ✗ Plugin directory missing: $PLUGIN_DIR"
  ERRORS=$((ERRORS + 1))
fi

# 3. Check plugin files
for f in plugin.yaml __init__.py hooks.py time_awareness/time_context.py; do
  if [[ -f "$PLUGIN_DIR/$f" ]]; then
    echo "  ✓ $f"
  else
    echo "  ✗ $f missing"
    ERRORS=$((ERRORS + 1))
  fi
done

# 4. Check Hermes plugin registration
if command -v hermes >/dev/null 2>&1; then
  if hermes plugins list 2>/dev/null | grep -q "hermes-time-awareness.*enabled"; then
    echo "  ✓ Plugin enabled in Hermes"
  else
    echo "  ⚠ Plugin not enabled — run: hermes plugins enable hermes-time-awareness"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "  ⚠ hermes CLI not found — skipping registration check"
fi

# 5. Test time context output
OUTPUT=$(python3 -c "from time_awareness.time_context import format_time_context; print(format_time_context())" 2>/dev/null)
if [[ "$OUTPUT" == *"[time:"* ]]; then
  echo "  ✓ Time context: $OUTPUT"
else
  echo "  ✗ Time context not working"
  ERRORS=$((ERRORS + 1))
fi

# 6. Run unit tests
echo ""
echo "Running tests..."
cd "$PLUGIN_DIR"
if python3 -m pytest tests/ -q --tb=no 2>/dev/null; then
  echo "  ✓ All tests passed"
else
  echo "  ✗ Some tests failed"
  ERRORS=$((ERRORS + 1))
fi

echo ""
if [[ "$ERRORS" -eq 0 ]]; then
  echo "✓ All checks passed. Restart Hermes to activate:"
  echo "  hermes gateway restart"
else
  echo "✗ $ERRORS issue(s) found. Fix them and re-run: bash scripts/doctor.sh"
  exit 1
fi
