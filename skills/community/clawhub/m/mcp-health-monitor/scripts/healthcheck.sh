#!/usr/bin/env bash
# mcp-healthcheck.sh — MCP & AI Service Health Monitor
# Checks HTTP endpoints and process presence, auto-restarts via launchctl,
# and sends Telegram alerts on failure. Silent on all-healthy.
set -euo pipefail

# --- Configuration (override via environment) ---
LOG_FILE="${LOG_FILE:-$HOME/.local/logs/mcp-healthcheck.log}"
ENV_FILE="${ENV_FILE:-$HOME/.env}"
HTTP_TIMEOUT="${HTTP_TIMEOUT:-5}"
RESTART_DELAY="${RESTART_DELAY:-3}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
FAILURES=()

# --- Service definitions ---
# Format: name|check_type|target|launchctl_label
#   check_type: "http" (curl endpoint) or "process" (pgrep pattern)
#   launchctl_label: macOS service label for auto-restart, "none" to skip
SERVICES=(
  "Claw-Empire|http|http://127.0.0.1:8790/api/health|com.claw-empire.server"
  "Hermes-Gateway|process|hermes_cli.main gateway|ai.hermes.gateway"
  "mem0-MCP|process|mem0_mcp/server.py|none"
  "Brave-Search-MCP|process|brave-search-mcp-server|none"
  "Context7-MCP|process|context7-mcp|none"
)

# --- Log directory ---
mkdir -p "$(dirname "$LOG_FILE")"

# --- Load environment variables ---
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_CHAT_ID:-}"

if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
  echo "[$TIMESTAMP] [SYSTEM] [WARN] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — Telegram alerts disabled" >> "$LOG_FILE"
fi

# --- Structured logging ---
log() {
  local service="$1" status="$2" message="$3"
  echo "[$TIMESTAMP] [$service] [$status] $message" >> "$LOG_FILE"
}

# --- Telegram notification (failure only) ---
send_telegram() {
  local message="$1"
  if [[ -n "$BOT_TOKEN" && -n "$CHAT_ID" ]]; then
    local http_code
    http_code=$(curl -s -o /dev/null -w '%{http_code}' -X POST \
      "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -d chat_id="$CHAT_ID" \
      -d text="$message" \
      -d parse_mode="Markdown" 2>/dev/null || echo "000")
    if [[ "$http_code" != "200" ]]; then
      log "SYSTEM" "WARN" "Telegram send failed (HTTP $http_code)"
    fi
  fi
}

# --- Service restart via launchctl ---
restart_service() {
  local label="$1" name="$2"
  if [[ "$label" == "none" ]]; then
    log "$name" "INFO" "No launchctl label — skipping restart (expects external respawn)"
    return
  fi
  launchctl stop "$label" 2>/dev/null || true
  sleep "$RESTART_DELAY"
  launchctl start "$label" 2>/dev/null || true
  log "$name" "ACTION" "launchctl restart triggered ($label)"
}

# --- HTTP health check ---
check_http() {
  local name="$1" url="$2" label="$3"
  local http_code
  http_code=$(curl -s -o /dev/null -w '%{http_code}' --max-time "$HTTP_TIMEOUT" "$url" 2>/dev/null || echo "000")
  if [[ "$http_code" == "200" ]]; then
    log "$name" "OK" "healthy (HTTP $http_code)"
  else
    log "$name" "FAIL" "unhealthy (HTTP $http_code) — restarting"
    FAILURES+=("$name (HTTP $http_code)")
    restart_service "$label" "$name"
  fi
}

# --- Process presence check ---
check_process() {
  local name="$1" pattern="$2" label="$3"
  if pgrep -f "$pattern" > /dev/null 2>&1; then
    log "$name" "OK" "running"
  else
    log "$name" "FAIL" "not running (process not found)"
    FAILURES+=("$name (process not found)")
    restart_service "$label" "$name"
  fi
}

# --- Main execution ---
log "SYSTEM" "INFO" "=== Health check start ==="

for entry in "${SERVICES[@]}"; do
  IFS='|' read -r name check_type target label <<< "$entry"
  case "$check_type" in
    http)    check_http "$name" "$target" "$label" ;;
    process) check_process "$name" "$target" "$label" ;;
    *)       log "$name" "ERROR" "Unknown check type: $check_type" ;;
  esac
done

if [[ ${#FAILURES[@]} -gt 0 ]]; then
  FAIL_LIST=$(printf '• %s\n' "${FAILURES[@]}")
  ALERT_MSG="🚨 *MCP Health Check Alert*
$TIMESTAMP

Failures detected (${#FAILURES[@]}):
$FAIL_LIST

Services with launchctl labels were auto-restarted.
Process-only services await external respawn."

  log "SYSTEM" "ALERT" "${#FAILURES[@]} failures detected — sending notification"
  send_telegram "$ALERT_MSG"

  # Console output when Telegram is not configured
  if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
    echo "$ALERT_MSG"
  fi
else
  log "SYSTEM" "OK" "All ${#SERVICES[@]} services healthy"
fi

log "SYSTEM" "INFO" "=== Health check end ==="
