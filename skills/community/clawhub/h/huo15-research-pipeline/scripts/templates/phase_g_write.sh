#!/bin/bash
#===============================================
# Phase G: 论文撰写 Prompt 模板
#===============================================

TOPIC="$1"
SCOPE_FILE="$2"
DISCOVERY_FILE="$3"
SYNTHESIS_FILE="$4"
EXPERIMENT_FILE="$5"
ANALYSIS_FILE="$6"
OUTPUT_FILE="$7"

SCOPE_CONTENT=$(cat "$SCOPE_FILE" 2>/dev/null || echo "无")
DISCOVERY_CONTENT=$(cat "$DISCOVERY_FILE" 2>/dev/null || echo "无")
SYNTHESIS_CONTENT=$(cat "$SYNTHESIS_FILE" 2>/dev/null || echo "无")
EXPERIMENT_CONTENT=$(cat "$EXPERIMENT_FILE" 2>/dev/null || echo "无")
ANALYSIS_CONTENT=$(cat "$ANALYSIS_FILE" 2>/dev/null || echo "无")

PAPER_PROMPT="你是一个学术论文撰写专家。请基于以下所有研究阶段产出，撰写一篇完整的学术论文。

## 研究课题
${TOPIC}

## Phase A - 研究范围
${SCOPE_CONTENT}

## Phase B - 文献发现
${DISCOVERY_CONTENT}

## Phase C - 知识综合
${SYNTHESIS_CONTENT}

## Phase D - 实验设计
${EXPERIMENT_CONTENT}

## Phase E - 结果分析框架
${ANALYSIS_CONTENT}

请撰写一篇结构完整的学术论文，包含：

1. **标题**（中英文）
2. **摘要**（200-300字，中英文）
3. **关键词**（5-8个，中英文）
4. **引言**（研究背景、动机、贡献）
5. **相关工作**（文献综述）
6. **方法**（详细方法论）
7. **结果**（基于分析框架的预期/实际结果）
8. **讨论**（结果解读、局限性、未来工作）
9. **结论**
10. **参考文献**（列出引用的文献）

请用中文撰写主要部分，英文标题和关键词。Markdown 格式，便于后续编辑转换。

注意：
- 论点要清晰，论据要充分
- 保持学术写作规范
- 字数目标：3000-6000字（正文）
- 图表可用 Markdown 表格占位"

echo "$PAPER_PROMPT" > "$OUTPUT_FILE"
echo "[Phase G] Prompt 已保存至 $OUTPUT_FILE"
