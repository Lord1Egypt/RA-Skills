#!/usr/bin/env bash
# idle-ping-gate.sh — 每分鐘檢查（command payload，零 model 成本）
# 2026-08-18 22:54 設計：idle ≥30min 後，每分鐘擲骰 1/30，中咗先觸發 idle-ping-send
# 2026-08-23 修正（框架 v2：次數制）：
#   - pingStreak = 連續「出貨而冇回應」次數，只喺中骰嗰陣先 update（唔再每分鐘 +1）
#   - 中骰 #1 出貨 → 中骰 #2 出貨 → 中骰 #N+1 唔出貨，直接暫停：send「知你忙」通知 + 收骰仔
#   - 用戶一覆 message → streak reset 0，自動重開
#   - 第一次擲骰照舊：用戶唔出聲 N 分鐘後先開始
#
# 2026-08-27 通用化 + 配置化（開源版）：
#   - 路徑/ID/行為參數全部可配置：環境變數 > scripts/idle-ping.env > 預設值
#   - 睇 idle-ping.env.example 了解全部變數
set -u

# === 配置解析（環境變數 > idle-ping.env > 預設值）===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/idle-ping.env" ]; then
  # shellcheck disable=SC1091  # optional config file; may not exist on first run
  . "$SCRIPT_DIR/idle-ping.env"
fi
WS="${IDLE_PING_WS:-$(cd "$SCRIPT_DIR/.." && pwd)}"
SESSIONS_JSON="${IDLE_PING_SESSIONS_JSON:-$HOME/.openclaw/agents/main/sessions/sessions.json}"
STATE_JSON="$WS/curiosity/state.json"
SEND_JOB_ID="${IDLE_PING_SEND_JOB_ID:-}"
PAUSE_JOB_ID="${IDLE_PING_PAUSE_JOB_ID:-}"
SYSLOG="$SCRIPT_DIR/system-log.sh"

# --- 行為參數（全部有預設值，唔填 = 原版行為）---
DICE_RANGE="${IDLE_PING_DICE_RANGE:-30}"            # 骰仔範圍：1/DICE_RANGE 中獎
IDLE_MIN_BEFORE="${IDLE_PING_IDLE_MIN:-30}"         # 冇講嘢幾多分鐘先開始擲骰
COOLDOWN_MIN="${IDLE_PING_COOLDOWN_MIN:-30}"        # 出貨後幾多分鐘內唔再 trigger（lock）
SILENT_START="${IDLE_PING_SILENT_START:-23}"        # 靜音窗口開始（24 小時制）
SILENT_END="${IDLE_PING_SILENT_END:-8}"             # 靜音窗口結束
TZ_NAME="${IDLE_PING_TZ:-Asia/Hong_Kong}"           # 時區
PAUSE_AFTER="${IDLE_PING_PAUSE_AFTER:-2}"           # 連續幾多次中骰出貨冇回應就收骰仔
PAUSE_STYLES="${IDLE_PING_PAUSE_STYLES:-月光詩意,貼心關心,幽默玩味,自嘲}"  # 暫停通知風格（逗號分隔）
DAILY_CAP="${IDLE_PING_DAILY_CAP:-0}"               # 每日出貨上限（0 = 無限）
TODAY="$(TZ="$TZ_NAME" date +%Y-%m-%d)"

# --- 攞用戶最後 message 時間戳 + idle 分鐘（排除 cron/heartbeat session） ---
read -r LAST_MSG IDLE_MIN < <(python3 - "$SESSIONS_JSON" <<'PY'
import json, sys, time
try:
    s = json.load(open(sys.argv[1]))
except Exception:
    print("0 9999"); raise SystemExit
last = 0
if isinstance(s, dict):
    for k, v in s.items():
        if not isinstance(v, dict):
            continue
        if ":cron:" in k or k.endswith(":heartbeat"):
            continue
        t = v.get("lastInteractionAt") or 0
        if t > last:
            last = t
idle = int((time.time()*1000 - last) / 60000) if last else 9999
print(f"{int(last)} {idle}")
PY
)

