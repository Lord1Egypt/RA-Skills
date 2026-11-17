#!/usr/bin/env python3
"""
sentencing_calculator.py — 量刑建议计算器

根据犯罪情节自动计算量刑建议区间：
输入：罪名 + 从重/从轻情节 + 地区量刑指导意见
输出：建议刑期区间 + 罚金区间 + 计算依据

用法：
    from sentencing_calculator import calculate_sentence
    result = calculate_sentence("故意伤害罪", base_injury="重伤", mitigating=["自首"])
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SentencingFactor:
    name: str                   # 情节名称
    type: str                   # 类型：mitigating(从轻)/aggravating(从重)
    impact: str                 # 影响描述
    reduction_pct: float        # 减少/增加比例（负数=减少）


@dataclass
class SentencingResult:
    crime: str                  # 罪名
    base_range: str             # 基准刑期区间
    adjusted_range: str         # 调整后刑期区间
    fine_range: str             # 罚金区间
    factors: list               # 量刑情节列表
    calculation_basis: str      # 计算依据
    risk_notes: list            # 风险提示


# ─── 常见罪名基准刑期 ─────────────────────────────────
CRIME_BASE_SENTENCES = {
    "故意伤害罪": {
        "轻伤": {"base": "6个月-2年", "fine": "0-5000元"},
        "重伤": {"base": "3-10年", "fine": "0-50000元"},
        "死亡": {"base": "10年以上-无期", "fine": "0-100000元"},
    },
    "盗窃罪": {
        "数额较大": {"base": "3年以下", "fine": "1000-10000元"},
        "数额巨大": {"base": "3-10年", "fine": "10000-100000元"},
        "数额特别巨大": {"base": "10年以上-无期", "fine": "100000元以上"},
    },
    "诈骗罪": {
        "数额较大": {"base": "3年以下", "fine": "2000-20000元"},
        "数额巨大": {"base": "3-10年", "fine": "20000-200000元"},
        "数额特别巨大": {"base": "10年以上-无期", "fine": "200000元以上"},
    },
    "危险驾驶罪": {
        "醉驾": {"base": "1-6个月拘役", "fine": "1000-5000元"},
    },
    "交通肇事罪": {
        "一般": {"base": "3年以下", "fine": "0-50000元"},
        "逃逸": {"base": "3-7年", "fine": "0-100000元"},
        "逃逸致死": {"base": "7年以上", "fine": "0-200000元"},
    },
    "抢劫罪": {
        "一般": {"base": "3-10年", "fine": "0-50000元"},
        "加重": {"base": "10年以上-无期/死刑", "fine": "0-100000元"},
    },
    "故意杀人罪": {
        "一般": {"base": "10年以上-无期", "fine": "0-100000元"},
        "情节较轻": {"base": "3-10年", "fine": "0-50000元"},
    },
    "贩卖毒品罪": {
        "少量": {"base": "3年以下", "fine": "0-10000元"},
        "较大": {"base": "3-7年", "fine": "0-50000元"},
        "大量": {"base": "15年-无期/死刑", "fine": "0-200000元"},
    },
    "帮信罪": {
        "一般": {"base": "3年以下", "fine": "0-50000元"},
    },
    "贪污罪": {
        "数额较大": {"base": "3年以下", "fine": "0-200000元"},
        "数额巨大": {"base": "3-10年", "fine": "0-500000元"},
        "数额特别巨大": {"base": "10年以上-无期", "fine": "0-1000000元"},
    },
    "受贿罪": {
        "数额较大": {"base": "3年以下", "fine": "0-200000元"},
        "数额巨大": {"base": "3-10年", "fine": "0-500000元"},
        "数额特别巨大": {"base": "10年以上-无期", "fine": "0-1000000元"},
    },
}


# ─── 量刑情节影响比例 ─────────────────────────────────
SENTENCING_FACTORS = {
    # 从轻/减轻情节
    "自首": {"type": "mitigating", "reduction": 0.2, "desc": "可以从轻或减轻处罚"},
    "坦白": {"type": "mitigating", "reduction": 0.1, "desc": "可以从轻处罚"},
    "立功": {"type": "mitigating", "reduction": 0.2, "desc": "可以从轻或减轻处罚"},
    "重大立功": {"type": "mitigating", "reduction": 0.3, "desc": "可以减轻或免除处罚"},
    "从犯": {"type": "mitigating", "reduction": 0.3, "desc": "应当从轻、减轻或免除处罚"},
    "未遂": {"type": "mitigating", "reduction": 0.2, "desc": "可以比照既遂从轻或减轻"},
    "中止": {"type": "mitigating", "reduction": 0.4, "desc": "应当减轻或免除处罚"},
    "初犯": {"type": "mitigating", "reduction": 0.05, "desc": "酌定从轻"},
    "认罪认罚": {"type": "mitigating", "reduction": 0.15, "desc": "可以从宽处理"},
    "退赃退赔": {"type": "mitigating", "reduction": 0.1, "desc": "酌定从轻"},
    "取得谅解": {"type": "mitigating", "reduction": 0.1, "desc": "酌定从轻"},
    "未成年人": {"type": "mitigating", "reduction": 0.3, "desc": "应当从轻或减轻处罚"},
    "75岁以上": {"type": "mitigating", "reduction": 0.2, "desc": "可以从轻或减轻处罚"},
    
    # 从重情节
    "累犯": {"type": "aggravating", "reduction": 0.2, "desc": "应当从重处罚"},
    "主犯": {"type": "aggravating", "reduction": 0.1, "desc": "应当按照其所参与的全部犯罪处罚"},
    "教唆犯": {"type": "aggravating", "reduction": 0.1, "desc": "应当按照其教唆的犯罪处罚"},
    "手段残忍": {"type": "aggravating", "reduction": 0.15, "desc": "酌定从重"},
    "后果严重": {"type": "aggravating", "reduction": 0.15, "desc": "酌定从重"},
    "拒不认罪": {"type": "aggravating", "reduction": 0.1, "desc": "酌定从重"},
    "前科": {"type": "aggravating", "reduction": 0.1, "desc": "酌定从重"},
    "涉黑涉恶": {"type": "aggravating", "reduction": 0.2, "desc": "依法从严惩处"},
}


def calculate_sentence(
    crime: str,
    severity: str = "一般",
    mitigating: list = None,
    aggravating: list = None,
) -> SentencingResult:
    """
    计算量刑建议。
    
    Args:
        crime: 罪名
        severity: 严重程度（如"轻伤"/"重伤"/"数额较大"等）
        mitigating: 从轻情节列表
        aggravating: 从重情节列表
    
    Returns:
        SentencingResult 包含量刑区间和计算依据
    """
    if mitigating is None:
        mitigating = []
    if aggravating is None:
        aggravating = []
    
    # 获取基准刑期
    crime_data = CRIME_BASE_SENTENCES.get(crime, {})
    if severity in crime_data:
        base = crime_data[severity]
    elif "一般" in crime_data:
        base = crime_data["一般"]
    elif crime_data:
        base = list(crime_data.values())[0]
    else:
        base = {"base": "需根据具体情节确定", "fine": "需根据具体情节确定"}
    
    # 收集量刑情节
    factors = []
    total_reduction = 0.0
    
    for m in mitigating:
        if m in SENTENCING_FACTORS:
            factor_data = SENTENCING_FACTORS[m]
            factors.append(SentencingFactor(
                name=m,
                type="mitigating",
                impact=factor_data["desc"],
                reduction_pct=-factor_data["reduction"],
            ))
            total_reduction -= factor_data["reduction"]
        else:
            factors.append(SentencingFactor(
                name=m,
                type="mitigating",
                impact="酌定从轻情节",
                reduction_pct=-0.05,
            ))
            total_reduction -= 0.05
    
    for a in aggravating:
        if a in SENTENCING_FACTORS:
            factor_data = SENTENCING_FACTORS[a]
            factors.append(SentencingFactor(
                name=a,
                type="aggravating",
                impact=factor_data["desc"],
                reduction_pct=factor_data["reduction"],
            ))
            total_reduction += factor_data["reduction"]
        else:
            factors.append(SentencingFactor(
                name=a,
                type="aggravating",
                impact="酌定从重情节",
                reduction_pct=0.05,
            ))
            total_reduction += 0.05
    
    # 构建计算依据
    basis_parts = [f"基准刑期：{base['base']}"]
    for f in factors:
        direction = "从轻" if f.type == "mitigating" else "从重"
        basis_parts.append(f"{f.name}（{direction}，{f.impact}）")
    calculation_basis = "；".join(basis_parts)
    
    # 风险提示
    risk_notes = []
    if total_reduction < -0.3:
        risk_notes.append("多个从轻情节叠加，建议在法定刑以下量刑需报请最高法核准")
    if total_reduction > 0.3:
        risk_notes.append("多个从重情节叠加，注意不超过法定刑上限")
    if "自首" in mitigating and "立功" in mitigating:
        risk_notes.append("自首+立功同时具备，可较大幅度从轻")
    if "认罪认罚" in mitigating:
        risk_notes.append("认罪认罚案件，建议适用速裁程序或简易程序")
    
    # 根据量刑情节计算调整后的刑期
    adjusted = _adjust_sentence_range(base["base"], total_reduction)
    
    return SentencingResult(
        crime=crime,
        base_range=base["base"],
        adjusted_range=adjusted,
        fine_range=base["fine"],
        factors=[asdict(f) for f in factors],
        calculation_basis=calculation_basis,
        risk_notes=risk_notes,
    )


def _adjust_sentence_range(base_range: str, reduction_pct: float) -> str:
    """根据总调整比例调整刑期区间"""
    import re
    
    # 解析基准刑期: "3-10年", "6个月-2年", "3年以下", "10年以上-无期"
    months_pattern = r'(\d+)个月'
    year_pattern = r'(\d+)年'
    
    parts = base_range.split('-')
    if len(parts) != 2:
        return base_range  # 无法解析时返回原值
    
    low_str, high_str = parts[0].strip(), parts[1].strip()
    
    # 转换为月数
    def to_months(s: str) -> int:
        total = 0
        m = re.search(months_pattern, s)
        y = re.search(year_pattern, s)
        if y:
            total += int(y.group(1)) * 12
        if m:
            total += int(m.group(1))
        return total if total > 0 else 0
    
    low = to_months(low_str)
    high = to_months(high_str)
    
    if low == 0 and high == 0:
        return base_range  # 无法解析
    if high == 0:
        high = low  # 单点
    if high <= low:
        high = low + 1
    
    # 应用调整
    low_adj = max(1, int(low * (1 - reduction_pct)))
    high_adj = max(low_adj + 1, int(high * (1 - reduction_pct)))
    
    # 格式化输出
    def fmt(m: int) -> str:
        years = m // 12
        months = m % 12
        if years > 0 and months > 0:
            return f"{years}年{months}个月"
        elif years > 0:
            return f"{years}年"
        else:
            return f"{months}个月"
    
    return f"{fmt(low_adj)}-{fmt(high_adj)}"


def format_sentencing_report(result: SentencingResult) -> str:
    """格式化量刑建议报告"""
    lines = []
    lines.append("## 量刑建议计算")
    lines.append(f"**罪名**：{result.crime}")
    lines.append(f"**基准刑期**：{result.base_range}")
    lines.append(f"**建议刑期**：{result.adjusted_range}")
    lines.append(f"**罚金区间**：{result.fine_range}")
    lines.append("")
    
    if result.factors:
        lines.append("### 量刑情节")
        for f in result.factors:
            icon = "🔽" if f["type"] == "mitigating" else "🔺"
            lines.append(f"- {icon} **{f['name']}**：{f['impact']}")
        lines.append("")
    
    lines.append(f"**计算依据**：{result.calculation_basis}")
    lines.append("")
    
    if result.risk_notes:
        lines.append("### ⚠️ 风险提示")
        for note in result.risk_notes:
            lines.append(f"- {note}")
    
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 sentencing_calculator.py <罪名> [严重程度] [--mitigating 情节1 情节2] [--aggravating 情节1]")
        print("示例: python3 sentencing_calculator.py 故意伤害罪 重伤 --mitigating 自首 认罪认罚")
        sys.exit(1)
    
    crime = sys.argv[1]
    severity = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "一般"
    
    mitigating = []
    aggravating = []
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--mitigating":
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith("--"):
                mitigating.append(sys.argv[i])
                i += 1
        elif sys.argv[i] == "--aggravating":
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith("--"):
                aggravating.append(sys.argv[i])
                i += 1
        else:
            i += 1
    
    result = calculate_sentence(crime, severity, mitigating, aggravating)
    print(format_sentencing_report(result))
