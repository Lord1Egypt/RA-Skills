#!/usr/bin/env python3
"""
融资诊断8维度评分脚本
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

输入: JSON格式企业数据 (stdin 或 命令行参数)
输出: JSON格式诊断结果

8维度评分体系:
- Traction: 用户/收入增长数据
- Market: 市场规模与验证
- Team: 团队完整度
- Product: 产品成熟度
- Story: 叙事逻辑
- Unit Economics: 单位经济模型
- Use of Funds: 资金使用规划
- Timing: 市场时机

用法:
    python3 funding_diagnosis.py < input.json
    python3 funding_diagnosis.py '{"company": {...}}'
"""

import json
import sys
from typing import Any, Dict, List, Optional


# ============================================================
# 评分常量与基准
# ============================================================

GRADE_THRESHOLDS = [
    (95, "A+", "顶级"),
    (85, "A", "优秀"),
    (78, "A-", "良好"),
    (70, "B+", "中上"),
    (62, "B", "中等"),
    (55, "B-", "中下"),
    (45, "C+", "待补强"),
    (35, "C", "较弱"),
    (25, "C-", "弱"),
    (0,  "D", "不足"),
]

DIMENSION_WEIGHTS = {
    "Traction": 0.18,
    "Market": 0.12,
    "Team": 0.16,
    "Product": 0.14,
    "Story": 0.10,
    "Unit Economics": 0.14,
    "Use of Funds": 0.08,
    "Timing": 0.08,
}

# ============================================================
# 核心评分函数
# ============================================================

def calculate_grade(total_score: int) -> str:
    """根据总分计算等级"""
    for threshold, grade, _ in GRADE_THRESHOLDS:
        if total_score >= threshold:
            return grade
    return "D"


def assess_traction(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Traction 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    mau = data.get("mau", 0)
    revenue = data.get("monthly_revenue", 0)
    growth = data.get("growth_rate", 0)

    if mau > 0:
        if mau >= 100000:
            score += 35
            evidence_parts.append(f"月活{format_number(mau)}，规模领先")
        elif mau >= 50000:
            score += 28
            evidence_parts.append(f"月活{format_number(mau)}，增长良好")
        elif mau >= 10000:
            score += 20
            evidence_parts.append(f"月活{format_number(mau)}，处于增长期")
        elif mau >= 1000:
            score += 12
            evidence_parts.append(f"月活{format_number(mau)}，早期阶段")
        else:
            score += 5
            evidence_parts.append(f"月活{format_number(mau)}，数据积累中")
        benchmark_parts.append("种子轮及格线：月活10k")
    else:
        warnings.append("月活数据缺失")

    if revenue > 0:
        if revenue >= 500000:
            score += 30
            evidence_parts.append(f"月收入¥{format_number(revenue)}")
        elif revenue >= 100000:
            score += 22
            evidence_parts.append(f"月收入¥{format_number(revenue)}")
        elif revenue >= 10000:
            score += 15
            evidence_parts.append(f"月收入¥{format_number(revenue)}")
        else:
            score += 8
            evidence_parts.append(f"月收入¥{format_number(revenue)}")
    else:
        warnings.append("收入数据缺失")

    if growth > 0:
        if growth >= 0.20:
            score += 35
            evidence_parts.append(f"环比增长{growth*100:.0f}%，高速增长")
        elif growth >= 0.10:
            score += 28
            evidence_parts.append(f"环比增长{growth*100:.0f}%，稳定增长")
        elif growth >= 0.05:
            score += 20
            evidence_parts.append(f"环比增长{growth*100:.0f}%，缓慢增长")
        else:
            score += 10
            evidence_parts.append(f"环比增长{growth*100:.0f}%，需加速")
        benchmark_parts.append("健康增长：≥10%/月")
    else:
        warnings.append("增长率数据缺失")

    score = min(score, 100)
    evidence = "；".join(evidence_parts) if evidence_parts else "数据不足"
    benchmark = "；".join(benchmark_parts) if benchmark_parts else "需补充数据"

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Traction",
        "score": score,
        "status": status,
        "evidence": evidence,
        "benchmark": benchmark,
        "warnings": warnings,
    }


