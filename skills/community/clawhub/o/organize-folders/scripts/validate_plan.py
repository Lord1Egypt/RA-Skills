#!/usr/bin/env python3
"""执行前校验整理计划。"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from orglib import is_system_path, load_json, markdown_table, write_json


BLOCKED_ACTIONS = {"delete", "overwrite", "clear"}
EXECUTABLE_ACTIONS = {"create_dir", "create_sandbox", "move", "rename", "copy", "archive", "backup", "skip", "manual-review"}


def validate(plan: dict) -> dict:
    issues: list[dict] = []
    targets = [item.get("target", "") for item in plan.get("items", []) if item.get("target")]
    duplicates = {target for target, count in Counter(t.lower() for t in targets).items() if count > 1}

    for index, item in enumerate(plan.get("items", []), start=1):
        action = item.get("action", "")
        source = Path(item["source"]) if item.get("source") else None
        target = Path(item["target"]) if item.get("target") else None

        def add(severity: str, message: str) -> None:
            issues.append({"index": index, "severity": severity, "message": message, "item": item})

        if action in BLOCKED_ACTIONS:
            add("error", f"禁止动作：{action}")
        if action not in EXECUTABLE_ACTIONS:
            add("warning", f"未知动作：{action}")
        if source and not source.exists() and action not in {"create_dir", "create_sandbox", "skip", "manual-review"}:
            add("error", "原路径不存在")
        if source and is_system_path(source):
            add("error", "原路径疑似系统目录")
        if target and is_system_path(target):
            add("error", "目标路径疑似系统目录")
        if target and str(target).lower() in duplicates:
            add("error", "多个计划项使用相同目标路径")
        if target and target.exists() and action in {"move", "rename", "copy", "archive", "backup"}:
            add("error", "目标路径已存在，可能覆盖")
        if item.get("risk") == "high" and not item.get("requires_confirmation"):
            add("warning", "高风险项未标记为需要确认")

    status = "valid" if not any(issue["severity"] == "error" for issue in issues) else "invalid"
    return {"version": 1, "status": status, "issue_count": len(issues), "issues": issues}


def to_markdown(report: dict) -> str:
    rows = [[issue["severity"], issue["index"], issue["message"], issue["item"].get("source", ""), issue["item"].get("target", "")] for issue in report["issues"]]
    return "\n".join(
        [
            "# 整理计划校验报告",
            "",
            f"- 状态：`{report['status']}`",
            f"- 问题数：`{report['issue_count']}`",
            "",
            markdown_table(["级别", "序号", "问题", "原路径", "目标路径"], rows),
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="校验整理计划。")
    parser.add_argument("--plan", required=True, help="整理计划 JSON 文件")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    report = validate(load_json(args.plan))
    text = to_markdown(report) if args.format == "markdown" else json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        if args.format == "json":
            write_json(args.output, report)
        else:
            Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    if report["status"] != "valid":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
