#!/usr/bin/env bash
set -euo pipefail

CLAUDE_CLI=${CLAUDE_CLI:-claude}
CODEX_CLI=${CODEX_CLI:-codex}
GEMINI_CLI=${GEMINI_CLI:-gemini}
REQUIRED_CMDS=("git" "$CLAUDE_CLI" "$CODEX_CLI" "$GEMINI_CLI" "jq")
ALLOW_DIRTY=${ALLOW_DIRTY:-0}
DRY_RUN=0
PLAN_FILE=""
PLAN_PROMPT=""
BACKEND_PROMPT=""
FRONTEND_PROMPT=""
REVIEW_PROMPT=""
CONTEXT_FILE=""

usage() {
  cat <<'USAGE'
用法: scripts/ccg_orchestrator.sh <plan-file> [--plan-prompt "..."] --backend "..." --frontend "..." [--review "..."] [--context PATH] [--allow-dirty] [--dry-run]

必填:
  <plan-file>      计划输出路径（例：.claude/plan.md）
  --backend        提供给 Codex 的后端指令
  --frontend       提供给 Gemini 的前端指令

可选:
  --plan-prompt    Claude 生成 plan 的提示语
  --review         Claude review 的提示语
  --context        额外上下文文件，传给 Claude plan/review
  --allow-dirty    跳过 git 工作区整洁检查（默认禁止）
  --dry-run        仅打印即将执行的命令
USAGE
}

log() { printf '[ccg] %s\n' "$*" >&2; }

die() { printf '[ccg][error] %s\n' "$*" >&2; exit 1; }

require_cmds() {
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      die "缺少命令: $cmd。请先安装 Claude Code CLI、Codex CLI、Gemini CLI 与 jq。"
    fi
  done
}

require_clean_git() {
  git update-index -q --refresh || true
  if [[ "$ALLOW_DIRTY" != "1" ]] && ! git diff --quiet --ignore-submodules HEAD --; then
    die "工作区存在未提交修改。请提交或设置 ALLOW_DIRTY=1。"
  fi
}

run_cmd() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "[dry-run] $*"
  else
    "$@"
  fi
}

run_claude_plan() {
  [[ -z "$PLAN_PROMPT" ]] && return 0
  mkdir -p "$(dirname "$PLAN_FILE")"
  local cmd=("$CLAUDE_CLI" run --prompt "$PLAN_PROMPT" --output "$PLAN_FILE")
  if [[ -n "$CONTEXT_FILE" ]]; then
    cmd+=(--context "$CONTEXT_FILE")
  fi
  log "调用 Claude 生成计划 -> $PLAN_FILE"
  run_cmd "${cmd[@]}"
}

run_codex_backend() {
  [[ -z "$BACKEND_PROMPT" ]] && die "必须提供 --backend 提示语"
  local cmd=("$CODEX_CLI" exec --prompt "$BACKEND_PROMPT" --plan "$PLAN_FILE")
  log "调用 Codex 执行后端任务"
  run_cmd "${cmd[@]}"
}

run_gemini_frontend() {
  [[ -z "$FRONTEND_PROMPT" ]] && die "必须提供 --frontend 提示语"
  local cmd=("$GEMINI_CLI" run --prompt "$FRONTEND_PROMPT" --plan "$PLAN_FILE")
  log "调用 Gemini 执行前端任务"
  run_cmd "${cmd[@]}"
}

run_claude_review() {
  [[ -z "$REVIEW_PROMPT" ]] && return 0
  local review_file="$(dirname "$PLAN_FILE")/review.md"
  local cmd=("$CLAUDE_CLI" run --prompt "$REVIEW_PROMPT" --output "$review_file" --context "$PLAN_FILE")
  log "调用 Claude 生成 review -> $review_file"
  run_cmd "${cmd[@]}"
}

parse_args() {
  [[ $# -lt 1 ]] && usage && exit 1
  PLAN_FILE=$1
  shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --plan-prompt)
        PLAN_PROMPT=$2; shift 2 ;;
      --backend)
        BACKEND_PROMPT=$2; shift 2 ;;
      --frontend)
        FRONTEND_PROMPT=$2; shift 2 ;;
      --review)
        REVIEW_PROMPT=$2; shift 2 ;;
      --context)
        CONTEXT_FILE=$2; shift 2 ;;
      --allow-dirty)
        ALLOW_DIRTY=1; shift ;;
      --dry-run)
        DRY_RUN=1; shift ;;
      --help|-h)
        usage; exit 0 ;;
      *)
        die "未知参数: $1" ;;
    esac
  done
}

main() {
  parse_args "$@"
  [[ -z "$BACKEND_PROMPT" ]] && die "缺少 --backend"
  [[ -z "$FRONTEND_PROMPT" ]] && die "缺少 --frontend"

  require_cmds
  require_clean_git
  run_claude_plan
  run_codex_backend
  run_gemini_frontend
  run_claude_review
  log "ccg orchestrator 完成"
}

main "$@"
