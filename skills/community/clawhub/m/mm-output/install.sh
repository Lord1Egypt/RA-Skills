#!/bin/bash
# PosterGen Parser Unit - 完整安装脚本
# 执行系统依赖安装、UV 环境初始化

set -e  # 遇到错误立即退出

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查系统
if ! command -v apt-get &> /dev/null; then
    log_error "此脚本仅支持 Debian/Ubuntu 系统"
    exit 1
fi

# 安装 UV
install_uv() {
    if ! command -v uv &> /dev/null; then
        log_info "安装 UV..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    log_success "UV 版本: $(uv --version)"
}

# 安装 Python 3.12
install_python() {
    log_info "安装 Python 3.12..."
    uv python install 3.12
    log_success "Python 3.12 安装完成"
}

# 初始化 Python 环境
setup_python_env() {
    log_info "初始化 Python 虚拟环境..."
    
    cd "$SCRIPT_DIR"
    
    # 使用 Python 3.12 创建虚拟环境
    uv venv "$VENV_DIR" --python 3.12
    
    # 同步依赖
    log_info "安装项目依赖..."
    uv sync
    
    # 安装 Playwright 浏览器
    log_info "安装 Playwright Chromium..."
    uv run playwright install chromium
    
    log_success "Python 环境初始化完成"
}

# 安装系统依赖
install_system_deps() {
    log_info "安装系统依赖..."
    
    apt-get update
    
    # 中文字体
    log_info "安装中文字体..."
    apt-get install -y fonts-noto-cjk fonts-wqy-zenhei fonts-wqy-microhei
    
    # Chromium 运行依赖
    log_info "安装 Chromium 依赖..."
    apt-get install -y \
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
        libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
        libxshmfence1 libasound2 libpangocairo-1.0-0 libgtk-3-0 \
        libx11-xcb1 libxcursor1 libxi6 libxss1 libxtst6 \
        libglib2.0-0 libfontconfig1 libfreetype6 libexpat1 \
        libuuid1 libdbus-1-3 libxkbcommon0 libatspi2.0-0 \
        libwayland-client0 libwayland-egl1 libwayland-cursor0 \
        libepoxy0 libharfbuzz-icu0 libharfbuzz-gobject0 \
        libjpeg-turbo8 libpng16-16 libwebp7 libwebpdemux2 \
        libvpx7 libcurl4 libgl1-mesa-glx
    
    # 刷新字体缓存
    fc-cache -fv
    
    log_success "系统依赖安装完成"
}

# 创建 .env 示例文件
create_env_example() {
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        log_info "创建 .env 配置文件..."
        cat > "$SCRIPT_DIR/.env" << 'EOF'
# LLM API 配置
TEXT_MODEL=gpt-4.1-2025-04-14
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 或 Gemini 配置
# TEXT_MODEL=gemini-3-pro-preview
# RUNWAY_API_KEY=your-key
# RUNWAY_API_BASE=https://runway.devops.xiaohongshu.com/openai
# RUNWAY_API_VERSION=2024-12-01-preview

# Chrome 路径（可选，留空使用 Playwright 自带的 Chromium）
CHROME_EXECUTABLE_PATH=
EOF
        log_warn "请编辑 .env 文件，填入你的 API 密钥"
    fi
}

# 主安装流程
main() {
    echo "========================================"
    echo "PosterGen Parser Unit - 安装脚本"
    echo "========================================"
    echo ""
    
    log_info "开始安装..."
    
    # 安装 UV
    install_uv
    
    # 安装 Python 3.12
    install_python
    
    # 安装系统依赖
    install_system_deps
    
    # 初始化 Python 环境
    setup_python_env
    
    # 创建 .env 文件
    create_env_example
    
    echo ""
    log_success "安装完成！"
    echo ""
    echo "使用方法:"
    echo "  1. 编辑 .env 文件，填入 API 密钥"
    echo "  2. 运行测试: bash run.sh"
    echo ""
    echo "或直接执行:"
    echo "  uv run python run.py --md_path <文件.md> --output_dir ./output"
}

main "$@"
