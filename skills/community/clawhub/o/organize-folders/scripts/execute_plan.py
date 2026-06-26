#!/usr/bin/env python3
"""按整理计划执行文件操作；默认 dry-run。"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from orglib import load_json, now_iso


def log_line(log_path: Path, entry: dict) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute_item(item: dict, apply: bool, include_high_risk: bool) -> tuple[str, str]:
    action = item.get("action")
    source = Path(item["source"]) if item.get("source") else None
    target = Path(item["target"]) if item.get("target") else None

    if action in {"skip", "manual-review"}:
        return "skipped", "跳过或需要人工确认"
    if item.get("risk") == "high" and not include_high_risk:
        return "skipped", "高风险项未启用执行"
    if action in {"create_dir", "create_sandbox"}:
        if not target:
            return "error", "缺少目标路径"
        if apply:
            target.mkdir(parents=True, exist_ok=True)
        return "created" if apply else "dry-run", "创建目录"
    if action in {"move", "rename", "copy", "archive", "backup"}:
        if not source or not target:
            return "error", "缺少原路径或目标路径"
        if not source.exists():
            return "error", "原路径不存在"
        if target.exists():
            return "error", "目标路径已存在"
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            if action == "copy" or action == "backup":
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
            else:
                shutil.move(str(source), str(target))
        return "done" if apply else "dry-run", action
    return "error", f"未知动作：{action}"


def markdown_log_from_jsonl(log_path: Path, markdown_path: Path) -> None:
    rows = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        rows.append([item["time"], item["action"], item.get("source", ""), item.get("target", ""), item["status"], item["note"]])
    lines = [
        "# 执行日志",
        "",
        "| 时间 | 操作 | 原路径 | 目标路径 | 结果 | 备注 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="执行整理计划。默认 dry-run。")
    parser.add_argument("--plan", required=True, help="整理计划 JSON 文件")
    parser.add_argument("--apply", action="store_true", help="真正执行计划；未指定时只 dry-run")
    parser.add_argument("--include-high-risk", action="store_true", help="允许执行高风险项")
    parser.add_argument("--log", help="JSONL 日志路径")
    args = parser.parse_args()

    plan = load_json(args.plan)
    log_path = Path(args.log) if args.log else Path(f"organize-log_{now_iso().replace(':', '').replace('-', '')}.jsonl")
    if log_path.exists():
        log_path.unlink()

    for item in plan.get("items", []):
        status, note = execute_item(item, args.apply, args.include_high_risk)
        log_line(
            log_path,
            {
                "time": now_iso(),
                "action": item.get("action"),
                "source": item.get("source", ""),
                "target": item.get("target", ""),
                "status": status,
                "note": note,
                "sandbox": plan.get("sandbox", False),
            },
        )

    markdown_log_from_jsonl(log_path, log_path.with_suffix(".md"))
    print(f"日志已生成：{log_path}")
    print(f"Markdown 日志：{log_path.with_suffix('.md')}")


if __name__ == "__main__":
    main()
