#!/usr/bin/env bash
# 向运行中的 Cursor 会话发送额外指令

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
  cat <<'EOF'
用法:
  ./scripts/send-command.sh <会话名或任务别名> <指令> [--json]

特殊指令:
  /pause
  /resume
  /status
  /focus [子任务]
  /expand [新增需求]
  /abort [原因]
EOF
}

ensure_runtime_dirs
require_command tmux "请先安装 tmux 3.3+。"
require_command python3 "请先安装 Python 3。"

OUTPUT_JSON="false"
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
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

[[ $# -ge 2 ]] || {
  usage
  exit 1
}

SESSION_QUERY="$1"
shift
COMMAND_TEXT="$*"
SESSION_NAME="$(resolve_session_name "${SESSION_QUERY}")" || die "未找到匹配会话: ${SESSION_QUERY}"
STATUS_FILE="$(status_file_path "${SESSION_NAME}")"

session_exists "${SESSION_NAME}" || die "tmux 会话不存在或已结束: ${SESSION_NAME}"

BEFORE_CAPTURE="$(capture_recent_output "${SESSION_NAME}" 10)"

if [[ "${OUTPUT_JSON}" != "true" ]]; then
  print_title "发送额外指令"
  printf '会话名称: %s\n' "${SESSION_NAME}"
  printf '发送内容: %s\n' "${COMMAND_TEXT}"
  printf '\n'
fi

tmux send-keys -t "${SESSION_NAME}" "${COMMAND_TEXT}" C-m
sleep 1

AFTER_CAPTURE="$(capture_recent_output "${SESSION_NAME}" 10)"
LAST_CAPTURE_JSON="$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read(), ensure_ascii=False))' <<<"${AFTER_CAPTURE}")"

DELIVERED="false"
if [[ "${AFTER_CAPTURE}" != "${BEFORE_CAPTURE}" ]] || [[ "${AFTER_CAPTURE}" == *"${COMMAND_TEXT}"* ]]; then
  DELIVERED="true"
fi

case "${COMMAND_TEXT}" in
  /pause*)
    update_status_file "${STATUS_FILE}" \
      "status=paused" \
      "progress.currentStep=已发送暂停指令，等待 Cursor 响应" \
      "lastCheckAt=$(now_iso)" \
      "output.lastCapture=json:${LAST_CAPTURE_JSON}"
    ;;
  /resume*)
    update_status_file "${STATUS_FILE}" \
      "status=running" \
      "progress.currentStep=已发送恢复指令，等待 Cursor 继续执行" \
      "lastCheckAt=$(now_iso)" \
      "output.lastCapture=json:${LAST_CAPTURE_JSON}"
    ;;
  /status*)
    update_status_file "${STATUS_FILE}" \
      "lastCheckAt=$(now_iso)" \
      "output.lastCapture=json:${LAST_CAPTURE_JSON}"
    ;;
  *)
    update_status_file "${STATUS_FILE}" \
      "status=running" \
      "progress.currentStep=已发送补充指令，等待 Cursor 消化新需求" \
      "lastCheckAt=$(now_iso)" \
      "output.lastCapture=json:${LAST_CAPTURE_JSON}"
    ;;
esac

if [[ "${OUTPUT_JSON}" == "true" ]]; then
  python3 - "${STATUS_FILE}" "${DELIVERED}" "${COMMAND_TEXT}" <<'PY'
import json
import sys

path = sys.argv[1]
delivered = sys.argv[2] == "true"
command = sys.argv[3]

with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)

print(json.dumps({
    "ok": delivered,
    "delivered": delivered,
    "sessionName": data.get("sessionName"),
    "command": command,
    "status": data,
}, ensure_ascii=False))
PY
else
  if [[ "${DELIVERED}" == "true" ]]; then
    info "指令已写入 tmux 会话。"
  else
    warn "已尝试发送指令，但暂未在最近输出中观察到回显。"
  fi

  print_divider
  printf '最近输出:\n'
  print_divider
  printf '%s\n' "${AFTER_CAPTURE:-"(暂无输出)"}"
  print_divider
fi
