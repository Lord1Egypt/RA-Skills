#!/bin/bash
# macOS 权限检测脚本（功能测试版）
# 用法：./check_permissions.sh

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🔐 检查 macOS 权限配置（功能测试法）${NC}"
echo ""
echo "⚠️  注：使用实际功能测试，而不是 tccutil（更准确）"
echo ""

# 计数器
granted=0
denied=0

# 检查辅助功能（通过鼠标控制测试）
echo "测试辅助功能权限..."
if python3 "$SCRIPT_DIR/desktop_ctrl.py" mouse position 2>&1 | grep -q "📍"; then
    echo -e "${GREEN}✅${NC} 辅助功能：已授予（鼠标控制正常）"
    ((granted++)) || true
else
    echo -e "${RED}❌${NC} 辅助功能：未授予"
    echo -e "   ${YELLOW}打开设置：${NC}open \"x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility\""
    ((denied++)) || true
fi

# 检查自动化（通过应用控制测试）
echo "测试自动化权限..."
if bash "$SCRIPT_DIR/app_control.sh" front 2>&1 | grep -q "📱"; then
    echo -e "${GREEN}✅${NC} 自动化：已授予（应用控制正常）"
    ((granted++)) || true
else
    echo -e "${RED}❌${NC} 自动化：未授予"
    echo -e "   ${YELLOW}打开设置：${NC}open \"x-apple.systempreferences:com.apple.preference.security?Privacy_AppleEvents\""
    ((denied++)) || true
fi

# 检查屏幕录制（通过截屏测试）
echo "测试屏幕录制权限..."
if bash "$SCRIPT_DIR/screenshot.sh" -o /tmp/permission_test_check.png 2>&1 | grep -q "✅"; then
    echo -e "${GREEN}✅${NC} 屏幕录制：已授予（截屏正常）"
    ((granted++)) || true
    # 清理测试文件
    rm -f /tmp/permission_test_check.png
else
    echo -e "${RED}❌${NC} 屏幕录制：未授予"
    echo -e "   ${YELLOW}打开设置：${NC}open \"x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture\""
    ((denied++)) || true
fi

# 检查完全磁盘访问
echo "测试完全磁盘访问权限..."
if [ -r ~/Documents ] 2>/dev/null; then
    echo -e "${GREEN}✅${NC} 完全磁盘访问：已授予"
    ((granted++)) || true
else
    echo -e "${YELLOW}⚠️${NC} 完全磁盘访问：未授予（可选）"
    echo -e "   ${YELLOW}打开设置：${NC}open \"x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles\""
    ((denied++)) || true
fi

echo ""
echo -e "${BLUE}────────────────────────────────${NC}"
echo -e "已授予：${GREEN}$granted${NC} | 未授予/可选：${RED}$denied${NC}"
echo ""

if [ $denied -eq 0 ]; then
    echo -e "${GREEN}✅ 所有权限已配置！${NC}"
    echo ""
    echo "🎉 所有功能都可以正常使用！"
else
    echo -e "${YELLOW}⚠️  部分权限未配置${NC}"
    echo ""
    if [ $granted -gt 0 ]; then
        echo -e "${GREEN}✅ 核心功能已可用！${NC}"
        echo ""
        echo "已可用的功能:"
        [ $granted -ge 1 ] && echo "  - 鼠标键盘控制"
        [ $granted -ge 2 ] && echo "  - 应用控制"
        [ $granted -ge 3 ] && echo "  - 截屏功能"
    fi
fi

echo ""
