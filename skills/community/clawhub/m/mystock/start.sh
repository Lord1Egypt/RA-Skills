#!/bin/bash

# MyStock 一键启动脚本
# 同时启动后端 API 和前端界面

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  MyStock - 我的股票 一键启动${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 设置 Node.js 全局模块路径（pywencai 依赖 jsdom）
export NODE_PATH=$(npm root -g 2>/dev/null)
if [ -n "$NODE_PATH" ]; then
    echo -e "${GREEN}✓${NC} Node.js 模块路径: $NODE_PATH"
else
    echo -e "${YELLOW}⚠${NC} 未找到 Node.js，请运行: npm install -g jsdom"
fi

# 检查后端依赖
echo ""
echo -e "${YELLOW}检查后端依赖...${NC}"
if [ -d "backend" ]; then
    echo -e "${GREEN}✓${NC} 后端目录存在"

    # 检查并升级 Python 依赖
    if [ -f "backend/requirements.txt" ]; then
        echo -e "  ${YELLOW}升级 Python 依赖...${NC}"

        # 升级 pip
        pip3 install --upgrade pip -q 2>&1 | grep -v "Requirement already satisfied" || true

        # 升级 requirements.txt 中的依赖
        pip3 install --upgrade -r backend/requirements.txt -q 2>&1 | grep -v "Requirement already satisfied" || true

        echo -e "${GREEN}  ✓${NC} Python 依赖已检查/升级"
    else
        echo -e "${YELLOW}  ⚠${NC} requirements.txt 不存在"
    fi
else
    echo -e "${RED}✗${NC} 后端目录不存在"
    exit 1
fi

# 检查前端依赖
echo ""
echo -e "${YELLOW}检查前端文件...${NC}"
if [ -f "frontend/index.html" ]; then
    echo -e "${GREEN}✓${NC} 前端文件存在"
else
    echo -e "${RED}✗${NC} 前端文件不存在"
    exit 1
fi

# 创建必要的目录
echo ""
echo -e "${YELLOW}创建数据目录...${NC}"
mkdir -p data 2>/dev/null || true
touch portfolio_data.json 2>/dev/null || true
touch stock_codes.json 2>/dev/null || true
touch memos.json 2>/dev/null || true
echo -e "${GREEN}✓${NC} 数据目录就绪"

# 启动后端服务
echo ""
echo -e "${YELLOW}启动后端 API 服务...${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
cd backend
export NODE_PATH=$(npm root -g 2>/dev/null)
python3 main.py > /tmp/mystock_backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}✓${NC} 后端服务已启动 (PID: $BACKEND_PID)"
echo -e "${GREEN}✓${NC} 后端日志: /tmp/mystock_backend.log"

# 等待后端启动
echo ""
echo -e "${YELLOW}等待后端服务启动...${NC}"
sleep 3

# 检查后端是否启动成功
if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 后端服务运行中"
else
    echo -e "${RED}✗${NC} 后端服务启动失败"
    echo -e "${RED}请检查日志: /tmp/mystock_backend.log${NC}"
    exit 1
fi

# 启动前端服务
echo ""
echo -e "${YELLOW}启动前端界面...${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
cd frontend
python3 -m http.server 5001 > /tmp/mystock_frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✓${NC} 前端服务已启动 (PID: $FRONTEND_PID)"
echo -e "${GREEN}✓${NC} 前端日志: /tmp/mystock_frontend.log"

# 等待前端启动
sleep 2

# 检查前端是否启动成功
if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 前端服务运行中"
else
    echo -e "${RED}✗${NC} 前端服务启动失败"
    echo -e "${RED}请检查日志: /tmp/mystock_frontend.log${NC}"
fi

# 完成
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  🎉 MyStock 启动成功！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "📱 访问地址："
echo -e "  ${GREEN}前端界面: http://localhost:5001${NC}"
echo -e "  ${GREEN}后端 API:  http://localhost:8000${NC}"
echo -e "  ${GREEN}API 文档:  http://localhost:8000/docs${NC}"
echo ""
echo -e "⚠️  提示："
echo -e "  - 首次使用请先配置 AI 服务（如需要）"
echo -e "  - 查看日志: tail -f /tmp/mystock_*.log"
echo -e "  - 停止服务: pkill -f 'python3.*main.py' && pkill -f 'http.server 5001'"
echo ""
echo -e "${YELLOW}正在打开浏览器...${NC}"

# 自动打开浏览器（macOS）
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 1
    open http://localhost:5001
fi

echo ""
echo -e "${GREEN}✨ 享受 MyStock 我的股票！${NC}"
echo ""
