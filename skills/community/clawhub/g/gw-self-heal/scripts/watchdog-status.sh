#!/bin/bash
# Gateway Watchdog Status Check

OPENCLAW_DIR="$HOME/.openclaw"
CONF="$OPENCLAW_DIR/openclaw.json"
BAK="$CONF.bak"
LOG="$OPENCLAW_DIR/watchdog.log"

echo "🐧 Gateway Watchdog Status"
echo "=========================="

# Cron registered?
if crontab -l 2>/dev/null | grep -q "watchdog.sh"; then
  echo "✅ Cron: 등록됨 (매분 실행)"
else
  echo "❌ Cron: 미등록"
fi

# Gateway process?
if pgrep -f "openclaw" > /dev/null 2>&1; then
  echo "✅ Gateway: 실행 중 (PID: $(pgrep -f 'openclaw gateway' | head -1))"
else
  echo "❌ Gateway: 중지됨"
fi

# Config files?
echo ""
echo "📁 Config Files:"
[ -f "$CONF" ] && echo "  ✅ openclaw.json ($(stat -f%z "$CONF" 2>/dev/null || stat -c%s "$CONF" 2>/dev/null) bytes)" || echo "  ❌ openclaw.json 없음"
[ -f "$BAK" ] && echo "  ✅ openclaw.json.bak ($(stat -f%z "$BAK" 2>/dev/null || stat -c%s "$BAK" 2>/dev/null) bytes)" || echo "  ❌ 백업 없음"

# Broken configs?
BROKEN_COUNT=$(ls "$CONF".broken.* 2>/dev/null | wc -l | tr -d ' ')
if [ "$BROKEN_COUNT" -gt 0 ]; then
  echo "  ⚠️  깨진 설정 $BROKEN_COUNT개 보존됨"
fi

# Recent log
echo ""
echo "📋 최근 로그 (마지막 5줄):"
if [ -f "$LOG" ]; then
  tail -5 "$LOG"
else
  echo "  (로그 없음)"
fi
