#!/usr/bin/env bats
# idle-ping monitoring BATS 測試（heartbeat.sh + watchdog.sh）
# 專業標準：mock curl（唔掂真實網絡）、獨立沙盒、測試心跳過期偵測

setup() {
  TEST_DIR="$(mktemp -d)"
  WS="$TEST_DIR/ws"
  mkdir -p "$WS/scripts" "$WS/curiosity" "$TEST_DIR/bin"
  SRC_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"

  cp "$SRC_DIR/scripts/heartbeat.sh" "$WS/scripts/"
  cp "$SRC_DIR/scripts/watchdog.sh" "$WS/scripts/"

  # mock curl：記錄呼叫（唔會掂真實網絡）
  printf '#!/bin/bash\necho "$@" >> "%s/curl.calls"\n' "$TEST_DIR" > "$TEST_DIR/bin/curl"
  chmod +x "$TEST_DIR/bin/curl"
  : > "$TEST_DIR/curl.calls"

  export PATH="$TEST_DIR/bin:$PATH"
  export IDLE_PING_WS="$WS"
  export IDLE_PING_HEARTBEAT_FILE="$WS/curiosity/heartbeat.txt"
  export IDLE_PING_LOG="$WS/curiosity/system-activity.log"
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "heartbeat 寫心跳檔（epoch 數字）" {
  run bash "$WS/scripts/heartbeat.sh"
  [ "$status" -eq 0 ]
  [ -f "$WS/curiosity/heartbeat.txt" ]
  run cat "$WS/curiosity/heartbeat.txt"
  [[ "$output" =~ ^[0-9]+$ ]]
}

@test "heartbeat 設定咗 URL 會 ping 外部監察服務" {
  export IDLE_PING_HEARTBEAT_URL="https://hc-ping.com/test-uuid"
  run bash "$WS/scripts/heartbeat.sh"
  [ "$status" -eq 0 ]
  grep -q "https://hc-ping.com/test-uuid" "$TEST_DIR/curl.calls"
}

@test "heartbeat 冇 URL 唔會 ping（零外部依賴）" {
  run bash "$WS/scripts/heartbeat.sh"
  [ "$status" -eq 0 ]
  [ ! -s "$TEST_DIR/curl.calls" ]
}

@test "watchdog：心跳檔唔存在 → alert + exit 1" {
  run bash "$WS/scripts/watchdog.sh"
  [ "$status" -eq 1 ]
  grep -q "🚨" "$WS/curiosity/system-activity.log"
}

@test "watchdog：心跳新鮮 → 唔 alert + exit 0" {
  date +%s > "$WS/curiosity/heartbeat.txt"
  run bash "$WS/scripts/watchdog.sh"
  [ "$status" -eq 0 ]
  [ ! -s "$WS/curiosity/system-activity.log" ]
}

@test "watchdog：心跳過期（超過 STALE_MIN）→ alert + exit 1" {
  echo "1" > "$WS/curiosity/heartbeat.txt"   # 1970 年 epoch = 極度過期
  run bash "$WS/scripts/watchdog.sh"
  [ "$status" -eq 1 ]
  grep -q "🚨" "$WS/curiosity/system-activity.log"
}

@test "watchdog：過期 + 有 URL → ping /fail 端點（Healthchecks.io fail signal）" {
  echo "1" > "$WS/curiosity/heartbeat.txt"
  export IDLE_PING_HEARTBEAT_URL="https://hc-ping.com/test-uuid"
  run bash "$WS/scripts/watchdog.sh"
  [ "$status" -eq 1 ]
  grep -q "https://hc-ping.com/test-uuid/fail" "$TEST_DIR/curl.calls"
}
