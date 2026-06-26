#!/usr/bin/env python3
"""
payroll-data-audit: 测试套件
运行方式：python -m pytest tests/test_rules_engine.py -v
"""

import pytest
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.rules_engine import PayrollRulesEngine

# ─── 路径 ────────────────────────────────────────────────────────────

# 从 tests/ → scripts/ → 项目根 → references/
RULES_PATH = Path(__file__).parent.parent.parent / "references" / "rules.json"


# ─── Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def engine():
    return PayrollRulesEngine()  # 自动找 references/rules.json


@pytest.fixture
def sample_df():
    """正常数据：10人，全部合规。字段名与 SOP 规范保持一致。"""
    return pd.DataFrame({
        "发薪月": ["2026年4月"] * 10,
        "公司主体": ["深圳公司"] * 10,
        "姓名代号": [f"员工{i}" for i in range(1, 11)],
        "工号": [f"A{1000+i}" for i in range(1, 11)],
        "一级部门": ["共享服务平台"] * 10,
        "二级部门": ["智能增长"] * 10,
        "三级部门": ["技术中心"] * 10,
        "四级部门": ["公共系统技术开发部"] * 10,
        "岗位": ["技术总监"] * 10,
        "状态": ["正式员工"] * 10,
        "入职日期": ["2025-01-01"] * 10,
        "离职日期": [pd.NA] * 10,
        "转正薪资生效日期": [pd.NA] * 10,
        "调薪生效日期": [pd.NA] * 10,
        "标准基本工资": [10000.0] * 10,
        "标准绩效工资": [3000.0] * 10,
        "应计薪出勤天数": [20.0] * 10,
        "实际计薪出勤天数": [20.0] * 10,
        "实际出勤工资小计": [10000.0] * 10,
        "绩效系数": [1.0] * 10,
        "实际绩效工资": [1000.0] * 10,
        "标准福利": [2000.0] * 10,
        "通讯补贴": [100.0] * 10,
        "电脑补贴": [200.0] * 10,
        "交通补贴": [100.0] * 10,
        "住房补贴": [300.0] * 10,
        "约定补贴": [0.0] * 10,
        "餐补": [200.0] * 10,
        "实际出勤福利小计": [500.0] * 10,
        "轮班补贴": [0.0] * 10,
        "C1&C2班天数": [0.0] * 10,
        "C班天数": [0.0] * 10,
        "D班天数": [0.0] * 10,
        "加班费小计": [0.0] * 10,
        "平时加班时数": [10.0] * 10,
        "周末加班时数": [0.0] * 10,
        "法定加班时数": [0.0] * 10,
        "业务线奖金合计": [0.0] * 10,
        "提成&其他&奖金": [0.0] * 10,
        "补发": [0.0] * 10,
        "其他扣减": [0.0] * 10,
        "应发合计": [11500.0] * 10,
        "个人社保": [800.0] * 10,
        "个人公积金": [500.0] * 10,
        "个人所得税": [500.0] * 10,
        "税后扣减项": [0.0] * 10,
        "个人住宿扣款": [0.0] * 10,
        "个人承担社保差额": [0.0] * 10,
        "个人承担公积金差额": [0.0] * 10,
        "经济补偿金": [0.0] * 10,
        "实发金额合计": [9700.0] * 10,
        "币种": ["CNY"] * 10,
        "病假（天）": [0.0] * 10,
        "事假（天）": [0.0] * 10,
    })


@pytest.fixture
def prev_df():
    """上月正常数据，用于跨月对比测试（SOP 规范字段名）"""
    return pd.DataFrame({
        "工号": [f"A{1000+i}" for i in range(1, 11)],
        "绩效系数": [1.0] * 10,
        "个人住宿扣款": [0.0] * 10,
        "标准基本工资": [10000.0] * 10,
        "标准绩效工资": [3000.0] * 10,
        "标准福利": [2000.0] * 10,
    })


# ─── 测试：红线规则 ──────────────────────────────────────────────────

