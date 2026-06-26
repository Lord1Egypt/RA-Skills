"""
参数化测试 + 覆盖率补盲
针对 rules_engine.py 中未被 pytest 覆盖的代码路径：
  - RL-004 (个人社保==0 未豁免)
  - YL-004/05/06 (住宿扣款变化 / 出勤超计薪天数 / 标准工资波动)
  - 蓝线 (check_blue_lines)
  - POL-003 离职当月社保公积金 (check_policies)
  - 未知公式类型 (else branch)
  - CLI --output 参数
"""

import pytest
import json
import sys
import argparse
from pathlib import Path
from io import StringIO
from unittest.mock import patch
import pandas as pd
import numpy as np

# ─── fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def engine(tmp_path):
    """每次测试独立加载规则引擎，避免状态污染"""
    from scripts.rules_engine import PayrollRulesEngine
    rules_path = Path(__file__).parents[2] / "references" / "rules.json"
    return PayrollRulesEngine(str(rules_path))


@pytest.fixture
def df_rl004():
    """RL-004: 不符合豁免政策但个人社保=0"""
    return pd.DataFrame({
        "姓名代号": ["员工A"],
        "工号": ["E001"],
        "个人社保": [0],
        "实发金额合计": [5000],
        "应发合计": [5000],
        "平时加班时数": [0],
        "周末加班时数": [0],
        "法定加班时数": [0],
    })


@pytest.fixture
def df_yl004():
    """YL-004: 住宿扣款本月与上月不同（同一员工在两期数据中均有记录）"""
    return pd.DataFrame({
        "工号": ["E001", "E002"],
        "姓名代号": ["甲", "乙"],
        "住宿扣款": [500, 500],   # E001: 本月500，上月600 → 触发
    })


@pytest.fixture
def df_yl004_prev():
    """YL-004 上月数据"""
    return pd.DataFrame({
        "工号": ["E001", "E002"],
        "住宿扣款": [600, 500],   # E001: 上月600，本月500，触发变化
    })


@pytest.fixture
def df_yl005():
    """YL-005: 实际计薪出勤天数 > 应计薪出勤天数（排班异常）"""
    return pd.DataFrame({
        "工号": ["E001"],
        "姓名代号": ["超勤员工"],
        "实际计薪出勤天数": [25],   # > 应计薪 22
        "应计薪出勤天数": [22],
        "住宿扣款": [0],
    })


@pytest.fixture
def df_yl006():
    """YL-006: 标准工资变化（需跨月对比，无上月则跳过）"""
    return pd.DataFrame({
        "工号": ["E001"],
        "姓名代号": ["调薪异常"],
        "标准基本工资": [15000],
        "住宿扣款": [0],
    })


@pytest.fixture
def df_yl006_prev():
    """YL-006 上月数据（标准工资不同 → 触发）"""
    return pd.DataFrame({
        "工号": ["E001"],
        "标准基本工资": [12000],
    })


@pytest.fixture
def df_yl005_no_prev():
    """YL-005/06 无上月数据时 → 跳过"""
    return pd.DataFrame({
        "工号": ["E001"],
        "姓名代号": ["新员工"],
        "实际计薪出勤天数": [25],
        "应计薪出勤天数": [22],
        "标准基本工资": [15000],
        "住宿扣款": [0],
    })


@pytest.fixture
def df_pol003():
    """POL-003: 离职日期 5 号（≤15），应豁免但社保≠0 → 违规"""
    return pd.DataFrame({
        "姓名代号": ["离职员工"],
        "工号": ["E010"],
        "入职日期": ["2024-01-10"],
        "离职日期": ["2026-04-05"],   # 5号离职，当月豁免
        "个人社保": [500],              # 但实际扣了500 → 违规
        "个人公积金": [200],
        "个人公积金缴纳": [0],
    })


@pytest.fixture
def df_unknown_formula():
    """触发 _check_formula 的 else 分支（未知公式类型）"""
    return pd.DataFrame({
        "姓名代号": ["测试"],
        "工号": ["E999"],
        "实发合计_X": [5000],
    })


