#!/usr/bin/env bash
set -euo pipefail

RCLONE_BIN="${RCLONE_BIN:-rclone}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${OPENCLAW_ROOT:-$HOME/.openclaw/workspace}}"
NUTSTORE_REMOTE="${NUTSTORE_REMOTE:-nutstore:/openclaw-backup}"
DRY_RUN="${NUTSTORE_DRY_RUN:-0}"
AGENTS="${AGENTS:-chief backend frontend openclawbot}"
CUSTOM_BACKUP_PATHS="${CUSTOM_BACKUP_PATHS:-}"
IDENTITY_FILES=(AGENTS.md HEARTBEAT.md IDENTITY.md MEMORY.md SOUL.md TOOLS.md USER.md)

if ! command -v "$RCLONE_BIN" >/dev/null 2>&1; then
  echo "[error] rclone 未安装，请先安装 rclone" >&2
  exit 1
fi

extra_args=()
if [ "$DRY_RUN" = "1" ]; then
  extra_args+=(--dry-run)
fi

sync_dir() {
  local src="$1"
  local dst="$2"
  if [ -d "$src" ]; then
    echo "[sync] $src -> $dst"
    "$RCLONE_BIN" sync "$src" "$dst" "${extra_args[@]}"
  else
    echo "[skip] directory not found: $src"
  fi
}

copy_file() {
  local src="$1"
  local dst="$2"
  if [ -f "$src" ]; then
    echo "[copy] $src -> $dst"
    "$RCLONE_BIN" copy "$src" "$dst" "${extra_args[@]}"
  else
    echo "[skip] file not found: $src"
  fi
}

copy_file_to() {
  local src="$1"
  local dst="$2"
  if [ -f "$src" ]; then
    echo "[copyto] $src -> $dst"
    "$RCLONE_BIN" copyto "$src" "$dst" "${extra_args[@]}"
  else
    echo "[skip] file not found: $src"
  fi
}

custom_backup() {
  local agent_root="$1"
  local remote_agent_root="$2"
  local raw_path rel_path src remote_file remote_dir

  echo "[mode] custom backup"

  IFS=',' read -r -a raw_paths <<< "$CUSTOM_BACKUP_PATHS"
  for raw_path in "${raw_paths[@]}"; do
    rel_path="$(printf '%s' "$raw_path" | xargs)"

    if [ -z "$rel_path" ]; then
      continue
    fi

    case "$rel_path" in
      /*|../*|*/../*|..)
        echo "[skip] unsafe custom path: $rel_path"
        continue
        ;;
    esac

    src="$agent_root/$rel_path"
    if [ -d "$src" ]; then
      sync_dir "$src" "$remote_agent_root/$rel_path"
    elif [ -f "$src" ]; then
      remote_dir="$(dirname "$rel_path")"
      if [ "$remote_dir" = "." ]; then
        remote_file="$remote_agent_root/$rel_path"
      else
        remote_file="$remote_agent_root/$remote_dir/$(basename "$rel_path")"
      fi
      copy_file_to "$src" "$remote_file"
    else
      echo "[skip] custom path not found: $src"
    fi
  done
}

default_backup() {
  local agent_root="$1"
  local remote_agent_root="$2"
  local file

  echo "[mode] default backup"

  for file in "${IDENTITY_FILES[@]}"; do
    copy_file "$agent_root/$file" "$remote_agent_root/identity"
  done

  sync_dir "$agent_root/memory" "$remote_agent_root/memory"
}

for agent in $AGENTS; do
  agent_root="$WORKSPACE_ROOT/$agent"
  remote_agent_root="$NUTSTORE_REMOTE/$agent"

  if [ ! -d "$agent_root" ]; then
    echo "[skip] agent workspace not found: $agent_root"
    continue
  fi

  echo "[agent] backing up $agent"

  if [ -n "$CUSTOM_BACKUP_PATHS" ]; then
    custom_backup "$agent_root" "$remote_agent_root"
  else
    default_backup "$agent_root" "$remote_agent_root"
  fi
done

echo "[done] nutstore backup finished"
