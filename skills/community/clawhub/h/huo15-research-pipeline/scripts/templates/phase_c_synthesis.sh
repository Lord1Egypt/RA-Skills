#!/bin/bash
#===============================================
# Phase C: 知识综合与假设生成 Prompt 模板
#===============================================

TOPIC="$1"
SCOPE_FILE="$2"
DISCOVERY_FILE="$3"
OUTPUT_FILE="$4"

SCOPE_CONTENT=$(cat "$SCOPE_FILE" 2>/dev/null || echo "无")
DISCOVERY_CONTENT=$(cat "$DISCOVERY_FILE" 2>/dev/null || echo "无")

SYNTHESIS_PROMPT="你是一个研究分析师。请综合以下研究范围和文献发现，生成假设和知识综合报告。

## 研究课题
${TOPIC}

## 研究范围定义
${SCOPE_CONTENT}

## 文献发现
${DISCOVERY_CONTENT}

请执行以下任务：

1. **知识图谱摘要**（200-300字）：总结该领域当前研究状态和主要发现
2. **核心发现列表**：列出 5-8 个经过文献验证的核心发现
3. **研究缺口**：找出当前研究中的空白或争议点
4. **假设 / 待验证命题**：基于核心发现，生成 3-5 个可验证的假设或待验证命题
5. **理论框架**：提出支撑假设的理论框架或概念模型
6. **方法论建议**：适合验证假设的研究方法

请用中文输出，Markdown 格式。"

echo "$SYNTHESIS_PROMPT" > "$OUTPUT_FILE"
echo "[Phase C] Prompt 已保存至 $OUTPUT_FILE"
