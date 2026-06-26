#!/usr/bin/env bash
set -euo pipefail

# State file for fallback persistence when OpenClaw does not persist auth state.
# Set LOGICX_STATE_FILE to override. File is created with 600 permissions.
LOGICX_STATE_FILE="${LOGICX_STATE_FILE:-${HOME:-/tmp}/.config/logicx/skill-state.json}"

# Official OpenClaw skill: built-in defaults so users need minimal config.
: "${LOGICX_BASE_URL:=http://43.139.104.95:8070}"
: "${LOGICX_AGENT_SERVICE_KEY:=openclaw-public}"
export LOGICX_BASE_URL LOGICX_AGENT_SERVICE_KEY

usage() {
  cat <<'EOF'
Usage:
  logicx_api.sh METHOD PATH [JSON_BODY]

Examples:
  logicx_api.sh GET /api/health
  logicx_api.sh POST agent/link/start '{"install_id":"openclaw-main"}'
  logicx_api.sh POST agent/link/status '{"link_code":"lc_xxx","install_id":"openclaw-main"}'
  logicx_api.sh POST agent/auth/login '{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}'
  logicx_api.sh GET user
  logicx_api.sh POST payment/create '{"plan":"pro_monthly","gateway":"mock"}'

Defaults: LOGICX_BASE_URL=http://43.139.104.95:8070, LOGICX_AGENT_SERVICE_KEY=openclaw-public.
When LOGICX_USER_TOKEN is not set, the script reads from the state file.
It auto-saves link_code and install_id after link/start, and user_token
when link/status or auth/login returns confirmed. When the user says
"我登录好了", run scripts/check_link_status.sh.
EOF
}

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: $name" >&2
    exit 1
  fi
}

# Load user_token from state file when not in env
load_state() {
  [[ -n "${LOGICX_USER_TOKEN:-}" ]] && return 0
  [[ ! -f "$LOGICX_STATE_FILE" ]] && return 0
  local val
  val="$(sed -n 's/.*"user_token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$LOGICX_STATE_FILE" 2>/dev/null | head -1)"
  if [[ -n "$val" ]]; then
    export LOGICX_USER_TOKEN="$val"
  fi
}

# Write JSON to state file. Creates parent dir and sets 600 perms.
write_state() {
  local content="$1"
  local dir
  dir="$(dirname "$LOGICX_STATE_FILE")"
  mkdir -p "$dir"
  printf '%s\n' "$content" > "$LOGICX_STATE_FILE"
  chmod 600 "$LOGICX_STATE_FILE" 2>/dev/null || true
}

# Save user_token (replaces any existing state — bind is complete)
save_user_token() {
  local token="$1"
  [[ -z "$token" ]] && return 0
  write_state "{\"user_token\":\"$token\"}"
}

# Save link_code and install_id after link/start (so "我登录好了" can call link/status)
save_bind_state() {
  local link_code="$1"
  local install_id="$2"
  [[ -z "$link_code" || -z "$install_id" ]] && return 0
  write_state "{\"install_id\":\"$install_id\",\"link_code\":\"$link_code\",\"status\":\"pending\"}"
}

# Extract link_code from JSON (single-line or multi-line)
extract_link_code() {
  grep -oE '"link_code"[[:space:]]*:[[:space:]]*"[^"]*"' 2>/dev/null | head -1 | sed 's/.*"\([^"]*\)"$/\1/'
}

# Extract install_id from JSON body
extract_install_id() {
  grep -oE '"install_id"[[:space:]]*:[[:space:]]*"[^"]*"' 2>/dev/null | head -1 | sed 's/.*"\([^"]*\)"$/\1/'
}

# Extract user_token from JSON body (handles single/multi-line)
extract_user_token() {
  grep -oE '"user_token"[[:space:]]*:[[:space:]]*"[^"]*"' 2>/dev/null | head -1 | sed 's/.*"\([^"]*\)"$/\1/'
}