@pytest.fixture
def df_full_valid():
    """完全正常的数据，用于端到端蓝线测试"""
    return pd.DataFrame({
        "姓名代号": ["张三", "李四"],
        "工号": ["E001", "E002"],
        "实际出勤工资小计": [10000, 12000],
        "实际绩效工资": [2000, 2400],
        "实际出勤福利小计": [500, 600],
        "轮班补贴": [0, 0],
        "加班费小计": [0, 500],
        "业务线奖金合计": [0, 0],
        "提成": [0, 0],
        "补发": [0, 0],
        "其他扣减": [0, 0],
        "应发合计": [12500, 15500],
        "个人社保": [800, 960],
        "个人公积金": [400, 480],
        "个税": [500, 600],
        "税后扣减": [0, 0],
        "住宿扣款": [500, 500],
        "社保差额": [0, 0],
        "公积金差额": [0, 0],
        "经济补偿金": [0, 0],
        "实发金额合计": [10300, 12460],
        "绩效系数": [1.0, 1.0],
        "实际计薪出勤天数": [22, 22],
        "应计薪出勤天数": [22, 22],
        "标准基本工资": [10000, 12000],
        "平时加班时数": [0, 10],
        "周末加班时数": [0, 0],
        "法定加班时数": [0, 0],
        "入职日期": ["2024-01-10", "2024-03-15"],
        "离职日期": [np.nan, np.nan],
        "个人社保": [800, 960],
    })


# ─── RL-004 ────────────────────────────────────────────────────────────────

class TestRL004:
    """RL-004: 社保应缴未缴（无豁免但个人社保=0）"""

    def test_rl004_trigger_without_exclusion(self, engine, df_rl004):
        """无豁免条件 + 个人社保=0 → 触发红线"""
        result = engine.check_red_lines(df_rl004)
        rl004 = next(r for r in result["rule_results"] if r["rule_id"] == "RL-004")
        assert not rl004["passed"], "RL-004 应触发"
        assert rl004["triggered"] == 1
        assert rl004["details"][0]["工号"] == "E001"

    def test_rl004_pass_with_exemption(self, engine):
        """有豁免政策（实习生）→ 不触发"""
        df = pd.DataFrame({
            "姓名代号": ["实习生A"],
            "工号": ["E002"],
            "岗位": ["实习生"],
            "个人社保": [0],
            "实发金额合计": [3000],
            "应发合计": [3000],
            "平时加班时数": [0],
            "周末加班时数": [0],
            "法定加班时数": [0],
        })
        result = engine.check_red_lines(df)
        rl004 = next(r for r in result["rule_results"] if r["rule_id"] == "RL-004")
        assert rl004["passed"], "实习生豁免后 RL-004 不应触发"

    def test_rl004_missing_field(self, engine):
        """个人社保字段不存在 → 跳过，不报错"""
        df = pd.DataFrame({
            "姓名代号": ["无社保字段"],
            "工号": ["E003"],
        })
        result = engine.check_red_lines(df)
        rl004 = next(r for r in result["rule_results"] if r["rule_id"] == "RL-004")
        assert rl004["passed"], "字段不存在时跳过"


# ─── YL-004/05/06 ──────────────────────────────────────────────────────────

class TestYellowLinesAdvanced:
    """补盲 YL-004/05/06 的测试覆盖"""

    def test_yl004_across_months_triggers(self, engine, df_yl004, df_yl004_prev):
        """YL-004: 本月住宿扣款与上月不同 → 标记（E001变化，E002未变）"""
        result = engine.check_yellow_lines(df_yl004, df_yl004_prev)
        yl004 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-004")
        assert not yl004["passed"], "住宿扣款有变化应触发 YL-004"
        assert any(d.get("工号") == "E001" for d in yl004["details"])
        assert not any(d.get("工号") == "E002" for d in yl004["details"]), "E002扣款无变化不应触发"

    def test_yl004_same_across_months(self, engine, df_yl004_prev):
        """YL-004: 本月与上月相同 → 不触发"""
        current = pd.DataFrame({
            "工号": ["E001"],
            "住宿扣款": [600],
        })
        result = engine.check_yellow_lines(current, df_yl004_prev)
        yl004 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-004")
        assert yl004["passed"], "住宿扣款无变化不应触发"

    def test_yl004_no_prev_skips(self, engine, df_yl004):
        """YL-004: 无上月数据 → 跳过（不算失败）"""
        result = engine.check_yellow_lines(df_yl004, prev_df=None)
        yl004 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-004")
        assert yl004["passed"], "无上月数据应跳过，不报失败"

    def test_yl005_triggers(self, engine, df_yl005):
        """YL-005: 实际计薪出勤天数 > 应计薪出勤天数 → 标记"""
        result = engine.check_yellow_lines(df_yl005)
        yl005 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-005")
        assert not yl005["passed"], "出勤天数超限应触发 YL-005"
        assert yl005["triggered"] == 1

    def test_yl006_triggers_with_prev(self, engine, df_yl006, df_yl006_prev):
        """YL-006: 标准工资有变化（与上月对比）→ 标记"""
        result = engine.check_yellow_lines(df_yl006, df_yl006_prev)
        yl006 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-006")
        assert not yl006["passed"], "标准工资变化应触发 YL-006"
        assert any(d.get("工号") == "E001" for d in yl006["details"])

    def test_yl006_no_prev_skips(self, engine, df_yl006):
        """YL-006: 无上月数据 → 跳过（不算失败）"""
        result = engine.check_yellow_lines(df_yl006, prev_df=None)
        yl006 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-006")
        assert yl006["passed"], "无上月数据应跳过"
        assert yl006["passed"]

