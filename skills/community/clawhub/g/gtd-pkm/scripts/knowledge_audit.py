#!/usr/bin/env python3
"""Audit a knowledge repository and suggest GTD-aligned improvements."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


EXPECTED_TOP_LEVEL = [
    "00-收集箱",
    "10-工作",
    "20-项目",
    "30-记录",
    "40-学习",
    "50-知识输出",
    "98-归档",
    "99-资源库",
]

IGNORE_DIRS = {
    ".git",
    ".obsidian",
    ".openclaw",
    ".agents",
    ".claude",
    ".codex",
    ".clawhub",
    "node_modules",
    ".trash",
    "__pycache__",
}
INVALID_FILENAME_CHARS = set('<>:"|?*')
HOUSEKEEPING_FILES = {
    "ReadMe.md",
    "README.md",
    "AGENTS.md",
    "HEARTBEAT.md",
    "MEMORY.md",
    "knowledge_audit_report.md",
    "knowledge_structure_report.md",
}


@dataclass
class Suggestion:
    path: str
    reason: str
    target: str


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name in HOUSEKEEPING_FILES:
            continue
        yield path


def parse_frontmatter_tags(text: str) -> list[str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return []
    fm = match.group(1)
    tag_match = re.search(r"^tags:\n((?:\s*-\s.*(?:\n|$))+)", fm, re.M)
    if not tag_match:
        return []
    tags = []
    for line in tag_match.group(1).splitlines():
        tag = re.sub(r"^\s*-\s*", "", line).strip()
        if tag:
            tags.append(tag)
    return tags


def infer_target(relative_path: str, tags: list[str]) -> Suggestion | None:
    parts = relative_path.split("/")
    name = parts[-1]
    name_lc = name.lower()

    if parts[0] in EXPECTED_TOP_LEVEL:
        return None

    text = " ".join([relative_path, " ".join(tags)])
    checks = [
        ("日志", "30-记录/01-日志", "包含日志特征"),
        ("日记", "30-记录/01-日志", "包含日志特征"),
        ("周报", "30-记录/03-周报", "包含周报特征"),
        ("会议", "30-记录/04-会议", "包含会议特征"),
        ("沟通", "30-记录/04-会议", "包含会议特征"),
        ("灵感", "30-记录/02-灵感", "包含灵感特征"),
        ("读书", "40-学习/01-读书笔记", "包含读书特征"),
        ("课程", "40-学习/02-课程笔记", "包含课程特征"),
        ("开源", "40-学习/05-开源仓库", "包含开源特征"),
        ("repo", "40-学习/05-开源仓库", "包含开源特征"),
        ("文章笔记", "40-学习/03-技术", "属于学习笔记"),
        ("技术", "40-学习/03-技术", "属于技术学习"),
        ("方法论", "40-学习/04-方法论", "属于方法论学习"),
        ("项目", "20-项目", "更像项目文档"),
        ("方案", "20-项目", "更像项目文档"),
        ("需求", "10-工作", "更像工作事项"),
        ("迭代", "10-工作", "更像工作事项"),
        ("工作", "10-工作", "更像工作事项"),
        ("输出", "50-知识输出/01-文章", "更像成品输出"),
        ("公众号", "50-知识输出/01-文章", "更像成品输出"),
        ("微信", "99-资源库/02-文章", "更像原始资料"),
        ("知乎", "99-资源库/02-文章", "更像原始资料"),
        ("b站", "99-资源库/04-视频", "更像原始资料"),
    ]

    for keyword, target, reason in checks:
        if keyword in text or keyword in name_lc:
            return Suggestion(relative_path, reason, target)

    return Suggestion(relative_path, "无法明确判断，先放入收集箱等待澄清", "00-收集箱")


def build_report(root: Path) -> str:
    markdown_files = list(iter_markdown_files(root))
    top_level_counter = Counter()
    tag_counter = Counter()
    missing_tags: list[str] = []
    filename_issues: list[str] = []
    misplaced: list[Suggestion] = []
    root_level_notes: list[str] = []
    unreadable_files: list[str] = []

    for path in markdown_files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            unreadable_files.append(rel)
            continue
        top_level = rel.split("/")[0]
        top_level_counter[top_level] += 1
        tags = parse_frontmatter_tags(text)
        if tags:
            tag_counter.update(tags)
        else:
            missing_tags.append(rel)

        if any(char in path.name for char in INVALID_FILENAME_CHARS):
            filename_issues.append(rel)

        if "/" not in rel and path.name not in HOUSEKEEPING_FILES:
            root_level_notes.append(rel)

        suggestion = infer_target(rel, tags)
        if suggestion:
            misplaced.append(suggestion)

    missing_dirs = [d for d in EXPECTED_TOP_LEVEL if not (root / d).exists()]
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# GTD 知识库审计报告",
        "",
        f"- 审计时间：{report_time}",
        f"- 根目录：{root}",
        f"- Markdown 文件数：{len(markdown_files)}",
        "",
        "## 顶层目录覆盖",
        "",
    ]

    for name in EXPECTED_TOP_LEVEL:
        status = "✅" if (root / name).exists() else "❌"
        lines.append(f"- {status} `{name}`")

    if missing_dirs:
        lines.extend(["", "## 缺失目录", ""])
        for item in missing_dirs:
            lines.append(f"- `{item}`")

    lines.extend(["", "## 顶层 Markdown 分布", ""])
    for name, count in sorted(top_level_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{name}`：{count}")

    if tag_counter:
        lines.extend(["", "## Frontmatter 标签统计", ""])
        for tag, count in tag_counter.most_common(20):
            lines.append(f"- `{tag}`：{count}")

    if missing_tags:
        lines.extend(["", "## 缺少 Frontmatter 标签的文件", ""])
        for rel in missing_tags[:30]:
            lines.append(f"- `{rel}`")
        if len(missing_tags) > 30:
            lines.append(f"- 其余 {len(missing_tags) - 30} 个文件未展开")

    if filename_issues:
        lines.extend(["", "## 命名风险", ""])
        for rel in filename_issues:
            lines.append(f"- `{rel}`：文件名包含跨平台风险字符")

    if unreadable_files:
        lines.extend(["", "## 不可读文件", ""])
        for rel in unreadable_files:
            lines.append(f"- `{rel}`：可能是断开的软链接或当前环境不可访问")

    if root_level_notes:
        lines.extend(["", "## 根目录待分拣文件", ""])
        for rel in root_level_notes:
            lines.append(f"- `{rel}`")

    if misplaced:
        lines.extend(["", "## GTD 迁移建议", ""])
        for item in misplaced[:40]:
            lines.append(
                f"- `{item.path}` → `{item.target}`：{item.reason}"
            )
        if len(misplaced) > 40:
            lines.append(f"- 其余 {len(misplaced) - 40} 条建议未展开")

    lines.extend(
        [
            "",
            "## 优先动作",
            "",
            "- 先补齐缺失的顶层目录，再做迁移",
            "- 先处理根目录散落文件和命名风险",
            "- 先统一标签，再批量整理旧笔记",
            "- 大搬家前先用 Git 留快照",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-root", required=True, help="知识库根目录")
    parser.add_argument(
        "--output",
        help="报告输出路径，默认写到知识库根目录下的 knowledge_audit_report.md",
    )
    args = parser.parse_args()

    root = Path(args.knowledge_root).expanduser().resolve()
    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else root / "knowledge_audit_report.md"
    )
    report = build_report(root)
    output.write_text(report, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
