#!/usr/bin/env bash
# Polymarket MR-V4 Deployment Verification Script
# Usage: bash verify.sh
set -o pipefail

BASE="/Users/0xbobby/.openclaw/workspace/polymarket-arb"
PASS=0
FAIL=0
WARN=0

pass() { echo "✅ PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "❌ FAIL: $1"; FAIL=$((FAIL+1)); }
warn() { echo "⚠️ WARN: $1"; WARN=$((WARN+1)); }

echo "═══════════════════════════════════════════"
echo "  Polymarket MR-V4 Deployment Verification"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════"
echo ""

# ── 1. Process Count ──
TRADER_PIDS=$(ps aux | grep '[t]rader.py' | grep -v grep | awk '{print $2}' | tr '\n' ' ')
TRADER_COUNT=$(echo $TRADER_PIDS | wc -w | tr -d ' ')

# Expected: 2 (V4 LIVE + V4-90s SIM). Update this when adding/removing strategies.
EXPECTED_TRADERS=2
if [ "$TRADER_COUNT" -eq "$EXPECTED_TRADERS" ]; then
  pass "Process count — $TRADER_COUNT traders (expected $EXPECTED_TRADERS)"
elif [ "$TRADER_COUNT" -gt "$EXPECTED_TRADERS" ]; then
  fail "Process count — $TRADER_COUNT traders (expected $EXPECTED_TRADERS, TOO MANY!)"
else
  fail "Process count — $TRADER_COUNT traders (expected $EXPECTED_TRADERS, MISSING)"
fi

# ── 2. No Duplicate Processes ──
DUPES=0
for PID in $TRADER_PIDS; do
  CWD=$(lsof -p "$PID" 2>/dev/null | grep cwd | awk '{print $NF}')
  echo "  → PID $PID in $(basename "$CWD")"
done

# Check V4 LIVE count
V4_COUNT=0
for PID in $TRADER_PIDS; do
  CWD=$(lsof -p "$PID" 2>/dev/null | grep cwd | awk '{print $NF}')
  [ "$(basename "$CWD")" = "mr-v4-cli" ] && V4_COUNT=$((V4_COUNT+1))
done
if [ "$V4_COUNT" -gt 1 ]; then
  fail "Duplicate check — V4 LIVE has $V4_COUNT processes!"
  DUPES=1
fi

[ "$DUPES" -eq 0 ] && pass "Duplicate check — no duplicate V4 LIVE processes"

# ── 3. V4 Flock Protection ──
LOCK_FILE="$BASE/mr-v4-cli/trader.lock"
if [ -f "$LOCK_FILE" ]; then
  if command -v flock &>/dev/null; then
    if flock -n "$LOCK_FILE" echo "unlocked" 2>/dev/null; then
      fail "V4 flock — lock file exists but NOT held"
    else
      pass "V4 flock — lock held by running process"
    fi
  else
    # macOS fallback: check with python
    FLOCK_STATUS=$(python3 -c "
import fcntl
f = open('$LOCK_FILE', 'w')
try:
  fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
  print('UNLOCKED')
  fcntl.flock(f.fileno(), fcntl.LOCK_UN)
except BlockingIOError:
  print('LOCKED')
" 2>/dev/null)
    if [ "$FLOCK_STATUS" = "LOCKED" ]; then
      pass "V4 flock — lock held by running process"
    else
      fail "V4 flock — lock NOT held"
    fi
  fi
else
  warn "V4 flock — no lock file found"
fi

# ── 4. Config Validation ──
CONFIG="$BASE/mr-v4-cli/config.json"
if [ -f "$CONFIG" ]; then
  CONFIG_RESULT=$(python3 -c "
import json
c = json.load(open('$CONFIG'))
s = c.get('strategy', {})
errors = []
checks = [
  ('dry_run', c.get('dry_run'), False),
  ('max_entries_per_slot', s.get('max_entries_per_slot'), 3),
  ('hedge_size_usd', s.get('hedge_size_usd', 0), 0),  # hedge currently disabled
  ('position_size_usd', s.get('position_size_usd'), 5.0),
  ('entry_threshold', s.get('entry_threshold'), 0.7),
  ('second_entry_delay', s.get('second_entry_delay'), 60),
]
for name, actual, expected in checks:
  if actual != expected:
    errors.append(f'{name}: got {actual}, expected {expected}')
if errors:
  print('FAIL|' + '; '.join(errors))
else:
  print('OK|dry_run=false, max_entries=3, hedge=$1, size=$5, threshold=70%, delay=60s')
" 2>&1)
  if [[ "$CONFIG_RESULT" == OK* ]]; then
    pass "Config — ${CONFIG_RESULT#OK|}"
  else
    fail "Config — ${CONFIG_RESULT#FAIL|}"
  fi
else
  fail "Config — config.json not found"
fi

# ── 5. Trade Activity ──
TRADES_FILE="$BASE/mr-v4-cli/logs/trades.jsonl"
if [ -f "$TRADES_FILE" ] && [ -s "$TRADES_FILE" ]; then
  TWO_HOURS_AGO=$(date -v-2H +%s 2>/dev/null || date -d '2 hours ago' +%s 2>/dev/null || echo 0)
  LAST_MOD=$(stat -f %m "$TRADES_FILE" 2>/dev/null || stat -c %Y "$TRADES_FILE" 2>/dev/null || echo 0)
  TRADE_COUNT=$(wc -l < "$TRADES_FILE" | tr -d ' ')
  if [ "$LAST_MOD" -gt "$TWO_HOURS_AGO" ]; then
    pass "Trade activity — $TRADE_COUNT trades, updated within 2h"
  else
    warn "Trade activity — $TRADE_COUNT trades, but not updated in 2+ hours"
  fi
else
  warn "Trade activity — trades.jsonl empty or missing (may be freshly cleared)"
fi

# ── 6. Sim-Trader Isolation ──
SIM_OK=true
for PID in $TRADER_PIDS; do
  CMD=$(ps -o command= -p "$PID" 2>/dev/null || true)
  CWD=$(lsof -p "$PID" 2>/dev/null | grep cwd | awk '{print $NF}')
  DIR_NAME=$(basename "$CWD" 2>/dev/null || echo "unknown")

  if echo "$CMD" | grep -q "\-\-config"; then
    # Sim trader
    if [ "$DIR_NAME" != "sim-trader" ]; then
      fail "Sim isolation — PID $PID (sim) in $DIR_NAME, should be sim-trader"
      SIM_OK=false
    fi
  else
    # V4 LIVE
    if [ "$DIR_NAME" != "mr-v4-cli" ]; then
      fail "Sim isolation — PID $PID (V4 LIVE) in $DIR_NAME, should be mr-v4-cli"
      SIM_OK=false
    fi
  fi
done
$SIM_OK && pass "Sim isolation — correct directories"

# ── 7. Data Collector ──
DC_PID=$(cat "$BASE/data-collector/collector.pid" 2>/dev/null || echo "")
if [ -n "$DC_PID" ] && kill -0 "$DC_PID" 2>/dev/null; then
  pass "Data collector — PID $DC_PID alive"
else
  fail "Data collector — not running"
fi

# ── 8. PGID Independence ──
PGID_OK=true
for PID in $TRADER_PIDS; do
  PGID=$(ps -o pgid= -p "$PID" 2>/dev/null | tr -d ' ')
  if [ -n "$PGID" ] && [ "$PGID" != "$PID" ]; then
    warn "PGID — PID $PID has PGID $PGID (not independent)"
    PGID_OK=false
  fi
done
$PGID_OK && pass "PGID — all traders have independent process groups"

# ── Summary ──
TOTAL=$((PASS + FAIL + WARN))
echo ""
echo "═══════════════════════════════════════════"
echo "  Summary: $PASS passed | $FAIL failed | $WARN warnings"
if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
  echo "  Status: 🟢 ALL CLEAR"
elif [ "$FAIL" -eq 0 ]; then
  echo "  Status: 🟡 WARNINGS ONLY"
else
  echo "  Status: 🔴 ISSUES FOUND"
fi
echo "═══════════════════════════════════════════"

exit $FAIL
