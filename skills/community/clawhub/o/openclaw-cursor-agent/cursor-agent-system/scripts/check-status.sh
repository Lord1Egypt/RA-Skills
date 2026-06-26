#!/usr/bin/env bash
# 检查 OpenClaw Cursor 后台任务状态

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
  cat <<'EOF'
用法:
  ./scripts/check-status.sh [会话名或任务别名] [--json]

说明:
  不带参数时列出所有已记录任务。
  传入会话名时显示详细状态、PID、最近输出和状态文件内容。
EOF
}

infer_state_and_progress() {
  python3 - "$1" "$2" "$3" "$4" <<'PY'
import json
import re
import sys

existing = sys.argv[1]
captured = sys.argv[2]
session_alive = sys.argv[3] == "true"
pane_command = sys.argv[4].strip().lower()

state = existing or "unknown"
completed = []
current = ""
progress = "0%"

lines = [line.strip() for line in captured.splitlines() if line.strip()]

for line in lines:
    if re.match(r"^已完成步骤\s*\d+[:：]", line):
        completed.append(line)
    elif re.match(r"^(开始执行|任务完成|遇到问题)[:：]", line):
        current = line

last_line = lines[-1] if lines else ""
shell_commands = {"bash", "sh", "zsh", "dash", "fish"}
shell_idle = session_alive and pane_command in shell_commands and (
    last_line in {"$", "#"} or
    last_line.endswith("$") or
    last_line.endswith("#")
)

failure_markers = [
    "unexpected EOF",
    "command not found",
    "agent_exit_code=",
    "Workspace Trust Required",
    "No such file or directory",
]
failure_reason = ""
for marker in failure_markers:
    if marker in captured:
        failure_reason = marker
        break

json_result_success = '"type":"result","subtype":"success"' in captured
json_result_error = '"type":"result","subtype":"error"' in captured or '"is_error":true' in captured
json_tool_started = '"type":"tool_call","subtype":"started"' in captured
json_tool_completed = '"type":"tool_call","subtype":"completed"' in captured
json_assistant = '"type":"assistant"' in captured
json_thinking = '"type":"thinking"' in captured

if "任务完成:" in captured:
    state = "completed"
    progress = "100%"
    if not current:
        current = "任务已完成"
elif json_result_success:
    state = "completed"
    progress = "100%"
    current = current or "Cursor Agent 已返回成功结果"
elif json_result_error:
    state = "failed"
    progress = "0%"
    current = current or "Cursor Agent 返回错误结果"
elif "遇到问题:" in captured:
    state = "blocked"
    progress = "90%" if completed else "20%"
    if not current:
        current = "任务阻塞，等待处理"
elif json_tool_started or json_tool_completed or json_assistant or json_thinking:
    state = "running"
    if json_tool_started and not current:
        current = "Cursor 正在调用工具"
    elif json_assistant and not current:
        current = "Cursor 正在输出阶段性结果"
    elif json_thinking and not current:
        current = "Cursor 正在分析任务"
    progress = "35%" if json_tool_started else "15%"
elif shell_idle and ("agent --trust" in captured or "cursor-agent --trust" in captured):
    state = "failed"
    progress = "0%"
    if failure_reason == "unexpected EOF":
        current = "Cursor CLI 启动命令解析失败"
    elif failure_reason == "command not found":
        current = "运行环境缺少必要命令"
    elif failure_reason == "Workspace Trust Required":
        current = "Cursor CLI 卡在工作区信任确认"
    elif failure_reason.startswith("agent_exit_code="):
        current = "Cursor CLI 已退出"
    else:
        current = "Cursor CLI 已退出或未正确启动"
elif "开始执行:" in captured or completed:
    state = "running"
    current = current or (completed[-1] if completed else "任务运行中")
    estimated = min(95, max(10, len(completed) * 15))
    progress = f"{estimated}%"
elif not session_alive and state in {"starting", "running", "paused", "blocked", "unknown"}:
    state = "stopped"
    current = current or "tmux 会话已结束"
    progress = "100%" if existing == "completed" else progress

payload = {
    "status": state,
    "currentStep": current or "暂无明确进度输出",
    "completedSteps": completed,
    "estimatedProgress": progress,
}
print(json.dumps(payload, ensure_ascii=False))
PY
}

ensure_runtime_dirs
require_command python3 "请先安装 Python 3。"
require_command tmux "请先安装 tmux 3.3+。"

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

