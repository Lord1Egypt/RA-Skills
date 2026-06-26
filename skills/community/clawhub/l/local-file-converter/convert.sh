#!/bin/bash
# File Converter Script
# Usage: ./convert.sh <input_file> <output_format>

set -e

INPUT="$1"
OUTPUT_FORMAT="$2"
# 默认输出到输入文件同目录，可通过环境变量 OUTPUT_DIR 覆盖
OUTPUT_DIR="${OUTPUT_DIR:-$(dirname "$INPUT")/converted}"

mkdir -p "$OUTPUT_DIR"

if [[ ! -f "$INPUT" ]]; then
    echo "错误：文件不存在 - $INPUT"
    exit 1
fi

BASENAME=$(basename "$INPUT")
NAME="${BASENAME%.*}"
OUTPUT="$OUTPUT_DIR/${NAME}.${OUTPUT_FORMAT}"

# 获取文件扩展名
EXT="${INPUT##*.}"

echo "🔄 转换：$INPUT → $OUTPUT"

# 图片转换
case "$OUTPUT_FORMAT" in
    jpg|jpeg|png|webp|gif|bmp|tiff|ico|svg)
        convert "$INPUT" "$OUTPUT"
        ;;
    heic|heif)
        convert "$INPUT" "$OUTPUT"
        ;;
esac

# 视频/音频转换
case "$OUTPUT_FORMAT" in
    mp4|avi|mkv|mov|webm|flv|wmv)
        ffmpeg -y -i "$INPUT" "$OUTPUT"
        ;;
    mp3|flac|wav|aac|ogg|m4a|wma)
        ffmpeg -y -i "$INPUT" "$OUTPUT"
        ;;
    gif)
        ffmpeg -y -i "$INPUT" -vf "fps=10,scale=500:-1" "$OUTPUT"
        ;;
esac

# 文档转换
case "$OUTPUT_FORMAT" in
    pdf)
        case "$EXT" in
            docx|doc|odt|rtf)
                libreoffice --headless --convert-to pdf "$INPUT" --outdir "$OUTPUT_DIR"
                mv "$OUTPUT_DIR/${NAME}.pdf" "$OUTPUT"
                ;;
            md|markdown)
                pandoc "$INPUT" -o "$OUTPUT"
                ;;
            *)
                libreoffice --headless --convert-to pdf "$INPUT" --outdir "$OUTPUT_DIR"
                ;;
        esac
        ;;
    docx|odt)
        libreoffice --headless --convert-to "$OUTPUT_FORMAT" "$INPUT" --outdir "$OUTPUT_DIR"
        ;;
    epub|mobi|azw3)
        ebook-convert "$INPUT" "$OUTPUT"
        ;;
esac

# 数据格式转换
case "$OUTPUT_FORMAT" in
    json|yaml|yml|xml|csv)
        # 尝试用 pandoc 或 dasel
        if command -v dasel &> /dev/null; then
            dasel -r auto -w "$OUTPUT_FORMAT" -f "$INPUT" > "$OUTPUT"
        else
            echo "提示：安装 dasel 以支持数据格式转换"
            pandoc "$INPUT" -o "$OUTPUT" 2>/dev/null || libreoffice --headless --convert-to csv "$INPUT" --outdir "$OUTPUT_DIR"
        fi
        ;;
esac

if [[ -f "$OUTPUT" ]]; then
    echo "✅ 转换成功！"
    echo "📁 输出文件：$OUTPUT"
    ls -lh "$OUTPUT"
else
    echo "❌ 转换失败"
    exit 1
fi