class TestRedLines:

    def test_rl001_pass_zero(self, engine, sample_df):
        """RL-001：实发=0 应通过（题目要求 > 0 才触发）"""
        df = sample_df.copy()
        df["实发金额合计"] = 0.0
        result = engine.check_red_lines(df)
        # 实发=0，条件是 <= 0，应触发
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-001")
        assert not rl["passed"]

    def test_rl001_pass_positive(self, engine, sample_df):
        """RL-001：实发>0 应通过"""
        df = sample_df.copy()
        df["实发金额合计"] = 5000.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-001")
        assert rl["passed"]

    def test_rl001_fail_negative(self, engine, sample_df):
        """RL-001：实发<0 应触发红线"""
        df = sample_df.copy()
        df["实发金额合计"] = -1200.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-001")
        assert not rl["passed"]
        assert rl["triggered"] == 10  # 全部违规

    def test_rl002_pass_32h(self, engine, sample_df):
        """RL-002：加班=32h 应通过（阈值已更新为32h）"""
        df = sample_df.copy()
        df["平时加班时数"] = 32.0
        df["周末加班时数"] = 0.0
        df["法定加班时数"] = 0.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-002")
        assert rl["passed"]

    def test_rl002_fail_33h(self, engine, sample_df):
        """RL-002：加班=33h 应触发红线（阈值32h）"""
        df = sample_df.copy()
        df["平时加班时数"] = 33.0
        df["周末加班时数"] = 0.0
        df["法定加班时数"] = 0.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-002")
        assert not rl["passed"]

    def test_rl002_exclusion_intern(self, engine, sample_df):
        """RL-002：实习生豁免，加班超32h不应触发"""
        df = sample_df.copy()
        df["状态"] = "实习生（月薪）"
        df["平时加班时数"] = 50.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-002")
        assert rl["passed"]  # 豁免后通过

    def test_rl003_pass_above_minimum(self, engine, sample_df):
        """RL-003：应发>最低工资 应通过"""
        df = sample_df.copy()
        df["应发合计"] = 3000.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-003")
        assert rl["passed"]

    def test_rl003_fail_below_minimum(self, engine, sample_df):
        """RL-003：应发<最低工资 应触发红线"""
        df = sample_df.copy()
        df["应发合计"] = 2000.0
        result = engine.check_red_lines(df)
        rl = next(r for r in result["rule_results"] if r["rule_id"] == "RL-003")
        assert not rl["passed"]


# ─── 测试：公式校验 ──────────────────────────────────────────────────

class TestFormulas:

    def test_fr001_pass(self, engine, sample_df):
        """FR-001：应发合计=各科目之和，应通过"""
        df = sample_df.copy()
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-001")
        assert fr["passed"]

    def test_fr001_fail_wrong_total(self, engine, sample_df):
        """FR-001：应发合计错误，应失败"""
        df = sample_df.copy()
        df.loc[0, "应发合计"] = 99999.0  # 故意写错
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-001")
        assert not fr["passed"]
        assert fr["violation_count"] == 1
        assert any(v.get("姓名代号") == "员工1" for v in fr["violations"])

    def test_fr002_pass(self, engine, sample_df):
        """FR-002：实发合计=应发-代扣+补贴，应通过"""
        df = sample_df.copy()
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-002")
        assert fr["passed"]

    def test_fr002_fail_wrong_total(self, engine, sample_df):
        """FR-002：实发合计错误，应失败"""
        df = sample_df.copy()
        df.loc[0, "实发金额合计"] = 99999.0
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-002")
        assert not fr["passed"]

    def test_fr003_pass_lte(self, engine, sample_df):
        """FR-003：出勤工资≤标准工资，应通过"""
        df = sample_df.copy()
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-003")
        assert fr["passed"]

    def test_fr003_fail_gt(self, engine, sample_df):
        """FR-003：出勤工资>标准工资，应失败"""
        df = sample_df.copy()
        df.loc[0, "实际出勤工资小计"] = 15000.0  # > 标准工资 10000
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-003")
        assert not fr["passed"]
        assert fr["violation_count"] == 1


# ─── 测试：黄线规则 ──────────────────────────────────────────────────