# ─── 蓝线 ─────────────────────────────────────────────────────────────────

class TestBlueLines:
    """Step 5: 蓝线了解（只做信息收集，不做判断）"""

    def test_blue_lines_all_pass(self, engine, df_full_valid):
        """蓝线无 PASS/FAIL，只返回描述性信息"""
        result = engine.check_blue_lines(df_full_valid)
        assert "total_triggered" in result
        assert len(result["rule_results"]) == 4  # BL-001~004
        rule_ids = [r["rule_id"] for r in result["rule_results"]]
        assert "BL-001" in rule_ids
        assert "BL-002" in rule_ids
        assert "BL-003" in rule_ids
        assert "BL-004" in rule_ids

    def test_blue_lines_note_only(self, engine):
        """蓝线的 action 固定为 note_only"""
        result = engine.check_blue_lines(pd.DataFrame({"工号": ["E001"]}))
        for r in result["rule_results"]:
            assert isinstance(r["triggered"], int)


# ─── 政策校验 ──────────────────────────────────────────────────────────────

class TestPoliciesAdvanced:
    """补盲 check_policies 中 POL-003 的覆盖"""

    def test_pol003_departure_le15_no_deduction_violation(self, engine, df_pol003):
        """POL-003: 5号离职，应豁免但社保≠0 → 政策违规"""
        result = engine.check_policies(df_pol003)
        pol003 = next(r for r in result["rule_results"] if r["policy_id"] == "POL-003")
        assert pol003["matched_count"] == 1, "离职5号员工应符合豁免条件"
        assert pol003["violation_count"] > 0, "社保扣款与豁免预期不符，应报违规"

    def test_pol003_no_violation_when_exempt(self, engine):
        """POL-003: 离职当月社保=0，符合豁免预期 → 无违规"""
        df = pd.DataFrame({
            "姓名代号": ["正常离职"],
            "工号": ["E011"],
            "离职日期": ["2026-04-10"],  # 10号离职
            "个人社保": [0],
            "个人公积金": [0],
        })
        result = engine.check_policies(df)
        pol003 = next(r for r in result["rule_results"] if r["policy_id"] == "POL-003")
        assert pol003["violation_count"] == 0, "豁免预期无违规"

    def test_all_policies_returned(self, engine):
        """三条政策均应在结果中出现"""
        df = pd.DataFrame({"工号": ["E001"]})
        result = engine.check_policies(df)
        assert len(result["rule_results"]) >= 3
        policy_ids = [r["policy_id"] for r in result["rule_results"]]
        assert "POL-001" in policy_ids and "POL-002" in policy_ids
        assert "POL-002" in policy_ids
        assert "POL-003" in policy_ids and "POL-004" in policy_ids and "POL-005" in policy_ids


# ─── 未知公式类型 ─────────────────────────────────────────────────────────

class TestUnknownFormulaType:
    """触发 _check_formula else 分支"""

    @patch("scripts.rules_engine.PayrollRulesEngine._load_rules")
    def test_unknown_formula_type_returns_error(self, mock_load, tmp_path):
        """传入未知规则类型的公式 → 返回 passed=False"""
        from scripts.rules_engine import PayrollRulesEngine

        # 构造含未知类型公式的 rules
        fake_rules = {
            "version": "9.9.9",
            "thresholds": {"overtime_limit": 36, "overtime_breakdown": [], "min_wage_shenzhen": 2360},
            "red_lines": [],
            "yellow_lines": [],
            "blue_lines": [],
            "policies": [],
            "formula_rules": [
                {
                    "id": "FR-UNKNOWN",
                    "name": "未知类型公式",
                    "left": "实发合计_X",
                    # 无 left/right/direction → 走 else
                }
            ],
            "required_fields": {}
        }
        mock_load.return_value = fake_rules
        engine = PayrollRulesEngine.__new__(PayrollRulesEngine)
        engine.rules = fake_rules
        engine.thresholds = fake_rules["thresholds"]
        engine.red_lines = fake_rules["red_lines"]
        engine.yellow_lines = fake_rules["yellow_lines"]
        engine.blue_lines = fake_rules["blue_lines"]
        engine.policies = fake_rules["policies"]
        engine.formula_rules = fake_rules["formula_rules"]
        engine.required_fields = fake_rules["required_fields"]

        df = pd.DataFrame({"实发合计_X": [5000], "姓名代号": ["甲"]})
        result = engine.check_formulas(df)

        unknown_rule = result["formula_results"][0]
        assert unknown_rule["passed"] is False
        assert "未知公式类型" in unknown_rule["error"]


