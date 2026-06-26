#!/bin/bash
#===============================================
# huo15-research-pipeline
# 从想法到论文的全自主研究管道
#===============================================

set -e

# 参数
TOPIC="$1"
DATE=$(date +%Y-%m-%d)
SLUG=$(echo "$TOPIC" | tr ' ' '-' | tr -d ':/?&' | cut -c1-50)

# 目录
RESEARCH_DIR="$HOME/.openclaw/agents/main/agent/kb/raw/research-${SLUG}-${DATE}"
mkdir -p "$RESEARCH_DIR"

LOG="$RESEARCH_DIR/log.txt"
echo "========================================" | tee -a "$LOG"
echo "研究管道启动: $TOPIC" | tee -a "$LOG"
echo "时间: $(date)" | tee -a "$LOG"
echo "输出目录: $RESEARCH_DIR" | tee -a "$LOG"
echo "========================================" | tee -a "$LOG"

#---------------------------------------
# 通用：调用 LLM 生成内容
#---------------------------------------
call_llm() {
  local prompt="$1"
  local output_file="$2"
  local model="${3:-minimax/MiniMax-M2.7-highspeed}"

  echo "[LLM] 生成中..." | tee -a "$LOG"

  local response
  response=$(openclaw llm generate \
    --model "$model" \
    --prompt "$prompt" 2>&1) || true

  if [ -n "$response" ]; then
    echo "$response" > "$output_file"
    echo "[LLM] 已保存至 $output_file ($(wc -c < "$output_file") bytes)" | tee -a "$LOG"
  else
    echo "[LLM] 警告: 未获取到响应" | tee -a "$LOG"
    echo "# 无内容" > "$output_file"
  fi
}

#---------------------------------------
# 通用：Web 搜索
#---------------------------------------
web_search() {
  local query="$1"
  echo "[搜索] $query" | tee -a "$LOG"
  openclaw web search --query "$query" --count 5 2>&1 || true
}

#---------------------------------------
# HITL：等待用户确认
#---------------------------------------
hitl() {
  local phase_name="$1"
  local output_file="$2"
  echo ""
  echo "========================================" | tee -a "$LOG"
  echo " Phase $phase_name 完成" | tee -a "$LOG"
  echo "========================================" | tee -a "$LOG"
  echo "产出预览:" | tee -a "$LOG"
  head -20 "$output_file" | tee -a "$LOG"
  echo "...(已保存至 $output_file)" | tee -a "$LOG"
  echo ""
  read -p "→ 输入 [c]继续 [a]调整 [q]退出: " user_input
  case "$user_input" in
    q|Q) echo "[退出] 研究管道终止"; exit 0 ;;
    a|A) echo "[调整] 请说明要调整的内容..."; read -r adjustment; return 1 ;;
    *)   echo "[继续] 进入下一阶段..." ;;
  esac
  return 0
}

#---------------------------------------
# Phase A: 研究范围定义
#---------------------------------------
phase_a() {
  echo ""
  echo "=== Phase A: 研究范围定义 ===" | tee -a "$LOG"

  local prompt="你是一个研究顾问。用户要研究以下课题：

课题: $TOPIC

请生成一份研究范围定义文档，包含：

1. **研究问题**：列出 1-3 个核心研究问题（精确、可验证）
2. **研究目标**：用 SMART 格式（具体、可衡量、可实现、相关、有时限）描述研究目标
3. **范围边界**：
   - In-scope（包含的内容）
   - Out-of-scope（不包含的内容）
4. **成功标准**：如何判断研究成功了？列出 3-5 个具体指标
5. **研究类型**：实证研究 / 理论研究 / 案例研究 / 文献综述

请用中文输出，Markdown 格式。"

  call_llm "$prompt" "$RESEARCH_DIR/00_scope.md"

  local retry=0
  while true; do
    if hitl "A" "$RESEARCH_DIR/00_scope.md"; then
      break
    fi
    retry=$((retry + 1))
    if [ $retry -gt 3 ]; then
      echo "[重试上限] 继续进入下一阶段"
      break
    fi
  done
}

