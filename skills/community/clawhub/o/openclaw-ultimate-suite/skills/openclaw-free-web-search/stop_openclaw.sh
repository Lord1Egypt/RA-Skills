#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

OPENCLAW_PID_FILE="${LOG_DIR}/openclaw.pid"
OLLAMA_PID_FILE="${LOG_DIR}/ollama.pid"

stop_by_pid_file() {
  local pid_file="$1"
  local name="$2"

  if [[ ! -f "${pid_file}" ]]; then
    log "${name}: 未找到 PID 文件，跳过。"
    return 0
  fi

  local pid
  pid="$(cat "${pid_file}")"

  if ! process_is_running "${pid}"; then
    log "${name}: 进程已不在运行，清理 PID 文件。"
    ensure_pid_file_gone "${pid_file}"
    return 0
  fi

  log "正在停止 ${name}，PID=${pid}"
  kill "${pid}"

  for _ in {1..10}; do
    if ! process_is_running "${pid}"; then
      ensure_pid_file_gone "${pid_file}"
      log "${name}: 已停止。"
      return 0
    fi
    sleep 1
  done

  log "${name}: 超时未退出，请手动检查。"
  exit 1
}

stop_by_pid_file "${OPENCLAW_PID_FILE}" "OpenClaw"

if openclaw_gateway_running; then
  log "正在停止 OpenClaw 后台网关。"
  openclaw gateway stop >/dev/null 2>&1 || true
fi

if [[ "${1:-}" == "--with-ollama" ]]; then
  stop_ollama "${OLLAMA_PID_FILE}"
else
  log "默认不停止 Ollama。若要一并停止，请执行 ./stop_openclaw.sh --with-ollama"
fi
