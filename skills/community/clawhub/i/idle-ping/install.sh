#!/usr/bin/env bash
# install.sh — idle-ping 機制安裝器（OpenClaw cron）
#
# 用法：
#   bash install.sh                      # 自動偵測 workspace（~/.openclaw/workspace）
#   bash install.sh /path/to/workspace   # 指定 workspace
#   bash install.sh --dry-run            # 預演（只顯示會做嘅嘢，唔實際執行）
#   bash install.sh --no-cron            # 只裝 scripts + templates，唔建立 cron job
#
# 環境變數：
#   IDLE_PING_WS          指定 workspace（或者用第一個 arg）
#   TELEGRAM_ID           Telegram chat id（send job announce 用，必須）
#   IDLE_PING_SESSIONS_JSON  sessions.json 路徑（可選，預設 ~/.openclaw/agents/main/sessions/sessions.json）
#   IDLE_PING_MODEL       出貨 job 用 model override（可選）
#
# 2026-08-27 建立（里程碑 4）：scripts + templates + 三個 cron job 一鍵安裝
set -u

# === 參數 ===
DRY=0
NO_CRON=0
WS=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --no-cron) NO_CRON=1 ;;
    *) WS="$arg" ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="${WS:-${IDLE_PING_WS:-$HOME/.openclaw/workspace}}"
TELEGRAM_ID="${TELEGRAM_ID:-}"
SESSIONS_JSON="${IDLE_PING_SESSIONS_JSON:-$HOME/.openclaw/agents/main/sessions/sessions.json}"
MODEL="${IDLE_PING_MODEL:-}"

say() { echo "==> $*"; }
warn() { echo "⚠️  $*"; }
run() {
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $*"
  else
    eval "$*"
  fi
}

# === 1. 前置檢查 ===
command -v openclaw >/dev/null 2>&1 || { warn "搵唔到 openclaw CLI——請先安裝 OpenClaw"; exit 1; }
[ -d "$WS" ] || { warn "workspace 唔存在: $WS（用 bash install.sh /path/to/workspace 指定）"; exit 1; }
if [ "$NO_CRON" = "0" ] && [ -z "$TELEGRAM_ID" ]; then
  warn "未設定 TELEGRAM_ID（send/pause job announce 需要）——用 TELEGRAM_ID=xxx bash install.sh"
  exit 1
fi

say "workspace: $WS"

# === 2. 複製 scripts ===
mkdir -p "$WS/scripts"
for f in idle-ping-gate.sh system-log.sh share-queue.py semantic-patrol.py topic-factory.py heartbeat.sh watchdog.sh; do
  if [ -f "$SCRIPT_DIR/scripts/$f" ]; then
    run "cp '$SCRIPT_DIR/scripts/$f' '$WS/scripts/$f'"
  else
    warn "缺少 $f（喺 $SCRIPT_DIR/scripts/）"
  fi
done

# === 3. 初始化 templates（唔覆蓋已有檔案）===
mkdir -p "$WS/curiosity"
for t in state.json channels.json topic-rotation.json; do
  if [ ! -f "$WS/curiosity/$t" ]; then
    run "cp '$SCRIPT_DIR/templates/$t' '$WS/curiosity/$t'"
    say "已初始化 $t"
  else
    say "skip（已存在）: $WS/curiosity/$t"
  fi
done

# === 4. 建立 cron job ===
SEND_ID=""
PAUSE_ID=""
if [ "$NO_CRON" = "1" ]; then
  say "跳過 cron job（--no-cron）——記住之後用 openclaw cron add 手動建立"
