#!/bin/bash
# openclaw-doctor diagnose.sh v1.0.0
# Comprehensive OpenClaw health diagnostics
# Works on macOS and Linux
set -uo pipefail

MODE="full"
FIX=false
for arg in "$@"; do
  case "$arg" in
    --fix) FIX=true ;;
    --quick) MODE="quick" ;;
  esac
done

PASS=0; FAIL=0; WARN=0; FIXED=0
OS=$(uname -s)
SYSCTL="/usr/sbin/sysctl"
[ "$OS" = "Linux" ] && SYSCTL="sysctl"
OC_HOME="${HOME}/.openclaw"
OC_WORKSPACE="${OC_HOME}/workspace"
OC_LOGS="${OC_HOME}/logs"
GW_PORT=18789

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
BLUE='\033[0;34m'; NC='\033[0m'

pass() { echo -e "  ${GREEN}✅${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}❌${NC} $1"; FAIL=$((FAIL+1)); }
warn() { echo -e "  ${YELLOW}⚠️${NC}  $1"; WARN=$((WARN+1)); }
fixed() { echo -e "  ${BLUE}🔧${NC} $1"; FIXED=$((FIXED+1)); }
section() { echo -e "\n${BLUE}== $1 ==${NC}"; }

echo -e "${BLUE}🔍 OpenClaw Doctor v1.0.0 — $(date '+%Y-%m-%d %H:%M')${NC}"
echo -e "   Mode: $MODE | Auto-fix: $FIX | OS: $OS"
echo ""

# ── 1. Gateway Health ──
section "Gateway"

# Check if gateway is reachable
GW_RESP=$(curl -sf -o /dev/null -w "%{http_code}:%{time_total}" "http://127.0.0.1:${GW_PORT}/" 2>/dev/null || echo "000:0")
GW_CODE=$(echo "$GW_RESP" | cut -d: -f1)
GW_TIME=$(echo "$GW_RESP" | cut -d: -f2)

if [ "$GW_CODE" != "000" ]; then
  GW_MS=$(echo "$GW_TIME" | awk '{printf "%.0f", $1*1000}')
  pass "Gateway reachable (${GW_MS}ms)"
  [ "$GW_MS" -gt 2000 ] && warn "Gateway latency high (${GW_MS}ms > 2000ms)"
else
  fail "Gateway unreachable on port $GW_PORT"
  if $FIX; then
    echo "    Attempting restart..."
    if [ "$OS" = "Darwin" ]; then
      launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway 2>/dev/null && fixed "Gateway restarted via launchctl"
    else
      systemctl --user restart openclaw-gateway 2>/dev/null && fixed "Gateway restarted via systemd"
    fi
  fi
fi

# Service configuration
if [ "$OS" = "Darwin" ]; then
  PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
  if [ -f "$PLIST" ]; then
    pass "LaunchAgent plist exists"
    if launchctl list 2>/dev/null | grep -q "ai.openclaw.gateway"; then
      GW_PID=$(launchctl list 2>/dev/null | awk '/ai.openclaw.gateway/ {print $1}')
      pass "LaunchAgent loaded (pid $GW_PID)"
    else
      fail "LaunchAgent not loaded"
      if $FIX; then
        launchctl load "$PLIST" 2>/dev/null && fixed "LaunchAgent loaded"
      fi
    fi
    grep -q "<key>KeepAlive</key>" "$PLIST" 2>/dev/null && pass "KeepAlive enabled" || warn "KeepAlive not configured"
    grep -q "<key>RunAtLoad</key>" "$PLIST" 2>/dev/null && pass "RunAtLoad enabled" || warn "RunAtLoad not configured"
    
    # Node path check
    PLIST_NODE=$(sed -n '/<key>ProgramArguments<\/key>/,/<\/array>/{/<string>.*node<\/string>/s/.*<string>\(.*\)<\/string>.*/\1/p;}' "$PLIST" 2>/dev/null | head -1)
    if [ -n "$PLIST_NODE" ] && [ -f "$PLIST_NODE" ]; then
      pass "Node path valid ($PLIST_NODE)"
    elif [ -n "$PLIST_NODE" ]; then
      fail "Node path broken ($PLIST_NODE) — update needed after node upgrade"
    fi
  else
    fail "LaunchAgent plist missing"
  fi
