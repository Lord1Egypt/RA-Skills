#!/bin/bash
# Hermes 系统部署脚本

set -e  # 遇到错误立即退出

# 颜色定义
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

# 配置变量
VERSION="1.0.0"
DEFAULT_WORKSPACE="$HOME/.openclaw/workspace"
DEFAULT_ENVIRONMENT="production"

# 解析参数
WORKSPACE="$DEFAULT_WORKSPACE"
ENVIRONMENT="$DEFAULT_ENVIRONMENT"
FORCE=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --workspace)
            WORKSPACE="$2"
            shift 2
            ;;
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --workspace DIR     OpenClaw 工作空间目录 (默认: $DEFAULT_WORKSPACE)"
            echo "  --environment ENV   运行环境 (development|staging|production) (默认: $DEFAULT_ENVIRONMENT)"
            echo "  --force             强制重新部署"
            echo "  --verbose           详细输出"
            echo "  --help              显示帮助信息"
            exit 0
            ;;
        *)
            log_error "未知参数: $1"
            exit 1
            ;;
    esac
done

# 验证环境
validate_environment() {
    log_info "验证环境..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_info "Python 版本: $PYTHON_VERSION"
    
    # 检查 PyYAML
    if ! python3 -c "import yaml" &> /dev/null; then
        log_error "PyYAML 未安装，请运行: pip install pyyaml"
        exit 1
    fi
    
    # 检查工作空间
    if [ ! -d "$WORKSPACE" ]; then
        log_warning "工作空间目录不存在: $WORKSPACE"
        if [ "$FORCE" = true ]; then
            log_info "强制模式，创建目录..."
            mkdir -p "$WORKSPACE"
        else
            log_error "请使用 --force 创建目录或指定正确的工作空间"
            exit 1
        fi
    fi
    
    log_success "环境验证通过"
}

# 备份现有部署
backup_existing() {
    local backup_dir="$WORKSPACE/backups"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$backup_dir/hermes_$timestamp"
    
    if [ -d "$WORKSPACE/hermes" ]; then
        log_info "备份现有部署..."
        
        mkdir -p "$backup_dir"
        
        if cp -r "$WORKSPACE/hermes" "$backup_path"; then
            log_success "现有部署已备份到: $backup_path"
            
            # 清理旧备份（保留最近5个）
            ls -1td "$backup_dir/hermes_"* 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
        else
            log_warning "备份失败，继续部署..."
        fi
    else
        log_info "没有现有部署需要备份"
    fi
}

# 创建目录结构
create_directories() {
    log_info "创建目录结构..."
    
    local directories=(
        "$WORKSPACE/hermes"
        "$WORKSPACE/hermes/bin"
        "$WORKSPACE/hermes/config"
        "$WORKSPACE/hermes/data"
        "$WORKSPACE/hermes/logs"
        "$WORKSPACE/hermes/cache"
        "$WORKSPACE/memory"
        "$WORKSPACE/trajectories"
        "$WORKSPACE/skill_analysis"
        "$WORKSPACE/skill_approvals"
        "$WORKSPACE/code_cases"
    )
    
    for dir in "${directories[@]}"; do
        if mkdir -p "$dir"; then
            if [ "$VERBOSE" = true ]; then
                log_info "创建目录: $dir"
            fi
        else
            log_error "创建目录失败: $dir"
            exit 1
        fi
    done
    
    log_success "目录结构创建完成"
}

