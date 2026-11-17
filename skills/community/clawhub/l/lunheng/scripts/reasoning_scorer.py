#!/usr/bin/env python3
"""
reasoning_scorer.py — 说理质量评分器

自动评估生成文书的说理质量，输出 6 维度评分 + 总分 + 差距分析。
与获奖文书基线对比，量化"好不好"。

用法：
    from reasoning_scorer import score_judgment
    report = score_judgment(judgment_text, cause="民间借贷纠纷")
    print(report.total_score)  # 0-60
"""

import re
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── 维度定义 ──────────────────────────────────────────
DIMENSIONS = {
    "争议焦点归纳": {
        "weight": 10,
        "keywords": ["争议焦点", "本案的争议", "双方争议", "焦点在于", "本案关键"],
        "negative": ["无争议", "没有争议"],
    },
    "法条引用准确度": {
        "weight": 10,
        "keywords": ["民法典", "刑法", "民事诉讼法", "行政诉讼法", "司法解释",
                      "第.*条", "根据.*规定", "依照.*法律"],
        "negative": ["已废止", "失效"],
    },
    "构成要件分析": {
        "weight": 10,
        "keywords": ["构成要件", "要件分析", "法律构成", "成立条件",
                      "应当具备", "需要满足", "前提条件"],
        "negative": [],
    },
    "事实认定与证据": {
        "weight": 10,
        "keywords": ["经审理查明", "本院认定", "证据证明", "证据链",
                      "举证责任", "证明标准", "高度盖然性"],
        "negative": ["证据不足", "无法证明"],
    },
    "逻辑连贯性": {
        "weight": 10,
        "keywords": ["因此", "故", "据此", "综上", "由此可见",
                      "基于上述", "综上所述", "理由如下"],
        "negative": ["但是", "然而", "不过"],  # 过多转折=逻辑不清晰
    },
    "语言规范性": {
        "weight": 10,
        "keywords": ["本院认为", "判决如下", "驳回", "支持",
                      "审判长", "审判员", "书记员"],
        "negative": ["我觉得", "可能", "大概", "也许", "应该吧"],
    },
}


@dataclass
class DimensionScore:
    """单维度评分"""
    name: str               # 维度名称
    score: float            # 得分（0-10）
    max_score: float        # 满分
    matched_keywords: list  # 匹配到的关键词
    issues: list            # 发现的问题
    suggestion: str         # 改进建议


@dataclass
class QualityReport:
    """质量评估报告"""
    cause: str                          # 案由
    total_score: float                  # 总分（0-60）
    max_total: float                    # 满分（60）
    percentage: float                   # 百分比
    grade: str                          # 等级（A/B/C/D/F）
    dimensions: list                    # 各维度评分（DimensionScore dict）
    strengths: list                     # 优势项
    weaknesses: list                    # 薄弱项
    improvement_suggestions: list       # 综合改进建议
    baseline_comparison: str            # 与获奖文书基线对比


