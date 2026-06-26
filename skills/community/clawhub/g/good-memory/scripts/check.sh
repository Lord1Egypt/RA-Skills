#!/bin/bash
#
# Good-Memory 环境检查脚本
# 运行安装前执行此脚本检查环境是否符合要求
#

set -e

OPENCLAW_BASE="${OPENCLAW_BASE:-/root/.openclaw}"
SKILL_DIR="${SKILL_DIR:-${OPENCLAW_BASE}/workspace/skills/good-memory}"

echo "=== Good-Memory 环境检查 ==="
echo ""

# 检查依赖命令
echo "[1/4] 检查依赖命令..."
REQUIRED_BINS=("bash" "tail" "ls" "date" "python3" "unzip" "curl")
MISSING_BINS=()

for bin in "${REQUIRED_BINS[@]}"; do
    if ! command -v "$bin" &> /dev/null; then
        MISSING_BINS+=("$bin")
        echo "  ❌ $bin: 未找到"
    else
        echo "  ✅ $bin: 已安装"
    fi
done

if [[ ${#MISSING_BINS[@]} -gt 0 ]]; then
    echo ""
    echo "❌ 缺少必要依赖: ${MISSING_BINS[*]}"
    echo "请先安装这些命令后再继续。"
    exit 1
fi

# 检查Python依赖
echo ""
echo "[2/4] 检查Python依赖..."
python3 -c "import json, os, subprocess, datetime" 2>/dev/null
if [[ $? -eq 0 ]]; then
    echo "  ✅ Python 依赖已满足"
else
    echo "  ❌ Python 依赖缺失，请确保安装了标准库"
    exit 1
fi

# 检查OpenClaw目录
echo ""
echo "[3/4] 检查OpenClaw目录..."
if [[ -d "$OPENCLAW_BASE" ]]; then
    echo "  ✅ OpenClaw 目录存在: $OPENCLAW_BASE"
else
    echo "  ❌ OpenClaw 目录不存在: $OPENCLAW_BASE"
    echo "  请设置 OPENCLAW_BASE 环境变量到你的OpenClaw安装目录"
    exit 1
fi

# 检查workspace目录
WORKSPACE_DIR="${OPENCLAW_BASE}/workspace"
if [[ -d "$WORKSPACE_DIR" ]]; then
    echo "  ✅ Workspace 目录存在: $WORKSPACE_DIR"
else
    echo "  ⚠️  Workspace 目录不存在，将在安装时自动创建"
fi

# 检查Agent目录
AGENTS_DIR="${OPENCLAW_BASE}/agents"
if [[ -d "$AGENTS_DIR" ]]; then
    echo "  ✅ Agents 目录存在: $AGENTS_DIR"
    AGENT_COUNT=$(ls -d "${AGENTS_DIR}"/*/ 2>/dev/null | wc -l)
    echo "  检测到 $AGENT_COUNT 个Agent"
else
    echo "  ❌ Agents 目录不存在: $AGENTS_DIR"
    exit 1
fi

# 检查AGENTS.md
echo ""
echo "[4/4] 检查AGENTS.md文件..."
MAIN_AGENTS_MD="${WORKSPACE_DIR}/AGENTS.md"
if [[ -f "$MAIN_AGENTS_MD" ]]; then
    echo "  ✅ 主AGENTS.md存在: $MAIN_AGENTS_MD"
else
    echo "  ⚠️  主AGENTS.md不存在，安装时会为你创建基础版本"
fi

# 检查Agent的AGENTS.md
FOUND_AGENTS_MD=0
for agent_dir in "${AGENTS_DIR}"/*/; do
    agent_name="$(basename "$agent_dir")"
    if [[ -f "$agent_dir/agent/AGENTS.md" || -f "$agent_dir/AGENTS.md" ]]; then
        FOUND_AGENTS_MD=$((FOUND_AGENTS_MD + 1))
    fi
done

echo "  检测到 $FOUND_AGENTS_MD 个Agent包含AGENTS.md"

echo ""
echo "✅ 环境检查通过！可以安装Good-Memory。"
echo ""
echo "快速安装命令（单Agent）："
echo "  INSTALL_MODE=single TARGET_AGENT=main bash ${SKILL_DIR}/scripts/install.sh"
echo ""
echo "完整安装命令（多Agent）："
echo "  bash ${SKILL_DIR}/scripts/install.sh"
