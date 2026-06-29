#!/usr/bin/env python3
"""Validate Life Fork user-report structure before rendering."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional


REQUIRED_ORDER = [
    "# ",
    "判词：",
    "看清：",
    "问题：",
    "核心判断：",
    "## 1. 你真正放不下的是什么",
    "## 2. 三种结果",
    "## 3. 事件冲击卡",
    "## 4. 哪些来自选择，哪些来自时代",
    "## 5. 30 天验证实验",
    "## 6. 继续解释：这份报告怎么判断",
]

REQUIRED_MARKERS = [
    "### 机制链",
    "### 反证条件",
    "### 证据债",
    "### 真正的盲点",
    "### 换几个角度看这件事",
    "### 那几年，外部环境也在变",
    "### 还有哪些信息会改写结论",
    "### 这份报告不能替你决定什么",
]

REQUIRED_TABLES = [
    "| 结果 | 会给你什么 | 会拿走什么 | 最大陷阱 |",
    "| 事件锚点 | 生活场景 | 现实代价 | 情绪代价 | 误判点 | 今天验证 |",
    "| 来源 | 它改变了什么 | 你该怎么理解 |",
    "| 时间 | 动作 | 怎么做 | 看什么 |",
    "| 来源 | 关键提醒 | 制衡点 |",
    "| 外部变化 | 时间 | 改变了什么 | 怎么理解 |",
]

REQUIRED_SOURCES = ["职业视角", "现金流视角", "健康视角", "时代事件视角", "反过来提醒"]

FORBIDDEN_DEFAULT_DELIVERY_TERMS = [
    "".join(parts)
    for parts in [
        ("小", "红", "书"),
        ("抖", "音"),
        ("口", "播"),
        ("公开", "图文"),
        ("传播", "资产"),
        ("系统", "运行", "日志"),
    ]
]

FORBIDDEN_CERTAINTY_TERMS = [
    "".join(parts)
    for parts in [
        ("预测", "命运"),
        ("准确", "模拟", "人生"),
        ("你", "当年", "选错了"),
        ("一定", "更成功"),
    ]
]

CONSULTING_REPORT_HEADINGS = [
    "".join(("## 1. ", "一页", "摘要")),
    "".join(("## 3. ", "多视角", "结论")),
    "".join(("## 4. ", "事件", "影响")),
    "".join(("## ", "依据", "层：这份判断怎么来的")),
    "".join(("冲突", "矩阵")),
]

PROJECT_MANAGEMENT_TERMS = [
    "产物",
    "判断门槛",
    "交付",
    "试运行",
    "反馈记录",
]


def line_index(lines: list[str], needle: str) -> Optional[int]:
    for index, line in enumerate(lines):
        if needle == "# ":
            if line.startswith("# "):
                return index
        elif line.startswith(needle) or needle in line:
            return index
    return None


def count_table_rows_between(text: str, start_heading: str, next_heading: Optional[str]) -> int:
    try:
        start = text.index(start_heading)
        end = text.index(next_heading, start) if next_heading else len(text)
    except ValueError:
        return 0
    section = text[start:end]
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and "---" not in stripped:
            rows.append(stripped)
    return max(0, len(rows) - 1)


def validate_report(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    positions: list[tuple[str, int]] = []
    for marker in REQUIRED_ORDER:
        index = line_index(lines, marker)
        if index is None:
            errors.append(f"missing required marker: {marker}")
        else:
            positions.append((marker, index))

    for (left_marker, left_index), (right_marker, right_index) in zip(positions, positions[1:]):
        if left_index >= right_index:
            errors.append(f"marker order error: {left_marker} should appear before {right_marker}")

    h1_count = sum(1 for line in lines if line.startswith("# "))
    if h1_count != 1:
        errors.append(f"expected exactly one H1, found {h1_count}")

    verdict_line = next((line for line in lines if line.startswith("判词：")), "")
    verdict_text = verdict_line.removeprefix("判词：").strip()
    if len(verdict_text) < 35 or len(verdict_text) > 130:
        errors.append("verdict sentence should be 35-130 Chinese characters")

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"missing required marker: {marker}")

    for table_head in REQUIRED_TABLES:
        if table_head not in text:
            errors.append(f"missing required table: {table_head}")

    for source in REQUIRED_SOURCES:
        if f"| {source} |" not in text:
            errors.append(f"missing judgement source row: {source}")

    line_rows = count_table_rows_between(text, "## 2. 三种结果", "## 3. 事件冲击卡")
    if line_rows < 3:
        errors.append(f"result table should contain at least 3 rows, found {line_rows}")

    variable_rows = count_table_rows_between(text, "## 3. 事件冲击卡", "### 被低估")
    if variable_rows < 4 or variable_rows > 6:
        errors.append(f"event shock table should contain 4-6 rows, found {variable_rows}")
    variable_section = text[text.find("## 3. 事件冲击卡") : text.find("### 被低估")]
    for marker in ("事件锚点", "生活场景", "现实代价", "情绪代价", "误判点", "今天验证"):
        if marker not in variable_section:
            errors.append(f"event shock column missing: {marker}")

    event_rows = count_table_rows_between(text, "### 那几年，外部环境也在变", "### 还有哪些信息会改写结论")
    if event_rows < 3 or event_rows > 5:
        errors.append(f"event table should contain 3-5 rows, found {event_rows}")

    action_section_start = text.find("## 5. 30 天验证实验")
    action_section_end = text.find("## 6. 继续解释：这份报告怎么判断")
    action_section = text[action_section_start:action_section_end] if action_section_start != -1 and action_section_end != -1 else ""
    action_rows = count_table_rows_between(text, "## 5. 30 天验证实验", "## 6. 继续解释：这份报告怎么判断")
    if action_rows != 4:
        errors.append(f"expected exactly 4 weekly action rows, found {action_rows}")
    for week in ("第 1 周", "第 2 周", "第 3 周", "第 4 周"):
        if week not in action_section:
            errors.append(f"30-day experiment missing weekly marker: {week}")
    for term in PROJECT_MANAGEMENT_TERMS:
        if term in action_section:
            errors.append(f"project-management term leaked into action section: {term}")

    question_marker_index = max(
        text.find("#### 还可以补的 5 个信息"),
        text.find("#### 还可以补的 3 个信息"),
        text.find("### 还需要补的 5 个问题"),
        text.find("### 还需要补的 3 个问题"),
    )
    if question_marker_index == -1:
        errors.append("missing supplement question section")
        question_count = 0
    else:
        question_count = len(re.findall(r"^\d+\.\s", text[question_marker_index:], flags=re.MULTILINE))
    if question_count < 3:
        errors.append(f"expected at least 3 numbered supplement questions, found {question_count}")
    if question_count > 5:
        errors.append(f"expected no more than 5 numbered supplement questions, found {question_count}")

    evidence_layer = text.find("## 6. 继续解释：这份报告怎么判断")
    if evidence_layer != -1:
        body_text = text[:evidence_layer]
        if "Agent" in body_text or "质量评分" in body_text or "置信度" in body_text:
            errors.append("backend details leaked into main body")

    for heading in CONSULTING_REPORT_HEADINGS:
        if heading in text:
            errors.append(f"old report heading should be removed: {heading}")

    forbidden_terms = FORBIDDEN_DEFAULT_DELIVERY_TERMS + FORBIDDEN_CERTAINTY_TERMS
    for term in forbidden_terms:
        if term in text:
            errors.append(f"forbidden term in default user report: {term}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Life Fork user report.")
    parser.add_argument("report", type=Path, help="Markdown report path")
    args = parser.parse_args()

    errors = validate_report(args.report)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