def _count_keyword_matches(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    """统计关键词匹配数"""
    matched = []
    for kw in keywords:
        if re.search(kw, text):
            matched.append(kw)
    return len(matched), matched


def _count_negative_matches(text: str, negatives: list[str]) -> tuple[int, list[str]]:
    """统计负面关键词匹配数"""
    matched = []
    for neg in negatives:
        count = len(re.findall(neg, text))
        if count > 0:
            matched.append(f"{neg}({count}次)")
    return len(matched), matched


def _score_dimension(text: str, dim_name: str, dim_config: dict) -> DimensionScore:
    """评估单个维度"""
    max_score = dim_config["weight"]
    keywords = dim_config["keywords"]
    negatives = dim_config.get("negative", [])
    
    # 正面匹配
    pos_count, pos_matched = _count_keyword_matches(text, keywords)
    # 负面匹配
    neg_count, neg_matched = _count_negative_matches(text, negatives)
    
    # 基础分 = 正面匹配比例 * 满分
    if keywords:
        base_score = (pos_count / len(keywords)) * max_score
    else:
        base_score = max_score * 0.5
    
    # 负面扣分（每个负面项扣 2 分，最多扣 4 分）
    neg_penalty = min(neg_count * 2, 4)
    
    # 最终得分
    score = max(0, min(max_score, base_score - neg_penalty))
    
    # 生成建议
    issues = []
    suggestion = ""
    if score < max_score * 0.3:
        issues.append(f"{dim_name}严重不足")
        suggestion = f"建议加强{dim_name}，参考获奖文书的写法"
    elif score < max_score * 0.6:
        issues.append(f"{dim_name}有待提升")
        suggestion = f"建议补充{dim_name}相关内容"
    else:
        suggestion = f"{dim_name}表现良好"
    
    if neg_matched:
        issues.extend([f"存在不当表述: {m}" for m in neg_matched])
    
    return DimensionScore(
        name=dim_name,
        score=round(score, 1),
        max_score=max_score,
        matched_keywords=pos_matched,
        issues=issues,
        suggestion=suggestion,
    )


def _calculate_grade(percentage: float) -> str:
    """计算等级"""
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def _generate_improvement_suggestions(dimensions: list[DimensionScore]) -> list[str]:
    """生成综合改进建议"""
    suggestions = []
    
    # 找出得分最低的 2 个维度
    sorted_dims = sorted(dimensions, key=lambda d: d.score / d.max_score)
    
    for dim in sorted_dims[:2]:
        ratio = dim.score / dim.max_score
        if ratio < 0.5:
            if dim.name == "争议焦点归纳":
                suggestions.append("在\"本院认为\"开头先明确归纳争议焦点，用\"本案的争议焦点在于...\"引导")
            elif dim.name == "法条引用准确度":
                suggestions.append("引用法条时写全称+条款号，如\"《中华人民共和国民法典》第六百六十七条\"")
            elif dim.name == "构成要件分析":
                suggestions.append("对每个争议焦点，先列出法律构成要件，再逐一对应事实分析")
            elif dim.name == "事实认定与证据":
                suggestions.append("事实认定部分引用具体证据，说明证据来源和证明目的")
            elif dim.name == "逻辑连贯性":
                suggestions.append("使用\"因此\"\"据此\"\"综上\"等连接词，确保推理链完整")
            elif dim.name == "语言规范性":
                suggestions.append("避免口语化表述，使用\"本院认为\"\"经审理查明\"等规范用语")
    
    # 通用建议
    if any(d.score / d.max_score < 0.4 for d in dimensions):
        suggestions.append("整体说理深度不足，建议参考优秀文书范式（style_retriever 输出）")
    
    return suggestions


def _compare_baseline(total_score: float, max_total: float) -> str:
    """与获奖文书基线对比"""
    percentage = (total_score / max_total) * 100 if max_total > 0 else 0
    
    # 获奖文书平均分估算（基于评审标准）
    baseline_high = 52   # 一等奖水平（87%）
    baseline_mid = 45    # 二等奖水平（75%）
    baseline_low = 38    # 入围水平（63%）
    
    if total_score >= baseline_high:
        return f"达到获奖文书优秀水平（{baseline_high}/{max_total}），接近一等奖标准"
    elif total_score >= baseline_mid:
        return f"达到获奖文书良好水平（{baseline_mid}/{max_total}），接近二等奖标准"
    elif total_score >= baseline_low:
        return f"达到获奖文书入围水平（{baseline_low}/{max_total}），仍有提升空间"
    else:
        return f"低于获奖文书入围标准（{baseline_low}/{max_total}），建议重点加强说理深度"


def score_judgment(judgment_text: str, cause: str = "") -> QualityReport:
    """
    评估裁判文书的说理质量。
    
    Args:
        judgment_text: 判决书全文
        cause: 案由（可选，用于基线对比）
    
    Returns:
        QualityReport 包含 6 维度评分 + 总分 + 改进建议
    """
    if not judgment_text or len(judgment_text) < 100:
        return QualityReport(
            cause=cause,
            total_score=0,
            max_total=60,
            percentage=0,
            grade="F",
            dimensions=[],
            strengths=[],
            weaknesses=["文书内容过短，无法评估"],
            improvement_suggestions=["请提供完整的判决书文本"],
            baseline_comparison="文书内容不足，无法对比",
        )
    
    # 评估各维度
    dimensions = []
    for dim_name, dim_config in DIMENSIONS.items():
        dim_score = _score_dimension(judgment_text, dim_name, dim_config)
        dimensions.append(dim_score)
    
    # 计算总分
    total_score = sum(d.score for d in dimensions)
    max_total = sum(d.max_score for d in dimensions)
    percentage = round((total_score / max_total) * 100, 1) if max_total > 0 else 0
    grade = _calculate_grade(percentage)
    
    # 优势和薄弱项
    strengths = [d.name for d in dimensions if d.score / d.max_score >= 0.7]
    weaknesses = [d.name for d in dimensions if d.score / d.max_score < 0.5]
    
    # 改进建议
    suggestions = _generate_improvement_suggestions(dimensions)
    
    # 基线对比
    baseline = _compare_baseline(total_score, max_total)
    
    return QualityReport(
        cause=cause,
        total_score=round(total_score, 1),
        max_total=max_total,
        percentage=percentage,
        grade=grade,
        dimensions=[asdict(d) for d in dimensions],
        strengths=strengths,
        weaknesses=weaknesses,
        improvement_suggestions=suggestions,
        baseline_comparison=baseline,
    )


def format_report(report: QualityReport) -> str:
    """格式化评估报告为可读文本"""
    lines = []
    lines.append(f"## 说理质量评估报告")
    lines.append(f"案由：{report.cause}")
    lines.append(f"**总分：{report.total_score}/{report.max_total}（{report.percentage}%）| 等级：{report.grade}**")
    lines.append("")
    
    # 维度详情
    lines.append("### 各维度评分")
    for d in report.dimensions:
        bar = "█" * int(d["score"]) + "░" * int(d["max_score"] - d["score"])
        lines.append(f"- {d['name']}: {d['score']}/{d['max_score']} {bar}")
    lines.append("")
    
    # 优势
    if report.strengths:
        lines.append(f"**✅ 优势项**：{'、'.join(report.strengths)}")
    
    # 薄弱项
    if report.weaknesses:
        lines.append(f"**⚠️ 薄弱项**：{'、'.join(report.weaknesses)}")
    lines.append("")
    
    # 基线对比
    lines.append(f"**📊 获奖文书基线对比**：{report.baseline_comparison}")
    lines.append("")
    
    # 改进建议
    if report.improvement_suggestions:
        lines.append("### 改进建议")
        for i, s in enumerate(report.improvement_suggestions, 1):
            lines.append(f"{i}. {s}")
    
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 reasoning_scorer.py <判决书文件路径> [案由]")
        print("示例: python3 reasoning_scorer.py judgment.md 民间借贷纠纷")
        sys.exit(1)
    
    file_path = sys.argv[1]
    cause = sys.argv[2] if len(sys.argv) > 2 else ""
    
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    
    report = score_judgment(text, cause)
    print(format_report(report))
