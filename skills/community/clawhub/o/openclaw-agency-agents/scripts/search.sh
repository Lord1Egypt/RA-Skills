#!/bin/bash
# search.sh - 搜索智能体

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

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <搜索关键词>"
    echo ""
    echo "示例："
    echo "  $0 小红书"
    echo "  $0 AI"
    echo "  $0 安全"
    exit 1
fi

KEYWORD="$*"
echo -e "${CYAN}搜索智能体: $KEYWORD${RESET}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

# 搜索智能体
AGENT_DIRS="academic design engineering finance game-development hr legal marketing paid-media sales product project-management supply-chain testing support spatial-computing specialized"

FOUND_COUNT=0

for dir in $AGENT_DIRS; do
    if [ -d "$REPO_DIR/$dir" ]; then
        # 搜索匹配的文件（不区分大小写）
        matches=$(find "$REPO_DIR/$dir" -maxdepth 1 -iname "*${KEYWORD}*.md" | sort)

        if [ -n "$matches" ]; then
            echo ""
            echo -e "${BLUE}📁 $dir${RESET}"
            echo "$matches" | while read file; do
                echo "  • $(basename "$file" .md)"
            done
            FOUND_COUNT=$((FOUND_COUNT + $(echo "$matches" | wc -l)))
        fi
    fi
done

echo ""
if [ $FOUND_COUNT -eq 0 ]; then
    echo -e "${YELLOW}未找到匹配的智能体${RESET}"
    echo ""
    echo "提示："
    echo "  - 尝试使用更简短的关键词"
    echo "  - 使用 '列出所有智能体' 查看完整列表"
else
    echo -e "${GREEN}找到 $FOUND_COUNT 个匹配的智能体${RESET}"
fi
