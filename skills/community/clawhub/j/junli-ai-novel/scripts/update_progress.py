#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 task_log.md、章节规划和伏笔记录。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from chapter_text import extract_body_section, is_chapter_file
except ModuleNotFoundError:
    from scripts.chapter_text import extract_body_section, is_chapter_file


STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"

LEGACY_OUTLINE_PATH = "docs/大纲.md"
PROJECT_OUTLINE_PATH = "docs/项目总纲.md"
CHAPTER_PLAN_PATH = "docs/章节规划.md"


def resolve_project_outline_path(project_dir: Path) -> Path | None:
    primary = project_dir / PROJECT_OUTLINE_PATH
    legacy = project_dir / LEGACY_OUTLINE_PATH
    if primary.exists():
        return primary
    if legacy.exists():
        return legacy
    return None


def resolve_chapter_plan_path(project_dir: Path) -> Path | None:
    primary = project_dir / CHAPTER_PLAN_PATH
    legacy = project_dir / LEGACY_OUTLINE_PATH
    if primary.exists():
        return primary
    if legacy.exists():
        return legacy
    return None


def extract_body(content: str) -> str:
    return extract_body_section(content)


def count_story_units(text: str) -> int:
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    latin_words = re.findall(r"[A-Za-z0-9_]+", text)
    return len(chinese_chars) + len(latin_words)


def compute_manuscript_stats(project_path: Path) -> tuple[int, int]:
    manuscript_dir = project_path / "manuscript"
    if not manuscript_dir.exists():
        return 0, 0

    chapter_files = [path for path in sorted(manuscript_dir.glob("*.md")) if is_chapter_file(path)]
    total_words = 0
    for chapter_path in chapter_files:
        content = chapter_path.read_text(encoding="utf-8")
        total_words += count_story_units(extract_body(content))
    return len(chapter_files), total_words


def update_field(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}.*$"
    replacement = f"- {label}{value}"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    current_state = "## 当前状态\n"
    if current_state in text:
        return text.replace(current_state, current_state + replacement + "\n", 1)
    return text.rstrip() + "\n\n## 当前状态\n" + replacement + "\n"


def replace_section(text: str, header: str, body_lines: list[str]) -> str:
    section_body = "\n".join(body_lines).rstrip() + "\n"
    pattern = rf"(?ms)(^## {re.escape(header)}\n)(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    if match:
        return text[: match.start(2)] + section_body + text[match.end(2) :]
    return text.rstrip() + f"\n\n## {header}\n" + section_body


def update_todo_subsection(text: str, header: str, chapter_label: str, new_line: str | None = None) -> str:
    pattern = rf"(?ms)(^### {re.escape(header)}\n)(.*?)(?=^### |\n## |\Z)"
    match = re.search(pattern, text)
    lines: list[str] = []
    if match:
        lines = [line for line in match.group(2).splitlines() if line.strip()]
        lines = [line for line in lines if "[X]" not in line]
        lines = [line for line in lines if chapter_label not in line]
        if new_line:
            lines.append(new_line)
        body = ("\n".join(lines) + "\n") if lines else "\n"
        return text[: match.start(2)] + body + text[match.end(2) :]

    suffix = f"\n### {header}\n"
    if new_line:
        suffix += new_line + "\n"
    return text.rstrip() + suffix


def build_todo_line(
    chapter_num: int,
    chapter_title: str | None,
    core_event: str | None = None,
    word_count: int | None = None,
    status: str = STATUS_IN_PROGRESS,
) -> str:
    title = chapter_title or "未命名章节"
    detail = f" - {core_event}" if core_event else ""
    if status == STATUS_DONE:
        word_display = str(word_count) if word_count is not None else "?"
        return f"- [x] 第{chapter_num}章：{title}{detail}（{word_display}字）"
    return f"- [ ] 第{chapter_num}章：{title}{detail}"


