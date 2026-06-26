#!/bin/bash
# install.sh - Obsidian Headless 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Obsidian Headless 安装程序"
echo "=========================="
echo

# 检查依赖
echo "检查依赖..."

# 检查 ripgrep
if command -v rg &>/dev/null; then
    echo -e "${GREEN}✓${NC} ripgrep (rg) 已安装"
else
    echo -e "${YELLOW}⚠${NC} ripgrep (rg) 未安装（推荐安装以获得更快的搜索速度）"
    echo "  安装命令:"
    echo "    Ubuntu/Debian: sudo apt install ripgrep"
    echo "    macOS: brew install ripgrep"
fi

# 检查 find
echo -e "${GREEN}✓${NC} find 已安装"

# 检查 grep
echo -e "${GREEN}✓${NC} grep 已安装"

echo

# 创建软链接到 PATH
echo "创建快捷命令..."

# 获取 bin 目录路径
BIN_DIR="$SCRIPT_DIR/bin"
OBS_SCRIPT="$SCRIPT_DIR/obs"

# 创建 obs 快捷命令
chmod +x "$OBS_SCRIPT"
chmod +x "$BIN_DIR/obsidian-headless.sh"

# 添加到 shell 配置文件
SHELL_RC=""
if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [[ -n "$SHELL_RC" && -f "$SHELL_RC" ]]; then
    # 检查是否已添加
    if ! grep -q "alias obs=" "$SHELL_RC" 2>/dev/null; then
        echo "alias obs='$OBS_SCRIPT'" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} 已添加 'obs' 别名到 $SHELL_RC"
        echo "  请运行: source $SHELL_RC"
    else
        echo -e "${YELLOW}⚠${NC} 'obs' 别名已存在于 $SHELL_RC"
    fi
fi

# 创建系统级链接（可选）
if [[ -d "/usr/local/bin" && -w "/usr/local/bin" ]]; then
    if [[ ! -f "/usr/local/bin/obsidian-headless" ]]; then
        ln -s "$BIN_DIR/obsidian-headless.sh" /usr/local/bin/obsidian-headless 2>/dev/null && \
            echo -e "${GREEN}✓${NC} 已创建系统命令: obsidian-headless" || \
            echo -e "${YELLOW}⚠${NC} 无法创建系统命令（可能需要 sudo）"
    fi
fi

echo
echo -e "${GREEN}安装完成!${NC}"
echo
echo "使用方法:"
echo "  obs '创建笔记 新想法'"
echo "  obs '搜索内容 home assistant'"
echo "  obs '今天日记'"
echo
echo "查看帮助:"
echo "  obs --help"
echo
