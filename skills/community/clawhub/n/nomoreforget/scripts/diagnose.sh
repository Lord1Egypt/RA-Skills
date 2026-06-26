#!/bin/bash
# No More Forget 诊断脚本
# 快速诊断记忆相关问题

echo "🏥 OpenClaw 记忆系统诊断"
echo "═══════════════════════════════════════════════════════"
echo ""

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"

DIAGNOSES=()

# 1. 检查 Memory Flush
echo "🔍 检查 Memory Flush 配置..."

FLUSH_ENABLED=$(python3 -c "
import json
try:
    with open('$OPENCLAW_JSON', 'r') as f:
        config = json.load(f)
    flush = config.get('agents', {}).get('defaults', {}).get('compaction', {}).get('memoryFlush', {})
    print('true' if flush.get('enabled', False) else 'false')
except:
    print('error')
" 2>/dev/null)

if [ "$FLUSH_ENABLED" = "true" ]; then
    echo "   ✅ Memory Flush 已启用"
else
    echo "   ❌ Memory Flush 未启用 → 可能导致压缩时丢失记忆"
    DIAGNOSES+=("启用 Memory Flush: 在 openclaw.json 中设置 agents.defaults.compaction.memoryFlush.enabled = true")
fi

# 2. 检查 reserveTokensFloor
RESERVE=$(python3 -c "
import json
try:
    with open('$OPENCLAW_JSON', 'r') as f:
        config = json.load(f)
    reserve = config.get('agents', {}).get('defaults', {}).get('compaction', {}).get('reserveTokensFloor', 20000)
    print(reserve)
except:
    print('error')
" 2>/dev/null)

if [ "$RESERVE" != "error" ] && [ "$RESERVE" -ge 30000 ]; then
    echo "   ✅ reserveTokensFloor: $RESERVE tokens"
elif [ "$RESERVE" != "error" ] && [ "$RESERVE" -lt 30000 ]; then
    echo "   ⚠️  reserveTokensFloor 偏低 ($RESERVE tokens) → 建议设置 40000"
    DIAGNOSES+=("提高 reserveTokensFloor 到 40000")
fi

# 3. 检查 MEMORY.md
echo ""
echo "🔍 检查 MEMORY.md..."

if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    LINES=$(wc -l < "$WORKSPACE_DIR/MEMORY.md")
    SIZE=$(du -h "$WORKSPACE_DIR/MEMORY.md" | cut -f1)
    
    if [ $LINES -gt 500 ]; then
        echo "   ⚠️  MEMORY.md 过长: $LINES 行 → 可能导致 Token 消耗过高"
        DIAGNOSES+=("精简 MEMORY.md，保持在 500 行以内")
    else
        echo "   ✅ MEMORY.md 行数正常: $LINES 行 ($SIZE)"
    fi
    
    # 检查关键内容位置
    if head -20 "$WORKSPACE_DIR/MEMORY.md" | grep -qi "重要\|关键\|决策"; then
        echo "   ✅ 关键内容在文件开头"
    else
        echo "   ⚠️  文件开头未发现关键内容 → 重要信息应放在开头"
        DIAGNOSES+=("将关键决策、重要规则放在 MEMORY.md 开头")
    fi
else
    echo "   ❌ MEMORY.md 不存在 → Agent 无长期记忆"
    DIAGNOSES+=("创建 MEMORY.md 文件")
fi

# 4. 检查 daily logs
echo ""
echo "🔍 检查 Daily Logs..."

if [ -d "$WORKSPACE_DIR/memory" ]; then
    LOG_COUNT=$(ls -1 "$WORKSPACE_DIR/memory"/*.md 2>/dev/null | wc -l)
    OLD_LOGS=$(find "$WORKSPACE_DIR/memory" -name "*.md" -mtime +30 2>/dev/null | wc -l)
    
    echo "   ℹ️  日志文件数: $LOG_COUNT"
    
    if [ $OLD_LOGS -gt 7 ]; then
        echo "   ⚠️  超过 30 天的日志: $OLD_LOGS 个 → 建议归档"
        DIAGNOSES+=("归档 30 天以上的旧日志")
    fi
else
    echo "   ℹ️  memory 目录不存在"
fi

# 5. 检查搜索能力
echo ""
echo "🔍 检查搜索能力..."

if command -v clawhub &> /dev/null && clawhub list 2>/dev/null | grep -q "qmd"; then
    echo "   ✅ qmd 搜索增强已安装"
else
    echo "   ℹ️  原生 SQLite 搜索 → 可安装 qmd 增强语义搜索"
    DIAGNOSES+=("(可选) 安装 qmd: clawhub install qmd")
fi

# 6. 检查备份
echo ""
echo "🔍 检查记忆备份..."

BACKUP_DIR="$OPENCLAW_DIR/backup_*"
LATEST_BACKUP=$(ls -dt $BACKUP_DIR 2>/dev/null | head -1)

if [ -n "$LATEST_BACKUP" ]; then
    BACKUP_DATE=$(stat -c %y "$LATEST_BACKUP" 2>/dev/null | cut -d' ' -f1)
    DAYS_SINCE=$(( ($(date +%s) - $(date -d "$BACKUP_DATE" +%s)) / 86400 ))
    
    if [ $DAYS_SINCE -gt 7 ]; then
        echo "   ⚠️  最近备份: $BACKUP_DATE ($DAYS_SINCE 天前) → 建议定期备份"
        DIAGNOSES+=("运行记忆备份: bash scripts/backup_memory.sh")
    else
        echo "   ✅ 最近备份: $BACKUP_DATE"
    fi
else
    echo "   ⚠️  未发现备份 → 建议定期备份记忆文件"
    DIAGNOSES+=("创建记忆备份")
fi

# 总结
echo ""
echo "═══════════════════════════════════════════════════════"

if [ ${#DIAGNOSES[@]} -eq 0 ]; then
    echo "✅ 记忆系统健康！未发现问题"
else
    echo "📋 发现 ${#DIAGNOSES[@]} 个优化建议："
    echo ""
    for i in "${!DIAGNOSES[@]}"; do
        echo "   $((i+1)). ${DIAGNOSES[$i]}"
    done
    echo ""
    echo "💡 一键修复: bash scripts/install.sh"
fi

echo "═══════════════════════════════════════════════════════"