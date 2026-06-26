#!/bin/bash
# opencli-content-hunter 前置检查脚本
# 检查 opencli 安装状态、Chrome 扩展连接、平台登录态

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== opencli-content-hunter 前置检查 ==="

# 1. 检查 opencli 是否安装
echo ""
echo "[1/3] 检查 opencli 安装状态..."
if which opencli > /dev/null 2>&1; then
    VERSION=$(opencli --version 2>/dev/null || echo "未知")
    echo -e "${GREEN}✓${NC} opencli 已安装 (v$VERSION)"
else
    echo -e "${RED}✗${NC} opencli 未安装"
    echo ""
    echo "请运行以下命令安装："
    echo "  npm install -g @jackwener/opencli"
    exit 1
fi

# 2. 检查 Chrome 扩展
echo ""
echo "[2/3] 检查 Chrome 扩展连接..."
DOCTOR_OUTPUT=$(opencli doctor 2>&1 || true)
if echo "$DOCTOR_OUTPUT" | grep -q "\[OK\].*Extension"; then
    echo -e "${GREEN}✓${NC} Chrome 扩展已连接"
else
    if echo "$DOCTOR_OUTPUT" | grep -q "\[MISSING\].*Extension"; then
        echo -e "${RED}✗${NC} Chrome 扩展未安装或未连接"
        echo ""
        echo "请按以下步骤安装扩展："
        echo "  1. 下载：https://github.com/jackwener/opencli/releases → opencli-extension.zip"
        echo "  2. 解压到任意位置"
        echo "  3. Chrome → chrome://extensions/ → 开启开发者模式"
        echo "  4. 点击「加载已解压的扩展程序」→ 选择 extension 文件夹"
        exit 1
    else
        echo -e "${YELLOW}⚠${NC} 扩展状态未知，尝试继续..."
    fi
fi

# 3. 快速测试平台连接
echo ""
echo "[3/3] 测试平台连接..."

# 测试B站（通常最稳定）
if opencli bilibili hot --limit 1 -f table > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} B站 连接成功"
else
    echo -e "${YELLOW}⚠${NC} B站 需要在 Chrome 中登录"
fi

# 测试小红书
XHS_OUTPUT=$(opencli xiaohongshu feed --limit 1 2>&1 || true)
if echo "$XHS_OUTPUT" | grep -q "Not logged in"; then
    echo -e "${YELLOW}⚠${NC} 小红书 需要在 Chrome 中登录 xiaohongshu.com"
elif echo "$XHS_OUTPUT" | grep -q "Error\|FAIL"; then
    echo -e "${YELLOW}⚠${NC} 小红书 连接异常"
else
    echo -e "${GREEN}✓${NC} 小红书 连接成功"
fi

echo ""
echo "=== 检查完成 ==="
echo ""
echo "提示："
echo "  - 如有平台未登录，请在 Chrome 中打开对应网站并登录"
echo "  - 登录一次后永久有效"
echo "  - 运行 'opencli doctor' 可查看详细状态"
