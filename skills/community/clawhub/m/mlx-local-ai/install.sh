#!/bin/bash

# MLX Local AI 安装脚本
# 支持 macOS Apple Silicon (M1/M2/M3/M4)

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$HOME/mlx-env"
MODEL_NAME="mlx-community/Qwen3.5-4B-OptiQ-4bit"
EMBEDDING_MODEL="BAAI/bge-base-zh-v1.5"
HF_MIRROR="https://hf-mirror.com"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统
check_system() {
    log_info "检查系统..."
    
    # 检查 macOS
    if [[ "$(uname)" != "Darwin" ]]; then
        log_error "此脚本仅支持 macOS"
        exit 1
    fi
    
    # 检查 Apple Silicon
    ARCH=$(uname -m)
    if [[ "$ARCH" != "arm64" ]]; then
        log_error "此脚本仅支持 Apple Silicon (M1/M2/M3/M4)"
        exit 1
    fi
    
    log_success "系统检测通过: macOS arm64"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装 Python"
        log_info "推荐使用 Homebrew: brew install python@3.11"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    log_success "Python 版本: $PYTHON_VERSION"
    
    # 检查 pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 未安装"
        exit 1
    fi
    
    # 检查 Homebrew (可选)
    if command -v brew &> /dev/null; then
        log_success "Homebrew 已安装"
    else
        log_warning "Homebrew 未安装 (可选)"
    fi
}

# 创建虚拟环境
create_venv() {
    log_info "创建 Python 虚拟环境..."
    
    if [[ -d "$VENV_DIR" ]]; then
        log_warning "虚拟环境已存在: $VENV_DIR"
        read -p "是否重新创建? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
        else
            log_info "跳过虚拟环境创建"
            return
        fi
    fi
    
    python3 -m venv "$VENV_DIR"
    log_success "虚拟环境创建完成: $VENV_DIR"
}

# 安装 Python 依赖
install_dependencies() {
    log_info "安装 Python 依赖..."
    
    source "$VENV_DIR/bin/activate"
    
    # 升级 pip
    pip install --upgrade pip
    
    # 安装 MLX 和 MLX-LM
    log_info "安装 MLX 和 MLX-LM..."
    pip install mlx mlx-lm
    
    # 安装 sentence-transformers (用于 Embedding)
    log_info "安装 sentence-transformers..."
    pip install sentence-transformers
    
    # 安装其他依赖
    pip install flask requests numpy
    
    log_success "Python 依赖安装完成"
}

# 下载模型
download_models() {
    log_info "下载模型 (这可能需要几分钟)..."
    
    source "$VENV_DIR/bin/activate"
    export HF_ENDPOINT="$HF_MIRROR"
    
    # 下载 LLM 模型
    log_info "下载 LLM 模型: $MODEL_NAME"
    python3 -c "from mlx_lm import load; load('$MODEL_NAME')" || {
        log_warning "LLM 模型下载可能已存在或失败，继续..."
    }
    
    # 下载 Embedding 模型
    log_info "下载 Embedding 模型: $EMBEDDING_MODEL"
    python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('$EMBEDDING_MODEL')" || {
        log_warning "Embedding 模型下载可能已存在或失败，继续..."
    }
    
    log_success "模型下载完成"
}

# 创建配置文件
create_config() {
    log_info "创建配置文件..."
    
    # 创建日志目录
    mkdir -p "$HOME/.openclaw/logs"
    
    # 创建环境变量文件
    cat > "$SCRIPT_DIR/config/env.example" << EOF
# MLX Local AI 环境变量
export HF_ENDPOINT="$HF_MIRROR"

# 百度 API (可选)
# export BAIDU_API_KEY="your-api-key"

# Tavily API (可选)
# export TAVILY_API_KEY="your-api-key"
EOF
    
    log_success "配置文件创建完成"
}

# 创建启动脚本
create_start_script() {
    log_info "创建启动脚本..."
    
    cp "$SCRIPT_DIR/start_ai.sh" "$HOME/start_ai.sh"
    chmod +x "$HOME/start_ai.sh"
    log_success "启动脚本创建完成: ~/start_ai.sh"
}

# 复制 embedding_server.py
create_embedding_server() {
    log_info "创建 Embedding 服务..."
    
    if [[ ! -f "$HOME/embedding_server.py" ]]; then
        # 从 scripts 目录复制或创建默认版本
        if [[ -f "$SCRIPT_DIR/scripts/embedding_server.py" ]]; then
            cp "$SCRIPT_DIR/scripts/embedding_server.py" "$HOME/embedding_server.py"
        else
            log_warning "embedding_server.py 不存在，请手动创建"
        fi
    fi
}

# 主安装流程
main() {
    echo ""
    echo "========================================"
    echo "   MLX Local AI 安装脚本"
    echo "========================================"
    echo ""
    
    check_system
    check_dependencies
    create_venv
    install_dependencies
    download_models
    create_config
    create_start_script
    create_embedding_server
    
    echo ""
    echo "========================================"
    echo -e "${GREEN}✅ 安装完成！${NC}"
    echo "========================================"
    echo ""
    echo "启动服务:"
    echo "  ~/start_ai.sh start"
    echo ""
    echo "检查状态:"
    echo "  ~/start_ai.sh status"
    echo ""
    echo "测试 API:"
    echo "  ~/start_ai.sh test"
    echo ""
}

# 处理命令行参数
case "${1:-}" in
    --update)
        log_info "更新模式..."
        install_dependencies
        log_success "更新完成"
        ;;
    --uninstall)
        log_info "卸载..."
        rm -rf "$VENV_DIR"
        rm -f "$HOME/start_ai.sh"
        rm -f "$HOME/embedding_server.py"
        log_success "卸载完成"
        ;;
    *)
        main
        ;;
esac
