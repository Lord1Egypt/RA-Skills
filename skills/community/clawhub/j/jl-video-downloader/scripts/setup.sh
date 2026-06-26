#!/bin/bash

# JL Video Downloader 安装和配置脚本

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# 检查并安装工具
install_tools() {
    log_info "检查系统工具..."
    
    # 检查uv
    if ! command -v uv &> /dev/null; then
        log_warning "未找到uv工具，正在安装..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        if [[ $? -eq 0 ]]; then
            log_success "uv安装成功"
            # 添加uv到PATH
            export PATH="$HOME/.cargo/bin:$PATH"
        else
            log_error "uv安装失败"
            return 1
        fi
    else
        log_success "uv已安装: $(uv --version)"
    fi
    
    # 检查ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        log_warning "未找到ffmpeg，请手动安装:"
        echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
        echo "  macOS: brew install ffmpeg"
        echo "  CentOS/RHEL: sudo yum install ffmpeg"
        return 1
    else
        log_success "ffmpeg已安装: $(ffmpeg -version | head -1)"
    fi
    
    # 安装jl-video-downloader
    log_info "安装jl-video-downloader..."
    if uv tool list | grep -q "jl-video-downloader"; then
        log_info "jl-video-downloader已安装，正在升级..."
        uv tool upgrade jl-video-downloader
    else
        uv tool install jl-video-downloader
    fi
    
    if [[ $? -eq 0 ]]; then
        log_success "jl-video-downloader安装成功"
    else
        log_error "jl-video-downloader安装失败"
        return 1
    fi
}

# 创建配置文件
create_config() {
    local config_dir="$HOME/.jl-video-downloader"
    local env_file="$config_dir/env"
    
    log_info "创建配置目录..."
    mkdir -p "$config_dir"
    
    if [[ -f "$env_file" ]]; then
        log_warning "配置文件已存在: $env_file"
        echo "是否覆盖？[y/N]"
        read -r answer
        if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
            log_info "保留现有配置文件"
            return 0
        fi
    fi
    
    # 复制示例配置文件
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local example_file="$script_dir/env.example.txt"
    
    if [[ -f "$example_file" ]]; then
        cp "$example_file" "$env_file"
        log_success "配置文件已创建: $env_file"
        log_info "请编辑该文件并设置API密钥等配置"
    else
        log_error "示例配置文件不存在: $example_file"
        return 1
    fi
}

# 创建加载环境变量的脚本
create_env_loader() {
    local config_dir="$HOME/.jl-video-downloader"
    local loader_file="$config_dir/load_env.sh"
    
    log_info "创建环境变量加载脚本..."
    
    cat > "$loader_file" << 'EOF'
#!/bin/bash

# JL Video Downloader 环境变量加载脚本
# 在shell配置文件中添加: source ~/.jl-video-downloader/load_env.sh

JL_VIDEO_ENV_FILE="$HOME/.jl-video-downloader/env"

if [[ -f "$JL_VIDEO_ENV_FILE" ]]; then
    # 安全地加载环境变量
    while IFS='=' read -r key value || [[ -n "$key" ]]; do
        # 跳过注释和空行
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        
        # 去除可能的空格和引号
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        
        # 设置环境变量
        if [[ -n "$key" && -n "$value" ]]; then
            export "$key"="$value"
        fi
    done < "$JL_VIDEO_ENV_FILE"
    
    # 创建必要的目录
    if [[ -n "${OUTPUT_DIR:-}" ]]; then
        mkdir -p "$OUTPUT_DIR"
    fi
    
    if [[ -n "${TEMP_DIR:-}" ]]; then
        mkdir -p "$TEMP_DIR"
    fi
    
    if [[ -n "${CACHE_DIR:-}" ]]; then
        mkdir -p "$CACHE_DIR"
    fi
fi
EOF
    
    chmod +x "$loader_file"
    log_success "环境变量加载脚本已创建: $loader_file"
}

# 添加到shell配置文件
add_to_shell() {
    local shell_rc=""
    
    # 检测当前shell
    if [[ -n "$ZSH_VERSION" ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        shell_rc="$HOME/.bashrc"
    else
        shell_rc="$HOME/.bashrc"
    fi
    
    local loader_file="$HOME/.jl-video-downloader/load_env.sh"
    
    if [[ ! -f "$shell_rc" ]]; then
        log_warning "未找到shell配置文件: $shell_rc"
        return 0
    fi
    
    # 检查是否已添加
    if grep -q "load_env.sh" "$shell_rc"; then
        log_info "已在 $shell_rc 中配置"
        return 0
    fi
    
    log_info "添加到shell配置文件: $shell_rc"
    
    cat >> "$shell_rc" << EOF

# JL Video Downloader 环境变量
if [[ -f "$loader_file" ]]; then
    source "$loader_file"
fi
EOF
    
    log_success "已添加到 $shell_rc"
    log_info "请运行 'source $shell_rc' 或重新打开终端使配置生效"
}

# 测试安装
test_installation() {
    log_info "测试安装..."
    
    # 测试uvx命令
    if uvx jl-video-downloader --help &> /dev/null; then
        log_success "jl-video-downloader 命令测试成功"
    else
        log_error "jl-video-downloader 命令测试失败"
        return 1
    fi
    
    # 测试download.sh脚本
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local download_script="$script_dir/download.sh"
    
    if [[ -x "$download_script" ]]; then
        if "$download_script" --help &> /dev/null; then
            log_success "download.sh 脚本测试成功"
        else
            log_error "download.sh 脚本测试失败"
            return 1
        fi
    fi
    
    log_success "所有测试通过！"
}

# 显示使用说明
show_usage() {
    cat << EOF
JL Video Downloader 安装和配置脚本

用法: $0 [选项]

选项:
  install    安装工具和创建配置（默认）
  config     仅创建配置文件
  test       测试安装
  help       显示此帮助信息

示例:
  $0 install    # 完整安装和配置
  $0 config     # 仅创建配置文件
  $0 test       # 测试安装

安装完成后，您可以使用:
  download.sh info <视频URL>      # 获取视频信息
  download.sh download <视频URL>  # 下载视频
  download.sh extract <视频URL>   # 提取文案
  download.sh process <视频URL>   # 完整处理

脚本位置: $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/
EOF
}

# 主函数
main() {
    local action="install"
    
    if [[ $# -gt 0 ]]; then
        action="$1"
    fi
    
    case "$action" in
        install)
            log_info "开始安装JL Video Downloader..."
            install_tools
            create_config
            create_env_loader
            add_to_shell
            test_installation
            log_success "安装完成！"
            ;;
        config)
            log_info "创建配置文件..."
            create_config
            create_env_loader
            log_success "配置完成！"
            ;;
        test)
            test_installation
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "未知操作: $action"
            show_usage
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"