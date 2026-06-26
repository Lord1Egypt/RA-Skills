#!/bin/bash
# 安装 italent-overtime 命令到系统 PATH
# 安装后可以直接在任何位置运行 `italent-overtime` 命令

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER_SCRIPT="$SCRIPT_DIR/italent-overtime"
INSTALL_DIR="/usr/local/bin"

echo "🔧 正在安装 italent-overtime 命令..."

# 检查是否需要 sudo
if [ ! -w "$INSTALL_DIR" ]; then
    echo "需要管理员权限来安装到 $INSTALL_DIR"
    if command -v sudo &> /dev/null; then
        sudo ln -sf "$WRAPPER_SCRIPT" "$INSTALL_DIR/italent-overtime"
        echo "✅ 安装完成！现在可以在任何位置运行：italent-overtime"
    else
        echo "❌ 无法获取 sudo 权限"
        echo "请手动执行：sudo ln -sf $WRAPPER_SCRIPT $INSTALL_DIR/italent-overtime"
        exit 1
    fi
else
    ln -sf "$WRAPPER_SCRIPT" "$INSTALL_DIR/italent-overtime"
    echo "✅ 安装完成！现在可以在任何位置运行：italent-overtime"
fi

# 验证安装
if command -v italent-overtime &> /dev/null; then
    echo "📍 命令位置：$(which italent-overtime)"
else
    echo "⚠️  命令未找到，请检查 PATH 配置"
fi
