#!/bin/bash
# OpenClaw 自动安装脚本 v1.0
# 支持: Ubuntu 20.04+ / Debian 11+
# 作者: Jarvis

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_system() {
    log "检测系统环境..."
    if [[ -f /etc/debian_version ]]; then
        log "检测到 Debian/Ubuntu 系统"
    else
        error "仅支持 Debian/Ubuntu 系统"
        exit 1
    fi
}

install_deps() {
    log "安装系统依赖..."
    apt update
    apt install -y curl git unzip sudo
}

install_nodejs() {
    log "安装 Node.js 20.x..."
    if command -v node &> /dev/null; then
        NODE_VER=$(node --version)
        warn "Node.js 已安装: $NODE_VER"
    else
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt install -y nodejs
        log "Node.js 版本: $(node --version)"
    fi
    log "npm 版本: $(npm --version)"
}

install_pnpm() {
    log "安装 pnpm..."
    if command -v pnpm &> /dev/null; then
        warn "pnpm 已安装: $(pnpm --version)"
    else
        npm install -g pnpm
        log "pnpm 版本: $(pnpm --version)"
    fi
}

install_openclaw() {
    log "安装 OpenClaw..."
    if command -v openclaw &> /dev/null; then
        warn "OpenClaw 已安装: $(openclaw --version)"
    else
        pnpm add -g openclaw
        log "OpenClaw 版本: $(openclaw --version)"
    fi
}

create_directories() {
    log "创建目录结构..."
    mkdir -p "${HOME}/.openclaw/skills"
    mkdir -p "${HOME}/.openclaw/logs"
    mkdir -p "${HOME}/.openclaw/data"
    log "目录创建完成"
}

show_next_steps() {
    echo ""
    log "========================================="
    log "  OpenClaw 安装完成！"
    log "========================================="
    echo ""
    log "下一步操作:"
    echo "  1. 配置: ./config.sh"
    echo "  2. Telegram配置: ./setup-telegram.sh"
    echo "  3. 启动: openclaw gateway start"
    echo ""
    log "或者运行: openclaw init 进行初始化"
    echo ""
}

main() {
    echo ""
    log "========================================="
    log "  OpenClaw 自动安装脚本 v1.0"
    log "========================================="
    echo ""
    
    check_system
    install_deps
    install_nodejs
    install_pnpm
    install_openclaw
    create_directories
    show_next_steps
}

main "$@"
