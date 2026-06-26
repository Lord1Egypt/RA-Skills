#!/usr/bin/env bash
# 优雅或强制终止 Cursor 后台会话

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
  cat <<'EOF'
用法:
  ./scripts/kill-session.sh <会话名或任务别名> [--force] [--yes] [--purge] [--json]

选项:
  --force   会话在优雅退出后仍存活时，直接 kill-session
  --yes     跳过确认提示
  --purge   终止后同时删除状态文件、任务文件和日志文件
EOF
}

ensure_runtime_dirs
require_command tmux "请先安装 tmux 3.3+。"
require_command python3 "请先安装 Python 3。"

FORCE="false"
ASSUME_YES="false"
PURGE="false"
OUTPUT_JSON="false"
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE="true"
      shift
      ;;
    --yes)
      ASSUME_YES="true"
      shift
      ;;
    --purge)
      PURGE="true"
      shift
      ;;
    --json)
      OUTPUT_JSON="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"
[[ $# -ge 1 ]] || {
  usage
  exit 1
}

SESSION_QUERY="$1"
SESSION_NAME="$(resolve_session_name "${SESSION_QUERY}")" || die "未找到匹配会话: ${SESSION_QUERY}"
STATUS_FILE="$(status_file_path "${SESSION_NAME}")"
TASK_FILE="$(task_file_path "${SESSION_NAME}")"
LOG_FILE="$(log_file_path "${SESSION_NAME}")"

if [[ "${OUTPUT_JSON}" != "true" ]]; then
  print_title "终止 Cursor 会话"
  printf '会话名称: %s\n' "${SESSION_NAME}"
  printf '强制模式: %s\n' "${FORCE}"
  printf '清理文件: %s\n' "${PURGE}"
  printf '\n'
fi

if [[ "${ASSUME_YES}" != "true" && -t 0 ]]; then
  read -r -p "确认继续终止该会话吗？[y/N] " answer
  case "${answer}" in
    y|Y|yes|YES) ;;
    *) die "已取消终止操作。" ;;
  esac
fi

LAST_CAPTURE=""
if session_exists "${SESSION_NAME}"; then
  LAST_CAPTURE="$(capture_recent_output "${SESSION_NAME}" 30)"
  if [[ "${OUTPUT_JSON}" != "true" ]]; then
    info "先尝试优雅终止（发送 Ctrl+C）..."
  fi
  tmux send-keys -t "${SESSION_NAME}" C-c

  for _ in 1 2 3 4 5; do
    sleep 1
    if ! session_exists "${SESSION_NAME}"; then
      break
    fi
  done
fi

FINAL_STATUS="terminated"
if session_exists "${SESSION_NAME}"; then
  if [[ "${FORCE}" == "true" ]]; then
    if [[ "${OUTPUT_JSON}" != "true" ]]; then
      warn "会话仍未退出，执行强制终止。"
    fi
    tmux kill-session -t "${SESSION_NAME}"
    FINAL_STATUS="killed"
  else
    if [[ "${OUTPUT_JSON}" != "true" ]]; then
      warn "会话仍在运行。如需强制结束，请追加 --force。"
    fi
    FINAL_STATUS="running"
  fi
fi

LAST_CAPTURE_JSON="$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read(), ensure_ascii=False))' <<<"${LAST_CAPTURE}")"
STOPPED_AT="$(now_iso)"

if [[ -f "${STATUS_FILE}" ]]; then
  update_status_file "${STATUS_FILE}" \
    "status=${FINAL_STATUS}" \
    "stoppedAt=${STOPPED_AT}" \
    "lastCheckAt=${STOPPED_AT}" \
    "progress.currentStep=会话已停止" \
    "output.lastCapture=json:${LAST_CAPTURE_JSON}"
fi

if [[ "${PURGE}" == "true" ]]; then
  rm -f "${STATUS_FILE}" "${TASK_FILE}" "${LOG_FILE}"
  if [[ "${OUTPUT_JSON}" != "true" ]]; then
    info "已清理关联文件。"
  fi
fi

if [[ "${FINAL_STATUS}" == "running" ]]; then
  if [[ "${OUTPUT_JSON}" == "true" ]]; then
    printf '{"ok":false,"sessionName":"%s","status":"%s"}\n' "${SESSION_NAME}" "${FINAL_STATUS}"
  fi
  exit 1
fi

if [[ "${OUTPUT_JSON}" == "true" ]]; then
  python3 - "${STATUS_FILE}" "${SESSION_NAME}" "${FINAL_STATUS}" "${PURGE}" <<'PY'
import json
import os
import sys

status_file = sys.argv[1]
session_name = sys.argv[2]
final_status = sys.argv[3]
purged = sys.argv[4] == "true"
data = None
if os.path.exists(status_file):
    with open(status_file, "r", encoding="utf-8") as fh:
        data = json.load(fh)
print(json.dumps({
    "ok": True,
    "sessionName": session_name,
    "status": final_status,
    "purged": purged,
    "statusData": data,
}, ensure_ascii=False))
PY
else
  info "会话已经结束。"
fi