def update_recent_summaries(text: str, chapter_label: str, summary: str | None) -> str:
    if not summary:
        return text

    body_match = re.search(r"(?ms)^## 最近三章摘要\n(.*?)(?=^## |\Z)", text)
    lines: list[str] = []
    if body_match:
        lines = [line for line in body_match.group(1).splitlines() if line.strip() and line.strip() != "- 暂无"]

    new_line = f"- {chapter_label}：{summary}"
    filtered = [line for line in lines if not line.startswith(f"- {chapter_label}：")]
    lines = [new_line] + filtered[:2]
    return replace_section(text, "最近三章摘要", lines or ["- 暂无"])


def update_task_log_active_plots(text: str, plot_note: str | None, chapter_label: str) -> str:
    if not plot_note:
        return text

    pattern = r"(?ms)(^## 活跃伏笔\n)(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    header_row = "| 伏笔名称 | 埋设章节 | 当前状态 | 关联章节 |"
    divider_row = "|----------|----------|----------|----------|"
    new_row = f"| {plot_note} | {chapter_label} | 待回收 | 待定 |"

    if match:
        lines = [line for line in match.group(2).splitlines() if line.strip()]
        data_rows: list[str] = []
        for line in lines:
            if line.startswith("| 伏笔名称 |") or set(line.replace("|", "").replace("-", "").strip()) == set():
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 3:
                cells.append("待定")
            if len(cells) >= 4:
                data_rows.append("| " + " | ".join(cells[:4]) + " |")
        if new_row not in data_rows:
            data_rows.append(new_row)
        body_lines = [header_row, divider_row] + data_rows
        return text[: match.start(2)] + "\n".join(body_lines) + "\n" + text[match.end(2) :]

    return text.rstrip() + (
        "\n\n## 活跃伏笔\n"
        f"{header_row}\n"
        f"{divider_row}\n"
        f"{new_row}\n"
    )


def append_plot_note(project_path: Path, plot_note: str, chapter_label: str) -> None:
    plot_path = project_path / "plot" / "伏笔记录.md"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    if not plot_path.exists():
        plot_path.write_text(
            "# 伏笔记录\n\n## 活跃伏笔\n| 伏笔名称 | 埋设章节 | 伏笔类型 | 关联章节 |\n|----------|----------|----------|----------|\n",
            encoding="utf-8",
        )

    content = plot_path.read_text(encoding="utf-8")
    row = f"| {plot_note} | {chapter_label} | 待定 | 待回收 |"
    if row in content:
        return

    if "## 已回收伏笔" in content:
        active, recovered = content.split("## 已回收伏笔", 1)
        active = active.rstrip() + "\n" + row + "\n\n"
        plot_path.write_text(active + "## 已回收伏笔" + recovered, encoding="utf-8")
    else:
        plot_path.write_text(content.rstrip() + "\n" + row + "\n", encoding="utf-8")


def parse_planned_total(text: str) -> int | None:
    estimate_match = re.search(r"预计章节数.*?(\d+(?:\s*-\s*\d+)*)", text)
    if estimate_match:
        numbers = [int(item) for item in re.findall(r"\d+", estimate_match.group(1))]
        if numbers:
            return max(numbers)

    chapter_numbers = [int(item) for item in re.findall(r"\|\s*第(\d+)章\s*\|", text)]
    if chapter_numbers:
        return max(chapter_numbers)
    return None


