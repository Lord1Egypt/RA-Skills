#!/bin/bash
#===============================================================================
# OpenClaw 自动备份脚本
# 
# 功能：
#   - 自动检查 OpenClaw 运行状态
#   - 备份配置文件、skills、agents、workspace、memory、credentials
#   - 上传到任意 rclone 支持的远程存储
#   - 自动轮转备份（保留最新 N 份）
#
# 使用方法：
#   ./backup.sh --remote <rclone路径> --keep <保留份数>
#
# 示例：
#   ./backup.sh --remote tencentcos:bucket/folder --keep 7
#   ./backup.sh --remote s3:bucket/backup --keep 5
#   ./backup.sh --check-only
#
# 配置定时任务（crontab）：
#   0 3 * * * /path/to/backup.sh --remote tencentcos:bucket/folder --keep 7
#===============================================================================

set -e

#-------------------------------------------------------------------------------
# 默认配置（可根据需要修改）
#-------------------------------------------------------------------------------
REMOTE_PATH=""          # ⚠️ 用户必须配置：rclone 远程路径，格式：remote:bucket/folder
KEEP_COUNT=7            # 保留的备份份数
INCLUDE_MEMORY=true     # 是否包含 memory/ 目录
INCLUDE_CONFIG=true    # 是否包含 openclaw.json 和 skills/
INCLUDE_WORKSPACE=true # 是否包含所有 workspace 目录
INCLUDE_CREDENTIALS=true # 是否包含 credentials/ 目录
INCLUDE_AGENTS=true    # 是否包含 agents/ 目录
INCLUDE_EXTENSIONS=false # 是否包含 extensions/ 目录（很大，约800MB）
CHECK_ONLY=false       # 仅检查状态，不执行备份

#-------------------------------------------------------------------------------
# 解析命令行参数
#-------------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case $1 in
    --remote)
      REMOTE_PATH="$2"
      shift 2
      ;;
    --keep)
      KEEP_COUNT="$2"
      shift 2
      ;;
    --include-memory)
      INCLUDE_MEMORY="$2"
      shift 2
      ;;
    --include-config)
      INCLUDE_CONFIG="$2"
      shift 2
      ;;
    --include-workspace)
      INCLUDE_WORKSPACE="$2"
      shift 2
      ;;
    --include-credentials)
      INCLUDE_CREDENTIALS="$2"
      shift 2
      ;;
    --include-extensions)
      INCLUDE_EXTENSIONS="$2"
      shift 2
      ;;
    --include-agents)
      INCLUDE_AGENTS="$2"
      shift 2
      ;;
    --check-only)
      CHECK_ONLY=true
      shift
      ;;
    *)
      echo "未知参数: $1"
      echo ""
      echo "用法: $0 --remote <rclone路径> --keep <保留份数>"
      echo ""
      echo "示例:"
      echo "  $0 --remote tencentcos:bucket/folder --keep 7"
      echo "  $0 --check-only"
      echo ""
      echo "完整参数说明请查看 SKILL.md"
      exit 1
      ;;
  esac
done

#-------------------------------------------------------------------------------
# 参数校验
#-------------------------------------------------------------------------------
if [[ -z "$REMOTE_PATH" ]] && [[ "$CHECK_ONLY" != "true" ]]; then
  echo "❌ 错误: 需要指定 --remote 参数"
  echo ""
  echo "用法: $0 --remote <rclone路径> --keep <保留份数>"
  echo ""
  echo "⚠️  请先配置 rclone 远程存储："
  echo "    1. 运行: rclone config"
  echo "    2. 添加新配置（如腾讯COS）"
  echo "    3. 使用格式: --remote remote-name:bucket/folder"
  echo ""
  echo "示例:"
  echo "  腾讯COS: --remote tencentcos:backup-1252695297/openclaw-backup"
  echo "  阿里OSS: --remote aliyunoss:bucket-name/backup"
  echo "  AWS S3:  --remote s3:bucket-name/backup"
  echo "  FTP:     --remote ftp:backup-folder"
  exit 1
fi

#-------------------------------------------------------------------------------
# 日志函数
#-------------------------------------------------------------------------------
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

#-------------------------------------------------------------------------------
# 检查 OpenClaw 运行状态
#-------------------------------------------------------------------------------
check_status() {
  log "检查 OpenClaw 运行状态..."
  
  if ! openclaw status > /dev/null 2>&1; then
    log "❌ OpenClaw 未运行，停止备份"
    log "请运行 'openclaw status' 查看详情"
    return 1
  fi
  
  STATUS_OUTPUT=$(openclaw status 2>&1 || true)
  # 检查是否有实际错误（排除统计信息中的数字）
  if echo "$STATUS_OUTPUT" | grep -qiE "state.*failed|error:|failed to|ERROR:|CRITICAL:"; then
    log "❌ OpenClaw 存在错误，停止备份"
    log "状态输出:"
    echo "$STATUS_OUTPUT" | head -20
    return 1
  fi
  
  log "✅ OpenClaw 运行正常"
  return 0
}

