#!/usr/bin/env bash
# 附加到运行中的 tmux 会话

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
  cat <<'EOF'
用法:
  ./scripts/attach-session.sh <会话名或任务别名>

说明:
  不带参数时列出所有已记录会话，方便你挑选后再附加。
EOF
}

ensure_runtime_dirs
require_command tmux "请先安装 tmux 3.3+。"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -eq 0 ]]; then
  print_title "可附加的会话"
  LIST_OUTPUT="$(list_known_sessions)"
  if [[ -z "${LIST_OUTPUT}" ]]; then
    info "当前没有已记录会话。"
    exit 0
  fi
  while IFS=$'\t' read -r session_name status task_name; do
    [[ -n "${session_name}" ]] || continue
    printf '%-38s %-12s %s\n' "${session_name}" "${status}" "${task_name}"
  done <<<"${LIST_OUTPUT}"
  printf '\n'
  info "请重新执行并传入具体会话名，例如: ./scripts/attach-session.sh myproj-auth-20260318-180000"
  exit 0
fi

SESSION_QUERY="$1"
SESSION_NAME="$(resolve_session_name "${SESSION_QUERY}")" || die "未找到匹配会话: ${SESSION_QUERY}"

session_exists "${SESSION_NAME}" || die "tmux 会话不存在或已结束: ${SESSION_NAME}"

print_title "附加到 tmux 会话"
printf '会话名称: %s\n' "${SESSION_NAME}"
printf '\n'
printf '%s\n' "分离会话请按: Ctrl+B, D"
printf '%s\n' "发送中断请按: Ctrl+C"
printf '%s\n' "直接退出 shell 会终止当前任务，请谨慎操作。"
printf '\n'

tmux attach -t "${SESSION_NAME}"