else
  # Linux systemd check
  if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
    pass "systemd service active"
  else
    warn "systemd service not active"
  fi
fi

# ── 2. System Resources ──
section "System Resources"

if [ "$OS" = "Darwin" ]; then
  MEM_TOTAL=$($SYSCTL -n hw.memsize 2>/dev/null)
  MEM_TOTAL_MB=$((MEM_TOTAL / 1024 / 1024))
  PAGE_SIZE=$($SYSCTL -n hw.pagesize 2>/dev/null)
  PAGES_FREE=$(vm_stat 2>/dev/null | awk '/Pages free/ {gsub(/\./,"",$3); print $3}')
  PAGES_INACTIVE=$(vm_stat 2>/dev/null | awk '/Pages inactive/ {gsub(/\./,"",$3); print $3}')
  MEM_FREE_MB=$(( (PAGES_FREE + PAGES_INACTIVE) * PAGE_SIZE / 1024 / 1024 ))
  MEM_USED_MB=$((MEM_TOTAL_MB - MEM_FREE_MB))
  MEM_PCT=$((MEM_USED_MB * 100 / MEM_TOTAL_MB))
  CPU_COUNT=$($SYSCTL -n hw.ncpu 2>/dev/null)
  LOAD=$($SYSCTL -n vm.loadavg 2>/dev/null | awk '{print $2}')
else
  MEM_TOTAL_MB=$(free -m 2>/dev/null | awk '/Mem:/ {print $2}')
  MEM_USED_MB=$(free -m 2>/dev/null | awk '/Mem:/ {print $3}')
  MEM_PCT=$((MEM_USED_MB * 100 / MEM_TOTAL_MB))
  CPU_COUNT=$(nproc 2>/dev/null)
  LOAD=$(awk '{print $1}' /proc/loadavg 2>/dev/null)
fi

[ "${MEM_PCT:-0}" -lt 85 ] && pass "Memory ${MEM_PCT}% (${MEM_USED_MB}MB/${MEM_TOTAL_MB}MB)" || warn "Memory high: ${MEM_PCT}%"

LOAD_INT=$(echo "$LOAD" | awk '{printf "%.0f", $1}')
[ "${LOAD_INT:-0}" -le "${CPU_COUNT:-4}" ] && pass "CPU load $LOAD (${CPU_COUNT} cores)" || warn "CPU load high: $LOAD (${CPU_COUNT} cores)"

DISK_PCT=$(df / 2>/dev/null | tail -1 | awk '{gsub(/%/,"",$5); print $5}')
if [ "${DISK_PCT:-0}" -lt 80 ]; then
  pass "Disk ${DISK_PCT}% used"
elif [ "${DISK_PCT:-0}" -lt 90 ]; then
  warn "Disk ${DISK_PCT}% used (getting full)"
else
  fail "Disk ${DISK_PCT}% used (critical!)"
fi

# Log sizes
if [ -d "$OC_LOGS" ]; then
  LOG_SIZE=$(du -sm "$OC_LOGS" 2>/dev/null | awk '{print $1}')
  if [ "${LOG_SIZE:-0}" -lt 100 ]; then
    pass "Logs ${LOG_SIZE}MB"
  elif [ "${LOG_SIZE:-0}" -lt 500 ]; then
    warn "Logs ${LOG_SIZE}MB (consider rotation)"
  else
    fail "Logs ${LOG_SIZE}MB (bloated!)"
    if $FIX && [ -f "$OC_WORKSPACE/scripts/log_rotate.sh" ]; then
      bash "$OC_WORKSPACE/scripts/log_rotate.sh" >/dev/null 2>&1 && fixed "Logs rotated"
    fi
  fi
fi

