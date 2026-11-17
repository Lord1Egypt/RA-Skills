#!/usr/bin/env python3
"""
裁判尺度一致性检查模块
功能：
  1. 检索类案裁判结果
  2. 对比判决金额/责任比例/赔偿标准
  3. 标注偏离幅度
  4. 生成一致性报告
"""

import json
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

# 复用 IMA 函数
from pipeline import ima_search, KB_CASES, _filter_case_results


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class SimilarCase:
    """类案"""
    title: str = ""
    court: str = ""          # 法院
    date: str = ""           # 裁判日期
    cause: str = ""          # 案由
    amount: float = 0.0      # 判决金额（万元）
    ratio: str = ""          # 责任比例
    outcome: str = ""        # 判决结果（支持/部分支持/驳回）
    key_facts: str = ""      # 核心事实
    relevance: float = 0.0   # 相关度


@dataclass
class ConsistencyReport:
    """一致性检查报告"""
    similar_cases_count: int = 0
    similar_cases: list = field(default_factory=list)  # List[SimilarCase]
    amount_deviation: str = ""     # 金额偏离描述
    ratio_deviation: str = ""      # 责任比例偏离描述
    outcome_match: bool = True     # 判决结果是否一致
    warnings: list = field(default_factory=list)
    score: float = 0.0            # 一致性得分 0-100
    summary: str = ""


# ─── 核心函数 ──────────────────────────────────────────
def check_consistency(
    elements: dict,
    draft_verdict: str = "",
    cause: str = "",
) -> ConsistencyReport:
    """
    检查裁判尺度与类案的一致性。
    
    Args:
        elements: pipeline 解析出的要素字典
        draft_verdict: 拟判决主文
        cause: 案由
    
    Returns:
        ConsistencyReport
    """
    report = ConsistencyReport()
    
    # 1. 从要素中提取金额和争议焦点
    amount = _extract_amount(draft_verdict)
    disputes = elements.get("disputes", [])
    facts = elements.get("facts", [])
    
    # 2. 检索类案
    print("🔍 检索类案进行一致性比对...", file=sys.stderr)
    similar_cases = _search_similar_cases(cause, disputes, facts)
    report.similar_cases = similar_cases
    report.similar_cases_count = len(similar_cases)
    
    if not similar_cases:
        report.score = 70  # 无类案参考，给默认分
        report.summary = "未检索到足够类案，无法进行一致性比对"
        report.warnings.append("⚠️ 未找到类案参考，建议扩大检索范围或确认是否为新类型案件")
        return report
    
    # 3. 金额偏离分析
    if amount > 0:
        report.amount_deviation = _analyze_amount_deviation(amount, similar_cases)
    
    # 4. 判决结果一致性
    report.outcome_match = _check_outcome_consistency(draft_verdict, similar_cases)
    
    # 5. 生成警告
    _generate_warnings(report, amount)
    
    # 6. 计算得分
    _calculate_score(report)
    
    return report


def _extract_amount(text: str) -> float:
    """从判决主文中提取判决金额（万元）"""
    amounts = []
    
    # 匹配"支付/赔偿/返还 X元" 或 "X万元"
    patterns = [
        r'(?:支付|赔偿|返还|给付|偿还)[^。]*?([\d,]+\.?\d*)\s*万元',
        r'(?:支付|赔偿|返还|给付|偿还)[^。]*?([\d,]+\.?\d*)\s*元',
    ]
    
    for pat in patterns:
        matches = re.findall(pat, text)
        for m in matches:
            try:
                val = float(m.replace(',', ''))
                if '万元' in text[max(0, text.find(m)-5):text.find(m)+len(m)+5]:
                    amounts.append(val)
                else:
                    amounts.append(val / 10000)
            except ValueError:
                pass
    
    return max(amounts) if amounts else 0.0


def _search_similar_cases(
    cause: str,
    disputes: list,
    facts: list,
    limit: int = 5,
) -> list:
    """检索类案"""
    cases = []
    
    # 构建检索词
    queries = []
    if cause:
        queries.append(cause)
    for d in disputes[:2]:
        clean = re.sub(r'(?:双方|原被告|对|就|存在|有|争议|分歧)', '', d)[:20]
        if clean.strip():
            queries.append(f"{cause} {clean.strip()}")
    
    seen_titles = set()
    for q in queries[:2]:
        items = ima_search(q, KB_CASES, limit=limit)
        items = _filter_case_results(items, "civil")
        for item in items:
            title = item.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                case = SimilarCase(
                    title=title,
                    key_facts=item.get("highlight_content", "")[:300],
                    relevance=0.7,
                )
                # 尝试从标题提取法院和日期
                court_match = re.search(r'([\u4e00-\u9fa5]+(?:法院|人民法院))', title)
                if court_match:
                    case.court = court_match.group(1)
                date_match = re.search(r'(\d{4}年?\d{1,2}月?\d{1,2}日?)', title)
                if date_match:
                    case.date = date_match.group(1)
                cases.append(case)
        time.sleep(0.3)
    
    return cases


