#!/bin/bash
# parse-video skill - 启动 HTTP 服务（Git 浅克隆版）
# 用法: bash scripts/serve.sh [端口]

set -e

# ============ 配置 ============
GITEE_REPO="https://gitee.com/qiushuihanjing/parse-video-nomark.git"
GITEE_BRANCH="master"
BIN_DIR="${HOME}/.cache/parse-video"
PORT="${1:-8080}"
# ==============================

# 检测操作系统和架构
detect_binary() {
    local os_type arch_type

    case "$(uname -s)" in
        Darwin*)  os_type="darwin" ;;
        MINGW*|MSYS*|CYGWIN*|Windows*) os_type="win64" ;;
        *)        os_type="linux" ;;
    esac

    case "$(uname -m)" in
        arm64|aarch64) arch_type="arm64" ;;
        x86_64|amd64)   arch_type="amd64" ;;
        *)              arch_type="amd64" ;;
    esac

    if [[ "$os_type" == "darwin" ]]; then
        arch_type="arm64"
    fi

    echo "parse-video-${os_type}-${arch_type}"
}

# 下载二进制（通过 git 浅克隆）
download_binary() {
    local binary_name="$1"
    local binary_path="$2"
    local git_dir="${BIN_DIR}/.git-repo"

    mkdir -p "$BIN_DIR"

    if [[ -f "$binary_path" && -x "$binary_path" ]]; then
        return 0
    fi

    echo "📦 首次使用，正在下载 $binary_name（通过 Git 克隆，约 30MB）..."

    if [[ -d "$git_dir" ]]; then
        echo "📡 更新仓库..."
        (cd "$git_dir" && git fetch --depth=1 origin "${GITEE_BRANCH}" 2>/dev/null) || {
            rm -rf "$git_dir"
        }
    fi

    if [[ ! -d "$git_dir" ]]; then
        echo "⏬ 克隆仓库（仅最新版本）..."
        rm -rf "$git_dir"
        git clone --depth=1 --branch "${GITEE_BRANCH}" "${GITEE_REPO}" "$git_dir" 2>&1
    fi

    if [[ -f "$git_dir/dist/$binary_name" ]]; then
        cp "$git_dir/dist/$binary_name" "$binary_path"
        chmod +x "$binary_path"
        echo "✅ 下载完成: $binary_path"
    else
        echo "错误: 仓库中找不到 $binary_name"
        exit 1
    fi
}

# ============ 主逻辑 ============
BINARY_NAME=$(detect_binary)
BINARY_PATH="${BIN_DIR}/${BINARY_NAME}"

download_binary "$BINARY_NAME" "$BINARY_PATH"

echo ""
echo "🚀 启动 parse-video 服务..."
echo "📍 端口: $PORT"
echo "🌐 访问 http://localhost:$PORT 查看 Web UI"
echo "按 Ctrl+C 停止服务"
echo "---"

"$BINARY_PATH" serve -p "$PORT"
