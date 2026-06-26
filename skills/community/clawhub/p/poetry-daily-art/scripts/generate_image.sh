#!/bin/bash
# 每日诗词配图脚本
# 从 poem_study_progress.json 读取最新学的诗，生成配图
set -e

OUTPUT_DIR="/Users/hwang/.openclaw/workspace/minimax-output"
mkdir -p "$OUTPUT_DIR"

PROGRESS_FILE="/Users/hwang/.openclaw/workspace/data/poem_study_progress.json"

# 从 poem_study_progress.json 读取最新学的诗名
POEM_TITLE=""
if [ -f "$PROGRESS_FILE" ]; then
    # 用 python 解析 JSON，取 studied 数组最后一个元素的 name
    POEM_TITLE=$(python3 -c "
import json
with open('$PROGRESS_FILE') as f:
    data = json.load(f)
studied = data.get('studied', [])
if studied:
    print(studied[-1].get('name', ''))
" 2>/dev/null || echo "")
fi

# fallback: 从最新 memory 文件搜索诗名
if [ -z "$POEM_TITLE" ]; then
    LATEST_MEMORY=$(ls -t /Users/hwang/.openclaw/workspace/memory/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_MEMORY" ]; then
        POEM_TITLE=$(grep -oE '《[^》]+》' "$LATEST_MEMORY" | tail -1 | tr -d '《》' || echo "")
    fi
fi

# 最终 fallback
if [ -z "$POEM_TITLE" ]; then
    POEM_TITLE="春晨"
fi

echo "今日诗词：$POEM_TITLE"

# 根据诗词标题构建中国古典风格的 prompt
PROMPT="A breathtaking landscape scene inspired by classical Chinese poetry titled '${POEM_TITLE}', traditional Chinese ink wash painting style blended with vivid photography, majestic mountains shrouded in mist, flowing rivers reflecting golden light, ancient pavilion on a cliff edge surrounded by blooming plum blossoms or bamboo, a lone scholar contemplating nature, dynamic composition with sweeping clouds and dramatic lighting, warm sunrise or cool moonlight atmosphere matching the poem's mood, birds in flight, no text or characters, ultra-detailed, cinematic quality, photorealistic masterpiece"

echo "生成图片中..."

# 清理旧图片避免混淆
rm -f "$OUTPUT_DIR"/image_*.jpg "$OUTPUT_DIR"/image_*.png 2>/dev/null

cd "$OUTPUT_DIR"
mmx image "$PROMPT" --aspect-ratio 9:16 --non-interactive 2>&1

# 找最新生成的图片
LATEST_IMG=$(ls -t "$OUTPUT_DIR"/*.jpg "$OUTPUT_DIR"/*.png 2>/dev/null | head -1)

if [ -n "$LATEST_IMG" ]; then
    echo "FOUND:$LATEST_IMG"
    echo "TITLE:$POEM_TITLE"
else
    echo "ERROR: 未找到生成的图片"
    exit 1
fi
