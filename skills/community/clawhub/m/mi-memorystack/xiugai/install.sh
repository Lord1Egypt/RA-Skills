#!/bin/bash

# Mi-MemoryStack 配置文件安装脚本
# 功能：将技能配置文件复制到 OpenClaw Workspace

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 路径定义
SKILL_DIR="$HOME/.openclaw/workspace/skills/Mi-MemoryStack/xiugai"
WORKSPACE_DIR="$HOME/.openclaw/workspace"

# 文件列表
FILES=("AGENTS.md" "SOUL.md" "start.sh")

echo -e "${YELLOW}开始安装 Mi-MemoryStack 配置文件...${NC}"

# 检查源目录是否存在
if [ ! -d "$SKILL_DIR" ]; then
    echo -e "${RED}错误：源目录不存在: $SKILL_DIR${NC}"
    echo "请确认 Mi-MemoryStack 技能已正确安装"
    exit 1
fi

# 检查目标目录是否存在
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${RED}错误：OpenClaw workspace 目录不存在: $WORKSPACE_DIR${NC}"
    exit 1
fi

# 备份已有文件（如果存在）
echo -e "${YELLOW}检查现有配置...${NC}"
BACKUP_DIR="$WORKSPACE_DIR/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for file in "${FILES[@]}"; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        echo -e "  备份: $file → backup/"
        cp "$WORKSPACE_DIR/$file" "$BACKUP_DIR/"
    fi
done

# 执行复制
echo -e "${YELLOW}复制新配置...${NC}"
for file in "${FILES[@]}"; do
    source_file="$SKILL_DIR/$file"
    target_file="$WORKSPACE_DIR/$file"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$target_file"
        echo -e "${GREEN}✓ $file 已安装${NC}"
    else
        echo -e "${RED}✗ $file 不存在于 $SKILL_DIR${NC}"
        exit 1
    fi
done

# 设置权限（start.sh 需要可执行）
if [ -f "$WORKSPACE_DIR/start.sh" ]; then
    chmod +x "$WORKSPACE_DIR/start.sh"
    echo -e "${GREEN}✓ start.sh 已设置为可执行${NC}"
fi

echo -e "\n${GREEN}=== 安装完成 ===${NC}"
echo -e "配置文件路径: $WORKSPACE_DIR"
if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR)" ]; then
    echo -e "原配置备份: $BACKUP_DIR"
fi
echo -e "\n${YELLOW}请执行以下命令重启 OpenClaw:${NC}"
echo -e "  openclaw gateway restart"