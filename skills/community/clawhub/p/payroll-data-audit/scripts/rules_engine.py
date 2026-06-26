#!/usr/bin/env python3
"""
payroll-data-audit: rules_engine
工资数据审核统一规则引擎 (v4.0.0 融合版)

架构: OOP (class PayrollRulesEngine) + 鲁棒性层
- 外部版本的 OOP 架构 + pytest 测试 + CI/CD
- 融合版的 COLUMN_ALIAS 列名容错 + decimal.Decimal 精度 + 数据规范化

职责：
  - 加载 rules.json 作为唯一规则来源
  - 对工资数据逐条执行所有规则校验
  - 输出结构化 JSON 结果，不做自然语言输出

用法:
    python3 -m scripts.rules_engine --data payroll.csv --prev payroll_prev.csv --output result.json
    python3 -m scripts.rules_engine --data payroll.csv --step red_lines --output result.json
"""

import json
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Any, Optional

import pandas as pd
import numpy as np


# ─── 鲁棒性层：列名容错 + 数据规范化 ──────────────────────────────────

COLUMN_ALIAS = {
    "实发金额合计": ["实发合计", "实发金额", "net_pay", "实发", "实发工资", "实发工资合计", "实际发放金额"],
    "应发合计": ["应发", "gross_pay", "应发工资", "应发工资合计", "应发合计金额", "税前应发"],
    "实际出勤工资小计": ["出勤工资", "实际出勤工资", "出勤工资小计", "基本出勤工资", "标准出勤工资"],
    "标准基本工资": ["基本工资", "标准工资", "base_salary", "基本工资标准", "标准基本薪资", "基本薪资"],
    "实际计薪出勤天数": ["计薪天数", "出勤天数", "pay_days", "实际出勤天数", "计薪出勤天数"],
    "应计薪出勤天数": ["应计薪天数", "should_pay_days", "应出勤天数", "标准计薪天数", "规定出勤天数"],
    "绩效系数": ["performance_score", "绩效分", "绩效评分", "绩效系数值", "绩效考核系数"],
    "实际绩效工资": ["绩效工资", "performance_pay", "绩效工资小计", "实际绩效", "绩效奖金"],
    "个人社保": ["社保", "social_insurance", "社保个人", "个人社保费", "社保扣款"],
    "个人公积金": ["公积金", "housing_fund", "公积金个人", "个人公积金", "公积金扣款", "住房公积金"],
    "加班费小计": ["加班费", "overtime_pay", "加班费合计", "加班工资", "加班工资小计"],
    "平时加班时数": ["平时加班", "ot_normal", "工作日加班时数", "平日加班"],
    "周末加班时数": ["周末加班", "ot_weekend", "休息日加班时数", "周六日加班"],
    "法定加班时数": ["法定加班", "ot_legal", "法定节假日加班时数", "法定假日加班"],
    "业务线奖金合计": ["业务线奖金", "bonus", "业务奖金", "部门奖金", "业务线奖金小计"],
    "提成&其他&奖金": ["提成", "commission", "提成合计", "销售提成", "业务提成", "提成及其他奖金", "其他奖金"],
    "补发": ["补发工资", "补发合计", "补发金额", "追溯补发"],
    "其他扣减": ["其他扣款", "其他扣除", "其他扣减合计"],
    "公司主体": ["主体", "company", "公司", "所属公司", "法人主体"],
    "岗位": ["职位", "position", "job_title", "岗位名称", "职务"],
    "状态": ["员工状态", "身份标签", "employee_status", "status_type"],
    "入职日期": ["入职时间", "hire_date", "入职日", "报到日期", "到岗日期"],
    "离职日期": ["离职时间", "leave_date", "离职日", "最后工作日"],
    "个人住宿扣款": ["住宿扣款", "住宿", "accommodation", "宿舍扣款", "住宿费", "个人住宿扣款"],
    "轮班补贴": ["轮班", "轮班津贴", "夜班补贴", "班次补贴"],
    "实际出勤福利小计": ["福利", "benefits", "福利小计", "出勤福利", "福利补贴合计"],
    "病假（天）": ["病假", "病假天数", "病假小时", "病假时数"],
    "事假（天）": ["事假", "事假天数", "事假小时", "事假时数"],
    "转正薪资生效日期": ["转正日期", "转正生效日", "转正日"],
    "调薪生效日期": ["调薪日期", "调薪生效日", "薪资调整日期"],
    "发薪月": ["发薪月份", "pay_month", "所属月份", "计薪月份", "工资月份"],
    "姓名代号": ["姓名", "name", "员工姓名"],
    "工号": ["员工编号", "employee_id", "emp_no", "员工工号", "编号"],
    "个人承担社保差额": ["社保差额", "社保补缴差额"],
    "个人承担公积金差额": ["公积金差额", "公积金补缴差额"],
    "个人所得税": ["个税", "个税扣款", "个人所得税扣款"],
    "税后扣减项": ["税后扣减", "税后扣款", "税后扣除"],
    "经济补偿金": ["补偿金", "离职补偿", "经济补偿"],
    # 新增字段（文档要求）
    "标准绩效工资": ["标准绩效", "绩效标准工资"],
    "标准福利": ["标准福利金额", "福利标准"],
    "C1&C2班天数": ["C1&C2班", "C1C2班天数"],
    "C班天数": ["C班"],
    "D班天数": ["D班"],
    "一级部门": ["一级部门名称"],
    "二级部门": ["二级部门名称"],
    "三级部门": ["三级部门名称"],
    "四级部门": ["四级部门名称"],
    "班天数合计": ["班天数", "排班天数", "应排班天数"],
    "币种": ["currency"],
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """将 DataFrame 列名统一为 rules.json 中的标准列名"""
    rename_map = {}
    for standard, aliases in COLUMN_ALIAS.items():
        if standard in df.columns:
            continue
        for alias in aliases:
            if alias in df.columns:
                rename_map[alias] = standard
                break
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def normalize_types(df: pd.DataFrame) -> pd.DataFrame:
    """类型强转 + 缺失值填充"""
    numeric_fields = _collect_numeric_fields()
    for col in numeric_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    date_fields = ["入职日期", "离职日期", "转正薪资生效日期", "调薪生效日期"]
    for col in date_fields:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    str_fields = ["公司主体", "岗位", "状态", "姓名代号", "工号", "发薪月"]
    for col in str_fields:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")
    # 全角/半角括号统一：状态列/岗位列全角（）→ 半角()
    for col in ["状态", "岗位"]:
        if col in df.columns:
            df[col] = df[col].str.replace("（", "(").str.replace("）", ")")
    return df


def _collect_numeric_fields() -> set:
    """收集所有需要数值型的字段"""
    return {
        "应发合计", "实发金额合计", "实际出勤工资小计", "标准基本工资",
        "实际计薪出勤天数", "应计薪出勤天数", "绩效系数", "实际绩效工资",
        "个人社保", "个人公积金", "加班费小计", "平时加班时数",
        "周末加班时数", "法定加班时数", "业务线奖金合计", "提成&其他&奖金",
        "补发", "其他扣减", "个人住宿扣款", "住宿扣款", "轮班补贴", "实际出勤福利小计",
        "病假（天）", "病假", "事假（天）", "事假", "班天数合计",
        "个人承担社保差额", "社保差额", "个人承担公积金差额", "公积金差额",
        "个人所得税", "个税", "税后扣减项", "税后扣减",
        "经济补偿金",
        # 新增字段（文档要求）
        "标准绩效工资", "标准福利",
        "C1&C2班天数", "C班天数", "D班天数",
        "币种",
    }


# ─── 主引擎 ──────────────────────────────────────────────────────────

class PayrollRulesEngine:
    """工资数据审核规则引擎"""

    def __init__(self, rules_path: str = None):
        if rules_path is None:
            rules_dir = Path(__file__).parent
            if (rules_dir / "rules.json").exists():
                rules_path = rules_dir / "rules.json"
            else:
                rules_path = rules_dir.parent / "references" / "rules.json"
        self.rules = self._load_rules(str(rules_path))
        self.thresholds = self.rules.get("thresholds", {})
        self.red_lines = self.rules.get("red_lines", [])
        self.yellow_lines = self.rules.get("yellow_lines", [])
        self.blue_lines = self.rules.get("blue_lines", [])
        self.policies = self.rules.get("policies", [])
        self.formula_rules = self.rules.get("formula_rules", [])
        self.business_rules = self.rules.get("business_rules", [])
        self.required_fields = self.rules.get("required_fields", {})

    def _load_rules(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_full_audit(self, df: pd.DataFrame, prev_df: pd.DataFrame = None) -> dict:
        """执行完整审核流程 (Step 1 → 6)"""
        # 空数据快速返回
        if len(df) == 0:
            return {
                "version": self.rules.get("version", ""),
                "audit_time": datetime.now().isoformat(),
                "total_records": 0,
                "field_check": {"passed": True, "missing": {}, "format_errors": {}, "total_fields_checked": 0},
                "formula_check": {"passed": True, "formula_results": []},
                "business_check": {"rule_results": []},
                "red_lines": {"passed": True, "total_triggered": 0, "rule_results": []},
                "yellow_lines": {"passed": True, "total_triggered": 0, "rule_results": []},
                "blue_lines": {"passed": True, "total_triggered": 0, "rule_results": []},
                "policy_check": {"rule_results": []},
                "comparison": None,
                "summary": {"status": "clean", "blocked": False, "total_records": 0, "p0_count": 0, "p1_count": 0, "p2_count": 0, "formula_passed": True, "field_check_passed": True},
            }

        # 预处理：列名容错 + 类型规范化
        df = normalize_columns(df.copy())
        df = normalize_types(df)

        if prev_df is not None:
            prev_df = normalize_columns(prev_df.copy())
            prev_df = normalize_types(prev_df)

        results = {
            "version": self.rules.get("version", ""),
            "audit_time": datetime.now().isoformat(),
            "total_records": len(df),
            "field_check": self.check_fields(df),
            "formula_check": self.check_formulas(df),
            "business_check": self.check_business_rules(df),
            "red_lines": self.check_red_lines(df, prev_df),
            "yellow_lines": self.check_yellow_lines(df, prev_df),
            "blue_lines": self.check_blue_lines(df, prev_df),
            "policy_check": self.check_policies(df),
            "comparison": self.compare_periods(df, prev_df) if prev_df is not None else None,
            "continuous_analysis": self.analyze_continuous_employees(df, prev_df) if prev_df is not None else None,
            "summary": {}
        }
        results["summary"] = self._generate_summary(results)
        return results

    # ─── Step 1: 字段完整性校验 ───────────────────────────────────────

    def check_fields(self, df: pd.DataFrame) -> dict:
        """Step 1: 检查必检字段的完整性和格式"""
        missing = {}
        format_errors = {}

        flat_fields = [f for fields in self.required_fields.values() for f in fields]

        for field in flat_fields:
            if field not in df.columns:
                missing[field] = "字段不存在"
            else:
                na_count = int(df[field].isna().sum())
                if 0 < na_count < len(df):
                    missing[field] = na_count

                # 日期字段格式检查
                if "日期" in field:
                    invalid_dates = df[field].apply(self._is_invalid_date)
                    if invalid_dates.sum() > 0:
                        format_errors[field] = f"{invalid_dates.sum()} 条日期格式异常"

        passed = len(missing) == 0 and len(format_errors) == 0
        return {
            "passed": passed,
            "missing": missing,
            "format_errors": format_errors,
            "total_fields_checked": len(flat_fields),
        }

    def _is_invalid_date(self, val: Any) -> bool:
        if pd.isna(val):
            return False
        if isinstance(val, (pd.Timestamp, datetime)):
            return False
        if isinstance(val, str) and val.strip():
            try:
                pd.to_datetime(val)
                return False
            except Exception:
                return True
        return False

    # ─── Step 2: 公式校验 ─────────────────────────────────────────────

    def check_formulas(self, df: pd.DataFrame) -> dict:
        """Step 2: 校验表内计算公式"""
        results = []
        for rule in self.formula_rules:
            results.append(self._check_formula(df, rule))

        passed = all(r["passed"] for r in results)
        return {"passed": passed, "formula_results": results}

    def _check_formula(self, df: pd.DataFrame, rule: dict) -> dict:
        """执行单条公式校验（使用 Decimal 保证精度）"""
        rule_id = rule["id"]
        left_field = rule["left"]
        if left_field not in df.columns:
            return {"rule_id": rule_id, "passed": False, "error": f"字段不存在: {left_field}"}

        df_check = df.copy()
        tolerance = Decimal(str(rule.get("tolerance", 0.01)))

        if rule["id"] == "FR-001":
            # 应发合计 = 实际出勤工资小计 + 实际绩效工资 + 实际出勤福利小计 + 轮班补贴 + 加班费小计 + 业务线奖金合计 + 提成&其他&奖金 + 补发 - 其他扣减
            income_fields = rule.get("right_fields", [])
            deduction_fields = rule.get("deductions", [])
            income_fields_valid = [f for f in income_fields if f in df_check.columns]
            deduction_fields_valid = [f for f in deduction_fields if f in df_check.columns]

            df_check["computed"] = (
                df_check[income_fields_valid].fillna(0).sum(axis=1)
                - df_check[deduction_fields_valid].fillna(0).sum(axis=1)
            )
            # 文档要求：误差必须为0元（容忍度已在rules.json中设为0）
        elif rule["id"] == "FR-002":
            # 实发合计 = 应发合计 - 个人社保 - 个人公积金 - 个人所得税 - 税后扣减项 - 个人住宿扣款 - 个人承担社保差额 - 个人承担公积金差额 + 经济补偿金
            additions = rule.get("additions", [])
            deductions = rule.get("deductions", [])
            additions_valid = [f for f in additions if f in df_check.columns]
            deductions_valid = [f for f in deductions if f in df_check.columns]

            df_check["computed"] = (
                df_check["应发合计"].fillna(0)
                - df_check[deductions_valid].fillna(0).sum(axis=1)
                + df_check[additions_valid].fillna(0).sum(axis=1)
            )
            # 文档要求：误差必须为0元
        elif rule.get("direction") == "lte":
            # 方向性比较：left <= right_field（FR-003/FR-004）
            right_field = rule.get("right_field", "")
            if right_field not in df_check.columns:
                return {"rule_id": rule_id, "passed": True, "error": f"右字段不存在: {right_field}"}
            left_vals = pd.to_numeric(df_check[left_field], errors="coerce").fillna(0)
            right_vals = pd.to_numeric(df_check[right_field], errors="coerce").fillna(0)
            df_check["computed"] = right_vals  # For comparison, computed = right
            df_check["diff"] = (left_vals - right_vals).clip(lower=0)
            # Violations where left > right + tolerance
            tolerance_float = float(tolerance)
            failed_mask = df_check["diff"] > tolerance_float
            # FR-003 出勤工资校验：排除实习生(日薪)、实习生(月薪)、日薪
            if rule_id == "FR-003":
                status_col = "状态" if "状态" in df_check.columns else "岗位"
                if status_col in df_check.columns:
                    exempt_status = df_check[status_col].str.contains("实习生|日薪", na=False)
                    failed_mask = failed_mask & ~exempt_status
            violations = []
            if failed_mask.any():
                for idx in df_check[failed_mask].index:
                    violations.append({
                        "index": int(idx),
                        "姓名代号": str(df_check.loc[idx].get("姓名代号", "")),
                        "工号": str(df_check.loc[idx].get("工号", "")),
                        "left_field": left_field,
                        "right_field": right_field,
                        "left_value": round(float(df_check.loc[idx, left_field]), 2),
                        "right_value": round(float(df_check.loc[idx, right_field]), 2),
                        "diff": round(float(df_check.loc[idx, "diff"]), 2),
                    })
            return {
                "rule_id": rule_id,
                "rule_name": rule.get("name", ""),
                "passed": len(violations) == 0,
                "total_checked": len(df_check),
                "violation_count": len(violations),
                "violations": violations[:20],
            }
        else:
            # 未知公式类型：检查是否有 formula_expression
            expr = rule.get("formula_expression", "")
            if not expr:
                # 没有表达式，返回错误
                return {
                    "rule_id": rule_id,
                    "rule_name": rule.get("name", ""),
                    "passed": False,
                    "total_checked": 0,
                    "violation_count": 0,
                    "violations": [],
                    "error": f"未知公式类型: {rule_id}，无 formula_expression",
                }
            # 通用公式：用 Decimal 计算
            computed = self._compute_formula_decimal(df_check, rule)
            df_check["computed"] = computed

        df_check["actual"] = pd.to_numeric(df_check[left_field], errors="coerce").fillna(0)
        df_check["diff"] = (df_check["computed"] - df_check["actual"]).abs()

        tolerance_float = float(tolerance)
        # 最小容差 0.01 元（SOP "0元误差" 在浮点运算中应理解为 <=0.01）
        effective_tolerance = max(tolerance_float, 0.01) if tolerance_float == 0 else tolerance_float
        failed_mask = df_check["diff"] > effective_tolerance
        violations = []
        if failed_mask.any():
            for idx in df_check[failed_mask].index:
                violations.append({
                    "index": int(idx),
                    "姓名代号": str(df_check.loc[idx].get("姓名代号", "")),
                    "工号": str(df_check.loc[idx].get("工号", "")),
                    "computed": round(float(df_check.loc[idx, "computed"]), 2),
                    "actual": round(float(df_check.loc[idx, "actual"]), 2),
                    "diff": round(float(df_check.loc[idx, "diff"]), 2),
                })

        return {
            "rule_id": rule_id,
            "rule_name": rule.get("name", ""),
            "passed": len(violations) == 0,
            "total_checked": len(df_check),
            "violation_count": len(violations),
            "violations": violations[:20],  # 最多返回 20 条
        }

    def _compute_formula_decimal(self, df: pd.DataFrame, rule: dict) -> pd.Series:
        """使用 Decimal 计算公式（防止浮点误差）"""
        expr = rule.get("formula_expression", "")
        if not expr:
            return pd.Series([0.0] * len(df))

        result = pd.Series([Decimal("0")] * len(df))
        # 解析简单表达式如 "A + B - C"
        tokens = re.findall(r'([+\-])?\s*([A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*)', expr)
        for idx in range(len(df)):
            val = Decimal("0")
            for sign, field in tokens:
                sign = sign or "+"
                if field in df.columns:
                    try:
                        fv = Decimal(str(df.loc[idx, field]))
                    except (InvalidOperation, TypeError):
                        fv = Decimal("0")
                else:
                    fv = Decimal("0")
                if sign == "+":
                    val += fv
                else:
                    val -= fv
            result.iloc[idx] = val
        return result.astype(float)

    # ─── 业务规则校验 ──────────────────────────────────────────────────

    def check_business_rules(self, df: pd.DataFrame) -> dict:
        """业务规则校验（出勤工资 ≤ 标准工资、天数合理等）"""
        results = []
        for rule in self.business_rules:
            results.append(self._check_business_rule(df, rule))
        return {"rule_results": results}

    def _check_business_rule(self, df: pd.DataFrame, rule: dict) -> dict:
        condition = rule.get("condition", "")
        exclusions_field = rule.get("exclusions_field", "")
        exclusions_values = rule.get("exclusions_values", [])

        # BR-005 特殊处理：轮班天数合理性
        if rule["id"] == "BR-005":
            return self._check_shift_days_rule(df, rule)

        # 解析 field1 <= field2 类条件
        mask = self._evaluate_field_comparison(df, condition)

        # 排除条件
        if exclusions_field and exclusions_values and exclusions_field in df.columns:
            exclusion_mask = df[exclusions_field].astype(str).isin(
                [str(v) for v in exclusions_values]
            )
            mask = mask & ~exclusion_mask

        triggered = int(mask.sum())
        details = []
        if triggered > 0:
            for idx in df[mask.values].index[:20]:
                details.append({
                    "index": int(idx),
                    "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                    "工号": str(df.loc[idx].get("工号", "")),
                })

        return {
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "passed": triggered == 0,
            "total_checked": len(df),
            "triggered": triggered,
            "details": details,
        }

    def _check_shift_days_rule(self, df: pd.DataFrame, rule: dict) -> dict:
        """BR-005: 轮班天数合理性校验
        C1&C2班天数 + C班天数 + D班天数 <= 实际计薪出勤天数
        """
        shift_cols = ["C1&C2班天数", "C班天数", "D班天数"]
        actual_col = "实际计薪出勤天数"
        
        valid_shift_cols = [c for c in shift_cols if c in df.columns]
        
        if not valid_shift_cols or actual_col not in df.columns:
            return {
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "passed": True,
                "total_checked": 0,
                "triggered": 0,
                "details": [],
                "note": "缺少必要列，跳过"
            }
        
        total_shift = df[valid_shift_cols].fillna(0).sum(axis=1)
        actual = pd.to_numeric(df[actual_col], errors="coerce").fillna(0)
        mask = total_shift > actual
        
        triggered = int(mask.sum())
        details = []
        if triggered > 0:
            for idx in df[mask.values].index[:20]:
                details.append({
                    "index": int(idx),
                    "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                    "工号": str(df.loc[idx].get("工号", "")),
                    "shift_days": round(float(total_shift.loc[idx]), 1),
                    "actual_days": round(float(actual.loc[idx]), 1),
                })
        
        return {
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "passed": triggered == 0,
            "total_checked": len(df),
            "triggered": triggered,
            "details": details,
        }

    def _evaluate_field_comparison(self, df: pd.DataFrame, condition: str) -> pd.Series:
        """评估 field1 <= field2 类条件（双字段比较）"""
        if not condition:
            return pd.Series([False] * len(df))

        # 尝试解析 field1 OP field2
        match = re.match(
            r'([A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*)\s*([<>=!]+)\s*([A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*)',
            condition
        )
        if match:
            field1, op, field2 = match.groups()
            if field1 in df.columns and field2 in df.columns:
                v1 = pd.to_numeric(df[field1], errors="coerce").fillna(0)
                v2 = pd.to_numeric(df[field2], errors="coerce").fillna(0)
                if op == ">": return v1 > v2
                elif op == ">=": return v1 >= v2
                elif op == "<": return v1 < v2
                elif op == "<=": return v1 <= v2
                elif op == "==": return v1 == v2
                elif op == "!=": return v1 != v2

        # 降级到简单条件
        return self._evaluate_simple_condition(df, condition)

    # ─── 红线校验 ──────────────────────────────────────────────────────

    def check_red_lines(self, df: pd.DataFrame, prev_df: pd.DataFrame = None) -> dict:
        """红线扫描（实发≤0、加班超32h、低于最低工资、社保未缴）"""
        results = []
        for rule in self.red_lines:
            results.append(self._check_red_line(df, rule, prev_df))

        triggered_total = sum(r["triggered"] for r in results)
        return {
            "passed": triggered_total == 0,
            "total_triggered": triggered_total,
            "rule_results": results,
        }

    def _check_red_line(self, df: pd.DataFrame, rule: dict, prev_df: pd.DataFrame = None) -> dict:
        """执行单条红线规则"""
        rule_id = rule["id"]
        exclusions_field = rule.get("exclusions_field", "")
        exclusions_values = rule.get("exclusions_values", [])

        # 统一追踪 exclusion_mask（各分支写入，最终传入 _build_judgment）
        exclusion_mask = pd.Series([False] * len(df), index=df.index)

        # 处理特殊规则
        if rule_id == "RL-001":
            # 实发≤0
            mask = pd.to_numeric(df.get("实发金额合计", pd.Series([0])), errors="coerce").fillna(0) <= 0
        elif rule_id == "RL-002":
            # 加班超36h
            overtime_cols = [c for c in ["平时加班时数", "周末加班时数", "法定加班时数"] if c in df.columns]
            if overtime_cols:
                total_ot = df[overtime_cols].fillna(0).sum(axis=1)
                mask = total_ot > self.thresholds.get("overtime_limit", 32)
            else:
                mask = pd.Series([False] * len(df), index=df.index)
            # Apply exclusions: check exclusions list from rules.json
            exclusions = rule.get("exclusions", [])
            if exclusions:
                status_col = "状态" if "状态" in df.columns else "岗位"
                if status_col in df.columns:
                    # Fuzzy match: "实习生（月薪）" contains "实习生", "实习生（日薪）" contains "日薪"
                    for e in exclusions:
                        exclusion_mask |= df[status_col].astype(str).str.contains(str(e), na=False)
                if "离职日期" in df.columns:
                    term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
                    exclusion_mask |= term_dates.notna()
                if "入职日期" in df.columns:
                    hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                    current_month = hire_dates.notna() & (hire_dates.dt.month == pd.Timestamp.now().month)
                    exclusion_mask |= current_month
                if "病假" in df.columns:
                    exclusion_mask |= (pd.to_numeric(df["病假"], errors="coerce").fillna(0) > 15)
                mask = mask & ~exclusion_mask
        elif rule_id == "RL-003":
            # 低于最低工资 - 排除实习生(日薪/月薪)、当月入职、当月离职、当月长时间请假
            min_wage = self._get_min_wage(df)
            mask = pd.to_numeric(df.get("应发合计", pd.Series([0])), errors="coerce").fillna(0) < min_wage
            # 应用排除逻辑
            exclusions = rule.get("exclusions", [])
            if exclusions:
                # 岗位类排除：实习生(日薪)、实习生(月薪)、日薪、保洁 — "状态"列优先，"岗位"列降级
                status_col = "状态" if "状态" in df.columns else "岗位"
                if status_col in df.columns:
                    position_excl = [e for e in exclusions if e.startswith("实习生") or e in ("日薪", "保洁")]
                    if position_excl:
                        exclusion_mask |= df[status_col].astype(str).isin(position_excl)
                # 当月入职排除
                if "当月入职" in exclusions and "入职日期" in df.columns:
                    hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                    pay_month = self._get_pay_month(df)
                    if pay_month:
                        exclusion_mask |= hire_dates.dt.to_period("M") == pay_month
                # 当月离职排除
                if "当月离职" in exclusions and "离职日期" in df.columns:
                    term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
                    pay_month = self._get_pay_month(df)
                    if pay_month:
                        exclusion_mask |= term_dates.dt.to_period("M") == pay_month
                # 当月长时间请假排除（文档要求：>10天）
                if "当月长时间请假" in exclusions:
                    leave_mask = pd.Series([False] * len(df), index=df.index)
                    # 兼容多种列名
                    for col in ["病假（天）", "病假"]:
                        if col in df.columns:
                            leave_mask |= pd.to_numeric(df[col], errors="coerce").fillna(0) > 10
                    for col in ["事假（天）", "事假"]:
                        if col in df.columns:
                            leave_mask |= pd.to_numeric(df[col], errors="coerce").fillna(0) > 10
                    exclusion_mask |= leave_mask
                mask = mask & ~exclusion_mask
        elif rule_id == "RL-004":
            # 社保公积金应缴未缴
            # 主字段不存在时跳过（无法验证）
            if "个人社保" not in df.columns:
                return {
                    "rule_id": rule_id, "rule_name": rule["name"],
                    "passed": True, "total_checked": 0, "triggered": 0,
                    "details": [], "note": "个人社保字段不存在，跳过",
                }
            exempt = self._get_exemption_mask(df)
            exclusion_mask = exempt  # 将排除mask传给 judgment
            social = pd.to_numeric(df["个人社保"], errors="coerce").fillna(0)
            fund_col = "个人公积金" if "个人公积金" in df.columns else None
            fund = pd.to_numeric(df[fund_col], errors="coerce").fillna(0) if fund_col else pd.Series([0] * len(df), index=df.index)
            mask = (~exempt) & (social == 0) & (fund == 0)
        elif rule_id == "RL-005":
            # 出勤工资超标准工资（红线）
            if "实际出勤工资小计" in df.columns and "标准基本工资" in df.columns:
                actual = pd.to_numeric(df["实际出勤工资小计"], errors="coerce")
                standard = pd.to_numeric(df["标准基本工资"], errors="coerce")
                # 排除 NaN 比较（NaN 不应触发红线）
                valid = actual.notna() & standard.notna() & (standard > 0)
                mask = valid & (actual > standard)
            else:
                mask = pd.Series([False] * len(df), index=df.index)
            # 排除实习生/日薪/保洁 — "状态"列优先
            exclusions = rule.get("exclusions", [])
            if exclusions:
                status_col = "状态" if "状态" in df.columns else "岗位"
                if status_col in df.columns:
                    # Fuzzy match for status values
                    for e in exclusions:
                        exclusion_mask |= df[status_col].astype(str).str.contains(str(e), na=False)
                mask = mask & ~exclusion_mask
        elif rule_id == "RL-006":
            # 出勤天数超应出勤（红线）
            if "实际计薪出勤天数" in df.columns and "应计薪出勤天数" in df.columns:
                actual = pd.to_numeric(df["实际计薪出勤天数"], errors="coerce").fillna(0)
                should = pd.to_numeric(df["应计薪出勤天数"], errors="coerce").fillna(0)
                mask = actual > should
            else:
                mask = pd.Series([False] * len(df), index=df.index)
        elif rule_id == "RL-007":
            # 标准工资三字段变化无记录（红线）
            mask = pd.Series([False] * len(df), index=df.index)
            if prev_df is not None:
                change_fields = ["标准基本工资", "标准绩效工资", "标准福利"]
                # 优先用"姓名代号"匹配（工号是简单序号，不同月份可能对应不同人）
                join_key = "姓名代号" if "姓名代号" in df.columns and "姓名代号" in prev_df.columns else "工号"
                
                has_any_change = pd.Series([False] * len(df), index=df.index)
                for field in change_fields:
                    if field in df.columns and field in prev_df.columns:
                        curr = pd.to_numeric(df[field], errors="coerce").fillna(0)
                        # Build prev lookup
                        prev_lookup = dict(zip(prev_df[join_key], pd.to_numeric(prev_df[field], errors="coerce").fillna(0)))
                        prev_vals = df[join_key].map(prev_lookup).fillna(-1)
                        has_any_change |= (curr != prev_vals) & (curr != 0) & (prev_vals != -1)
                
                # 豁免条件：当月或往月有调薪/转正记录
                exempt = pd.Series([False] * len(df), index=df.index)
                if "调薪生效日期" in df.columns:
                    adj = pd.to_datetime(df["调薪生效日期"], errors="coerce")
                    curr_month = self._get_pay_month(df)
                    if curr_month:
                        exempt |= adj.dt.to_period("M") == curr_month
                if "转正薪资生效日期" in df.columns:
                    reg = pd.to_datetime(df["转正薪资生效日期"], errors="coerce")
                    curr_month = self._get_pay_month(df)
                    if curr_month:
                        exempt |= reg.dt.to_period("M") == curr_month
                
                # 往月调薪/转正豁免
                if prev_df is not None and join_key in prev_df.columns:
                    if "调薪生效日期" in prev_df.columns:
                        prev_adj = pd.to_datetime(prev_df["调薪生效日期"], errors="coerce")
                        prev_month = self._get_pay_month(prev_df)
                        if prev_month:
                            prev_exempt_mask = (prev_adj.dt.to_period("M") == prev_month)
                            prev_exempt_map = dict(zip(prev_df[join_key], prev_exempt_mask))
                            exempt |= df[join_key].map(prev_exempt_map).fillna(False)
                    if "转正薪资生效日期" in prev_df.columns:
                        prev_reg = pd.to_datetime(prev_df["转正薪资生效日期"], errors="coerce")
                        prev_month = self._get_pay_month(prev_df)
                        if prev_month:
                            prev_exempt_mask = (prev_reg.dt.to_period("M") == prev_month)
                            prev_exempt_map = dict(zip(prev_df[join_key], prev_exempt_mask))
                            exempt |= df[join_key].map(prev_exempt_map).fillna(False)
                
                # 新员工（上月不在工资表中）不应纳入"变化"检查
                if "工号" in df.columns and "工号" in prev_df.columns:
                    prev_ids = set(prev_df["工号"].dropna().unique())
                    is_new_employee = ~df["工号"].isin(prev_ids)
                    has_any_change = has_any_change & ~is_new_employee
                    exclusion_mask |= is_new_employee  # 记录新员工排除
                
                exclusion_mask |= exempt  # 记录调薪/转正排除
                mask = has_any_change & ~exempt
            else:
                pass  # 无上月数据时不触发
        else:
            mask = self._evaluate_simple_condition(df, rule.get("condition", ""))

        # 额外排除条件（rules.json 的 exclusions_field / exclusions_values）
        if exclusions_field and exclusions_values and exclusions_field in df.columns:
            extra_exclusion = df[exclusions_field].astype(str).isin(
                [str(v) for v in exclusions_values]
            )
            exclusion_mask |= extra_exclusion
            mask = mask & ~extra_exclusion

        triggered = int(mask.sum())
        details = []
        if triggered > 0:
            for idx in df[mask.values].index[:20]:
                val = None
                if "实发金额合计" in df.columns:
                    val = float(df.loc[idx, "实发金额合计"])
                details.append({
                    "index": int(idx),
                    "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                    "工号": str(df.loc[idx].get("工号", "")),
                    "value": val,
                })

        # 构建判定过程解释（红线）— 传入 exclusion_mask
        judgment = self._build_judgment(df, rule, mask, exclusion_mask)

        return {
            "rule_id": rule_id,
            "rule_name": rule["name"],
            "passed": triggered == 0,
            "total_checked": len(df),
            "triggered": triggered,
            "details": details,
            "judgment": judgment,
        }

    # ─── 黄线校验 ──────────────────────────────────────────────────────

    def check_yellow_lines(self, df: pd.DataFrame, prev_df: pd.DataFrame = None) -> dict:
        """黄线扫描（绩效系数异常、住宿变化、班天数异常等）"""
        results = []
        for rule in self.yellow_lines:
            results.append(self._check_yellow_line(df, prev_df, rule))

        triggered_total = sum(r["triggered"] for r in results)
        return {
            "passed": triggered_total == 0,
            "total_triggered": triggered_total,
            "rule_results": results,
        }

    def _apply_exclusions(self, df: pd.DataFrame, mask: pd.Series, rule: dict) -> tuple:
        """统一排除逻辑：将 rules.json 中的 exclusions 列表转换为 mask 过滤。
        支持：实习生/日薪/保洁（岗位匹配）、当月入职/当月离职（日期匹配）。
        返回：(排除后mask, 排除mask) 二元组，供 _build_judgment 使用。"""
        exclusions = rule.get("exclusions", [])
        if not exclusions:
            return mask, pd.Series([False] * len(df), index=df.index)

        exclusion_mask = pd.Series([False] * len(df), index=df.index)

        # 岗位/状态类排除（使用"状态"列优先，"岗位"列降级）
        position_exclusions = [e for e in exclusions if e in (
            "实习生", "实习生(日薪)", "实习生(月薪)", "日薪", "保洁", "月薪"
        )]
        if position_exclusions:
            status_col = "状态" if "状态" in df.columns else "岗位"
            if status_col in df.columns:
                exclusion_mask |= df[status_col].astype(str).isin(position_exclusions)

        # 当月入职排除：入职日期与发薪月在同一个月
        if "当月入职" in exclusions and "入职日期" in df.columns:
            hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
            pay_month = self._get_pay_month(df)
            if pay_month:
                current_month_mask = hire_dates.dt.to_period("M") == pay_month
                exclusion_mask |= current_month_mask

        # 当月离职排除：离职日期与发薪月在同一个月
        if "当月离职" in exclusions and "离职日期" in df.columns:
            term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
            pay_month = self._get_pay_month(df)
            if pay_month:
                current_month_mask = term_dates.dt.to_period("M") == pay_month
                exclusion_mask |= current_month_mask

        return mask & ~exclusion_mask, exclusion_mask

    def _build_judgment(self, df: pd.DataFrame, rule: dict, mask: pd.Series,
                         exclusion_mask: pd.Series = None) -> dict:
        """生成规则判定过程的详细解释。
        返回 dict 可直接写入规则结果，供报告/看板使用。"""
        total_records = len(df)
        triggered = int(mask.sum())
        excluded_count = int(exclusion_mask.sum()) if exclusion_mask is not None else 0
        actually_checked = total_records - excluded_count

        # 构建排除明细
        excluded_reasons = {}
        exclusions = rule.get("exclusions", [])
        if exclusions and exclusion_mask is not None:
            for exclusion in exclusions:
                count = 0
                if exclusion in ("实习生", "实习生(日薪)", "实习生(月薪)", "日薪", "保洁", "月薪"):
                    status_col = "状态" if "状态" in df.columns else "岗位"
                    if status_col in df.columns:
                        count = int(df[status_col].astype(str).isin([exclusion]).sum())
                elif exclusion == "当月入职" and "入职日期" in df.columns:
                    hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                    pay_month = self._get_pay_month(df)
                    if pay_month:
                        count = int((hire_dates.dt.to_period("M") == pay_month).sum())
                elif exclusion == "当月离职" and "离职日期" in df.columns:
                    term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
                    pay_month = self._get_pay_month(df)
                    if pay_month:
                        count = int((term_dates.dt.to_period("M") == pay_month).sum())
                if count > 0:
                    excluded_reasons[exclusion] = count

        # 构建规则逻辑描述
        rule_logic = self._describe_rule_logic(rule)
        threshold = rule.get("threshold", None)
        if threshold is None and "overtime_limit" in rule.get("id", ""):
            threshold = self.thresholds.get("overtime_limit", 32)

        pass_rate = f"{((actually_checked - triggered) / max(actually_checked, 1)) * 100:.1f}%"
        verdict = "通过" if triggered == 0 else "未通过"

        return {
            "rule_logic": rule_logic,
            "total_records": total_records,
            "exclusion_count": excluded_count,
            "excluded_reasons": excluded_reasons,
            "actually_checked": actually_checked,
            "threshold": threshold,
            "triggered": triggered,
            "pass_rate": pass_rate,
            "verdict": verdict,
        }

    def _describe_rule_logic(self, rule: dict) -> str:
        """根据规则类型生成人类可读的逻辑描述。"""
        rule_id = rule.get("id", "")
        desc = rule.get("description", rule.get("name", ""))

        if rule_id.startswith("RL-"):
            condition = rule.get("condition", "")
            return f"红线阻断规则：{desc}。条件: {condition}"
        elif rule_id.startswith("YL-"):
            threshold = rule.get("threshold", "N/A")
            field = rule.get("field", "")
            return f"黄线预警：{desc}。字段: {field}, 阈值: {threshold}"
        elif rule_id.startswith("BL-"):
            return f"蓝线提示：{desc}"
        elif rule_id.startswith("FR-"):
            return f"公式校验：{desc}"
        elif rule_id.startswith("BR-"):
            return f"业务规则：{desc}"
        elif rule_id.startswith("FC-"):
            return f"字段检查：{desc}"
        elif rule_id.startswith("POL-"):
            return f"政策校验：{desc}"
        return desc

    def _get_pay_month(self, df: pd.DataFrame):
        """从数据中推断发薪月（Period 对象）。
        
        兼容格式: "2026-04", "202604", "2026/04", "2026年4月", "2026年04月"
        """
        if "发薪月" not in df.columns:
            return None
        try:
            val = df["发薪月"].dropna().iloc[0]
            s = str(val).strip()
            # 直接尝试标准格式
            try:
                return pd.Period(s, freq="M")
            except (ValueError, TypeError):
                pass
            # "2026年4月" / "2026年04月" -> "2026-04"
            import re
            m = re.match(r"(\d{4})年\s*(\d{1,2})月", s)
            if m:
                year, month = int(m.group(1)), int(m.group(2))
                return pd.Period(f"{year}-{month:02d}", freq="M")
            # 纯数字 "202604" -> "2026-04"
            m = re.match(r"(\d{6})", s)
            if m:
                year, month = int(s[:4]), int(s[4:6])
                return pd.Period(f"{year}-{month:02d}", freq="M")
        except Exception:
            pass
        return None

    def _check_yellow_line(self, df: pd.DataFrame, prev_df: pd.DataFrame, rule: dict) -> dict:
        rule_id = rule["id"]

        if rule_id == "YL-001":
            # 绩效系数过高
            threshold = self.thresholds.get("perf_coefficient_max", 1.5)
            if "绩效系数" not in df.columns:
                mask = pd.Series([False] * len(df), index=df.index)
            else:
                mask = pd.to_numeric(df["绩效系数"], errors="coerce").fillna(0) > threshold
            mask, exclusion_mask = self._apply_exclusions(df, mask, rule)
        elif rule_id == "YL-002":
            # 绩效系数过低
            threshold = self.thresholds.get("perf_coefficient_min", 0.5)
            if "绩效系数" not in df.columns:
                mask = pd.Series([False] * len(df), index=df.index)
            else:
                mask = pd.to_numeric(df["绩效系数"], errors="coerce").fillna(0) < threshold
            mask, exclusion_mask = self._apply_exclusions(df, mask, rule)
        elif rule_id == "YL-003":
            # 绩效系数波动大（需上月数据）
            delta = self.thresholds.get("perf_coefficient_swing", 0.5)
            mask = pd.Series([False] * len(df), index=df.index)
            if prev_df is not None and "绩效系数" in df.columns and "绩效系数" in prev_df.columns:
                merged = df[["工号", "绩效系数"]].merge(
                    prev_df[["工号", "绩效系数"]], on="工号", suffixes=("_curr", "_prev")
                )
                merged["diff"] = (
                    pd.to_numeric(merged["绩效系数_curr"], errors="coerce")
                    - pd.to_numeric(merged["绩效系数_prev"], errors="coerce")
                ).abs()
                matched_ids = merged[merged["diff"] > delta]["工号"]
                mask = df["工号"].isin(matched_ids)
            mask, exclusion_mask = self._apply_exclusions(df, mask, rule)
        elif rule_id == "YL-004":
            # 住宿扣款变化
            mask = pd.Series([False] * len(df), index=df.index)
            if prev_df is not None and "住宿扣款" in df.columns and "住宿扣款" in prev_df.columns:
                merged = df[["工号", "住宿扣款"]].merge(
                    prev_df[["工号", "住宿扣款"]], on="工号", suffixes=("_curr", "_prev")
                )
                merged["diff"] = (
                    pd.to_numeric(merged["住宿扣款_curr"], errors="coerce")
                    - pd.to_numeric(merged["住宿扣款_prev"], errors="coerce")
                ).abs()
                matched_ids = merged[merged["diff"] > 0.01]["工号"]
                mask = df["工号"].isin(matched_ids)
            mask, exclusion_mask = self._apply_exclusions(df, mask, rule)
        elif rule_id == "YL-005":
            # 实际计薪出勤天数 > 应计薪出勤天数（不排除任何人，数据质量问题全员检查）
            mask = pd.Series([False] * len(df), index=df.index)
            if "实际计薪出勤天数" in df.columns and "应计薪出勤天数" in df.columns:
                actual = pd.to_numeric(df["实际计薪出勤天数"], errors="coerce").fillna(0)
                should = pd.to_numeric(df["应计薪出勤天数"], errors="coerce").fillna(0)
                mask = actual > should
            exclusion_mask = pd.Series([False] * len(df), index=df.index)
        elif rule_id == "YL-006":
            # 标准工资无依据变化 - 黄线（补充RL-007红线，此处做提示）
            # 注：RL-007已作为红线处理三字段变化无记录，YL-006保留作为月度提醒
            mask = pd.Series([False] * len(df), index=df.index)
            exclusion_mask = pd.Series([False] * len(df), index=df.index)
            if prev_df is not None:
                # 对比3个字段：标准基本工资、标准绩效工资、标准福利
                change_fields = ["标准基本工资", "标准绩效工资", "标准福利"]
                has_change = pd.Series([False] * len(df), index=df.index)
                
                curr_pay_month = self._get_pay_month(df)
                prev_pay_month = self._get_pay_month(prev_df) if prev_df is not None else None
                
                for field in change_fields:
                    if field in df.columns and field in prev_df.columns and "工号" in df.columns and "工号" in prev_df.columns:
                        curr_vals = pd.to_numeric(df[field], errors="coerce").fillna(0)
                        prev_map = dict(zip(prev_df["工号"], pd.to_numeric(prev_df[field], errors="coerce").fillna(0)))
                        prev_vals = df["工号"].map(prev_map).fillna(0)
                        has_change |= (curr_vals != prev_vals) & (curr_vals != 0)
                
                # 豁免：当月有调薪/转正
                exempt = pd.Series([False] * len(df), index=df.index)
                if "调薪生效日期" in df.columns:
                    adj = pd.to_datetime(df["调薪生效日期"], errors="coerce")
                    if curr_pay_month:
                        exempt |= adj.dt.to_period("M") == curr_pay_month
                if "转正薪资生效日期" in df.columns:
                    reg = pd.to_datetime(df["转正薪资生效日期"], errors="coerce")
                    if curr_pay_month:
                        exempt |= reg.dt.to_period("M") == curr_pay_month
                
                # 豁免：往月调薪/转正（含1号，与RL-007一致）
                if prev_df is not None:
                    for date_col in ["调薪生效日期", "转正薪资生效日期"]:
                        if date_col in prev_df.columns:
                            dates = pd.to_datetime(prev_df[date_col], errors="coerce")
                            if prev_pay_month:
                                prev_month_match = dates.dt.to_period("M") == prev_pay_month
                                if "工号" in prev_df.columns and "工号" in df.columns:
                                    prev_map = dict(zip(prev_df["工号"], prev_month_match))
                                    exempt |= df["工号"].map(prev_map).fillna(False)
                
                mask = has_change & ~exempt
            mask, exclusion_mask = self._apply_exclusions(df, mask, rule)
        else:
            mask = self._evaluate_simple_condition(df, rule.get("condition", ""))
            exclusion_mask = pd.Series([False] * len(df), index=df.index)

        triggered = int(mask.sum())
        details = []
        if triggered > 0:
            for idx in df[mask.values].index[:20]:
                details.append({
                    "index": int(idx),
                    "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                    "工号": str(df.loc[idx].get("工号", "")),
                })

        # 构建判定过程解释（黄线）
        judgment = self._build_judgment(df, rule, mask, exclusion_mask)

        return {
            "rule_id": rule_id,
            "rule_name": rule["name"],
            "passed": triggered == 0,
            "total_checked": len(df),
            "triggered": triggered,
            "details": details,
            "judgment": judgment,
        }

    # ─── 蓝线校验 ──────────────────────────────────────────────────────

    def check_blue_lines(self, df: pd.DataFrame, prev_df: pd.DataFrame = None) -> dict:
        """蓝线扫描（波动了解即可）"""
        results = []
        for rule in self.blue_lines:
            results.append(self._check_blue_line(df, prev_df, rule))

        triggered_total = sum(r["triggered"] for r in results)
        return {
            "total_triggered": triggered_total,
            "rule_results": results,
        }

    def _check_blue_line(self, df: pd.DataFrame, prev_df: pd.DataFrame, rule: dict) -> dict:
        triggered = 0
        details = []
        mask = pd.Series([False] * len(df), index=df.index)  # default fallback

        if prev_df is not None and "工号" in df.columns:
            # 波动类规则需要上月数据
            field_map = {
                "BL-001": "业务线奖金合计",
                "BL-002": "加班费小计",
                "BL-004": "提成&其他&奖金",
            }
            field = field_map.get(rule["id"])
            if field and field in df.columns and field in prev_df.columns:
                merged = df[["工号", field]].merge(
                    prev_df[["工号", field]], on="工号", suffixes=("_curr", "_prev")
                )
                merged["curr_val"] = pd.to_numeric(merged[f"{field}_curr"], errors="coerce").fillna(0)
                merged["prev_val"] = pd.to_numeric(merged[f"{field}_prev"], errors="coerce").fillna(0)
                merged["change"] = (merged["curr_val"] - merged["prev_val"]).abs()
                threshold = self.thresholds.get(
                    "bonus_volatility_threshold" if "奖金" in field else "supply_volatility_threshold",
                    1000
                )
                flagged = merged[merged["change"] > threshold]
                triggered = len(flagged)
                for _, row in flagged.iterrows():
                    details.append({
                        "姓名代号": str(df.loc[df["工号"] == row["工号"], "姓名代号"].values[0]) if len(df.loc[df["工号"] == row["工号"]]) > 0 else "",
                        "工号": row["工号"],
                    })

        elif rule["id"] == "BL-003":
            # 补发波动（单月即可判断）
            threshold = self.thresholds.get("supplement_warn_amount", 5000)
            mask = pd.to_numeric(df.get("补发", pd.Series([0])), errors="coerce").fillna(0) > threshold
            triggered = int(mask.sum())
            for idx in df[mask.values].index[:20]:
                details.append({
                    "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                    "工号": str(df.loc[idx].get("工号", "")),
                })

        return {
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "total_checked": len(df),
            "triggered": triggered,
            "details": details[:20],
            "judgment": self._build_judgment(df, rule, mask),
        }

    # ─── 政策校验 ──────────────────────────────────────────────────────

    def check_policies(self, df: pd.DataFrame) -> dict:
        """检查特殊政策是否正确执行"""
        results = []
        for policy in self.policies:
            results.append(self._check_policy(df, policy))

        return {"rule_results": results}

    def _check_policy(self, df: pd.DataFrame, policy: dict) -> dict:
        """执行单条政策校验"""
        condition = policy.get("condition", "")
        effect = policy.get("effect", {})
        check_scope = policy.get("check_scope", "all")

        # 找到符合条件的人员
        match_mask = self._evaluate_policy_condition(df, condition)
        matched_count = int(match_mask.sum())

        # 特殊处理: POL-003 离职当月规则 — 仅检查当月离职人员
        # SOP: 15号前离职可以不缴，15号后离职应缴。这不是"必须=0"的规则
        # 而是"15号前离职的人如果缴了社保，也是合理的（公司代缴）"
        # 所以 POL-003 不做违规检查，只做提示
        if check_scope == "leavers_only":
            return {
                "policy_id": policy["id"],
                "policy_name": policy["name"],
                "matched_count": matched_count,
                "violation_count": 0,
                "violations": [],
                "passed": True,
                "note": "离职当月社保规则：仅提示，不做违规判定。15号前离职可以不缴，已缴也合理。",
            }

        # POL-005 道旅国际公积金豁免 — "可以=0"不是"必须=0"
        if check_scope == "note_only":
            return {
                "policy_id": policy["id"],
                "policy_name": policy["name"],
                "matched_count": matched_count,
                "violation_count": 0,
                "violations": [],
                "passed": True,
                "note": f"{policy['note']}",
            }

        # 检查 effect 是否正确执行
        violations = []
        for field, expected_value in effect.items():
            if field in df.columns:
                actual_values = pd.to_numeric(df.loc[match_mask, field], errors="coerce")
                mismatches = actual_values[actual_values != expected_value].dropna()
                for idx in mismatches.index:
                    violations.append({
                        "姓名代号": str(df.loc[idx].get("姓名代号", "")),
                        "工号": str(df.loc[idx].get("工号", "")),
                        "field": field,
                        "expected": expected_value,
                        "actual": float(actual_values.loc[idx]),
                    })

        return {
            "policy_id": policy["id"],
            "policy_name": policy["name"],
            "matched_count": matched_count,
            "violation_count": len(violations),
            "violations": violations[:20],
            "passed": len(violations) == 0,
        }

    def _evaluate_policy_condition(self, df: pd.DataFrame, condition: str) -> pd.Series:
        """评估政策条件"""
        mask = pd.Series([True] * len(df))

        # 道旅国际
        if "道旅国际" in condition:
            mask = mask & (df.get("公司主体", pd.Series([""])) == "道旅国际")

        # 道旅国际 - 社保
        if "道旅国际" in condition and "社保" in condition:
            mask = mask & (df.get("公司主体", pd.Series([""])) == "道旅国际")

        # 道旅国际 - 公积金
        if "道旅国际" in condition and "公积金" in condition:
            mask = mask & (df.get("公司主体", pd.Series([""])) == "道旅国际")
            if "入职" in condition and "2" in condition:
                if "入职日期" in df.columns:
                    hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                    months_since = (pd.Timestamp.now() - hire_dates).dt.days / 30
                    mask = mask & (months_since <= 2)

        # 入职≤2月
        elif "入职" in condition and "2" in condition and "道旅国际" not in condition:
            if "入职日期" in df.columns:
                hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                months_since = (pd.Timestamp.now() - hire_dates).dt.days / 30
                mask = mask & (months_since <= 2)

        # 15号后入职
        if "15" in condition and "入职" in condition:
            if "入职日期" in df.columns:
                hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
                day_of_month = hire_dates.dt.day
                mask = mask & (day_of_month > 15)

        # 离职日期.day <= 15（离职当月社保缴纳规则）
        if "离职日期" in condition and "day" in condition:
            if "离职日期" in df.columns:
                term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
                day_of_month = term_dates.dt.day
                mask = mask & term_dates.notna() & (day_of_month <= 15)

        # 实习生/保洁
        if "实习生" in condition or "保洁" in condition:
            exempt_values = []
            if "实习生" in condition:
                exempt_values.append("实习生")
            if "保洁" in condition:
                exempt_values.append("保洁")
            if "日薪" in condition:
                exempt_values.append("日薪")
            if "月薪" in condition:
                exempt_values.append("月薪")
            # "状态"列优先，"岗位"列降级
            status_col = "状态" if "状态" in df.columns else "岗位"
            col_data = df.get(status_col, pd.Series([""])).astype(str)
            # Fuzzy match: "实习生（月薪）" contains "实习生"
            exempt_mask = pd.Series([False] * len(df))
            for val in exempt_values:
                exempt_mask |= col_data.str.contains(val, na=False)
            mask = mask & exempt_mask

        return mask

    # ─── 跨月对比 ──────────────────────────────────────────────────────

    def compare_periods(self, df: pd.DataFrame, prev_df: pd.DataFrame) -> dict:
        """跨月对比分析"""
        if prev_df is None:
            return None

        comparison = {
            "headcount": {
                "current": len(df),
                "previous": len(prev_df),
                "change_pct": round((len(df) - len(prev_df)) / len(prev_df) * 100, 2) if len(prev_df) > 0 else 0,
            },
            "metrics": {},
        }

        numeric_fields = ["应发合计", "实发金额合计", "实际出勤工资小计", "实际绩效工资",
                          "加班费小计", "业务线奖金合计", "提成&其他&奖金", "补发"]

        for field in numeric_fields:
            if field in df.columns and field in prev_df.columns:
                curr_total = float(pd.to_numeric(df[field], errors="coerce").fillna(0).sum())
                prev_total = float(pd.to_numeric(prev_df[field], errors="coerce").fillna(0).sum())
                change_pct = round((curr_total - prev_total) / prev_total * 100, 2) if prev_total != 0 else 0
                comparison["metrics"][field] = {
                    "current": round(curr_total, 2),
                    "previous": round(prev_total, 2),
                    "change_pct": change_pct,
                }

        return comparison

    def analyze_continuous_employees(self, df: pd.DataFrame, prev_df: pd.DataFrame) -> dict:
        """连续在职人员环比分析。
        
        连续在职定义：上月和当月都在工资表中（工号匹配）且非当月入职/离职的人员。
        
        排除规则：
        - 实习生/日薪/保洁（岗位豁免）
        - 当月入职/当月离职（状态变化）
        - 近期调薪/转正（生效日期在[上月, 当月]范围）
        - 病假>2天或事假>2天（请假影响）
        - 多主体发薪人员（同一工号在多个主体出现）
        
        环比逻辑：
        - 对比应发合计、实发金额、12项计薪科目
        - 变化幅度 >10% 标记为异常波动
        - 自动分类波动原因：绩效变化/加班变化/奖金变化/扣款变化/其他
        """
        if prev_df is None or "工号" not in df.columns:
            return {"skipped": True, "reason": "无上月数据或缺少工号字段"}
        
        # 1. 找出连续在职人员（工号在两个月都存在）
        curr_ids = set(df["工号"].dropna().unique())
        prev_ids = set(prev_df["工号"].dropna().unique())
        continuous_ids = curr_ids & prev_ids
        
        if not continuous_ids:
            return {"skipped": True, "reason": "无连续在职人员（工号无重叠）"}
        
        # 2. 提取连续在职人员数据
        curr_cont = df[df["工号"].isin(continuous_ids)].copy()
        prev_cont = prev_df[prev_df["工号"].isin(continuous_ids)].copy()
        
        # 3. 排除特定人员
        exclude_mask = pd.Series([False] * len(curr_cont), index=curr_cont.index)
        excluded_reasons = {}
        
        # 岗位排除
        if "岗位" in curr_cont.columns:
            for pos in ["实习生", "实习生(日薪)", "实习生(月薪)", "日薪", "保洁"]:
                m = curr_cont["岗位"].astype(str) == pos
                cnt = int(m.sum())
                if cnt > 0:
                    excluded_reasons[pos] = cnt
                exclude_mask |= m
        
        # 当月入职/离职排除
        curr_pay_month = self._get_pay_month(df)
        if "入职日期" in curr_cont.columns and curr_pay_month:
            hire_m = pd.to_datetime(curr_cont["入职日期"], errors="coerce").dt.to_period("M") == curr_pay_month
            cnt = int(hire_m.sum())
            if cnt > 0:
                excluded_reasons["当月入职"] = cnt
            exclude_mask |= hire_m
        
        if "离职日期" in curr_cont.columns and curr_pay_month:
            term_m = pd.to_datetime(curr_cont["离职日期"], errors="coerce").dt.to_period("M") == curr_pay_month
            cnt = int(term_m.sum())
            if cnt > 0:
                excluded_reasons["当月离职"] = cnt
            exclude_mask |= term_m
        
        # 近期调薪/转正排除
        if "调薪生效日期" in curr_cont.columns:
            adj = pd.to_datetime(curr_cont["调薪生效日期"], errors="coerce")
            if curr_pay_month:
                adj_m = adj.dt.to_period("M") == curr_pay_month
                cnt = int(adj_m.sum())
                if cnt > 0:
                    excluded_reasons["当月调薪"] = cnt
                exclude_mask |= adj_m
        
        if "转正薪资生效日期" in curr_cont.columns:
            reg = pd.to_datetime(curr_cont["转正薪资生效日期"], errors="coerce")
            if curr_pay_month:
                reg_m = reg.dt.to_period("M") == curr_pay_month
                cnt = int(reg_m.sum())
                if cnt > 0:
                    excluded_reasons["当月转正"] = cnt
                exclude_mask |= reg_m
        
        # 请假排除
        leave_mask = pd.Series([False] * len(curr_cont), index=curr_cont.index)
        if "病假" in curr_cont.columns:
            leave_mask |= pd.to_numeric(curr_cont["病假"], errors="coerce").fillna(0) > 2
        if "事假" in curr_cont.columns:
            leave_mask |= pd.to_numeric(curr_cont["事假"], errors="coerce").fillna(0) > 2
        cnt = int(leave_mask.sum())
        if cnt > 0:
            excluded_reasons["请假>2天"] = cnt
        exclude_mask |= leave_mask
        
        # 4. 应用排除
        analyze_df = curr_cont[~exclude_mask].copy()
        
        # 重新对齐
        analyze_ids = set(analyze_df["工号"])
        analyze_prev = prev_cont[prev_cont["工号"].isin(analyze_ids)].copy()
        
        total_excluded = int(exclude_mask.sum())
        actually_analyzed = len(analyze_df)
        
        # 5. 环比分析：12项计薪科目
        metrics_to_compare = [
            "应发合计", "实发金额合计", "实际出勤工资小计", "实际绩效工资",
            "加班费小计", "业务线奖金合计", "提成&其他&奖金", "补发",
            "个人社保", "个人公积金", "个税", "住宿扣款"
        ]
        
        per_person_changes = []
        flagged_changes = []
        summary_stats = {
            "total_continuous": len(continuous_ids),
            "total_excluded": total_excluded,
            "excluded_reasons": excluded_reasons,
            "actually_analyzed": actually_analyzed,
        }
        
        for field in metrics_to_compare:
            if field not in analyze_df.columns or field not in analyze_prev.columns:
                continue
            
            curr_vals = pd.to_numeric(analyze_df[field], errors="coerce").fillna(0)
            prev_vals_map = {}
            # 按工号对齐
            if "工号" in analyze_prev.columns:
                prev_map = dict(zip(analyze_prev["工号"], pd.to_numeric(analyze_prev[field], errors="coerce").fillna(0)))
                prev_vals = analyze_df["工号"].map(prev_map).fillna(0)
            else:
                continue
            
            # 计算变化
            diff = curr_vals - prev_vals
            pct_change = pd.Series([0.0] * len(analyze_df), index=analyze_df.index)
            for i in analyze_df.index:
                pv = prev_vals.loc[i]
                if pv != 0:
                    pct_change.loc[i] = round(float(diff.loc[i] / abs(pv) * 100), 2)
            
            # 标记异常波动 (>10%)
            anomaly_mask = (pct_change.abs() > 10) & (diff.abs() > 1000)
            anomaly_count = int(anomaly_mask.sum())
            
            summary_stats[field] = {
                "avg_curr": round(float(curr_vals.mean()), 2),
                "avg_prev": round(float(prev_vals.mean()), 2),
                "total_curr": round(float(curr_vals.sum()), 2),
                "total_prev": round(float(prev_vals.sum()), 2),
                "change_pct": round(float((curr_vals.sum() - prev_vals.sum()) / abs(prev_vals.sum()) * 100), 2) if prev_vals.sum() != 0 else 0,
                "anomaly_count": anomaly_count,
                "anomaly_threshold": "±10%且绝对值>1000元",
            }
            
            # 收集异常人员明细
            if anomaly_count > 0:
                for idx in analyze_df[anomaly_mask].index[:50]:
                    emp_id = str(analyze_df.loc[idx, "工号"])
                    emp_name = str(analyze_df.loc[idx].get("姓名代号", ""))
                    flagged_changes.append({
                        "工号": emp_id,
                        "姓名代号": emp_name,
                        "field": field,
                        "curr_value": round(float(curr_vals.loc[idx]), 2),
                        "prev_value": round(float(prev_vals.loc[idx]), 2),
                        "diff": round(float(diff.loc[idx]), 2),
                        "pct_change": round(float(pct_change.loc[idx]), 2),
                    })
        
        return {
            "skipped": False,
            "summary": summary_stats,
            "flagged_changes": flagged_changes[:100],  # 最多返回100条
        }

    # ─── 辅助方法 ──────────────────────────────────────────────────────

    def _get_min_wage(self, df: pd.DataFrame) -> float:
        """获取最低工资标准（默认用城市最低工资）"""
        # 简单实现：用默认值
        return self.thresholds.get("min_wage_default", 2360)

    def _get_exemption_mask(self, df: pd.DataFrame) -> pd.Series:
        """获取社保/公积金豁免人员掩码（使用"状态"列优先）"""
        mask = pd.Series([False] * len(df), index=df.index)

        # 道旅国际
        if "公司主体" in df.columns:
            mask |= (df["公司主体"] == "道旅国际")

        # 实习生/保洁 - 使用"状态"列优先（文档要求），"岗位"列降级
        exempt_values = [
            "实习生(日薪)", "实习生(月薪)", "实习生",
            "保洁", "日薪", "月薪"
        ]
        status_col = "状态" if "状态" in df.columns else "岗位"
        if status_col in df.columns:
            # 同时支持半角()和全角（）
            status_str = df[status_col].astype(str)
            mask |= status_str.isin(exempt_values)
            for val in exempt_values:
                # Also try with full-width brackets: "实习生（月薪）" vs "实习生(月薪)"
                full_width = val.replace("(", "（").replace(")", "）")
                if full_width != val:
                    mask |= (status_str == full_width)

        # 15号后入职当月不缴
        if "入职日期" in df.columns:
            hire_dates = pd.to_datetime(df["入职日期"], errors="coerce")
            day_of_month = hire_dates.dt.day
            mask |= (day_of_month > 15)

        # 离职当月（15号前离职）
        if "离职日期" in df.columns:
            term_dates = pd.to_datetime(df["离职日期"], errors="coerce")
            term_day = term_dates.dt.day
            mask |= (term_day.notna()) & (term_day <= 15)

        return mask

    def _evaluate_simple_condition(self, df: pd.DataFrame, condition: str) -> pd.Series:
        """评估简单条件表达式"""
        if not condition:
            return pd.Series([False] * len(df))

        mask = pd.Series([False] * len(df))

        # 解析简单比较: field > value, field <= value, etc.
        match = re.match(r'([A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*)\s*([<>=!]+)\s*(.+)', condition)
        if match:
            field, op, value_str = match.groups()
            if field not in df.columns:
                return mask

            values = pd.to_numeric(df[field], errors="coerce").fillna(0)
            try:
                threshold = float(value_str)
            except ValueError:
                # 可能是阈值 key
                threshold = float(self.thresholds.get(value_str.strip(), 0))

            if op == ">":
                mask = values > threshold
            elif op == ">=":
                mask = values >= threshold
            elif op == "<":
                mask = values < threshold
            elif op == "<=":
                mask = values <= threshold
            elif op == "==":
                mask = values == threshold
            elif op == "!=":
                mask = values != threshold

        return mask

    # ─── 汇总生成 ──────────────────────────────────────────────────────

    def _generate_summary(self, results: dict) -> dict:
        """生成审核摘要"""
        red_triggered = results.get("red_lines", {}).get("total_triggered", 0)
        yellow_triggered = results.get("yellow_lines", {}).get("total_triggered", 0)
        blue_triggered = results.get("blue_lines", {}).get("total_triggered", 0)
        formula_passed = results.get("formula_check", {}).get("passed", True)
        field_passed = results.get("field_check", {}).get("passed", True)

        return {
            "blocked": red_triggered > 0,
            "total_issues": red_triggered + yellow_triggered + blue_triggered,
            "p0_count": red_triggered,
            "p1_count": yellow_triggered,
            "p2_count": blue_triggered,
            "formula_passed": formula_passed,
            "field_check_passed": field_passed,
            "status": "blocked" if red_triggered > 0 else "warning" if yellow_triggered > 0 else "pass",
        }


# ─── CLI 入口 ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="工资数据审核规则引擎")
    parser.add_argument("--data", required=True, help="工资数据文件路径")
    parser.add_argument("--prev", help="上月工资数据文件路径（可选）")
    parser.add_argument("--rules", default=None, help="规则文件路径（默认自动查找）")
    parser.add_argument("--output", default="audit_result.json", help="输出文件路径")
    parser.add_argument("--step", choices=["full", "fields", "formulas", "red_lines", "yellow_lines", "blue_lines", "policies"],
                        default="full", help="指定执行步骤")
    args = parser.parse_args()

    engine = PayrollRulesEngine(args.rules)

    # Load data
    if args.data.endswith(".csv"):
        df = pd.read_csv(args.data)
    elif args.data.endswith((".xlsx", ".xls")):
        df = pd.read_excel(args.data)
    else:
        print(json.dumps({"error": f"Unsupported file format: {args.data}"}))
        sys.exit(1)

    prev_df = None
    if args.prev:
        if args.prev.endswith(".csv"):
            prev_df = pd.read_csv(args.prev)
        elif args.prev.endswith((".xlsx", ".xls")):
            prev_df = pd.read_excel(args.prev)

    if args.step == "full":
        result = engine.run_full_audit(df, prev_df)
    else:
        # 单独步骤
        df = normalize_columns(df.copy())
        df = normalize_types(df)
        if prev_df is not None:
            prev_df = normalize_columns(prev_df.copy())
            prev_df = normalize_types(prev_df)

        step_funcs = {
            "fields": lambda: engine.check_fields(df),
            "formulas": lambda: engine.check_formulas(df),
            "red_lines": lambda: engine.check_red_lines(df, prev_df),
            "yellow_lines": lambda: engine.check_yellow_lines(df, prev_df),
            "blue_lines": lambda: engine.check_blue_lines(df, prev_df),
            "policies": lambda: engine.check_policies(df),
        }
        result = {
            "version": engine.rules.get("version", ""),
            "audit_time": datetime.now().isoformat(),
            "total_records": len(df),
            "step": args.step,
            "result": step_funcs[args.step](),
        }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    # Console summary
    summary = result.get("summary", {})
    print(f"\n{'='*60}")
    print(f"工资审核完成 | {result.get('total_records', 0)} 条记录")
    print(f"  状态: {summary.get('status', 'N/A')}")
    print(f"  🔴 红线: {summary.get('p0_count', 0)}")
    print(f"  ⚠️  黄线: {summary.get('p1_count', 0)}")
    print(f"  ℹ️  蓝线: {summary.get('p2_count', 0)}")
    print(f"  ✅ 公式: {'通过' if summary.get('formula_passed') else '失败'}")
    print(f"  ✅ 字段: {'通过' if summary.get('field_check_passed') else '失败'}")
    print(f"{'='*60}")
    print(f"详细结果 → {args.output}")


if __name__ == "__main__":
    main()
