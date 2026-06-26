#!/bin/bash
# setup.sh - 初始化 openmaic-agents-lite skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPO_DIR="$SKILL_DIR/repo"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

info() { echo -e "${GREEN}[OK]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!!]${RESET} $*"; }
error() { echo -e "${RED}[ERR]${RESET} $*" >&2; }

echo -e "${CYAN}════════════════════════════════════════════════════════════════${RESET}"
echo -e "${CYAN}OpenMAIC Agents - 初始化${RESET}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${RESET}"
echo ""

# 检查是否已经初始化
if [ -d "$REPO_DIR" ]; then
    warn "仓库目录已存在：$REPO_DIR"
    echo ""
    read -p "是否重新下载？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "初始化已取消"
        exit 0
    fi
    rm -rf "$REPO_DIR"
fi

info "正在克隆 agency-agents-zh 仓库..."
echo ""

git clone https://github.com/jnMetaCode/agency-agents-zh.git "$REPO_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${RESET}"
    echo -e "${GREEN}✓ 初始化完成！${RESET}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${RESET}"
    echo ""
    info "仓库位置：$REPO_DIR"
    echo ""
    echo -e "${YELLOW}现在可以开始使用：${RESET}"
    echo "  - 列出所有智能体：列出所有智能体"
    echo "  - 激活智能体：激活 [智能体名称]"
    echo "  - 搜索智能体：搜索智能体 [关键词]"
else
    echo ""
    error "克隆失败！请检查网络连接。"
    exit 1
fi
