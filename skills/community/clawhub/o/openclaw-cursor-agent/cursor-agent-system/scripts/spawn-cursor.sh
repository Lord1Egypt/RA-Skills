#!/usr/bin/env bash
# 启动 OpenClaw -> tmux -> Cursor CLI 后台任务

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
  cat <<'EOF'
用法:
  ./scripts/spawn-cursor.sh <任务标识> <任务描述> [项目路径] [--priority 优先级] [--eta 预计耗时] [--task-file 现成任务文件] [--json]

参数:
  任务标识            简短任务名，例如 feature-auth
  任务描述            要发给 Cursor CLI 的核心任务描述
  项目路径            可选，默认当前目录

选项:
  --priority          任务优先级，默认 normal
  --eta               预计耗时，默认 30-60分钟
  --task-file         使用现成 Markdown 任务文件，不再自动生成正文
  --json              只输出机器可读 JSON
  -h, --help          显示帮助

示例:
  ./scripts/spawn-cursor.sh feature-auth "实现 JWT 登录接口" /workspace/myapp --priority high --eta 45分钟
EOF
}

ensure_runtime_dirs

PRIORITY="normal"
ETA="30-60分钟"
EXTERNAL_TASK_FILE=""
OUTPUT_JSON="false"
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --priority)
      [[ $# -ge 2 ]] || die "--priority 需要一个值。"
      PRIORITY="$2"
      shift 2
      ;;
    --eta)
      [[ $# -ge 2 ]] || die "--eta 需要一个值。"
      ETA="$2"
      shift 2
      ;;
    --task-file)
      [[ $# -ge 2 ]] || die "--task-file 需要一个路径。"
      EXTERNAL_TASK_FILE="$2"
      shift 2
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

TASK_NAME="${1:-}"
TASK_DESCRIPTION="${2:-}"
PROJECT_PATH="${3:-$(pwd)}"
ORIGINAL_PROJECT_PATH="${PROJECT_PATH}"

[[ -n "${TASK_NAME}" && -n "${TASK_DESCRIPTION}" ]] || {
  usage
  exit 1
}

require_command tmux "请先安装 tmux 3.3+。"
require_command python3 "请先安装 Python 3。"
AGENT_BIN="$(detect_agent_command)" || die "未找到 Cursor CLI。请先安装 agent 或 cursor-agent。"

[[ -d "${PROJECT_PATH}" ]] || die "项目路径不存在: ${PROJECT_PATH}"

if command -v cygpath >/dev/null 2>&1; then
  case "${PROJECT_PATH}" in
    [A-Za-z]:[\\/]*)
      PROJECT_PATH="$(cygpath -u "${PROJECT_PATH}")"
      ;;
  esac
  if [[ -n "${EXTERNAL_TASK_FILE}" ]]; then
    case "${EXTERNAL_TASK_FILE}" in
      [A-Za-z]:[\\/]*)
        EXTERNAL_TASK_FILE="$(cygpath -u "${EXTERNAL_TASK_FILE}")"
        ;;
    esac
  fi
fi

WORKSPACE_PATH="${PROJECT_PATH}"
if command -v cygpath >/dev/null 2>&1; then
  WORKSPACE_PATH="$(cygpath -w "${PROJECT_PATH}" 2>/dev/null || printf '%s' "${ORIGINAL_PROJECT_PATH}")"
fi

TASK_SLUG="$(slugify "${TASK_NAME}")"
PROJECT_SLUG="$(slugify "$(basename "${PROJECT_PATH}")")"
TIMESTAMP="$(timestamp_compact)"
SESSION_NAME="${PROJECT_SLUG}-${TASK_SLUG}-${TIMESTAMP}"
TASK_ID="${SESSION_NAME}"
TASK_FILE="$(task_file_path "${SESSION_NAME}")"
RUNNER_FILE="$(runner_file_path "${SESSION_NAME}")"
STATUS_FILE="$(status_file_path "${SESSION_NAME}")"
LOG_FILE="$(log_file_path "${SESSION_NAME}")"
CREATED_AT="$(now_iso)"

if [[ "${OUTPUT_JSON}" != "true" ]]; then
  print_title "启动 Cursor 后台任务"
  printf '任务 ID:    %s\n' "${TASK_ID}"
  printf '会话名称:   %s\n' "${SESSION_NAME}"
  printf '项目路径:   %s\n' "${PROJECT_PATH}"
  printf '优先级:     %s\n' "${PRIORITY}"
  printf '预计耗时:   %s\n' "${ETA}"
  printf '任务文件:   %s\n' "${TASK_FILE}"
  printf '启动脚本:   %s\n' "${RUNNER_FILE}"
  printf '状态文件:   %s\n' "${STATUS_FILE}"
  printf '日志文件:   %s\n' "${LOG_FILE}"
  printf '\n'
fi

if [[ -n "${EXTERNAL_TASK_FILE}" ]]; then
  [[ -f "${EXTERNAL_TASK_FILE}" ]] || die "指定的任务文件不存在: ${EXTERNAL_TASK_FILE}"
  cp "${EXTERNAL_TASK_FILE}" "${TASK_FILE}"
  if [[ "${OUTPUT_JSON}" != "true" ]]; then
    info "已复制现成任务文件。"
  fi
else
  cat > "${TASK_FILE}" <<EOF
# OpenClaw Cursor 任务

## 基本信息
- 任务 ID: ${TASK_ID}
- 会话名: ${SESSION_NAME}
- 项目路径: ${PROJECT_PATH}
- 创建时间: ${CREATED_AT}
- 优先级: ${PRIORITY}
- 预计耗时: ${ETA}

## 任务描述
${TASK_DESCRIPTION}

## 角色
你是 Cursor CLI Agent，通过 tmux 会话接收来自 OpenClaw 的任务。请在开始编码前先阅读相关代码，再按现有架构实现需求。

## 执行要求
1. 先理解项目结构和已有实现，再开始修改。
2. 遵循现有命名、风格、测试和文档约定。
3. 修改前说明要做什么，执行过程中持续输出进度。
4. 遇到阻塞时明确说明问题、已尝试方案和需要的决策。
5. 完成后给出修改文件、测试结果和后续建议。

## 标准输出格式
开始任务时输出：
\`\`\`
============================================================
开始执行: ${TASK_NAME}
工作目录: ${PROJECT_PATH}
预计耗时: ${ETA}
============================================================
\`\`\`

完成步骤时输出：
\`\`\`
已完成步骤 N: [步骤名称]
耗时: [X 分钟]
产出: [简要说明]
\`\`\`

遇到问题时输出：
\`\`\`
遇到问题: [问题描述]
详情: [详细说明]
尝试方案:
1. [方案一]
2. [方案二]
建议: [需要用户决策的内容]
\`\`\`

任务完成时输出：
\`\`\`
============================================================
任务完成: ${TASK_NAME}
总耗时: [总时间]
完成清单:
- [子任务]
修改文件:
- [文件路径] (+新增/-删除)
测试结果:
- [测试摘要]
备注:
- [重要说明]
============================================================
\`\`\`

## 运行中可能收到的控制指令
- /pause: 暂停当前推进并进入等待输入状态
- /resume: 恢复推进
- /status: 输出当前步骤、已完成事项、剩余工作
- /focus [子任务]: 缩小范围，优先处理指定部分
- /expand [需求]: 接受新增范围并说明影响
- /abort [原因]: 保存当前状态并优雅退出
EOF
  if [[ "${OUTPUT_JSON}" != "true" ]]; then
    info "已生成标准任务文件。"
  fi
fi

cat > "${STATUS_FILE}" <<EOF
{
  "taskId": "${TASK_ID}",
  "taskName": "${TASK_NAME}",
  "sessionName": "${SESSION_NAME}",
  "status": "starting",
  "projectPath": "${PROJECT_PATH}",
  "priority": "${PRIORITY}",
  "estimatedDuration": "${ETA}",
  "createdAt": "${CREATED_AT}",
  "startedAt": "${CREATED_AT}",
  "lastCheckAt": "${CREATED_AT}",
  "taskFile": "${TASK_FILE}",
  "runnerFile": "${RUNNER_FILE}",
  "logFile": "${LOG_FILE}",
  "cursor": {
    "pid": null,
    "command": "${AGENT_BIN}",
    "exitCode": null
  },
  "progress": {
    "currentStep": "准备启动 Cursor CLI",
    "completedSteps": [],
    "estimatedProgress": "0%"
  },
  "output": {
    "lastCapture": "",
    "logFile": "${LOG_FILE}"
  }
}
EOF

cat > "${RUNNER_FILE}" <<EOF
#!/usr/bin/env bash
set -euo pipefail

if [ -f ~/.bashrc ]; then . ~/.bashrc; fi

export OPENCLAW_TASK_ID='${TASK_ID}'
export OPENCLAW_SESSION_NAME='${SESSION_NAME}'
export OPENCLAW_PRIORITY='${PRIORITY}'
export OPENCLAW_ESTIMATED_DURATION='${ETA}'
export PYTHONIOENCODING='utf-8'
export PYTHONUTF8='1'
export LANG='C.UTF-8'
export LC_ALL='C.UTF-8'
export OPENCLAW_WORKSPACE_PATH='${WORKSPACE_PATH}'

PROMPT_FILE='${TASK_FILE}'
PROMPT_CONTENT="\$(cat "\${PROMPT_FILE}")"

printf '\\n[openclaw] 使用任务文件: %s\\n' "\${PROMPT_FILE}"
set +e
'${AGENT_BIN}' --trust --force --print --output-format stream-json --stream-partial-output --workspace "\${OPENCLAW_WORKSPACE_PATH}" "\${PROMPT_CONTENT}"
AGENT_EXIT_CODE="\$?"
set -e
printf '[openclaw] agent_exit_code=%s\\n' "\${AGENT_EXIT_CODE}"
exit "\${AGENT_EXIT_CODE}"
EOF
chmod +x "${RUNNER_FILE}"

if [[ "${OUTPUT_JSON}" != "true" ]]; then
  info "正在创建 tmux 会话..."
fi
tmux new-session -d -s "${SESSION_NAME}" -c "${PROJECT_PATH}"
tmux pipe-pane -o -t "${SESSION_NAME}" "cat >> '${LOG_FILE}'"

printf -v RUNNER_COMMAND 'bash %q' "${RUNNER_FILE}"
tmux send-keys -t "${SESSION_NAME}" "${RUNNER_COMMAND}" C-m
sleep 1

PANE_PID="$(pane_pid "${SESSION_NAME}")"
LAST_CAPTURE="$(capture_recent_output "${SESSION_NAME}" 30)"
LAST_CAPTURE_JSON="$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read(), ensure_ascii=False))' <<<"${LAST_CAPTURE}")"
if [[ -n "${PANE_PID}" ]]; then
  PANE_PID_VALUE="${PANE_PID}"
else
  PANE_PID_VALUE="null"
fi

update_status_file "${STATUS_FILE}" \
  "status=running" \
  "cursor.pid=${PANE_PID_VALUE}" \
  "progress.currentStep=Cursor CLI 已启动，等待任务响应" \
  "progress.estimatedProgress=5%" \
  "lastCheckAt=$(now_iso)" \
  "output.lastCapture=json:${LAST_CAPTURE_JSON}"

if [[ "${OUTPUT_JSON}" == "true" ]]; then
  python3 - "${STATUS_FILE}" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
payload = {
    "ok": True,
    "taskId": data.get("taskId"),
    "taskName": data.get("taskName"),
    "sessionName": data.get("sessionName"),
    "status": data.get("status"),
    "projectPath": data.get("projectPath"),
    "priority": data.get("priority"),
    "estimatedDuration": data.get("estimatedDuration"),
    "taskFile": data.get("taskFile"),
    "statusFile": path,
    "logFile": data.get("logFile"),
    "cursor": data.get("cursor", {}),
}
print(json.dumps(payload, ensure_ascii=False))
PY
else
  printf '\n'
  info "任务已经在后台启动。"
  print_divider
  printf '检查状态: ./scripts/check-status.sh %s\n' "${SESSION_NAME}"
  printf '实时附加: ./scripts/attach-session.sh %s\n' "${SESSION_NAME}"
  printf '发送指令: ./scripts/send-command.sh %s "补充说明"\n' "${SESSION_NAME}"
  printf '终止会话: ./scripts/kill-session.sh %s\n' "${SESSION_NAME}"
  print_divider
fi
