#!/usr/bin/env python3
"""Validate that a Life Fork report contains concrete, auditable insight."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_MARKERS = [
    "判词：",
    "### 机制链",
    "### 反证条件",
    "### 证据债",
    "### 真正的盲点",
    "| 事件锚点 | 生活场景 | 现实代价 | 情绪代价 | 误判点 | 今天验证 |",
    "| 时间 | 动作 | 怎么做 | 看什么 |",
]

ABSTRACT_TERMS = [
    "机会密度",
    "平台网络",
    "职业上限",
    "可见度",
    "核心项目",
    "圈层",
]

SPECIFIC_ANCHORS = [
    "团队",
    "KPI",
    "预算",
    "数据",
    "通勤",
    "房租",
    "税后",
    "签证",
    "岗位",
    "租金",
    "现金流",
    "储蓄",
    "睡眠",
    "复盘",
    "项目样本",
    "项目卡",
    "作品",
    "用户",
    "反馈",
    "访谈",
    "收入",
    "看什么",
]

DISALLOWED_ACTION_TERMS = ["每周都有动作", "产物", "判断门槛", "试运行", "交付"]


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"missing specificity marker: {marker}")

    verdict_line = next((line for line in text.splitlines() if line.startswith("判词：")), "")
    verdict_text = verdict_line.removeprefix("判词：").strip()
    if not verdict_text or len(verdict_text) < 35:
        errors.append("verdict sentence is too weak or missing")

    anchor_hits = sum(1 for anchor in SPECIFIC_ANCHORS if anchor in text)
    if anchor_hits < 6:
        errors.append(f"expected at least 6 concrete anchors, found {anchor_hits}")

    abstract_hits = sum(text.count(term) for term in ABSTRACT_TERMS)
    if abstract_hits > 10:
        errors.append(f"too many abstract terms: {abstract_hits}")

    if "多思考" in text or "多了解" in text or "保持关注" in text:
        errors.append("action advice is too vague")

    action_start = text.find("## 5. 30 天验证实验")
    action_end = text.find("## 6. 继续解释：这份报告怎么判断")
    action_section = text[action_start:action_end] if action_start != -1 and action_end != -1 else ""
    action_rows = [
        line
        for line in action_section.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|") and "---" not in line
    ]
    if len(action_rows) != 5:
        errors.append(f"expected action table header plus 4 weekly rows, found {len(action_rows)} rows")
    for week in ("第 1 周", "第 2 周", "第 3 周", "第 4 周"):
        if week not in action_section:
            errors.append(f"30-day experiment missing weekly marker: {week}")
    for term in DISALLOWED_ACTION_TERMS:
        if term in action_section:
            errors.append(f"project-management term leaked into action section: {term}")
    if "每周都有动作、可保存记录和结果判断" in text:
        errors.append("quality evidence uses planning-style wording")

    variable_start = text.find("## 3. 事件冲击卡")
    variable_end = text.find("### 被低估", variable_start)
    variable_section = text[variable_start:variable_end] if variable_start != -1 and variable_end != -1 else ""
    variable_rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in variable_section.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|") and "---" not in line
    ]
    body_rows = variable_rows[1:] if variable_rows else []
    if len(body_rows) < 4 or len(body_rows) > 6:
        errors.append(f"expected 4-6 event shock rows, found {len(body_rows)}")
    for index, row in enumerate(body_rows, start=1):
        if len(row) != 6:
            errors.append(f"event shock row {index} should use 6 fields, found {len(row)}")
            continue
        combined = "".join(row)
        if len(combined) < 160:
            errors.append(f"event shock row {index} is too thin: {len(combined)} chars")
        if len(combined) > 520:
            errors.append(f"event shock row {index} is too dense: {len(combined)} chars")
        for field_index, field_name in ((2, "生活场景"), (3, "现实代价"), (4, "情绪代价"), (5, "误判点"), (6, "今天验证")):
            if len(row[field_index - 1]) < 14:
                errors.append(f"event shock row {index} field {field_name} is too thin")
        if not any(anchor in combined for anchor in ("2008", "2016", "2018", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "项目", "同行", "收入", "通勤", "睡眠", "签证", "用户", "反馈", "作品", "预算", "岗位", "家庭", "团队", "问题", "流程", "测试", "朋友", "社群", "同学", "导师", "父母", "关系", "房贷", "月供", "首付", "公司", "会议", "租金")):
            errors.append(f"event shock row {index} lacks a concrete scene, year, or evidence cue")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Life Fork report insight specificity.")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    errors = validate(args.report)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