else
  say "建立五個 cron job（gate / send / pause / heartbeat / watchdog；用 declaration-key 確保冪等，重跑唔會重複）..."

  # 4a. idle-ping-gate — 每 N 分鐘 command payload（零 model 成本；間隔由 IDLE_PING_ROLL_EVERY 控制）
  GATE_CMD="openclaw cron add --name idle-ping-gate --declaration-key idle-ping-gate --every '${IDLE_PING_ROLL_EVERY:-1m}' --command 'bash $WS/scripts/idle-ping-gate.sh' --no-deliver --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $GATE_CMD"
  else
    GATE_OUT="$(eval "$GATE_CMD" 2>/dev/null)"
    GATE_ID="$(printf '%s' "$GATE_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$GATE_ID" ]; then
      say "gate job ID: $GATE_ID"
    else
      warn "gate job 建立失敗/攞唔到 ID（可能已存在，用 openclaw cron list 檢查）"
    fi
  fi

  # 4b. idle-ping-send — agentTurn，disabled（由 gate trigger），600s
  # shellcheck disable=SC2034  # SEND_PROMPT is expanded inside SEND_CMD's eval below
  SEND_PROMPT="$(sed -e "s|{{WORKSPACE}}|$WS|g" -e "s|{{SESSIONS_JSON}}|$SESSIONS_JSON|g" "$SCRIPT_DIR/templates/send-job-prompt.txt")"
  SEND_CMD="openclaw cron add --name idle-ping-send --declaration-key idle-ping-send --at 2036-01-01T00:00:00Z --session isolated --timeout-seconds 600 --light-context --disabled --keep-after-run --announce --channel telegram --to '$TELEGRAM_ID' --message \"\$SEND_PROMPT\" --json"
  [ -n "$MODEL" ] && SEND_CMD="openclaw cron add --name idle-ping-send --declaration-key idle-ping-send --at 2036-01-01T00:00:00Z --session isolated --timeout-seconds 600 --light-context --disabled --model '$MODEL' --announce --channel telegram --to '$TELEGRAM_ID' --message \"\$SEND_PROMPT\" --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $SEND_CMD"
  else
    SEND_OUT="$(eval "$SEND_CMD" 2>/dev/null)"
    SEND_ID="$(printf '%s' "$SEND_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$SEND_ID" ]; then
      say "send job ID: $SEND_ID"
    else
      warn "send job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4c. idle-ping-pause-notice — agentTurn，disabled（由 gate trigger），300s
  # shellcheck disable=SC2034  # PAUSE_PROMPT is expanded inside PAUSE_CMD's eval below
  PAUSE_PROMPT="$(sed "s|{{WORKSPACE}}|$WS|g" "$SCRIPT_DIR/templates/pause-job-prompt.txt")"
  PAUSE_CMD="openclaw cron add --name idle-ping-pause-notice --declaration-key idle-ping-pause-notice --at 2036-01-01T00:00:00Z --session isolated --timeout-seconds 300 --light-context --disabled --keep-after-run --announce --channel telegram --to '$TELEGRAM_ID' --message \"\$PAUSE_PROMPT\" --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $PAUSE_CMD"
  else
    PAUSE_OUT="$(eval "$PAUSE_CMD" 2>/dev/null)"
    PAUSE_ID="$(printf '%s' "$PAUSE_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$PAUSE_ID" ]; then
      say "pause job ID: $PAUSE_ID"
    else
      warn "pause job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4d. idle-ping-heartbeat — production 監察心跳（每 10 分鐘 command payload，零 model 成本）
  #      更新心跳檔 + 可選 ping 外部監察服務（Healthchecks.io 等）
  HB_EVERY="${IDLE_PING_HEARTBEAT_EVERY:-10m}"
  HB_CMD="openclaw cron add --name idle-ping-heartbeat --declaration-key idle-ping-heartbeat --every '$HB_EVERY' --command 'bash $WS/scripts/heartbeat.sh' --no-deliver --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $HB_CMD"
  else
    HB_OUT="$(eval "$HB_CMD" 2>/dev/null)"
    HB_ID="$(printf '%s' "$HB_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$HB_ID" ]; then
      say "heartbeat job ID: $HB_ID"
    else
      warn "heartbeat job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4e. idle-ping-watchdog — 心跳過期偵測（每 1 小時，偵測 cron 靜靜雞死）
  WD_EVERY="${IDLE_PING_WATCHDOG_EVERY:-1h}"
  WD_CMD="openclaw cron add --name idle-ping-watchdog --declaration-key idle-ping-watchdog --every '$WD_EVERY' --command 'bash $WS/scripts/watchdog.sh' --no-deliver --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $WD_CMD"
  else
    WD_OUT="$(eval "$WD_CMD" 2>/dev/null)"
    WD_ID="$(printf '%s' "$WD_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$WD_ID" ]; then
      say "watchdog job ID: $WD_ID"
    else
      warn "watchdog job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4f. idle-ping-crawler — 內容生產鏈：每小時主題爬蟲（command payload，零 model 成本）
  #      讀 topic-rotation.json 攞當前主題 → 全部主題可搜渠道搜（news 中英 + arxiv + reddit）
  #      → Ollama 歸納 → share-queue 入倉（channel=topic）→ index+1
  CRAWLER_CMD="openclaw cron add --name idle-ping-crawler --declaration-key idle-ping-crawler --cron '15 * * * *' --tz '${IDLE_PING_TZ:-Asia/Hong_Kong}' --command 'python3 $WS/scripts/semantic-patrol.py --mode rotation' --command-env 'IDLE_PING_WS=$WS' --no-deliver --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $CRAWLER_CMD"
  else
    CRAWLER_OUT="$(eval "$CRAWLER_CMD" 2>/dev/null)"
    CRAWLER_ID="$(printf '%s' "$CRAWLER_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$CRAWLER_ID" ]; then
      say "crawler job ID: $CRAWLER_ID"
    else
      warn "crawler job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4g. idle-ping-topic-factory — 內容生產鏈：夜晚主題工廠（每晚 22:30，agentTurn，delivery none）
  #      agent 睇 topic-factory.py show → 諗新主題 → refresh 補到 30 條（crawler 聽日用）
  # shellcheck disable=SC2034  # TF_PROMPT is expanded inside TF_CMD's eval below
  TF_PROMPT="$(sed "s|{{WORKSPACE}}|$WS|g" "$SCRIPT_DIR/templates/topic-factory-job-prompt.txt")"
  TF_CMD="openclaw cron add --name idle-ping-topic-factory --declaration-key idle-ping-topic-factory --cron '30 22 * * *' --tz '${IDLE_PING_TZ:-Asia/Hong_Kong}' --session isolated --timeout-seconds 600 --light-context --no-deliver --message \"\$TF_PROMPT\" --json"
  [ -n "$MODEL" ] && TF_CMD="openclaw cron add --name idle-ping-topic-factory --declaration-key idle-ping-topic-factory --cron '30 22 * * *' --tz '${IDLE_PING_TZ:-Asia/Hong_Kong}' --session isolated --timeout-seconds 600 --light-context --model '$MODEL' --no-deliver --message \"\$TF_PROMPT\" --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $TF_CMD"
  else
    TF_OUT="$(eval "$TF_CMD" 2>/dev/null)"
    TF_ID="$(printf '%s' "$TF_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$TF_ID" ]; then
      say "topic-factory job ID: $TF_ID"
    else
      warn "topic-factory job 建立失敗/攞唔到 ID"
    fi
  fi

  # 4h. idle-ping-deep-explore — 內容生產鏈：凌晨深度探索（每日 01:00，agentTurn，delivery none）
  #      自主揀範疇 → 深入探索 3-5 個來源 → 4 條最得意入倉（channel=deep，俾 idle-ping 出貨）
  # shellcheck disable=SC2034  # DE_PROMPT is expanded inside DE_CMD's eval below
  DE_PROMPT="$(sed "s|{{WORKSPACE}}|$WS|g" "$SCRIPT_DIR/templates/deep-explore-job-prompt.txt")"
  DE_CMD="openclaw cron add --name idle-ping-deep-explore --declaration-key idle-ping-deep-explore --cron '0 1 * * *' --tz '${IDLE_PING_TZ:-Asia/Hong_Kong}' --session isolated --timeout-seconds 600 --light-context --no-deliver --message \"\$DE_PROMPT\" --json"
  [ -n "$MODEL" ] && DE_CMD="openclaw cron add --name idle-ping-deep-explore --declaration-key idle-ping-deep-explore --cron '0 1 * * *' --tz '${IDLE_PING_TZ:-Asia/Hong_Kong}' --session isolated --timeout-seconds 600 --light-context --model '$MODEL' --no-deliver --message \"\$DE_PROMPT\" --json"
  if [ "$DRY" = "1" ]; then
    echo "   [dry-run] $DE_CMD"
  else
    DE_OUT="$(eval "$DE_CMD" 2>/dev/null)"
    DE_ID="$(printf '%s' "$DE_OUT" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("job",{}).get("id",""))
