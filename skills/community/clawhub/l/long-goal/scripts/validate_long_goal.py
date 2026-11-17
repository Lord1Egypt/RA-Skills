#!/usr/bin/env python3
"""Validate a long-goal goal.md as the single persistent source of truth."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path


GOAL_HEADINGS = (
    "## 总目标",
    "## 完成条件",
    "## 范围与约束",
    "## sub goal matrix",
    "## 当前检查点",
    "## 进展",
    "## 重大决策",
    "## 重要信息",
)

TEMPLATE_PLACEHOLDERS = (
    "<长期目标名称>",
    "<稳定标识>",
    "<带时区的 ISO 8601 日期时间>",
    "<本文件绝对路径或稳定工作区路径>",
    "<描述最终结果，而不是只描述活动。>",
    "<可以独立验证的结束条件。>",
    "<必须遵守的边界、资源或禁止项。>",
    "<子目标>",
    "<可观察结果>",
    "<证据索引或待验证>",
    "<恢复后应先执行的动作及完成判据。>",
    "<尚未验证、等待输入或存在风险的事项；没有时写“无”。>",
    "<日期>",
    "<本轮完成内容、验证结论和剩余差距。>",
    "<稳定取舍、原因和影响范围；没有时写“暂无”。>",
    "<恢复任务所需、但不属于目标或决策的稳定信息；没有时写“暂无”。>",
)


def field_values(text: str, label: str) -> list[str]:
    return [
        match.strip().strip("`")
        for match in re.findall(rf"(?m)^[>\-][ \t]*{re.escape(label)}[ \t]*(.*?)[ \t]*\r?$", text)
    ]


def field_value(text: str, label: str) -> str | None:
    values = field_values(text, label)
    return values[0] if len(values) == 1 else None


def heading_count(text: str, heading: str) -> int:
    return len(re.findall(rf"(?m)^{re.escape(heading)}[ \t]*\r?$", text))


def section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}[ \t]*\r?\n(.*?)(?=^##\s|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def sub_goal_rows(text: str) -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"SG[\w-]+", cells[0], re.IGNORECASE):
            continue
        rows.append((cells[0].upper(), cells[1], cells[2], cells[3], cells[4]))
    return rows


def unresolved_placeholders(text: str) -> list[str]:
    return [placeholder for placeholder in TEMPLATE_PLACEHOLDERS if placeholder in text]


def resolve_pointer(owner: Path, value: str) -> Path:
    pointer = Path(value)
    return pointer.resolve() if pointer.is_absolute() else (owner.parent / pointer).resolve()


def is_zoned_iso_datetime(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value and parsed.tzinfo is not None and parsed.utcoffset() is not None
    except ValueError:
        return False


def validate_goal_text(text: str) -> list[str]:
    errors: list[str] = []

    for heading in GOAL_HEADINGS:
        if heading_count(text, heading) != 1:
            errors.append(f"目标文件必须且只能包含一次标题：{heading}")
        elif not section_body(text, heading):
            errors.append(f"目标文件章节不能为空：{heading}")

    normalized_lines = {line.replace(" ", "") for line in text.splitlines()}
    if "|ID|子目标|完成判据|状态|证据|" not in normalized_lines:
        errors.append("sub goal matrix 必须包含 ID、子目标、完成判据、状态和证据列")

    rows = sub_goal_rows(text)
    if not rows:
        errors.append("sub goal matrix 至少需要一个 SG 子目标")
    ids = [row[0] for row in rows]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"sub goal ID 必须唯一，发现重复：{', '.join(duplicates)}")
    for row in rows:
        if any(not cell for cell in row[1:]):
            errors.append(f"{row[0]} 的子目标、完成判据、状态和证据都必须非空")

    for label in ("状态：", "Goal ID：", "最近维护：", "权威目标：", "当前子目标：", "唯一下一步：", "未闭环项："):
        values = field_values(text, label)
        if len(values) != 1 or not values[0]:
            errors.append(f"目标文件必须且只能包含一个非空字段：{label}")

    maintained_at = field_value(text, "最近维护：")
    if maintained_at and not is_zoned_iso_datetime(maintained_at):
        errors.append("最近维护时间必须是包含有效时区的 ISO 8601 日期时间")

    current_sub_goal = field_value(text, "当前子目标：")
    if current_sub_goal and current_sub_goal.upper() not in set(ids):
        errors.append("当前子目标不在 sub goal matrix 中")

    placeholders = unresolved_placeholders(text)
    if placeholders:
        errors.append(f"目标文件仍包含模板占位符：{', '.join(placeholders)}")

    return errors


def validate_goal_path(goal_path: Path, text: str) -> list[str]:
    authority = field_value(text, "权威目标：")
    if authority and resolve_pointer(goal_path, authority) != goal_path.resolve():
        return ["goal.md 的权威目标没有指向自身"]
    return []


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"文件不是有效 UTF-8：{path}") from exc


def run_self_test() -> int:
    valid_goal = """# 示例长期目标
