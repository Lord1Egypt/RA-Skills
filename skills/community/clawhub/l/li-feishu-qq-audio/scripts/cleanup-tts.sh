#!/bin/bash
# TTS 临时文件清理脚本
# 用法：./cleanup-tts.sh [保留数量] [--weekly]
# 支持用户自定义目录配置
# 每周自动清理模式：./cleanup-tts.sh --weekly

# 加载用户配置的环境变量
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
    source "${SCRIPT_DIR}/.env"
fi

# 日志目录配置
LOG_DIR="${LOG_DIR:-/tmp/openclaw}"
LOG_FILE="${LOG_DIR}/cleanup-$(date +%Y-%m-%d).log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 日志函数（输出到日志文件和 stderr，不输出到 stdout）
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" >> "$LOG_FILE"
    echo "$msg" >&2
}

# 检查是否为每周清理模式
WEEKLY_MODE=false
KEEP_COUNT=${1:-10}

if [ "$1" = "--weekly" ]; then
    WEEKLY_MODE=true
    KEEP_COUNT=5  # 每周清理保留更少
fi

TEMP_DIR="${TEMP_DIR:-/tmp}"
TTS_BASE="${TEMP_DIR}/openclaw"
MAX_SIZE_MB=100

log "=== TTS 文件清理 ==="
log "模式：$([ "$WEEKLY_MODE" = true ] && echo "每周清理" || echo "日常清理")"
log "保留最近 $KEEP_COUNT 个目录"
log "最大空间：${MAX_SIZE_MB}MB"
log "临时目录：$TTS_BASE"
log "日志文件：$LOG_FILE"

# 1. 获取所有 TTS 目录（按时间排序）
TTS_DIRS=$(ls -td ${TTS_BASE}/tts-*/ 2>/dev/null)
TOTAL_DIRS=$(echo "$TTS_DIRS" | grep -c . 2>/dev/null || echo 0)

if [ -z "$TTS_DIRS" ] || [ "$TOTAL_DIRS" -eq 0 ]; then
    log "无需清理：没有 TTS 目录"
    exit 0
fi

log "当前目录数：$TOTAL_DIRS"

# 2. 删除旧目录（保留最新的 KEEP_COUNT 个）
if [ "$TOTAL_DIRS" -gt "$KEEP_COUNT" ]; then
    DELETE_COUNT=$((TOTAL_DIRS - KEEP_COUNT))
    log "删除 $DELETE_COUNT 个旧目录..."
    
    ls -td ${TTS_BASE}/tts-*/ 2>/dev/null | tail -n $DELETE_COUNT | while read dir; do
        rm -rf "$dir"
        log "  已删除：$dir"
    done
else
    log "目录数正常，无需删除"
fi

# 3. 检查总大小
TOTAL_SIZE=$(du -sm ${TTS_BASE} 2>/dev/null | cut -f1 || echo 0)
log "当前总大小：${TOTAL_SIZE}MB"

if [ "$TOTAL_SIZE" -gt "$MAX_SIZE_MB" ]; then
    log "超过限制，清理旧文件..."
    # 删除超过一半的旧目录
    DELETE_COUNT=$((TOTAL_DIRS / 2))
    ls -td ${TTS_BASE}/tts-*/ 2>/dev/null | tail -n $DELETE_COUNT | while read dir; do
        rm -rf "$dir"
        log "  已删除：$dir"
    done
else
    log "空间充足"
fi

# 4. 清理脚本临时文件
log "清理脚本临时文件..."
rm -f ${TEMP_DIR}/feishu-test.mp3 ${TEMP_DIR}/test-voice.mp3 ${TEMP_DIR}/tts-test.mp3 2>/dev/null
rm -f ${TEMP_DIR}/feishu-audio-*.opus 2>/dev/null

# 5. 每周清理模式：清理旧日志文件（保留 7 天）
if [ "$WEEKLY_MODE" = true ]; then
    log "执行每周日志清理..."
    find "$LOG_DIR" -name "cleanup-*.log" -type f -mtime +7 -delete 2>/dev/null
    log "已清理 7 天前的日志文件"
fi

REMAINING_DIRS=$(ls -d ${TTS_BASE}/tts-*/ 2>/dev/null | wc -l)
REMAINING_SIZE=$(du -sh ${TTS_BASE} 2>/dev/null | cut -f1 || echo "0")

log "=== 清理完成 ==="
log "剩余目录数：$REMAINING_DIRS"
log "剩余总大小：$REMAINING_SIZE"
log "日志文件：$LOG_FILE"

# 输出简洁结果到 stdout（供 cron 使用）
echo "OK: $REMAINING_DIRS dirs, $REMAINING_SIZE"
