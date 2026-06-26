#!/bin/bash

# MyStock 一键安装脚本
# 用于快速安装 MyStock 所有依赖

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  MyStock 一键安装脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Python 版本
echo -e "${YELLOW}检查 Python 版本...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION} 已安装${NC}"
else
    echo -e "${RED}✗ Python 未安装，请先安装 Python 3.8+${NC}"
    exit 1
fi

# 检查 Node.js 和 npm
echo ""
echo -e "${YELLOW}检查 Node.js 和 npm...${NC}"
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}✓ Node.js ${NODE_VERSION} 已安装${NC}"
else
    echo -e "${YELLOW}⚠ Node.js 未安装${NC}"
    echo -e "${YELLOW}  请安装 Node.js: https://nodejs.org/${NC}"
fi

# 安装 jsdom（pywencai 依赖）
echo ""
echo -e "${YELLOW}安装 jsdom（pywencai 数据获取依赖）...${NC}"
if command -v npm &> /dev/null; then
    npm install -g jsdom 2>&1 | grep -v "^npm warn" || true
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ jsdom 安装完成${NC}"
        # 设置 NODE_PATH
        export NODE_PATH=$(npm root -g)
        echo -e "${GREEN}✓ NODE_PATH 已设置: $NODE_PATH${NC}"
    else
        echo -e "${YELLOW}⚠ jsdom 安装可能失败，请手动运行: npm install -g jsdom${NC}"
    fi
else
    echo -e "${YELLOW}⚠ npm 未安装，跳过 jsdom 安装${NC}"
fi

# 检查 pip
echo ""
echo -e "${YELLOW}检查 pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip 已安装${NC}"
else
    echo -e "${RED}✗ pip 未安装${NC}"
    exit 1
fi

# 安装后端依赖
echo ""
echo -e "${YELLOW}安装后端依赖...${NC}"
if [ -f backend/requirements.txt ]; then
    pip3 install -r backend/requirements.txt
    echo -e "${GREEN}✓ 后端依赖安装完成${NC}"
else
    echo -e "${RED}✗ backend/requirements.txt 文件不存在${NC}"
    exit 1
fi

# 复制环境变量文件
echo ""
echo -e "${YELLOW}配置环境变量...${NC}"
if [ -f backend/.env.example ]; then
    if [ ! -f backend/.env ]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✓ 已创建 backend/.env 文件${NC}"
        echo -e "${YELLOW}  请编辑 backend/.env 填写你的 API Key${NC}"
    else
        echo -e "${GREEN}✓ 环境变量文件已存在${NC}"
    fi
else
    echo -e "${YELLOW}⚠ backend/.env.example 不存在，跳过${NC}"
fi

# 创建必要的目录
echo ""
echo -e "${YELLOW}创建数据目录...${NC}"
mkdir -p data
touch portfolio_data.json 2>/dev/null || true
touch stock_codes.json 2>/dev/null || true
echo -e "${GREEN}✓ 数据目录创建完成${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  安装完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "下一步："
echo -e "  1. 启动全部服务（后端+前端）: ${YELLOW}./start.sh${NC}"
echo -e "  2. 访问: ${YELLOW}http://localhost:5001${NC}"
echo -e "     后端 API: ${YELLOW}http://localhost:8000${NC}"
echo ""
echo -e "⚠️  重要提示："
echo -e "  - 确保已安装 Node.js 和 jsdom（见上方安装步骤）"
echo -e "  - 启动脚本会自动设置 NODE_PATH"
echo -e "  - 如遇数据获取问题，请运行: npm install -g jsdom"
echo ""
echo -e "其他命令："
echo -e "  API 健康检查: ${YELLOW}python3 scripts/check_api.py${NC}"
echo -e "  Skill 测试: ${YELLOW}python3 scripts/test_skill.py${NC}"
echo ""