def update_chapter_plan_table(
    text: str,
    chapter_num: int,
    chapter_title: str | None,
    core_event: str | None,
    hook: str | None,
    word_count: int | None,
    status_label: str,
) -> str:
    match = re.search(r"(?ms)(^## 章节规划\n\n\|.*?\n\|[-| ]+\n)(.*?)(?=^\n## |\Z)", text)
    if not match:
        return text

    prefix = match.group(1)
    body = match.group(2)
    rows = [line for line in body.splitlines() if line.strip()]
    updated_rows: list[str] = []
    target_label = f"第{chapter_num}章"
    found = False

    for row in rows:
        row_match = re.match(r"^\|\s*第(\d+)章\s*\|(.*)\|$", row)
        if not row_match:
            updated_rows.append(row)
            continue

        current_num = int(row_match.group(1))
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) < 6:
            updated_rows.append(row)
            continue

        if current_num == chapter_num:
            found = True
            cells[0] = target_label
            if chapter_title:
                cells[1] = chapter_title
            if core_event:
                cells[2] = core_event
            if hook:
                cells[3] = hook
            if word_count is not None:
                cells[4] = str(word_count)
            cells[5] = status_label
            updated_rows.append("| " + " | ".join(cells[:6]) + " |")
        else:
            updated_rows.append(row)

    if not found:
        updated_rows.append(
            "| "
            + " | ".join(
                [
                    target_label,
                    chapter_title or "",
                    core_event or "",
                    hook or "",
                    str(word_count) if word_count is not None else "",
                    status_label,
                ]
            )
            + " |"
        )

    table = prefix + "\n".join(updated_rows).rstrip() + "\n"
    return text[: match.start()] + table + text[match.end() :]


def upsert_outline_summary_section(text: str, chapter_num: int, chapter_title: str | None, summary: str | None) -> str:
    if not summary:
        return text

    title = chapter_title or "未命名章节"
    new_header = f"### 第{chapter_num}章：{title}"
    new_block = f"{new_header}\n**摘要**：{summary}"
    blocks: dict[int, str] = {}
    marker = "## 章节摘要"
    marker_index = text.find(marker)
    if marker_index != -1:
        body_start = marker_index + len(marker)
        next_match = re.search(r"(?m)^## ", text[body_start:])
        body_end = body_start + next_match.start() if next_match else len(text)
        body = text[body_start:body_end]
        for block in re.findall(r"(?ms)^### 第\d+章[：:].*?(?=^### 第\d+章|^## |\Z)", body):
            header_match = re.match(r"^### 第(\d+)章[：:]", block)
            if not header_match:
                continue
            blocks[int(header_match.group(1))] = block.strip()

    blocks[chapter_num] = new_block
    ordered_blocks = [blocks[key] for key in sorted(blocks)]
    section_body = "（后续章节摘要依次追加）\n\n" + "\n\n".join(ordered_blocks) + "\n"

    if marker_index != -1:
        body_start = marker_index + len(marker)
        next_match = re.search(r"(?m)^## ", text[body_start:])
        body_end = body_start + next_match.start() if next_match else len(text)
        return text[:marker_index] + marker + "\n\n" + section_body + text[body_end:]

    return text.rstrip() + "\n\n## 章节摘要\n" + section_body


def update_chapter_plan(
    project_dir: Path,
    chapter_num: int,
    chapter_title: str | None,
    summary: str | None,
    word_count: int | None,
    core_event: str | None,
    hook: str | None,
    chapter_count: int,
    total_words: int,
    status: str = STATUS_DONE,
) -> None:
    chapter_plan_path = resolve_chapter_plan_path(project_dir)
    if chapter_plan_path is None:
        return

    text = chapter_plan_path.read_text(encoding="utf-8")
    chapter_label = f"第{chapter_num}章"
    text = update_todo_subsection(text, "待创作", chapter_label)
    if status == STATUS_IN_PROGRESS:
        text = update_todo_subsection(
            text,
            "进行中",
            chapter_label,
            build_todo_line(chapter_num, chapter_title, core_event=core_event, status=STATUS_IN_PROGRESS),
        )
        text = update_todo_subsection(text, "已完成", chapter_label)
        text = update_chapter_plan_table(
            text,
            chapter_num,
            chapter_title,
            core_event,
            hook,
            word_count,
            status_label="进行中",
        )
    else:
        text = update_todo_subsection(text, "进行中", chapter_label)
        text = update_todo_subsection(
            text,
            "已完成",
            chapter_label,
            build_todo_line(
                chapter_num,
                chapter_title,
                core_event=core_event,
                word_count=word_count,
                status=STATUS_DONE,
            ),
        )
        text = update_chapter_plan_table(
            text,
            chapter_num,
            chapter_title,
            core_event,
            hook,
            word_count,
            status_label="已完成",
        )
    text = re.sub(r"(?m)^- 已完成章节数：.*$", f"- 已完成章节数：{chapter_count} 章", text)
    text = re.sub(r"(?m)^- 累计字数：.*$", f"- 累计字数：{total_words} 字", text)
    planned_total = parse_planned_total(text)
    if planned_total and planned_total > 0:
        progress = min(100, round(chapter_count / planned_total * 100))
        text = re.sub(r"(?m)^- 完成进度：.*$", f"- 完成进度：{progress}%", text)

    if summary and status == STATUS_DONE:
        text = upsert_outline_summary_section(text, chapter_num, chapter_title, summary)

    chapter_plan_path.write_text(text, encoding="utf-8")


