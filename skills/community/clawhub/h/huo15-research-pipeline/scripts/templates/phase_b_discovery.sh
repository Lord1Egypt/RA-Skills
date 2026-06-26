#!/bin/bash
#===============================================
# Phase B: 文献发现与筛选 Prompt 模板
#===============================================

TOPIC="$1"
SCOPE_FILE="$2"
OUTPUT_FILE="$3"

SCOPE_CONTENT=$(cat "$SCOPE_FILE" 2>/dev/null || echo "无")

DISCOVERY_PROMPT="你是一个文献检索专家。用户正在研究以下课题：

课题: ${TOPIC}

Phase A 产出的研究问题摘要:
${SCOPE_CONTENT}

请执行以下任务：

1. **生成关键词列表**：列出 10-15 个用于搜索的关键词（中英文），包括同义词和下位词
2. **文献搜索**：基于上述关键词，搜索相关学术论文、技术报告、博客文章
3. **文献筛选**：从搜索结果中筛选出 8-15 篇高质量文献，说明筛选标准
4. **文献列表**：每篇文献包含：标题、作者/来源、年份、URL、摘要要点（3-5句）、相关性评分（1-10）

请用中文输出，Markdown 格式。如果无法访问学术数据库，请使用网络搜索补充。"

echo "$DISCOVERY_PROMPT" > "$OUTPUT_FILE"
echo "[Phase B] Prompt 已保存至 $OUTPUT_FILE"
