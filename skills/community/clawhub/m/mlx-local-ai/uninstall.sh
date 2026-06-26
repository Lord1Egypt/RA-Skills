#!/bin/bash

# MLX Local AI 卸载脚本

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

VENV_DIR="$HOME/mlx-env"
LOG_DIR="$HOME/.openclaw/logs"

echo ""
echo "========================================"
echo "   MLX Local AI 卸载脚本"
echo "========================================"
echo ""

read -p "确定要卸载 MLX Local AI? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消卸载"
    exit 0
fi

echo -e "${YELLOW}停止服务...${NC}"
~/start_ai.sh stop 2>/dev/null || true

echo -e "${YELLOW}删除虚拟环境...${NC}"
rm -rf "$VENV_DIR"

echo -e "${YELLOW}删除启动脚本...${NC}"
rm -f "$HOME/start_ai.sh"

echo -e "${YELLOW}删除日志文件...${NC}"
rm -rf "$LOG_DIR"

echo ""
echo -e "${GREEN}✅ 卸载完成${NC}"
echo ""
echo "注意: 模型缓存未删除，如需删除请运行:"
echo "  rm -rf ~/.cache/huggingface/hub/models--mlx-community--Qwen3.5-4B-OptiQ-4bit"
echo "  rm -rf ~/.cache/huggingface/hub/models--BAAI--bge-base-zh-v1.5"
