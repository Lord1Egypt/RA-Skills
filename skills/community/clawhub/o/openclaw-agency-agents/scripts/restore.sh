#!/bin/bash
# restore.sh - 恢复默认配置

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$SKILL_DIR/../.."
BACKUP_DIR="$SKILL_DIR/backups"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

info() { echo -e "${GREEN}[OK]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!!]${RESET} $*"; }
error() { echo -e "${RED}[ERR]${RESET} $*" >&2; }

# 检查备份目录
if [ ! -d "$BACKUP_DIR" ]; then
    error "未找到备份目录: $BACKUP_DIR"
    exit 1
fi

# 列出所有备份
backups=($(ls -t "$BACKUP_DIR"))

if [ ${#backups[@]} -eq 0 ]; then
    error "没有可用的备份"
    exit 1
fi

echo "可用的备份："
for i in "${!backups[@]}"; do
    echo "  [$((i+1))] ${backups[$i]}"
done

# 如果没有指定备份，使用最新的
if [ $# -eq 0 ]; then
    BACKUP_SUBDIR="$BACKUP_DIR/${backups[0]}"
else
    index=$(( $1 - 1 ))
    if [ $index -ge 0 ] && [ $index -lt ${#backups[@]} ]; then
        BACKUP_SUBDIR="$BACKUP_DIR/${backups[$index]}"
    else
        error "无效的备份编号"
        exit 1
    fi
fi

echo ""
info "从备份恢复: $BACKUP_SUBDIR"
echo ""

# 恢复文件
for file in SOUL.md IDENTITY.md AGENTS.md; do
    if [ -f "$BACKUP_SUBDIR/$file" ]; then
        cp "$BACKUP_SUBDIR/$file" "$WORKSPACE_DIR/"
        info "已恢复 $file"
    fi
done

echo ""
info "✓ 配置已恢复到默认状态"
