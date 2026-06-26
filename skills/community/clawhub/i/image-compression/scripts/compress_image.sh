
#!/bin/bash

# 图片压缩脚本
# 使用 sips 命令压缩图片
# 支持调整压缩后的宽度和质量
# 作者：Honcy Ye

# 默认参数
DEFAULT_MAX_WIDTH=1024
DEFAULT_QUALITY=85
DEFAULT_MAX_SIZE=$((10 * 1024 * 1024)) # 10MB

# 输入参数
IMAGE_PATH="$1"
MAX_WIDTH="${2:-$DEFAULT_MAX_WIDTH}"
QUALITY="${3:-$DEFAULT_QUALITY}"
MAX_SIZE="${4:-$DEFAULT_MAX_SIZE}"

# 检查输入参数
if [ -z "$IMAGE_PATH" ]; then
    echo "Usage: $0 <image_path> [max_width] [quality] [max_size]"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: Image file not found"
    exit 1
fi

# 获取文件大小
FILE_SIZE=$(stat -c "%s" "$IMAGE_PATH" 2>/dev/null || stat -f "%z" "$IMAGE_PATH")

# 检查是否需要压缩
if [ "$FILE_SIZE" -le "$MAX_SIZE" ]; then
    echo "Image size is below limit, no compression needed: $IMAGE_PATH"
    echo "$IMAGE_PATH"
    exit 0
fi

# 获取文件名和扩展名
FILE_DIR=$(dirname "$IMAGE_PATH")
FILE_NAME=$(basename "$IMAGE_PATH")
FILE_EXT="${FILE_NAME##*.}"

# 生成压缩后的文件名
if [[ "$FILE_NAME" =~ .*_compressed\..* ]]; then
    OUTPUT_PATH="$IMAGE_PATH"
else
    OUTPUT_NAME="${FILE_NAME%.*}_compressed.${FILE_EXT}"
    OUTPUT_PATH="${FILE_DIR}/${OUTPUT_NAME}"
fi

# 压缩图片
if [ "$FILE_EXT" = "png" ]; then
    # PNG 压缩
    sips -Z "$MAX_WIDTH" "$IMAGE_PATH" --out "$OUTPUT_PATH"
    # PNG 优化（使用 optipng）
    if command -v optipng >/dev/null 2>&1; then
        optipng -o2 -q "$OUTPUT_PATH"
    fi
elif [ "$FILE_EXT" = "gif" ]; then
    # GIF 压缩
    sips -Z "$MAX_WIDTH" "$IMAGE_PATH" --out "$OUTPUT_PATH"
else
    # 其他格式（JPEG）
    sips -Z "$MAX_WIDTH" -s formatOptions "${QUALITY}%" "$IMAGE_PATH" --out "$OUTPUT_PATH"
fi

# 检查压缩是否成功
if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Error: Failed to compress image"
    exit 1
fi

# 获取压缩后的文件大小
COMPRESSED_SIZE=$(stat -c "%s" "$OUTPUT_PATH" 2>/dev/null || stat -f "%z" "$OUTPUT_PATH")

# 输出压缩信息
echo "Compression successful:"
echo "  Original: $IMAGE_PATH"
echo "  Size: $((FILE_SIZE / 1024)) KB"
echo "  Compressed: $OUTPUT_PATH"
echo "  Size: $((COMPRESSED_SIZE / 1024)) KB"
echo "  Compression ratio: $(( (1 - COMPRESSED_SIZE / FILE_SIZE) * 100 ))%"

# 输出压缩后的文件路径
echo "$OUTPUT_PATH"
