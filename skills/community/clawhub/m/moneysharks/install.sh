#!/usr/bin/env bash
# MoneySharks install / setup verification script.
# Run once after cloning / installing the skill.
# Does NOT start trading — run onboarding.py for that.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
LOGS_DIR="$SCRIPT_DIR/logs"
PYTHON="${PYTHON:-python3}"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   🦈  MoneySharks — Install & Verification      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Python version check ──
echo "── Checking Python version ─────────────────────────"
PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
  echo "  ✗ Python 3.10+ required (found: $PYTHON_VERSION)"
  echo "    Install from https://python.org or via your package manager."
  exit 1
fi
echo "  ✓ Python $PYTHON_VERSION"

# ── Standard library only (no pip install needed) ──
echo ""
echo "── Checking required stdlib modules ────────────────"
REQUIRED_MODULES="json os sys pathlib subprocess hashlib hmac urllib.request urllib.parse urllib.error time datetime math"
ALL_OK=1
for mod in $REQUIRED_MODULES; do
  if "$PYTHON" -c "import $mod" 2>/dev/null; then
    : # ok
  else
    echo "  ✗ Missing module: $mod"
    ALL_OK=0
  fi
done
if [ "$ALL_OK" -eq 1 ]; then
  echo "  ✓ All required modules available (stdlib only — no pip install needed)"
fi

# ── Create required directories ──
echo ""
echo "── Creating directories ─────────────────────────────"
mkdir -p "$LOGS_DIR"
echo "  ✓ logs/"

# ── Validate scripts are executable ──
echo ""
echo "── Validating scripts ───────────────────────────────"
SCRIPTS=(
  autonomous_runner.py
  trade_loop.py
  market_scan_from_aster.py
  compute_features.py
  compute_signal.py
  compute_confluence.py
  recommend_leverage.py
  size_position.py
  risk_checks.py
  live_execution_adapter.py
  aster_readonly_client.py
  fetch_trade_outcomes.py
  review_trades.py
  update_metrics.py
  journal_trade.py
  validate_config.py
  reconcile_state.py
  halt.py
  resume.py
  status.py
  onboarding.py
)
MISSING=0
for script in "${SCRIPTS[@]}"; do
  if [ -f "$SCRIPTS_DIR/$script" ]; then
    chmod +x "$SCRIPTS_DIR/$script" 2>/dev/null || true
    echo "  ✓ scripts/$script"
  else
    echo "  ✗ scripts/$script  ← MISSING"
    MISSING=$((MISSING+1))
  fi
done
if [ "$MISSING" -gt 0 ]; then
  echo ""
  echo "  ✗ $MISSING script(s) missing. Reinstall the skill."
  exit 1
fi

# ── Quick syntax check ──
echo ""
echo "── Syntax check (py_compile) ────────────────────────"
SYNTAX_ERRORS=0
for script in "${SCRIPTS[@]}"; do
  if ! "$PYTHON" -m py_compile "$SCRIPTS_DIR/$script" 2>/dev/null; then
    echo "  ✗ Syntax error in: scripts/$script"
    SYNTAX_ERRORS=$((SYNTAX_ERRORS+1))
  fi
done
if [ "$SYNTAX_ERRORS" -eq 0 ]; then
  echo "  ✓ All scripts pass syntax check"
else
  echo "  ✗ $SYNTAX_ERRORS syntax error(s) found"
  exit 1
fi

# ── Check example config ──
echo ""
echo "── Config check ─────────────────────────────────────"
if [ -f "$SCRIPT_DIR/config.json" ]; then
  VALIDATION=$("$PYTHON" "$SCRIPTS_DIR/validate_config.py" < "$SCRIPT_DIR/config.json" 2>/dev/null || echo '{"ok":false}')
  V_OK=$(echo "$VALIDATION" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print('yes' if d.get('ok') else 'no')" 2>/dev/null || echo "no")
  if [ "$V_OK" = "yes" ]; then
    echo "  ✓ config.json validates OK"
  else
    echo "  ⚠ config.json has validation issues (run onboarding.py to reconfigure)"
  fi
  ERRORS=$(echo "$VALIDATION" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); [print('    -',e) for e in d.get('errors',[])]" 2>/dev/null)
  [ -n "$ERRORS" ] && echo "$ERRORS"
  WARNINGS=$(echo "$VALIDATION" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); [print('    ⚠',w) for w in d.get('warnings',[])]" 2>/dev/null)
  [ -n "$WARNINGS" ] && echo "$WARNINGS"
else
  echo "  ℹ config.json not found — run onboarding.py to create it:"
  echo "    python3 scripts/onboarding.py"
fi

# ── Check credentials ──
echo ""
echo "── Credentials ──────────────────────────────────────"
if [ -n "${ASTER_API_KEY:-}" ] && [ -n "${ASTER_API_SECRET:-}" ]; then
  KEY_MASKED="****${ASTER_API_KEY: -4}"
  echo "  ✓ ASTER_API_KEY is set ($KEY_MASKED)"
  echo "  ✓ ASTER_API_SECRET is set"
else
  echo "  ⚠ ASTER_API_KEY / ASTER_API_SECRET not set in environment."
  echo "    Add to your ~/.zshrc or ~/.bashrc:"
  echo '    export ASTER_API_KEY="your-key-here"'
  echo '    export ASTER_API_SECRET="your-secret-here"'
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅  Installation verified."
echo ""
echo "  Next steps:"
echo ""
echo "  1. Run onboarding to configure and start trading:"
echo "     python3 scripts/onboarding.py"
echo ""
echo "  2. Check status at any time:"
echo "     python3 scripts/status.py config.json"
echo ""
echo "  3. Emergency halt:"
echo "     python3 scripts/halt.py config.json --cancel-orders"
echo ""
echo "  Full docs: see SKILL.md and references/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