#---------------------------------------
# Phase B: 文献发现
#---------------------------------------
phase_b() {
  echo ""
  echo "=== Phase B: 文献发现与筛选 ===" | tee -a "$LOG"

  # 读取 Phase A 的研究问题用于指导搜索
  local research_questions=""
  if [ -f "$RESEARCH_DIR/00_scope.md" ]; then
    research_questions=$(grep -A5 "研究问题" "$RESEARCH_DIR/00_scope.md" | head -20 || true)
  fi

  local prompt="你是一个文献检索专家。用户正在研究以下课题：

课题: $TOPIC

Phase A 产出的研究问题摘要:
$research_questions

请执行以下任务：

1. **生成关键词列表**：列出 10-15 个用于搜索的关键词（中英文），包括同义词和下位词
2. **文献搜索**：基于上述关键词，搜索相关学术论文、技术报告、博客文章
3. **文献筛选**：从搜索结果中筛选出 8-15 篇高质量文献，说明筛选标准
4. **文献列表**：每篇文献包含：标题、作者/来源、年份、URL、摘要要点（3-5句）、相关性评分（1-10）

请用中文输出，Markdown 格式。如果无法访问学术数据库，请使用网络搜索补充。"

  call_llm "$prompt" "$RESEARCH_DIR/01_discovery.md"

  local retry=0
  while true; do
    if hitl "B" "$RESEARCH_DIR/01_discovery.md"; then
      break
    fi
    retry=$((retry + 1))
    if [ $retry -gt 3 ]; then
      echo "[重试上限] 继续进入下一阶段"
      break
    fi
  done
}

#---------------------------------------
# Phase C: 知识综合
#---------------------------------------
phase_c() {
  echo ""
  echo "=== Phase C: 知识综合与假设生成 ===" | tee -a "$LOG"

  local scope_content=""
  local discovery_content=""
  [ -f "$RESEARCH_DIR/00_scope.md" ] && scope_content=$(cat "$RESEARCH_DIR/00_scope.md")
  [ -f "$RESEARCH_DIR/01_discovery.md" ] && discovery_content=$(cat "$RESEARCH_DIR/01_discovery.md")

  local prompt="你是一个研究分析师。请综合以下研究范围和文献发现，生成假设和知识综合报告。

## 研究课题
$TOPIC

## 研究范围定义
$scope_content

## 文献发现
$discovery_content

请执行以下任务：

1. **知识图谱摘要**（200-300字）：总结该领域当前研究状态和主要发现
2. **核心发现列表**：列出 5-8 个经过文献验证的核心发现
3. **研究缺口**：找出当前研究中的空白或争议点
4. **假设 / 待验证命题**：基于核心发现，生成 3-5 个可验证的假设或待验证命题
5. **理论框架**：提出支撑假设的理论框架或概念模型
6. **方法论建议**：适合验证假设的研究方法

请用中文输出，Markdown 格式。"

  call_llm "$prompt" "$RESEARCH_DIR/02_synthesis.md"

  local retry=0
  while true; do
    if hitl "C" "$RESEARCH_DIR/02_synthesis.md"; then
      break
    fi
    retry=$((retry + 1))
    if [ $retry -gt 3 ]; then
      echo "[重试上限] 继续进入下一阶段"
      break
    fi
  done
}

#---------------------------------------
# Phase D: 实验设计
#---------------------------------------
phase_d() {
  echo ""
  echo "=== Phase D: 实验设计与执行 ===" | tee -a "$LOG"

  local synthesis_content=""
  [ -f "$RESEARCH_DIR/02_synthesis.md" ] && synthesis_content=$(cat "$RESEARCH_DIR/02_synthesis.md")

  local prompt="你是一个实验设计专家。请为以下研究假设设计实验方案。

## 研究课题
$TOPIC

## Phase C 知识综合
$synthesis_content

请执行以下任务：

1. **实验设计方案**：为每个假设设计具体的实验方案（描述实验组/对照组、变量设置）
2. **数据需求**：
   - 需要什么类型的数据？
   - 数据来源在哪里？
   - 数据量预估
3. **实验步骤**：详细的实验执行步骤（分步说明）
4. **评估指标**：定义如何衡量实验成功（准确率、提升幅度、A/B测试指标等）
5. **潜在偏差与控制**：识别可能的混杂变量和消除方法
6. **伦理考量**：实验是否涉及伦理问题？如何处理？
7. **资源需求**：计算资源、数据存储、工具依赖

如果该研究不适合实验方法（如纯理论研究或文献综述），请说明并提供替代验证方案。

请用中文输出，Markdown 格式。"

  call_llm "$prompt" "$RESEARCH_DIR/03_experiment.md"

  local retry=0
  while true; do
    if hitl "D" "$RESEARCH_DIR/03_experiment.md"; then
      break
    fi
    retry=$((retry + 1))
    if [ $retry -gt 3 ]; then
      echo "[重试上限] 继续进入下一阶段"
      break
    fi
  done
}

