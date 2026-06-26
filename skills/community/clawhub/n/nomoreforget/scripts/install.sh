#!/bin/bash
# No More Forget 一键安装脚本
# 解决 OpenClaw 记忆系统的三大痛点

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"

echo "🦞 No More Forget 安装开始..."
echo ""

# 1. 检查 OpenClaw 是否已安装
if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "❌ 未检测到 OpenClaw 安装目录"
    echo "   请先安装 OpenClaw: https://docs.openclaw.ai"
    exit 1
fi

echo "✅ 检测到 OpenClaw 安装目录: $OPENCLAW_DIR"

# 2. 备份现有配置
BACKUP_DIR="$OPENCLAW_DIR/backup_$(date +%Y%m%d_%H%M%S)"
echo ""
echo "📦 备份现有配置到: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
    cp "$OPENCLAW_DIR/openclaw.json" "$BACKUP_DIR/"
fi

if [ -d "$WORKSPACE_DIR" ]; then
    [ -f "$WORKSPACE_DIR/MEMORY.md" ] && cp "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/"
    [ -d "$WORKSPACE_DIR/memory" ] && cp -r "$WORKSPACE_DIR/memory" "$BACKUP_DIR/"
fi

# 3. 配置 Memory Flush
echo ""
echo "⚙️  配置 Memory Flush..."

OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"

if [ ! -f "$OPENCLAW_JSON" ]; then
    echo '{}' > "$OPENCLAW_JSON"
fi

# 使用 Python 合并 JSON 配置
python3 << 'EOF'
import json
import os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

# 读取现有配置
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except:
    config = {}

# 确保结构存在
if "agents" not in config:
    config["agents"] = {}
if "defaults" not in config["agents"]:
    config["agents"]["defaults"] = {}
if "compaction" not in config["agents"]["defaults"]:
    config["agents"]["defaults"]["compaction"] = {}

# 设置 Memory Flush 配置
config["agents"]["defaults"]["compaction"]["reserveTokensFloor"] = 40000
config["agents"]["defaults"]["compaction"]["memoryFlush"] = {
    "enabled": True,
    "softThresholdTokens": 4000,
    "systemPrompt": "Session nearing compaction. Store durable memories to memory/YYYY-MM-DD.md now.",
    "prompt": "Pre-compaction memory flush. Capture: (1) Key decisions (2) Active todos (3) Important facts. Use memory/YYYY-MM-DD.md."
}

# 写回配置
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Memory Flush 配置完成")
EOF

# 4. 创建/更新 MEMORY.md 模板
echo ""
echo "📝 配置 MEMORY.md 模板..."

if [ ! -d "$WORKSPACE_DIR" ]; then
    mkdir -p "$WORKSPACE_DIR"
fi

if [ ! -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    cp "$SKILL_DIR/assets/MEMORY.md.template" "$WORKSPACE_DIR/MEMORY.md"
    echo "✅ 创建 MEMORY.md 模板"
else
    echo "ℹ️  MEMORY.md 已存在，保留现有内容"
    echo "   模板可参考: $SKILL_DIR/assets/MEMORY.md.template"
fi

# 5. 创建 memory 目录
if [ ! -d "$WORKSPACE_DIR/memory" ]; then
    mkdir -p "$WORKSPACE_DIR/memory"
    echo "✅ 创建 memory 目录"
fi

# 6. 创建今日日志文件
TODAY=$(date +%Y-%m-%d)
TODAY_LOG="$WORKSPACE_DIR/memory/$TODAY.md"

if [ ! -f "$TODAY_LOG" ]; then
    cat > "$TODAY_LOG" << EOF
# $TODAY Daily Log

## Session Notes
_No More Forget installed on $(date '+%Y-%m-%d %H:%M:%S')_

EOF
    echo "✅ 创建今日日志: $TODAY_LOG"
fi

# 7. 安装维护脚本到用户目录
MAINTAIN_DIR="$OPENCLAW_DIR/no-more-forget"
mkdir -p "$MAINTAIN_DIR"

cp "$SCRIPT_DIR/optimize_memory.sh" "$MAINTAIN_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/backup_memory.sh" "$MAINTAIN_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/diagnose.sh" "$MAINTAIN_DIR/" 2>/dev/null || true

echo "✅ 维护脚本已安装到: $MAINTAIN_DIR"

# 8. 可选：安装 qmd 搜索增强
echo ""
echo "🔍 搜索增强插件（可选）"
echo "   qmd - 更强大的记忆搜索"
echo "   安装命令: clawhub install qmd"
echo ""

# 完成提示
echo "═══════════════════════════════════════════════════════"
echo "🎉 No More Forget 安装完成！"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "已启用功能："
echo "  ✅ Memory Flush 自动保存关键记忆"
echo "  ✅ reserveTokensFloor: 40000 tokens"
echo "  ✅ 记忆模板已配置"
echo ""
echo "维护命令："
echo "  诊断问题: bash $MAINTAIN_DIR/diagnose.sh"
echo "  优化记忆: bash $MAINTAIN_DIR/optimize_memory.sh"
echo "  备份记忆: bash $MAINTAIN_DIR/backup_memory.sh"
echo ""
echo "可选增强："
echo "  安装 qmd: clawhub install qmd"
echo ""