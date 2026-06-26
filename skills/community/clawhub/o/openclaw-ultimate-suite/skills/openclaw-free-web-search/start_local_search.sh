#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

if local_search_running; then
  log "本地搜索服务已在运行: ${LOCAL_SEARCH_URL}"
  exit 0
fi

if [[ ! -x "${LOCAL_SEARCH_VENV_DIR}/bin/python" ]]; then
  log "未找到本地搜索虚拟环境。请先执行 ./install_local_search.sh"
  exit 1
fi

if [[ ! -f "${LOCAL_SEARCH_SETTINGS_FILE}" ]]; then
  log "未找到本地搜索配置。请先执行 ./install_local_search.sh"
  exit 1
fi

log "启动本地搜索服务: ${LOCAL_SEARCH_URL}"
if command -v screen >/dev/null 2>&1; then
  screen -S "${LOCAL_SEARCH_SCREEN_SESSION}" -X quit >/dev/null 2>&1 || true
  screen -dmS "${LOCAL_SEARCH_SCREEN_SESSION}" bash -lc \
    "export SEARXNG_SETTINGS_PATH='${LOCAL_SEARCH_SETTINGS_FILE}'; exec '${LOCAL_SEARCH_VENV_DIR}/bin/waitress-serve' --listen='${LOCAL_SEARCH_HOST}:${LOCAL_SEARCH_PORT}' searx.webapp:app >>'${LOCAL_SEARCH_LOG_FILE}' 2>&1"
else
  nohup env SEARXNG_SETTINGS_PATH="${LOCAL_SEARCH_SETTINGS_FILE}" \
    "${LOCAL_SEARCH_VENV_DIR}/bin/waitress-serve" --listen="${LOCAL_SEARCH_HOST}:${LOCAL_SEARCH_PORT}" searx.webapp:app \
    >>"${LOCAL_SEARCH_LOG_FILE}" 2>&1 &
  echo $! > "${LOCAL_SEARCH_PID_FILE}"
fi

if wait_for_local_search 30; then
  log "本地搜索服务已就绪。"
  exit 0
fi

log "本地搜索服务启动失败，请查看 ${LOCAL_SEARCH_LOG_FILE}"
exit 1