# ── 3. Power & Resilience (macOS) ──
if [ "$MODE" = "full" ] && [ "$OS" = "Darwin" ]; then
  section "Power & Resilience"
  
  AUTO_RESTART=$(pmset -g 2>/dev/null | awk '/autorestart/ {print $2}')
  [ "$AUTO_RESTART" = "1" ] && pass "Auto-restart after power loss" || warn "Auto-restart disabled (sudo pmset -a autorestart 1)"
  
  SLEEP_VAL=$(pmset -g 2>/dev/null | awk '/^ sleep / {print $2}')
  [ "$SLEEP_VAL" = "0" ] && pass "System never sleeps" || warn "System may sleep (sleep=$SLEEP_VAL, fix: sudo pmset -a sleep 0)"
  
  WOMP=$(pmset -g 2>/dev/null | awk '/womp/ {print $2}')
  [ "$WOMP" = "1" ] && pass "Wake on LAN enabled" || warn "Wake on LAN disabled"
fi

# ── 4. Cron & Automation ──
if [ "$MODE" = "full" ]; then
  section "Cron & Automation"
  
  CRON_OUTPUT=$(openclaw cron list 2>/dev/null)
  if [ -n "$CRON_OUTPUT" ]; then
    CRON_COUNT=$(echo "$CRON_OUTPUT" | tail -n +2 | wc -l | tr -d ' ')
    CRON_FAIL=$(echo "$CRON_OUTPUT" | grep -c "fail" || true)
    pass "$CRON_COUNT cron jobs configured"
    [ "$CRON_FAIL" -gt 0 ] && fail "$CRON_FAIL cron jobs failing" || pass "All cron jobs healthy"
  else
    warn "No cron jobs or openclaw CLI unavailable"
  fi
fi

# ── 5. Security ──
section "Security"

# Config permissions
if [ -f "$OC_HOME/openclaw.json" ]; then
  if [ "$OS" = "Darwin" ]; then
    PERM=$(stat -f "%Lp" "$OC_HOME/openclaw.json" 2>/dev/null)
  else
    PERM=$(stat -c "%a" "$OC_HOME/openclaw.json" 2>/dev/null)
  fi
  if [ "$PERM" = "600" ]; then
    pass "Config permissions 600"
  else
    warn "Config permissions $PERM (should be 600)"
    if $FIX; then
      chmod 600 "$OC_HOME/openclaw.json" 2>/dev/null && fixed "Config permissions set to 600"
    fi
  fi
fi

# Auth profiles
if [ -f "$OC_HOME/agents/main/agent/auth-profiles.json" ]; then
  if [ "$OS" = "Darwin" ]; then
    AP=$(stat -f "%Lp" "$OC_HOME/agents/main/agent/auth-profiles.json" 2>/dev/null)
  else
    AP=$(stat -c "%a" "$OC_HOME/agents/main/agent/auth-profiles.json" 2>/dev/null)
  fi
  [ "$AP" = "600" ] && pass "Auth profiles permissions 600" || warn "Auth profiles permissions $AP"
fi

# ── 6. Memory & Backups ──
if [ "$MODE" = "full" ]; then
  section "Memory & Backups"
  
  if [ -d "$OC_WORKSPACE/memory" ]; then
    MEM_FILES=$(find "$OC_WORKSPACE/memory" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    pass "$MEM_FILES memory files"
  fi
  
  BACKUP_DIR="$HOME/backups/openclaw"
  if [ -d "$BACKUP_DIR" ]; then
    BK_COUNT=$(ls "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BK_COUNT" -gt 0 ]; then
      LATEST=$(ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | head -1)
      pass "$BK_COUNT backups (latest: $(basename $LATEST))"
    else
      warn "Backup directory exists but empty"
    fi
  else
    warn "No backups found (run scripts/smart_backup.sh)"
  fi
fi

# ── Summary ──
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
TOTAL=$((PASS + FAIL + WARN))
echo -e "📊 Results: ${GREEN}✅${PASS}${NC} pass | ${YELLOW}⚠️ ${WARN}${NC} warn | ${RED}❌${FAIL}${NC} fail"
[ "$FIXED" -gt 0 ] && echo -e "   ${BLUE}🔧${FIXED} auto-fixed${NC}"

if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}🚨 Critical issues found — needs attention${NC}"
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  Warnings found — consider optimizing${NC}"
  exit 0
else
  echo -e "${GREEN}💪 System healthy — all checks passed${NC}"
  exit 0
fi
