#!/bin/bash
# TTS 临时文件清理脚本
# 用法：./cleanup-tts.sh [保留数量]
# 支持用户自定义目录配置

# 加载用户配置的环境变量
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
    source "${SCRIPT_DIR}/.env"
fi

KEEP_COUNT=${1:-10}
TEMP_DIR="${TEMP_DIR:-/tmp}"
TTS_BASE="${TEMP_DIR}/openclaw"
MAX_SIZE_MB=100

echo "=== TTS 文件清理 ==="
echo "保留最近 $KEEP_COUNT 个目录"
echo "最大空间：${MAX_SIZE_MB}MB"
echo "临时目录：$TTS_BASE"
echo ""

# 1. 获取所有 TTS 目录（按时间排序）
TTS_DIRS=$(ls -td ${TTS_BASE}/tts-*/ 2>/dev/null)
TOTAL_DIRS=$(echo "$TTS_DIRS" | wc -l)

if [ -z "$TTS_DIRS" ] || [ "$TOTAL_DIRS" -eq 0 ]; then
    echo "无需清理：没有 TTS 目录"
    exit 0
fi

echo "当前目录数：$TOTAL_DIRS"

# 2. 删除旧目录（保留最新的 KEEP_COUNT 个）
if [ "$TOTAL_DIRS" -gt "$KEEP_COUNT" ]; then
    DELETE_COUNT=$((TOTAL_DIRS - KEEP_COUNT))
    echo "删除 $DELETE_COUNT 个旧目录..."
    
    ls -td ${TTS_BASE}/tts-*/ 2>/dev/null | tail -n $DELETE_COUNT | while read dir; do
        rm -rf "$dir"
        echo "  已删除：$dir"
    done
else
    echo "目录数正常，无需删除"
fi

# 3. 检查总大小
TOTAL_SIZE=$(du -sm ${TTS_BASE} 2>/dev/null | cut -f1)
echo ""
echo "当前总大小：${TOTAL_SIZE}MB"

if [ "$TOTAL_SIZE" -gt "$MAX_SIZE_MB" ]; then
    echo "超过限制，清理旧文件..."
    # 删除超过一半的旧目录
    DELETE_COUNT=$((TOTAL_DIRS / 2))
    ls -td ${TTS_BASE}/tts-*/ 2>/dev/null | tail -n $DELETE_COUNT | while read dir; do
        rm -rf "$dir"
        echo "  已删除：$dir"
    done
else
    echo "空间充足"
fi

# 4. 清理脚本临时文件
echo ""
echo "清理脚本临时文件..."
rm -f ${TEMP_DIR}/feishu-test.mp3 ${TEMP_DIR}/test-voice.mp3 ${TEMP_DIR}/tts-test.mp3 2>/dev/null
rm -f ${TEMP_DIR}/feishu-audio-*.opus 2>/dev/null

echo ""
echo "=== 清理完成 ==="
echo "剩余目录数：$(ls -d ${TTS_BASE}/tts-*/ 2>/dev/null | wc -l)"
echo "剩余总大小：$(du -sh ${TTS_BASE} 2>/dev/null | cut -f1)"
