#!/bin/bash
# 视频质量验证脚本 - ppt-video v2.0 Phase 4
# 用法: bash verify_video.sh <video_path> [expected_pages]

VIDEO_PATH="$1"
EXPECTED_PAGES="${2:-0}"

if [ -z "$VIDEO_PATH" ]; then
    echo "❌ 用法: bash verify_video.sh <video_path> [expected_pages]"
    exit 1
fi

if [ ! -f "$VIDEO_PATH" ]; then
    echo "❌ 文件不存在: $VIDEO_PATH"
    exit 1
fi

echo "🔍 视频质量验证"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📹 文件: $(basename "$VIDEO_PATH")"
echo ""

# 1. 文件大小
SIZE=$(stat -c%s "$VIDEO_PATH" 2>/dev/null || stat -f%z "$VIDEO_PATH" 2>/dev/null)
SIZE_MB=$(echo "scale=1; $SIZE / 1048576" | bc)
if [ "$SIZE" -lt 1048576 ]; then
    echo "❌ 文件过小: ${SIZE_MB}MB (< 1MB)"
    FAIL=1
else
    echo "✅ 文件大小: ${SIZE_MB}MB"
fi

# 2. ffprobe 解析
INFO=$(ffprobe -v error -show_entries stream=codec_name,width,height,duration -show_entries format=duration,bit_rate -of json "$VIDEO_PATH" 2>&1)

VIDEO_CODEC=$(echo "$INFO" | grep -o '"codec_name": "[^"]*"' | head -1 | cut -d'"' -f4)
AUDIO_CODEC=$(echo "$INFO" | grep -o '"codec_name": "[^"]*"' | tail -1 | cut -d'"' -f4)
WIDTH=$(echo "$INFO" | grep -o '"width": [0-9]*' | head -1 | cut -d' ' -f2)
HEIGHT=$(echo "$INFO" | grep -o '"height": [0-9]*' | head -1 | cut -d' ' -f2)
DURATION=$(echo "$INFO" | grep -o '"duration": "[^"]*"' | tail -1 | cut -d'"' -f4)
BITRATE=$(echo "$INFO" | grep -o '"bit_rate": "[^"]*"' | tail -1 | cut -d'"' -f4)

# 3. 编码格式
if [ "$VIDEO_CODEC" = "h264" ]; then
    echo "✅ 视频编码: H.264"
else
    echo "⚠️ 视频编码: $VIDEO_CODEC (期望: h264)"
fi

if [ "$AUDIO_CODEC" = "aac" ]; then
    echo "✅ 音频编码: AAC"
else
    echo "⚠️ 音频编码: $AUDIO_CODEC (期望: aac)"
fi

# 4. 分辨率
if [ "$WIDTH" = "1280" ] && [ "$HEIGHT" = "720" ]; then
    echo "✅ 分辨率: ${WIDTH}x${HEIGHT}"
else
    echo "⚠️ 分辨率: ${WIDTH}x${HEIGHT} (期望: 1280x720)"
fi

# 5. 时长
echo "⏱️  总时长: ${DURATION}s"

# 6. 比特率
BITRATE_KBPS=$(echo "scale=0; $BITRATE / 1000" | bc)
echo "📊 比特率: ${BITRATE_KBPS} kbps"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 验证完成"
