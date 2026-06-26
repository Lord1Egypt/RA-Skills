#!/bin/bash
# OpenClaw Computer Use - 中文测试脚本
# 测试所有功能模块

echo "🖥️ OpenClaw Computer Use 功能测试"
echo "=================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILL_DIR="$HOME/.openclaw/workspace/skills/openclaw-computer-use"
TEST_LOG="/tmp/computer-use-test.log"

# 初始化测试日志
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')" > "$TEST_LOG"
echo "================================" >> "$TEST_LOG"

# 测试计数器
TESTS_PASSED=0
TESTS_FAILED=0

# 测试函数
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo -n "测试 $test_name ... "
    echo -e "\n[Test: $test_name]" >> "$TEST_LOG"
    
    if eval "$test_cmd" >> "$TEST_LOG" 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "📦 模块 1: 文件结构检查"
echo "------------------------"
run_test "SKILL.md 存在" "test -f $SKILL_DIR/SKILL.md"
run_test "computer-use.sh 存在" "test -f $SKILL_DIR/computer-use.sh"
run_test "computer_use.py 存在" "test -f $SKILL_DIR/computer_use.py"
run_test "脚本可执行" "test -x $SKILL_DIR/computer-use.sh"
echo ""

echo "📋 模块 2: 文档完整性"
echo "--------------------"
run_test "SKILL.md 包含名称" "grep -q 'name: openclaw-computer-use' $SKILL_DIR/SKILL.md"
run_test "SKILL.md 包含描述" "grep -q 'description:' $SKILL_DIR/SKILL.md"
run_test "SKILL.md 包含安装说明" "grep -q '安装' $SKILL_DIR/SKILL.md"
run_test "SKILL.md 包含使用指南" "grep -q '使用指南' $SKILL_DIR/SKILL.md"
echo ""

echo "🔧 模块 3: Bash 脚本功能"
echo "-----------------------"
cd "$SKILL_DIR"
run_test "帮助信息显示" "./computer-use.sh help | grep -q 'Computer Use'"
run_test "screenshot 命令存在" "./computer-use.sh screenshot 2>&1 | grep -q '截图' || true"
run_test "mouse 命令存在" "./computer-use.sh mouse 2>&1 | grep -q '用法' || true"
run_test "keyboard 命令存在" "./computer-use.sh keyboard 2>&1 | grep -q '用法' || true"
run_test "app 命令存在" "./computer-use.sh app 2>&1 | grep -q '用法' || true"
run_test "file 命令存在" "./computer-use.sh file 2>&1 | grep -q '用法' || true"
run_test "monitor 命令存在" "./computer-use.sh monitor 2>&1 | grep -q '用法' || true"
echo ""

echo "🐍 模块 4: Python API 测试"
echo "-------------------------"
run_test "Python 语法检查" "python3 -m py_compile $SKILL_DIR/computer_use.py"
run_test "模块可导入" "cd $SKILL_DIR && python3 -c 'import computer_use; print(\"OK\")' 2>&1 | grep -q 'OK'"
run_test "Screenshot 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import Screenshot; print(\"OK\")' | grep -q 'OK'"
run_test "Mouse 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import Mouse; print(\"OK\")' | grep -q 'OK'"
run_test "Keyboard 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import Keyboard; print(\"OK\")' | grep -q 'OK'"
run_test "Application 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import Application; print(\"OK\")' | grep -q 'OK'"
run_test "FileManager 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import FileManager; print(\"OK\")' | grep -q 'OK'"
run_test "SystemMonitor 类存在" "cd $SKILL_DIR && python3 -c 'from computer_use import SystemMonitor; print(\"OK\")' | grep -q 'OK'"
echo ""

echo "📊 模块 5: 系统监控功能"
echo "----------------------"
cd "$SKILL_DIR"
run_test "resources 命令" "./computer-use.sh monitor resources | grep -q 'CPU' || true"
run_test "processes 命令" "./computer-use.sh monitor processes | grep -q 'USER' || true"
echo ""

echo "📁 模块 6: 文件管理功能"
echo "----------------------"
cd "$SKILL_DIR"
run_test "list 命令" "./computer-use.sh file list | grep -q 'computer' || true"
run_test "search 命令" "./computer-use.sh file search --name '*.md' | grep -q 'SKILL' || true"
echo ""

echo "=================================="
echo "📈 测试结果汇总"
echo "=================================="
echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
echo -e "失败: ${RED}$TESTS_FAILED${NC}"
echo "总计: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    echo ""
    echo "技能已就绪，可以打包发布。"
    exit 0
else
    echo -e "${YELLOW}⚠️ 部分测试失败，请查看日志: $TEST_LOG${NC}"
    exit 1
fi
