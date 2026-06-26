#!/usr/bin/env python3
"""
Data Index Generator v6.0 - 数据支撑索引表

这是报告(report)和看板(kanban)之间的关联核心。
生成一个 JSON 索引文件，包含每个规则的完整数据，
报告和看板都引用同一份数据，保证数据一致性。

输入: rules_engine.py 输出的 audit_result.json
输出: data_index.json

用法:
    python3 scripts/generate_data_index.py --input audit_result.json --output data_index.json
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_index(results, link_template=None):
    """生成数据支撑索引"""
    total_records = results.get("total_records", 0)
    audit_time = results.get("audit_time", datetime.now().isoformat())
    version = results.get("version", "")
    audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M')}_{total_records}"

    index = {
        "audit_id": audit_id,
        "timestamp": audit_time,
        "version": version,
        "total_records": total_records,
        "rule_index": {},
        "summary": {
            "blocked": results.get("summary", {}).get("blocked", False),
            "red_count": 0,
            "yellow_count": 0,
            "blue_count": 0,
            "total_rules": 0,
            "passed_rules": 0,
        },
    }

    rule_index = index["rule_index"]
    summary = index["summary"]

    def add_rule(rule_id, category, name, checked, passed, failed, details,
                 report_anchor="", status="", action=""):
        """添加规则到索引"""
        if not rule_id:
            rule_id = hashlib.md5(f"{category}-{name}".encode()).hexdigest()[:8]

        rate = f"{(passed / max(checked, 1)) * 100:.1f}%"
        if status == "":
            if failed == 0:
                status = "pass"
            elif category == "红线":
                status = "block"
            else:
                status = "warning"

        if action == "" and failed > 0:
            if category == "红线":
                action = f"立即核实并修正: {failed}人"
            else:
                action = f"核实: {failed}人"
        elif action == "":
            action = "无需操作"

        rule_index[rule_id] = {
            "category": category,
            "name": name,
            "checked": checked,
            "passed": passed,
            "failed": failed,
            "rate": rate,
            "status": status,
            "report_anchor": f"report_v6.html#{rule_id}" if not report_anchor else report_anchor,
            "kanban_anchor": f"kanban_v6.html?rule={rule_id}",
            "action": action,
            "details": details[:50] if details else [],  # Cap at 50 for index size
            "detail_count": len(details),
        }

        summary["total_rules"] += 1
        if failed == 0:
            summary["passed_rules"] += 1
        if category == "红线":
            summary["red_count"] += failed
        elif category == "黄线":
            summary["yellow_count"] += failed
        elif category == "蓝线":
            summary["blue_count"] += failed

    # 1. Field check
    fc = results.get("field_check", {})
    fc_checked = fc.get("total_fields_checked", 0)
    fc_failed = 0 if fc.get("passed", True) else len(fc.get("missing", {}))
    add_rule(
        "FC-001", "字段完整性", "必填字段检查",
        fc_checked, fc_checked - fc_failed, fc_failed,
        [{"field": k, "reason": v} for k, v in fc.get("missing", {}).items()],
        status="pass" if fc.get("passed", True) else "warning",
        action="补充缺失字段后重新审核" if not fc.get("passed", True) else "无需操作",
    )

    # 2. Formula check
    formula_check = results.get("formula_check", {})
    for fr in formula_check.get("formula_results", []):
        rid = fr.get("rule_id", f"FM-{len(rule_index)}")
        fail = fr.get("violation_count", 0)
        chk = fr.get("total_checked", 0)
        add_rule(
            rid, "公式校验", fr.get("rule_name", ""),
            chk, chk - fail, fail,
            fr.get("violations", []),
            status="pass" if fail == 0 else "warning",
            action="核实公式偏差" if fail > 0 else "无需操作",
        )

    # 3. Business rules
    business_check = results.get("business_check", {})
    for br in business_check.get("rule_results", []):
        rid = br.get("rule_id", f"BR-{len(rule_index)}")
        triggered = br.get("triggered", 0)
        chk = br.get("total_checked", 0)
        add_rule(
            rid, "业务规则", br.get("rule_name", ""),
            chk, chk - triggered, triggered,
            br.get("details", []),
        )

    # 4. Red lines
    red_check = results.get("red_lines", {})
    for rl in red_check.get("rule_results", []):
        rid = rl.get("rule_id", f"RL-{len(rule_index)}")
        triggered = rl.get("triggered", 0)
        chk = rl.get("total_checked", 0)
        add_rule(
            rid, "红线", rl.get("name", ""),
            chk, chk - triggered, triggered,
            rl.get("details", []),
            status="pass" if triggered == 0 else "block",
            action="立即核实并修正" if triggered > 0 else "无需操作",
        )

    # 5. Yellow lines
    yellow_check = results.get("yellow_lines", {})
    for yl in yellow_check.get("rule_results", []):
        rid = yl.get("rule_id", f"YL-{len(rule_index)}")
        triggered = yl.get("triggered", 0)
        chk = yl.get("total_checked", 0)
        add_rule(
            rid, "黄线", yl.get("name", ""),
            chk, chk - triggered, triggered,
            yl.get("details", []),
        )

    # 6. Blue lines
    blue_check = results.get("blue_lines", {})
    for bl in blue_check.get("rule_results", []):
        rid = bl.get("rule_id", f"BL-{len(rule_index)}")
        triggered = bl.get("triggered", 0)
        chk = bl.get("total_checked", 0)
        add_rule(
            rid, "蓝线", bl.get("name", ""),
            chk, chk - triggered, triggered,
            bl.get("details", []),
            status="pass" if triggered == 0 else "note",
            action="关注趋势变化" if triggered > 0 else "无需操作",
        )

    # 7. Policy check
    policy_check = results.get("policy_check", {})
    for pol in policy_check.get("rule_results", []):
        rid = pol.get("rule_id", f"POL-{len(rule_index)}")
        triggered = pol.get("violation_count", 0)
        chk = pol.get("matched_count", 0)
        add_rule(
            rid, "政策校验", pol.get("name", pol.get("policy_name", "")),
            chk, chk - triggered, triggered,
            pol.get("violations", []),
        )

    # Cross-links
    index["cross_links"] = {
        "report_file": "audit_report_v6.html",
        "kanban_file": "kanban_v6.html",
        "source_file": "audit_result.json",
        "usage": "报告和看板都通过 rule_index 中的 rule_id 关联到同一份数据",
    }

    return index


def main():
    parser = argparse.ArgumentParser(description="数据支撑索引生成器 v6.0")
    parser.add_argument("--input", required=True, help="audit_result.json 路径")
    parser.add_argument("--output", default="data_index.json", help="输出文件路径")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        results = json.load(f)

    index = generate_index(results)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"✅ 数据索引已生成: {args.output}")
    print(f"   规则数: {index['summary']['total_rules']}")
    print(f"   通过: {index['summary']['passed_rules']}")
    print(f"   异常: {index['summary']['total_rules'] - index['summary']['passed_rules']}")
    print(f"   红线: {index['summary']['red_count']}")
    print(f"   黄线: {index['summary']['yellow_count']}")
    print(f"   蓝线: {index['summary']['blue_count']}")


if __name__ == "__main__":
    main()
