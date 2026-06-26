#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

if screen -ls 2>/dev/null | grep -q "[.]${LOCAL_SEARCH_SCREEN_SESSION}[[:space:]]"; then
  log "正在停止本地搜索 screen 会话: ${LOCAL_SEARCH_SCREEN_SESSION}"
  screen -S "${LOCAL_SEARCH_SCREEN_SESSION}" -X quit >/dev/null 2>&1 || true
  rm -f "${LOCAL_SEARCH_PID_FILE}"
  log "本地搜索服务已停止。"
  exit 0
fi

if [[ ! -f "${LOCAL_SEARCH_PID_FILE}" ]]; then
  log "本地搜索服务: 未找到 PID 文件，跳过。"
  exit 0
fi

PID="$(cat "${LOCAL_SEARCH_PID_FILE}")"

if ! process_is_running "${PID}"; then
  log "本地搜索服务: 进程已不在运行，清理 PID 文件。"
  ensure_pid_file_gone "${LOCAL_SEARCH_PID_FILE}"
  exit 0
fi

log "正在停止本地搜索服务，PID=${PID}"
kill "${PID}"

for _ in {1..10}; do
  if ! process_is_running "${PID}"; then
    ensure_pid_file_gone "${LOCAL_SEARCH_PID_FILE}"
    log "本地搜索服务已停止。"
    exit 0
  fi
  sleep 1
done

log "本地搜索服务停止超时，请手动检查。"
exit 1