class TestYellowLines:

    def test_yl001_pass_normal(self, engine, sample_df):
        """YL-001：绩效系数=1.0，应通过"""
        result = engine.check_yellow_lines(sample_df)
        yl = next(r for r in result["rule_results"] if r["rule_id"] == "YL-001")
        assert yl["passed"]

    def test_yl001_fail_high(self, engine, sample_df):
        """YL-001：绩效系数=1.6，应标记"""
        df = sample_df.copy()
        df["绩效系数"] = 1.6
        result = engine.check_yellow_lines(df)
        yl = next(r for r in result["rule_results"] if r["rule_id"] == "YL-001")
        assert not yl["passed"]
        assert yl["triggered"] == 10

    def test_yl003_pass_no_prev(self, engine, sample_df):
        """YL-003：无上月数据时跳过，不报失败"""
        result = engine.check_yellow_lines(sample_df, prev_df=None)
        yl = next(r for r in result["rule_results"] if r["rule_id"] == "YL-003")
        # 无上月数据，该规则跳过，不是失败
        assert yl["passed"]

    def test_yl003_fail_big_swing(self, engine, sample_df, prev_df):
        """YL-003：绩效波动>0.5，应标记"""
        df = sample_df.copy()
        df["绩效系数"] = [2.0] * 10  # 上月1.0，本月2.0，差=1.0 > 0.5
        result = engine.check_yellow_lines(df, prev_df)
        yl = next(r for r in result["rule_results"] if r["rule_id"] == "YL-003")
        assert not yl["passed"]
        assert yl["triggered"] == 10


# ─── 测试：字段完整性 ────────────────────────────────────────────────

class TestFields:

    def test_check_fields_pass(self, engine, sample_df):
        """所有字段存在且格式正确，应通过"""
        result = engine.check_fields(sample_df)
        assert result["passed"]
        assert len(result["missing"]) == 0
        assert len(result["format_errors"]) == 0

    def test_check_fields_missing(self, engine):
        """缺少字段，应报告缺失"""
        df = pd.DataFrame({"姓名代号": ["张三"], "工号": ["A001"]})
        result = engine.check_fields(df)
        assert not result["passed"]
        assert len(result["missing"]) > 0

    def test_check_fields_invalid_date(self, engine, sample_df):
        """日期格式错误，应报告格式错误"""
        df = sample_df.copy()
        df["入职日期"] = "not-a-date"
        result = engine.check_fields(df)
        assert not result["passed"]
        assert "入职日期" in result["format_errors"]


# ─── 测试：政策豁免 ──────────────────────────────────────────────────

class TestPolicies:

    def test_policy_after_15th(self, engine, sample_df):
        """POL-001：15号后入职，应豁免社保公积金"""
        df = sample_df.copy()
        df["入职日期"] = "2026-04-16"  # 16号入职
        df["个人社保"] = 0.0  # 按豁免逻辑
        df["个人公积金"] = 0.0
        result = engine.check_policies(df)
        pol = next(r for r in result["rule_results"] if r["policy_id"] == "POL-001")
        assert pol["matched_count"] == 10

    def test_policy_intern_exemption(self, engine, sample_df):
        """POL-002：实习生应豁免社保公积金"""
        df = sample_df.copy()
        df["状态"] = "实习生（月薪）"
        df["个人社保"] = 0.0
        df["个人公积金"] = 0.0
        result = engine.check_policies(df)
        pol = next(r for r in result["rule_results"] if r["policy_id"] == "POL-002")
        assert pol["matched_count"] == 10


# ─── 测试：完整审核流程 ──────────────────────────────────────────────

class TestFullAudit:

    def test_full_audit_pass(self, engine, sample_df, prev_df):
        """正常数据完整审核，应通过"""
        result = engine.run_full_audit(sample_df, prev_df)
        summary = result["summary"]
        assert not summary["blocked"]  # 无红线
        assert summary["p0_count"] == 0
        assert result["total_records"] == 10

    def test_full_audit_fail_red(self, engine, sample_df, prev_df):
        """有红线时 blocked=True"""
        df = sample_df.copy()
        df["实发金额合计"] = -1000.0  # 触发 RL-001
        result = engine.run_full_audit(df, prev_df)
        summary = result["summary"]
        assert summary["blocked"]
        assert summary["p0_count"] > 0

    def test_full_audit_no_prev(self, engine, sample_df):
        """无上月数据时，完整审核仍应正常运行"""
        result = engine.run_full_audit(sample_df, prev_df=None)
        assert "summary" in result
        assert result["total_records"] == 10


# ─── 测试：边界情况 ──────────────────────────────────────────────────

