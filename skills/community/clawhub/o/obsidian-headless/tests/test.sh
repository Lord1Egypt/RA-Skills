#!/bin/bash
# test.sh - Obsidian Headless 测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$SCRIPT_DIR/bin/obsidian-headless.sh"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

# 测试函数
run_test() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    
    echo -n "测试: $name ... "
    
    if result=$($cmd 2>&1); then
        if [[ -n "$expected" && "$result" == *"$expected"* ]]; then
            echo -e "${GREEN}通过${NC}"
            ((PASSED++))
        elif [[ -z "$expected" ]]; then
            echo -e "${GREEN}通过${NC}"
            ((PASSED++))
        else
            echo -e "${RED}失败${NC} (输出不匹配)"
            ((FAILED++))
        fi
    else
        if [[ "$expected" == "FAIL" ]]; then
            echo -e "${GREEN}通过${NC} (预期失败)"
            ((PASSED++))
        else
            echo -e "${RED}失败${NC}"
            ((FAILED++))
        fi
    fi
}

echo "Obsidian Headless 测试"
echo "====================="
echo

# 检查环境
if [[ -z "$OBSIDIAN_VAULT" ]]; then
    echo -e "${YELLOW}警告: OBSIDIAN_VAULT 未设置，使用自动检测${NC}"
fi

echo

# 基础功能测试
echo "基础功能测试:"
run_test "帮助命令" "$BIN '帮助'" "Obsidian Headless"
run_test "列出所有" "$BIN '列出所有'" "所有笔记"
run_test "列出文件夹" "$BIN '列出文件夹'" "所有文件夹"

# 创建笔记测试
echo
echo "创建笔记测试:"
TEST_NOTE="测试笔记_$(date +%s)"
run_test "创建笔记" "$BIN 创建笔记 ${TEST_NOTE} 测试内容" "创建笔记成功"

# 查看笔记测试
run_test "查看笔记" "$BIN 查看笔记 ${TEST_NOTE}" "测试内容"

# 搜索测试
echo
echo "搜索测试:"
run_test "搜索标题" "$BIN '搜索标题 测试'" "测试"
run_test "搜索内容" "$BIN '搜索内容 测试内容'" "测试内容"
run_test "模糊搜索" "$BIN '模糊搜索 测试'" "标题匹配"

# 日记测试
echo
echo "日记测试:"
run_test "今天日记" "$BIN '今天日记 测试日记内容'" "创建今天日记"

# 清理测试笔记
echo
echo "清理测试数据..."
rm -f "$OBSIDIAN_VAULT/$TEST_NOTE.md" 2>/dev/null || true
rm -f "$OBSIDIAN_VAULT/${TEST_NOTE}.md" 2>/dev/null || true

echo
echo "====================="
echo -e "通过: ${GREEN}$PASSED${NC}"
echo -e "失败: ${RED}$FAILED${NC}"

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}所有测试通过!${NC}"
    exit 0
else
    echo -e "${RED}部分测试失败${NC}"
    exit 1
fi
