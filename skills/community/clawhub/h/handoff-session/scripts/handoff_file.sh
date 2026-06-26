#!/usr/bin/env bash
set -euo pipefail

HANDOFF_ROOT="${HANDOFF_ROOT:-$HOME/.agents/handoff_context}"

usage() {
  cat <<USAGE
Usage:
  handoff_file.sh create [topic]    # 创建 handoff 目录和模板，输出路径
  handoff_file.sh latest            # 输出最近一次 handoff.md 的路径
  handoff_file.sh resolve <id>      # 输出指定 ID 的 handoff.md 路径
  handoff_file.sh list [n]          # 列出最近 n 条（默认 5）
USAGE
}

generate_id() {
  local ts
  local rand
  ts="$(date '+%Y%m%d-%H%M')"
  rand="$(head -c 4 /dev/urandom | xxd -p)"
  printf '%s-%s' "$ts" "$rand"
}

latest_project_session() {
  local project_path="$1"
  local files=()

  [ -d "$project_path" ] || return 0

  shopt -s nullglob
  files=("$project_path"/*.jsonl)
  shopt -u nullglob

  [ "${#files[@]}" -gt 0 ] || return 0
  ls -t "${files[@]}" 2>/dev/null | head -n 1 || true
}

get_session_id() {
  if [ -n "${CODEX_THREAD_ID:-}" ]; then
    printf '%s\n' "$CODEX_THREAD_ID"
    return
  fi

  if [ -n "${CODEX_TUI_SESSION_LOG_PATH:-}" ]; then
    basename "$CODEX_TUI_SESSION_LOG_PATH" .jsonl
    return
  fi

  if [ -n "${CLAUDE_SESSION_ID:-}" ]; then
    printf '%s\n' "$CLAUDE_SESSION_ID"
    return
  fi

  local cwd
  local project_dir
  local session_file

  cwd="$(pwd)"
  project_dir="$(printf '%s' "$cwd" | sed 's|^/|-|' | tr '/._' '---')"

  session_file="$(latest_project_session "$HOME/.claude/projects/$project_dir")"
  if [ -n "$session_file" ]; then
    basename "$session_file" .jsonl
    return
  fi

  session_file="$(latest_project_session "$HOME/.codex/projects/$project_dir")"
  if [ -n "$session_file" ]; then
    basename "$session_file" .jsonl
    return
  fi

  echo ""
}

latest_handoff_dir() {
  local dirs=()

  [ -d "$HANDOFF_ROOT" ] || return 1

  shopt -s nullglob
  dirs=("$HANDOFF_ROOT"/*/)
  shopt -u nullglob

  [ "${#dirs[@]}" -gt 0 ] || return 1
  printf '%s\n' "${dirs[@]}" | sort -r | head -n 1
}

list_handoff_dirs() {
  local n="$1"
  local dirs=()

  [ -d "$HANDOFF_ROOT" ] || return 1

  shopt -s nullglob
  dirs=("$HANDOFF_ROOT"/*/)
  shopt -u nullglob

  [ "${#dirs[@]}" -gt 0 ] || return 1
  printf '%s\n' "${dirs[@]}" | sort -r | head -n "$n"
}

create_template() {
  local target_file="$1"
  local topic="$2"
  local handoff_id="$3"
  local session_id="$4"
  local timestamp="$5"

  cat > "$target_file" <<DOC
# Handoff：$topic

- 时间：$timestamp
- Handoff ID：$handoff_id
- Session ID：${session_id:-N/A}

## 当前任务
- 未记录

## 当前状态
- 未记录

## 已完成
- 未记录

## 关键决策
- 未记录

## 关键约束
- 未记录

## 关键文件
- 未记录

## 下一步
- 未记录

## 待确认
- 无
DOC
}

mode="${1:-}"
[ -n "$mode" ] || { usage; exit 1; }
shift || true

case "$mode" in
  create)
    topic="${1:-}"
    handoff_id="$(generate_id)"
    session_id="$(get_session_id)"
    timestamp="$(date '+%Y-%m-%d %H:%M')"
    safe_topic="$(printf '%s' "${topic:-handoff}" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
    target_dir="$HANDOFF_ROOT/$handoff_id"

    mkdir -p "$target_dir"
    create_template "$target_dir/handoff.md" "$safe_topic" "$handoff_id" "$session_id" "$timestamp"
    printf '%s\n' "$target_dir/handoff.md"
    ;;

  latest)
    latest_dir="$(latest_handoff_dir || true)"
    if [ -z "$latest_dir" ] || [ ! -f "${latest_dir}handoff.md" ]; then
      echo "No handoff found." >&2
      exit 1
    fi
    printf '%s\n' "${latest_dir}handoff.md"
    ;;

  resolve)
    id="${1:-}"
    [ -n "$id" ] || { echo "Usage: handoff_file.sh resolve <handoff_id>" >&2; exit 1; }
    target="$HANDOFF_ROOT/$id/handoff.md"
    [ -f "$target" ] || { echo "Handoff not found: $id" >&2; exit 1; }
    printf '%s\n' "$target"
    ;;

  list)
    n="${1:-5}"
    handoff_dirs="$(list_handoff_dirs "$n" || true)"

    if [ -z "$handoff_dirs" ]; then
      echo "No handoff found." >&2
      exit 1
    fi

    printf '%s\n' "$handoff_dirs" | while read -r dir; do
      [ -n "$dir" ] || continue
      dir_name="$(basename "$dir")"
      title="$(head -n 1 "$dir/handoff.md" 2>/dev/null | sed 's/^# Handoff：//' || echo "unknown")"
      printf '%s  %s\n' "$dir_name" "$title"
    done
    ;;

  *)
    usage
    exit 1
    ;;
esac
