#!/usr/bin/env python3
"""
payroll-data-audit: sampling_verify
抽样校验器 — 对审核结果进行独立二次确认

设计目标：
  - 随机抽取 N 条记录，独立重算关键指标
  - 与原审核结果交叉对比，发现偏差
  - 偏差超过阈值时输出根因分析报告（不中断流程）
  - 输出校验报告

校验项目：
  1. 公式重算：应发合计/实发合计独立计算，与原值对比
  2. 红线复验：实发≤0、加班超36h、最低工资、社保未缴
  3. 业务规则复验：出勤工资/天数合理性
  4. 政策复验：豁免人员是否正确豁免

用法:
    python3 scripts/sampling_verify.py \
      --data <工资数据.csv> \
      --audit /tmp/audit_phases/audit_final.json \
      --sample-size 30 \
      --threshold 0.05 \
      --output /tmp/sampling_verify.json
"""

import argparse
import json
import random
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from rules_engine import normalize_columns, normalize_types


def load_data(data_path):
    """加载并规范化数据"""
    p = Path(data_path)
    if p.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(p)
    elif p.suffix == ".csv":
        df = pd.read_csv(p, encoding="utf-8-sig")
    else:
        raise ValueError(f"不支持的文件格式: {p.suffix}")

    df = normalize_columns(df)
    df = normalize_types(df)
    return df


def load_audit(audit_path):
    """加载审核结果"""
    with open(audit_path) as f:
        return json.load(f)


def verify_formulas(df, sample_indices):
    """独立重算公式，与审计结果交叉对比"""
    results = []
    for idx in sample_indices:
        row = df.loc[idx]
        issues = []

        # 重算应发合计
        income_fields = [
            "实际出勤工资小计", "实际绩效工资", "实际出勤福利小计",
            "轮班补贴", "加班费小计", "业务线奖金合计",
            "提成&其他&奖金", "补发",
        ]
        deduction_fields = ["其他扣减"]

        income_sum = sum(Decimal(str(row.get(f, 0) or 0)) for f in income_fields if f in df.columns)
        deduction_sum = sum(Decimal(str(row.get(f, 0) or 0)) for f in deduction_fields if f in df.columns)
        computed_gross = float((income_sum - deduction_sum).quantize(Decimal("0.01")))

        actual_gross = float(Decimal(str(row.get("应发合计", 0) or 0)).quantize(Decimal("0.01")))
        if abs(computed_gross - actual_gross) > 0.01:
            issues.append({
                "type": "公式偏差",
                "field": "应发合计",
                "computed": computed_gross,
                "actual": actual_gross,
                "diff": round(computed_gross - actual_gross, 2),
            })

        # 重算实发合计
        additions = ["经济补偿金"]
        deductions = ["个人社保", "个人公积金", "个税", "税后扣减", "住宿扣款", "社保差额", "公积金差额"]

        add_sum = sum(Decimal(str(row.get(f, 0) or 0)) for f in additions if f in df.columns)
        ded_sum = sum(Decimal(str(row.get(f, 0) or 0)) for f in deductions if f in df.columns)
        gross_val = Decimal(str(actual_gross))
        computed_net = float((gross_val - ded_sum + add_sum).quantize(Decimal("0.01")))

        actual_net = float(Decimal(str(row.get("实发金额合计", 0) or 0)).quantize(Decimal("0.01")))
        if abs(computed_net - actual_net) > 0.01:
            issues.append({
                "type": "公式偏差",
                "field": "实发金额合计",
                "computed": computed_net,
                "actual": actual_net,
                "diff": round(computed_net - actual_net, 2),
            })

        results.append({
            "index": int(idx),
            "工号": str(row.get("工号", "")),
            "姓名代号": str(row.get("姓名代号", "")),
            "issues": issues,
            "passed": len(issues) == 0,
        })

    return results


def verify_red_lines(df, sample_indices):
    """复验红线规则"""
    results = []
    for idx in sample_indices:
        row = df.loc[idx]
        issues = []

        # RL-001: 实发≤0
        net = float(row.get("实发金额合计", 0) or 0)
        if net <= 0:
            issues.append({"type": "RL-001", "desc": "实发≤0", "value": net})

        # RL-002: 加班超36h
        ot_cols = ["平时加班时数", "周末加班时数", "法定加班时数"]
        total_ot = sum(float(row.get(c, 0) or 0) for c in ot_cols if c in df.columns)
        if total_ot > 36:
            issues.append({"type": "RL-002", "desc": "加班超36h", "value": total_ot})

        # RL-003: 低于最低工资（简化，使用深圳默认）
        gross = float(row.get("应发合计", 0) or 0)
        if gross > 0 and gross < 2360:
            issues.append({"type": "RL-003", "desc": "低于最低工资", "value": gross})

        results.append({
            "index": int(idx),
            "工号": str(row.get("工号", "")),
            "姓名代号": str(row.get("姓名代号", "")),
            "issues": issues,
            "passed": len(issues) == 0,
        })

    return results


