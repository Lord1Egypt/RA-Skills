#!/usr/bin/env python3
"""
MktClaw Eval Test Runner — 自动执行 evals.json 中的测试用例
支持 regex / keyword / json_path 三种断言引擎 + L5 Validator 量化门禁

用法:
  python test_runner.py --evals ../evals/evals.json --results results.json
  python test_runner.py --evals ../evals/evals.json --filter intake --verbose
  python test_runner.py --evals ../evals/evals.json --format markdown
  python test_runner.py --evals ../evals/evals.json --gate-check

注意：本脚本仅执行程序化断言（regex/keyword/json_path）。
LLM-as-Judge 断言需要外部 LLM API，本脚本会标记为 "manual" 跳过。
"""

import json
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_evals(evals_path: str) -> dict[str, Any]:
    """加载 evals.json"""
    path = Path(evals_path)
    if not path.exists():
        print(f"错误：evals 文件不存在 {evals_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_regex_check(pattern: str, text: str, flags: str = "") -> bool:
    """执行 regex 断言"""
    regex_flags = 0
    if "i" in flags:
        regex_flags |= re.IGNORECASE
    if "m" in flags:
        regex_flags |= re.MULTILINE
    try:
        return bool(re.search(pattern, text, regex_flags))
    except re.error:
        return False


def run_keyword_check(check: dict, output_text: str) -> dict[str, Any]:
    """执行单个断言检查"""
    field = check.get("field", "output_text")
    pattern = check.get("pattern", "")
    flags = check.get("flags", "")
    required = check.get("required", True)
    negate = field.startswith("negate_")
    actual_field = field.replace("negate_", "") if negate else field
    description = check.get("description", "")

    # 实际检查
    matched = run_regex_check(pattern, output_text, flags)

    # negate 模式：匹配到 = 失败
    if negate:
        passed = not matched
    else:
        passed = matched

    # required=False 时不影响通过率，仅记录
    result = {
        "field": actual_field,
        "pattern": pattern[:50] + "..." if len(pattern) > 50 else pattern,
        "description": description,
        "matched": matched,
        "passed": passed if required else True,
        "required": required,
        "severity": "required" if required else "optional",
    }

    return result


def run_eval_case(case: dict, mock_output: str = "") -> dict[str, Any]:
    """执行单个 eval 用例"""
    case_id = case.get("id", "?")
    name = case.get("name", "unnamed")
    category = case.get("category", "unknown")
    assertions = case.get("assertions", {})

    result = {
        "id": case_id,
        "name": name,
        "category": category,
        "checks": [],
        "passed": True,
        "status": "pass",
    }

    # 模拟输出（实际使用时由 LLM 生成）
    output_text = mock_output or f"[模拟输出] {case.get('prompt', '')}"

    assertion_type = assertions.get("type", "keyword_match")
    checks = assertions.get("checks", [])

    if assertion_type == "llm_as_judge":
        result["status"] = "manual"
        result["passed"] = None
        result["note"] = "需要 LLM-as-Judge 外部评估"
        return result

    for check in checks:
        check_result = run_keyword_check(check, output_text)
        result["checks"].append(check_result)
        if not check_result["passed"] and check_result["required"]:
            result["passed"] = False

    result["status"] = "pass" if result["passed"] else "fail"
    return result


def run_all_evals(evals_data: dict, filter_category: str = None) -> dict[str, Any]:
    """执行所有 eval 用例"""
    evals = evals_data.get("evals", [])
    if filter_category:
        evals = [e for e in evals if e.get("category") == filter_category]

    results = []
    for case in evals:
        result = run_eval_case(case)
        results.append(result)

    # 统计
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    manual = sum(1 for r in results if r["status"] == "manual")
    pass_rate = passed / total if total > 0 else 0

    return {
        "generated_at": datetime.now().isoformat(),
        "skill_name": evals_data.get("skill_name", "unknown"),
        "version": evals_data.get("version", "unknown"),
        "total": total,
        "passed": passed,
        "failed": failed,
        "manual": manual,
        "pass_rate": round(pass_rate, 4),
        "threshold": evals_data.get("metadata", {}).get("pass_threshold", 0.8),
        "decision": "GO" if pass_rate >= 0.8 else "NO GO",
        "results": results,
    }


def format_markdown(report: dict) -> str:
    """格式化为 Markdown 报告"""
    lines = [
        f"# MktClaw Eval 测试报告",
        f"",
        f"**Skill**: {report['skill_name']} v{report['version']}",
        f"**时间**: {report['generated_at']}",
        f"**通过率**: {report['pass_rate']*100:.1f}% ({report['passed']}/{report['total']})",
        f"**阈值**: {report['threshold']*100:.0f}%",
        f"**决策**: {report['decision']}",
        f"",
        "## 概览",
        f"",
        f"| 指标 | 值 |",
        f"|------|-----|",
        f"| 总用例 | {report['total']} |",
        f"| 通过 | {report['passed']} |",
        f"| 失败 | {report['failed']} |",
        f"| 需人工 | {report['manual']} |",
        f"",
        "## 详细结果",
        f"",
        f"| ID | 名称 | 分类 | 状态 |",
        f"|-----|------|------|------|",
    ]

    for r in report["results"]:
        status_map = {"pass": "✅", "fail": "❌", "manual": "📋"}
        status = status_map.get(r["status"], "?")
        lines.append(f"| {r['id']} | {r['name'][:40]} | {r['category']} | {status} |")

    # 失败用例详情
    failed = [r for r in report["results"] if r["status"] == "fail"]
    if failed:
        lines.append("")
        lines.append("## 失败用例详情")
        for f in failed:
            lines.append(f"")
            lines.append(f"### #{f['id']} {f['name']}")
            for c in f.get("checks", []):
                if not c["passed"]:
                    lines.append(f"- ❌ {c['description']} (pattern: `{c['pattern']}`)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="MktClaw Eval Test Runner")
    parser.add_argument("--evals", required=True, help="evals.json 文件路径")
    parser.add_argument("--results", help="输出结果文件路径")
    parser.add_argument("--filter", help="按分类过滤 (如 intake, router, strategy)")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    parser.add_argument("--gate-check", action="store_true", help="执行 L5 Validator 量化门禁检查")
    args = parser.parse_args()

    evals_data = load_evals(args.evals)
    report = run_all_evals(evals_data, args.filter)

    # L5 Validator 量化门禁
    if args.gate_check:
        gate = check_l5_gate(report, evals_data)
        report["l5_validator"] = gate

    if args.format == "markdown":
        output = format_markdown(report)
    else:
        output = json.dumps(report, ensure_ascii=False, indent=2)

    if args.results:
        Path(args.results).write_text(output, encoding="utf-8")
        print(f"结果已写入: {args.results}")
    else:
        print(output)

    if args.verbose:
        print(f"\n--- 摘要 ---", file=sys.stderr)
        print(f"通过率: {report['pass_rate']*100:.1f}%", file=sys.stderr)
        print(f"决策: {report['decision']}", file=sys.stderr)
        if args.gate_check and "l5_validator" in report:
            print(f"门禁: {'通过' if report['l5_validator']['gate_passed'] else '未通过'}", file=sys.stderr)

    # 退出码：eval 或门禁未通过均返回 1
    exit_code = 0 if report["decision"] == "GO" else 1
    if args.gate_check and "l5_validator" in report and not report["l5_validator"]["gate_passed"]:
        exit_code = 1
    sys.exit(exit_code)


def check_l5_gate(report: dict, evals_data: dict) -> dict[str, Any]:
    """L5 Validator 量化门禁检查"""
    # 从 evals metadata 或默认值获取阈值
    metadata = evals_data.get("metadata", {})
    pass_threshold = metadata.get("pass_threshold", 0.8)

    # 加载 config.yaml 中的门禁阈值
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"
    gate_thresholds = {}
    if config_path.exists():
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            gate_thresholds = config.get("runtime_harness", {}).get("l5_validator", {}).get("gate_thresholds", {})
        except Exception:
            pass

    # 默认阈值
    if not gate_thresholds:
        gate_thresholds = {
            "pass_rate": pass_threshold,
            "failure_count_max": 5,
        }

    checks = {}

    # Eval 通过率门禁
    pass_rate = report.get("pass_rate", 0)
    threshold = gate_thresholds.get("pass_rate", pass_threshold)
    checks["pass_rate"] = {
        "value": pass_rate,
        "threshold": threshold,
        "passed": pass_rate >= threshold,
    }

    # 失败用例数门禁
    failed_count = report.get("failed", 0)
    max_failures = gate_thresholds.get("failure_count_max", 5)
    checks["failed_count"] = {
        "value": failed_count,
        "threshold": max_failures,
        "passed": failed_count <= max_failures,
    }

    gate_passed = all(c["passed"] for c in checks.values())

    return {
        "gate_passed": gate_passed,
        "checks": checks,
        "config_source": "config.yaml" if gate_thresholds else "default",
    }


if __name__ == "__main__":
    main()
