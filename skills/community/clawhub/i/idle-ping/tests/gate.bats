#!/usr/bin/env bats
# idle-ping-gate BATS 測試套件
# 專業標準（HackerOne / BATS-core 推薦做法）：
#   - 每個 @test 獨立沙盒（setup/teardown）
#   - mock 外部指令（fake shuf 強制中骰、fake openclaw 記錄呼叫）
#   - 用 run + assert 檢查 exit code / output / state 變化

setup() {
  TEST_DIR="$(mktemp -d)"
  WS="$TEST_DIR/ws"
  mkdir -p "$WS/scripts" "$WS/curiosity" "$TEST_DIR/bin"
  SRC_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"

  cp "$SRC_DIR/scripts/idle-ping-gate.sh" "$WS/scripts/"
  cp "$SRC_DIR/scripts/system-log.sh" "$WS/scripts/"
  cp "$SRC_DIR/templates/state.json" "$WS/curiosity/state.json"

  # mock shuf：永遠出 1（強制中骰）
  printf '#!/bin/bash\necho 1\n' > "$TEST_DIR/bin/shuf"
  chmod +x "$TEST_DIR/bin/shuf"

  # mock openclaw：記錄所有 cron run 呼叫（唔會掂真實 gateway）
  # 注意：$TEST_DIR 要喺寫入時展開，唔可以留喺 script 入面
  printf '#!/bin/bash\necho "$@" >> "%s/openclaw.calls"\n' "$TEST_DIR" > "$TEST_DIR/bin/openclaw"
  chmod +x "$TEST_DIR/bin/openclaw"
  : > "$TEST_DIR/openclaw.calls"

  export PATH="$TEST_DIR/bin:$PATH"
  export IDLE_PING_WS="$WS"
  export IDLE_PING_SESSIONS_JSON="$WS/sessions.json"
  export IDLE_PING_SEND_JOB_ID="fake-send-job"
  export IDLE_PING_PAUSE_JOB_ID="fake-pause-job"
  # 測試用：關閉靜音窗口（99 = 永遠唔靜音）
  export IDLE_PING_SILENT_START=99
  export IDLE_PING_SILENT_END=0
}

teardown() {
  rm -rf "$TEST_DIR"
}

# === 測試 helpers ===
write_state() { # $1 = python 語句
  python3 - "$WS/curiosity/state.json" "$1" <<'PY'
import json, sys, time
s = json.load(open(sys.argv[1]))
exec(sys.argv[2])
json.dump(s, open(sys.argv[1], 'w'), ensure_ascii=False, indent=2)
PY
}

write_sessions() { # $1 = 幾多分鐘前
  python3 - "$WS/sessions.json" "$1" <<'PY'
import json, sys, time
now = int(time.time()*1000) - int(sys.argv[2])*60000
json.dump({'agent:main:telegram:direct:000000000': {'lastInteractionAt': now}}, open(sys.argv[1], 'w'))
PY
}

run_gate() {
  bash "$WS/scripts/idle-ping-gate.sh"
}

# === 預設值行為測試 ===

@test "idle 少過門檻 → NO_REPLY（唔會擲骰）" {
  write_sessions 5
  run run_gate
  [ "$status" -eq 0 ]
  [ "$output" = "NO_REPLY" ]
  [ ! -s "$TEST_DIR/openclaw.calls" ]
}

@test "lock 期間 → NO_REPLY（等上個 run 完）" {
  write_sessions 40
  write_state "s['lastPingTriggerAt']=int(time.time()*1000)-5*60000"
  run run_gate
  [ "$output" = "NO_REPLY" ]
  [ ! -s "$TEST_DIR/openclaw.calls" ]
}

@test "已暫停（streak 滿）→ NO_REPLY，唔會出貨" {
  write_state "s['pingStreak']=3; s['lastShipAt']=int(time.time()*1000)-60*60000; s['lastPingTriggerAt']=0"
  write_sessions 90
  run run_gate
  [ "$output" = "NO_REPLY" ]
  [ ! -s "$TEST_DIR/openclaw.calls" ]
}

@test "暫停中用戶覆咗 → RESET（✅ log + 重新出貨）" {
  write_state "s['pingStreak']=3; s['lastShipAt']=int(time.time()*1000)-60*60000; s['lastPingTriggerAt']=0"
  write_sessions 40
  run run_gate
  grep -q "✅" "$WS/curiosity/system-activity.log"
  # RESET 之後會繼續擲骰（fake shuf 必中）→ 直接出貨 → streak=1
  grep -q "fake-send-job" "$TEST_DIR/openclaw.calls"
  run python3 -c "import json; print(json.load(open('$WS/curiosity/state.json'))['pingStreak'])"
  [ "$output" = "1" ]
}

