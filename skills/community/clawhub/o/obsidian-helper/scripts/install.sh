#!/bin/bash
# install.sh - 安装 obsidian helper

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Obsidian Helper 安装 ==="

# 创建 bin 目录
mkdir -p ~/bin

# 复制脚本
cp "$SCRIPT_DIR/scripts/obsidian" ~/bin/obsidian
chmod +x ~/bin/obsidian

# 添加到 PATH
if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    echo "已添加 ~/bin 到 PATH"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  obsidian list        # 列出笔记"
echo "  obsidian search 关键词 # 搜索"
echo "  obsidian create 文件名 # 创建笔记"
echo "  obsidian help        # 查看帮助"
echo ""
echo "配置 vault 路径:"
echo "  export OBSIDIAN_VAULT=/path/to/your/vault"