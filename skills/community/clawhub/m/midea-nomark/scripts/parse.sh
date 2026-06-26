#!/bin/bash
# parse-video skill - 解析视频分享链接
# 用法: bash scripts/parse.sh "<视频分享链接>"

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$SKILL_DIR/assets"

# 检测操作系统和架构
detect_binary() {
    local os_type
    local arch_type

    case "$(uname -s)" in
        Darwin*)
            os_type="darwin"
            ;;
        MINGW*|MSYS*|CYGWIN*|Windows*)
            os_type="win64"
            ;;
        *)
            os_type="linux"
            ;;
    esac

    case "$(uname -m)" in
        arm64|aarch64)
            arch_type="arm64"
            ;;
        x86_64|amd64)
            arch_type="amd64"
            ;;
        *)
            arch_type="amd64"
            ;;
    esac

    # macOS 统一用 arm64 版本（兼容 Intel Mac）
    if [[ "$os_type" == "darwin" ]]; then
        arch_type="arm64"
    fi

    echo "parse-video-${os_type}-${arch_type}"
}

# 检查参数
if [ -z "$1" ]; then
    echo "用法: bash scripts/parse.sh \"<视频分享链接>\""
    echo ""
    echo "示例:"
    echo '  bash scripts/parse.sh "https://v.douyin.com/xxx"'
    echo '  bash scripts/parse.sh "https://www.doubao.com/video-sharing?share_id=xxx&video_id=xxx"'
    echo '  bash scripts/parse.sh "https://b23.tv/xxx"'
    exit 1
fi

VIDEO_URL="$1"
BINARY_NAME=$(detect_binary)
BINARY_PATH="$ASSETS_DIR/$BINARY_NAME"

# 检查二进制文件
if [ ! -f "$BINARY_PATH" ]; then
    echo "错误: 找不到适合当前系统的二进制文件: $BINARY_NAME"
    echo "请确认已正确安装 parse-video skill"
    exit 1
fi

# 确保二进制可执行
chmod +x "$BINARY_PATH" 2>/dev/null || true

# 执行解析
echo "正在解析: $VIDEO_URL"
echo "---"
"$BINARY_PATH" parse "$VIDEO_URL"