# 1. 靜音窗口（預設 23:00-$SILENT_END）→ 收工
H=$(TZ="$TZ_NAME" date +%H)
if [ "$H" -ge "$SILENT_START" ] || [ "$H" -lt "$SILENT_END" ]; then
  echo "NO_REPLY"; exit 0
fi

# 2. idle check：用戶最後 message ≥ $IDLE_MIN_BEFORE 分鐘先開始擲骰
if [ "${IDLE_MIN:-9999}" -lt "$IDLE_MIN_BEFORE" ]; then
  echo "NO_REPLY"; exit 0
fi

# 3. 防重複：上次出貨 < $COOLDOWN_MIN 分鐘前 → 收工（等 agent run 完先再考慮）
COOLDOWN_MS=$((COOLDOWN_MIN * 60000))
LOCKED=$(python3 -c "
import json, time
s = json.load(open('$STATE_JSON'))
now = int(time.time()*1000)
last = s.get('lastPingTriggerAt', 0) or 0
if last > now + 300000:  # 未來時間 = 污染，當冇 lock
    last = 0
print(1 if (now - last) < $COOLDOWN_MS else 0)
" 2>/dev/null || echo 0)
if [ "$LOCKED" = "1" ]; then
  echo "NO_REPLY"; exit 0
fi

# 4. 已暫停 check（pingStreak >= PAUSE_AFTER+1 = 上次已收骰仔）：
#    - 用戶覆咗（last_msg > last_ping）→ 重開：streak=0, pauseNoticeSent=false，繼續
#    - 未覆 → 保持暫停，skip
PAUSED=$(python3 - "$STATE_JSON" "$LAST_MSG" "$PAUSE_AFTER" <<'PY'
import json, sys, time
p, last_msg = sys.argv[1], int(sys.argv[2])
pause_after = int(sys.argv[3])
s = json.load(open(p))
streak = s.get('pingStreak', 0) or 0
if streak >= pause_after + 1:
    last_ship = s.get('lastShipAt', 0) or s.get('lastPingTriggerAt', 0) or 0
    now = int(time.time()*1000)
    if last_ship > now + 300000:
        last_ship = 0
    if last_msg > last_ship:
        s['pingStreak'] = 0
        s['pauseNoticeSent'] = False
        json.dump(s, open(p, 'w'), ensure_ascii=False, indent=2)
        print("RESET")  # 已重開，繼續
    else:
        print("PAUSED")  # 保持暫停
else:
    print("OK")
PY
)
if [ "$PAUSED" = "PAUSED" ]; then
  echo "NO_REPLY"; exit 0
fi
if [ "$PAUSED" = "RESET" ]; then
  bash "$SYSLOG" "✅ 暫停重開（用戶覆咗）→ streak reset 0，機制重新啟動"
fi

# 5. 擲骰 1/$DICE_RANGE（平均 idle 後 $DICE_RANGE 分鐘中一次 → 時間密度自然唔規則）
if [ "$(shuf -i 1-"$DICE_RANGE" -n 1)" != "1" ]; then
  echo "NO_REPLY"; exit 0
fi

# 5b. 每日出貨上限（DAILY_CAP=0 = 無限）
if [ "$DAILY_CAP" -gt 0 ]; then
  CAPPED=$(python3 - "$STATE_JSON" "$DAILY_CAP" "$TODAY" <<'PY'
import json, sys
p, cap, today = sys.argv[1], int(sys.argv[2]), sys.argv[3]
s = json.load(open(p))
count = s.get('dailyCount', 0)
if s.get('dailyDate') != today:
    count = 0
if count >= cap:
    print("CAPPED")
else:
    print("OK")
PY
)
  if [ "$CAPPED" = "CAPPED" ]; then
    echo "NO_REPLY"; exit 0
  fi
fi

# 6+7. 中骰 → 出貨前 update streak：
#      - 上次出貨後用戶有覆（last_msg > last_ping）→ streak = 0（重新計）
#      - 冇覆 → streak 保持累計
#      - streak >= PAUSE_AFTER（已出 N 次貨都冇回應）→ 收骰仔（PAUSE，唔出貨），streak 設 PAUSE_AFTER+1（暫停狀態）
#      - 否則 → 出貨（SHIP）：lastPingTriggerAt = now, streak += 1
RESULT=$(python3 - "$STATE_JSON" "$LAST_MSG" "$PAUSE_AFTER" "$DAILY_CAP" "$TODAY" <<'PY'
import json, sys, time
p, last_msg = sys.argv[1], int(sys.argv[2])
pause_after = int(sys.argv[3])
daily_cap = int(sys.argv[4])
today = sys.argv[5]
s = json.load(open(p))
last_ship = s.get('lastShipAt', 0) or s.get('lastPingTriggerAt', 0) or 0
now = int(time.time()*1000)
if last_ship > now + 300000:
    last_ship = 0
streak = s.get('pingStreak', 0) or 0
if last_msg > last_ship:
    streak = 0
if streak >= pause_after:
    s['pingStreak'] = pause_after + 1
    json.dump(s, open(p, 'w'), ensure_ascii=False, indent=2)
    print("PAUSE")
else:
    s['lastPingTriggerAt'] = int(time.time()*1000)
    s['lastShipAt'] = s['lastPingTriggerAt']
    s['pingStreak'] = streak + 1
    if daily_cap > 0:
        s['dailyCount'] = s.get('dailyCount', 0) if s.get('dailyDate') == today else 0
        s['dailyCount'] += 1
        s['dailyDate'] = today
    json.dump(s, open(p, 'w'), ensure_ascii=False, indent=2)
    print(f"SHIP|{streak + 1}")
PY
)

if [ "$RESULT" = "PAUSE" ]; then
  # 收骰仔：send「知你忙」通知（一次，唔重複）
  # 風格輪盤：由 IDLE_PING_PAUSE_STYLES 逗號分隔清單 4 揀 1（預設：月光詩意/貼心關心/幽默玩味/自嘲）
  if [ -n "$PAUSE_JOB_ID" ]; then
    NOTICED=$(python3 - "$STATE_JSON" "$PAUSE_STYLES" <<'PY'
import json, sys, random, time
p, styles_str = sys.argv[1], sys.argv[2]
styles = [x.strip() for x in styles_str.split(',') if x.strip()]
s = json.load(open(p))
# 2026-08-28 修：改用 timestamp 比較（lastPauseNoticeAt vs lastShipAt）而唔靠 bool flag
# —— 舊版靠 pauseNoticeSent flag，如果 RESET 分支 crash（例如 import 漏咗 time 嘅 NameError）flag 會卡死 true，之後永遠唔再 send
now = int(time.time()*1000)
last_notice = s.get('lastPauseNoticeAt', 0) or 0
last_ship = s.get('lastShipAt', 0) or s.get('lastPingTriggerAt', 0) or 0
if last_notice < last_ship:
    s['pauseNoticeSent'] = True
    s['lastPauseNoticeAt'] = now
    s['pauseNoticeStyle'] = random.choice(styles)
    json.dump(s, open(p, 'w'), ensure_ascii=False, indent=2)
    print(0)
else:
    print(1)
PY
)
    if [ "$NOTICED" = "0" ]; then
      bash "$SYSLOG" "🛑 收骰仔（連續 $((PAUSE_AFTER+1)) 次冇回應）→ send 知你忙通知"
      openclaw cron run "$PAUSE_JOB_ID" >/dev/null 2>&1
    fi
  fi
  echo "NO_REPLY"; exit 0
fi

# 8. 出貨：觸發 idle-ping-send（agentTurn 做新鮮探索 + send）
if [ -z "$SEND_JOB_ID" ]; then
  echo "NO_REPLY"; exit 0
fi
STREAK_VAL="${RESULT#SHIP|}"
bash "$SYSLOG" "🎲 中骰出貨（streak=$STREAK_VAL）→ 觸發 idle-ping-send"
openclaw cron run "$SEND_JOB_ID" >/dev/null 2>&1
echo "NO_REPLY"