if [[ $# -eq 0 ]]; then
  if [[ "${OUTPUT_JSON}" == "true" ]]; then
    python3 - "${STATUS_DIR}" <<'PY'
import json
import os
import sys

status_dir = sys.argv[1]
items = []
if os.path.isdir(status_dir):
    for name in os.listdir(status_dir):
        if not name.endswith(".json"):
            continue
        path = os.path.join(status_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue
        items.append({
            "sessionName": data.get("sessionName") or os.path.splitext(name)[0],
            "taskName": data.get("taskName"),
            "status": data.get("status"),
            "createdAt": data.get("createdAt"),
            "statusFile": path,
        })
print(json.dumps({"ok": True, "items": items}, ensure_ascii=False))
PY
    exit 0
  fi
  print_title "已记录的 Cursor 会话"
  if [[ ! -d "${STATUS_DIR}" ]]; then
    info "当前还没有状态文件。"
    exit 0
  fi

  LIST_OUTPUT="$(list_known_sessions)"
  if [[ -z "${LIST_OUTPUT}" ]]; then
    info "当前还没有状态文件。"
    exit 0
  fi

  printf '%-38s %-12s %s\n' "会话名" "状态" "任务标识"
  print_divider
  while IFS=$'\t' read -r session_name status task_name; do
    [[ -n "${session_name}" ]] || continue
    printf '%-38s %-12s %s\n' "${session_name}" "${status}" "${task_name}"
  done <<<"${LIST_OUTPUT}"
  exit 0
fi

SESSION_QUERY="$1"
SESSION_NAME="$(resolve_session_name "${SESSION_QUERY}")" || die "未找到匹配会话: ${SESSION_QUERY}"
STATUS_FILE="$(status_file_path "${SESSION_NAME}")"
[[ -f "${STATUS_FILE}" ]] || die "状态文件不存在: ${STATUS_FILE}"

LAST_CHECK_AT="$(now_iso)"
STATUS_JSON="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("status","unknown"))' "${STATUS_FILE}")"
HAS_SESSION="false"
PID=""
PROCESS_INFO=""
LAST_CAPTURE=""
PANE_COMMAND=""
PANE_PATH=""

if session_exists "${SESSION_NAME}"; then
  HAS_SESSION="true"
  PID="$(pane_pid "${SESSION_NAME}")"
  PANE_COMMAND="$(pane_current_command "${SESSION_NAME}")"
  PANE_PATH="$(pane_current_path "${SESSION_NAME}")"
  LAST_CAPTURE="$(capture_recent_output "${SESSION_NAME}" 30)"
  if [[ -n "${PID}" ]]; then
    PROCESS_INFO="$(ps -p "${PID}" -o pid=,stat=,etime=,command= 2>/dev/null || true)"
  fi
else
  LAST_CAPTURE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("output",{}).get("lastCapture",""))' "${STATUS_FILE}")"
fi

INFERRED_JSON="$(infer_state_and_progress "${STATUS_JSON}" "${LAST_CAPTURE}" "${HAS_SESSION}" "${PANE_COMMAND}")"
LAST_CAPTURE_JSON="$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read(), ensure_ascii=False))' <<<"${LAST_CAPTURE}")"
if [[ -n "${PID}" ]]; then
  PID_UPDATE="${PID}"
else
  PID_UPDATE="null"
fi

update_status_file "${STATUS_FILE}" \
  "status=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["status"])' "${INFERRED_JSON}")" \
  "lastCheckAt=${LAST_CHECK_AT}" \
  "cursor.pid=${PID_UPDATE}" \
  "progress.currentStep=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["currentStep"])' "${INFERRED_JSON}")" \
  "progress.completedSteps=json:$(python3 -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1])["completedSteps"], ensure_ascii=False))' "${INFERRED_JSON}")" \
  "progress.estimatedProgress=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["estimatedProgress"])' "${INFERRED_JSON}")" \
  "output.lastCapture=json:${LAST_CAPTURE_JSON}"

if [[ "${OUTPUT_JSON}" == "true" ]]; then
  python3 - "${STATUS_FILE}" "${HAS_SESSION}" "${PID}" "${PROCESS_INFO}" "${PANE_COMMAND}" "${PANE_PATH}" <<'PY'
import json
import sys

path = sys.argv[1]
has_session = sys.argv[2] == "true"
pid = sys.argv[3] or None
process_info = sys.argv[4]
pane_command = sys.argv[5]
pane_path = sys.argv[6]

with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)

print(json.dumps({
    "ok": True,
    "sessionName": data.get("sessionName"),
    "statusFile": path,
    "hasSession": has_session,
    "pid": pid,
    "processInfo": process_info,
    "paneCommand": pane_command,
    "panePath": pane_path,
    "status": data,
}, ensure_ascii=False))
PY
  exit 0
fi

print_title "任务状态"
printf '查询输入:   %s\n' "${SESSION_QUERY}"
printf '会话名称:   %s\n' "${SESSION_NAME}"
printf '状态文件:   %s\n' "${STATUS_FILE}"
printf '最近检查:   %s\n' "${LAST_CHECK_AT}"
printf '\n'

if [[ "${HAS_SESSION}" == "true" ]]; then
  printf 'tmux 会话:   运行中\n'
  if [[ -n "${PID}" ]]; then
    printf 'Pane PID:    %s\n' "${PID}"
  fi
  if [[ -n "${PANE_COMMAND}" ]]; then
    printf 'Pane 命令:   %s\n' "${PANE_COMMAND}"
  fi
  if [[ -n "${PANE_PATH}" ]]; then
    printf 'Pane 路径:   %s\n' "${PANE_PATH}"
  fi
else
  printf 'tmux 会话:   未运行或已结束\n'
fi

if [[ -n "${PROCESS_INFO}" ]]; then
  printf '进程信息:    %s\n' "${PROCESS_INFO}"
fi

printf '\n状态内容:\n'
print_divider
pretty_print_json "${STATUS_FILE}"
print_divider

printf '\n最近输出 (最后 30 行):\n'
print_divider
if [[ -n "${LAST_CAPTURE}" ]]; then
  printf '%s\n' "${LAST_CAPTURE}"
else
  printf '%s\n' "(暂无输出)"
fi
print_divider