except Exception: print("")' 2>/dev/null)"
    if [ -n "$DE_ID" ]; then
      say "deep-explore job ID: $DE_ID"
    else
      warn "deep-explore job 建立失敗/攞唔到 ID"
    fi
  fi

  # === 5. 寫 idle-ping.env（gate script 會讀呢個檔）===
  if [ -f "$WS/scripts/idle-ping.env" ]; then
    say "skip（已存在）: $WS/scripts/idle-ping.env"
  else
    ENV_CONTENT="IDLE_PING_WS=$WS
IDLE_PING_SESSIONS_JSON=$SESSIONS_JSON
IDLE_PING_SEND_JOB_ID=$SEND_ID
IDLE_PING_PAUSE_JOB_ID=$PAUSE_ID
IDLE_PING_HEARTBEAT_FILE=$WS/curiosity/heartbeat.txt
IDLE_PING_WATCHDOG_STALE_MIN=60

# ===== Behavior tunables (optional — uncomment to change) =====
# IDLE_PING_DICE_RANGE=30          # Dice denominator (1/N chance per roll)
# IDLE_PING_IDLE_MIN=30            # Minutes of silence before rolling starts
# IDLE_PING_COOLDOWN_MIN=30        # Cooldown after a shipment (minutes)
# IDLE_PING_DAILY_CAP=0            # Max shipments per day (0 = unlimited)
# IDLE_PING_SILENT_START=23        # Silent window start (24h)
# IDLE_PING_SILENT_END=8           # Silent window end
# IDLE_PING_TZ=Asia/Hong_Kong      # Timezone
# IDLE_PING_PAUSE_AFTER=2          # Unanswered shipments before auto-pause
# IDLE_PING_PAUSE_STYLES=月光詩意,貼心關心,幽默玩味,自嘲  # Pause-notice style pool"
    if [ "$DRY" = "1" ]; then
      echo "   [dry-run] 寫入 $WS/scripts/idle-ping.env"
    else
      printf '%s\n' "$ENV_CONTENT" > "$WS/scripts/idle-ping.env"
      say "已寫入 idle-ping.env（SEND/PAUSE job ID 自動填入）"
    fi
  fi
fi

# === 6. 完成 ===
say "安裝完成！"
echo
echo "  下一步："
echo "  1. 檢查 cron job:  openclaw cron list"
echo "  2. 手動測試出貨:  openclaw cron run <send-job-id>"
echo "  3. 睇系統 log:    cat $WS/curiosity/system-activity.log"
echo "  4. 靜音窗口/骰仔設定: 編輯 $WS/scripts/idle-ping.env 或 curiosity/state.json"
