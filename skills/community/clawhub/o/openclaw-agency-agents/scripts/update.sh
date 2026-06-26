#!/bin/bash
# update.sh - 更新智能体仓库

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPO_DIR="$SKILL_DIR/repo"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

info() { echo -e "${GREEN}[OK]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!!]${RESET} $*"; }
error() { echo -e "${RED}[ERR]${RESET} $*" >&2; }

# 检查仓库是否存在
if [ ! -d "$REPO_DIR" ]; then
    error "仓库未找到！"
    echo "请先运行：cd $SKILL_DIR && git clone https://github.com/jnMetaCode/agency-agents-zh.git repo"
    exit 1
fi

info "更新智能体库..."
echo ""

cd "$REPO_DIR"

# 拉取最新代码
git pull origin main

echo ""
info "✓ 智能体库更新完成！"
