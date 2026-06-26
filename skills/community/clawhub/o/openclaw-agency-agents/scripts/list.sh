#!/bin/bash
# list.sh - 列出所有可用智能体

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPO_DIR="$SKILL_DIR/repo"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

# 检查仓库是否存在
if [ ! -d "$REPO_DIR" ]; then
    echo -e "${RED}[ERR]${RESET} 仓库未找到！"
    echo "请先运行：cd $SKILL_DIR && git clone https://github.com/jnMetaCode/agency-agents-zh.git repo"
    exit 1
fi

# 智能体分类
declare -A CATEGORIES
CATEGORIES["engineering"]="🛠️  工程部"
CATEGORIES["design"]="🎨  设计部"
CATEGORIES["marketing"]="📢  营销部"
CATEGORIES["paid-media"]="💰  付费媒体部"
CATEGORIES["sales"]="💼  销售部"
CATEGORIES["product"]="📋  产品部"
CATEGORIES["finance"]="💵  财务部"
CATEGORIES["legal"]="⚖️  法律部"
CATEGORIES["hr"]="👥  人力资源部"
CATEGORIES["project-management"]="📊  项目管理部"
CATEGORIES["supply-chain"]="🚏  供应链部"
CATEGORIES["testing"]="🔍  测试部"
CATEGORIES["support"]="💬  支持部"
CATEGORIES["academic"]="🎓  学术部"
CATEGORIES["game-development"]="🎮  游戏开发部"
CATEGORIES["spatial-computing"]="🥽  空间计算部"
CATEGORIES["specialized"]="⭐  专家部"

# 如果指定了分类，只显示该分类
if [ $# -gt 0 ]; then
    CATEGORY="$1"
    if [ -d "$REPO_DIR/$CATEGORY" ]; then
        echo -e "${CYAN}${CATEGORIES[$CATEGORY]}${RESET}"
        echo ""
        find "$REPO_DIR/$CATEGORY" -maxdepth 1 -name "*.md" | sort | while read file; do
            basename "$file" .md
        done
    else
        echo "未找到分类: $CATEGORY"
        echo ""
        echo "可用分类："
        for key in "${!CATEGORIES[@]}"; do
            echo "  - $key"
        done
    fi
    exit 0
fi

# 显示所有分类
for dir in "${!CATEGORIES[@]}"; do
    if [ -d "$REPO_DIR/$dir" ]; then
        echo ""
        echo -e "${BLUE}${CATEGORIES[$dir]}${RESET}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
        find "$REPO_DIR/$dir" -maxdepth 1 -name "*.md" | sort | while read file; do
            echo "  • $(basename "$file" .md)"
        done
    fi
done

echo ""
echo -e "${GREEN}共 176 个专业智能体${RESET}"
