#!/bin/bash
# openclaw-memory-cn 诊断脚本
# 一键检测你的 OpenClaw 记忆系统是否需要优化

set -e

MEMORY_DB="$HOME/.openclaw/memory/main.sqlite"
WORKSPACE="$HOME/.openclaw/workspace"

echo "🧠 OpenClaw 记忆系统诊断"
echo "========================"
echo ""

# 检查 SQLite 数据库
if [ ! -f "$MEMORY_DB" ]; then
    echo "❌ 找不到记忆数据库: $MEMORY_DB"
    echo "   请确认 OpenClaw 已运行过且启用了 memorySearch"
    exit 1
fi

echo "📊 基本信息"
echo "----------"
FILES=$(sqlite3 "$MEMORY_DB" "SELECT COUNT(*) FROM files;" 2>/dev/null || echo "0")
CHUNKS=$(sqlite3 "$MEMORY_DB" "SELECT COUNT(*) FROM chunks;" 2>/dev/null || echo "0")
echo "  已索引文件: $FILES"
echo "  总 chunks: $CHUNKS"
echo ""

# 检查 FTS5 中文分词问题
echo "🔍 FTS5 中文分词检测"
echo "-------------------"
LONG_TOKENS=$(sqlite3 "$MEMORY_DB" "
SELECT COUNT(*) FROM chunks_fts_vocab 
WHERE col='*' AND length(term) > 8 
AND term GLOB '*[一-龥]*[一-龥]*[一-龥]*[一-龥]*[一-龥]*[一-龥]*[一-龥]*[一-龥]*';
" 2>/dev/null || echo "error")

if [ "$LONG_TOKENS" = "error" ]; then
    echo "  ⚠️ 无法查询 FTS5 词汇表（可能没有 fts5vocab 表）"
elif [ "$LONG_TOKENS" -gt 0 ]; then
    echo "  ❌ 发现 $LONG_TOKENS 个超长中文 token（FTS5 unicode61 bug 影响了你）"
    echo "  示例："
    sqlite3 "$MEMORY_DB" "
    SELECT '    ' || term FROM chunks_fts_vocab 
    WHERE col='*' AND length(term) > 8 
    AND term GLOB '*[一-龥]*[一-龥]*[一-龥]*[一-龥]*'
    LIMIT 5;
    " 2>/dev/null
else
    echo "  ✅ 未发现超长中文 token（FTS5 分词正常）"
fi
echo ""

# 检查记忆文件大小
echo "📁 文件大小检测"
echo "--------------"
if [ -d "$WORKSPACE/memory" ]; then
    TOTAL_SIZE=$(find "$WORKSPACE/memory" -name '*.md' -exec cat {} + 2>/dev/null | wc -c | tr -d ' ')
    LARGE_FILES=$(find "$WORKSPACE/memory" -maxdepth 1 -name '*.md' -size +30k 2>/dev/null | wc -l | tr -d ' ')
    echo "  记忆总大小: $(echo "scale=0; $TOTAL_SIZE / 1024" | bc)KB"
    echo "  超过 30KB 的日志: $LARGE_FILES 个"
    
    if [ "$LARGE_FILES" -gt 0 ]; then
        echo "  ⚠️ 以下文件建议压缩："
        find "$WORKSPACE/memory" -maxdepth 1 -name '*.md' -size +30k -exec ls -lh {} \; 2>/dev/null | awk '{print "    " $5 " " $NF}'
    fi
else
    echo "  ⚠️ 找不到 workspace/memory 目录"
fi
echo ""

# 检查 tags 覆盖率
echo "🏷️ Tags 标签覆盖率"
echo "-----------------"
if [ -d "$WORKSPACE/memory/projects" ]; then
    TOTAL_PROJECTS=$(find "$WORKSPACE/memory/projects" -name '*.md' | wc -l | tr -d ' ')
    TAGGED=$(find "$WORKSPACE/memory/projects" -name '*.md' -exec head -1 {} \; | grep -c 'tags:' || true)
    echo "  项目文件: $TOTAL_PROJECTS 个"
    echo "  已加标签: $TAGGED 个"
    
    if [ "$TAGGED" -lt "$TOTAL_PROJECTS" ]; then
        UNTAGGED=$((TOTAL_PROJECTS - TAGGED))
        echo "  ⚠️ $UNTAGGED 个项目文件缺少 tags（影响 FTS5 搜索）"
    else
        echo "  ✅ 所有项目文件都有标签"
    fi
else
    echo "  ℹ️ 没有 projects 目录"
fi
echo ""

# 检查 lessons 目录
echo "📚 知识库检测"
echo "------------"
if [ -d "$WORKSPACE/memory/lessons" ]; then
    LESSONS=$(find "$WORKSPACE/memory/lessons" -name '*.md' | wc -l | tr -d ' ')
    echo "  lessons 文件: $LESSONS 个"
    if [ "$LESSONS" -lt 3 ]; then
        echo "  ⚠️ 经验知识库较少，建议从日志中提取常见踩坑整理成 lessons/"
    else
        echo "  ✅ 知识库健康"
    fi
else
    echo "  ⚠️ 没有 lessons 目录（建议创建，这是搜索命中率最高的文件类型）"
fi
echo ""

# 总结
echo "📋 诊断总结"
echo "==========="
ISSUES=0
[ "$LONG_TOKENS" -gt 0 ] 2>/dev/null && ISSUES=$((ISSUES + 1))
[ "$LARGE_FILES" -gt 0 ] 2>/dev/null && ISSUES=$((ISSUES + 1))
[ "$TAGGED" -lt "$TOTAL_PROJECTS" ] 2>/dev/null && ISSUES=$((ISSUES + 1))

if [ "$ISSUES" -eq 0 ]; then
    echo "✅ 你的记忆系统状态良好！"
else
    echo "发现 $ISSUES 个可优化项，建议："
    echo "  1. 运行: openclaw config patch < config/memory-search.json"
    echo "  2. 运行: python3 scripts/add-tags.py $WORKSPACE/memory/projects/"
    echo "  3. 运行: python3 scripts/compress-logs.py $WORKSPACE/memory/"
    echo "  4. 运行: openclaw memory index --force"
    echo ""
    echo "详见 README.md 获取完整指南。"
fi
