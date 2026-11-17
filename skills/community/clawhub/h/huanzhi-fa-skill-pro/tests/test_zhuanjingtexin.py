#!/usr/bin/env python3
"""
专精特新评估脚本测试集
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

用法: python3 -m pytest tests/test_zhuanjingtexin.py -v
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from zhuanjingtexin_assessor import run_assessment


def test_qualified_company():
    """测试达标企业"""
    data = {
        "company_name": "测试科技",
        "rd_ratio": 0.15,
        "rd_personnel_ratio": 0.4,
        "patents_invention": 3,
        "patents_utility": 5,
        "software_copyrights": 2,
        "revenue_growth": 0.3,
        "profit_growth": 0.15,
        "main_business_revenue_ratio": 0.85,
        "has_quality_cert": True,
        "has_cloud_adoption": True,
        "has_ai_application": True,
        "years_in_segment": 5,
        "rd_expense": 5000000,
        "revenue_last_year": 200000000,
        "employees": 50,
        "rd_employees": 20,
        "establishment_date": "2019-01-01",
        "sector": "AI",
    }
    result = run_assessment(data)
    innovative = result["assessment"]["innovative_sme"]
    specialized = result["assessment"]["specialized_sme"]
    little_giant = result["assessment"]["little_giant"]

    assert innovative["achievable"] is True
    assert specialized["achievable"] is True
    assert little_giant["achievable"] is True or little_giant["score"] >= 70


def test_early_stage_company():
    """测试早期企业"""
    data = {
        "company_name": "早期创业",
        "rd_ratio": 0.02,
        "rd_personnel_ratio": 0.05,
        "patents_invention": 0,
        "patents_utility": 0,
        "software_copyrights": 0,
        "revenue_growth": 0.03,
        "profit_growth": 0,
        "main_business_revenue_ratio": 0.5,
        "has_quality_cert": False,
        "years_in_segment": 1,
        "rd_expense": 500000,
        "revenue_last_year": 5000000,
        "employees": 5,
        "rd_employees": 1,
        "sector": "内容创作",
    }
    result = run_assessment(data)
    innovative = result["assessment"]["innovative_sme"]
    assert innovative["achievable"] is False


def test_field_structure():
    """测试输出字段完整性"""
    data = {"company_name": "测试"}
    result = run_assessment(data)
    required_keys = ["version", "module", "assessment", "roadmap", "document_checklist"]
    for key in required_keys:
        assert key in result, f"缺少关键字段: {key}"


def test_roadmap_generation():
    """测试路线图生成"""
    data = {"company_name": "测试", "rd_ratio": 0.15, "rd_personnel_ratio": 0.4, "patents_invention": 3, "revenue_growth": 0.3, "main_business_revenue_ratio": 0.85, "revenue_last_year": 200000000, "years_in_segment": 5, "rd_expense": 5000000, "profit_growth": 0.15}
    result = run_assessment(data)
    assert "milestones" in result["roadmap"]


def test_document_checklist():
    """测试材料清单生成"""
    data = {"company_name": "测试"}
    result = run_assessment(data)
    assert len(result["document_checklist"]) > 0


def test_next_tiers_for_early_stage():
    """测试早期企业的下一层级建议"""
    data = {"company_name": "测试", "sector": "内容创作", "rd_ratio": 0.02, "rd_personnel_ratio": 0.05, "revenue_growth": 0.03, "main_business_revenue_ratio": 0.5, "revenue_last_year": 5000000, "years_in_segment": 1}
    result = run_assessment(data)
    # 早期企业应该能看到下一层级建议
    assert len(result["next_tiers"]) > 0


def test_next_tiers_for_little_giant():
    """测试小巨人企业（已达最高层级）"""
    data = {"company_name": "测试", "rd_ratio": 0.15, "rd_personnel_ratio": 0.5, "patents_invention": 5, "revenue_growth": 0.3, "profit_growth": 0.15, "main_business_revenue_ratio": 0.9, "years_in_segment": 5, "rd_expense": 5000000, "revenue_last_year": 200000000}
    result = run_assessment(data)
    # 小巨人已达最高层级，next_tiers可能为空
    assert "next_tiers" in result


def test_deterministic():
    """测试幂等性"""
    data = {"company_name": "测试", "rd_ratio": 0.1, "revenue_growth": 0.2, "main_business_revenue_ratio": 0.8, "revenue_last_year": 100000000}
    r1 = run_assessment(data)
    r2 = run_assessment(data)
    assert r1["assessment"]["innovative_sme"]["score"] == r2["assessment"]["innovative_sme"]["score"]


if __name__ == "__main__":
    test_funcs = [
        test_qualified_company, test_early_stage_company, test_field_structure,
        test_roadmap_generation, test_document_checklist, test_next_tiers_for_early_stage,
        test_next_tiers_for_little_giant, test_deterministic,
    ]
    passed = 0
    failed = 0
    for func in test_funcs:
        try:
            func()
            print(f"✅ {func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {func.__name__}: {e}")
            failed += 1
    print(f"\n结果: {passed} 通过, {failed} 失败")
    sys.exit(0 if failed == 0 else 1)