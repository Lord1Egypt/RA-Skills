#!/bin/bash
# macOS Desktop Control 安装脚本
# 用法：./install.sh

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🦐 安装 macOS Desktop Control...${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Step 1: 检查 Python
echo -e "${BLUE}Step 1/5: 检查 Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Python: $($PYTHON_CMD --version)${NC}"
elif command -v python &> /dev/null; then
    if python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD="python"
        echo -e "${GREEN}✅ Python: $($PYTHON_CMD --version)${NC}"
    else
        echo -e "${YELLOW}⚠️  警告：找到 Python 2，建议安装 Python 3${NC}"
        PYTHON_CMD="python"
    fi
else
    echo -e "${YELLOW}⚠️  Python 未安装，部分功能将不可用${NC}"
    echo "   安装：brew install python"
    PYTHON_CMD=""
fi
echo ""

# Step 2: 设置脚本权限
echo -e "${BLUE}Step 2/5: 设置脚本权限...${NC}"
chmod +x "$SCRIPT_DIR"/*.sh
echo -e "${GREEN}✅ 脚本权限已设置${NC}"
echo ""

# Step 3: 检查依赖（可选）
echo -e "${BLUE}Step 3/5: 检查可选依赖...${NC}"

# 检查 pyautogui
if [ -n "$PYTHON_CMD" ]; then
    if $PYTHON_CMD -c "import pyautogui" 2>/dev/null; then
        echo -e "${GREEN}✅ pyautogui: 已安装${NC}"
    else
        echo -e "${YELLOW}⚠️  pyautogui: 未安装${NC}"
        echo "   安装：pip3 install --user pyautogui pyscreeze pillow psutil"
    fi
fi

# 检查 jq（可选）
if command -v jq &> /dev/null; then
    echo -e "${GREEN}✅ jq: 已安装${NC}"
else
    echo -e "${YELLOW}ℹ️  jq: 未安装（可选）${NC}"
    echo "   安装：brew install jq"
fi
echo ""

# Step 4: 创建输出目录
echo -e "${BLUE}Step 4/5: 创建输出目录...${NC}"
OUTPUT_DIR="$HOME/Desktop/OpenClaw-Screenshots"
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✅ 输出目录：$OUTPUT_DIR${NC}"
echo ""

# Step 5: 权限检查
echo -e "${BLUE}Step 5/5: 检查权限配置...${NC}"
echo ""

# 运行权限检测
if [ -x "$SCRIPT_DIR/check_permissions.sh" ]; then
    "$SCRIPT_DIR/check_permissions.sh" || true
else
    echo -e "${YELLOW}⚠️  权限检测脚本不存在，跳过${NC}"
fi
echo ""

# 安装完成
echo -e "${GREEN}────────────────────────────────${NC}"
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo "📚 使用方式："
echo "  # 截屏"
echo "  bash scripts/screenshot.sh"
echo ""
echo "  # 进程列表"
echo "  bash scripts/processes.sh"
echo ""
echo "  # 系统信息"
echo "  bash scripts/system_info.sh"
echo ""
echo "  # 剪贴板"
echo "  bash scripts/clipboard.sh get"
echo "  bash scripts/clipboard.sh set \"文字\""
echo ""
echo "📖 查看文档："
echo "  cat SKILL.md"
echo ""
echo "⚠️  重要提示："
echo "  如果权限刚授予，请重启终端应用使其生效！"
echo ""
