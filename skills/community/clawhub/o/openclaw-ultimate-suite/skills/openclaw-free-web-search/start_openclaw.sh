#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

OLLAMA_BIN="$(find_ollama_bin || true)"
OLLAMA_LOG="${LOG_DIR}/ollama.log"
OPENCLAW_LOG="${LOG_DIR}/openclaw.log"
OLLAMA_PID_FILE="${LOG_DIR}/ollama.pid"
OPENCLAW_PID_FILE="${LOG_DIR}/openclaw.pid"
MODEL="${OPENCLAW_MODEL:-qwen3:14b}"
FOREGROUND="${OPENCLAW_FOREGROUND:-0}"
NPM_CACHE_DIR="${OPENCLAW_NPM_CACHE:-${ROOT_DIR}/.npm-cache}"

if [[ -z "${OLLAMA_BIN}" ]]; then
  log "未找到 ollama。请先安装官方 Ollama，或在 .env 中设置 OPENCLAW_OLLAMA_BIN。"
  exit 1
fi

if ! start_ollama "${OLLAMA_BIN}" "${OLLAMA_LOG}" "${OLLAMA_PID_FILE}"; then
  log "Ollama 仍不可用，请查看 ${OLLAMA_LOG}。"
  exit 1
fi

if ! "${OLLAMA_BIN}" list 2>/dev/null | awk '{print $1}' | grep -Fxq "${MODEL}"; then
  log "未找到主模型 ${MODEL}。请先执行: ${OLLAMA_BIN} pull ${MODEL}"
  exit 1
fi

if openclaw_gateway_running; then
  log "OpenClaw 网关已在后台运行。"
  exit 0
fi

if [[ "${FOREGROUND}" == "1" ]]; then
  log "以前台模式启动 OpenClaw。首次安装/配置建议使用此前台模式，以便处理官方交互提示。"
  exec env NPM_CONFIG_CACHE="${NPM_CACHE_DIR}" "${OLLAMA_BIN}" launch openclaw --model "${MODEL}"
fi

if command -v openclaw >/dev/null 2>&1; then
  log "正在通过 OpenClaw 官方网关命令准备后台服务。"
  openclaw gateway install >>"${OPENCLAW_LOG}" 2>&1 || true
  if openclaw gateway start >>"${OPENCLAW_LOG}" 2>&1; then
    sleep 2
    if openclaw_gateway_running; then
      log "OpenClaw 后台网关已启动。"
      exit 0
    fi
  fi
fi

log "后台网关启动失败，回退到 ollama launch openclaw。"
nohup env NPM_CONFIG_CACHE="${NPM_CACHE_DIR}" "${OLLAMA_BIN}" launch openclaw --model "${MODEL}" >>"${OPENCLAW_LOG}" 2>&1 &
echo $! > "${OPENCLAW_PID_FILE}"
sleep 3

if [[ -f "${OPENCLAW_PID_FILE}" ]] && process_is_running "$(cat "${OPENCLAW_PID_FILE}")"; then
  log "OpenClaw 已启动，PID=$(cat "${OPENCLAW_PID_FILE}")"
else
  log "OpenClaw 启动失败，请查看 ${OPENCLAW_LOG}"
  ensure_pid_file_gone "${OPENCLAW_PID_FILE}"
  exit 1
fi
