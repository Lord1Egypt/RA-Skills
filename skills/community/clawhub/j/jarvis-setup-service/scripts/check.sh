#!/bin/bash
# OpenClaw 环境检测脚本 v1.0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1: $($1 --version 2>/dev/null || $1 -version 2>/dev/null | head -1)"
    else
        echo -e "${RED}✗${NC} $1: 未安装"
    fi
}

echo "🔍 OpenClaw 环境检测"
echo "================================"
echo ""

echo "【系统信息】"
echo "系统: $(uname -s) $(uname -r)"
echo "架构: $(uname -m)"
echo "运行时间: $(uptime -p)"
echo ""

echo "【Node.js 生态】"
check node
check npm
check pnpm
check openclaw
echo ""

echo "【系统资源】"
echo "内存总量: $(free -h | awk '/^Mem:/ {print $2}')"
echo "内存使用: $(free -h | awk '/^Mem:/ {print $3}')"
echo "磁盘剩余: $(df -h / | awk 'NR==2 {print $4}')"
echo ""

echo "【OpenClaw 目录】"
if [[ -d "${HOME}/.openclaw" ]]; then
    echo -e "${GREEN}✓${NC} 配置目录: ${HOME}/.openclaw"
    echo "  技能: $(ls -d ${HOME}/.openclaw/skills/*/ 2>/dev/null | wc -l) 个"
else
    echo -e "${RED}✗${NC} 配置目录: 未创建"
fi

echo ""
echo "【运行状态】"
if pgrep -f "openclaw" > /dev/null; then
    echo -e "${GREEN}✓${NC} OpenClaw 正在运行"
else
    echo -e "${YELLOW}○${NC} OpenClaw 未运行"
fi

echo ""
echo "================================"
echo "检测完成"