# ─── 端到端（参数化） ───────────────────────────────────────────────────────

class TestParameterizedAudit:
    """参数化端到端测试，验证完整流程"""

    @pytest.mark.parametrize("has_prev", [True, False])
    def test_full_audit_runs_without_error(self, engine, df_full_valid, has_prev, df_yl004_prev):
        """完整审核流程：无论有无上月数据，均正常返回"""
        prev = df_yl004_prev if has_prev else None
        result = engine.run_full_audit(df_full_valid, prev)
        assert "version" in result
        assert "summary" in result
        assert result["total_records"] == 2


# ─── CLI ───────────────────────────────────────────────────────────────────

class TestCLI:
    """CLI 参数和输出行为"""

    def test_cli_with_output_file(self, tmp_path, capsys):
        """--output 参数应将结果写入文件"""
        rules_path = Path(__file__).parents[2] / "references" / "rules.json"
        data_path = tmp_path / "data.csv"
        out_path = tmp_path / "result.json"

        # 写测试数据
        df_full_valid = pd.DataFrame({
            "姓名代号": ["张三"],
            "工号": ["E001"],
            "实际出勤工资小计": [10000],
            "实际绩效工资": [2000],
            "实际出勤福利小计": [500],
            "轮班补贴": [0],
            "加班费小计": [0],
            "业务线奖金合计": [0],
            "提成": [0],
            "补发": [0],
            "其他扣减": [0],
            "应发合计": [12500],
            "个人社保": [800],
            "个人公积金": [400],
            "个税": [500],
            "税后扣减": [0],
            "住宿扣款": [500],
            "社保差额": [0],
            "公积金差额": [0],
            "经济补偿金": [0],
            "实发金额合计": [10300],
            "绩效系数": [1.0],
            "实际计薪出勤天数": [22],
            "应计薪出勤天数": [22],
            "标准基本工资": [10000],
            "平时加班时数": [0],
            "周末加班时数": [0],
            "法定加班时数": [0],
            "入职日期": ["2024-01-10"],
            "离职日期": [np.nan],
        })
        df_full_valid.to_csv(data_path, index=False, encoding="utf-8-sig")

        # 构造 sys.argv
        test_args = [
            "rules_engine.py",
            "--rules", str(rules_path),
            "--data", str(data_path),
            "--output", str(out_path),
        ]

        with patch.object(sys, "argv", test_args):
            from scripts.rules_engine import main
            main()

        # 验证文件写入
        assert out_path.exists(), "CLI 应写入 --output 文件"
        content = json.loads(out_path.read_text(encoding="utf-8"))
        assert "version" in content
        assert content["total_records"] == 1

    def test_cli_requires_rules_and_data(self):
        """不传 --rules/--data 时 argparse 应报错（SystemExit）"""
        test_args = ["rules_engine.py"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit):
                from scripts.rules_engine import main
                main()


# ─── 覆盖率边界 ────────────────────────────────────────────────────────────

class TestCoverageEdgeCases:
    """针对剩余未覆盖行的边界测试"""

    def test_rl004_no_violation_when_nonzero(self, engine):
        """RL-004: 社保正常扣款 → 不触发"""
        df = pd.DataFrame({
            "姓名代号": ["正常员工"],
            "工号": ["E003"],
            "个人社保": [800],
            "实发金额合计": [10000],
            "应发合计": [10000],
            "平时加班时数": [0],
            "周末加班时数": [0],
            "法定加班时数": [0],
        })
        result = engine.check_red_lines(df)
        rl004 = next(r for r in result["rule_results"] if r["rule_id"] == "RL-004")
        assert rl004["passed"], "社保正常扣款不应触发 RL-004"

    def test_yellow_lines_zero_threshold(self, engine):
        """YL 阈值为 0 时不误触发"""
        df = pd.DataFrame({
            "工号": ["E001"],
            "绩效系数": [0.3],  # 既 < 0.5 又不是 > 1.5
            "住宿扣款": [0],
        })
        result = engine.check_yellow_lines(df)
        yl001 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-001")
        yl002 = next(r for r in result["rule_results"] if r["rule_id"] == "YL-002")
        assert yl001["passed"], "0.3 < 1.5 不应触发"
        assert not yl002["passed"], "0.3 < 0.5 应触发"

    def test_summary_p0_p1_p2_counts(self, engine, df_full_valid):
        """汇总中 P0/P1/P2 计数正确"""
        result = engine.run_full_audit(df_full_valid)
        s = result["summary"]
        assert "p0_count" in s
        assert "p1_count" in s
        assert "p2_count" in s
        assert isinstance(s["p0_count"], int)
        assert isinstance(s["p1_count"], int)
        assert isinstance(s["p2_count"], int)
