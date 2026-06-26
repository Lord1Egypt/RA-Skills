#!/usr/bin/env python3
"""
payroll-data-audit: run_audit
分段审核编排器 — 将完整审核拆分为多个独立阶段，每阶段输出独立 JSON

设计目标：
  - 避免一次性运行导致上下文截断
  - 每阶段可独立执行、独立验证
  - 支持断点续传（某阶段失败后重跑不影响已完成阶段）
  - 最终合并所有阶段结果为完整审核报告

审核阶段划分：
  Phase 1: 数据扫描 + 字段完整性    (轻量, ~1秒)
  Phase 2: 公式校验                  (中等, ~5秒)
  Phase 3: 业务规则 + 政策校验       (中等, ~5秒)
  Phase 4: 红线扫描                  (轻量, ~1秒, P0标记)
  Phase 5: 黄线扫描 + 跨月对比       (较重, ~10秒)
  Phase 6: 蓝线扫描                  (轻量, ~1秒)
  Phase 7: 汇总分析                  (轻量, ~1秒)

用法:
    # 完整分段审核（推荐）
    python3 scripts/run_audit.py \
      --data <本月数据.csv> --prev <上月数据.csv> \
      --output-dir /tmp/audit_phases

    # 单独执行某阶段
    python3 scripts/run_audit.py \
      --data <本月数据.csv> --prev <上月数据.csv> \
      --phase 4 --output-dir /tmp/audit_phases

    # 从断点续传
    python3 scripts/run_audit.py \
      --data <本月数据.csv> --prev <上月数据.csv> \
      --resume --output-dir /tmp/audit_phases
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from rules_engine import PayrollRulesEngine, normalize_columns, normalize_types


# ─── 阶段定义 ─────────────────────────────────────────────────────────

PHASES = [
    {
        "id": 1,
        "name": "数据扫描+字段完整性",
        "key": "phase_1_fields",
        "requires_prev": False,
        "is_gate": False,
    },
    {
        "id": 2,
        "name": "公式校验",
        "key": "phase_2_formulas",
        "requires_prev": False,
        "is_gate": False,
    },
    {
        "id": 3,
        "name": "业务规则+政策校验",
        "key": "phase_3_business_policy",
        "requires_prev": False,
        "is_gate": False,
    },
    {
        "id": 4,
        "name": "红线扫描（P0标记）",
        "key": "phase_4_red_lines",
        "requires_prev": False,
        "is_gate": True,  # 红线触发时停止后续阶段
    },
    {
        "id": 5,
        "name": "黄线扫描+跨月对比",
        "key": "phase_5_yellow_compare",
        "requires_prev": True,
        "is_gate": False,
    },
    {
        "id": 6,
        "name": "蓝线扫描",
        "key": "phase_6_blue_lines",
        "requires_prev": True,
        "is_gate": False,
    },
    {
        "id": 7,
        "name": "汇总分析",
        "key": "phase_7_summary",
        "requires_prev": True,
        "is_gate": False,
    },
]


def load_data(data_path, prev_path=None):
    """加载数据文件，支持 CSV/Excel"""
    p = Path(data_path)
    if p.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(p)
    elif p.suffix == ".csv":
        df = pd.read_csv(p, encoding="utf-8-sig")
    else:
        raise ValueError(f"不支持的文件格式: {p.suffix}")

    prev_df = None
    if prev_path:
        pp = Path(prev_path)
        if pp.suffix in (".xlsx", ".xls"):
            prev_df = pd.read_excel(pp)
        elif pp.suffix == ".csv":
            prev_df = pd.read_csv(pp, encoding="utf-8-sig")

    # 规范化
    df = normalize_columns(df)
    df = normalize_types(df)
    if prev_df is not None:
        prev_df = normalize_columns(prev_df)
        prev_df = normalize_types(prev_df)

    return df, prev_df


def execute_phase(phase, engine, df, prev_df):
    """执行单个审核阶段，返回阶段结果"""
    phase_id = phase["id"]
    phase_name = phase["name"]
    start = time.time()

    result = {
        "phase_id": phase_id,
        "phase_name": phase_name,
        "phase_key": phase["key"],
        "status": "running",
        "started_at": datetime.now().isoformat(),
    }

    try:
        if phase_id == 1:
            result["field_check"] = engine.check_fields(df)

        elif phase_id == 2:
            result["formula_check"] = engine.check_formulas(df)

        elif phase_id == 3:
            result["business_check"] = engine.check_business_rules(df)
            result["policy_check"] = engine.check_policies(df)

        elif phase_id == 4:
            result["red_lines"] = engine.check_red_lines(df)

        elif phase_id == 5:
            result["yellow_lines"] = engine.check_yellow_lines(df, prev_df)
            if prev_df is not None:
                result["comparison"] = engine.compare_periods(df, prev_df)
            else:
                result["comparison"] = {"skipped": True, "reason": "无上月数据"}

        elif phase_id == 6:
            result["blue_lines"] = engine.check_blue_lines(df, prev_df)

        elif phase_id == 7:
            # 汇总阶段需要前面所有阶段的结果
            result["summary"] = engine._generate_summary(result)

        elapsed = time.time() - start
        result["status"] = "completed"
        result["completed_at"] = datetime.now().isoformat()
        result["elapsed_seconds"] = round(elapsed, 2)

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["completed_at"] = datetime.now().isoformat()

    return result


def check_gate(phase_result):
    """检查是否为阻断门（红线阶段）"""
    red = phase_result.get("red_lines", {})
    triggered = red.get("total_triggered", 0)
    return triggered > 0


def generate_summary(all_phases, total_records):
    """生成最终汇总"""
    summary = {
        "version": "v5.4.0",
        "audit_time": datetime.now().isoformat(),
        "total_records": total_records,
        "phases_completed": len(all_phases),
        "phases_total": len(PHASES),
        "phase_results": {},
        "summary": {},
    }

    # 合并各阶段结果
    merged = {
        "field_check": {},
        "formula_check": {},
        "business_check": {},
        "policy_check": {},
        "red_lines": {},
        "yellow_lines": {},
        "blue_lines": {},
        "comparison": None,
    }

    for pr in all_phases:
        if pr["status"] != "completed":
            continue
        key = pr["phase_key"]
        summary["phase_results"][key] = {
            "status": pr["status"],
            "elapsed": pr.get("elapsed_seconds", 0),
        }
        for k in merged:
            if k in pr:
                merged[k] = pr[k]

    # 生成 summary
    engine_summary = {
        "status": "completed",
        "blocked": False,
        "total_records": total_records,
    }

    red = merged.get("red_lines", {})
    red_triggered = red.get("total_triggered", 0)
    if red_triggered > 0:
        engine_summary["blocked"] = True
        engine_summary["status"] = "blocked"
    elif red_triggered == 0:
        yellow = merged.get("yellow_lines", {})
        yellow_triggered = yellow.get("total_triggered", 0) if yellow else 0
        engine_summary["status"] = "warnings" if yellow_triggered > 0 else "clean"

    # 统计
    stats = {"red": red_triggered, "yellow": 0, "blue": 0}
    for yl in merged.get("yellow_lines", {}).get("rule_results", []):
        stats["yellow"] += yl.get("triggered", 0)
    for bl in merged.get("blue_lines", {}).get("rule_results", []):
        stats["blue"] += bl.get("triggered", 0)

    engine_summary["p0_count"] = stats["red"]
    engine_summary["p1_count"] = stats["yellow"]
    engine_summary["p2_count"] = stats["blue"]

    formula = merged.get("formula_check", {})
    engine_summary["formula_passed"] = formula.get("passed", True)

    field = merged.get("field_check", {})
    engine_summary["field_check_passed"] = field.get("passed", True)

    summary["summary"] = engine_summary
    summary.update(merged)

    return summary


def main():
    parser = argparse.ArgumentParser(description="分段审核编排器 v5.4")
    parser.add_argument("--data", required=True, help="本月工资数据文件")
    parser.add_argument("--prev", help="上月工资数据文件（跨月对比需要）")
    parser.add_argument("--output-dir", default="/tmp/audit_phases", help="阶段输出目录")
    parser.add_argument("--phase", type=int, help="单独执行某阶段 (1-7)")
    parser.add_argument("--resume", action="store_true", help="从断点续传")
    parser.add_argument("--rules", help="rules.json 路径")

    args = parser.parse_args()

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载数据
    print(f"📂 加载数据: {args.data}")
    df, prev_df = load_data(args.data, args.prev)
    print(f"   {len(df)} 条记录, 上月数据: {'有' if prev_df is not None else '无'}")

    # 初始化引擎
    engine = PayrollRulesEngine(args.rules)

    # 确定要执行的阶段
    if args.phase:
        phases = [p for p in PHASES if p["id"] == args.phase]
    else:
        phases = PHASES

    # 断点续传
    completed_phases = {}
    if args.resume:
        for p in phases:
            phase_file = output_dir / f"{p['key']}.json"
            if phase_file.exists():
                with open(phase_file) as f:
                    completed_phases[p["key"]] = json.load(f)
                print(f"   ⏭️ 跳过阶段{p['id']}: {p['name']} (已完成)")

    phases_to_run = [p for p in phases if p["key"] not in completed_phases]

    if not phases_to_run:
        print("✅ 所有阶段已完成，无需执行。")
        return

    # 执行阶段
    all_results = list(completed_phases.values())
    blocked = False

    for phase in phases_to_run:
        print(f"\n{'='*50}")
        print(f"🔍 阶段{phase['id']}: {phase['name']}")
        print(f"{'='*50}")

        result = execute_phase(phase, engine, df, prev_df)
        all_results.append(result)

        # 保存阶段结果
        phase_file = output_dir / f"{phase['key']}.json"
        with open(phase_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        print(f"   📄 已保存: {phase_file}")

        # 检查阻断门
        if phase["is_gate"] and check_gate(result):
            print(f"\n🚨 阶段{phase['id']} 触发阻断门！红线异常，停止后续阶段。")
            blocked = True
            break

        print(f"   ⏱️  耗时: {result.get('elapsed_seconds', 0)}秒")

    # 合并汇总
    print(f"\n{'='*50}")
    print("📊 审核汇总")
    print(f"{'='*50}")

    final = generate_summary(all_results, len(df))
    final_file = output_dir / "audit_final.json"
    with open(final_file, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2, default=str)
    print(f"📄 最终结果: {final_file}")

    # 控制台摘要
    s = final.get("summary", {})
    print(f"\n   状态: {s.get('status', 'N/A')}")
    print(f"   🔴 红线: {s.get('p0_count', 0)}")
    print(f"   ⚠️  黄线: {s.get('p1_count', 0)}")
    print(f"   ℹ️  蓝线: {s.get('p2_count', 0)}")
    print(f"   ✅ 公式: {'通过' if s.get('formula_passed') else '失败'}")
    print(f"   ✅ 字段: {'通过' if s.get('field_check_passed') else '失败'}")
    print(f"   阶段完成: {len(all_results)}/{len(PHASES)}")

    if blocked:
        print(f"\n🚨 审核完成，发现红线异常（已记录在问题清单中）")


if __name__ == "__main__":
    main()
