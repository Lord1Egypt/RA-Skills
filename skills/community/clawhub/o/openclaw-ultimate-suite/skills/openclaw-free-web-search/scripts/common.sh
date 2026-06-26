#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${ROOT_DIR}/logs"
ENV_FILE="${ROOT_DIR}/.env"
ENV_EXAMPLE="${ROOT_DIR}/.env.example"
OLLAMA_MODE_FILE="${LOG_DIR}/ollama.mode"
OPENCLAW_NPM_CACHE_DEFAULT="${ROOT_DIR}/.npm-cache"
LOCAL_SEARCH_ROOT_DEFAULT="${ROOT_DIR}/local-search/searxng"
LOCAL_SEARCH_HOST_DEFAULT="127.0.0.1"
LOCAL_SEARCH_PORT_DEFAULT="18080"

PRESERVE_OLLAMA_HOST="${OLLAMA_HOST-}"
PRESERVE_OPENCLAW_MODEL="${OPENCLAW_MODEL-}"
PRESERVE_OPENCLAW_CODE_MODEL="${OPENCLAW_CODE_MODEL-}"
PRESERVE_OPENCLAW_LOG_DIR="${OPENCLAW_LOG_DIR-}"
PRESERVE_OPENCLAW_OLLAMA_BIN="${OPENCLAW_OLLAMA_BIN-}"
PRESERVE_OPENCLAW_NPM_CACHE="${OPENCLAW_NPM_CACHE-}"
PRESERVE_OPENCLAW_FOREGROUND="${OPENCLAW_FOREGROUND-}"
PRESERVE_LOCAL_SEARCH_ROOT="${LOCAL_SEARCH_ROOT-}"
PRESERVE_LOCAL_SEARCH_HOST="${LOCAL_SEARCH_HOST-}"
PRESERVE_LOCAL_SEARCH_PORT="${LOCAL_SEARCH_PORT-}"
PRESERVE_LOCAL_SEARCH_URL="${LOCAL_SEARCH_URL-}"

if [[ -f "${ENV_EXAMPLE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_EXAMPLE}"
fi

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

if [[ -n "${PRESERVE_OLLAMA_HOST}" ]]; then OLLAMA_HOST="${PRESERVE_OLLAMA_HOST}"; fi
if [[ -n "${PRESERVE_OPENCLAW_MODEL}" ]]; then OPENCLAW_MODEL="${PRESERVE_OPENCLAW_MODEL}"; fi
if [[ -n "${PRESERVE_OPENCLAW_CODE_MODEL}" ]]; then OPENCLAW_CODE_MODEL="${PRESERVE_OPENCLAW_CODE_MODEL}"; fi
if [[ -n "${PRESERVE_OPENCLAW_LOG_DIR}" ]]; then OPENCLAW_LOG_DIR="${PRESERVE_OPENCLAW_LOG_DIR}"; fi
if [[ -n "${PRESERVE_OPENCLAW_OLLAMA_BIN}" ]]; then OPENCLAW_OLLAMA_BIN="${PRESERVE_OPENCLAW_OLLAMA_BIN}"; fi
if [[ -n "${PRESERVE_OPENCLAW_NPM_CACHE}" ]]; then OPENCLAW_NPM_CACHE="${PRESERVE_OPENCLAW_NPM_CACHE}"; fi
if [[ -n "${PRESERVE_OPENCLAW_FOREGROUND}" ]]; then OPENCLAW_FOREGROUND="${PRESERVE_OPENCLAW_FOREGROUND}"; fi
if [[ -n "${PRESERVE_LOCAL_SEARCH_ROOT}" ]]; then LOCAL_SEARCH_ROOT="${PRESERVE_LOCAL_SEARCH_ROOT}"; fi
if [[ -n "${PRESERVE_LOCAL_SEARCH_HOST}" ]]; then LOCAL_SEARCH_HOST="${PRESERVE_LOCAL_SEARCH_HOST}"; fi
if [[ -n "${PRESERVE_LOCAL_SEARCH_PORT}" ]]; then LOCAL_SEARCH_PORT="${PRESERVE_LOCAL_SEARCH_PORT}"; fi
if [[ -n "${PRESERVE_LOCAL_SEARCH_URL}" ]]; then LOCAL_SEARCH_URL="${PRESERVE_LOCAL_SEARCH_URL}"; fi

LOCAL_SEARCH_ROOT="${LOCAL_SEARCH_ROOT:-${LOCAL_SEARCH_ROOT_DEFAULT}}"
LOCAL_SEARCH_HOST="${LOCAL_SEARCH_HOST:-${LOCAL_SEARCH_HOST_DEFAULT}}"
LOCAL_SEARCH_PORT="${LOCAL_SEARCH_PORT:-${LOCAL_SEARCH_PORT_DEFAULT}}"
LOCAL_SEARCH_URL="${LOCAL_SEARCH_URL:-http://${LOCAL_SEARCH_HOST}:${LOCAL_SEARCH_PORT}}"
LOCAL_SEARCH_SETTINGS_FILE="${LOCAL_SEARCH_ROOT}/settings.yml"
LOCAL_SEARCH_VENV_DIR="${LOCAL_SEARCH_ROOT}/venv"
LOCAL_SEARCH_SRC_PARENT="${LOCAL_SEARCH_ROOT}/src"
LOCAL_SEARCH_LOG_FILE="${LOG_DIR}/searxng.log"
LOCAL_SEARCH_PID_FILE="${LOG_DIR}/searxng.pid"
LOCAL_SEARCH_ARCHIVE="${LOCAL_SEARCH_ROOT}/searxng-master.tar.gz"
LOCAL_SEARCH_SCREEN_SESSION="openclaw_local_search"

mkdir -p "${LOG_DIR}"
mkdir -p "${OPENCLAW_NPM_CACHE:-${OPENCLAW_NPM_CACHE_DEFAULT}}"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*"
}

find_ollama_bin() {
  if [[ -n "${OPENCLAW_OLLAMA_BIN:-}" && -x "${OPENCLAW_OLLAMA_BIN}" ]]; then
    printf '%s\n' "${OPENCLAW_OLLAMA_BIN}"
    return 0
  fi

  if command -v ollama >/dev/null 2>&1; then
    command -v ollama
    return 0
  fi

  if [[ -x "/Applications/Ollama.app/Contents/Resources/ollama" ]]; then
    printf '%s\n' "/Applications/Ollama.app/Contents/Resources/ollama"
    return 0
  fi

  return 1
}

ensure_pid_file_gone() {
  local pid_file="$1"
  if [[ -f "${pid_file}" ]]; then
    rm -f "${pid_file}"
  fi
}

process_is_running() {
  local pid="$1"
  if [[ -z "${pid}" ]]; then
    return 1
  fi
  kill -0 "${pid}" >/dev/null 2>&1
}

wait_for_ollama() {
  local url="${OLLAMA_HOST:-http://127.0.0.1:11434}/api/tags"
  local retries="${1:-20}"

  for _ in $(seq 1 "${retries}"); do
    if curl -fsS "${url}" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  return 1
}

python3_bin() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return 0
  fi

  return 1
}

