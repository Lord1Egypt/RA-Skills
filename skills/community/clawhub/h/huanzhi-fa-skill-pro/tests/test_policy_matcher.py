#!/usr/bin/env python3
"""
政策匹配引擎测试集
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

用法: python3 -m pytest tests/test_policy_matcher.py -v
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from policy_matcher import match_policies


def test_shanghai_ai_company():
    """测试上海AI公司的政策匹配"""
    data = {
        "district": "徐汇区",
        "sector": "AI智能体",
        "stage": "刚注册",
    }
    result = match_policies(data)
    assert result["module"] == "policy_matcher"
    assert len(result["matched_policies"]) > 0
    assert result["recommended_community"] is not None


def test_lingang_overseas():
    """测试临港出海公司的政策匹配"""
    data = {
        "district": "临港新片区",
        "sector": "出海",
        "stage": "有产品",
    }
    result = match_policies(data)
    assert len(result["matched_policies"]) > 0
    assert "零界魔方" in result["recommended_community"]["name"]


def test_unknown_district():
    """测试未知区域"""
    data = {
        "district": "未知区",
        "sector": "AI",
        "stage": "刚注册",
    }
    result = match_policies(data)
    # 国家政策仍然可以匹配
    assert len(result["matched_policies"]) >= 6  # 国家政策


def test_field_structure():
    """测试输出字段完整性"""
    data = {"district": "徐汇区", "sector": "AI", "stage": "刚注册"}
    result = match_policies(data)
    required_keys = ["version", "module", "user_profile", "matched_policies", "recommended_community", "action_plan", "disclaimer"]
    for key in required_keys:
        assert key in result, f"缺少关键字段: {key}"


def test_deterministic_output():
    """测试幂等性"""
    data = {"district": "徐汇区", "sector": "AI", "stage": "刚注册"}
    r1 = match_policies(data)
    r2 = match_policies(data)
    assert len(r1["matched_policies"]) == len(r2["matched_policies"])


def test_community_recommendation():
    """测试社区推荐"""
    data = {"district": "徐汇区", "sector": "大模型", "stage": "刚注册"}
    result = match_policies(data)
    assert "模速空间" in result["recommended_community"]["name"]


def test_estimated_amount():
    """测试补贴估算"""
    data = {"district": "徐汇区", "sector": "AI智能体", "stage": "刚注册"}
    result = match_policies(data)
    est = result["total_estimated"]
    if est.get("min"):
        assert est["min"] > 0


if __name__ == "__main__":
    test_funcs = [
        test_shanghai_ai_company, test_lingang_overseas, test_unknown_district,
        test_field_structure, test_deterministic_output, test_community_recommendation,
        test_estimated_amount,
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