#!/usr/bin/env python3
"""Validate archetype library and Magic Score scaffolding."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]

ARCHETYPE_FILE = ROOT / "references" / "life-archetype-library.md"
COMPOSER_FILE = ROOT / "references" / "archetype-composer.md"
TENSION_FILE = ROOT / "references" / "archetype-tension-axes.md"
MAGIC_FILE = ROOT / "references" / "magic-score-rubric.md"
VERDICT_FILE = ROOT / "references" / "verdict-rewrite-patterns.md"
SKILL_FILE = ROOT / "SKILL.md"
TEMPLATE_FILE = ROOT / "templates" / "life-fork-simulation-report.md"
QUALITY_FILE = ROOT / "templates" / "quality-scorecard.md"
DIALOGUE_FILE = ROOT / "examples" / "real-dialogue-flows.md"
REGRESSION_FILE = ROOT / "examples" / "magic-score-regression.md"
FINAL_REVIEW_DIR = WORKSPACE / "final-review"

ARCHETYPES = [
    "城市折返",
    "海外未竟",
    "AI 错过窗口",
    "买房绑定",
    "体制安全",
    "大厂牌桌",
    "旧公司离开",
    "小城回流",
    "创业未尝试",
]

REQUIRED_ARCHETYPE_FIELDS = [
    "隐藏不甘",
    "典型判词",
    "事件冲击",
    "幻想校正",
    "可回收资产",
]

MAGIC_DIMENSIONS = [
    "首屏判词击中",
    "不可替换",
    "隐秘交换",
    "具体事件承托",
]

TENSION_AXES = [
    "熟悉环境 vs 陌生竞争",
    "安全感 vs 可见度",
    "国际身份 vs 中文舒适区",
    "作品资产 vs 收藏观察",
    "家庭托底 vs 个人扩张",
    "现金流底盘 vs 高波动机会",
    "组织背书 vs 独立判断",
    "身体节奏 vs 快速跃迁",
    "固定身份 vs 新技术身份",
    "城市锚点 vs 流动弹性",
]

REGRESSION_TOPICS = [
    "去北京",
    "留学后没有回国",
    "那年没买房",
    "当年进了体制",
    "没有离开上一家公司",
    "2023 年认真做 AI",
    "小城回流",
    "创业未尝试",
]

UNKNOWN_COMPOSITION_TOPICS = [
    "如果当年没有因为家里回老家",
    "如果当年没有转管理岗",
    "如果身体那年没垮掉",
    "如果当年没有结束那段关系",
]

CONCRETE_ANCHORS = [
    "2016",
    "2018",
    "2020-2022",
    "2023",
    "Brexit",
    "疫情",
    "签证",
    "月供",
    "裁员",
    "AI",
    "房价",
    "旧公司",
    "北京",
    "海外",
    "英国",
    "深圳",
    "体制",
    "上一家公司",
    "收藏夹",
    "作品窗口",
    "平台会议",
    "月供",
    "房子",
    "小城",
    "创业",
    "客户反馈",
    "父母",
    "一线城市",
    "家乡",
    "管理岗",
    "身体中断",
    "关系",
]

GENERIC_VERDICT_PHRASES = [
    "你放不下的是过去的自己",
    "看清机会和代价",
    "这段经历塑造了你",
    "现在开始也可以",
]

EVENT_ACTION_CUES = [
    "找",
    "问",
    "写",
    "发给",
    "记录",
    "测试",
    "做一张",
    "约",
    "看",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def section_for(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## 原型 \d+：{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"^## 原型 \d+：", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(text)
    return text[match.start() : end]


def validate_archetype_file(errors: list[str]) -> None:
    text = read(ARCHETYPE_FILE)
    for archetype in ARCHETYPES:
        block = section_for(text, archetype)
        if not block:
            fail(errors, f"archetype library missing archetype: {archetype}")
            continue
        for field in REQUIRED_ARCHETYPE_FIELDS:
            if field not in block:
                fail(errors, f"archetype {archetype} missing field: {field}")
        if len(re.findall(r"^- ", block, flags=re.MULTILINE)) < 4:
            fail(errors, f"archetype {archetype} should contain at least four event bullets")

    for term in ("混合原型处理", "原型命中要求", "承载物", "隐秘交换", "时间或事件承托"):
        if term not in text:
            fail(errors, f"archetype library missing rule: {term}")


def validate_tension_file(errors: list[str]) -> None:
    text = read(TENSION_FILE)
    for axis in TENSION_AXES:
        if axis not in text:
            fail(errors, f"tension axes missing axis: {axis}")
    for term in ("隐秘交换", "承载物", "回收资产", "张力轴组合示例", "禁止退化"):
        if term not in text:
            fail(errors, f"tension axes missing rule: {term}")


def validate_composer_file(errors: list[str]) -> None:
    text = read(COMPOSER_FILE)
    for term in (
        "使用时机",
        "临时原型输出格式",
        "组合公式",
        "承载物",
        "隐秘交换",
        "判词母句",
        "幻想校正",
        "事件冲击",
        "未知题组合示例",
        "回到固定原型的条件",
    ):
        if term not in text:
            fail(errors, f"archetype composer missing rule: {term}")
    example_rows = markdown_table_rows(section_between(text, "未知题组合示例"))
    if len(example_rows) < len(UNKNOWN_COMPOSITION_TOPICS):
        fail(errors, "archetype composer should contain unknown-topic composition examples")
    example_topics = {row.get("用户问题", "") for row in example_rows}
    for topic in UNKNOWN_COMPOSITION_TOPICS:
        if topic not in example_topics:
            fail(errors, f"archetype composer missing unknown topic: {topic}")


def validate_magic_file(errors: list[str]) -> None:
    text = read(MAGIC_FILE)
    for dimension in MAGIC_DIMENSIONS:
        if dimension not in text:
            fail(errors, f"magic rubric missing dimension: {dimension}")
    for term in (
        "18-20 分",
        "16-17 分",
        "15 分及以下",
        "任一维度低于 4 分",
        "life-archetype-library.md",
        "verdict-rewrite-patterns.md",
        "替换测试",
        "交换测试",
        "事件测试",
    ):
        if term not in text:
            fail(errors, f"magic rubric missing threshold/rule: {term}")

    verdict = read(VERDICT_FILE)
    for term in ("判词四件套", "替换测试", "命中感三问", "弱判词与强判词", "失败判词"):
        if term not in verdict:
            fail(errors, f"verdict rewrite patterns missing section: {term}")


def validate_skill_and_template_links(errors: list[str]) -> None:
    skill = read(SKILL_FILE)
    template = read(TEMPLATE_FILE)
    quality = read(QUALITY_FILE)
    dialogue = read(DIALOGUE_FILE)
    for link in (
        "references/archetype-tension-axes.md",
        "references/life-archetype-library.md",
        "references/archetype-composer.md",
        "references/verdict-rewrite-patterns.md",
        "references/magic-score-rubric.md",
        "scripts/validate_magic_score.py",
    ):
        if link not in skill:
            fail(errors, f"SKILL.md missing magic workflow link: {link}")
    for term in ("张力轴识别", "原型识别", "Magic Score", "隐藏不甘", "隐秘交换"):
        if term not in quality:
            fail(errors, f"quality scorecard missing magic term: {term}")
    for term in ("## 1. 你真正放不下的是什么", "## 2. 三种结果", "## 3. 事件冲击卡", "## 5. 30 天验证实验"):
        if term not in template:
            fail(errors, f"simulation template missing user-report term: {term}")
    for term in ("原型回归映射", "Magic 回归映射", "判词替换测试", "主原型", "隐藏不甘", "主张力轴"):
        if term not in dialogue:
            fail(errors, f"dialogue regression missing archetype term: {term}")


def validate_verdict_text(label: str, verdict: str, errors: list[str]) -> None:
    verdict = verdict.strip()
    if len(verdict) < 42:
        fail(errors, f"{label} verdict is too short")
    if not any(anchor in verdict for anchor in CONCRETE_ANCHORS):
        fail(errors, f"{label} verdict lacks concrete anchor: {verdict}")
    if "换成" not in verdict and "拿走" not in verdict and "换" not in verdict:
        fail(errors, f"{label} verdict lacks hidden exchange: {verdict}")
    for phrase in GENERIC_VERDICT_PHRASES:
        if phrase in verdict:
            fail(errors, f"{label} verdict contains generic phrase: {phrase}")


def section_between(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return ""
    next_heading = text.find("\n## ", start + len(marker))
    if next_heading == -1:
        return text[start:]
    return text[start:next_heading]


def markdown_table_rows(section: str) -> list[dict[str, str]]:
    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|") and "---" not in line
    ]
    if len(lines) < 2:
        return []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def validate_event_shock_row(row: dict[str, str], errors: list[str]) -> None:
    label = row.get("Demo", "unknown")
    required_fields = ["事件锚点", "生活场景", "现实代价", "情绪代价", "误判点", "今天验证"]
    for field in required_fields:
        value = row.get(field, "")
        if len(value) < 18:
            fail(errors, f"{label} event shock field too thin: {field}")
    combined = "".join(row.get(field, "") for field in required_fields)
    if len(combined) < 180:
        fail(errors, f"{label} event shock row too thin: {len(combined)} chars")
    if not any(anchor in combined for anchor in CONCRETE_ANCHORS):
        fail(errors, f"{label} event shock lacks concrete anchor")
    if not any(cue in row.get("今天验证", "") for cue in EVENT_ACTION_CUES):
        fail(errors, f"{label} event shock lacks concrete validation action")
    for weak in ("提升", "规划", "关注", "多了解"):
        if weak in row.get("今天验证", ""):
            fail(errors, f"{label} event shock action is too vague: {weak}")


def validate_regression(errors: list[str]) -> None:
    text = read(REGRESSION_FILE)
    for topic in REGRESSION_TOPICS:
        if topic not in text:
            fail(errors, f"magic regression missing topic: {topic}")
    for archetype in ARCHETYPES:
        if archetype not in text:
            fail(errors, f"magic regression should cover common archetype: {archetype}")
    if text.count("20 / 20") < 8:
        fail(errors, "magic regression should include eight 20 / 20 score rows")
    verdicts = re.findall(r"判词：(.+)", text)
    if len(verdicts) < 8:
        fail(errors, "magic regression should contain at least eight verdict lines")
    for index, verdict in enumerate(verdicts, start=1):
        validate_verdict_text(f"magic regression {index}", verdict, errors)

    event_section = section_between(text, "事件冲击回归")
    event_rows = markdown_table_rows(event_section)
    if len(event_rows) < len(REGRESSION_TOPICS):
        fail(errors, f"event shock regression should contain at least {len(REGRESSION_TOPICS)} rows")
    covered_topics = {row.get("Demo", "") for row in event_rows}
    for topic in REGRESSION_TOPICS:
        if topic not in covered_topics:
            fail(errors, f"event shock regression missing topic: {topic}")
    for row in event_rows:
        validate_event_shock_row(row, errors)

    unknown_section = section_between(text, "未知题组合回归")
    unknown_rows = markdown_table_rows(unknown_section)
    if len(unknown_rows) < len(UNKNOWN_COMPOSITION_TOPICS):
        fail(errors, "unknown-topic composition regression has too few rows")
    covered_unknown = {row.get("用户问题", "") for row in unknown_rows}
    for topic in UNKNOWN_COMPOSITION_TOPICS:
        if topic not in covered_unknown:
            fail(errors, f"unknown-topic composition regression missing topic: {topic}")
    for row in unknown_rows:
        label = row.get("用户问题", "unknown")
        min_lengths = {
            "临时原型名": 8,
            "岔路动作": 4,
            "系统切换": 8,
            "主张力轴": 10,
            "隐藏不甘": 14,
            "判词母句": 42,
            "可回收资产": 8,
        }
        for field, min_length in min_lengths.items():
            if len(row.get(field, "")) < min_length:
                fail(errors, f"{label} unknown composition field too thin: {field}")
        validate_verdict_text(f"{label} unknown composition", row.get("判词母句", ""), errors)


def validate_report_verdicts(errors: list[str]) -> None:
    if not FINAL_REVIEW_DIR.exists():
        return
    report_paths = sorted(FINAL_REVIEW_DIR.glob("life-fork-*-user-report-*/report.md"))
    if not report_paths:
        return
    for path in report_paths:
        text = read(path)
        match = re.search(r"^判词：(.+)$", text, flags=re.MULTILINE)
        if not match:
            fail(errors, f"{path} missing report verdict")
            continue
        validate_verdict_text(path.name, match.group(1), errors)


def main() -> int:
    errors: list[str] = []
    validate_archetype_file(errors)
    validate_tension_file(errors)
    validate_composer_file(errors)
    validate_magic_file(errors)
    validate_skill_and_template_links(errors)
    validate_regression(errors)
    validate_report_verdicts(errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
