#!/bin/bash
# Hermes Agent 卸载脚本 (Linux/macOS)
# 用法: bash uninstall.sh [--keep-config]

set -e

HERMES_DIR="$HOME/.hermes"
KEEP_CONFIG=false

# 解析参数
if [ "$1" = "--keep-config" ]; then
    KEEP_CONFIG=true
fi

echo "=== Hermes Agent 卸载 ==="
echo ""

# 检查是否存在
if [ ! -d "$HERMES_DIR" ]; then
    echo "❌ Hermes Agent 未安装，无需卸载"
    exit 0
fi

# 停止网关
echo "🛑 停止网关..."
cd "$HERMES_DIR/hermes-agent" 2>/dev/null && source venv/bin/activate 2>/dev/null && hermes gateway stop 2>/dev/null || true

# 确认卸载
if [ "$KEEP_CONFIG" = true ]; then
    echo "⚠️  将删除程序文件，但保留配置文件"
    echo ""
    read -p "确认卸载? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "❌ 已取消"
        exit 0
    fi
    
    # 保留配置，只删除程序
    echo "🗑️ 删除程序文件..."
    rm -rf "$HERMES_DIR/hermes-agent"
    rm -rf "$HERMES_DIR/venv"
    echo "✅ 卸载完成！配置文件保留在 $HERMES_DIR"
else
    echo "⚠️  将完全删除 Hermes Agent 及所有配置"
    echo "   配置文件: $HERMES_DIR/config.yaml"
    echo "   环境变量: $HERMES_DIR/.env"
    echo ""
    read -p "确认完全卸载? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "❌ 已取消"
        exit 0
    fi
    
    # 完全删除
    echo "🗑️ 删除所有文件..."
    rm -rf "$HERMES_DIR"
    echo "✅ 完全卸载完成！"
fi

echo ""
echo "💡 如需重新安装，请运行:"
echo "   git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent"
