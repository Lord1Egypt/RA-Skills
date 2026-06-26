#!/usr/bin/env python3
"""测试脚本：验证 funding_diagnosis.py 的正确性"""
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from funding_diagnosis import run_diagnosis, validate_output

PASS = 0
FAIL = 0

def assert_eq(label, got, expected):
    global PASS, FAIL
    if got == expected:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}: 期望 {expected}, 得到 {got}")

def assert_in(label, key, d):
    global PASS, FAIL
    if key in d:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}: 缺少 key '{key}'")

print("🧪 测试: 融资诊断评分")
print("="*50)

# 测试1：满分输入
print("\n📝 测试1: 满分输入（所有维度优秀）")
r1 = run_diagnosis({
    "traction": {"mao": 100000, "moq_growth": 0.25, "mrr": 100000},
    "market": {"competitors": 1, "customers_interviewed": 100, "tam": 50000000000},
    "team": {"has_cto": True, "founder_count": 3, "industry_exp_years": 12},
    "product": {"has_mvp": True, "version": "v3.0", "active_users": 5000},
    "story": {"has_bp": True, "bp_score": 95},
    "unit_econ": {"ltv_cac": 6.0, "gross_margin": 0.8},
    "use_funds": {"has_plan": True, "breakdown": {"研发": 50, "市场": 30, "团队": 20}},
    "timing": {"runway_months": 14, "market_window": "AI赛道火热"}
})
assert_in("输出含score", "score", r1)
assert_in("输出含grade", "grade", r1)
assert_in("输出含dimensions", "dimensions", r1)
assert_eq("等级为S", r1["grade"], "S")
assert_eq("总分>80", r1["score"]["total"] >= 80, True)
assert_eq("无短板", len(r1["weakness"]), 0)

# 测试2：低分输入
print("\n📝 测试2: 低分输入（所有维度差）")
r2 = run_diagnosis({
    "traction": {"mao": 100, "moq_growth": 0.01},
    "market": {"competitors": 20, "customers_interviewed": 2},
    "team": {"has_cto": False, "founder_count": 1},
    "product": {"has_mvp": False, "version": ""},
    "story": {"has_bp": False, "bp_score": 0},
    "unit_econ": {"ltv_cac": 0.5},
    "use_funds": {"has_plan": False},
    "timing": {"runway_months": 2}
})
assert_in("输出含grade", "grade", r2)
assert_eq("等级为D", r2["grade"], "D")
assert_eq("总分<40", r2["score"]["total"] < 40, True)
assert_eq("有短板", len(r2["weakness"]) > 0, True)

# 测试3：输出格式校验
print("\n📝 测试3: 输出格式校验")
assert_eq("validate_output返回True", validate_output(r1), True)

# 测试4：幂等性（相同输入两次跑）
print("\n📝 测试4: 幂等性测试")
r3a = run_diagnosis({
    "traction": {"mao": 50000, "moq_growth": 0.15},
    "market": {"competitors": 5, "customers_interviewed": 30, "tam": 50000000000},
    "team": {"has_cto": False, "founder_count": 2, "industry_exp_years": 8},
    "product": {"has_mvp": True, "version": "v2.1", "active_users": 500},
    "story": {"has_bp": True, "bp_score": 62},
    "unit_econ": {"ltv_cac": 3.2, "gross_margin": 0.6},
    "use_funds": {"has_plan": False, "breakdown": {}},
    "timing": {"runway_months": 8, "market_window": ""}
})
r3b = run_diagnosis({
    "traction": {"mao": 50000, "moq_growth": 0.15},
    "market": {"competitors": 5, "customers_interviewed": 30, "tam": 50000000000},
    "team": {"has_cto": False, "founder_count": 2, "industry_exp_years": 8},
    "product": {"has_mvp": True, "version": "v2.1", "active_users": 500},
    "story": {"has_bp": True, "bp_score": 62},
    "unit_econ": {"ltv_cac": 3.2, "gross_margin": 0.6},
    "use_funds": {"has_plan": False, "breakdown": {}},
    "timing": {"runway_months": 8, "market_window": ""}
})
assert_eq("相同输入产生相同输出", json.dumps(r3a, sort_keys=True), json.dumps(r3b, sort_keys=True))

# 测试5：边界情况
print("\n📝 测试5: 边界输入")
r4 = run_diagnosis({})
assert_in("空输入也能出结果", "score", r4)
assert_eq("空输入等级至少为D", r4["grade"] in ("D", "C"), True)

print(f"\n{'='*50}")
print(f"📊 测试结果: {PASS} 通过, {FAIL} 失败")
if FAIL == 0:
    print("🎉 全部通过!")
else:
    print(f"❌ {FAIL} 个测试失败")
    sys.exit(1)
