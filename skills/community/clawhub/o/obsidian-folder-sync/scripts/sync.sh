#!/bin/bash
# Obsidian Folder Sync — 将任意文件夹同步到 Obsidian Vault
# 用法: bash sync.sh <源目录> <目标Vault> [目标子目录]
#
# 示例:
#   bash sync.sh ~/my-notes /Users/me/Obsidian/MyVault
#   bash sync.sh ~/projects/notes /Users/me/Obsidian/MyVault Notes

set -e

SOURCE_DIR="${1:-}"
OBSIDIAN_VAULT="${2:-}"
DEST_SUBDIR="${3:-}"
LOG_FILE="${HOME}/.openclaw/workspace/logs/obsidian-folder-sync.log"
TMP_DIR="/tmp/obsidian-folder-sync-$$"

usage() {
    echo "用法: $0 <源目录> <目标Vault> [目标子目录]"
    echo ""
    echo "参数:"
    echo "  源目录       要同步的文件夹路径（必填）"
    echo "  目标Vault    Obsidian Vault 路径（必填）"
    echo "  目标子目录   Vault内的目标子文件夹（可选，默认：源目录名）"
    echo ""
    echo "示例:"
    echo "  $0 ~/my-notes /Users/me/Obsidian/MyVault"
    echo "  $0 ~/projects/notes /Users/me/Obsidian/MyVault Notes"
    exit 1
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查参数
if [ -z "$SOURCE_DIR" ] || [ -z "$OBSIDIAN_VAULT" ]; then
    usage
fi

# 解析绝对路径
SOURCE_DIR="$(cd "$SOURCE_DIR" 2>/dev/null && pwd)"
if [ -z "$SOURCE_DIR" ] || [ ! -d "$SOURCE_DIR" ]; then
    echo "错误: 源目录不存在: $1"
    exit 1
fi

if [ ! -d "$OBSIDIAN_VAULT" ]; then
    echo "错误: Obsidian Vault 不存在: $OBSIDIAN_VAULT"
    exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"

# 确定目标子目录（默认为源目录名）
if [ -z "$DEST_SUBDIR" ]; then
    DEST_SUBDIR="$(basename "$SOURCE_DIR")"
fi

DEST_DIR="$OBSIDIAN_VAULT/$DEST_SUBDIR"

log "========== Obsidian Folder Sync 开始 =========="
log "📂 源:      $SOURCE_DIR"
log "📂 目标:    $DEST_DIR"
log "📋 文件:    *.md (Markdown文件)"
log "📋 排除:   node_modules, .git, __pycache__, .venv"

mkdir -p "$TMP_DIR"
mkdir -p "$DEST_DIR"

# 收集所有 .md 文件（排除指定目录）
find "$SOURCE_DIR" -name "*.md" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.venv/*" \
    -not -path "*/.clawhub/*" \
    -not -path "*/.learnings/*" \
    2>/dev/null | sed "s|^$SOURCE_DIR/||" > "$TMP_DIR/files.txt"

FILE_COUNT=$(wc -l < "$TMP_DIR/files.txt" | tr -d ' ')

if [ -z "$FILE_COUNT" ] || [ "$FILE_COUNT" = "0" ]; then
    log "⚠️  未找到 .md 文件"
    rm -rf "$TMP_DIR"
    exit 0
fi

# 使用 rsync 同步（--include='*' 在 --exclude='*' 之前是关键）
rsync -av --files-from="$TMP_DIR/files.txt" \
    --include='*' --exclude='*' \
    "$SOURCE_DIR/" "$DEST_DIR/" 2>/dev/null

log "✅ 同步完成 ($FILE_COUNT 个 .md 文件)"

rm -rf "$TMP_DIR"
log "========== 完成 =========="
