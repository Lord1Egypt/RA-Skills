#!/usr/bin/env python3
"""根据执行日志生成回滚计划；只生成计划，不执行回滚。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orglib import markdown_table, now_iso, write_json


REVERSIBLE = {"move", "rename", "archive"}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def build_plan(log_rows: list[dict]) -> dict:
    items = []
    manual = []
    for row in reversed(log_rows):
        if row.get("status") not in {"done"}:
            continue
        action = row.get("action")
        if action in REVERSIBLE:
            items.append(
                {
                    "action": "move",
                    "source": row.get("target", ""),
                    "target": row.get("source", ""),
                    "reason": f"回滚 {action} 操作",
                    "risk": "medium",
                    "requires_confirmation": True,
                }
            )
        else:
            manual.append(row)
    return {"version": 1, "generated_at": now_iso(), "items": items, "manual_review": manual}


def to_markdown(plan: dict) -> str:
    rows = [[item["action"], item["source"], item["target"], item["reason"], item["risk"]] for item in plan["items"]]
    manual_rows = [[row.get("action"), row.get("source", ""), row.get("target", ""), row.get("note", "")] for row in plan["manual_review"]]
    return "\n".join(
        [
            "# 回滚计划",
            "",
            f"- 生成时间：`{plan['generated_at']}`",
            "",
            "## 可回滚操作",
            "",
            markdown_table(["动作", "原路径", "目标路径", "原因", "风险"], rows),
            "",
            "## 需要人工确认",
            "",
            markdown_table(["原动作", "原路径", "目标路径", "备注"], manual_rows),
            "",
            "> 此文件只生成回滚计划，不自动执行。",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="根据执行日志生成回滚计划。")
    parser.add_argument("--log", required=True, help="execute_plan.py 生成的 JSONL 日志")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    plan = build_plan(load_jsonl(Path(args.log)))
    text = to_markdown(plan) if args.format == "markdown" else json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        if args.format == "json":
            write_json(args.output, plan)
        else:
            Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
