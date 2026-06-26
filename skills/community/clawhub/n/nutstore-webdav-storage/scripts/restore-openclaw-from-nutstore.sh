#!/usr/bin/env bash
set -euo pipefail

RCLONE_BIN="${RCLONE_BIN:-rclone}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${OPENCLAW_ROOT:-$HOME/.openclaw/workspace}}"
RESTORE_TARGET_ROOT="${RESTORE_TARGET_ROOT:-$WORKSPACE_ROOT}"
NUTSTORE_REMOTE="${NUTSTORE_REMOTE:-nutstore:/openclaw-backup}"
DRY_RUN="${NUTSTORE_DRY_RUN:-0}"
RESTORE_FORCE="${RESTORE_FORCE:-0}"
AGENT="${1:-}"
RESTORE_SCOPE="${2:-}"
RESTORE_PATH="${3:-}"

if ! command -v "$RCLONE_BIN" >/dev/null 2>&1; then
  echo "[error] rclone 未安装，请先安装 rclone" >&2
  exit 1
fi

if [ -z "$AGENT" ] || [ -z "$RESTORE_SCOPE" ]; then
  cat <<EOF >&2
用法：
  bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief identity
  bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief memory
  bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md
  bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh backend path docs/reports

说明：
  - 第 1 个参数：agent 名称（如 chief / backend / frontend / openclawbot）
  - 第 2 个参数：恢复范围，支持 identity / memory / path
  - 第 3 个参数：仅在 path 模式下必填，为 agent 工作区内相对路径
  - 设 NUTSTORE_DRY_RUN=1 可执行 dry-run
  - 设 RESTORE_TARGET_ROOT=/some/test/dir 可恢复到安全测试目录，而不是正式工作区
  - 如 path 模式目标是正式工作区，需显式设 RESTORE_FORCE=1 才允许执行
EOF
  exit 2
fi

extra_args=()
if [ "$DRY_RUN" = "1" ]; then
  extra_args+=(--dry-run)
fi

agent_root="$RESTORE_TARGET_ROOT/$AGENT"

require_force_for_live_path_restore() {
  if [ "$RESTORE_SCOPE" != "path" ]; then
    return 0
  fi

  if [ "$RESTORE_TARGET_ROOT" != "$WORKSPACE_ROOT" ]; then
    return 0
  fi

  if [ "$RESTORE_FORCE" = "1" ]; then
    return 0
  fi

  echo "[error] path 模式恢复到正式工作区时必须显式确认：RESTORE_FORCE=1" >&2
  echo "[hint] 如需安全验收，优先设置 RESTORE_TARGET_ROOT 到测试目录" >&2
  exit 2
}

restore_scope_default() {
  local scope="$1"
  local remote_path destination

  remote_path="$NUTSTORE_REMOTE/$AGENT/$scope"
  if [ "$scope" = "identity" ]; then
    destination="$agent_root"
  else
    destination="$agent_root/memory"
  fi

  mkdir -p "$destination"
  echo "[restore] $remote_path -> $destination"
  "$RCLONE_BIN" copy "$remote_path" "$destination" "${extra_args[@]}"
}

restore_custom_path() {
  local rel_path="$1"
  local remote_path destination remote_dir remote_name remote_type

  if [ -z "$rel_path" ]; then
    echo "[error] path 模式必须提供第 3 个参数（agent 工作区内相对路径）" >&2
    exit 2
  fi

  case "$rel_path" in
    /*|../*|*/../*|..)
      echo "[error] 不安全的恢复路径：$rel_path" >&2
      exit 2
      ;;
  esac

  remote_path="$NUTSTORE_REMOTE/$AGENT/$rel_path"
  destination="$agent_root/$rel_path"
  remote_dir="$NUTSTORE_REMOTE/$AGENT/$(dirname "$rel_path")"
  remote_name="$(basename "$rel_path")"

  remote_type="$($RCLONE_BIN lsf "$remote_dir" --format p --files-only 2>/dev/null | grep -Fx "$remote_name" || true)"

  if [ -n "$remote_type" ]; then
    mkdir -p "$(dirname "$destination")"
    echo "[restore-file] $remote_path -> $destination"
    "$RCLONE_BIN" copyto "$remote_path" "$destination" "${extra_args[@]}"
  else
    mkdir -p "$destination"
    echo "[restore-dir] $remote_path -> $destination"
    "$RCLONE_BIN" copy "$remote_path" "$destination" "${extra_args[@]}"
  fi
}

case "$RESTORE_SCOPE" in
  identity|memory)
    restore_scope_default "$RESTORE_SCOPE"
    ;;
  path)
    require_force_for_live_path_restore
    restore_custom_path "$RESTORE_PATH"
    ;;
  *)
    echo "[error] 不支持的恢复范围：$RESTORE_SCOPE（仅支持 identity / memory / path）" >&2
    exit 2
    ;;
esac

echo "[done] restore finished"
