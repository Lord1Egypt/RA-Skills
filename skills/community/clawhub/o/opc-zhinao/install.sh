#!/bin/bash

# OPC智脑 - 统一安装入口
# 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）
# 用法：bash install.sh [IDE类型] [目标项目路径]

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 显示帮助
show_help() {
    echo -e "${BLUE}OPC智脑 - 一键安装工具${NC}"
    echo ""
    echo "用法：bash install.sh [IDE类型] [目标项目路径]"
    echo ""
    echo "支持的IDE类型："
    echo "  codearts    码道IDE（完整功能，推荐）"
    echo "  prompt      通用安装（自动检测IDE环境）"
    echo ""
    echo "示例："
    echo "  bash install.sh codearts /path/to/project"
    echo "  bash install.sh prompt /path/to/project"
    echo "  bash install.sh prompt .              # 自动检测当前项目IDE"
    echo ""
    echo "说明："
    echo "  - codearts：使用install-codearts.sh（码道IDE专用）"
    echo "  - prompt：使用install-prompt.sh（智能检测，支持码道/Cursor/VSCode/通用）"
}

# 检查参数
if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    show_help
    exit 0
fi

# IDE类型和目标路径
IDE_TYPE="${1:-}"
TARGET_DIR="${2:-.}"

# 如果没有指定IDE类型，进入交互式选择
if [ -z "$IDE_TYPE" ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  OPC智脑 - 一键安装${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "请选择安装方式："
    echo ""
    echo "  1) 码道IDE（使用install-codearts.sh）"
    echo "  2) 通用安装（使用install-prompt.sh，自动检测IDE环境）"
    echo ""
    read -p "请输入选项 [1-2，默认2]: " choice
    
    case $choice in
        1) IDE_TYPE="codearts" ;;
        *) IDE_TYPE="prompt" ;;
    esac
    
    read -p "请输入目标项目路径（默认为当前目录）: " input_dir
    TARGET_DIR="${input_dir:-.}"
fi

# 执行对应的安装脚本
case "$IDE_TYPE" in
    codearts)
        INSTALL_SCRIPT="$SCRIPT_DIR/install-codearts.sh"
        ;;
    prompt)
        INSTALL_SCRIPT="$SCRIPT_DIR/install-prompt.sh"
        ;;
    *)
        # cursor、vscode等统一使用install-prompt.sh
        echo -e "${YELLOW}提示：'$IDE_TYPE' 将使用通用安装脚本（install-prompt.sh）${NC}"
        echo -e "${YELLOW}      install-prompt.sh 会自动检测并适配目标IDE环境${NC}"
        echo ""
        INSTALL_SCRIPT="$SCRIPT_DIR/install-prompt.sh"
        ;;
esac

if [ ! -f "$INSTALL_SCRIPT" ]; then
    echo -e "${RED}错误：安装脚本不存在 '$INSTALL_SCRIPT'${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}正在为 $IDE_TYPE 安装OPC智脑...${NC}"
echo ""

bash "$INSTALL_SCRIPT" "$TARGET_DIR"