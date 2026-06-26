#!/bin/bash
# parse-video skill - 启动 HTTP 服务
# 用法: bash scripts/serve.sh [端口]

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$SKILL_DIR/assets"
PORT="${1:-8080}"

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

    # macOS 统一用 arm64 版本
    if [[ "$os_type" == "darwin" ]]; then
        arch_type="arm64"
    fi

    echo "parse-video-${os_type}-${arch_type}"
}

BINARY_NAME=$(detect_binary)
BINARY_PATH="$ASSETS_DIR/$BINARY_NAME"

# 检查二进制文件
if [ ! -f "$BINARY_PATH" ]; then
    echo "错误: 找不到适合当前系统的二进制文件: $BINARY_NAME"
    exit 1
fi

# 确保二进制可执行
chmod +x "$BINARY_PATH" 2>/dev/null || true

echo "启动 parse-video 服务..."
echo "端口: $PORT"
echo "访问 http://localhost:$PORT 查看 Web UI"
echo "按 Ctrl+C 停止服务"
echo "---"

# 启动服务
"$BINARY_PATH" serve -p "$PORT"