> 状态：ACTIVE
> Goal ID：demo
> 最近维护：2026-01-01T12:00:00+08:00
> 权威目标：goal.md
## 总目标
完成结果。
## 完成条件
- 已验证。
## 范围与约束
- 只读。
## sub goal matrix
| ID | 子目标 | 完成判据 | 状态 | 证据 |
| --- | --- | --- | --- | --- |
| SG1 | 调研 | 有来源 | 进行中 | round-1 |
## 当前检查点
- 当前子目标：SG1
- 唯一下一步：核实反证并记录边界。
- 未闭环项：来源完整性待验证。
## 进展
- 已完成初筛。
## 重大决策
- 暂无。
## 重要信息
- 数学表达式 <x> 是有效内容。
"""
    with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp_dir:
        goal_path = Path(temp_dir) / "goal.md"
        goal_path.write_text(valid_goal, encoding="utf-8")
        checks = (
            not validate_goal_text(valid_goal),
            not validate_goal_path(goal_path, valid_goal),
            bool(validate_goal_text("# 缺失结构")),
            bool(validate_goal_text(valid_goal.replace("- 已验证。", "- <可以独立验证的结束条件。>"))),
            bool(validate_goal_text(valid_goal.replace("2026-01-01T12:00:00+08:00", "not-a-time+99:99"))),
            bool(validate_goal_text(valid_goal.replace("| SG1 | 调研 | 有来源 | 进行中 | round-1 |", "| SG1 | 调研 | 有来源 | 进行中 | round-1 |\n| SG1 | 写作 | 已发布 | 已完成 | report |"))),
            bool(validate_goal_text(valid_goal.replace("当前子目标：SG1", "当前子目标：SG9"))),
            bool(validate_goal_text(valid_goal.replace("唯一下一步：核实反证并记录边界。", "唯一下一步："))),
            bool(validate_goal_text(valid_goal.replace("| SG1 | 调研 | 有来源 | 进行中 | round-1 |", "| SG1 | 调研 | 有来源 | 进行中 |  |"))),
            bool(validate_goal_path(goal_path, valid_goal.replace("权威目标：goal.md", "权威目标：other.md"))),
            not unresolved_placeholders("数学表达式 <x> 不是模板占位符"),
        )
    if all(checks):
        print(f"PASS: validator self-test passed ({len(checks)}/{len(checks)})")
        return 0
    failed = [str(index) for index, passed in enumerate(checks, start=1) if not passed]
    print(f"FAIL: validator self-test failed at checks {', '.join(failed)}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--goal", type=Path, help="Path to the canonical goal.md")
    parser.add_argument("--self-test", action="store_true", help="Run built-in validation tests")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.goal is None:
        parser.error("--goal is required unless --self-test is used")

    errors: list[str] = []
    try:
        goal_text = read_utf8(args.goal)
        errors.extend(validate_goal_text(goal_text))
        errors.extend(validate_goal_path(args.goal, goal_text))
    except (OSError, ValueError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: long-goal structure is valid (goal={args.goal})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
