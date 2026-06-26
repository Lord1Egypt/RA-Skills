#!/bin/bash
# 冲突处理脚本
# 用法: handle_conflict.sh --mode cover|backup|update --target <dir> --source <dir>

set -euo pipefail

# 颜色支持
export TERM=${TERM:-xterm-256color}

MODE="cover"
TARGET=""
SOURCE=""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "$1"; }
err() { echo -e "${RED}❌ $1${NC}"; }

usage() {
  cat <<EOF
Usage: $0 --mode cover|backup|update --target <dir> --source <dir>
EOF
}

safe_path() {
  local path="$1"
  if [ -z "$path" ] || [ "$path" = "/" ] || [ "$path" = "." ] || [ "$path" = ".." ]; then
    return 1
  fi
  return 0
}

require_safe_path() {
  local path="$1"
  if ! safe_path "$path"; then
    err "拒绝对危险路径执行操作: '$path'"
    exit 1
  fi
}

while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2;;
    --target) TARGET="$2"; shift 2;;
    --source) SOURCE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) err "未知参数: $1"; usage; exit 1;;
  esac
done

if [ -z "$TARGET" ] || [ -z "$SOURCE" ]; then
  err "缺少 --target 或 --source"
  usage
  exit 1
fi

if [ ! -d "$SOURCE" ]; then
  err "source 目录不存在: $SOURCE"
  exit 1
fi

require_safe_path "$TARGET"
require_safe_path "$SOURCE"

TARGET_PARENT=$(dirname "$TARGET")
BACKUP_DIR="$TARGET_PARENT/backup"
TS=$(date +%Y%m%d%H%M%S)

rsync_copy() {
  local src="$1"
  local dst="$2"
  if command -v rsync >/dev/null 2>&1; then
    # -I: 忽略修改时间差异，强制覆盖（兼容 macOS）
    rsync -aI --delete "$src/" "$dst/"
  else
    require_safe_path "$dst"
    rm -rf "$dst"
    mkdir -p "$dst"
    cp -R "$src/"* "$dst/" 2>/dev/null || true
  fi
}

case "$MODE" in
  cover)
    log "${YELLOW}🧹 覆盖模式: 将覆盖旧版本${NC}"
    rm -rf "$TARGET"
    mv "$SOURCE" "$TARGET"
    ;;
  backup)
    log "${YELLOW}📦 备份模式: 备份后覆盖${NC}"
    if [ -d "$TARGET" ]; then
      mkdir -p "$BACKUP_DIR"
      local_backup="$BACKUP_DIR/$(basename "$TARGET")-$TS"
      mv "$TARGET" "$local_backup"
      log "${GREEN}✅ 已备份到: $local_backup${NC}"
    fi
    mv "$SOURCE" "$TARGET"
    ;;
  update)
    log "${YELLOW}🔄 更新模式: 仅更新配置与插件${NC}"
    if [ ! -d "$TARGET" ]; then
      log "${YELLOW}目标不存在，切换为覆盖部署${NC}"
      rm -rf "$TARGET"
      mv "$SOURCE" "$TARGET"
    else
      # 仅更新 config 与 skills
      mkdir -p "$TARGET/config" "$TARGET/skills"
      if [ -d "$SOURCE/config" ]; then
        rsync_copy "$SOURCE/config" "$TARGET/config"
      fi
      if [ -d "$SOURCE/skills" ]; then
        rsync_copy "$SOURCE/skills" "$TARGET/skills"
      fi
      # 保留其它内容，清理临时源
      rm -rf "$SOURCE"
    fi
    ;;
  *)
    err "不支持的 mode: $MODE"
    exit 1
    ;;
esac

log "${GREEN}✅ 冲突处理完成${NC}"
