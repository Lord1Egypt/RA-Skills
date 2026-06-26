#!/bin/bash
# ControlMemory 测试脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════╗"
echo "║   ControlMemory 功能测试               ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 测试 1: 检查文件是否存在
echo "测试 1: 检查文件..."
if [ -f "$SCRIPT_DIR/controlmemory.md" ]; then
    echo "  ✅ controlmemory.md 存在"
else
    echo "  ❌ controlmemory.md 不存在"
fi

if [ -f "$SCRIPT_DIR/control_memory.py" ]; then
    echo "  ✅ control_memory.py 存在"
else
    echo "  ❌ control_memory.py 不存在"
fi

if [ -f "$SCRIPT_DIR/clawhub_sync.py" ]; then
    echo "  ✅ clawhub_sync.py 存在"
else
    echo "  ❌ clawhub_sync.py 不存在"
fi

echo ""

# 测试 2: 测试记录功能
echo "测试 2: 测试记录功能..."
python3 "$SCRIPT_DIR/control_memory.py" record \
    --app "测试应用" \
    --command "测试命令" \
    --script "echo test" \
    --rate "100%" \
    --notes "测试备注" \
    --perms "无"

echo ""

# 测试 3: 查看记录
echo "测试 3: 查看记录..."
echo "  打开 controlmemory.md 查看记录"
echo "  路径：$SCRIPT_DIR/controlmemory.md"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   测试完成！                           ║"
echo "╚════════════════════════════════════════╝"
