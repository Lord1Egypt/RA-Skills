#!/usr/bin/env python3
"""
case_divergence.py — 类案裁判差异分析

对比多个类案的裁判结果，识别裁判分歧点，输出"同案不同判"风险提示。

用法：
    from case_divergence import analyze_divergence
    report = analyze_divergence(case_results, current_conclusion="支持原告诉请")
"""

import re
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class DivergencePoint:
    """裁判分歧点"""
    issue: str                  # 争议问题
    position_a: str             # 观点A
    position_b: str             # 观点B
    case_a: str                 # 支持观点A的案例
    case_b: str                 # 支持观点B的案例
    risk_level: str             # 风险等级（high/medium/low）
    suggestion: str             # 建议


@dataclass
class DivergenceReport:
    """差异分析报告"""
    total_cases: int            # 分析案例数
    divergence_points: list     # 分歧点列表
    risk_summary: str           # 风险摘要
    consistency_score: float    # 一致性评分（0-1，1=完全一致）
    recommendations: list       # 建议列表


# ─── 常见裁判分歧模式 ─────────────────────────────────
DIVERGENCE_PATTERNS = {
    "利息保护上限": {
        "keywords": ["利息", "利率", "年利率", "LPR", "四倍"],
        "positions": [
            ("按合同约定支持", "约定利率未超过法定上限"),
            ("按LPR四倍调整", "超过LPR四倍部分不予保护"),
        ],
        "risk": "high",
    },
    "保证责任方式": {
        "keywords": ["保证", "连带责任", "一般保证", "担保"],
        "positions": [
            ("认定为连带责任保证", "明确约定连带责任"),
            ("认定为一般保证", "未明确约定保证方式"),
        ],
        "risk": "medium",
    },
    "违约金调整": {
        "keywords": ["违约金", "过高", "调整", "实际损失"],
        "positions": [
            ("按合同约定支持", "违约金未明显过高"),
            ("酌情调减", "违约金明显高于实际损失"),
        ],
        "risk": "medium",
    },
    "举证责任分配": {
        "keywords": ["举证责任", "证明责任", "举证倒置"],
        "positions": [
            ("原告承担举证责任", "谁主张谁举证"),
            ("被告承担举证责任", "举证责任倒置"),
        ],
        "risk": "high",
    },
    "合同效力认定": {
        "keywords": ["合同效力", "无效", "可撤销", "效力"],
        "positions": [
            ("认定合同有效", "双方真实意思表示"),
            ("认定合同无效/可撤销", "存在欺诈/胁迫/重大误解"),
        ],
        "risk": "high",
    },
}


def _detect_divergence_patterns(texts: list[str]) -> list[dict]:
    """检测文本中的裁判分歧模式"""
    detected = []
    
    for issue, config in DIVERGENCE_PATTERNS.items():
        match_count = 0
        for text in texts:
            if any(kw in text for kw in config["keywords"]):
                match_count += 1
        
        if match_count >= 2:
            detected.append({
                "issue": issue,
                "keywords": config["keywords"],
                "positions": config["positions"],
                "risk": config["risk"],
            })
    
    return detected


def analyze_divergence(
    case_results: list,
    current_conclusion: str = "",
) -> DivergenceReport:
    """
    分析类案裁判差异。
    
    Args:
        case_results: CaseResult 列表或摘要文本列表
        current_conclusion: 当前案件的拟判结论
    
    Returns:
        DivergenceReport 包含分歧点和风险提示
    """
    # 提取文本
    texts = []
    case_names = []
    for r in case_results:
        if hasattr(r, "summary"):
            texts.append(r.summary)
            case_names.append(getattr(r, "case_number", "") or "未知案例")
        elif isinstance(r, str):
            texts.append(r)
            case_names.append("案例")
    
    # 检测分歧模式
    patterns = _detect_divergence_patterns(texts)
    
    # 构建分歧点
    divergence_points = []
    for pattern in patterns:
        # 分析每个案例倾向哪个观点
        for i, (pos_a, pos_b) in enumerate([pattern["positions"]]):
            case_a = case_names[0] if len(case_names) > 0 else ""
            case_b = case_names[1] if len(case_names) > 1 else ""
            
            divergence_points.append(DivergencePoint(
                issue=pattern["issue"],
                position_a=pos_a,
                position_b=pos_b,
                case_a=case_a,
                case_b=case_b,
                risk_level=pattern["risk"],
                suggestion=f"建议在说理部分明确论证为何采用{pos_a}而非{pos_b}",
            ))
    
    # 如果有当前结论，检查是否与类案一致
    recommendations = []
    if current_conclusion and divergence_points:
        for dp in divergence_points:
            if dp.risk_level == "high":
                recommendations.append(
                    f"⚠️ {dp.issue}存在裁判分歧（{dp.risk_level}风险），"
                    f"建议在说理部分明确回应为何采用此裁判路径"
                )
    
    # 一致性评分
    if not divergence_points:
        consistency = 1.0
    else:
        high_risk = sum(1 for dp in divergence_points if dp.risk_level == "high")
        medium_risk = sum(1 for dp in divergence_points if dp.risk_level == "medium")
        consistency = max(0, 1.0 - high_risk * 0.3 - medium_risk * 0.15)
    
    # 风险摘要
    if not divergence_points:
        risk_summary = "未发现明显裁判分歧，类案裁判较为一致"
    else:
        high_count = sum(1 for dp in divergence_points if dp.risk_level == "high")
        if high_count > 0:
            risk_summary = f"发现 {high_count} 个高风险分歧点，建议重点关注"
        else:
            risk_summary = f"发现 {len(divergence_points)} 个中低风险分歧点"
    
    if not recommendations:
        recommendations.append("类案裁判较为一致，可参考类案裁判思路")
    
    return DivergenceReport(
        total_cases=len(texts),
        divergence_points=[asdict(dp) for dp in divergence_points],
        risk_summary=risk_summary,
        consistency_score=round(consistency, 2),
        recommendations=recommendations,
    )


def format_divergence_report(report: DivergenceReport) -> str:
    """格式化差异分析报告"""
    lines = []
    lines.append("## 类案裁判差异分析")
    lines.append(f"分析案例数：{report.total_cases} | 一致性评分：{report.consistency_score}")
    lines.append(f"**风险摘要**：{report.risk_summary}")
    lines.append("")
    
    if report.divergence_points:
        lines.append("### 裁判分歧点")
        for i, dp in enumerate(report.divergence_points, 1):
            risk_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(dp["risk_level"], "⚪")
            lines.append(f"{i}. {risk_icon} **{dp['issue']}**（{dp['risk_level']}风险）")
            lines.append(f"   - 观点A：{dp['position_a']}")
            lines.append(f"   - 观点B：{dp['position_b']}")
            lines.append(f"   - 建议：{dp['suggestion']}")
            lines.append("")
    
    if report.recommendations:
        lines.append("### 建议")
        for r in report.recommendations:
            lines.append(f"- {r}")
    
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    # 示例用法
    sample_cases = [
        "借贷双方约定年利率18%，借款人主张过高请求调整。法院按LPR四倍保护。",
        "借贷合同约定年利率15%，出借人请求按约定支持。法院认为未超过法定上限，予以支持。",
    ]
    
    report = analyze_divergence(sample_cases, "支持原告诉请")
    print(format_divergence_report(report))
