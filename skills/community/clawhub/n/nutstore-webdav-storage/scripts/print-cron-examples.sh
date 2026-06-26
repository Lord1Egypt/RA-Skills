#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-${OPENCLAW_ROOT:-$HOME/.openclaw/workspace}}"
AGENT="${1:-chief}"
CUSTOM_PATHS_EXAMPLE="${CUSTOM_PATHS_EXAMPLE:-docs/reports,docs/decisions}"
DEFAULT_CRON="${DEFAULT_CRON:-0 2 * * *}"
CUSTOM_CRON="${CUSTOM_CRON:-30 2 * * *}"
DEFAULT_LOG_NAME="${DEFAULT_LOG_NAME:-nutstore-backup.log}"
CUSTOM_LOG_NAME="${CUSTOM_LOG_NAME:-nutstore-custom-backup.log}"
AGENT_DIR="$WORKSPACE_ROOT/$AGENT"

cat <<EOF
# nutstore-webdav-storage cron examples
#
# 使用前提：
# 1. 已完成 rclone nutstore remote 配置
# 2. 已手动完成至少一次默认备份验证
# 3. 已完成至少一次恢复 dry-run
# 4. 建议先确认目录存在：$AGENT_DIR
#
# 当前参数：
# - AGENT=$AGENT
# - WORKSPACE_ROOT=$WORKSPACE_ROOT
# - DEFAULT_CRON=$DEFAULT_CRON
# - CUSTOM_CRON=$CUSTOM_CRON
# - CUSTOM_PATHS_EXAMPLE=$CUSTOM_PATHS_EXAMPLE
#
# 建议先创建日志目录：
#   mkdir -p "$AGENT_DIR/temp"
#
# 默认备份 cron
$DEFAULT_CRON cd "$AGENT_DIR" && bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh >> temp/$DEFAULT_LOG_NAME 2>&1
#
# 自定义备份 cron（仅在明确要求固定备份额外目录时启用）
$CUSTOM_CRON cd "$AGENT_DIR" && CUSTOM_BACKUP_PATHS="$CUSTOM_PATHS_EXAMPLE" AGENTS="$AGENT" bash skills/nutstore-webdav-storage/scripts/backup-openclaw-to-nutstore.sh >> temp/$CUSTOM_LOG_NAME 2>&1
EOF