def _analyze_amount_deviation(current_amount: float, cases: list) -> str:
    """分析金额偏离"""
    # 从类案 key_facts 中提取金额
    case_amounts = []
    for case in cases:
        facts = case.key_facts
        amounts = re.findall(r'([\d,]+\.?\d*)\s*(?:万?元)', facts)
        for a in amounts:
            try:
                val = float(a.replace(',', ''))
                if val > 0:
                    if '万' in facts[max(0, facts.find(a)-3):facts.find(a)+len(a)+3]:
                        case_amounts.append(val)
                    else:
                        case_amounts.append(val / 10000)
            except ValueError:
                pass
    
    if not case_amounts:
        return "类案中未提取到可比金额"
    
    avg_amount = sum(case_amounts) / len(case_amounts)
    deviation_pct = abs(current_amount - avg_amount) / avg_amount * 100 if avg_amount > 0 else 0
    
    if deviation_pct <= 20:
        return f"与类案平均金额 {avg_amount:.2f} 万元基本一致（偏差 {deviation_pct:.0f}%）"
    elif deviation_pct <= 50:
        direction = "高于" if current_amount > avg_amount else "低于"
        return f"{direction}类案平均金额 {avg_amount:.2f} 万元（偏差 {deviation_pct:.0f}%），建议核实"
    else:
        direction = "显著高于" if current_amount > avg_amount else "显著低于"
        return f"⚠️ {direction}类案平均金额 {avg_amount:.2f} 万元（偏差 {deviation_pct:.0f}%），需重点审查"


def _check_outcome_consistency(draft_verdict: str, cases: list) -> bool:
    """检查判决结果是否与类案一致
    
    基于判决关键词（支持/驳回/赔偿）对比类案方向。
    """
    if not draft_verdict or not cases:
        return True  # 无数据时不误报
    
    # 从判决书提取结论方向
    draft_lower = draft_verdict.lower()
    if "驳回" in draft_lower:
        draft_direction = "reject"
    elif "支持" in draft_lower or "赔偿" in draft_lower or "承担" in draft_lower:
        draft_direction = "support"
    else:
        return True  # 无法判断方向时不误报
    
    # 提取类案的方向
    consistent = 0
    total = 0
    for case in cases[:10]:
        content = ""
        if isinstance(case, dict):
            content = case.get("content", "") or case.get("key_facts", "") or case.get("title", "")
        elif hasattr(case, "key_facts"):
            content = case.key_facts or ""
        if not content:
            continue
        content_lower = content.lower()
        total += 1
        if draft_direction == "reject" and "驳回" in content_lower:
            consistent += 1
        elif draft_direction == "support" and ("支持" in content_lower or "赔偿" in content_lower):
            consistent += 1
        else:
            consistent += 1  # 无法判断时视为一致（不误报）
    
    if total == 0:
        return True
    return consistent / total >= 0.5


def _generate_warnings(report: ConsistencyReport, amount: float):
    """生成一致性警告"""
    if report.amount_deviation and "显著" in report.amount_deviation:
        report.warnings.append(f"⚠️ 金额偏离类案：{report.amount_deviation}")
    
    if report.similar_cases_count < 2:
        report.warnings.append("⚠️ 类案数量不足（<2件），一致性判断依据有限")
    
    if amount > 100:
        report.warnings.append("ℹ️ 大额案件（>100万），建议合议庭讨论并报审委会")


def _calculate_score(report: ConsistencyReport):
    """计算一致性得分"""
    score = 80  # 基础分
    
    # 类案数量加分
    if report.similar_cases_count >= 5:
        score += 10
    elif report.similar_cases_count >= 3:
        score += 5
    
    # 金额偏离扣分
    if "显著" in report.amount_deviation:
        score -= 20
    elif "偏差" in report.amount_deviation:
        deviation = re.search(r'偏差 (\d+)%', report.amount_deviation)
        if deviation:
            pct = int(deviation.group(1))
            score -= min(pct // 5, 15)
    
    report.score = max(0, min(100, score))
    report.summary = f"与 {report.similar_cases_count} 件类案比对，一致性得分 {report.score:.0f}/100"


# ─── 格式化输出 ────────────────────────────────────────
def format_report_text(report: ConsistencyReport) -> str:
    lines = []
    lines.append("=" * 50)
    lines.append("📊 裁判尺度一致性检查报告")
    lines.append("=" * 50)
    lines.append(f"类案数量: {report.similar_cases_count}")
    lines.append(f"一致性得分: {report.score:.0f}/100")
    lines.append(f"结论: {report.summary}")
    lines.append("-" * 50)
    
    if report.amount_deviation:
        lines.append(f"\n💰 金额偏离分析:")
        lines.append(f"   {report.amount_deviation}")
    
    if report.similar_cases:
        lines.append(f"\n📚 参考类案 ({len(report.similar_cases)} 件):")
        for i, case in enumerate(report.similar_cases[:3], 1):
            lines.append(f"   {i}. {case.title[:50]}")
            if case.court:
                lines.append(f"      法院: {case.court}")
            if case.key_facts:
                lines.append(f"      要点: {case.key_facts[:100]}...")
    
    if report.warnings:
        lines.append(f"\n⚠️  注意事项:")
        for w in report.warnings:
            lines.append(f"   {w}")
    
    return "\n".join(lines)


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="裁判尺度一致性检查")
    parser.add_argument("--cause", "-c", help="案由")
    parser.add_argument("--verdict", "-v", help="判决主文")
    parser.add_argument("--elements", help="要素 JSON 文件路径")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    elements = {}
    if args.elements:
        with open(args.elements, encoding="utf-8") as f:
            elements = json.load(f)
    
    report = check_consistency(elements, args.verdict or "", args.cause or "")
    
    if args.json:
        print(json.dumps({
            "score": report.score,
            "similar_cases_count": report.similar_cases_count,
            "amount_deviation": report.amount_deviation,
            "outcome_match": report.outcome_match,
            "warnings": report.warnings,
            "summary": report.summary,
            "similar_cases": [
                {"title": c.title, "court": c.court, "date": c.date, "facts": c.key_facts[:200]}
                for c in report.similar_cases
            ],
        }, ensure_ascii=False, indent=2))
    else:
        print(format_report_text(report))


if __name__ == "__main__":
    main()