#-------------------------------------------------------------------------------
# 打包文件
#-------------------------------------------------------------------------------
create_backup() {
  log "开始备份..."
  
  # 创建临时目录
  BACKUP_DIR=$(mktemp -d)
  
  # 备份文件名
  TIMESTAMP=$(date '+%Y-%m-%d-%H%M%S')
  BACKUP_FILE="openclaw-backup-${TIMESTAMP}.tar.gz"
  BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"
  
  # OpenClaw 主目录
  OPENCLAW_DIR="/root/.openclaw"
  
  # 打包文件列表
  FILE_LIST=()
  
  #-----------------
  # 配置文件
  #-----------------
  if [[ "$INCLUDE_CONFIG" == "true" ]]; then
    if [[ -f "$OPENCLAW_DIR/openclaw.json" ]]; then
      FILE_LIST+=("openclaw.json")
    fi
    # 配置文件备份
    for bak in "$OPENCLAW_DIR"/openclaw.json.bak*; do
      [[ -f "$bak" ]] && FILE_LIST+=("$(basename "$bak")")
    done
    # skills 目录
    if [[ -d "$OPENCLAW_DIR/skills" ]]; then
      FILE_LIST+=("skills")
    fi
    # config-backups 目录
    if [[ -d "$OPENCLAW_DIR/config-backups" ]]; then
      FILE_LIST+=("config-backups")
    fi
  fi
  
  #-----------------
  # workspace 目录
  #-----------------
  if [[ "$INCLUDE_WORKSPACE" == "true" ]]; then
    for ws in "$OPENCLAW_DIR"/workspace*; do
      if [[ -d "$ws" ]]; then
        FILE_LIST+=("$(basename "$ws")")
      fi
    done
  fi
  
  #-----------------
  # memory 目录
  #-----------------
  if [[ "$INCLUDE_MEMORY" == "true" ]]; then
    if [[ -d "$OPENCLAW_DIR/memory" ]]; then
      FILE_LIST+=("memory")
    fi
    # workspace-main 下的 memory
    if [[ -d "$OPENCLAW_DIR/workspace-main/memory" ]]; then
      FILE_LIST+=("workspace-main/memory")
    fi
    if [[ -f "$OPENCLAW_DIR/workspace-main/MEMORY.md" ]]; then
      FILE_LIST+=("workspace-main/MEMORY.md")
    fi
  fi
  
  #-----------------
  # credentials 目录
  #-----------------
  if [[ "$INCLUDE_CREDENTIALS" == "true" ]]; then
    if [[ -d "$OPENCLAW_DIR/credentials" ]]; then
      FILE_LIST+=("credentials")
    fi
  fi
  
  #-----------------
  # extensions 目录
  #-----------------
  if [[ "$INCLUDE_EXTENSIONS" == "true" ]]; then
    if [[ -d "$OPENCLAW_DIR/extensions" ]]; then
      FILE_LIST+=("extensions")
    fi
  fi
  
  #-----------------
  # agents 目录
  #-----------------
  if [[ "$INCLUDE_AGENTS" == "true" ]]; then
    if [[ -d "$OPENCLAW_DIR/agents" ]]; then
      FILE_LIST+=("agents")
    fi
  fi
  
  #-----------------
  # 执行打包
  #-----------------
  log "打包文件: ${FILE_LIST[*]}"
  cd "$OPENCLAW_DIR"
  tar -czf "$BACKUP_PATH" "${FILE_LIST[@]}"
  
  local size=$(du -h "$BACKUP_PATH" | cut -f1)
  log "备份文件大小: $size"
  
  #-----------------
  # 上传
  #-----------------
  log "上传到 $REMOTE_PATH..."
  rclone copy "$BACKUP_PATH" "$REMOTE_PATH/"
  
  #-----------------
  # 备份轮转
  #-----------------
  rotate_backups
  
  #-----------------
  # 清理
  #-----------------
  rm -rf "$BACKUP_DIR"
  
  log "✅ 备份完成: $REMOTE_PATH/$BACKUP_FILE"
  
  echo ""
  echo "📦 备份文件: $BACKUP_FILE"
  echo "🌐 远程路径: $REMOTE_PATH/"
  echo "🗑️ 保留份数: $KEEP_COUNT"
}

#-------------------------------------------------------------------------------
# 备份轮转
#-------------------------------------------------------------------------------
rotate_backups() {
  log "检查备份轮转 (保留 $KEEP_COUNT 份)..."
  
  # 获取远程文件列表并排序
  local files=$(rclone lsl "$REMOTE_PATH/" 2>/dev/null | grep "openclaw-backup-" || true)
  
  if [[ -z "$files" ]]; then
    return
  fi
  
  # 按时间排序，保留最新的 KEEP_COUNT 个
  echo "$files" | sort -r -k3 | tail -n +$((KEEP_COUNT + 1)) | while read -r line; do
    local filename=$(echo "$line" | awk '{print $NF}')
    if [[ -n "$filename" ]]; then
      log "删除旧备份: $filename"
      rclone deletefile "$REMOTE_PATH/$filename" 2>/dev/null || true
    fi
  done
}

#-------------------------------------------------------------------------------
# 主程序
#-------------------------------------------------------------------------------
main() {
  if [[ "$CHECK_ONLY" == "true" ]]; then
    check_status
    exit $?
  fi
  
  # 检查状态
  if ! check_status; then
    exit 1
  fi
  
  # 执行备份
  create_backup
}

main "$@"