local_search_healthcheck_url() {
  printf '%s/search?q=%s&format=json&language=zh-CN\n' "${LOCAL_SEARCH_URL}" "openclaw"
}

wait_for_local_search() {
  local retries="${1:-20}"
  local url
  url="$(local_search_healthcheck_url)"

  for _ in $(seq 1 "${retries}"); do
    if curl -fsS "${url}" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  return 1
}

local_search_running() {
  if [[ -f "${LOCAL_SEARCH_PID_FILE}" ]] && process_is_running "$(cat "${LOCAL_SEARCH_PID_FILE}")"; then
    return 0
  fi

  if wait_for_local_search 1; then
    return 0
  fi

  return 1
}

generate_local_search_secret() {
  local python_bin
  python_bin="$(python3_bin)"
  "${python_bin}" - <<'PY'
import secrets
print(secrets.token_hex(24))
PY
}

start_ollama() {
  local ollama_bin="$1"
  local ollama_log="$2"
  local ollama_pid_file="$3"

  if wait_for_ollama 1; then
    return 0
  fi

  if [[ -d "/Applications/Ollama.app" ]] && [[ "$(uname -s)" == "Darwin" ]]; then
    log "Ollama 未运行，正在通过 macOS App 启动。"
    open -gja "/Applications/Ollama.app"
    printf 'app\n' > "${OLLAMA_MODE_FILE}"

    if wait_for_ollama 20; then
      return 0
    fi
  fi

  log "App 启动未就绪，回退到 CLI serve。"
  nohup env OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 "${ollama_bin}" serve >>"${ollama_log}" 2>&1 &
  echo $! > "${ollama_pid_file}"
  printf 'cli\n' > "${OLLAMA_MODE_FILE}"

  wait_for_ollama 20
}

stop_ollama() {
  local ollama_pid_file="$1"

  if [[ -f "${OLLAMA_MODE_FILE}" ]] && [[ "$(cat "${OLLAMA_MODE_FILE}")" == "app" ]]; then
    osascript -e 'quit app "Ollama"' >/dev/null 2>&1 || pkill -x Ollama || true
    rm -f "${OLLAMA_MODE_FILE}"
    log "已请求退出 Ollama App。"
    return 0
  fi

  if [[ -f "${ollama_pid_file}" ]]; then
    local pid
    pid="$(cat "${ollama_pid_file}")"
    if process_is_running "${pid}"; then
      kill "${pid}"
      sleep 1
    fi
    ensure_pid_file_gone "${ollama_pid_file}"
    rm -f "${OLLAMA_MODE_FILE}"
    log "已停止 CLI 模式的 Ollama。"
    return 0
  fi

  log "未记录到由脚本启动的 Ollama。"
}

openclaw_gateway_running() {
  if ! command -v openclaw >/dev/null 2>&1; then
    return 1
  fi

  local status_output
  status_output="$(openclaw gateway status 2>&1 || true)"

  if printf '%s\n' "${status_output}" | grep -q 'RPC probe: ok'; then
    return 0
  fi

  return 1
}
