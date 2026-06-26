#!/bin/bash
#
# OpenClaw 自动化安装脚本
# 支持 Linux/macOS/Windows WSL2
# 自动处理环境检测、依赖安装、OpenClaw 安装、配置初始化
#

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
OPENCLAW_VERSION="latest"
NODE_VERSION_MIN=22
INSTALL_DIR="${HOME}/.openclaw"
BACKUP_DIR="${HOME}/openclaw-backup"
LOG_FILE="${INSTALL_DIR}/install.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if [[ -f /etc/os-release ]]; then
            . /etc/os-release
            DISTRO="$ID"
        else
            DISTRO="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        DISTRO="macos"
    else
        log_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi

    log_info "检测到操作系统: $OS ($DISTRO)"
}

# 检查是否为 root 用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "不推荐使用 root 用户安装 OpenClaw"
        log_info "建议使用普通用户,遇到权限提升时输入密码"
        read -p "是否继续? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
}

# 检查并安装 Node.js
install_nodejs() {
    log_info "检查 Node.js 版本..."

    if command -v node &> /dev/null; then
        NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        log_info "当前 Node.js 版本: v$(node -v)"

        if [[ $NODE_VERSION -ge $NODE_VERSION_MIN ]]; then
            log_success "Node.js 版本满足要求 (v$NODE_VERSION >= v$NODE_VERSION_MIN)"
            return 0
        else
            log_warning "Node.js 版本过低 (v$NODE_VERSION < v$NODE_VERSION_MIN),需要升级"
        fi
    else
        log_info "未检测到 Node.js,准备安装..."
    fi

    # 安装 Node.js
    if [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            log_info "使用 Homebrew 安装 Node.js..."
            brew install node@22
            brew link node@22
        else
            log_error "未找到 Homebrew,请先安装: https://brew.sh/"
            exit 1
        fi
    elif [[ "$OS" == "linux" ]]; then
        # 优先使用 nvm 安装
        if [[ ! -d "$HOME/.nvm" ]]; then
            log_info "安装 nvm (Node Version Manager)..."
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
            export NVM_DIR="$HOME/.nvm"
            [[ -s "$NVM_DIR/nvm.sh" ]] && \. "$NVM_DIR/nvm.sh"
        fi

        log_info "使用 nvm 安装 Node.js v22..."
        source "$HOME/.nvm/nvm.sh"
        nvm install 22
        nvm use 22
        nvm alias default 22
    fi

    # 验证安装
    if command -v node &> /dev/null; then
        log_success "Node.js 安装成功: v$(node -v)"
        log_success "npm 版本: $(npm -v)"
    else
        log_error "Node.js 安装失败"
        exit 1
    fi
}

# 检查并安装 Git
install_git() {
    log_info "检查 Git..."

    if command -v git &> /dev/null; then
        log_success "Git 已安装: $(git --version)"
        return 0
    fi

    log_info "安装 Git..."

    if [[ "$OS" == "macos" ]]; then
        brew install git
    elif [[ "$DISTRO" == "ubuntu" ]] || [[ "$DISTRO" == "debian" ]]; then
        sudo apt-get update
        sudo apt-get install -y git
    elif [[ "$DISTRO" == "centos" ]] || [[ "$DISTRO" == "rhel" ]]; then
        sudo yum install -y git
    elif [[ "$DISTRO" == "fedora" ]]; then
        sudo dnf install -y git
    else
        log_warning "无法自动安装 Git,请手动安装后重试"
        return 1
    fi

    log_success "Git 安装成功: $(git --version)"
}

# 检查并安装构建工具
install_build_tools() {
    log_info "检查构建工具..."

    if [[ "$OS" == "linux" ]]; then
        local missing_tools=()

        for tool in gcc g++ make python3; do
            if ! command -v $tool &> /dev/null; then
                missing_tools+=($tool)
            fi
        done

        if [[ ${#missing_tools[@]} -gt 0 ]]; then
            log_info "安装构建工具: ${missing_tools[*]}"

            if [[ "$DISTRO" == "ubuntu" ]] || [[ "$DISTRO" == "debian" ]]; then
                sudo apt-get update
                sudo apt-get install -y build-essential python3
            elif [[ "$DISTRO" == "centos" ]] || [[ "$DISTRO" == "rhel" ]]; then
                sudo yum groupinstall -y "Development Tools"
                sudo yum install -y python3
            elif [[ "$DISTRO" == "fedora" ]]; then
                sudo dnf install -y @development-tools python3
            fi
        else
            log_success "构建工具已就绪"
        fi
    elif [[ "$OS" == "macos" ]]; then
        # macOS 通常自带 Xcode Command Line Tools
        if ! command -v gcc &> /dev/null; then
            log_info "安装 Xcode Command Line Tools..."
            xcode-select --install
        else
            log_success "构建工具已就绪"
        fi
    fi
}

# 配置 npm 镜像源(国内用户)
configure_npm_registry() {
    log_info "配置 npm 源..."

    # 检测是否在中国大陆
    local current_registry=$(npm config get registry)

    if [[ "$current_registry" == *"npmmirror"* ]]; then
        log_success "已使用国内镜像源: $current_registry"
        return 0
    fi

    # 询问用户
    log_info "是否使用国内镜像源加速下载? (推荐)"
    read -p "使用国内镜像? (y/n) [默认: y] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        npm config set registry https://registry.npmmirror.com
        log_success "已配置国内镜像源: https://registry.npmmirror.com"
    else
        log_info "保持使用官方源: $current_registry"
    fi
}

# 修复 npm 权限
fix_npm_permissions() {
    log_info "检查 npm 权限..."

    local npm_global=$(npm config get prefix)
    if [[ "$npm_global" == "/usr" ]] || [[ "$npm_global" == "/usr/local" ]]; then
        log_warning "npm 全局安装目录需要管理员权限"

        # 方案1: 修复目录权限
        log_info "尝试修复 npm 目录权限..."
        if [[ -d "$npm_global/lib/node_modules" ]]; then
            sudo chown -R $(whoami) "$npm_global/lib/node_modules"
            sudo chown -R $(whoami) "$npm_global/bin"
        fi

        # 方案2: 配置用户级安装目录
        log_info "或配置用户级安装目录..."
        mkdir -p "$HOME/.npm-global"
        npm config set prefix "$HOME/.npm-global"

        # 添加到 PATH
        local shell_rc=""
        if [[ -f "$HOME/.zshrc" ]]; then
            shell_rc="$HOME/.zshrc"
        elif [[ -f "$HOME/.bashrc" ]]; then
            shell_rc="$HOME/.bashrc"
        fi

        if [[ -n "$shell_rc" ]]; then
            if ! grep -q "\.npm-global/bin" "$shell_rc"; then
                echo "export PATH=\"$HOME/.npm-global/bin:\$PATH\"" >> "$shell_rc"
                log_success "已将 npm 全局路径添加到 $shell_rc"
                log_warning "请执行: source $shell_rc"
            fi
        fi
    fi
}

# 安装 OpenClaw
install_openclaw() {
    log_info "开始安装 OpenClaw..."

    # 清理旧的安装
    if command -v openclaw &> /dev/null; then
        log_warning "检测到已安装的 OpenClaw,准备备份..."
        backup_existing_installation

        log_info "卸载旧版本..."
        npm uninstall -g openclaw || true
    fi

    # 安装 OpenClaw
    log_info "正在下载并安装 OpenClaw (这可能需要几分钟)..."

    if ! npm install -g openclaw@${OPENCLAW_VERSION}; then
        log_error "OpenClaw 安装失败"
        log_info "常见解决方法:"
        log_info "1. 清理 npm 缓存: npm cache clean --force"
        log_info "2. 切换镜像源: npm config set registry https://registry.npmmirror.com"
        log_info "3. 查看完整错误日志: cat $LOG_FILE"
        exit 1
    fi

    log_success "OpenClaw 安装成功!"
}

# 备份现有安装
backup_existing_installation() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="${BACKUP_DIR}/backup_${timestamp}"

    mkdir -p "$backup_path"

    # 备份配置文件
    if [[ -d "$INSTALL_DIR" ]]; then
        cp -r "$INSTALL_DIR" "$backup_path/" 2>/dev/null || true
        log_info "配置已备份到: $backup_path"
    fi

    # 保留最近 3 个备份
    ls -t "${BACKUP_DIR}"/backup_* 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
}

# 验证安装
verify_installation() {
    log_info "验证安装..."

    if ! command -v openclaw &> /dev/null; then
        log_error "openclaw 命令不可用"
        exit 1
    fi

    local version=$(openclaw --version 2>&1 || echo "unknown")
    log_success "OpenClaw 版本: $version"
}

# 初始化配置
initialize_config() {
    log_info "初始化配置..."

    if [[ ! -d "$INSTALL_DIR" ]]; then
        mkdir -p "$INSTALL_DIR"
        log_info "创建配置目录: $INSTALL_DIR"
    fi

    # 创建日志目录
    mkdir -p "$INSTALL_DIR/logs"
    mkdir -p "$INSTALL_DIR/workspace"

    log_success "配置目录初始化完成"
}

# 安装守护进程(可选)
install_daemon() {
    log_info "是否安装系统服务(开机自启)?"
    read -p "安装服务? (y/n) [默认: n] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v openclaw &> /dev/null; then
            log_info "运行 openclaw onboard --install-daemon..."
            openclaw onboard --install-daemon || log_warning "服务安装失败,可稍后手动配置"
        fi
    fi
}

# 显示后续步骤
show_next_steps() {
    echo ""
    echo "=========================================="
    echo "  OpenClaw 安装完成!"
    echo "=========================================="
    echo ""
    echo "后续步骤:"
    echo ""
    echo "1. 运行配置向导:"
    echo "   openclaw onboard"
    echo ""
    echo "2. 启动网关服务:"
    echo "   openclaw gateway start"
    echo ""
    echo "3. 访问 Web UI:"
    echo "   http://127.0.0.1:18789"
    echo ""
    echo "4. 查看状态:"
    echo "   openclaw status"
    echo ""
    echo "5. 查看帮助:"
    echo "   openclaw --help"
    echo ""
    echo "如有问题,请查看日志: $LOG_FILE"
    echo "=========================================="
}

# 主函数
main() {
    echo ""
    echo "=========================================="
    echo "  OpenClaw 自动化安装脚本"
    echo "=========================================="
    echo ""

    # 解析参数
    REINSTALL=false
    SKIP_DEPS=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --reinstall)
                REINSTALL=true
                shift
                ;;
            --skip-deps)
                SKIP_DEPS=true
                shift
                ;;
            -h|--help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --reinstall    重新安装 OpenClaw(保留配置)"
                echo "  --skip-deps    跳过依赖安装"
                echo "  -h, --help     显示帮助信息"
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                exit 1
                ;;
        esac
    done

    # 执行安装流程
    detect_os
    check_root

    if [[ "$SKIP_DEPS" == false ]]; then
        install_nodejs
        install_git
        install_build_tools
    fi

    configure_npm_registry
    fix_npm_permissions
    install_openclaw

    if [[ "$REINSTALL" == false ]]; then
        initialize_config
    fi

    verify_installation
    install_daemon
    show_next_steps

    log_success "安装流程完成!"
}

# 捕获错误
trap 'log_error "安装过程中出现错误,请查看日志: $LOG_FILE"; exit 1' ERR

# 执行主函数
main "$@"
