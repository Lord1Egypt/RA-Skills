#!/bin/bash
# Nano-banana 图像生成与编辑脚本
# 用法:
#   文生图: ./image-gen.sh "图像描述" [output.png] [aspect_ratio]
#   图生图: ./image-gen.sh "图像描述" [output.png] [aspect_ratio] [参考图路径]

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 .env 文件
if [[ ! -f "$ENV_FILE" ]]; then
    log_error "未找到 .env 文件"
    echo "请在 $SCRIPT_DIR 目录下创建 .env 文件"
    echo "参考 .env.example 文件格式"
    exit 1
fi

# 加载环境变量
source "$ENV_FILE"

# 检查必要的环境变量
if [[ -z "$IMAGE_API_BASE_URL" || -z "$IMAGE_API_KEY" ]]; then
    log_error ".env 文件中缺少 IMAGE_API_BASE_URL 或 IMAGE_API_KEY"
    exit 1
fi

# 设置默认值
MODEL="${IMAGE_MODEL:-gemini-3.1-flash-image-preview}"
SIZE="${IMAGE_SIZE:-2K}"
ASPECT_RATIO="${3:-${IMAGE_ASPECT_RATIO:-1:1}}"

# 获取参数
PROMPT="$1"
OUTPUT="${2:-generated_image_$(date +%Y%m%d_%H%M%S).png}"
REFERENCE_IMAGE="$4"

if [[ -z "$PROMPT" ]]; then
    echo "用法:"
    echo "  文生图: $0 \"图像描述\" [output.png] [aspect_ratio]"
    echo "  图生图: $0 \"图像描述\" [output.png] [aspect_ratio] [参考图路径]"
    echo ""
    echo "支持的宽高比: 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 4:5, 5:4, 21:9, 1:4, 4:1, 8:1, 1:8"
    echo "支持的尺寸: 1K, 2K, 4K, 512px"
    exit 1
fi

log_info "正在生成图像..."
echo "  模型: $MODEL"
echo "  提示词: $PROMPT"
echo "  宽高比: $ASPECT_RATIO"
echo "  尺寸: $SIZE"

# 构建 JSON 请求体
if [[ -n "$REFERENCE_IMAGE" && -f "$REFERENCE_IMAGE" ]]; then
    log_info "使用参考图: $REFERENCE_IMAGE"

    # 检测图片类型
    MIME_TYPE=$(file -b --mime-type "$REFERENCE_IMAGE")

    # 转为 base64
    IMAGE_BASE64=$(base64 -w 0 "$REFERENCE_IMAGE")
    IMAGE_DATA_URI="data:${MIME_TYPE};base64,${IMAGE_BASE64}"

    log_info "参考图已转为 base64 (大小: $(echo "$IMAGE_BASE64" | wc -c) 字符)"

    # 构建 JSON，包含 image 参数
    # 使用 jq 来安全构建 JSON
    JSON_PAYLOAD=$(jq -n \
        --arg model "$MODEL" \
        --arg prompt "$PROMPT" \
        --arg aspect_ratio "$ASPECT_RATIO" \
        --arg image "$IMAGE_DATA_URI" \
        '{
            model: $model,
            prompt: $prompt,
            response_format: "url",
            aspect_ratio: $aspect_ratio,
            image: [$image]
        }')

    echo "  模式: 图生图 (Image-to-Image)"
else
    # 文生图模式
    JSON_PAYLOAD=$(cat <<EOF
{
    "model": "$MODEL",
    "prompt": "$PROMPT",
    "response_format": "url",
    "aspect_ratio": "$ASPECT_RATIO"
}
EOF
)
    echo "  模式: 文生图 (Text-to-Image)"
fi

# 调用 API
RESPONSE=$(curl -s -X POST "${IMAGE_API_BASE_URL}/v1/images/generations" \
    -H "Authorization: Bearer ${IMAGE_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD")

# 尝试解析图像 URL
# 支持多种响应格式
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.data[0].url // .url // .image_url // empty' 2>/dev/null)

if [[ -z "$IMAGE_URL" || "$IMAGE_URL" == "null" ]]; then
    log_error "未能获取图像 URL"
    echo "响应: $RESPONSE"
    exit 1
fi

# 下载图像
log_info "下载图像到 $OUTPUT..."
curl -s -o "$OUTPUT" "$IMAGE_URL"

if [[ -f "$OUTPUT" ]]; then
    log_info "✅ 图像已保存到: $OUTPUT"
    log_info "文件大小: $(du -h "$OUTPUT" | cut -f1)"
else
    log_error "图像下载失败"
    exit 1
fi
