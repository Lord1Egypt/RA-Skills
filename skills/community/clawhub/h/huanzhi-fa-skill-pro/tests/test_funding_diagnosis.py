#!/usr/bin/env python3
"""
融资诊断脚本测试集
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

用法: python3 -m pytest tests/test_funding_diagnosis.py -v
"""

import sys
import os
import json
from pathlib import Path

# 确保可以导入父目录的scripts
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from funding_diagnosis import run_diagnosis


def test_full_healthy_company():
    """测试一个健康公司的完整诊断"""
    data = {
        "mau": 150000,
        "monthly_revenue": 800000,
        "growth_rate": 0.25,
        "tam": 50000000000,
        "sam": 5000000000,
        "market_validation": "bottom-up验证通过，已有100+付费用户",
        "team_size": 12,
        "has_cto": True,
        "has_cmo": True,
        "founder_experience": 8,
        "tech_team_ratio": 0.6,
        "has_previous_funding": True,
        "has_mvp": True,
        "has_pmf": True,
        "paying_users": 150,
        "retention_rate": 0.65,
        "nps_score": 55,
        "has_clear_narrative": True,
        "has_emotional_hook": True,
        "has_pitch_deck": True,
        "pitch_deck_quality": 18,
        "ltv": 5000,
        "cac": 500,
        "gross_margin": 0.75,
        "funding_amount": 8000000,
        "has_detailed_plan": True,
        "runway_months": 24,
        "allocation_detail": "50%研发, 30%市场, 20%运营",
        "sector": "AI智能体",
        "market_education_cost": "低",
        "competitor_count": 5,
        "market_trend": "AI智能体需求爆发",
        "anxiety_level": 3,
    }
    result = run_diagnosis(data)
    assert result["score"]["total"] >= 70
    assert result["score"]["grade"] in ("A+", "A", "A-", "B+")
    assert len(result["dimensions"]) == 8
    for dim in result["dimensions"]:
        assert dim["score"] >= 0
        assert dim["score"] <= 100


def test_early_stage_company():
    """测试早期阶段公司"""
    data = {
        "mau": 1000,
        "monthly_revenue": 10000,
        "growth_rate": 0.05,
        "tam": 100000000,
        "sam": 10000000,
        "team_size": 2,
        "has_cto": False,
        "founder_experience": 2,
        "has_mvp": False,
        "has_pmf": False,
        "paying_users": 0,
        "has_clear_narrative": False,
        "has_pitch_deck": False,
        "ltv": 0,
        "cac": 0,
        "gross_margin": 0,
        "funding_amount": 500000,
        "has_detailed_plan": False,
        "runway_months": 3,
        "sector": "内容创作",
        "anxiety_level": 8,
    }
    result = run_diagnosis(data)
    assert result["score"]["total"] < 50
    assert result["capital_eq_note"] != ""


def test_score_range():
    """测试评分范围"""
    data = {"mau": 50000, "monthly_revenue": 200000, "growth_rate": 0.12}
    result = run_diagnosis(data)
    assert 0 <= result["score"]["total"] <= 100


def test_empty_input():
    """测试空输入"""
    data = {}
    result = run_diagnosis(data)
    assert 0 <= result["score"]["total"] <= 100
    assert len(result["dimensions"]) == 8


def test_traction_edge_cases():
    """测试Traction维度的边界情况"""
    data = {"mau": 0, "monthly_revenue": 0, "growth_rate": 0}
    result = run_diagnosis(data)
    traction = [d for d in result["dimensions"] if d["name"] == "Traction"][0]
    assert traction["score"] >= 0
    assert traction["score"] <= 100
    assert len(traction["warnings"]) > 0  # 应该提示数据缺失


def test_team_missing_cto():
    """测试缺CTO的Team评分"""
    data = {"team_size": 3, "has_cto": False, "founder_experience": 5}
    result = run_diagnosis(data)
    team = [d for d in result["dimensions"] if d["name"] == "Team"][0]
    # 缺CTO时应该有警告
    cto_warnings = [w for w in team.get("warnings", []) if "CTO" in w]
    assert len(cto_warnings) > 0


def test_high_anxiety_triggers_ceq():
    """测试高焦虑触发Capital EQ提示"""
    data = {"anxiety_level": 9, "mau": 1000}
    result = run_diagnosis(data)
    assert result["capital_eq_note"] != ""


def test_low_anxiety_no_ceq():
    """测试低焦虑不触发Capital EQ提示"""
    data = {"anxiety_level": 1, "mau": 50000, "monthly_revenue": 200000, "growth_rate": 0.15}
    result = run_diagnosis(data)
    assert result["capital_eq_note"] == ""


def test_weaknesses_identification():
    """测试短板识别"""
    data = {"mau": 100, "has_cto": False, "has_mvp": False}
    result = run_diagnosis(data)
    assert len(result["weaknesses"]) > 0


def test_key_fields_present():
    """测试输出关键字段完整性"""
    data = {"mau": 50000, "sector": "AI", "has_cto": True}
    result = run_diagnosis(data)
    required_keys = ["version", "module", "score", "summary", "dimensions", "suggestions"]
    for key in required_keys:
        assert key in result, f"缺少关键字段: {key}"


def test_suggestions_structure():
    """测试建议结构"""
    data = {"mau": 50000, "sector": "AI"}
    result = run_diagnosis(data)
    assert "short_term" in result["suggestions"]
    assert "medium_term" in result["suggestions"]
    assert "long_term" in result["suggestions"]
    for period in ["short_term", "medium_term", "long_term"]:
        assert "timeframe" in result["suggestions"][period]
        assert "tasks" in result["suggestions"][period]


def test_deterministic_output():
    """测试幂等性：相同输入相同输出"""
    data = {"mau": 50000, "monthly_revenue": 200000, "growth_rate": 0.12, "sector": "AI"}
    result1 = run_diagnosis(data)
    result2 = run_diagnosis(data)
    assert result1["score"]["total"] == result2["score"]["total"]
    for d1, d2 in zip(result1["dimensions"], result2["dimensions"]):
        assert d1["score"] == d2["score"]


if __name__ == "__main__":
    # 直接运行测试
    test_funcs = [
        test_full_healthy_company, test_early_stage_company, test_score_range,
        test_empty_input, test_traction_edge_cases, test_team_missing_cto,
        test_high_anxiety_triggers_ceq, test_low_anxiety_no_ceq,
        test_weaknesses_identification, test_key_fields_present,
        test_suggestions_structure, test_deterministic_output,
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