class TestEdgeCases:

    def test_empty_df(self, engine):
        """空 DataFrame 应正常处理，不崩溃"""
        df = pd.DataFrame()
        result = engine.run_full_audit(df)
        assert result["total_records"] == 0
        assert not result["summary"]["blocked"]

    def test_nan_handling(self, engine, sample_df):
        """空值处理：NaN 应不影响计算"""
        df = sample_df.copy()
        df.loc[0, "应发合计"] = np.nan
        result = engine.check_formulas(df)
        fr = next(r for r in result["formula_results"] if r["rule_id"] == "FR-001")
        # NaN参与计算不应崩溃
        assert isinstance(fr["passed"], bool)

    def test_missing_optional_field(self, engine, sample_df):
        """可选字段缺失（如无住宿扣款列）不应崩溃"""
        df = sample_df.copy()
        if "住宿扣款" in df.columns:
            df = df.drop(columns=["住宿扣款"])
        result = engine.check_yellow_lines(df)
        assert "rule_results" in result

    def test_special_char_name(self, engine, sample_df):
        """姓名含特殊字符（·/空格/emoji）应正常处理"""
        df = sample_df.copy()
        df.loc[0, "姓名代号"] = "欧阳·Alice🎯"
        result = engine.run_full_audit(df)
        assert result["total_records"] == 10


# ─── 测试：规则版本一致性 ────────────────────────────────────────────

class TestRulesVersion:

    def test_rules_loads(self):
        """rules.json 应能正常加载"""
        engine = PayrollRulesEngine(str(RULES_PATH))
        assert engine.rules["version"] == "7.0.0"

    def test_all_red_lines_have_id(self):
        """所有红线规则必须有 id"""
        with open(RULES_PATH, encoding="utf-8") as f:
            rules = json.load(f)
        for rl in rules["red_lines"]:
            assert "id" in rl, f"红线规则缺少 id: {rl.get('name')}"
            assert "RL-" in rl["id"]

    def test_all_yellow_lines_have_id(self):
        """所有黄线规则必须有 id"""
        with open(RULES_PATH, encoding="utf-8") as f:
            rules = json.load(f)
        for yl in rules["yellow_lines"]:
            assert "id" in yl, f"黄线规则缺少 id: {yl.get('name')}"
            assert "YL-" in yl["id"]

    def test_formula_tolerance_is_zero(self):
        """应发/实发合计公式容差必须为0"""
        with open(RULES_PATH, encoding="utf-8") as f:
            rules = json.load(f)
        for fr in rules["formula_rules"]:
            if fr["id"] in ["FR-001", "FR-002"]:
                assert fr["tolerance"] == 0, f"{fr['id']} 容差必须为0，实际={fr['tolerance']}"


class TestGetPayMonth:
    """测试 _get_pay_month 对多种发薪月格式的兼容（P0: v7.1.1 原版无法解析中文格式）"""

    def test_standard_format(self):
        """2026-04"""
        df = pd.DataFrame({"发薪月": ["2026-04"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")

    def test_chinese_format_month_single_digit(self):
        """2026年4月（v7.1.1 原版崩溃格式）"""
        df = pd.DataFrame({"发薪月": ["2026年4月"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")

    def test_chinese_format_month_double_digit(self):
        """2026年04月"""
        df = pd.DataFrame({"发薪月": ["2026年04月"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")

    def test_chinese_format_december(self):
        """2025年12月"""
        df = pd.DataFrame({"发薪月": ["2025年12月"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2025-12", freq="M")

    def test_numeric_format(self):
        """202604"""
        df = pd.DataFrame({"发薪月": ["202604"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")

    def test_slash_format(self):
        """2026/04"""
        df = pd.DataFrame({"发薪月": ["2026/04"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")

    def test_no_column_returns_none(self):
        """没有发薪月列返回None"""
        df = pd.DataFrame({"工号": ["E001"]})
        engine = PayrollRulesEngine()
        assert engine._get_pay_month(df) is None

    def test_with_nan_returns_valid(self):
        """含NaN的数据仍能正常解析"""
        df = pd.DataFrame({"发薪月": ["2026年4月", None, "2026年4月"]})
        engine = PayrollRulesEngine()
        result = engine._get_pay_month(df)
        assert result == pd.Period("2026-04", freq="M")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