# 复制文件
copy_files() {
    log_info "复制文件..."
    
    # 获取脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    
    # 复制可执行文件
    if [ -d "$PROJECT_DIR/bin" ]; then
        cp -r "$PROJECT_DIR/bin/"* "$WORKSPACE/hermes/bin/"
        chmod +x "$WORKSPACE/hermes/bin/"*
        log_info "复制可执行文件"
    fi
    
    # 复制配置文件
    if [ -d "$PROJECT_DIR/config" ]; then
        cp -r "$PROJECT_DIR/config/"* "$WORKSPACE/hermes/config/"
        log_info "复制配置文件"
        
        # 应用环境配置
        local env_config="$PROJECT_DIR/config/profiles/$ENVIRONMENT.yaml"
        if [ -f "$env_config" ]; then
            cp "$env_config" "$WORKSPACE/hermes/config/environment.yaml"
            log_info "应用环境配置: $ENVIRONMENT"
        else
            log_warning "环境配置不存在: $ENVIRONMENT，使用默认配置"
        fi
    fi
    
    # 复制源代码（创建符号链接）
    if [ -d "$PROJECT_DIR/src" ]; then
        local src_link="$WORKSPACE/hermes/src"
        if [ -L "$src_link" ]; then
            rm "$src_link"
        fi
        
        if ln -s "$PROJECT_DIR/src" "$src_link"; then
            log_info "创建源代码符号链接"
        else
            log_warning "创建符号链接失败，尝试复制文件..."
            cp -r "$PROJECT_DIR/src" "$WORKSPACE/hermes/"
        fi
    fi
    
    # 复制文档
    if [ -d "$PROJECT_DIR/docs" ]; then
        cp -r "$PROJECT_DIR/docs" "$WORKSPACE/hermes/"
        log_info "复制文档"
    fi
    
    # 创建版本文件
    echo "$VERSION" > "$WORKSPACE/hermes/VERSION"
    
    log_success "文件复制完成"
}

# 初始化系统
initialize_system() {
    log_info "初始化系统..."
    
    local init_script="$WORKSPACE/hermes/bin/hermes-init"
    
    if [ -x "$init_script" ]; then
        if "$init_script" --workspace "$WORKSPACE" --config "$WORKSPACE/hermes/config/hermes.yaml" --environment "$ENVIRONMENT"; then
            log_success "系统初始化完成"
        else
            log_error "系统初始化失败"
            exit 1
        fi
    else
        log_warning "初始化脚本不存在或不可执行，跳过初始化"
    fi
}

# 验证部署
validate_deployment() {
    log_info "验证部署..."
    
    local status_script="$WORKSPACE/hermes/bin/hermes-status"
    
    if [ -x "$status_script" ]; then
        if "$status_script" --workspace "$WORKSPACE" --health --quiet; then
            log_success "部署验证通过"
        else
            log_error "部署验证失败"
            exit 1
        fi
    else
        log_warning "状态检查脚本不存在，跳过验证"
    fi
}

# 显示部署信息
show_deployment_info() {
    log_success "🎉 Hermes 系统部署完成!"
    echo ""
    echo "📊 部署信息:"
    echo "   版本: $VERSION"
    echo "   环境: $ENVIRONMENT"
    echo "   工作空间: $WORKSPACE"
    echo "   配置目录: $WORKSPACE/hermes/config"
    echo "   数据目录: $WORKSPACE/hermes/data"
    echo "   日志目录: $WORKSPACE/hermes/logs"
    echo ""
    echo "🚀 下一步:"
    echo "   1. 检查配置: cat $WORKSPACE/hermes/config/hermes.yaml"
    echo "   2. 启动系统: $WORKSPACE/hermes/bin/hermes-start"
    echo "   3. 验证状态: $WORKSPACE/hermes/bin/hermes-status --health"
    echo "   4. 查看日志: tail -f $WORKSPACE/hermes/logs/hermes.log"
    echo ""
    echo "🔧 管理命令:"
    echo "   启动: $WORKSPACE/hermes/bin/hermes-start"
    echo "   停止: $WORKSPACE/hermes/bin/hermes-stop"
    echo "   重启: $WORKSPACE/hermes/bin/hermes-restart"
    echo "   状态: $WORKSPACE/hermes/bin/hermes-status"
    echo ""
    echo "📚 文档: $WORKSPACE/hermes/docs/"
}

# 主函数
main() {
    echo ""
    echo "🚀 Hermes 系统部署"
    echo "========================"
    echo "版本: $VERSION"
    echo "环境: $ENVIRONMENT"
    echo "工作空间: $WORKSPACE"
    echo "========================"
    echo ""
    
    # 验证环境
    validate_environment
    
    # 备份现有部署
    backup_existing
    
    # 创建目录结构
    create_directories
    
    # 复制文件
    copy_files
    
    # 初始化系统
    initialize_system
    
    # 验证部署
    validate_deployment
    
    # 显示部署信息
    show_deployment_info
    
    echo ""
    log_success "部署流程完成!"
}

# 执行主函数
main "$@"