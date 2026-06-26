#!/bin/bash
# OpenClaw Memory Mi 启动脚本
# 用法: source start.sh 或 ./start.sh

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 路径配置
SKILL_DIR="$HOME/.openclaw/workspace/skills/mi-memorystack-v2"
SCRIPT_DIR="$SKILL_DIR/scripts"
DATA_DIR="$SKILL_DIR/data"
LOG_FILE="$HOME/.openclaw/memory_daemon.log"

echo "🚀 OpenClaw Memory Mi 启动中..."
echo "================================"

# 1. 检查目录结构
if [ ! -d "$SCRIPT_DIR" ]; then
    echo -e "${RED}✗ 错误: 找不到脚本目录 $SCRIPT_DIR${NC}"
    exit 1
fi

# 2. 确保 data 目录存在
mkdir -p "$DATA_DIR"

# 3. 检查并启动 Memory Daemon
echo ""
echo "📋 步骤 1: 检查 Memory Daemon 状态..."

DAEMON_STATUS=$(python3 "$SCRIPT_DIR/memory_daemon.py" status 2>&1) || true

if echo "$DAEMON_STATUS" | grep -q "运行中\|running"; then
    echo -e "${GREEN}✓ Memory Daemon 已在运行${NC}"
    echo "   $DAEMON_STATUS"
else
    echo -e "${YELLOW}! Memory Daemon 未运行，正在启动...${NC}"
    START_OUTPUT=$(python3 "$SCRIPT_DIR/memory_daemon.py" start 2>&1) || true
    echo "   $START_OUTPUT"
    sleep 1
    
    # 再次检查
    CHECK_STATUS=$(python3 "$SCRIPT_DIR/memory_daemon.py" status 2>&1) || true
    if echo "$CHECK_STATUS" | grep -q "运行中\|running"; then
        echo -e "${GREEN}✓ Memory Daemon 启动成功${NC}"
    else
        echo -e "${YELLOW}! 注意: 可能启动失败或有其他问题${NC}"
        echo "   状态输出: $CHECK_STATUS"
    fi
fi

# 4. 显示当前数据文件
echo ""
echo "📊 步骤 2: 当前记忆数据..."
MEMORY_FILES=$(ls -la "$DATA_DIR"/*.jsonl 2>/dev/null | wc -l)
if [ "$MEMORY_FILES" -gt 0 ]; then
    echo -e "${GREEN}✓ 找到 $MEMORY_FILES 个用户记忆文件${NC}"
    ls -lh "$DATA_DIR"/*.jsonl 2>/dev/null | awk '{print "   - " $9 " (" $5 ")"}'
else
    echo -e "${YELLOW}! 暂无记忆数据文件${NC}"
fi

# 5. 设置环境变量（供后续使用）
export MEMORY_FRAMEWORK_ENABLED="true"
export MEMORY_FRAMEWORK_DIR="$SKILL_DIR"
export MEMORY_DAEMON_LOG="$LOG_FILE"

echo ""
echo "================================"
echo -e "${GREEN}✓ Memory Framework 准备就绪${NC}"
echo ""
echo "💡 使用提示:"
echo "   检索记忆: python3 $SCRIPT_DIR/memory_search.py --user-id '<USER_ID>' --query '<查询>'"
echo "   保存记忆: python3 $SCRIPT_DIR/memory_daemon.py queue --user-id '<USER_ID>' --query '...' --response '...'"
echo "   查看日志: tail -f $LOG_FILE"
echo ""