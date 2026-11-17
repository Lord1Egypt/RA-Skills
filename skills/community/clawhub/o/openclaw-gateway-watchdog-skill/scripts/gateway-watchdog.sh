#!/usr/bin/env bash
# Gateway + Spark Watchdog — Minimal Edition
# Purpose: Alert on gateway/spark disconnection, notify on recovery.
# No config drift, no auto-heal, no baseline promotion.
set -euo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-$(command -v openclaw 2>/dev/null || echo /opt/homebrew/bin/openclaw)}"

BASE_DIR="${GW_WATCHDOG_BASE_DIR:-$HOME/.openclaw/watchdogs/gateway-discord}"
STATE_FILE="$BASE_DIR/state.json"
EVENT_LOG="$BASE_DIR/events.jsonl"
LOCK_DIR="$BASE_DIR/lock"
CONFIG_ENV_FILE="$BASE_DIR/config.env"
OPENCLAW_ENV_FILE="${OPENCLAW_ENV_FILE:-$HOME/.openclaw/.env}"
SPARK_STATE_FILE="$BASE_DIR/spark_state.json"
API_HUB_STATE_FILE="$BASE_DIR/api_hub_state.json"
DASHBOARD_STATE_FILE="$BASE_DIR/dashboard_state.json"

FAIL_THRESHOLD="${GW_WATCHDOG_FAIL_THRESHOLD:-3}"
COOLDOWN_SECONDS="${GW_WATCHDOG_COOLDOWN_SECONDS:-600}"
HEALTH_TIMEOUT_MS="${GW_WATCHDOG_HEALTH_TIMEOUT_MS:-10000}"

# Read one value without sourcing a shell file. This keeps the watchdog
# independent from unrelated shell expressions in local configuration.
read_env_value() {
  local key="$1" file="$2"
  [[ -f "$file" ]] || return 1
  awk -v wanted="$key" '
    {
      line = $0
      sub(/^[[:space:]]*/, "", line)
      sub(/^export[[:space:]]+/, "", line)
      separator = index(line, "=")
      if (separator == 0) next
      candidate = substr(line, 1, separator - 1)
      gsub(/[[:space:]]/, "", candidate)
      if (candidate != wanted) next
      value = substr(line, separator + 1)
      sub(/^[[:space:]]*/, "", value)
      sub(/[[:space:]]*$/, "", value)
      found = value
    }
    END {
      if (found == "") exit 1
      first = substr(found, 1, 1)
      last = substr(found, length(found), 1)
      if ((first == "\"" && last == "\"") || (first == "\047" && last == "\047")) {
        found = substr(found, 2, length(found) - 2)
      }
      print found
    }
  ' "$file"
}

load_allowlisted_config() {
  local key value
  for key in \
    DISCORD_WEBHOOK_URL DISCORD_BOT_TOKEN DISCORD_CHANNEL_ID \
    SPARK_API_URL SPARK_API_TOKEN LOCAL_API_URL DASHBOARD_PORT \
    GW_WATCHDOG_FAIL_THRESHOLD GW_WATCHDOG_COOLDOWN_SECONDS \
    GW_WATCHDOG_HEALTH_TIMEOUT_MS GW_WATCHDOG_LOCK_TIMEOUT_SECONDS; do
    if value=$(read_env_value "$key" "$CONFIG_ENV_FILE" 2>/dev/null); then
      printf -v "$key" '%s' "$value"
      export "$key"
    fi
  done
}

mkdir -p "$BASE_DIR"
load_allowlisted_config

FAIL_THRESHOLD="${GW_WATCHDOG_FAIL_THRESHOLD:-$FAIL_THRESHOLD}"
COOLDOWN_SECONDS="${GW_WATCHDOG_COOLDOWN_SECONDS:-$COOLDOWN_SECONDS}"
HEALTH_TIMEOUT_MS="${GW_WATCHDOG_HEALTH_TIMEOUT_MS:-$HEALTH_TIMEOUT_MS}"
DISCORD_WEBHOOK_URL="${DISCORD_WEBHOOK_URL:-}"
DISCORD_BOT_TOKEN="${DISCORD_BOT_TOKEN:-}"
DISCORD_CHANNEL_ID="${DISCORD_CHANNEL_ID:-}"

SOURCE_TAG="${GW_WATCHDOG_SOURCE:-unknown}"

# --- Helpers (must be defined before use) ---
now_epoch() { date +%s; }
now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

# --- Event log (append-only, for debugging) ---
log_event() {
  local event="$1" detail="$2"
  printf '{"time":"%s","event":"%s","source":"%s","detail":"%s"}\n' \
    "$(now_iso)" "$event" "$SOURCE_TAG" "$detail" >> "$EVENT_LOG"
}

# --- Lock with timeout ---
LOCK_TIMEOUT_SECONDS="${GW_WATCHDOG_LOCK_TIMEOUT_SECONDS:-300}"

acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    return 0
  fi
  
  # Lock exists, check if it's stale
  if [[ -f "$LOCK_DIR/pid" ]]; then
    local old_pid
    old_pid=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
    if [[ -n "$old_pid" ]] && ! kill -0 "$old_pid" 2>/dev/null; then
      # Process is dead, remove stale lock
      log_event "stale_lock_removed" "pid=$old_pid"
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null && return 0
    fi
  fi
  
  # Check lock age
  if [[ -f "$LOCK_DIR/created" ]]; then
    local lock_time now
    lock_time=$(cat "$LOCK_DIR/created" 2>/dev/null || echo "0")
    now=$(now_epoch)
    if (( now - lock_time > LOCK_TIMEOUT_SECONDS )); then
      log_event "lock_timeout_removed" "age=$((now - lock_time))s"
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null && return 0
    fi
  fi
  
  # Cannot acquire lock
  exit 0
}

acquire_lock

# Write lock metadata
echo $$ > "$LOCK_DIR/pid"
now_epoch > "$LOCK_DIR/created"

cleanup() { rm -rf "$LOCK_DIR" >/dev/null 2>&1 || true; }
trap cleanup EXIT

format_duration() {
  local s="${1:-0}"
  local d=$((s / 86400)) h=$(((s % 86400) / 3600)) m=$(((s % 3600) / 60))
  local out=""
  (( d > 0 )) && out+="${d}天"
  (( h > 0 )) && out+="${h}小时"
  (( m > 0 )) && out+="${m}分"
  (( s % 60 > 0 || ${#out} == 0 )) && out+="$((s % 60))秒"
  echo "$out"
}

# --- State (flat file, 5 fields) ---
# status | consecutive_failures | last_alert_epoch | outage_start_epoch | alerted_this_incident
load_state() {
  local file="${1:-$STATE_FILE}"
  if [[ -f "$file" ]]; then
    cat "$file"
  else
    echo "healthy 0 0 0 0"
  fi
}

write_state() {
  local file="${5:-$STATE_FILE}"
  echo "$1 $2 $3 $4 $6" > "$file"
}

# --- Discord ---
send_discord() {
  local title="$1" body="$2"
  local payload
  payload=$(printf '{"content":"**%s**\\n%s"}' "$title" "$body")

  if [[ -n "$DISCORD_WEBHOOK_URL" ]]; then
    echo "$payload" | curl -sS -X POST "$DISCORD_WEBHOOK_URL" \
      -H "Content-Type: application/json" --data @- >/dev/null 2>&1 || true
    return
  fi

  if [[ -n "$DISCORD_BOT_TOKEN" && -n "$DISCORD_CHANNEL_ID" ]]; then
    echo "$payload" | curl -sS -X POST \
      "https://discord.com/api/v10/channels/${DISCORD_CHANNEL_ID}/messages" \
      -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
      -H "Content-Type: application/json" --data @- >/dev/null 2>&1 || true
  fi
}

# --- Health Check (simple: is gateway running + responsive?) ---
check_gateway() {
  # 1. Can we get status?
  if ! "$OPENCLAW_BIN" gateway status --json >/dev/null 2>&1; then
    echo "fail"
    return
  fi
  # 2. Is health endpoint responsive?
  if ! "$OPENCLAW_BIN" health --json --timeout "$HEALTH_TIMEOUT_MS" >/dev/null 2>&1; then
    echo "fail"
    return
  fi
  echo "pass"
}

# --- Spark connectivity check (authenticated loopback tunnel) ---
check_spark() {
  local spark_api="${SPARK_API_URL:-http://127.0.0.1:17070}"
  local spark_token="${SPARK_API_TOKEN:-}"
  local response
  local curl_args=(-fsS --max-time 5 -H "Accept: application/json")

  if [[ -z "$spark_token" ]]; then
    spark_token=$(read_env_value "SPARK_API_TOKEN" "$OPENCLAW_ENV_FILE" 2>/dev/null || true)
  fi
  if [[ -n "$spark_token" ]]; then
    curl_args+=(-H "Authorization: Bearer ${spark_token}")
  fi

  if ! response=$(curl "${curl_args[@]}" "${spark_api}/status" 2>/dev/null); then
    echo "fail"
    return
  fi

  # This watchdog reports disconnection only. A successful authenticated
  # response with a non-empty JSON object proves that the Spark status service
  # is reachable; detailed model/GPU health belongs to ops_health_checks.py.
  if printf '%s' "$response" | python3 -c \
    'import json, sys; payload = json.load(sys.stdin); raise SystemExit(0 if isinstance(payload, dict) and payload else 1)' \
    >/dev/null 2>&1; then
    echo "pass"
    return
  fi

  echo "fail"
}

# --- Local API Hub Health Check ---
check_api_hub() {
  local api_url="${LOCAL_API_URL:-http://localhost:3456}"
  if ! curl -fsS --max-time 3 "${api_url}/health" >/dev/null 2>&1; then
    echo "fail"
    return
  fi
  echo "pass"
}

# --- Dashboard Health Check ---
check_dashboard() {
  local dashboard_port="${DASHBOARD_PORT:-18793}"
  local response
  if ! response=$(curl -fsS --max-time 3 "http://localhost:${dashboard_port}/health" 2>/dev/null); then
    echo "fail"
    return
  fi
  # Check if status is ok
  if echo "$response" | grep -q '"status":"ok"'; then
    echo "pass"
  else
    echo "fail"
  fi
}

# --- Process Check Result ---
# Args: service_name check_result prev_status prev_failures prev_alert_at prev_outage_start prev_alerted
# Returns: new_status new_failures should_alert outage_start alerted
process_check() {
  local service="$1"
  local result="$2"
  local prev_status="$3"
  local prev_failures="$4"
  local prev_alert_at="$5"
  local prev_outage_start="$6"
  local prev_alerted="$7"
  
  local now
  now=$(now_epoch)
  
  if [[ "$result" == "pass" ]]; then
    # Healthy
    if [[ "$prev_status" != "healthy" && "$prev_alerted" == "1" ]]; then
      local outage_seconds=$((now - prev_outage_start))
      send_discord "✅ ${service} 已恢复" \
        "来源: $SOURCE_TAG\n服务: ${service}\n断连时长: $(format_duration "$outage_seconds")\n恢复时间: $(now_iso)"
      log_event "${service}_recovered" "outage_duration=${outage_seconds}s"
    elif [[ "$prev_status" != "healthy" ]]; then
      log_event "${service}_silent_recovery" "failures=${prev_failures},never_alerted"
    fi
    echo "healthy 0 0 0 0"
  else
    # Unhealthy
    local new_failures=$((prev_failures + 1))
    local outage_start="$prev_outage_start"
    if [[ "$prev_status" == "healthy" ]]; then
      outage_start="$now"
    fi
    
    local should_alert=0
    if (( new_failures >= FAIL_THRESHOLD )); then
      if [[ "$prev_alerted" == "0" ]]; then
        should_alert=1
      elif (( now - prev_alert_at >= COOLDOWN_SECONDS )); then
        should_alert=1
      fi
    fi
    
    if [[ "$should_alert" == "1" ]]; then
      local outage_seconds=$((now - outage_start))
      send_discord "🚨 ${service} 断连告警" \
        "来源: $SOURCE_TAG\n服务: ${service}\n连续失败: $new_failures\n已断连: $(format_duration "$outage_seconds")\n检测时间: $(now_iso)"
      log_event "${service}_alert" "failures=${new_failures},outage=${outage_seconds}s"
      echo "down $new_failures $now $outage_start 1"
    else
      log_event "${service}_check_failed" "failures=${new_failures},suppressed"
      echo "down $new_failures $prev_alert_at $outage_start $prev_alerted"
    fi
  fi
}

# === Main ===
now=$(now_epoch)

# --- Check Gateway ---
read -r gw_status gw_failures gw_alert_at gw_outage_start gw_alerted <<< "$(load_state "$STATE_FILE")"
gw_result=$(check_gateway)
read -r new_gw_status new_gw_failures new_gw_alert_at new_gw_outage_start new_gw_alerted <<< "$(process_check "Gateway" "$gw_result" "$gw_status" "$gw_failures" "$gw_alert_at" "$gw_outage_start" "$gw_alerted")"
write_state "$new_gw_status" "$new_gw_failures" "$new_gw_alert_at" "$new_gw_outage_start" "$STATE_FILE" "$new_gw_alerted"

# --- Check Spark ---
read -r sp_status sp_failures sp_alert_at sp_outage_start sp_alerted <<< "$(load_state "$SPARK_STATE_FILE")"
sp_result=$(check_spark)
read -r new_sp_status new_sp_failures new_sp_alert_at new_sp_outage_start new_sp_alerted <<< "$(process_check "Spark" "$sp_result" "$sp_status" "$sp_failures" "$sp_alert_at" "$sp_outage_start" "$sp_alerted")"
write_state "$new_sp_status" "$new_sp_failures" "$new_sp_alert_at" "$new_sp_outage_start" "$SPARK_STATE_FILE" "$new_sp_alerted"

# --- Check Local API Hub ---
read -r ah_status ah_failures ah_alert_at ah_outage_start ah_alerted <<< "$(load_state "$API_HUB_STATE_FILE")"
ah_result=$(check_api_hub)
read -r new_ah_status new_ah_failures new_ah_alert_at new_ah_outage_start new_ah_alerted <<< "$(process_check "API_Hub" "$ah_result" "$ah_status" "$ah_failures" "$ah_alert_at" "$ah_outage_start" "$ah_alerted")"
write_state "$new_ah_status" "$new_ah_failures" "$new_ah_alert_at" "$new_ah_outage_start" "$API_HUB_STATE_FILE" "$new_ah_alerted"

# --- Check Dashboard ---
read -r db_status db_failures db_alert_at db_outage_start db_alerted <<< "$(load_state "$DASHBOARD_STATE_FILE")"
db_result=$(check_dashboard)
read -r new_db_status new_db_failures new_db_alert_at new_db_outage_start new_db_alerted <<< "$(process_check "Dashboard" "$db_result" "$db_status" "$db_failures" "$db_alert_at" "$db_outage_start" "$db_alerted")"
write_state "$new_db_status" "$new_db_failures" "$new_db_alert_at" "$new_db_outage_start" "$DASHBOARD_STATE_FILE" "$new_db_alerted"

exit 0
