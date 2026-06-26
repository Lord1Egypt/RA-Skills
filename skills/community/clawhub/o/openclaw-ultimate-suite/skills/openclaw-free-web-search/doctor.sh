#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

OLLAMA_BIN="$(find_ollama_bin || true)"
MODEL="${OPENCLAW_MODEL:-qwen3:14b}"
CODE_MODEL="${OPENCLAW_CODE_MODEL:-qwen3-coder:30b}"
OLLAMA_PID_FILE="${LOG_DIR}/ollama.pid"
OPENCLAW_PID_FILE="${LOG_DIR}/openclaw.pid"

log "工作目录: ${ROOT_DIR}"

if [[ -z "${OLLAMA_BIN}" ]]; then
  log "Ollama: 未安装或未在 PATH 中。"
  exit 1
fi

log "Ollama 二进制: ${OLLAMA_BIN}"

if curl -fsS "${OLLAMA_HOST:-http://127.0.0.1:11434}/api/tags" >/dev/null 2>&1; then
  log "Ollama 服务: 正常"
  if [[ -f "${LOG_DIR}/ollama.mode" ]]; then
    log "Ollama 启动方式: $(cat "${LOG_DIR}/ollama.mode")"
  fi
else
  log "Ollama 服务: 不可达"
  if [[ -f "${OLLAMA_PID_FILE}" ]]; then
    log "建议: 查看 ${LOG_DIR}/ollama.log"
  else
    log "建议: 先执行 ./start_openclaw.sh 或手动运行 ollama serve"
  fi
fi

log "模型列表:"
"${OLLAMA_BIN}" list 2>/dev/null || log "无法读取模型列表，通常表示 Ollama 自身未正常启动。"

if "${OLLAMA_BIN}" list 2>/dev/null | awk '{print $1}' | grep -Fxq "${MODEL}"; then
  log "主模型 ${MODEL}: 已安装"
else
  log "主模型 ${MODEL}: 未安装"
  if screen -ls 2>&1 | grep -q 'qwen3_pull'; then
    log "主模型下载: 后台会话 qwen3_pull 正在运行"
    if [[ -f "${LOG_DIR}/qwen3-14b-pull.log" ]]; then
      log "最近下载日志:"
      tail -n 3 "${LOG_DIR}/qwen3-14b-pull.log"
    fi
  fi
fi

if "${OLLAMA_BIN}" list 2>/dev/null | awk '{print $1}' | grep -Fxq "${CODE_MODEL}"; then
  log "代码模型 ${CODE_MODEL}: 已安装"
else
  log "代码模型 ${CODE_MODEL}: 未安装（可选）"
fi

if [[ -f "${OPENCLAW_PID_FILE}" ]] && process_is_running "$(cat "${OPENCLAW_PID_FILE}")"; then
  log "OpenClaw 进程: 运行中，PID=$(cat "${OPENCLAW_PID_FILE}")"
elif openclaw_gateway_running; then
  log "OpenClaw 网关: 后台 LaunchAgent 运行中"
else
  log "OpenClaw 进程: 未检测到由本项目脚本启动的实例"
  log "建议: 首次安装使用 OPENCLAW_FOREGROUND=1 ./start_openclaw.sh，观察官方交互提示。"
fi

if [[ -x "${LOCAL_SEARCH_VENV_DIR}/bin/python" ]] || [[ -f "${LOCAL_SEARCH_SETTINGS_FILE}" ]]; then
  if local_search_running; then
    log "本地搜索服务: 正常 (${LOCAL_SEARCH_URL})"
  else
    log "本地搜索服务: 已安装但未运行"
    log "建议: 执行 ./start_local_search.sh"
  fi
else
  log "本地搜索服务: 未安装（可选）"
fi
