#!/bin/bash
# =============================================================================
# MP4 to SRT - 將本地影片轉成 SRT 字幕 (自動轉繁體)
# =============================================================================
# Author: Kuanlin
# Usage: mp4-to-srt.sh <video_file> [output.srt] [model]
# Output: SRT 字幕檔 (自動轉為繁體中文)
# =============================================================================

set -e

# 參數
VIDEO="${1:-}"
OUTPUT="${2:-}"
MODEL="${3:-small}"
CONVERT_TW="${4:-true}"

if [ -z "$VIDEO" ]; then
    echo "用法: mp4-to-srt.sh <影片檔案> [輸出.srt] [模型] [轉繁體:true/false]"
    echo "模型: tiny, base, small, medium, large"
    echo "範例: mp4-to-srt.sh video.mp4 output.srt small"
    exit 1
fi

# 檢查檔案
if [ ! -f "$VIDEO" ]; then
    echo "錯誤: 找不到檔案 $VIDEO"
    exit 1
fi

# 自動產生輸出檔名
if [ -z "$OUTPUT" ]; then
    OUTPUT="${VIDEO%.*}.srt"
fi

# 臨時檔案
TEMP_OUTPUT="${OUTPUT%.srt}_temp.srt"

echo "================================================"
echo "  MP4 to SRT 轉換 (自動轉繁體)"
echo "================================================"
echo "輸入: $VIDEO"
echo "輸出: $OUTPUT"
echo "模型: $MODEL"
echo ""

# 檢查 Whisper
if ! command -v whisper &> /dev/null; then
    echo "錯誤: 請先安裝 Whisper"
    echo "pip3 install openai-whisper"
    exit 1
fi

# 開始轉換
echo "1. Whisper 轉錄中..."
whisper "$VIDEO" --model "$MODEL" --output_format srt --output_dir "$(dirname "$TEMP_OUTPUT")" --filename_format "$(basename "$TEMP_OUTPUT" .srt)"

# 檢查 opencc
if command -v opencc &> /dev/null; then
    echo ""
    echo "2. 轉換為繁體中文..."
    opencc -i "$TEMP_OUTPUT" -o "$OUTPUT" -c s2tw.json
    
    # 刪除臨時檔案
    rm -f "$TEMP_OUTPUT"
    echo "✅ 已轉換為繁體中文"
else
    # 沒 opencc 就用原檔
    mv "$TEMP_OUTPUT" "$OUTPUT"
    echo "⚠️ opencc 未安裝，跳過轉換"
fi

echo ""
echo "✅ 完成！"
echo "輸出檔案: $OUTPUT"
