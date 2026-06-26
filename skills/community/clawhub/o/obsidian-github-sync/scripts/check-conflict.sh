#!/bin/bash
# 检查 Obsidian Vault 同步冲突
#
# 环境变量配置（必需）：
#   CONFLICT_FLAG_FILE    - 冲突标记文件路径 (默认: /tmp/obsidian-sync-conflict.flag)

CONFLICT_FLAG_FILE="${CONFLICT_FLAG_FILE:-/tmp/obsidian-sync-conflict.flag}"

if [ -f "$CONFLICT_FLAG_FILE" ]; then
    echo "🚨 Obsidian Vault Git Sync Conflict Detected"
    echo ""
    echo "Details:"
    cat "$CONFLICT_FLAG_FILE"
    exit 1
else
    echo "✅ Obsidian Vault sync is healthy - no conflicts detected"
    exit 0
fi
