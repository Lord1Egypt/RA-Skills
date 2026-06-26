#!/usr/bin/env bash
set -euo pipefail

RCLONE_BIN="${RCLONE_BIN:-rclone}"
NUTSTORE_REMOTE="${NUTSTORE_REMOTE:-nutstore:/openclaw-backup}"
AGENT="${1:-chief}"
CHECK_PATH="${2:-}"

ok_count=0
warn_count=0
error_count=0

ok() {
  echo "[ok] $*"
  ok_count=$((ok_count + 1))
}

warn() {
  echo "[warn] $*"
  warn_count=$((warn_count + 1))
}

error() {
  echo "[error] $*" >&2
  error_count=$((error_count + 1))
}

path_exists() {
  local target="$1"
  "$RCLONE_BIN" lsf "$target" >/dev/null 2>&1
}

file_exists() {
  local target="$1"
  local parent base
  parent="$(dirname "$target")"
  base="$(basename "$target")"
  "$RCLONE_BIN" lsf "$parent" --files-only 2>/dev/null | grep -Fx "$base" >/dev/null 2>&1
}

if ! command -v "$RCLONE_BIN" >/dev/null 2>&1; then
  echo "[error] rclone 未安装，请先安装 rclone" >&2
  exit 1
fi

agent_remote="$NUTSTORE_REMOTE/$AGENT"
identity_remote="$agent_remote/identity"
memory_remote="$agent_remote/memory"

if path_exists "$NUTSTORE_REMOTE"; then
  ok "remote 可访问：$NUTSTORE_REMOTE"
else
  error "remote 不可访问：$NUTSTORE_REMOTE"
fi

if path_exists "$agent_remote"; then
  ok "agent 远端目录存在：$agent_remote"
else
  error "agent 远端目录不存在：$agent_remote"
fi

if path_exists "$identity_remote"; then
  ok "identity 目录存在：$identity_remote"
else
  warn "identity 目录不存在：$identity_remote"
fi

if path_exists "$memory_remote"; then
  ok "memory 目录存在：$memory_remote"
else
  warn "memory 目录不存在：$memory_remote"
fi

if [ -n "$CHECK_PATH" ]; then
  case "$CHECK_PATH" in
    /*|../*|*/../*|..)
      error "不安全的检查路径：$CHECK_PATH"
      echo "[summary] ok=$ok_count warn=$warn_count error=$error_count"
      exit 2
      ;;
  esac

  remote_target="$agent_remote/$CHECK_PATH"
  if file_exists "$remote_target"; then
    ok "指定文件存在：$remote_target"
  elif path_exists "$remote_target"; then
    ok "指定目录存在：$remote_target"
  else
    warn "指定路径不存在：$remote_target"
  fi
fi

echo "[summary] ok=$ok_count warn=$warn_count error=$error_count"

if [ "$error_count" -gt 0 ]; then
  exit 2
fi

if [ "$warn_count" -gt 0 ]; then
  exit 1
fi

exit 0
