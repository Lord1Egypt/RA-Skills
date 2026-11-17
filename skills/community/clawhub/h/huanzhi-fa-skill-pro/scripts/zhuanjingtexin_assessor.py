#!/usr/bin/env python3
"""
专精特新资质评估脚本
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

输入: 企业基本信息JSON
输出: 差距分析+申报路径JSON

专精特新晋升阶梯:
  创新型中小企业 → 专精特新中小企业 → 专精特新「小巨人」 → 国家重点「小巨人」

用法:
    python3 zhuanjingtexin_assessor.py < input.json
    python3 zhuanjingtexin_assessor.py '{"company_name": "XXX科技", "revenue_last_year": 2000000, ...}'
"""

import json
import sys
from typing import Any, Dict, List, Optional


# ============================================================
# 创新型中小企业评价标准
# ============================================================

INNOVATIVE_SME_METRICS = {
    "innovation_capacity": {
        "rd_ratio": {"weight": 10, "threshold": 0.03, "description": "研发投入占比≥3%"},
        "rd_personnel_ratio": {"weight": 5, "threshold": 0.10, "description": "研发人员占比≥10%"},
        "ip_count": {"weight": 10, "threshold": 1, "description": "知识产权数量≥1项"},
        "standard_participation": {"weight": 10, "threshold": 1, "description": "参与标准制定"},
    },
    "growth": {
        "revenue_growth": {"weight": 15, "threshold": 0.10, "description": "主营收入增长率≥10%"},
        "profit_growth": {"weight": 10, "threshold": 0.05, "description": "净利润增长率≥5%"},
    },
    "specialization": {
        "revenue_ratio": {"weight": 10, "threshold": 0.70, "description": "主营业务收入占比≥70%"},
    },
    "bonus": {
        "quality_cert": {"weight": 3, "description": "质量管理体系认证"},
        "cloud_adoption": {"weight": 3, "description": "核心业务系统上云"},
        "ai_application": {"weight": 3, "description": "AI应用场景"},
    },
    "passing_score": 60,
    "max_score": 100,
}


# ============================================================
# 专精特新中小企业认定标准
# ============================================================

SPECIALIZED_SME_REQUIREMENTS = {
    "basic_conditions": {
        "min_years_in_segment": 2,
        "min_rd_expense": 1000000,
        "min_rd_ratio": 0.03,
        "min_revenue": 10000000,
        "min_equity_funding": 20000000,
    },
    "passing_score": 60,
    "max_score": 100,
}


# ============================================================
# 小巨人认定标准
# ============================================================

LITTLE_GIANT_REQUIREMENTS = {
    "basic_conditions": {
        "min_years_in_segment": 3,
        "min_revenue_ratio": 0.70,
        "min_revenue_growth": 0.05,
        "min_rd_ratio_high": 0.03,  # 营收≥1亿
        "min_rd_ratio_mid": 0.06,   # 营收5000万-1亿
        "min_rd_ratio_low": 0.06,   # 营收<5000万
        "min_rd_expense_low": 30000000,
        "min_class_i_ip": 2,
        "min_revenue": 100000000,
        "min_equity_funding": 60000000,
    },
}


# ============================================================
# 评估函数
# ============================================================