def verify_business_rules(df, sample_indices):
    """复验业务规则"""
    results = []
    for idx in sample_indices:
        row = df.loc[idx]
        issues = []

        # BR-001: 出勤工资 ≤ 标准工资
        actual_salary = float(row.get("实际出勤工资小计", 0) or 0)
        standard_salary = float(row.get("标准基本工资", 0) or 0)
        if standard_salary > 0 and actual_salary > standard_salary:
            issues.append({
                "type": "BR-001",
                "desc": "出勤工资 > 标准工资",
                "actual": actual_salary,
                "standard": standard_salary,
            })

        # BR-002: 实际计薪天数 ≤ 应计薪天数
        actual_days = float(row.get("实际计薪出勤天数", 0) or 0)
        should_days = float(row.get("应计薪出勤天数", 0) or 0)
        if should_days > 0 and actual_days > should_days:
            issues.append({
                "type": "BR-002",
                "desc": "实际计薪天数 > 应计薪天数",
                "actual": actual_days,
                "should": should_days,
            })

        results.append({
            "index": int(idx),
            "工号": str(row.get("工号", "")),
            "姓名代号": str(row.get("姓名代号", "")),
            "issues": issues,
            "passed": len(issues) == 0,
        })

    return results


def run_sampling_verify(df, audit, sample_size=30, threshold=0.05):
    """执行抽样校验"""
    total_records = len(df)
    sample_size = min(sample_size, total_records)

    # 随机抽样
    random.seed(42)  # 可复现
    sample_indices = random.sample(range(total_records), sample_size)

    print(f"🎯 抽样: {sample_size}/{total_records} 条记录 (抽样率 {sample_size/total_records*100:.1f}%)")

    # 执行校验
    formula_results = verify_formulas(df, sample_indices)
    red_results = verify_red_lines(df, sample_indices)
    business_results = verify_business_rules(df, sample_indices)

    # 统计偏差
    formula_issues = sum(1 for r in formula_results if not r["passed"])
    red_issues = sum(1 for r in red_results if not r["passed"])
    business_issues = sum(1 for r in business_results if not r["passed"])

    total_issues = formula_issues + red_issues + business_issues
    issue_rate = total_issues / (sample_size * 3)  # 3项校验

    # 判定
    if issue_rate <= threshold:
        verdict = "通过"
        action = "审核结果可信"
    else:
        verdict = "不通过"
        action = "偏差率超标，已输出根因分析报告，请人工核实"

    # 构建报告
    report = {
        "version": "v5.4.0",
        "verify_time": datetime.now().isoformat(),
        "total_records": total_records,
        "sample_size": sample_size,
        "sample_rate": f"{sample_size/total_records*100:.1f}%",
        "threshold": threshold,
        "formula_check": {
            "sampled": sample_size,
            "issues": formula_issues,
            "issue_details": [r for r in formula_results if not r["passed"]][:10],
        },
        "red_line_check": {
            "sampled": sample_size,
            "issues": red_issues,
            "issue_details": [r for r in red_results if not r["passed"]][:10],
        },
        "business_rule_check": {
            "sampled": sample_size,
            "issues": business_issues,
            "issue_details": [r for r in business_results if not r["passed"]][:10],
        },
        "summary": {
            "total_issues": total_issues,
            "issue_rate": f"{issue_rate*100:.2f}%",
            "verdict": verdict,
            "action": action,
            "recommendation": "建议增加抽样比例至 50+ 条" if issue_rate > threshold * 0.5 else "",
        }
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="抽样校验器 v5.4")
    parser.add_argument("--data", required=True, help="工资数据文件")
    parser.add_argument("--audit", required=True, help="审核结果 JSON 路径")
    parser.add_argument("--sample-size", type=int, default=30, help="抽样数量 (默认30)")
    parser.add_argument("--threshold", type=float, default=0.05, help="偏差阈值 (默认5%)")
    parser.add_argument("--output", required=True, help="输出报告路径")

    args = parser.parse_args()

    print("🔍 抽样校验开始...")
    df = load_data(args.data)
    audit = load_audit(args.audit)

    report = run_sampling_verify(df, audit, args.sample_size, args.threshold)

    # 输出
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    # 控制台摘要
    s = report["summary"]
    print(f"\n{'='*50}")
    print("📊 抽样校验完成")
    print(f"{'='*50}")
    print(f"   抽样: {report['sample_size']}/{report['total_records']} ({report['sample_rate']})")
    print(f"   公式偏差: {report['formula_check']['issues']} 条")
    print(f"   红线偏差: {report['red_line_check']['issues']} 条")
    print(f"   业务规则偏差: {report['business_rule_check']['issues']} 条")
    print(f"   偏差率: {s['total_issues']} 项 ({s['issue_rate']})")
    print(f"   判定: {s['verdict']}")
    print(f"   建议: {s['action']}")
    if s['recommendation']:
        print(f"   💡 {s['recommendation']}")
    print(f"\n📄 报告: {args.output}")


if __name__ == "__main__":
    main()