normalize_url() {
  local base_url="$1"
  local path_arg="$2"
  local trimmed="${path_arg#/}"

  case "$path_arg" in
    http://*|https://*)
      printf '%s\n' "$path_arg"
      ;;
    /api/health|api/health)
      printf '%s/api/health\n' "$base_url"
      ;;
    /api/proxy/*|api/proxy/*)
      printf '%s/%s\n' "$base_url" "${trimmed}"
      ;;
    *)
      printf '%s/api/proxy/%s\n' "$base_url" "${trimmed}"
      ;;
  esac
}

needs_user_token() {
  local path_arg="$1"
  case "$path_arg" in
    /api/health|api/health|\
    /api/proxy/agent/link/start|api/proxy/agent/link/start|agent/link/start|\
    /api/proxy/agent/link/status|api/proxy/agent/link/status|agent/link/status|\
    /api/proxy/agent/link/confirm|api/proxy/agent/link/confirm|agent/link/confirm|\
    /api/proxy/agent/auth/login|api/proxy/agent/auth/login|agent/auth/login)
      return 1
      ;;
    *)
      return 0
      ;;
  esac
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -lt 2 ]]; then
    usage
    exit 0
  fi

  local method
  method="$(printf '%s' "$1" | tr '[:lower:]' '[:upper:]')"
  local path_arg="$2"
  local body="${3:-}"

  # LOGICX_BASE_URL and LOGICX_AGENT_SERVICE_KEY have defaults for the official skill
  [[ -n "${LOGICX_BASE_URL:-}" ]] || { echo "Missing LOGICX_BASE_URL" >&2; exit 1; }

  # Fallback: load user_token from state file when OpenClaw does not persist it
  load_state

  local base_url="${LOGICX_BASE_URL%/}"
  local url
  url="$(normalize_url "$base_url" "$path_arg")"

  if needs_user_token "$path_arg"; then
    require_env "LOGICX_USER_TOKEN"
  fi

  # Write response body to a temp file, capture HTTP status on stdout
  local tmp_body
  tmp_body="$(mktemp /tmp/logicx_api_XXXXXX)"

  local -a curl_args
  curl_args=(
    -sS
    -o "$tmp_body"
    -w "%{http_code}"
    -X "$method"
    -H "Authorization: Bearer ${LOGICX_AGENT_SERVICE_KEY}"
  )

  if [[ -n "${LOGICX_USER_TOKEN:-}" ]]; then
    curl_args+=(-H "X-LogicX-User-Token: ${LOGICX_USER_TOKEN}")
  fi

  if [[ -n "$body" ]]; then
    curl_args+=(
      -H "Content-Type: application/json"
      --data "$body"
    )
  fi

  local http_code
  http_code="$(curl "${curl_args[@]}" "$url")"

  if [[ -s "$tmp_body" ]]; then
    cat "$tmp_body"
    printf '\n'
    # Auto-save state when OpenClaw does not persist it
    if [[ "$http_code" -lt 400 ]]; then
      case "$path_arg" in
        agent/link/start|api/proxy/agent/link/start)
          # Save link_code and install_id so "我登录好了" can call link/status
          save_bind_state "$(extract_link_code < "$tmp_body")" "$(extract_install_id <<< "$body")"
          ;;
        agent/link/status|api/proxy/agent/link/status)
          if grep -q '"status"[[:space:]]*:[[:space:]]*"confirmed"' "$tmp_body" 2>/dev/null; then
            save_user_token "$(extract_user_token < "$tmp_body")"
          fi
          ;;
        agent/auth/login|api/proxy/agent/auth/login)
          if grep -q '"ok"[[:space:]]*:[[:space:]]*true' "$tmp_body" 2>/dev/null; then
            save_user_token "$(extract_user_token < "$tmp_body")"
          fi
          ;;
      esac
    fi
  fi

  rm -f "$tmp_body"

  printf 'HTTP_STATUS:%s\n' "$http_code"

  if [[ "$http_code" -ge 400 ]]; then
    exit 1
  fi
}

main "$@"