def assess_market(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Market 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    tam = data.get("tam", 0)
    sam = data.get("sam", 0)
    market_validation = data.get("market_validation", "")

    if tam > 0:
        if tam >= 10_000_000_000:
            score += 30
            evidence_parts.append(f"TAM ¥{format_number(tam)}，市场空间巨大")
        elif tam >= 1_000_000_000:
            score += 22
            evidence_parts.append(f"TAM ¥{format_number(tam)}，市场空间充足")
        elif tam >= 100_000_000:
            score += 15
            evidence_parts.append(f"TAM ¥{format_number(tam)}，市场空间中等")
        else:
            score += 8
            evidence_parts.append(f"TAM ¥{format_number(tam)}，市场偏小")
        benchmark_parts.append("TAM建议≥10亿")
    else:
        warnings.append("TAM数据缺失")

    if sam > 0:
        if sam >= 1_000_000_000:
            score += 30
            evidence_parts.append(f"SAM ¥{format_number(sam)}，可触达市场大")
        elif sam >= 100_000_000:
            score += 22
            evidence_parts.append(f"SAM ¥{format_number(sam)}，可触达市场中等")
        elif sam >= 10_000_000:
            score += 15
            evidence_parts.append(f"SAM ¥{format_number(sam)}，可触达市场较小")
        else:
            score += 8
            evidence_parts.append(f"SAM ¥{format_number(sam)}")
        benchmark_parts.append("SAM需≥1亿美元(约7亿人民币)")
    else:
        warnings.append("SAM数据缺失")

    if market_validation:
        validation_score = min(len(market_validation) * 5, 30)
        score += validation_score
        evidence_parts.append(f"市场验证：{market_validation[:50]}")
    else:
        score += 10
        evidence_parts.append("市场验证信息不足，建议补充bottom-up分析")

    if data.get("top_down_tam") and not data.get("bottom_up_sam"):
        warnings.append("TAM计算偏乐观，缺乏bottom-up验证")
        score = max(score - 10, 0)

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Market",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def assess_team(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Team 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    team_size = data.get("team_size", 0)
    has_cto = data.get("has_cto", False)
    has_cmo = data.get("has_cmo", False)
    founder_experience = data.get("founder_experience", 0)
    tech_team_ratio = data.get("tech_team_ratio", 0)

    if team_size > 0:
        if team_size >= 10:
            score += 20
            evidence_parts.append(f"团队{team_size}人，初具规模")
        elif team_size >= 5:
            score += 15
            evidence_parts.append(f"团队{team_size}人，核心团队完整")
        elif team_size >= 3:
            score += 10
            evidence_parts.append(f"团队{team_size}人，核心团队初步形成")
        else:
            score += 5
            evidence_parts.append(f"团队{team_size}人，单人/双人团队")
        benchmark_parts.append("种子轮建议3-5人核心团队")
    else:
        warnings.append("团队规模数据缺失")

    if has_cto:
        score += 30
        evidence_parts.append("有CTO/技术负责人")
    else:
        score += 5
        evidence_parts.append("缺CTO，技术风险较高")
        warnings.append("关键短板：缺CTO或技术负责人")
    benchmark_parts.append("种子轮需至少1名技术合伙人")

    if has_cmo:
        score += 15
        evidence_parts.append("有CMO/市场负责人")

    if founder_experience > 0:
        if founder_experience >= 10:
            score += 20
            evidence_parts.append(f"创始人{founder_experience}年行业经验")
        elif founder_experience >= 5:
            score += 15
            evidence_parts.append(f"创始人{founder_experience}年行业经验")
        elif founder_experience >= 2:
            score += 10
            evidence_parts.append(f"创始人{founder_experience}年行业经验")
        else:
            score += 5
            evidence_parts.append(f"创始人{founder_experience}年经验，尚浅")
        benchmark_parts.append("创始人建议≥5年行业经验")
    else:
        score += 5
        evidence_parts.append("创始人经验信息不足")

    if tech_team_ratio > 0:
        if tech_team_ratio >= 0.5:
            score += 15
            evidence_parts.append(f"技术团队占比{tech_team_ratio*100:.0f}%，合理")
        else:
            score += 5
            evidence_parts.append(f"技术团队占比{tech_team_ratio*100:.0f}%，偏低")

    if data.get("has_previous_funding"):
        score += 10
        evidence_parts.append("有融资经验")

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Team",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def assess_product(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Product 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    has_mvp = data.get("has_mvp", False)
    has_pmf = data.get("has_pmf", False)
    paying_users = data.get("paying_users", 0)
    retention_rate = data.get("retention_rate", 0)
    nps_score = data.get("nps_score", 0)

    if has_mvp:
        score += 25
        evidence_parts.append("MVP已验证")
    else:
        score += 5
        evidence_parts.append("MVP尚未完成")
        warnings.append("建议尽快完成MVP开发")
    benchmark_parts.append("需有可用MVP")

    if has_pmf:
        score += 30
        evidence_parts.append("PMF初步确认")
    else:
        score += 10
        evidence_parts.append("PMF尚未确认")
        warnings.append("需验证产品市场匹配")
    benchmark_parts.append("需有付费用户或高留存")

    if paying_users > 0:
        if paying_users >= 100:
            score += 20
            evidence_parts.append(f"付费用户{format_number(paying_users)}，市场验证良好")
        elif paying_users >= 10:
            score += 15
            evidence_parts.append(f"付费用户{format_number(paying_users)}，初步验证")
        else:
            score += 8
            evidence_parts.append(f"付费用户{format_number(paying_users)}，早期阶段")
    else:
        warnings.append("暂无付费用户")

    if retention_rate > 0:
        if retention_rate >= 0.6:
            score += 15
            evidence_parts.append(f"留存率{retention_rate*100:.0f}%，优秀")
        elif retention_rate >= 0.3:
            score += 10
            evidence_parts.append(f"留存率{retention_rate*100:.0f}%，良好")
        else:
            score += 5
            evidence_parts.append(f"留存率{retention_rate*100:.0f}%，需改善")
        benchmark_parts.append("月留存≥30%")
    else:
        warnings.append("留存率数据缺失")

    if nps_score > 0:
        if nps_score >= 50:
            score += 10
            evidence_parts.append(f"NPS {nps_score}，用户推荐意愿强")
        elif nps_score >= 30:
            score += 6
            evidence_parts.append(f"NPS {nps_score}，良好")
        else:
            score += 3
            evidence_parts.append(f"NPS {nps_score}")

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Product",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def assess_story(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Story 维度"""
    score = 0
    evidence_parts = []
    warnings = []

    has_clear_narrative = data.get("has_clear_narrative", False)
    has_emotional_hook = data.get("has_emotional_hook", False)
    has_pitch_deck = data.get("has_pitch_deck", False)
    pitch_deck_quality = data.get("pitch_deck_quality", 0)

    if has_clear_narrative:
        score += 30
        evidence_parts.append("叙事逻辑清晰")
    else:
        score += 10
        evidence_parts.append("叙事逻辑不够清晰")
        warnings.append("需打磨BP故事线")
    evidence_parts.append("投资人3分钟内能理解并记住—目标")

    if has_emotional_hook:
        score += 25
        evidence_parts.append("有情感共鸣点")
    else:
        score += 10
        evidence_parts.append("缺乏情感共鸣，建议强化'为什么是你'")
        warnings.append("缺少情感共鸣要素")

    if has_pitch_deck:
        score += 15
        evidence_parts.append("已有BP/Deck")
        if pitch_deck_quality > 0:
            score += min(pitch_deck_quality, 20)
            evidence_parts.append(f"BP质量评分：{pitch_deck_quality}/20")
    else:
        evidence_parts.append("还未制作BP/Deck")
        warnings.append("建议尽快准备专业BP")

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Story",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "投资人3分钟内能理解并记住",
        "warnings": warnings,
    }


