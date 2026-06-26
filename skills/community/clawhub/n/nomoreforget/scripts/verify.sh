#!/bin/bash
# No More Forget 验证脚本

echo "🔍 No More Forget 验证检查..."
echo ""

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
ISSUES=0

# 1. 检查 OpenClaw 目录
echo "📁 检查目录结构..."
if [ -d "$OPENCLAW_DIR" ]; then
    echo "  ✅ OpenClaw 目录存在"
else
    echo "  ❌ OpenClaw 目录不存在"
    ((ISSUES++))
fi

if [ -d "$WORKSPACE_DIR" ]; then
    echo "  ✅ Workspace 目录存在"
else
    echo "  ❌ Workspace 目录不存在"
    ((ISSUES++))
fi

if [ -d "$WORKSPACE_DIR/memory" ]; then
    echo "  ✅ Memory 目录存在"
else
    echo "  ⚠️  Memory 目录不存在（将在首次使用时创建）"
fi

# 2. 检查配置文件
echo ""
echo "⚙️  检查配置文件..."
OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"

if [ -f "$OPENCLAW_JSON" ]; then
    echo "  ✅ openclaw.json 存在"
    
    # 检查 Memory Flush 配置
    if python3 -c "
import json
with open('$OPENCLAW_JSON', 'r') as f:
    config = json.load(f)
    flush = config.get('agents', {}).get('defaults', {}).get('compaction', {}).get('memoryFlush', {})
    if flush.get('enabled', False):
        print('FLUSH_ENABLED')
    else:
        print('FLUSH_DISABLED')
" 2>/dev/null | grep -q "FLUSH_ENABLED"; then
        echo "  ✅ Memory Flush 已启用"
    else
        echo "  ❌ Memory Flush 未启用"
        echo "     运行: bash scripts/install.sh 修复"
        ((ISSUES++))
    fi
else
    echo "  ❌ openclaw.json 不存在"
    ((ISSUES++))
fi

# 3. 检查记忆文件
echo ""
echo "📝 检查记忆文件..."

if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    LINES=$(wc -l < "$WORKSPACE_DIR/MEMORY.md")
    if [ $LINES -gt 500 ]; then
        echo "  ⚠️  MEMORY.md 过长 ($LINES 行，建议 < 500 行)"
        echo "     运行: bash scripts/optimize_memory.sh 优化"
    else
        echo "  ✅ MEMORY.md 存在 ($LINES 行)"
    fi
else
    echo "  ⚠️  MEMORY.md 不存在"
fi

# 4. 检查今日日志
TODAY=$(date +%Y-%m-%d)
TODAY_LOG="$WORKSPACE_DIR/memory/$TODAY.md"

if [ -f "$TODAY_LOG" ]; then
    echo "  ✅ 今日日志存在: $TODAY_LOG"
else
    echo "  ℹ️  今日日志尚未创建（正常，会话后自动创建）"
fi

# 5. 检查插件（可选）
echo ""
echo "🔌 检查记忆插件..."

if command -v clawhub &> /dev/null; then
    if clawhub list 2>/dev/null | grep -q "qmd"; then
        echo "  ✅ qmd 搜索增强已安装"
    else
        echo "  ℹ️  qmd 未安装（可选）"
        echo "     安装: clawhub install qmd"
    fi
else
    echo "  ℹ️  clawhub 命令不可用"
fi

# 总结
echo ""
echo "═══════════════════════════════════════════════════════"
if [ $ISSUES -eq 0 ]; then
    echo "✅ 验证通过！No More Forget 运行正常"
else
    echo "❌ 发现 $ISSUES 个问题，请运行安装脚本修复："
    echo "   bash scripts/install.sh"
fi
echo "═══════════════════════════════════════════════════════"