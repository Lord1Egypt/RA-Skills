#!/bin/bash
# one-mail 卸载脚本

set -e

INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="$HOME/.onemail"

echo "🗑️  one-mail 卸载"
echo "==============="
echo ""

# 检查是否已安装
if [ ! -L "$INSTALL_DIR/onemail" ]; then
    echo "⚠️  one-mail 未安装"
    exit 0
fi

# 询问是否删除配置
read -p "是否删除配置文件? ($CONFIG_DIR) [y/N]: " delete_config

# 删除符号链接
echo "删除符号链接: $INSTALL_DIR/onemail"
if [ -w "$INSTALL_DIR" ]; then
    rm -f "$INSTALL_DIR/onemail"
else
    sudo rm -f "$INSTALL_DIR/onemail"
fi

# 删除配置（如果用户确认）
if [ "$delete_config" = "y" ]; then
    if [ -d "$CONFIG_DIR" ]; then
        echo "删除配置目录: $CONFIG_DIR"
        rm -rf "$CONFIG_DIR"
    fi
fi

echo "✅ 卸载完成"
