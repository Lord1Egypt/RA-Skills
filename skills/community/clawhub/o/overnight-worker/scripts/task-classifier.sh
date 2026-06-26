#!/usr/bin/env bash
# =============================================================================
# task-classifier.sh — 任务分类脚本
# 根据任务描述中的关键词判断任务类型，返回推荐的执行策略
# =============================================================================

set -euo pipefail

TASK_DESC="${1:-}"

if [[ -z "$TASK_DESC" ]]; then
    echo "用法: task-classifier.sh <任务描述>"
    exit 1
fi

# 转为小写，方便匹配
TASK_LOWER=$(echo "$TASK_DESC" | tr '[:upper:]' '[:lower:]')

# ---------- 关键词权重表 ----------
# 每个类型累计得分，最高分的类型胜出

score_research=0
score_writing=0
score_data=0
score_code_review=0

# 调研类关键词
for kw in "调研" "研究" "分析" "竞品" "对比" "市场" "趋势" "行业" "调查" \
          "research" "analyze" "compare" "competitor" "market" "survey" "investigate" \
          "benchmark" "评测" "测评" "了解" "探索" "explore"; do
    if echo "$TASK_LOWER" | grep -qi "$kw"; then
        score_research=$((score_research + 10))
    fi
done

# 写作类关键词
for kw in "写" "撰写" "起草" "文案" "报告" "文章" "博客" "邮件" "文档" "说明" \
          "write" "draft" "article" "blog" "email" "document" "report" "copy" \
          "方案" "提案" "proposal" "总结" "summary" "readme" "prd"; do
    if echo "$TASK_LOWER" | grep -qi "$kw"; then
        score_writing=$((score_writing + 10))
    fi
done

# 数据整理类关键词
for kw in "数据" "整理" "清洗" "表格" "csv" "json" "excel" "统计" "汇总" \
          "data" "clean" "transform" "aggregate" "table" "spreadsheet" "etl" \
          "格式化" "去重" "排序" "筛选" "filter" "sort" "merge" "合并"; do
    if echo "$TASK_LOWER" | grep -qi "$kw"; then
        score_data=$((score_data + 10))
    fi
done

# 代码审查类关键词
for kw in "代码" "审查" "review" "code" "重构" "refactor" "bug" "安全" "漏洞" \
          "性能" "优化" "lint" "pr" "pull request" "merge request" "codebase" \
          "源码" "源代码" "检查" "audit" "质量"; do
    if echo "$TASK_LOWER" | grep -qi "$kw"; then
        score_code_review=$((score_code_review + 10))
    fi
done

# ---------- 判定最高分 ----------
max_score=0
task_type="research"  # 默认为调研

if [[ $score_research -gt $max_score ]]; then
    max_score=$score_research
    task_type="research"
fi
if [[ $score_writing -gt $max_score ]]; then
    max_score=$score_writing
    task_type="writing"
fi
if [[ $score_data -gt $max_score ]]; then
    max_score=$score_data
    task_type="data"
fi
if [[ $score_code_review -gt $max_score ]]; then
    max_score=$score_code_review
    task_type="code-review"
fi

# 如果没有匹配到任何关键词，检查是否有混合特征
if [[ $max_score -eq 0 ]]; then
    task_type="research"  # 无法判断时默认为调研类
fi

# 检查是否有多种类型混合（第二高分达到最高分的 70%+）
scores=($score_research $score_writing $score_data $score_code_review)
types=("research" "writing" "data" "code-review")
second_max=0
second_type=""

for i in "${!scores[@]}"; do
    if [[ ${scores[$i]} -lt $max_score && ${scores[$i]} -gt $second_max ]]; then
        second_max=${scores[$i]}
        second_type="${types[$i]}"
    fi
done

# 如果第二高分 >= 最高分的 70%，标记为混合类型
if [[ $max_score -gt 0 && $second_max -gt 0 ]]; then
    threshold=$((max_score * 70 / 100))
    if [[ $second_max -ge $threshold ]]; then
        task_type="${task_type}+${second_type}"
    fi
fi

# ---------- 输出结果 ----------
# 格式: type|strategy_hint
case "$task_type" in
    research*)
        echo "${task_type}|优先使用 WebSearch 收集信息，每个关键问题至少搜索 2 个角度，结果去重后整理"
        ;;
    writing*)
        echo "${task_type}|先确定大纲结构，再逐段填充内容，最终通读一遍确保连贯性"
        ;;
    data*)
        echo "${task_type}|先明确数据源和目标格式，分批处理避免内存溢出，每批处理后验证数据完整性"
        ;;
    code-review*)
        echo "${task_type}|先全局扫描目录结构，再按模块深入审查，安全问题优先级最高"
        ;;
    *)
        echo "${task_type}|通用策略：先分析任务目标，再拆解为可执行步骤"
        ;;
esac