def assess_innovative_sme(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估创新型中小企业"""
    score = 0
    gap_analysis = []
    details = []

    # 创新能力
    rd_ratio = data.get("rd_ratio", 0)
    if rd_ratio >= 0.03:
        score += 10
        details.append({"indicator": "研发投入占比", "current": f"{rd_ratio*100:.1f}%", "required": "≥3%", "status": "pass"})
    else:
        details.append({"indicator": "研发投入占比", "current": f"{rd_ratio*100:.1f}%", "required": "≥3%", "status": "fail"})
        gap_analysis.append({"indicator": "研发投入占比", "priority": 2})

    rd_personnel = data.get("rd_personnel_ratio", 0)
    if rd_personnel >= 0.10:
        score += 5
        details.append({"indicator": "研发人员占比", "current": f"{rd_personnel*100:.1f}%", "required": "≥10%", "status": "pass"})
    else:
        details.append({"indicator": "研发人员占比", "current": f"{rd_personnel*100:.1f}%", "required": "≥10%", "status": "fail"})
        gap_analysis.append({"indicator": "研发人员占比", "priority": 3})

    ip_count = data.get("patents_invention", 0) + data.get("patents_utility", 0) + data.get("software_copyrights", 0)
    if ip_count >= 1:
        score += 10
        details.append({"indicator": "知识产权数量", "current": f"{ip_count}项", "required": "≥1项", "status": "pass"})
    else:
        details.append({"indicator": "知识产权数量", "current": f"{ip_count}项", "required": "≥1项", "status": "fail"})
        gap_analysis.append({"indicator": "知识产权数量", "priority": 1})

    # 成长性
    revenue_growth = data.get("revenue_growth", 0)
    if revenue_growth >= 0.10:
        score += 15
        details.append({"indicator": "主营收入增长率", "current": f"{revenue_growth*100:.1f}%", "required": "≥10%", "status": "pass"})
    else:
        details.append({"indicator": "主营收入增长率", "current": f"{revenue_growth*100:.1f}%", "required": "≥10%", "status": "fail"})
        gap_analysis.append({"indicator": "主营收入增长率", "priority": 2})

    profit_growth = data.get("profit_growth", 0)
    if profit_growth >= 0.05:
        score += 10
        details.append({"indicator": "净利润增长率", "current": f"{profit_growth*100:.1f}%", "required": "≥5%", "status": "pass"})
    else:
        details.append({"indicator": "净利润增长率", "current": f"{profit_growth*100:.1f}%", "required": "≥5%", "status": "fail"})
        gap_analysis.append({"indicator": "净利润增长率", "priority": 3})

    # 专业化
    revenue_ratio = data.get("main_business_revenue_ratio", 0)
    if revenue_ratio >= 0.70:
        score += 10
        details.append({"indicator": "主营业务收入占比", "current": f"{revenue_ratio*100:.1f}%", "required": "≥70%", "status": "pass"})
    else:
        details.append({"indicator": "主营业务收入占比", "current": f"{revenue_ratio*100:.1f}%", "required": "≥70%", "status": "fail"})
        gap_analysis.append({"indicator": "主营业务收入占比", "priority": 3})

    # 加分项
    if data.get("has_quality_cert"):
        score += 3
    if data.get("has_cloud_adoption"):
        score += 3
    if data.get("has_ai_application"):
        score += 3

    # 排序差距
    gap_analysis.sort(key=lambda x: x["priority"])

    return {
        "tier": "innovative_sme",
        "tier_name": "创新型中小企业",
        "score": min(score, 100),
        "max_score": 100,
        "passing_score": 60,
        "achievable": score >= 60,
        "details": details,
        "gaps": gap_analysis,
    }


def assess_specialized_sme(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估专精特新中小企业"""
    gaps = []
    details = []

    # 基本条件检查
    years_in_segment = data.get("years_in_segment", 0)
    if years_in_segment >= 2:
        details.append({"indicator": "细分市场年限", "current": f"{years_in_segment}年", "required": "≥2年", "status": "pass"})
    else:
        details.append({"indicator": "细分市场年限", "current": f"{years_in_segment}年", "required": "≥2年", "status": "fail"})
        gaps.append({"indicator": "细分市场年限", "priority": 3})

    rd_expense = data.get("rd_expense", 0)
    if rd_expense >= 1000000:
        details.append({"indicator": "研发费用总额", "current": f"¥{rd_expense:,.0f}", "required": "≥100万", "status": "pass"})
    else:
        details.append({"indicator": "研发费用总额", "current": f"¥{rd_expense:,.0f}", "required": "≥100万", "status": "fail"})
        gaps.append({"indicator": "研发费用总额", "priority": 2})

    rd_ratio = data.get("rd_ratio", 0)
    if rd_ratio >= 0.03:
        details.append({"indicator": "研发投入占比", "current": f"{rd_ratio*100:.1f}%", "required": "≥3%", "status": "pass"})
    else:
        details.append({"indicator": "研发投入占比", "current": f"{rd_ratio*100:.1f}%", "required": "≥3%", "status": "fail"})
        gaps.append({"indicator": "研发投入占比", "priority": 2})

    revenue = data.get("revenue_last_year", 0)
    if revenue >= 10000000:
        details.append({"indicator": "上年度营收", "current": f"¥{revenue:,.0f}", "required": "≥1000万", "status": "pass"})
    else:
        details.append({"indicator": "上年度营收", "current": f"¥{revenue:,.0f}", "required": "≥1000万", "status": "fail"})
        gaps.append({"indicator": "上年度营收", "priority": 1})

    ip_count = data.get("patents_invention", 0)
    utility_count = data.get("patents_utility", 0)
    if ip_count >= 1 or utility_count >= 2:
        details.append({"indicator": "知识产权", "current": f"发明专利{ip_count}项，实用新型{utility_count}项", "required": "≥1项发明或≥2项实用新型", "status": "pass"})
    else:
        details.append({"indicator": "知识产权", "current": f"发明专利{ip_count}项，实用新型{utility_count}项", "required": "≥1项发明或≥2项实用新型", "status": "fail"})
        gaps.append({"indicator": "知识产权数量不足", "priority": 1})

    gaps.sort(key=lambda x: x["priority"])

    # 简单评分（基于达标比例）
    pass_count = sum(1 for d in details if d["status"] == "pass")
    score = int((pass_count / len(details)) * 100) if details else 0

    return {
        "tier": "specialized_sme",
        "tier_name": "专精特新中小企业",
        "score": score,
        "max_score": 100,
        "passing_score": 60,
        "achievable": score >= 60 and len(gaps) <= 1,
        "details": details,
        "gaps": gaps,
    }


def assess_little_giant(data: Dict[str, Any]) -> Dict[str, Any]:
    """评估专精特新小巨人"""
    gaps = []
    details = []

    years_in_segment = data.get("years_in_segment", 0)
    if years_in_segment >= 3:
        details.append({"indicator": "细分市场年限", "current": f"{years_in_segment}年", "required": "≥3年", "status": "pass"})
    else:
        details.append({"indicator": "细分市场年限", "current": f"{years_in_segment}年", "required": "≥3年", "status": "fail"})
        gaps.append({"indicator": "细分市场年限", "priority": 3})

    revenue_ratio = data.get("main_business_revenue_ratio", 0)
    if revenue_ratio >= 0.70:
        details.append({"indicator": "主营业务收入占比", "current": f"{revenue_ratio*100:.1f}%", "required": "≥70%", "status": "pass"})
    else:
        details.append({"indicator": "主营业务收入占比", "current": f"{revenue_ratio*100:.1f}%", "required": "≥70%", "status": "fail"})
        gaps.append({"indicator": "主营业务收入占比", "priority": 3})

    revenue = data.get("revenue_last_year", 0)
    if revenue >= 100000000:
        details.append({"indicator": "上年度营收", "current": f"¥{revenue:,.0f}", "required": "≥1亿", "status": "pass"})
    else:
        details.append({"indicator": "上年度营收", "current": f"¥{revenue:,.0f}", "required": "≥1亿", "status": "fail"})
        gaps.append({"indicator": "上年度营收", "priority": 1})

    ip_count = data.get("patents_invention", 0)
    if ip_count >= 2:
        details.append({"indicator": "Ⅰ类知识产权", "current": f"{ip_count}项", "required": "≥2项发明专利", "status": "pass"})
    else:
        details.append({"indicator": "Ⅰ类知识产权", "current": f"{ip_count}项", "required": "≥2项发明专利", "status": "fail"})
        gaps.append({"indicator": "Ⅰ类知识产权数量不足", "priority": 1})

    revenue_growth = data.get("revenue_growth", 0)
    if revenue_growth >= 0.05:
        details.append({"indicator": "近2年营收增长率", "current": f"{revenue_growth*100:.1f}%", "required": "≥5%", "status": "pass"})
    else:
        details.append({"indicator": "近2年营收增长率", "current": f"{revenue_growth*100:.1f}%", "required": "≥5%", "status": "fail"})
        gaps.append({"indicator": "营收增长率", "priority": 2})

    gaps.sort(key=lambda x: x["priority"])

    pass_count = sum(1 for d in details if d["status"] == "pass")
    score = int((pass_count / len(details)) * 100) if details else 0

    return {
        "tier": "little_giant",
        "tier_name": "专精特新「小巨人」",
        "score": score,
        "max_score": 100,
        "passing_score": 70,
        "achievable": score >= 70 and len(gaps) <= 1,
        "details": details,
        "gaps": gaps,
    }


# ============================================================
# 主评估函数
# ============================================================

def run_assessment(data: Dict[str, Any]) -> Dict[str, Any]:
    """执行完整专精特新资质评估"""

    innovative = assess_innovative_sme(data)
    specialized = assess_specialized_sme(data)
    little_giant = assess_little_giant(data)

    # 确定当前层级和下一层级
    current_tier = "none"
    next_tier = "innovative_sme"
    next_tier_name = "创新型中小企业"

    if little_giant["achievable"]:
        current_tier = "little_giant"
        next_tier = "little_giant"
        next_tier_name = "专精特新「小巨人」"
    elif specialized["achievable"]:
        current_tier = "specialized_sme"
        next_tier = "little_giant"
        next_tier_name = "专精特新「小巨人」"
    elif innovative["achievable"]:
        current_tier = "innovative_sme"
        next_tier = "specialized_sme"
        next_tier_name = "专精特新中小企业"

    # 生成路线图
    roadmap = generate_roadmap(current_tier, next_tier, data)

    # 生成材料清单
    document_checklist = generate_document_checklist(current_tier, data)

    # 下一层级展望
    next_tiers = []
    if current_tier in ("none", "innovative_sme"):
        next_tiers.append({
            "tier": "specialized_sme",
            "tier_name": "专精特新中小企业",
            "achievable_in": "12-18个月",
            "key_gaps": ["营收需达1000万", "需1项Ⅰ类知识产权", "需2年细分市场经验"],
        })
    if current_tier in ("none", "innovative_sme", "specialized_sme"):
        next_tiers.append({
            "tier": "little_giant",
            "tier_name": "专精特新「小巨人」",
            "achievable_in": "24-36个月",
            "key_gaps": ["营收需达1亿", "需2项Ⅰ类知识产权", "需全国市场占有率≥10%"],
        })

    return {
        "version": "3.0.0",
        "module": "zhuanjingtexin_assessment",
        "user_profile": {
            "company_name": data.get("company_name", ""),
            "establishment_date": data.get("establishment_date", ""),
            "sector": data.get("sector", ""),
            "revenue_last_year": data.get("revenue_last_year", 0),
            "revenue_growth": data.get("revenue_growth", 0),
            "rd_expense": data.get("rd_expense", 0),
            "rd_ratio": data.get("rd_ratio", 0),
            "employees": data.get("employees", 0),
            "rd_employees": data.get("rd_employees", 0),
            "patents_invention": data.get("patents_invention", 0),
            "patents_utility": data.get("patents_utility", 0),
            "software_copyrights": data.get("software_copyrights", 0),
            "years_in_segment": data.get("years_in_segment", 0),
        },
        "assessment": {
            "current_tier": current_tier,
            "next_tier": next_tier,
            "next_tier_name": next_tier_name,
            "innovative_sme": innovative,
            "specialized_sme": specialized,
            "little_giant": little_giant,
        },
        "roadmap": roadmap,
        "next_tiers": next_tiers,
        "document_checklist": document_checklist,
    }


def generate_roadmap(current_tier: str, target_tier: str, data: Dict) -> Dict:
    """生成申报路线图"""
    if current_tier == "little_giant" or target_tier == "little_giant":
        return {
            "target_tier": target_tier,
            "estimated_timeline": "6-12个月",
            "milestones": [
                {"phase": "准备期", "duration": "3个月", "tasks": ["整理知识产权布局", "补充营收数据", "准备审计报告"]},
                {"phase": "申报期", "duration": "1个月", "tasks": ["在线填写申报表", "上传支撑材料", "提交审核"]},
                {"phase": "等待期", "duration": "4-6周", "tasks": ["关注公示信息", "准备答辩材料"]},
            ],
        }
    elif target_tier == "specialized_sme":
        return {
            "target_tier": target_tier,
            "estimated_timeline": "12-18个月",
            "milestones": [
                {"phase": "准备期", "duration": "6个月", "tasks": ["冲刺营收至1000万", "申请1-2项发明专利", "建立研发费用台账"]},
                {"phase": "申报期", "duration": "1个月", "tasks": ["在线填写申报表", "上传支撑材料", "提交审核"]},
                {"phase": "等待期", "duration": "4-6周", "tasks": ["关注公示信息", "准备后续材料"]},
            ],
        }
    else:
        return {
            "target_tier": "innovative_sme",
            "estimated_timeline": "2-3个月",
            "milestones": [
                {"phase": "准备期", "duration": "2周", "tasks": ["整理研发投入台账", "汇总知识产权证书", "准备审计报告"]},
                {"phase": "申报期", "duration": "1周", "tasks": ["在线填写评价表", "上传支撑材料", "提交审核"]},
                {"phase": "等待期", "duration": "4-6周", "tasks": ["关注公示信息", "准备后续材料"]},
            ],
        }


def generate_document_checklist(current_tier: str, data: Dict) -> List[Dict]:
    """生成材料清单"""
    checklist = [
        {"item": "营业执照", "required": True, "ready": True},
        {"item": "审计报告（近2年）", "required": True, "ready": bool(data.get("revenue_last_year"))},
        {"item": "纳税证明", "required": True, "ready": False},
        {"item": "知识产权证书", "required": True, "ready": bool(data.get("patents_invention") or data.get("patents_utility") or data.get("software_copyrights"))},
        {"item": "研发项目清单", "required": True, "ready": bool(data.get("rd_expense"))},
        {"item": "研发人员花名册", "required": True, "ready": bool(data.get("rd_employees"))},
        {"item": "社保缴纳证明", "required": True, "ready": False},
        {"item": "主导产品说明", "required": True, "ready": False},
    ]

    if current_tier == "specialized_sme" or current_tier == "little_giant":
        checklist.extend([
            {"item": "细分市场占有率说明", "required": True, "ready": False},
            {"item": "为大企业配套证明", "required": True, "ready": False},
            {"item": "质量管理体系认证", "required": True, "ready": False},
        ])

    return checklist


def main():
    if len(sys.argv) > 1:
        input_data = json.loads(sys.argv[1])
    else:
        input_data = json.load(sys.stdin)

    result = run_assessment(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()