def update_progress(
    project_path: str,
    chapter_num: int,
    word_count: int | None = None,
    chapter_title: str | None = None,
    summary: str | None = None,
    core_event: str | None = None,
    hook: str | None = None,
    next_goal: str | None = None,
    viewpoint: str | None = None,
    protagonist_location: str | None = None,
    protagonist_state: str | None = None,
    stage: str | None = None,
    target_total_words: str | None = None,
    target_volumes: str | None = None,
    current_volume: str | None = None,
    current_phase: str | None = None,
    phase_goal: str | None = None,
    pending_setting_sync: str | None = None,
    plot_note: str | None = None,
    status: str = STATUS_DONE,
) -> None:
    project_dir = Path(project_path).expanduser().resolve()
    log_path = project_dir / "task_log.md"

    if not log_path.exists():
        raise FileNotFoundError(f"未找到 task_log.md: {log_path}")

    content = log_path.read_text(encoding="utf-8")
    chapter_label = f"第{chapter_num}章"
    latest_chapter = chapter_label if not chapter_title else f"{chapter_label}《{chapter_title}》"

    chapter_count, total_words = compute_manuscript_stats(project_dir)
    if word_count and total_words == 0:
        total_words = word_count
        chapter_count = max(chapter_count, 1)

    content = update_field(content, "创作阶段：", stage or "正文创作中")
    content = update_field(content, "当前处理章节：", latest_chapter if status == STATUS_IN_PROGRESS else "无")
    if status == STATUS_DONE:
        content = update_field(content, "最新章节：", latest_chapter)
        content = update_field(content, "累计完成章节：", str(max(chapter_count, chapter_num)))
        content = update_field(content, "累计完成字数：", str(total_words))
    else:
        content = update_field(content, "累计完成章节：", str(chapter_count))
        content = update_field(content, "累计完成字数：", str(total_words))

    if next_goal:
        content = update_field(content, "下一章目标：", next_goal)
    if viewpoint:
        content = update_field(content, "当前视角：", viewpoint)
    if protagonist_location:
        content = update_field(content, "主角位置：", protagonist_location)
    if protagonist_state:
        content = update_field(content, "主角状态：", protagonist_state)
    if target_total_words is not None:
        content = update_field(content, "目标总字数：", str(target_total_words))
    if target_volumes is not None:
        content = update_field(content, "目标卷数：", str(target_volumes))
    if current_volume is not None:
        content = update_field(content, "当前卷：", current_volume)
    if current_phase is not None:
        content = update_field(content, "当前阶段：", current_phase)
    if phase_goal is not None:
        content = update_field(content, "当前阶段目标：", phase_goal)
    if pending_setting_sync is not None:
        content = update_field(content, "设定变更待同步：", pending_setting_sync)

    if status == STATUS_DONE:
        content = update_recent_summaries(content, latest_chapter, summary)
        content = update_task_log_active_plots(content, plot_note, chapter_label)
    log_path.write_text(content, encoding="utf-8")
    update_chapter_plan(
        project_dir,
        chapter_num,
        chapter_title,
        summary,
        word_count,
        core_event,
        hook,
        max(chapter_count, chapter_num) if status == STATUS_DONE else chapter_count,
        total_words,
        status=status,
    )

    if plot_note and status == STATUS_DONE:
        append_plot_note(project_dir, plot_note, chapter_label)

    action = "进入创作中" if status == STATUS_IN_PROGRESS else f"已完成，累计 {total_words} 字"
    print(f"进度已更新：{latest_chapter}，{action}")