def assess_unit_economics(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Unit Economics 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    ltv = data.get("ltv", 0)
    cac = data.get("cac", 0)
    gross_margin = data.get("gross_margin", 0)

    if ltv > 0 and cac > 0:
        ltv_cac = ltv / cac
        if ltv_cac >= 5:
            score += 35
            evidence_parts.append(f"LTV/CAC = {ltv_cac:.1f}，极优秀")
        elif ltv_cac >= 3:
            score += 28
            evidence_parts.append(f"LTV/CAC = {ltv_cac:.1f}，健康")
        elif ltv_cac >= 1:
            score += 18
            evidence_parts.append(f"LTV/CAC = {ltv_cac:.1f}，需优化")
        else:
            score += 8
            evidence_parts.append(f"LTV/CAC = {ltv_cac:.1f}，不健康")
        benchmark_parts.append("LTV/CAC ≥ 3")
    else:
        warnings.append("LTV或CAC数据缺失")
        score += 15

    if ltv > 0:
        if ltv >= 10000:
            score += 20
            evidence_parts.append(f"LTV ¥{format_number(ltv)}，高价值用户")
        elif ltv >= 1000:
            score += 15
            evidence_parts.append(f"LTV ¥{format_number(ltv)}")
        else:
            score += 8
            evidence_parts.append(f"LTV ¥{format_number(ltv)}，偏低")

    if cac > 0:
        if cac <= 100:
            score += 15
            evidence_parts.append(f"CAC ¥{format_number(cac)}，获客成本低")
        elif cac <= 500:
            score += 10
            evidence_parts.append(f"CAC ¥{format_number(cac)}，获客成本中等")
        else:
            score += 5
            evidence_parts.append(f"CAC ¥{format_number(cac)}，获客成本偏高")

    if gross_margin > 0:
        if gross_margin >= 0.7:
            score += 20
            evidence_parts.append(f"毛利率{gross_margin*100:.0f}%，优秀")
        elif gross_margin >= 0.5:
            score += 15
            evidence_parts.append(f"毛利率{gross_margin*100:.0f}%，良好")
        elif gross_margin >= 0.3:
            score += 10
            evidence_parts.append(f"毛利率{gross_margin*100:.0f}%，一般")
        else:
            score += 5
            evidence_parts.append(f"毛利率{gross_margin*100:.0f}%，偏低")
        benchmark_parts.append("毛利率建议≥50%")
    else:
        warnings.append("毛利率数据缺失")

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Unit Economics",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def assess_use_of_funds(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Use of Funds 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    funding_amount = data.get("funding_amount", 0)
    has_detailed_plan = data.get("has_detailed_plan", False)
    runway_months = data.get("runway_months", 0)
    allocation_detail = data.get("allocation_detail", "")

    if funding_amount > 0:
        if funding_amount >= 5_000_000:
            score += 15
            evidence_parts.append(f"计划融资¥{format_number(funding_amount)}")
        elif funding_amount >= 1_000_000:
            score += 10
            evidence_parts.append(f"计划融资¥{format_number(funding_amount)}")
        else:
            score += 5
            evidence_parts.append(f"计划融资¥{format_number(funding_amount)}")
    else:
        warnings.append("融资额未明确")

    if has_detailed_plan:
        score += 30
        evidence_parts.append("资金用途有详细分配方案")
    else:
        score += 8
        evidence_parts.append("资金用途分配不够具体")
        warnings.append("需制定详细的资金使用计划")

    if allocation_detail:
        score += 20
        evidence_parts.append(f"分配明细：{allocation_detail[:50]}")

    if runway_months > 0:
        if runway_months >= 18:
            score += 20
            evidence_parts.append(f"{runway_months}个月runway，充裕")
        elif runway_months >= 12:
            score += 15
            evidence_parts.append(f"{runway_months}个月runway，达标")
        elif runway_months >= 6:
            score += 8
            evidence_parts.append(f"{runway_months}个月runway，偏紧")
        else:
            score += 3
            evidence_parts.append(f"{runway_months}个月runway，危险")
        benchmark_parts.append("18个月 runway，分季度拆解")
    else:
        warnings.append("runway数据缺失")
        score += 10

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Use of Funds",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def assess_timing(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估 Timing 维度"""
    score = 0
    evidence_parts = []
    benchmark_parts = []
    warnings = []

    sector = data.get("sector", "")
    market_education_cost = data.get("market_education_cost", "")
    competitor_count = data.get("competitor_count", 0)
    market_trend = data.get("market_trend", "")

    if sector:
        early_stage_sectors = ["AI", "智能体", "大模型", "AIGC", "出海", "跨境电商", "短剧", "web3"]
        is_early = any(kw in sector for kw in early_stage_sectors)
        if is_early:
            score += 30
            evidence_parts.append(f"{sector}赛道处于早期爆发期")
        else:
            score += 20
            evidence_parts.append(f"{sector}赛道处于成长期")
        benchmark_parts.append("市场教育成本下降，需求上升")
    else:
        warnings.append("赛道信息缺失")
        score += 15

    if market_education_cost:
        if "低" in market_education_cost or "下降" in market_education_cost:
            score += 20
            evidence_parts.append("市场教育成本低/下降")
        else:
            score += 10
            evidence_parts.append(f"市场教育成本：{market_education_cost}")
    else:
        score += 10

    if competitor_count > 0:
        if competitor_count <= 5:
            score += 20
            evidence_parts.append(f"竞争对手{competitor_count}家，竞争格局清晰")
        elif competitor_count <= 20:
            score += 15
            evidence_parts.append(f"竞争对手{competitor_count}家，中等竞争")
        else:
            score += 8
            evidence_parts.append(f"竞争对手{competitor_count}家，竞争激烈")
    else:
        score += 10

    if market_trend:
        score += 20
        evidence_parts.append(f"市场趋势：{market_trend[:50]}")

    score = min(score, 100)

    status = "healthy" if score >= 60 else ("warning" if score >= 40 else "critical")

    return {
        "name": "Timing",
        "score": score,
        "status": status,
        "evidence": "；".join(evidence_parts),
        "benchmark": "；".join(benchmark_parts),
        "warnings": warnings,
    }


def format_number(num: float) -> str:
    """格式化数字为中文单位"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}亿"
    elif num >= 10_000:
        return f"{num/10_000:.1f}万"
    else:
        return f"{num:.0f}"


# ============================================================
# 主诊断函数
# ============================================================

def run_diagnosis(data: Dict[str, Any]) -> Dict[str, Any]:
    """执行完整融资诊断"""
    
    # 逐维度评估
    dimensions = [
        assess_traction(data),
        assess_market(data),
        assess_team(data),
        assess_product(data),
        assess_story(data),
        assess_unit_economics(data),
        assess_use_of_funds(data),
        assess_timing(data),
    ]

    # 计算加权总分
    total_score = 0
    for dim in dimensions:
        weight = DIMENSION_WEIGHTS.get(dim["name"], 0.125)
        total_score += dim["score"] * weight
    total_score = round(total_score)

    # 计算等级
    grade = calculate_grade(total_score)

    # 生成总结
    if total_score >= 80:
        summary = "融资准备度良好，可以启动融资"
    elif total_score >= 60:
        summary = "建议补强短板后启动融资"
    elif total_score >= 40:
        summary = "需要重点补强，暂时不建议启动融资"
    else:
        summary = "融资准备度不足，建议先专注产品和增长"

    # 识别短板（按影响排序）
    weaknesses = []
    for dim in sorted(dimensions, key=lambda d: d["score"]):
        if dim["score"] < 60:
            for w in dim.get("warnings", []) or []:
                if len(weaknesses) < 5:
                    weaknesses.append({
                        "dimension": dim["name"],
                        "issue": w,
                        "impact": "critical" if dim["score"] < 40 else ("high" if dim["score"] < 50 else "medium"),
                    })
            if not dim.get("warnings") and len(weaknesses) < 5:
                weaknesses.append({
                    "dimension": dim["name"],
                    "issue": f"{dim['name']}评分偏低({dim['score']}/100)",
                    "impact": "high" if dim["score"] < 40 else "medium",
                })

    # 生成建议
    suggestions = {
        "short_term": {
            "timeframe": "本周",
            "tasks": _generate_short_term_tasks(weaknesses, dimensions),
        },
        "medium_term": {
            "timeframe": "本月",
            "tasks": _generate_medium_term_tasks(weaknesses, dimensions),
        },
        "long_term": {
            "timeframe": "本季度",
            "tasks": _generate_long_term_tasks(weaknesses, dimensions),
        },
    }

    # Capital EQ 情绪提示
    capital_eq_note = ""
    anxiety_score = data.get("anxiety_level", 0)
    if anxiety_score >= 7:
        capital_eq_note = "创始人当前焦虑指数偏高，建议先做CEQ干预"
    elif anxiety_score >= 4:
        capital_eq_note = "创始人有一定焦虑，建议关注融资情绪管理"

    return {
        "version": "3.0.0",
        "module": "funding_diagnosis",
        "score": {
            "total": total_score,
            "max": 100,
            "grade": grade,
        },
        "summary": summary,
        "dimensions": dimensions,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "capital_eq_note": capital_eq_note,
    }


def _generate_short_term_tasks(weaknesses: List[Dict], dimensions: List[Dict]) -> List[str]:
    """生成短期建议"""
    tasks = []
    for w in weaknesses[:3]:
        dim_name = w["dimension"]
        if "CTO" in w["issue"] or "技术" in w["issue"]:
            tasks.append("招聘CTO或联合创始人")
        elif "TAM" in w["issue"] or "Market" in dim_name:
            tasks.append("整理TAM bottom-up验证数据")
        elif "BP" in w["issue"] or "Deck" in w["issue"] or "叙事" in w["issue"]:
            tasks.append("打磨BP故事线，强化情感共鸣")
        elif "资金" in w["issue"] or "Use of Funds" in dim_name:
            tasks.append("制定详细的资金使用分配表")
        elif "MVP" in w["issue"] or "PMF" in w["issue"]:
            tasks.append("加速产品迭代，验证PMF")
        elif "留存" in w["issue"]:
            tasks.append("分析用户流失原因，改善留存")
    if not tasks:
        tasks.append("整理最新经营数据，准备融资材料")
    return tasks[:3]


def _generate_medium_term_tasks(weaknesses: List[Dict], dimensions: List[Dict]) -> List[str]:
    """生成中期建议"""
    tasks = []
    for dim in dimensions:
        if dim["name"] == "Traction" and dim["score"] < 70:
            tasks.append("冲刺关键数据里程碑")
            break
    if not tasks:
        tasks.append("完善融资材料包（BP+财务模型+数据包）")
    tasks.append("建立投资人关系清单（50-100家）")
    return tasks[:2]


def _generate_long_term_tasks(weaknesses: List[Dict], dimensions: List[Dict]) -> List[str]:
    """生成长期建议"""
    return ["启动融资路演", "持续优化产品数据"]


# ============================================================
# 入口
# ============================================================

def main():
    if len(sys.argv) > 1:
        input_data = json.loads(sys.argv[1])
    else:
        input_data = json.load(sys.stdin)

    result = run_diagnosis(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()