@test "中骰 + streak=0 → SHIP（streak→1，觸發 send job）" {
  write_state "s['pingStreak']=0; s['lastPingTriggerAt']=0; s['lastShipAt']=0"
  write_sessions 40
  run run_gate
  grep -q "fake-send-job" "$TEST_DIR/openclaw.calls"
  run python3 -c "import json; print(json.load(open('$WS/curiosity/state.json'))['pingStreak'])"
  [ "$output" = "1" ]
}

@test "中骰 + streak 滿 2 冇回應 → PAUSE（streak→3 + 暫停通知）" {
  write_state "s['pingStreak']=2; s['lastPingTriggerAt']=0; s['lastShipAt']=int(time.time()*1000)-60*60000"
  write_sessions 90
  run run_gate
  grep -q "fake-pause-job" "$TEST_DIR/openclaw.calls"
  grep -q "🛑" "$WS/curiosity/system-activity.log"
  run python3 -c "import json; s=json.load(open('$WS/curiosity/state.json')); print(s['pingStreak'], s['pauseNoticeSent'])"
  [ "$output" = "3 True" ]
}

# === 配置化測試 ===

@test "IDLE_PING_IDLE_MIN=5 → idle 10 分鐘都開始擲骰" {
  write_state "s['pingStreak']=0; s['lastPingTriggerAt']=0; s['lastShipAt']=0"
  write_sessions 10
  IDLE_PING_IDLE_MIN=5 run run_gate
  grep -q "fake-send-job" "$TEST_DIR/openclaw.calls"
}

@test "IDLE_PING_PAUSE_AFTER=1 → 1 次冇回應就暫停" {
  write_state "s['pingStreak']=1; s['lastPingTriggerAt']=0; s['lastShipAt']=int(time.time()*1000)-60*60000"
  write_sessions 90
  IDLE_PING_PAUSE_AFTER=1 run run_gate
  grep -q "fake-pause-job" "$TEST_DIR/openclaw.calls"
  run python3 -c "import json; print(json.load(open('$WS/curiosity/state.json'))['pingStreak'])"
  [ "$output" = "2" ]
}

@test "IDLE_PING_DAILY_CAP=1 → 第二日出貨會被擋" {
  write_state "s['pingStreak']=0; s['lastPingTriggerAt']=0; s['lastShipAt']=0"
  write_sessions 40
  IDLE_PING_DAILY_CAP=1 run run_gate
  grep -q "fake-send-job" "$TEST_DIR/openclaw.calls"
  # 第二次（同日）：應該被 cap 擋住
  : > "$TEST_DIR/openclaw.calls"
  IDLE_PING_DAILY_CAP=1 run run_gate
  [ "$output" = "NO_REPLY" ]
  [ ! -s "$TEST_DIR/openclaw.calls" ]
}

@test "IDLE_PING_PAUSE_STYLES 自訂 → 用自訂風格" {
  write_state "s['pingStreak']=2; s['lastPingTriggerAt']=0; s['lastShipAt']=int(time.time()*1000)-60*60000; s['pauseNoticeSent']=False"
  write_sessions 90
  IDLE_PING_PAUSE_STYLES="A風格,B風格,C風格" run run_gate
  run python3 -c "import json; print(json.load(open('$WS/curiosity/state.json'))['pauseNoticeStyle'])"
  [[ "$output" =~ ^(A風格|B風格|C風格)$ ]]
}

@test "靜音窗口（SILENT_START=0）→ 永遠 NO_REPLY" {
  write_sessions 40
  IDLE_PING_SILENT_START=0 IDLE_PING_SILENT_END=24 run run_gate
  [ "$output" = "NO_REPLY" ]
  [ ! -s "$TEST_DIR/openclaw.calls" ]
}

@test "IDLE_PING_DICE_RANGE=1 → 必中（shuf 出 1）" {
  write_state "s['pingStreak']=0; s['lastPingTriggerAt']=0; s['lastShipAt']=0"
  write_sessions 40
  IDLE_PING_DICE_RANGE=1 run run_gate
  grep -q "fake-send-job" "$TEST_DIR/openclaw.calls"
}