def update_governance_state(
    project_path: str,
    *,
    target_total_words: str | None = None,
    target_volumes: str | None = None,
    current_volume: str | None = None,
    current_phase: str | None = None,
    phase_goal: str | None = None,
    pending_setting_sync: str | None = None,
    clear_pending_setting_sync: bool = False,
) -> None:
    project_dir = Path(project_path).expanduser().resolve()
    log_path = project_dir / "task_log.md"

    if not log_path.exists():
        raise FileNotFoundError(f"未找到 task_log.md: {log_path}")

    content = log_path.read_text(encoding="utf-8")

    if target_total_words is not None:
        content = update_field(content, "目标总字数：", str(target_total_words))
    if target_volumes is not None:
        content = update_field(content, "目标卷数：", str(target_volumes))
    if current_volume is not None:
        content = update_field(content, "当前卷：", current_volume)
    if current_phase is not None:
        content = update_field(content, "当前阶段：", current_phase)
    if phase_goal is not None:
        content = update_field(content, "当前阶段目标：", phase_goal)

    if clear_pending_setting_sync:
        content = update_field(content, "设定变更待同步：", "无")
    elif pending_setting_sync is not None:
        content = update_field(content, "设定变更待同步：", pending_setting_sync)

    log_path.write_text(content, encoding="utf-8")
    print(f"长篇治理状态已更新：{project_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="更新小说项目进度")
    parser.add_argument("project_path", help="项目根目录")
    parser.add_argument("chapter_num", type=int, help="最新完成章节号")
    parser.add_argument("--word-count", type=int, help="当前章节字数，可选")
    parser.add_argument("--chapter-title", help="章节标题")
    parser.add_argument("--summary", help="本章摘要")
    parser.add_argument("--core-event", help="本章核心事件，用于同步章节规划表格")
    parser.add_argument("--hook", help="本章悬念钩子，用于同步章节规划表格")
    parser.add_argument("--next-goal", help="下一章目标")
    parser.add_argument("--viewpoint", help="当前视角人物")
    parser.add_argument("--protagonist-location", help="主角位置")
    parser.add_argument("--protagonist-state", help="主角状态")
    parser.add_argument("--stage", help="创作阶段")
    parser.add_argument("--target-total-words", help="目标总字数，例如 3000000 或 300万")
    parser.add_argument("--target-volumes", help="目标卷数")
    parser.add_argument("--current-volume", help="当前卷，例如 第一卷")
    parser.add_argument("--current-phase", help="当前阶段，例如 阶段1")
    parser.add_argument("--phase-goal", help="当前阶段目标")
    parser.add_argument("--pending-setting-sync", help="待同步的设定变更摘要")
    parser.add_argument("--plot-note", help="新增伏笔备注")
    parser.add_argument(
        "--status",
        choices=(STATUS_IN_PROGRESS, STATUS_DONE),
        default=STATUS_DONE,
        help="更新状态：进行中或已完成",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    update_progress(
        project_path=args.project_path,
        chapter_num=args.chapter_num,
        word_count=args.word_count,
        chapter_title=args.chapter_title,
        summary=args.summary,
        core_event=args.core_event,
        hook=args.hook,
        next_goal=args.next_goal,
        viewpoint=args.viewpoint,
        protagonist_location=args.protagonist_location,
        protagonist_state=args.protagonist_state,
        stage=args.stage,
        target_total_words=args.target_total_words,
        target_volumes=args.target_volumes,
        current_volume=args.current_volume,
        current_phase=args.current_phase,
        phase_goal=args.phase_goal,
        pending_setting_sync=args.pending_setting_sync,
        plot_note=args.plot_note,
        status=args.status,
    )
