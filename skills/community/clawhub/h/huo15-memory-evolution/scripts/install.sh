#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 从零安装脚本
#
# 用法: ./install.sh
#
# 功能: 在全新的 OpenClaw 上初始化记忆系统
#       1. 先安装依赖 fluid-memory
#       2. 创建记忆目录结构
#
# 依赖: fluid-memory (自动安装)
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y-%m-%d)

echo "=========================================="
echo "huo15-memory-evolution 从零安装"
echo "=========================================="
echo "   时间: ${TIMESTAMP}"
echo ""

#===========================================
# 步骤 0: 安装依赖（fluid-memory）
#===========================================
echo "[步骤0] 检查并安装依赖..."

# 检查 fluid-memory 是否已安装
if [ -d "$OPENCLAW_DIR/workspace/skills/fluid-memory" ]; then
    echo "   [OK] fluid-memory 已安装"
else
    echo "   [安装] 正在安装 fluid-memory..."
    if command -v clawhub &> /dev/null; then
        cd "$OPENCLAW_DIR/workspace" && clawhub install fluid-memory --force 2>&1 || {
            echo "   [警告] fluid-memory 安装失败，请手动安装: clawhub install fluid-memory"
        }
        cd "$SKILL_DIR"
    else
        echo "   [警告] clawhub 未找到，请手动安装: clawhub install fluid-memory"
    fi
fi

echo ""

#===========================================
# 步骤 1: 检查环境
#===========================================
echo "[步骤1] 检查环境..."

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "   [错误] OpenClaw workspace 不存在: $WORKSPACE_DIR"
    exit 1
fi

echo "   [OK] OpenClaw workspace 存在"

# 检查企微插件
if [ -d "$OPENCLAW_DIR/extensions/wecom" ] || [ -d "$OPENCLAW_DIR/plugins/wecom" ]; then
    echo "   [OK] 企微插件: 已安装"
else
    echo "   [提示] 企微插件未安装，动态Agent隔离功能将不可用"
fi

echo ""

#===========================================
# 步骤 2: 创建记忆目录
#===========================================
echo "[步骤2] 创建记忆目录..."

mkdir -p "$WORKSPACE_DIR/memory"
mkdir -p "$WORKSPACE_DIR/memory/user"
mkdir -p "$WORKSPACE_DIR/memory/feedback"
mkdir -p "$WORKSPACE_DIR/memory/project"
mkdir -p "$WORKSPACE_DIR/memory/reference"
mkdir -p "$WORKSPACE_DIR/memory/archive"
mkdir -p "$WORKSPACE_DIR/memory/shared"  # Team Memory 共享目录

echo "   [OK] memory/{user,feedback,project,reference,archive,shared}/ 已创建"

#===========================================
# 步骤 3: 创建 index.json
#===========================================
echo "[步骤3] 创建 index.json..."

cat << 'EOF' > "$WORKSPACE_DIR/memory/index.json"
{
  "version": "1.0",
  "installedAt": "TIMESTAMP",
  "dependency": "fluid-memory",
  "entries": []
}
EOF

sed -i '' "s/TIMESTAMP/${TIMESTAMP}/" "$WORKSPACE_DIR/memory/index.json"
echo "   [OK] memory/index.json 已创建"

#===========================================
# 步骤 4: 创建 MEMORY.md
#===========================================
echo "[步骤4] 创建 MEMORY.md..."

cat << EOF > "$WORKSPACE_DIR/MEMORY.md"
# Memory Index

*最后更新: ${TIMESTAMP} | 最多 200 行*

## user
（用户偏好和习惯）

## feedback
（纠正和确认偏好）

## project
（项目上下文和进展）

## reference
（外部系统指针）

---

*此文件为索引，内容在 memory/{type}/ 目录下*
*协同 fluid-memory 工作，专注组织和共享*
EOF

echo "   [OK] MEMORY.md 已创建"

#===========================================
# 完成
#===========================================
echo ""
echo "=========================================="
echo "安装完成!"
echo "=========================================="
echo ""
echo "下一步:"
echo "  1. 运行 verify.sh 验证安装"
echo "  2. 运行 dream.sh 测试日志提炼"
echo "  3. 查看 MEMORY.md 确认结构正确"