#---------------------------------------
# Phase E: 结果分析
#---------------------------------------
phase_e() {
  echo ""
  echo "=== Phase E: 结果分析 ===" | tee -a "$LOG"

  local experiment_content=""
  [ -f "$RESEARCH_DIR/03_experiment.md" ] && experiment_content=$(cat "$RESEARCH_DIR/03_experiment.md")

  local prompt="你是一个数据分析专家。请基于实验设计方案，提供结果分析框架。

## 研究课题
$TOPIC

## Phase D 实验设计
$experiment_content

请执行以下任务：

1. **结果分析框架**：描述如何分析实验/研究结果（统计分析方法、可视化方案）
2. **预期结果模式**：描述可能的几种结果模式及其解读方式
3. **统计显著性判断**：如何判断结果是否具有统计显著性（置信区间、p值等）
4. **结果解读指南**：不同类型的结果应如何解读
5. **敏感性分析**：如何检验结果对假设条件的敏感性
6. **局限性讨论**：本研究的潜在局限性

如果用户已有实验数据，请替换上述内容并提供实际分析。

请用中文输出，Markdown 格式。"

  call_llm "$prompt" "$RESEARCH_DIR/04_analysis.md"

  local retry=0
  while true; do
    if hitl "E" "$RESEARCH_DIR/04_analysis.md"; then
      break
    fi
    retry=$((retry + 1))
    if [ $retry -gt 3 ]; then
      echo "[重试上限] 继续进入下一阶段"
      break
    fi
  done
}

#---------------------------------------
# Phase F: 论文撰写
#---------------------------------------
phase_f() {
  echo ""
  echo "=== Phase F: 论文撰写 ===" | tee -a "$LOG"

  local scope_content=""
  local discovery_content=""
  local synthesis_content=""
  local experiment_content=""
  local analysis_content=""

  [ -f "$RESEARCH_DIR/00_scope.md" ] && scope_content=$(cat "$RESEARCH_DIR/00_scope.md")
  [ -f "$RESEARCH_DIR/01_discovery.md" ] && discovery_content=$(cat "$RESEARCH_DIR/01_discovery.md")
  [ -f "$RESEARCH_DIR/02_synthesis.md" ] && synthesis_content=$(cat "$RESEARCH_DIR/02_synthesis.md")
  [ -f "$RESEARCH_DIR/03_experiment.md" ] && experiment_content=$(cat "$RESEARCH_DIR/03_experiment.md")
  [ -f "$RESEARCH_DIR/04_analysis.md" ] && analysis_content=$(cat "$RESEARCH_DIR/04_analysis.md")

  local prompt="你是一个学术论文撰写专家。请基于以下所有研究阶段产出，撰写一篇完整的学术论文。

## 研究课题
$TOPIC

## Phase A - 研究范围
$scope_content

## Phase B - 文献发现
$discovery_content

## Phase C - 知识综合
$synthesis_content

## Phase D - 实验设计
$experiment_content

## Phase E - 结果分析框架
$analysis_content

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

  call_llm "$prompt" "$RESEARCH_DIR/05_paper.md"

  echo ""
  echo "========================================" | tee -a "$LOG"
  echo " Phase F: 论文撰写 完成" | tee -a "$LOG"
  echo "========================================" | tee -a "$LOG"
  echo "产出: $RESEARCH_DIR/05_paper.md" | tee -a "$LOG"
}

#---------------------------------------
# 输出到 Obsidian（可选）
#---------------------------------------
output_to_obsidian() {
  echo ""
  echo "=== 同步到 Obsidian ===" | tee -a "$LOG"

  if command -v obsidian &>/dev/null; then
    obsidian new research --title "$TOPIC" --folder "research" 2>&1 || true
  fi

  echo "[Obsidian] 可手动导入以下文件:"
  echo "  $RESEARCH_DIR/05_paper.md"
}

#---------------------------------------
# 主流程
#---------------------------------------
main() {
  if [ -z "$TOPIC" ]; then
    echo "用法: $0 <研究课题>"
    echo "示例: $0 \"大语言模型在代码补全任务中的性能评估\""
    exit 1
  fi

  echo "[研究管道] 启动: $TOPIC"
  echo "[输出目录] $RESEARCH_DIR"

  phase_a
  phase_b
  phase_c
  phase_d
  phase_e
  phase_f

  echo ""
  echo "========================================"
  echo "研究管道完成！"
  echo "========================================"
  echo "所有产出保存在: $RESEARCH_DIR"
  echo ""
  echo "文件列表:"
  ls -lh "$RESEARCH_DIR"/*.md 2>/dev/null || echo "  (无文件)"
  echo ""

  output_to_obsidian

  echo ""
  echo "如需继续编辑论文，请查看: $RESEARCH_DIR/05_paper.md"
}

main "$@"
