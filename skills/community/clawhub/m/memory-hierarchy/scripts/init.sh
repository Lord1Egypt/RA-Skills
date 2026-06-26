#!/bin/bash
# 初始化记忆目录结构
# 用法: bash scripts/init.sh

WORKSPACE="${MEMORY_WORKSPACE:-${HOME}/.openclaw/workspace}"
MEMORY_DIR="${WORKSPACE}/memory"

mkdir -p "$MEMORY_DIR/user"
mkdir -p "$MEMORY_DIR/feedback"
mkdir -p "$MEMORY_DIR/project"
mkdir -p "$MEMORY_DIR/reference"

echo "✅ 记忆目录已创建:"
echo "   memory/user/       - 用户偏好和背景"
echo "   memory/feedback/   - 反馈和纠正记录"
echo "   memory/project/    - 项目进展和目标"
echo "   memory/reference/  - 外部系统索引"
