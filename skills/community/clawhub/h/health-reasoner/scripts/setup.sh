#!/bin/bash
# Health Reasoner - Setup Script (Linux/macOS)
set -e

echo "=== Health Reasoner 安装 ==="

# Python 检查
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要 Python 3.6+"
    exit 1
fi

echo "✓ Python $(python3 --version) 已安装"

# 核心推理模块零依赖
echo "✓ 核心推理模块无需额外依赖"

# 可选：安装 Flask（用于 REST API 模式）
read -p "是否安装 Flask 以启用 API 服务? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip3 install flask
    echo "✓ Flask 已安装"
else
    echo "跳过 Flask（CLI/JSON 模式可用）"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "快速测试:"
echo "  python3 health_reasoner.py --test"
echo ""
echo "CLI 模式:"
echo "  python3 health_reasoner.py --cli"
echo ""
echo "API 模式 (需 Flask):"
echo "  python3 health_reasoner.py --api"
