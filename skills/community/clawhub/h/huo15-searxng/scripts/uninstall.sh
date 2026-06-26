#!/bin/bash
# uninstall.sh — SearXNG 卸载脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$HOME/docker/searxng"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo "🗑️  huo15-searxng — 卸载 SearXNG"
echo "═══════════════════════════════════════════════════"
echo ""

# 停止容器
if docker ps 2>/dev/null | grep -q "^searxng "; then
    log_info "停止 SearXNG 容器..."
    cd "$DOCKER_DIR" && docker compose down --remove-orphans 2>/dev/null || true
else
    log_warn "SearXNG 容器未运行"
fi

# 删除数据目录
if [ -d "$DOCKER_DIR" ]; then
    log_info "删除配置目录: $DOCKER_DIR"
    rm -rf "$DOCKER_DIR"
else
    log_warn "配置目录不存在: $DOCKER_DIR"
fi

# 从 ~/.zshrc 移除环境变量
if grep -q "SEARXNG_BASE_URL" "$HOME/.zshrc" 2>/dev/null; then
    log_info "从 ~/.zshrc 移除 SEARXNG_BASE_URL..."
    # 移除相关行（huo15-searxng 注释块和变量）
    sed -i '' '/# SearXNG.*huo15-searxng/d' "$HOME/.zshrc"
    sed -i '' '/export SEARXNG_BASE_URL=/d' "$HOME/.zshrc"
fi

# 清理当前 shell 环境变量（不影响 ~/.zshrc）
unset SEARXNG_BASE_URL 2>/dev/null || true

echo ""
echo "═══════════════════════════════════════════════════"
echo -e "  ${GREEN}✅ 卸载完成${NC}"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  已清理:"
echo "    - SearXNG 容器和数据"
echo "    - $DOCKER_DIR 目录"
echo "    - ~/.zshrc 中的 SEARXNG_BASE_URL"
echo ""
echo "  ⚠️  重要: 请运行以下命令使环境变量变更生效:"
echo "     source ~/.zshrc"
echo ""
echo "═══════════════════════════════════════════════════"
