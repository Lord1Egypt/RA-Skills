#!/bin/bash
# examples.sh - Obsidian Headless 使用示例

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBS="$SCRIPT_DIR/bin/obsidian-headless.sh"

echo "Obsidian Headless 使用示例"
echo "=========================="
echo

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

run_example() {
    local description="$1"
    local cmd="$2"
    
    echo -e "${BLUE}$description${NC}"
    echo "命令: obs '$cmd'"
    echo "---"
    $OBS "$cmd"
    echo
}

echo "1. 创建笔记示例"
echo "---------------"
run_example "创建简单笔记" "创建笔记 想法收集"
run_example "创建带内容的笔记" "创建笔记 会议记录 今天讨论了项目进度..."

echo "2. 搜索笔记示例"
echo "---------------"
run_example "按标题搜索" "搜索标题 openclaw"
run_example "按内容搜索" "搜索内容 home assistant"
run_example "模糊搜索" "模糊搜索 tavily"

echo "3. 日记示例"
echo "-----------"
run_example "创建今天日记" "今天日记"
run_example "创建带内容的日记" "今天日记 今天完成了技能开发..."

echo "4. 查看和管理示例"
echo "-----------------"
run_example "列出所有笔记" "列出所有"
run_example "列出文件夹" "列出文件夹"
run_example "查看最近笔记" "最近笔记"

echo "5. 删除笔记示例（演示）"
echo "-----------------------"
echo "命令: obs '删除笔记 旧笔记'"
echo "说明: 会显示匹配笔记并要求确认"
echo
