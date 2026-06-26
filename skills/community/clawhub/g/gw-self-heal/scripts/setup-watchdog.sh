#!/bin/bash
# Gateway Watchdog Setup Script
# Author: 김여명 (dawnkim_master)
# Auto-healing watchdog for OpenClaw gateway

set -e

OPENCLAW_DIR="$HOME/.openclaw"
CONF="$OPENCLAW_DIR/openclaw.json"
BAK="$CONF.bak"
WATCHDOG="$OPENCLAW_DIR/watchdog.sh"
LOG="$OPENCLAW_DIR/watchdog.log"

echo "🐧 Gateway Watchdog 설치 시작..."

# 1. Validate openclaw.json exists
if [ ! -f "$CONF" ]; then
  echo "❌ $CONF 파일이 없습니다. OpenClaw가 설치되어 있는지 확인하세요."
  exit 1
fi

# 2. Initial backup
cp "$CONF" "$BAK"
echo "✅ 초기 백업 완료: $BAK"

# 3. Create watchdog script
cat > "$WATCHDOG" << 'WATCHDOG_SCRIPT'
#!/bin/bash
# OpenClaw Gateway Watchdog
# Auto-restart + config rollback on failure

OPENCLAW_DIR="$HOME/.openclaw"
CONF="$OPENCLAW_DIR/openclaw.json"
BAK="$CONF.bak"
LOG="$OPENCLAW_DIR/watchdog.log"
HEALTH_PORT="${OPENCLAW_HEALTH_PORT:-3377}"
MAX_LOG_LINES=500

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
  
  # Log rotation: keep last MAX_LOG_LINES
  if [ -f "$LOG" ] && [ "$(wc -l < "$LOG")" -gt "$MAX_LOG_LINES" ]; then
    tail -n "$MAX_LOG_LINES" "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
  fi
}

# Check if config exists
if [ ! -f "$CONF" ]; then
  log "CRITICAL: openclaw.json missing!"
  if [ -f "$BAK" ]; then
    cp "$BAK" "$CONF"
    log "RECOVERED: Restored from backup"
  else
    log "FATAL: No backup available. Manual intervention required."
    exit 1
  fi
fi

# Level 1: Process check
if ! pgrep -f "openclaw" > /dev/null 2>&1; then
  log "LEVEL1: Gateway process not found → restarting"
  openclaw gateway start >> "$LOG" 2>&1
  sleep 5
  
  if pgrep -f "openclaw" > /dev/null 2>&1; then
    log "LEVEL1: Restart successful"
  else
    log "LEVEL1: Restart failed → trying config rollback"
    # Fall through to Level 2
  fi
fi

# Level 2: Health check (process alive but possibly broken)
if pgrep -f "openclaw" > /dev/null 2>&1; then
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$HEALTH_PORT/health" --max-time 10 2>/dev/null || echo "000")
  
  if [ "$HTTP_CODE" = "200" ]; then
    # Healthy → update backup with current good config
    cp "$CONF" "$BAK"
    # Silent success, no log spam
    exit 0
  fi
  
  # Health check failed
  log "LEVEL2: Health check failed (HTTP $HTTP_CODE)"
  
  if [ -f "$BAK" ]; then
    # Save broken config for debugging
    cp "$CONF" "$CONF.broken.$(date +%s)"
    
    # Rollback to last known good
    cp "$BAK" "$CONF"
    log "LEVEL2: Config rolled back from backup"
    
    # Restart gateway
    openclaw gateway stop >> "$LOG" 2>&1
    sleep 2
    openclaw gateway start >> "$LOG" 2>&1
    sleep 5
    
    # Verify recovery
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$HEALTH_PORT/health" --max-time 10 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
      log "LEVEL2: Recovery successful ✅"
    else
      log "LEVEL3: Recovery failed. Manual intervention required ❌"
    fi
  else
    log "LEVEL3: No backup available. Manual intervention required ❌"
  fi
fi
WATCHDOG_SCRIPT

chmod +x "$WATCHDOG"
echo "✅ Watchdog 스크립트 생성: $WATCHDOG"

# 4. Register cron job (every minute)
CRON_JOB="* * * * * $WATCHDOG"

# Remove existing watchdog cron if any
(crontab -l 2>/dev/null | grep -v "watchdog.sh") | crontab -

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
echo "✅ Cron 등록 완료 (매분 실행)"

# 5. Initial run
bash "$WATCHDOG"
echo "✅ 초기 실행 완료"

echo ""
echo "🐧 Gateway Watchdog 설치 완료!"
echo "   로그: $LOG"
echo "   상태: bash $OPENCLAW_DIR/../.openclaw/workspace/skills/gateway-watchdog/scripts/watchdog-status.sh"
echo ""
echo "   제거: crontab -l | grep -v watchdog | crontab -"
