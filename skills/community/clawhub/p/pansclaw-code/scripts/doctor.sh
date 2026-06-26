#!/bin/bash
# 健康检查脚本

BIN="$HOME/.local/bin/claw"

if [ ! -f "$BIN" ]; then
    echo "❌ Claw 二进制未找到: $BIN"
    echo "   运行 scripts/build.sh 先构建"
    exit 1
fi

echo "🔍 运行健康检查..."
echo ""

$BIN /doctor
