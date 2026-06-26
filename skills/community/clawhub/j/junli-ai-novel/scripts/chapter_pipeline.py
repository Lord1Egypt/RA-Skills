#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一的新建、恢复、开写、质检与完结入口。"""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
LONGFORM_TARGET_WORDS = 1_000_000
LONGFORM_FALLBACK_TOTAL_WORDS = 300_000
LONGFORM_FALLBACK_CHAPTERS = 20

try:
    from chapter_text import is_chapter_file
    from check_chapter_wordcount import check_chapter
    from check_emotion_curve import analyze_chapter_emotion_curve
    from extract_thrills import analyze_thrills_and_poisons
    from new_project import create_novel_project, ensure_longform_governance_files
    from update_progress import (
        CHAPTER_PLAN_PATH,
        LEGACY_OUTLINE_PATH,
        PROJECT_OUTLINE_PATH,
        STATUS_DONE,
        STATUS_IN_PROGRESS,
        compute_manuscript_stats,
        resolve_chapter_plan_path,
        resolve_project_outline_path,
        update_governance_state,
        update_progress,
    )
except ModuleNotFoundError:
    from scripts.chapter_text import is_chapter_file
    from scripts.check_chapter_wordcount import check_chapter
    from scripts.check_emotion_curve import analyze_chapter_emotion_curve
    from scripts.extract_thrills import analyze_thrills_and_poisons
    from scripts.new_project import create_novel_project, ensure_longform_governance_files
    from scripts.update_progress import (
        CHAPTER_PLAN_PATH,
        LEGACY_OUTLINE_PATH,
        PROJECT_OUTLINE_PATH,
        STATUS_DONE,
        STATUS_IN_PROGRESS,
        compute_manuscript_stats,
        resolve_chapter_plan_path,
        resolve_project_outline_path,
        update_governance_state,
        update_progress,
    )


REQUIRED_MEMORY_BASE_FILES = (
    "task_log.md",
    "plot/伏笔记录.md",
    "plot/时间线.md",
)

LONGFORM_GOVERNANCE_FILES = (
    "docs/全书宪法.md",
    "docs/卷纲.md",
    "docs/阶段规划.md",
    "docs/变更日志.md",
)

RULE_LAYER_CATALOG: list[dict[str, Any]] = [
    {
        "id": "constitution",
        "title": "全书宪法与世界规则",
        "kind": "memory",
        "sources": ["docs/全书宪法.md", "docs/世界观.md", "docs/法则.md", "characters/*.md"],
        "summary": "最高优先级硬约束，控制终局、法则、关系边界与角色一致性。",
    },
    {
        "id": "structure-governance",
        "title": "结构治理规则",
        "kind": "memory",
        "sources": ["docs/项目总纲.md", "docs/卷纲.md", "docs/阶段规划.md", "docs/变更日志.md"],
        "summary": "约束全书主线、当前卷、当前阶段和结构变更，避免中长篇失控平推。",
    },
    {
        "id": "runtime-memory",
        "title": "项目运行记忆",
        "kind": "memory",
        "sources": ["task_log.md", "docs/章节规划.md", "plot/伏笔记录.md", "plot/时间线.md"],
        "summary": "服务章节续写、最近摘要、章节状态、活跃伏笔与时间线承接。",
    },
    {
        "id": "novel-lint",
        "title": "规则化文本巡检",
        "kind": "rule-set",
        "sources": ["rules/novel-lint/*.yaml", "references/rule-linting.md"],
        "summary": "抓 AI 套语、结尾升华、视角越权、对白说明感、解释腔和转场过密。",
    },
    {
        "id": "consistency",
        "title": "连贯性检查清单",
        "kind": "checklist",
        "sources": ["references/consistency.md", "references/quality-checklist.md"],
        "summary": "检查人物、伏笔、时间线、POV 边界和场景承接是否前后一致。",
    },
]

WORKFLOW_LAYER_CATALOG: list[dict[str, Any]] = [
    {
        "id": "next-chapter",
        "title": "续写下一章单入口",
        "steps": ["preflight", "resume", "plan", "compose", "start", "finish"],
        "summary": "把续写命令链包成一个入口；准备阶段和完结阶段都走同一条命令。",
    },
    {
        "id": "review",
        "title": "单章结构化审稿",
        "steps": ["check", "lint", "dialogue-pass", "consistency"],
        "summary": "把字数、情绪、爽毒点、规则命中、对白与连贯性合并成一份报告。",
    },
    {
        "id": "governance",
        "title": "长篇治理闭环",
        "steps": ["bootstrap-longform", "governance", "audit"],
        "summary": "负责补齐治理文件、同步卷/阶段状态并执行阶段或卷审计。",
    },
    {
        "id": "marketing",
        "title": "商业化包装入口",
        "steps": ["resume", "作者意图", "当前焦点", "项目总纲/章节规划", "补充提示词/参考"],
        "summary": "把营销包装所需的信息、提示词、词库和参考统一编译成营销 Brief。",
    },
]

COMMAND_LAYER_CATALOG: list[dict[str, Any]] = [
    {
        "group": "Layer",
        "commands": [
            "rules",
            "workflows",
            "commands",
        ],
    },
    {
        "group": "Workflow",
        "commands": [
            "next-chapter",
            "review",
            "marketing",
            "governance",
            "audit",
        ],
    },
    {
        "group": "Primitive",
        "commands": [
            "init",
            "preflight",
            "resume",
            "plan",
            "compose",
            "start",
            "check",
            "lint",
            "dialogue-pass",
            "consistency",
            "finish",
            "bootstrap-longform",
        ],
    },
]

CONSISTENCY_MANUAL_CHECKS = [
    "人物行为符合既有性格设定",
    "伏笔有回扣或继续保持前台未决",
    "时间线与场景转场没有跳错",
    "主 POV 稳定，没有同段乱切脑内",
    "信息暴露符合 POV 边界，没有作者越权透题",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_state_field(text: str, label: str, default: str = "无") -> str:
    match = re.search(rf"(?m)^- {re.escape(label)}(.*)$", text)
    if not match:
        return default
    value = match.group(1).strip()
    return value or default


def extract_section_lines(text: str, header: str) -> list[str]:
    match = re.search(rf"(?ms)^## {re.escape(header)}\n(.*?)(?=^## |\Z)", text)
    if not match:
        return []
    lines: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line in {"-", "- 暂无"}:
            continue
        lines.append(line)
    return lines


def extract_active_plot_rows(text: str) -> list[str]:
    rows = []
    for line in extract_section_lines(text, "活跃伏笔"):
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").replace("-", "").strip()) == set():
            continue
        if "伏笔名称" in line:
            continue
        rows.append(line)
    return rows


def list_recent_chapters(project_dir: Path, limit: int = 3) -> list[Path]:
    manuscript_dir = project_dir / "manuscript"
    if not manuscript_dir.exists():
        return []
    chapters = [path for path in sorted(manuscript_dir.glob("*.md")) if is_chapter_file(path)]
    return chapters[-limit:]


def parse_chapter_number_from_text(raw: str) -> int | None:
    match = re.search(r"第(\d+)章", raw)
    if match:
        return int(match.group(1))
    return None


def parse_chapter_number_from_path(path: Path) -> int | None:
    match = re.match(r"^(\d{3,4})[_-]", path.name)
    if match:
        return int(match.group(1))
    return parse_chapter_number_from_text(path.stem)


def collect_missing_memory_files(project_dir: Path) -> list[str]:
    missing = [relative for relative in REQUIRED_MEMORY_BASE_FILES if not (project_dir / relative).exists()]
    if resolve_project_outline_path(project_dir) is None:
        missing.append(f"{PROJECT_OUTLINE_PATH}（兼容旧 {LEGACY_OUTLINE_PATH}）")
    if resolve_chapter_plan_path(project_dir) is None:
        missing.append(f"{CHAPTER_PLAN_PATH}（兼容旧 {LEGACY_OUTLINE_PATH}）")
    return missing


def collect_missing_longform_files(project_dir: Path) -> list[str]:
    return [relative for relative in LONGFORM_GOVERNANCE_FILES if not (project_dir / relative).exists()]


def parse_count_value(raw_value: str) -> int | None:
    if not raw_value or raw_value in {"未记录", "无", "待定", "未知"}:
        return None
    raw_value = raw_value.replace(",", "").replace("，", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)", raw_value)
    if not match:
        return None
    value = float(match.group(1))
    if "万" in raw_value:
        value *= 10000
    return int(value)


def task_log_update_field(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}.*$"
    replacement = f"- {label}{value}"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    current_state = "## 当前状态\n"
    if current_state in text:
        return text.replace(current_state, current_state + replacement + "\n", 1)
    return text.rstrip() + "\n\n## 当前状态\n" + replacement + "\n"


def append_section_bullet(text: str, header: str, line: str) -> str:
    pattern = rf"(?ms)(^## {re.escape(header)}\n)(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    if match:
        lines = [item for item in match.group(2).splitlines() if item.strip() and item.strip() != "- 暂无"]
        lines.insert(0, line)
        body = "\n".join(lines[:10]).rstrip() + "\n"
        return text[: match.start(2)] + body + text[match.end(2) :]
    return text.rstrip() + f"\n\n## {header}\n{line}\n"


def update_task_log_audit(project_dir: Path, scope: str, status: str, summary_line: str) -> None:
    task_log_path = project_dir / "task_log.md"
    if not task_log_path.exists():
        return
    text = task_log_path.read_text(encoding="utf-8")
    today = date.today().isoformat()
    label = "最近阶段审计：" if scope == "stage" else "最近卷审计："
    chapter_label = "最近阶段审计章节：" if scope == "stage" else "最近卷审计章节："
    header = "阶段审计记录" if scope == "stage" else "卷审计记录"
    chapter_count, _ = compute_manuscript_stats(project_dir)
    text = task_log_update_field(text, label, f"{today} {status}")
    text = task_log_update_field(text, chapter_label, str(chapter_count))
    text = append_section_bullet(text, header, f"- {today} | {status} | {summary_line}")
    task_log_path.write_text(text, encoding="utf-8")


def requires_longform_governance(project_dir: Path, summary: dict) -> bool:
    chapter_count, total_words = compute_manuscript_stats(project_dir)
    target_words = parse_count_value(summary.get("planned_total_words", ""))
    if target_words and target_words >= LONGFORM_TARGET_WORDS:
        return True
    if total_words >= LONGFORM_FALLBACK_TOTAL_WORDS:
        return True
    if chapter_count >= LONGFORM_FALLBACK_CHAPTERS:
        return True
    return False


def resolve_rule_project_dir(
    chapter_path: Path | None = None,
    project_dir: Path | None = None,
    rule_set: str = "novel-lint",
) -> Path:
    candidates: list[Path] = []
    if project_dir is not None:
        candidates.append(project_dir)
    if chapter_path is not None:
        inferred = infer_project_dir_from_chapter(chapter_path)
        if inferred is not None:
            candidates.append(inferred)
    candidates.append(ROOT_DIR)

    for candidate in candidates:
        if (candidate / "rules" / rule_set).exists():
            return candidate
    return ROOT_DIR


def stage_audit_is_stale(summary: dict, chapter_count: int, interval: int = 20) -> bool:
    last_audit_chapter = parse_count_value(summary.get("last_stage_audit_chapter", "")) or 0
    if chapter_count < interval:
        return False
    return chapter_count - last_audit_chapter >= interval


def summarize_project(project_dir: Path) -> dict:
    task_log_path = project_dir / "task_log.md"
    task_log = read_text(task_log_path)
    recent_chapter_files = list_recent_chapters(project_dir)

    recent_summaries = extract_section_lines(task_log, "最近三章摘要")
    if not recent_summaries:
        recent_summaries = [f"- {path.stem}" for path in recent_chapter_files]

    active_plots = extract_active_plot_rows(task_log)
    if not active_plots:
        plot_log = read_text(project_dir / "plot" / "伏笔记录.md")
        active_plots = extract_active_plot_rows(plot_log)

    return {
        "project_dir": str(project_dir),
        "missing_files": collect_missing_memory_files(project_dir),
        "book_title": extract_state_field(task_log, "书名：", project_dir.name),
        "stage": extract_state_field(task_log, "创作阶段：", "未知"),
        "latest_chapter": extract_state_field(task_log, "最新章节：", "无"),
        "current_chapter": extract_state_field(task_log, "当前处理章节：", "无"),
        "planned_total_words": extract_state_field(task_log, "目标总字数：", "未记录"),
        "target_volumes": extract_state_field(task_log, "目标卷数：", "未记录"),
        "current_volume": extract_state_field(task_log, "当前卷：", "未记录"),
        "current_phase": extract_state_field(task_log, "当前阶段：", "未记录"),
        "phase_goal": extract_state_field(task_log, "当前阶段目标：", "未记录"),
        "last_stage_audit": extract_state_field(task_log, "最近阶段审计：", "未记录"),
        "last_stage_audit_chapter": extract_state_field(task_log, "最近阶段审计章节：", "0"),
        "last_volume_audit": extract_state_field(task_log, "最近卷审计：", "未记录"),
        "last_volume_audit_chapter": extract_state_field(task_log, "最近卷审计章节：", "0"),
        "pending_setting_sync": extract_state_field(task_log, "设定变更待同步：", "未记录"),
        "viewpoint": extract_state_field(task_log, "当前视角：", "未记录"),
        "protagonist_location": extract_state_field(task_log, "主角位置：", "未记录"),
        "protagonist_state": extract_state_field(task_log, "主角状态：", "未记录"),
        "next_goal": extract_state_field(task_log, "下一章目标：", "未记录"),
        "recent_summaries": recent_summaries[:3],
        "active_plots": active_plots[:6],
        "active_plot_count": len(active_plots),
        "missing_longform_files": collect_missing_longform_files(project_dir),
        "recent_chapter_files": [str(path) for path in recent_chapter_files],
    }


def determine_target_chapter_num(project_dir: Path, summary: dict, explicit: int | None = None) -> int:
    if explicit is not None:
        return explicit

    current_num = parse_chapter_number_from_text(summary.get("current_chapter", ""))
    if current_num is not None:
        return current_num

    latest_num = parse_chapter_number_from_text(summary.get("latest_chapter", ""))
    if latest_num is not None:
        return latest_num + 1

    recent_files = list_recent_chapters(project_dir, limit=1)
    if recent_files:
        recent_num = parse_chapter_number_from_path(recent_files[-1])
        if recent_num is not None:
            return recent_num + 1

    return 1


def read_guidance(args: argparse.Namespace) -> str:
    guidance = (getattr(args, "guidance", None) or "").strip()
    guidance_file = getattr(args, "guidance_file", None)
    if guidance_file:
        file_text = Path(guidance_file).expanduser().resolve().read_text(encoding="utf-8").strip()
        if guidance and file_text:
            return guidance + "\n" + file_text
        if file_text:
            return file_text
    return guidance


def first_meaningful_value(*values: str | None) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = str(value).strip()
        if normalized and normalized not in {"未记录", "无", "待定", "未知", "未开始"}:
            return normalized
    return None


def runtime_prefix(chapter_num: int) -> str:
    return f"chapter-{chapter_num:04d}"


def runtime_paths(project_dir: Path, chapter_num: int) -> dict[str, Path]:
    prefix = runtime_prefix(chapter_num)
    runtime_dir = project_dir / "runtime"
    return {
        "runtime_dir": runtime_dir,
        "intent": runtime_dir / f"{prefix}.intent.md",
        "context": runtime_dir / f"{prefix}.context.json",
        "scenes": runtime_dir / f"{prefix}.scenes.md",
        "rule_stack": runtime_dir / f"{prefix}.rule-stack.yaml",
        "trace": runtime_dir / f"{prefix}.trace.json",
    }


def excerpt_text(text: str, keyword: str | None = None, max_chars: int = 600) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    if keyword and keyword in cleaned:
        index = cleaned.index(keyword)
        start = max(0, index - max_chars // 3)
        end = min(len(cleaned), index + (max_chars * 2 // 3))
        cleaned = cleaned[start:end]
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars].rstrip() + "..."
    return cleaned


def split_paragraph_units(text: str) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    current: list[str] = []
    start_line = 1

    for line_num, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped:
            if not current:
                start_line = line_num
            current.append(stripped)
            continue
        if current:
            units.append({
                "index": len(units) + 1,
                "label": f"段{len(units) + 1}",
                "line": start_line,
                "text": "\n".join(current),
            })
            current = []

    if current:
        units.append({
            "index": len(units) + 1,
            "label": f"段{len(units) + 1}",
            "line": start_line,
            "text": "\n".join(current),
        })
    return units


def split_sentence_units(text: str) -> list[dict[str, Any]]:
    parts = [item.strip() for item in re.split(r"(?<=[。！？!?])", text) if item.strip()]
    return [
        {
            "index": index,
            "label": f"句{index}",
            "line": None,
            "text": item,
        }
        for index, item in enumerate(parts, start=1)
    ]


def extract_dialogue_units(text: str) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    patterns = (r"“([^”]{1,260})”", r"\"([^\"]{1,260})\"")
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            chunk = match.group(1).strip()
            if not chunk:
                continue
            units.append({
                "index": len(units) + 1,
                "label": f"对白{len(units) + 1}",
                "line": None,
                "text": chunk,
            })
    return units


def scope_units_for_rule(text: str, scope: str) -> list[dict[str, Any]]:
    paragraphs = split_paragraph_units(text)
    if scope == "dialogue":
        return extract_dialogue_units(text)
    if scope == "ending":
        if not paragraphs:
            return []
        return paragraphs[-max(1, min(2, len(paragraphs))):]
    if scope == "opening":
        return paragraphs[: min(3, len(paragraphs))]
    if scope == "sentence":
        return split_sentence_units(text)
    return paragraphs or split_sentence_units(text)


def collect_keyword_hits(units: list[dict[str, Any]], keywords: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    hits: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    total = 0

    for keyword in keywords:
        keyword_count = 0
        keyword_examples = 0
        for unit in units:
            count = unit["text"].count(keyword)
            if count <= 0:
                continue
            total += count
            keyword_count += count
            if keyword_examples < 2 and len(evidence) < 8:
                evidence.append({
                    "kind": "keyword",
                    "label": unit["label"],
                    "line": unit.get("line"),
                    "match": keyword,
                    "count": count,
                    "excerpt": excerpt_text(unit["text"], keyword=keyword, max_chars=120),
                })
                keyword_examples += 1
        if keyword_count > 0:
            hits.append({"keyword": keyword, "count": keyword_count})
    return hits, evidence, total


def collect_regex_hits(units: list[dict[str, Any]], patterns: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    hits: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    total = 0

    for pattern in patterns:
        compiled = re.compile(pattern)
        pattern_count = 0
        pattern_examples = 0
        for unit in units:
            matches = list(compiled.finditer(unit["text"]))
            if not matches:
                continue
            count = len(matches)
            total += count
            pattern_count += count
            if pattern_examples < 2 and len(evidence) < 8:
                match_text = matches[0].group(0)
                evidence.append({
                    "kind": "regex",
                    "label": unit["label"],
                    "line": unit.get("line"),
                    "match": match_text,
                    "pattern": pattern,
                    "count": count,
                    "excerpt": excerpt_text(unit["text"], keyword=match_text, max_chars=120),
                })
                pattern_examples += 1
        if pattern_count > 0:
            hits.append({"pattern": pattern, "count": pattern_count})
    return hits, evidence, total


def load_lint_rules(project_dir: Path, rule_set: str = "novel-lint") -> list[dict[str, Any]]:
    rule_dir = project_dir / "rules" / rule_set
    if not rule_dir.exists():
        return []

    rules: list[dict[str, Any]] = []
    for path in sorted(rule_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            continue
        data["path"] = str(path)
        rules.append(data)
    return rules


def lint_chapter_text(text: str, rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rule in rules:
        scope = str(rule.get("scope", "full"))
        threshold = int(rule.get("threshold", 1))
        units = scope_units_for_rule(text, scope)
        rule_type = str(rule.get("type", "keywords"))

        if rule_type == "regex":
            hits, evidence, total = collect_regex_hits(units, list(rule.get("patterns", [])))
        else:
            hits, evidence, total = collect_keyword_hits(units, list(rule.get("keywords", [])))
        if total < threshold:
            continue
        findings.append({
            "id": rule.get("id"),
            "name": rule.get("name"),
            "severity": rule.get("severity", "warning"),
            "scope": scope,
            "message": rule.get("message", ""),
            "total_hits": total,
            "hits": hits,
            "evidence": evidence,
            "rule_path": rule.get("path"),
        })
    return findings


def load_context_source(path: Path, reason: str, keyword: str | None = None, max_chars: int = 600) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    excerpt = excerpt_text(text, keyword=keyword, max_chars=max_chars)
    if not excerpt:
        return None
    return {
        "source": str(path),
        "reason": reason,
        "excerpt": excerpt,
    }


def infer_project_dir_from_chapter(chapter_path: Path) -> Path | None:
    for candidate in chapter_path.parents:
        if (candidate / "task_log.md").exists():
            return candidate
    return None


def find_chapter_file_by_number(project_dir: Path, chapter_num: int | None) -> Path | None:
    if chapter_num is None:
        return None
    for path in sorted((project_dir / "manuscript").glob("*.md")):
        if not is_chapter_file(path):
            continue
        if parse_chapter_number_from_path(path) == chapter_num:
            return path
    return None


def build_chapter_intent(summary: dict, chapter_num: int, chapter_title: str | None, guidance: str, selected_sources: list[dict], project_dir: Path | None = None) -> str:
    goal = first_meaningful_value(guidance, summary.get("phase_goal"), summary.get("next_goal")) or "推进当前主线"

    must_keep: list[str] = []
    if summary.get("current_volume") not in {"未记录", "未开始", "无", ""}:
        must_keep.append(f"本章仍属于{summary['current_volume']}，不要写成跨卷结算。")
    if summary.get("current_phase") not in {"未记录", "未开始", "无", ""}:
        must_keep.append(f"本章必须服务{summary['current_phase']}。")
    if summary.get("phase_goal") not in {"未记录", "无", ""}:
        must_keep.append(f"阶段目标：{summary['phase_goal']}")
    if summary.get("protagonist_state") not in {"未记录", "无", ""}:
        must_keep.append(f"主角当前状态：{summary['protagonist_state']}")
    if summary.get("viewpoint") not in {"未记录", "无", ""}:
        must_keep.append(f"当前视角优先贴紧：{summary['viewpoint']}")

    must_avoid: list[str] = []
    if summary.get("pending_setting_sync") not in {"未记录", "无", ""}:
        must_avoid.append(f"不要跳过待同步设定变更：{summary['pending_setting_sync']}")
    must_avoid.append("不要让本章把主线、支线和阶段问题同时清零。")
    must_avoid.append("不要无计划新增大量新设定或新伏笔。")

    conflicts: list[str] = []
    if summary.get("next_goal") not in {"未记录", "无", ""}:
        conflicts.append(f"推进目标：{summary['next_goal']}")
    for hook_row in summary.get("active_plots", [])[:3]:
        conflicts.append(f"伏笔压力：{hook_row}")

    hook_lines = summary.get("active_plots", [])[:3]
    if not hook_lines:
        hook_lines = ["- 暂无高优先级伏笔推进"]
    else:
        hook_lines = [f"- {row}" if not str(row).startswith("-") else str(row) for row in hook_lines]

    source_lines = [f"- {Path(item['source']).name}: {item['reason']}" for item in selected_sources]
    if not source_lines:
        source_lines = ["- 暂无"]

    must_keep_lines = [f"- {item}" for item in must_keep] or ["- 暂无"]
    must_avoid_lines = [f"- {item}" for item in must_avoid] or ["- 暂无"]
    conflict_lines = [f"- {item}" for item in conflicts] or ["- 暂无"]

    lines = [
        "# Chapter Intent",
        "",
        f"## Chapter",
        f"第{chapter_num}章" + (f"：{chapter_title}" if chapter_title else ""),
        "",
        "## Goal",
        goal,
        "",
        "## Scope",
        f"- 当前卷：{summary.get('current_volume', '未记录')}",
        f"- 当前阶段：{summary.get('current_phase', '未记录')}",
        f"- 当前阶段目标：{summary.get('phase_goal', '未记录')}",
        "",
        "## Must Keep",
        *must_keep_lines,
        "",
        "## Must Avoid",
        *must_avoid_lines,
        "",
        "## Conflicts",
        *conflict_lines,
        "",
        "## Hook Agenda",
        "### Must Advance",
        *hook_lines,
        "",
        "## Inputs",
        *source_lines,
        "",
    ]

    kb_queries: list[str] = []
    if chapter_title:
        kb_queries.append(chapter_title)
    if goal and goal not in {"推进当前主线"}:
        kb_queries.append(goal)
    for plot_row in summary.get("active_plots", [])[:2]:
        cell = str(plot_row).lstrip("- |").split("|")[0].strip()
        if cell and cell not in kb_queries:
            kb_queries.append(cell)
    if not kb_queries:
        kb_queries.append("网文章节续写")

    lines += [
        "## Knowledge Base Query（正文前必须执行）",
        "",
        "在开始写正文之前，必须调用以 `coze-mcp-` 开头的知识库 MCP 工具查询相关参考材料。",
        "",
        "建议查询关键词（从本章目标和活跃伏笔中提取，可按需调整）：",
        *[f"- {q}" for q in kb_queries],
        "",
        "执行要求：",
        "- 至少完成一次查询，将命中的方法论或案例整合进写作策略",
        "- 查询结果与本章 Goal / Must Keep / Writing Quick Reference 矛盾时，以后者为准",
        "- 若 coze-mcp- 工具不可用，跳过本节，不影响后续流程",
        "",
    ]

    quickref_path = (project_dir / "references" / "writing-quickref.md") if project_dir else None
    if quickref_path is None:
        quickref_path = ROOT_DIR / "references" / "writing-quickref.md"
    if quickref_path.exists():
        lines += ["## Writing Quick Reference", ""]
        lines += quickref_path.read_text(encoding="utf-8").strip().splitlines()
        lines.append("")

    return "\n".join(lines)


def build_runtime_sources(project_dir: Path, summary: dict, chapter_num: int, guidance: str) -> list[dict]:
    sources: list[dict] = []

    def add(path_value: str | Path | None, reason: str, keyword: str | None = None, max_chars: int = 600) -> None:
        if path_value is None:
            return
        path = project_dir / path_value if isinstance(path_value, str) else path_value
        source = load_context_source(path, reason, keyword=keyword, max_chars=max_chars)
        if source:
            sources.append(source)

    current_volume = summary.get("current_volume")
    current_phase = summary.get("current_phase")
    project_outline_path = resolve_project_outline_path(project_dir)
    chapter_plan_path = resolve_chapter_plan_path(project_dir)
    add("docs/全书宪法.md", "最高优先级硬约束", keyword="## 全书终局")
    add(project_outline_path, "全书主线与终局锚点", keyword="## 主线三步法骨架")
    add("docs/卷纲.md", "当前卷推进约束", keyword=current_volume if current_volume not in {"未记录", "未开始", "无", ""} else None)
    add("docs/阶段规划.md", "当前阶段推进约束", keyword=current_phase if current_phase not in {"未记录", "未开始", "无", ""} else None)
    add("docs/作者意图.md", "长期作者意图")
    add("docs/当前焦点.md", "最近 1-3 章焦点")
    add(chapter_plan_path, "章节规划与近期摘要", keyword="## 章节规划")
    add("task_log.md", "当前运行状态与最近摘要", keyword="## 当前状态")
    add("plot/伏笔记录.md", "活跃伏笔与回收债务", keyword="## 活跃伏笔")
    add("plot/时间线.md", "时间线与出场顺序")
    character_dir = project_dir / "characters"
    if character_dir.exists():
        for character_path in sorted(character_dir.glob("*.md")):
            add(character_path, f"角色档案：{character_path.stem}")

    recent_files = list_recent_chapters(project_dir, limit=1)
    if recent_files:
        previous = recent_files[-1]
        prev = load_context_source(previous, "上一章正文结尾与承接", max_chars=800)
        if prev:
            sources.append(prev)

    if guidance:
        sources.append({
            "source": "cli:guidance",
            "reason": "本次人工补充指令",
            "excerpt": excerpt_text(guidance, max_chars=400),
        })

    return sources


def render_rule_stack_yaml(summary: dict, chapter_num: int, chapter_title: str | None) -> str:
    hard_rules = [
        "遵守 docs/全书宪法.md 的终局、法则和关系边界",
        "不得与 docs/世界观.md / docs/法则.md / characters/*.md 冲突",
        "本章必须服务当前卷、当前阶段和当前阶段目标",
        "正文必须写入纯正文，不输出章节壳",
    ]
    soft_rules = [
        f"目标章节：第{chapter_num}章" + (f"《{chapter_title}》" if chapter_title else ""),
        f"当前卷：{summary.get('current_volume', '未记录')}",
        f"当前阶段：{summary.get('current_phase', '未记录')}",
        f"当前阶段目标：{summary.get('phase_goal', '未记录')}",
        f"下一章目标：{summary.get('next_goal', '未记录')}",
    ]
    diagnostic_rules = [
        "检查是否缺少前台问题、阶段回报和结尾钩子",
        "检查是否出现视角越权、设定污染和伏笔债务堆积",
        "检查是否新增了与当前阶段无关的支线负担",
    ]

    lines = [
        "chapter:",
        f"  number: {chapter_num}",
        f"  title: \"{chapter_title or ''}\"",
        "layers:",
        "  - id: constitution",
        "    scope: L4",
        "    precedence: 400",
        "  - id: structure-governance",
        "    scope: L3",
        "    precedence: 300",
        "  - id: project-runtime",
        "    scope: L2",
        "    precedence: 200",
        "  - id: chapter-execution",
        "    scope: L1",
        "    precedence: 100",
        "sections:",
        "  hard:",
        *(f"    - {item}" for item in hard_rules),
        "  soft:",
        *(f"    - {item}" for item in soft_rules),
        "  diagnostic:",
        *(f"    - {item}" for item in diagnostic_rules),
        "",
    ]
    return "\n".join(lines)


def build_scene_cards(summary: dict, chapter_num: int, chapter_title: str | None, guidance: str) -> str:
    pov = first_meaningful_value(summary.get("viewpoint")) or "主 POV"
    location = first_meaningful_value(summary.get("protagonist_location")) or "当前主要场域"
    goal = first_meaningful_value(guidance, summary.get("phase_goal"), summary.get("next_goal")) or "推进当前主线"
    state = first_meaningful_value(summary.get("protagonist_state")) or "带着未结问题入场"
    hook_pressure = summary.get("active_plots", [])[:2]
    hook_note = "；".join(str(item) for item in hook_pressure) if hook_pressure else "暂无高优先级伏笔压力"

    scenes = [
        {
            "title": "场景一：承接与入场",
            "tag": "必选",
            "function": "承接上章钩子，迅速把主角推回当前前台问题",
            "want": goal,
            "block": "立刻出现的规则压力、资源压力或关系阻力",
            "relation": "至少让一组人物关系出现轻微错位、试探或拉扯",
            "info": "补足本章必须知道但此前未说透的信息",
            "handoff": "把局势推进到必须正面对抗或做选择",
        },
        {
            "title": "场景二：试探 / 铺垫升级",
            "tag": "可选",
            "function": "适合过渡章、悬疑章、关系章，先把风险和欲望拧紧，再进入主冲突",
            "want": "试探、埋钩、交换信息或逼近目标",
            "block": "局势尚未全面撕开，但阻力已经露头",
            "relation": "让试探、误会、拉扯或站位变化先发生",
            "info": "补一个后续会爆的细节，而不是一次说透",
            "handoff": "把局面推到必须亮牌或必须忍让",
        },
        {
            "title": "场景三：主冲突 / 失衡",
            "tag": "必选",
            "function": "让人物围绕目标发生真正对抗、误判或代价，不只是信息复述",
            "want": "拿到、守住、证明、隐瞒或逃离某件事",
            "block": "来自人物、规则或现实条件的直接阻拦",
            "relation": "关系发生可感知变化，不能只是态度重复",
            "info": f"给出本章最重要的信息增量，并注意伏笔压力：{hook_note}",
            "handoff": "形成新的失衡、误判、代价或认知拐点",
        },
        {
            "title": "场景四：余波 / 反扑 / 补刀",
            "tag": "可选",
            "function": "适合高潮章、翻盘章、多线章，在主冲突后追加反扑、余波或第二层代价",
            "want": "扩大收益，或者把局部胜利转成更大风险",
            "block": "旧问题未清，新问题已逼近",
            "relation": "把本章关系变化坐实，不让它停在口头态度",
            "info": "补足最关键的后果、代价或下一层谜面",
            "handoff": "把读者送进更高一层的问题，而不是平着收掉",
        },
        {
            "title": "场景五：结算与钩子",
            "tag": "必选",
            "function": "给阶段性回报，同时把读者送进下一章问题",
            "want": "让本章至少兑现一项回报：爽点、情绪点、关系点或信息收益",
            "block": "不能把主线、支线和阶段问题同时清零",
            "relation": "让本章关系变化固定下来，留下下一步张力",
            "info": "明确本章结尾的新问题、新危险或新选择",
            "handoff": "结尾停在动作、发现、选择或危险上",
        },
    ]

    lines = [
        "# Scene Cards",
        "",
        "## Chapter",
        f"第{chapter_num}章" + (f"：{chapter_title}" if chapter_title else ""),
        "",
        "## Usage",
        "- 默认按 3-5 场编排，不是固定三场景模板。",
        "- 场景一 / 三 / 五是骨架；场景二 / 四按章节类型增删。",
        "- 过渡章可只保留 3 场，悬疑章 / 群像章 / 高潮章可扩到 4-5 场。",
        "",
        "## Runtime Summary",
        f"- 当前卷：{summary.get('current_volume', '未记录')}",
        f"- 当前阶段：{summary.get('current_phase', '未记录')}",
        f"- 当前阶段目标：{summary.get('phase_goal', '未记录')}",
        f"- 主 POV：{pov}",
        f"- 主角位置：{location}",
        f"- 主角状态：{state}",
        f"- 本章总目标：{goal}",
        "",
    ]

    for scene in scenes:
        lines.extend([
            scene["title"],
            f"- 类型：{scene['tag']}",
            f"- 地点：{location}",
            f"- POV：{pov}",
            f"- 场景功能：{scene['function']}",
            f"- 谁想要什么：{scene['want']}",
            f"- 谁阻止谁：{scene['block']}",
            f"- 关系怎么变：{scene['relation']}",
            f"- 信息增量：{scene['info']}",
            f"- 推向下一场：{scene['handoff']}",
            "",
        ])

    return "\n".join(lines)


def materialize_plan(project_dir: Path, summary: dict, chapter_num: int, chapter_title: str | None, guidance: str) -> dict:
    paths = runtime_paths(project_dir, chapter_num)
    paths["runtime_dir"].mkdir(parents=True, exist_ok=True)
    selected_sources = build_runtime_sources(project_dir, summary, chapter_num, guidance)
    intent_content = build_chapter_intent(summary, chapter_num, chapter_title, guidance, selected_sources, project_dir=project_dir)
    paths["intent"].write_text(intent_content, encoding="utf-8")
    return {
        "chapter": chapter_num,
        "intent_path": str(paths["intent"]),
        "goal": first_meaningful_value(guidance, summary.get("phase_goal"), summary.get("next_goal")) or "推进当前主线",
        "selected_sources": selected_sources,
    }


def materialize_runtime_package(project_dir: Path, summary: dict, chapter_num: int, chapter_title: str | None, guidance: str) -> dict:
    plan_result = materialize_plan(project_dir, summary, chapter_num, chapter_title, guidance)
    paths = runtime_paths(project_dir, chapter_num)
    selected_sources = plan_result["selected_sources"]
    context_payload = {
        "chapter": chapter_num,
        "title": chapter_title or "",
        "goal": plan_result["goal"],
        "current_volume": summary.get("current_volume", "未记录"),
        "current_phase": summary.get("current_phase", "未记录"),
        "phase_goal": summary.get("phase_goal", "未记录"),
        "selectedContext": selected_sources,
    }
    trace_payload = {
        "chapter": chapter_num,
        "plannerInputs": [item["source"] for item in selected_sources],
        "composerInputs": [
            "docs/全书宪法.md",
            PROJECT_OUTLINE_PATH,
            "docs/卷纲.md",
            "docs/阶段规划.md",
            "docs/作者意图.md",
            "docs/当前焦点.md",
            CHAPTER_PLAN_PATH,
            "task_log.md",
            "plot/伏笔记录.md",
            "plot/时间线.md",
            "characters/*.md",
        ],
        "selectedSources": [item["source"] for item in selected_sources],
        "notes": [
            "本章运行时产物由本地项目记忆编译生成，不依赖在线 LLM。",
            "如果本章目标或上下文变化，应重新执行 plan / compose。",
        ],
    }

    paths["context"].write_text(json.dumps(context_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["scenes"].write_text(build_scene_cards(summary, chapter_num, chapter_title, guidance), encoding="utf-8")
    paths["trace"].write_text(json.dumps(trace_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["rule_stack"].write_text(render_rule_stack_yaml(summary, chapter_num, chapter_title), encoding="utf-8")

    return {
        "chapter": chapter_num,
        "intent_path": str(paths["intent"]),
        "context_path": str(paths["context"]),
        "scenes_path": str(paths["scenes"]),
        "rule_stack_path": str(paths["rule_stack"]),
        "trace_path": str(paths["trace"]),
        "goal": plan_result["goal"],
        "selected_sources": selected_sources,
    }


def print_resume_summary(summary: dict) -> None:
    print("\n" + "=" * 60)
    print("项目恢复摘要")
    print("=" * 60)
    print(f"项目目录: {summary['project_dir']}")
    print(f"书名: {summary['book_title']}")
    print(f"创作阶段: {summary['stage']}")
    print(f"目标总字数: {summary['planned_total_words']}")
    print(f"目标卷数: {summary['target_volumes']}")
    print(f"最新章节: {summary['latest_chapter']}")
    print(f"当前处理章节: {summary['current_chapter']}")
    print(f"当前卷: {summary['current_volume']}")
    print(f"当前阶段: {summary['current_phase']}")
    print(f"当前阶段目标: {summary['phase_goal']}")
    print(f"当前视角: {summary['viewpoint']}")
    print(f"主角位置: {summary['protagonist_location']}")
    print(f"主角状态: {summary['protagonist_state']}")
    print(f"下一章目标: {summary['next_goal']}")
    print(f"最近阶段审计: {summary['last_stage_audit']}")
    print(f"最近阶段审计章节: {summary['last_stage_audit_chapter']}")
    print(f"最近卷审计: {summary['last_volume_audit']}")
    print(f"最近卷审计章节: {summary['last_volume_audit_chapter']}")

    if summary["missing_files"]:
        print("\n缺失记忆文件:")
        for item in summary["missing_files"]:
            print(f"- {item}")

    if summary["missing_longform_files"]:
        print("\n缺失超长篇治理文件:")
        for item in summary["missing_longform_files"]:
            print(f"- {item}")

    print("\n最近两到三章摘要:")
    if summary["recent_summaries"]:
        for line in summary["recent_summaries"]:
            print(line if line.startswith("-") else f"- {line}")
    else:
        print("- 暂无")

    print("\n活跃伏笔:")
    if summary["active_plots"]:
        for row in summary["active_plots"]:
            print(f"- {row}")
    else:
        print("- 暂无")

    if summary["recent_chapter_files"]:
        print("\n最近章节文件:")
        for path in summary["recent_chapter_files"]:
            print(f"- {path}")


def print_gate_failures(title: str, failures: list[str]) -> None:
    print("\n" + "!" * 60)
    print(title)
    print("!" * 60)
    for item in failures:
        print(f"- {item}")


def print_named_list(title: str, items: list[str], empty_value: str = "无") -> None:
    print(f"\n{title}:")
    if items:
        for item in items:
            print(f"- {item}")
    else:
        print(f"- {empty_value}")


def evaluate_preflight(project_dir: Path) -> tuple[dict, list[str]]:
    summary = summarize_project(project_dir)
    chapter_count, _ = compute_manuscript_stats(project_dir)

    failures: list[str] = []
    if summary["missing_files"]:
        failures.append("缺失项目记忆文件，禁止直接续写或开写正文")
    if summary["stage"] == "未知":
        failures.append("task_log.md 未记录创作阶段")
    if summary["next_goal"] in {"未记录", "无", ""}:
        failures.append("task_log.md 未记录下一章目标")
    if requires_longform_governance(project_dir, summary) and summary["missing_longform_files"]:
        failures.append("已进入长篇治理范围，但缺失全书宪法/卷纲/阶段规划/变更日志；先执行 bootstrap-longform")
    if requires_longform_governance(project_dir, summary) and summary["current_volume"] in {"未记录", "未开始", "无", ""}:
        failures.append("长篇项目未记录当前卷，禁止继续推进")
    if requires_longform_governance(project_dir, summary) and summary["current_phase"] in {"未记录", "未开始", "无", ""}:
        failures.append("长篇项目未记录当前阶段，禁止继续推进")
    if requires_longform_governance(project_dir, summary) and stage_audit_is_stale(summary, chapter_count):
        failures.append("阶段审计已过期，先执行 audit --scope stage 再继续正文")
    return summary, failures


def handle_preflight(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary, failures = evaluate_preflight(project_dir)
    print_resume_summary(summary)

    if failures:
        print_gate_failures("前置校验失败: preflight 未通过", failures)
        return 2

    print("\n前置校验通过，可继续执行 resume / start / 正文创作。")
    return 0


def build_check_report(chapter_path: Path, rule_project_dir: Path | None = None) -> dict:
    rules = load_lint_rules(resolve_rule_project_dir(chapter_path=chapter_path, project_dir=rule_project_dir))
    chapter_text = chapter_path.read_text(encoding="utf-8") if chapter_path.exists() else ""
    return {
        "wordcount": check_chapter(str(chapter_path)),
        "emotion": analyze_chapter_emotion_curve(str(chapter_path)),
        "thrills": analyze_thrills_and_poisons(str(chapter_path)),
        "lint": lint_chapter_text(chapter_text, rules) if chapter_text else [],
    }


def print_check_summary(report: dict) -> None:
    wordcount = report["wordcount"]
    emotion = report["emotion"]
    thrills = report["thrills"]
    lint_findings = report.get("lint", [])

    print("\n" + "=" * 60)
    print(f"章节检查摘要: {Path(wordcount['file']).name}")
    print("=" * 60)

    if not wordcount.get("exists"):
        print(f"- 文件错误: {wordcount.get('message', '未知错误')}")
        return

    print(f"- 字数: {wordcount['word_count']} ({wordcount['status']})")
    print(f"- 情绪走向: {emotion.get('transition', 'unknown')}")
    print(
        f"- 爽点/毒点: thrill={thrills.get('thrill_score', 0)}, "
        f"poison={thrills.get('poison_score', 0)}, overall={thrills.get('overall', 'unknown')}"
    )
    print("- 说明: 爽毒点评估是静态启发式信号，不替代上下文语义判断。")
    print(f"- 规则检查: {len(lint_findings)} 条命中")

    issues: list[str] = []
    if wordcount["status"] != "pass":
        issues.append("字数未达默认下限")
    if thrills.get("overall") == "negative":
        issues.append("静态爽毒点评估偏负面，仅作启发式信号；返修前先结合上下文人工确认")
    if emotion.get("opening_emotion") == "neutral" and emotion.get("ending_emotion") == "neutral":
        issues.append("情绪曲线过平，检查是否缺少冲突或钩子")

    if issues:
        print("- 警告:")
        for item in issues:
            print(f"  - {item}")
    if lint_findings:
        print("- 规则命中:")
        for item in lint_findings[:5]:
            print(f"  - {item['name']} ({item['severity']}): {item['message']}")


def handle_lint(args: argparse.Namespace) -> int:
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    if not chapter_path.exists():
        print(json.dumps({"error": f"文件不存在: {chapter_path}"}, ensure_ascii=False, indent=2))
        return 2

    rules = load_lint_rules(resolve_rule_project_dir(chapter_path=chapter_path, rule_set=args.rule_set), rule_set=args.rule_set)
    content = chapter_path.read_text(encoding="utf-8")
    findings = lint_chapter_text(content, rules)

    if args.json:
        print(json.dumps({"file": str(chapter_path), "findings": findings}, ensure_ascii=False, indent=2))
        return 0

    print("\n" + "=" * 60)
    print(f"规则检查: {chapter_path.name}")
    print("=" * 60)
    if not findings:
        print("- 未命中规则")
        return 0

    for item in findings:
        print(f"- {item['name']} [{item['severity']}]")
        print(f"  {item['message']}")
        for hit in item["hits"][:5]:
            label = hit.get("keyword") or hit.get("pattern") or "match"
            print(f"  - {label} x{hit['count']}")
        for evidence in item.get("evidence", [])[:3]:
            line = f" line={evidence['line']}" if evidence.get("line") else ""
            print(f"  - {evidence['label']}{line}: {evidence['excerpt']}")
    return 0


def extract_dialogue_stats(text: str) -> dict[str, Any]:
    dialogue_chunks: list[str] = []
    for pattern in (r"“([^”]{1,400})”", r"\"([^\"]{1,400})\""):
        dialogue_chunks.extend(re.findall(pattern, text))
    total_lines = len(dialogue_chunks)
    total_chars = sum(len(chunk) for chunk in dialogue_chunks)
    avg_chars = round(total_chars / total_lines, 1) if total_lines else 0
    long_lines = [chunk for chunk in dialogue_chunks if len(chunk) >= 30]
    return {
        "dialogue_lines": total_lines,
        "dialogue_chars": total_chars,
        "avg_chars_per_line": avg_chars,
        "long_lines": long_lines[:5],
    }


def build_consistency_report(
    chapter_path: Path,
    project_dir: Path | None = None,
    lint_findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    resolved_project_dir = project_dir or infer_project_dir_from_chapter(chapter_path)
    chapter_num = parse_chapter_number_from_path(chapter_path)
    issues: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] | None = None
    previous_path: Path | None = None
    next_path: Path | None = None

    if resolved_project_dir and (resolved_project_dir / "task_log.md").exists():
        summary = summarize_project(resolved_project_dir)
        previous_path = find_chapter_file_by_number(resolved_project_dir, chapter_num - 1 if chapter_num else None)
        next_path = find_chapter_file_by_number(resolved_project_dir, chapter_num + 1 if chapter_num else None)

        if summary["missing_files"]:
            issues.append("项目记忆文件缺失，无法完成完整连贯性校验")
        if requires_longform_governance(resolved_project_dir, summary) and summary["missing_longform_files"]:
            issues.append("超长篇治理文件缺失，卷/阶段一致性无法保证")
        if chapter_num and chapter_num > 1 and previous_path is None:
            warnings.append(f"未找到第{chapter_num - 1}章正文，无法检查上一章承接")
        if summary["active_plot_count"] == 0:
            warnings.append("当前没有活跃伏笔记录，检查是否漏记伏笔债务")
        if summary["next_goal"] in {"未记录", "无", ""}:
            warnings.append("task_log.md 未记录下一章目标，章节承接目标不够明确")
        if summary["pending_setting_sync"] not in {"未记录", "无", ""}:
            warnings.append(f"存在待同步设定变更：{summary['pending_setting_sync']}，先核对是否已经污染正文")
        current_chapter_num = parse_chapter_number_from_text(summary["current_chapter"])
        if chapter_num is not None and current_chapter_num not in {None, chapter_num} and summary["current_chapter"] != "无":
            warnings.append(f"task_log.md 当前处理章节为 {summary['current_chapter']}，与待审章节不一致")
    else:
        warnings.append("无法定位项目根目录，consistency 仅基于当前章节和规则命中做检查")

    pov_findings = [item for item in (lint_findings or []) if item.get("id") == "pov_leak"]
    if pov_findings:
        issues.append(f"命中 {len(pov_findings)} 条 POV 越权提示")

    return {
        "file": str(chapter_path),
        "chapter_num": chapter_num,
        "project_dir": str(resolved_project_dir) if resolved_project_dir else None,
        "previous_chapter": str(previous_path) if previous_path else None,
        "next_chapter": str(next_path) if next_path else None,
        "expected": {
            "viewpoint": summary.get("viewpoint", "未记录") if summary else "未知",
            "protagonist_location": summary.get("protagonist_location", "未记录") if summary else "未知",
            "protagonist_state": summary.get("protagonist_state", "未记录") if summary else "未知",
            "current_volume": summary.get("current_volume", "未记录") if summary else "未知",
            "current_phase": summary.get("current_phase", "未记录") if summary else "未知",
            "phase_goal": summary.get("phase_goal", "未记录") if summary else "未知",
            "next_goal": summary.get("next_goal", "未记录") if summary else "未知",
            "active_plots": (summary or {}).get("active_plots", [])[:3],
        },
        "issues": issues,
        "warnings": warnings,
        "manual_checks": CONSISTENCY_MANUAL_CHECKS,
    }


def print_consistency_summary(report: dict[str, Any]) -> None:
    print("\n" + "=" * 60)
    print(f"连贯性检查: {Path(report['file']).name}")
    print("=" * 60)
    print(f"- 项目目录: {report.get('project_dir') or '未定位'}")
    print(f"- 章节号: {report.get('chapter_num') or '未知'}")
    print(f"- 上一章: {report.get('previous_chapter') or '未定位'}")
    print(f"- 下一章: {report.get('next_chapter') or '未定位'}")
    print(f"- 预期 POV: {report['expected']['viewpoint']}")
    print(f"- 预期主角位置: {report['expected']['protagonist_location']}")
    print(f"- 预期主角状态: {report['expected']['protagonist_state']}")
    print(f"- 当前阶段目标: {report['expected']['phase_goal']}")
    print(f"- 下一章目标: {report['expected']['next_goal']}")

    print_named_list("阻塞问题", report.get("issues", []))
    print_named_list("风险提示", report.get("warnings", []))
    print_named_list("活跃伏笔压力", report["expected"].get("active_plots", []), empty_value="暂无")
    print_named_list("人工复核清单", report.get("manual_checks", []))


OPENING_HOOK_PATTERNS = [
    r"危险|威胁|追|逃|杀|逼|撞|闯|拦|发现|看见|听见|忽然|突然|围住|压低声音|响起",
    r"“|\"",
]

ENDING_HOOK_PATTERNS = [
    r"[？?]",
    r"危险|威胁|发现|选择|下一瞬|忽然|突然|同时|响起|逼近|冲|扑|拔|按住|铃声",
]


def join_units_text(units: list[dict[str, Any]]) -> str:
    return "\n\n".join(unit["text"] for unit in units if unit.get("text")).strip()


def collect_signal_matches(text: str, patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            value = match.group(0)
            if value not in matches:
                matches.append(value)
            if len(matches) >= 6:
                return matches
    return matches


def build_review_dossier(
    chapter_path: Path,
    chapter_text: str,
    project_dir: Path | None,
    consistency_report: dict[str, Any],
    lint_findings: list[dict[str, Any]],
    dialogue_findings: list[dict[str, Any]],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    paragraphs = split_paragraph_units(chapter_text)
    opening_excerpt = join_units_text(paragraphs[: min(3, len(paragraphs))])
    ending_excerpt = join_units_text(paragraphs[-min(2, len(paragraphs)):])
    previous_excerpt = ""

    if consistency_report.get("previous_chapter"):
        previous_excerpt = excerpt_text(read_text(Path(consistency_report["previous_chapter"])), max_chars=260)

    opening_matches = collect_signal_matches(opening_excerpt, OPENING_HOOK_PATTERNS)
    ending_matches = collect_signal_matches(ending_excerpt, ENDING_HOOK_PATTERNS)
    ending_summary_hit = any(item.get("id") == "ending_summary" for item in lint_findings)
    pov_hit = any(item.get("id") == "pov_leak" for item in lint_findings)

    auto_checks = [
        {
            "id": "opening_hook",
            "title": "开头钩子信号",
            "status": "pass" if len(opening_matches) >= 2 else "warn",
            "reason": "开头三段内检测到可见冲突/动作/对白信号。" if len(opening_matches) >= 2 else "开头三段缺少足够强的即时钩子信号。",
            "evidence": [excerpt_text(opening_excerpt, max_chars=220)],
            "signals": opening_matches,
        },
        {
            "id": "ending_hook",
            "title": "结尾钩子信号",
            "status": "warn" if ending_summary_hit or len(ending_matches) < 1 else "pass",
            "reason": "结尾命中升华/总结倾向。" if ending_summary_hit else (
                "结尾保留了未决动作、发现或危险信号。" if len(ending_matches) >= 1 else "结尾缺少足够明确的未决动作或危险信号。"
            ),
            "evidence": [excerpt_text(ending_excerpt, max_chars=220)],
            "signals": ending_matches,
        },
        {
            "id": "dialogue_load",
            "title": "对白负载",
            "status": "warn" if dialogue_findings or metrics["dialogue"]["avg_chars_per_line"] >= 28 else "pass",
            "reason": "对白里有明显说明感或平均句长偏高。" if dialogue_findings or metrics["dialogue"]["avg_chars_per_line"] >= 28 else "对白长度和说明感未见明显异常。",
            "evidence": [f"对白行数={metrics['dialogue']['dialogue_lines']}, 平均句长={metrics['dialogue']['avg_chars_per_line']}"],
            "signals": [item["name"] for item in dialogue_findings[:4]],
        },
        {
            "id": "pov_boundary",
            "title": "POV 边界",
            "status": "warn" if pov_hit else "manual",
            "reason": "规则命中可能的视角越权表达。" if pov_hit else "未命中静态 POV 规则，但是否越权仍需人工/模型逐段判断。",
            "evidence": [f"预期 POV={consistency_report['expected']['viewpoint']}"],
            "signals": [item["name"] for item in lint_findings if item.get("id") == "pov_leak"],
        },
        {
            "id": "reward_compensation",
            "title": "回报/补偿信号",
            "status": "warn" if metrics["thrills"].get("overall") == "negative" else "manual",
            "reason": "静态爽毒点评估偏负面，主角受挫后回报可能不足。" if metrics["thrills"].get("overall") == "negative" else "静态爽毒点评估未见明显失衡，但是否有真实回报仍需语义审稿。",
            "evidence": [f"thrill={metrics['thrills'].get('thrill_score', 0)}, poison={metrics['thrills'].get('poison_score', 0)}, overall={metrics['thrills'].get('overall', 'unknown')}"],
            "signals": [],
        },
        {
            "id": "continuity_context",
            "title": "上下文承接",
            "status": "warn" if consistency_report["warnings"] else "manual",
            "reason": "项目记忆或伏笔记录存在缺口。" if consistency_report["warnings"] else "静态承接检查未见明显阻塞，但主线推进仍需对照项目总纲与章节规划人工确认。",
            "evidence": [f"上一章={consistency_report.get('previous_chapter') or '未定位'}", f"下一章目标={consistency_report['expected']['next_goal']}"],
            "signals": consistency_report["warnings"][:3],
        },
    ]

    semantic_questions = [
        {
            "id": "mainline_push",
            "question": "本章是否真的推进了当前主线或重要支线，而不是只完成气氛和入场？",
            "why": "这是网文章节能否站住的第一判断。",
            "evidence": [
                f"当前阶段目标：{consistency_report['expected']['phase_goal']}",
                f"下一章目标：{consistency_report['expected']['next_goal']}",
                excerpt_text(opening_excerpt, max_chars=160),
                excerpt_text(ending_excerpt, max_chars=160),
            ],
        },
        {
            "id": "relationship_change",
            "question": "本章是否让关键人物关系、站位或认知发生了可感知变化？",
            "why": "没有关系变化，很多章节会只剩事件播报。",
            "evidence": [
                f"预期 POV：{consistency_report['expected']['viewpoint']}",
                excerpt_text(opening_excerpt, max_chars=160),
                excerpt_text(ending_excerpt, max_chars=160),
            ],
        },
        {
            "id": "foreshadow_and_hook",
            "question": "本章是否回应了旧悬念，并留下了新的前台问题或升级旧钩子？",
            "why": "追读牵引取决于旧债有没有回扣、新债有没有立住。",
            "evidence": consistency_report["expected"].get("active_plots", [])[:3] + [excerpt_text(ending_excerpt, max_chars=160)],
        },
        {
            "id": "reward_vs_pain",
            "question": "主角受压后，是否拿到了信息收益、反制基础、关系回应或阶段性回报？",
            "why": "只有压力没有补偿，读者会把它感知成纯受气。",
            "evidence": [
                f"静态爽毒点：{metrics['thrills'].get('overall', 'unknown')}",
                excerpt_text(ending_excerpt, max_chars=160),
            ],
        },
        {
            "id": "pov_and_information",
            "question": "正文是否始终贴紧主 POV，没有偷偷宣布别人的内心、判断或群体认知？",
            "why": "这是连载稳定性和沉浸感的硬边界。",
            "evidence": [f"预期 POV：{consistency_report['expected']['viewpoint']}"] + [
                excerpt_text(item["excerpt"], max_chars=120) for item in sum((finding.get("evidence", [])[:1] for finding in lint_findings if finding.get("id") == "pov_leak"), [])
            ],
        },
        {
            "id": "ending_strength",
            "question": "章节结尾是把读者推进下一章，还是只是把情绪总结了一遍？",
            "why": "平台向章节结尾必须服务追更，而不是替作者收束主题。",
            "evidence": [excerpt_text(ending_excerpt, max_chars=200)],
        },
    ]

    return {
        "static_review_complete": True,
        "semantic_review_complete": False,
        "semantic_review_requires": "human_or_model",
        "evidence_pack": {
            "opening_excerpt": excerpt_text(opening_excerpt, max_chars=260),
            "ending_excerpt": excerpt_text(ending_excerpt, max_chars=260),
            "previous_excerpt": previous_excerpt or "未定位上一章正文摘录",
            "active_plot_pressure": consistency_report["expected"].get("active_plots", []),
        },
        "auto_checks": auto_checks,
        "semantic_questions": semantic_questions,
    }


def build_review_report(chapter_path: Path, project_dir: Path | None = None) -> dict[str, Any]:
    effective_rule_project_dir = resolve_rule_project_dir(chapter_path=chapter_path, project_dir=project_dir)
    check_report = build_check_report(chapter_path, rule_project_dir=effective_rule_project_dir)
    content = chapter_path.read_text(encoding="utf-8") if chapter_path.exists() else ""
    dialogue_stats = extract_dialogue_stats(content) if content else extract_dialogue_stats("")
    dialogue_rules = [
        rule
        for rule in load_lint_rules(effective_rule_project_dir, rule_set="novel-lint")
        if str(rule.get("scope", "")) == "dialogue"
    ]
    dialogue_findings = lint_chapter_text(content, dialogue_rules) if content else []
    consistency_report = build_consistency_report(
        chapter_path,
        project_dir=project_dir,
        lint_findings=check_report.get("lint", []),
    )

    blocking_issues = list(consistency_report["issues"])
    warnings = list(consistency_report["warnings"])
    actions: list[str] = []

    wordcount = check_report["wordcount"]
    emotion = check_report["emotion"]
    thrills = check_report["thrills"]
    lint_findings = check_report.get("lint", [])

    if not wordcount.get("exists"):
        blocking_issues.append(wordcount.get("message", "章节文件不存在"))
    if wordcount.get("status") != "pass":
        warnings.append("字数未达默认范围，优先补足场景后果、人物反应和信息交锋")
        actions.append("先补字数，不要靠总结句和解释段灌水")
    if thrills.get("overall") == "negative":
        warnings.append("静态爽毒点评估偏负面；这是启发式信号，需结合上下文确认是否真的失衡")
        actions.append("人工复核受压后是否给出信息收益、关系回应或反制基础，不要只看关键词分数")
    if emotion.get("opening_emotion") == "neutral" and emotion.get("ending_emotion") == "neutral":
        warnings.append("情绪曲线偏平，检查是否缺少冲突抬升或结尾钩子")
        actions.append("把结尾停在动作、发现、选择或危险上")
    if dialogue_stats["avg_chars_per_line"] >= 28:
        warnings.append("平均对白偏长，检查对白是否承担了过多解释工作")
        actions.append("把部分台词改写成动作、环境或心理承载")
    if dialogue_findings:
        warnings.append(f"对白专审命中 {len(dialogue_findings)} 条规则")
    if lint_findings:
        warnings.append(f"规则检查命中 {len(lint_findings)} 条")

    rule_action_map = {
        "ending_summary": "删除结尾总结句，改停在未决动作或危险上",
        "explanation_tone": "把说明句改写成动作、代价和后果",
        "dialogue_exposition": "压缩对白说明感，避免人物替作者讲设定",
        "transition_overexplained": "删掉过桥连接词堆积，让因果落回场面",
        "ai_tells": "把抽象 AI 套语换成具体物体、动作和关系压力",
        "abstract_psychology": "把抽象心理直说改写成动作、反应、停顿和后果",
    }
    for finding in lint_findings:
        suggestion = rule_action_map.get(str(finding.get("id")))
        if suggestion and suggestion not in actions:
            actions.append(suggestion)

    if not actions:
        actions.append("本章未见明显硬伤，按连贯性清单做一次人工复核即可")

    if blocking_issues:
        verdict = "fail"
    elif warnings:
        verdict = "warn"
    else:
        verdict = "pass"

    dossier = build_review_dossier(
        chapter_path,
        content,
        project_dir,
        consistency_report,
        lint_findings,
        dialogue_findings,
        {
            "wordcount": wordcount,
            "emotion": emotion,
            "thrills": thrills,
            "dialogue": dialogue_stats,
        },
    )

    return {
        "file": str(chapter_path),
        "project_dir": str(project_dir) if project_dir else consistency_report.get("project_dir"),
        "review_mode": "static_precheck_plus_dossier",
        "verdict": verdict,
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "metrics": {
            "wordcount": wordcount,
            "emotion": emotion,
            "thrills": thrills,
            "dialogue": dialogue_stats,
        },
        "lint_findings": lint_findings,
        "dialogue_findings": dialogue_findings,
        "consistency": consistency_report,
        "actions": actions[:6],
        "dossier": dossier,
    }


def print_review_summary(report: dict[str, Any]) -> None:
    metrics = report["metrics"]
    wordcount = metrics["wordcount"]
    emotion = metrics["emotion"]
    thrills = metrics["thrills"]
    dialogue = metrics["dialogue"]

    print("\n" + "=" * 60)
    print(f"Review 预审与审稿稿本: {Path(report['file']).name}")
    print("=" * 60)
    print(f"- 模式: {report.get('review_mode', 'unknown')}")
    print(f"- 静态预审 Verdict: {report['verdict']}")
    print(f"- 语义审稿完成: {report['dossier']['semantic_review_complete']}")
    print(f"- 审稿要求: {report['dossier']['semantic_review_requires']}")
    print(f"- 项目目录: {report.get('project_dir') or '未定位'}")
    print(f"- 字数: {wordcount.get('word_count', 0)} ({wordcount.get('status', 'unknown')})")
    print(f"- 情绪走向: {emotion.get('transition', 'unknown')}")
    print(
        f"- 爽点/毒点: thrill={thrills.get('thrill_score', 0)}, "
        f"poison={thrills.get('poison_score', 0)}, overall={thrills.get('overall', 'unknown')}"
    )
    print("- 说明: 爽毒点评估是静态启发式信号，不替代上下文语义判断。")
    print(
        f"- 对白: lines={dialogue['dialogue_lines']}, chars={dialogue['dialogue_chars']}, "
        f"avg={dialogue['avg_chars_per_line']}"
    )
    print(f"- 规则命中: {len(report['lint_findings'])}")
    print(f"- 对白命中: {len(report['dialogue_findings'])}")
    print("- 说明: 当前命令只完成静态预审，并生成审稿稿本；它不再冒充已经完成语义审稿。")

    print_named_list("阻塞问题", report.get("blocking_issues", []))
    print_named_list("风险提示", report.get("warnings", []))

    if report["lint_findings"]:
        print("\n规则命中详情:")
        for item in report["lint_findings"][:8]:
            print(f"- {item['name']} [{item['severity']}] {item['message']}")
            for evidence in item.get("evidence", [])[:2]:
                line = f" line={evidence['line']}" if evidence.get("line") else ""
                print(f"  - {evidence['label']}{line}: {evidence['excerpt']}")

    if report["dialogue_findings"]:
        print("\n对白专审命中:")
        for item in report["dialogue_findings"][:5]:
            print(f"- {item['name']} [{item['severity']}] {item['message']}")

    print("\n自动预审检查:")
    for item in report["dossier"]["auto_checks"]:
        print(f"- {item['title']} [{item['status']}] {item['reason']}")
        for evidence in item.get("evidence", [])[:2]:
            print(f"  - {evidence}")

    print("\n待完成语义审稿问题:")
    for item in report["dossier"]["semantic_questions"]:
        print(f"- {item['question']}")
        print(f"  - 为什么看: {item['why']}")
        for evidence in item.get("evidence", [])[:3]:
            if evidence:
                print(f"  - 证据: {evidence}")

    print_named_list("建议下一轮动作", report.get("actions", []))


def read_extra_texts(inline_values: list[str] | None, file_values: list[str] | None) -> list[str]:
    texts: list[str] = []
    for value in inline_values or []:
        normalized = value.strip()
        if normalized:
            texts.append(normalized)
    for file_value in file_values or []:
        content = Path(file_value).expanduser().resolve().read_text(encoding="utf-8").strip()
        if content:
            texts.append(content)
    return texts


def build_marketing_brief(
    project_dir: Path,
    summary: dict[str, Any],
    extra_prompts: list[str],
    ai_words: list[str],
    references: list[str],
    platform: str | None = None,
    audience: str | None = None,
    angle: str | None = None,
) -> dict[str, Any]:
    author_intent = read_text(project_dir / "docs" / "作者意图.md")
    current_focus = read_text(project_dir / "docs" / "当前焦点.md")
    project_outline = read_text(resolve_project_outline_path(project_dir) or project_dir / PROJECT_OUTLINE_PATH)
    chapter_plan = read_text(resolve_chapter_plan_path(project_dir) or project_dir / CHAPTER_PLAN_PATH)

    long_goal_lines = extract_section_lines(author_intent, "长期目标")
    platform_lines = extract_section_lines(author_intent, "平台与商业约束")
    focus_lines = extract_section_lines(current_focus, "最近 1-3 章优先事项")
    no_go_lines = extract_section_lines(current_focus, "最近 1-3 章禁止偏航项")
    project_outline_excerpt = excerpt_text(project_outline, keyword="## 主线三步法骨架", max_chars=500)
    if not project_outline_excerpt or project_outline_excerpt.count("[") >= 2:
        project_outline_excerpt = "未读取到可直接投喂的项目总纲摘录；请先补充 docs/项目总纲.md 的主线骨架。"
    chapter_plan_excerpt = excerpt_text(chapter_plan, keyword="## 章节规划", max_chars=800)
    if not chapter_plan_excerpt or chapter_plan_excerpt.count("[") >= 2:
        chapter_plan_excerpt = "未读取到可直接投喂的章节规划摘录；请先补充 docs/章节规划.md 的真实章节规划或章节摘要。"

    compiled_prompt_lines = [
        "你是平台向网文商业化包装助手。",
        "请基于下面的项目 Brief 输出：书名备选、平台卖点一句话、长简介、渠道文案、章节推送钩子、读者承诺。",
        "不要把故事写成纯文学自嗨文案；优先突出题材钩子、长期回报、人物冲突和追读牵引。",
    ]
    if platform:
        compiled_prompt_lines.append(f"目标平台：{platform}")
    if audience:
        compiled_prompt_lines.append(f"目标读者：{audience}")
    if angle:
        compiled_prompt_lines.append(f"本次主打商业角度：{angle}")
    compiled_prompt_lines.extend(f"补充提示词：{item}" for item in extra_prompts)
    if ai_words:
        compiled_prompt_lines.append("可用商业词/AI 味词汇：" + " / ".join(ai_words))
    if references:
        compiled_prompt_lines.append("补充参考材料：")
        compiled_prompt_lines.extend(f"参考：{item}" for item in references)

    brief_lines = [
        f"# Marketing Brief - {summary['book_title']}",
        "",
        "## 项目定位",
        f"- 书名：{summary['book_title']}",
        f"- 创作阶段：{summary['stage']}",
        f"- 目标平台：{platform or '未指定'}",
        f"- 目标读者：{audience or '未指定'}",
        f"- 当前商业角度：{angle or '未指定'}",
        "",
        "## 长期卖点",
        *(long_goal_lines or ["- 未从 docs/作者意图.md 读取到长期卖点"]),
        "",
        "## 平台与商业约束",
        *(platform_lines or ["- 未从 docs/作者意图.md 读取到平台约束"]),
        "",
        "## 近期宣传焦点",
        *(focus_lines or ["- 未从 docs/当前焦点.md 读取到近期焦点"]),
        "",
        "## 禁止偏航项",
        *(no_go_lines or ["- 未从 docs/当前焦点.md 读取到禁止偏航项"]),
        "",
        "## 最近剧情抓手",
        *(summary.get("recent_summaries", []) or ["- 暂无最近章节摘要"]),
        "",
        "## 活跃伏笔与钩子压力",
        *(summary.get("active_plots", []) or ["- 暂无活跃伏笔"]),
        "",
        "## 可复用营销 Prompt",
        *[f"- {line}" for line in compiled_prompt_lines],
        "",
        "## 补充词库",
        *([f"- {item}" for item in ai_words] or ["- 暂无额外词汇"]),
        "",
        "## 参考摘录",
        *([f"- {item}" for item in references] or ["- 暂无额外参考"]),
        "",
        "## 项目总纲摘录",
        project_outline_excerpt,
        "",
        "## 章节规划摘录",
        chapter_plan_excerpt,
        "",
    ]

    return {
        "project_dir": str(project_dir),
        "book_title": summary["book_title"],
        "platform": platform or "未指定",
        "audience": audience or "未指定",
        "angle": angle or "未指定",
        "prompt_lines": compiled_prompt_lines,
        "brief_markdown": "\n".join(brief_lines),
    }


def print_layer_catalog(title: str, items: list[dict[str, Any]], json_mode: bool = False) -> None:
    if json_mode:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    for item in items:
        if "group" in item:
            print(f"- {item['group']}: {', '.join(item['commands'])}")
            continue
        sources = ", ".join(item.get("sources", []))
        steps = " -> ".join(item.get("steps", []))
        print(f"- {item['id']}: {item['title']}")
        print(f"  {item['summary']}")
        if sources:
            print(f"  sources: {sources}")
        if steps:
            print(f"  steps: {steps}")


def handle_dialogue_pass(args: argparse.Namespace) -> int:
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    if not chapter_path.exists():
        print(json.dumps({"error": f"文件不存在: {chapter_path}"}, ensure_ascii=False, indent=2))
        return 2

    content = chapter_path.read_text(encoding="utf-8")
    stats = extract_dialogue_stats(content)
    rules = [
        rule
        for rule in load_lint_rules(resolve_rule_project_dir(chapter_path=chapter_path, rule_set=args.rule_set), rule_set=args.rule_set)
        if str(rule.get("scope", "")) == "dialogue"
    ]
    findings = lint_chapter_text(content, rules)
    result = {
        "file": str(chapter_path),
        "stats": stats,
        "findings": findings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("\n" + "=" * 60)
    print(f"对白专审: {chapter_path.name}")
    print("=" * 60)
    print(f"- 对白行数: {stats['dialogue_lines']}")
    print(f"- 对白总字数: {stats['dialogue_chars']}")
    print(f"- 平均每句长度: {stats['avg_chars_per_line']}")
    if stats["long_lines"]:
        print("- 过长对白示例:")
        for item in stats["long_lines"]:
            print(f"  - {excerpt_text(item, max_chars=60)}")
    if findings:
        print("- 规则命中:")
        for item in findings:
            print(f"  - {item['name']} [{item['severity']}] {item['message']}")
    else:
        print("- 规则命中: 无")
    return 0


def handle_consistency(args: argparse.Namespace) -> int:
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    project_dir = Path(args.project_path).expanduser().resolve() if getattr(args, "project_path", None) else None
    report = build_consistency_report(chapter_path, project_dir=project_dir)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_consistency_summary(report)
    return 0


def handle_review(args: argparse.Namespace) -> int:
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    project_dir = Path(args.project_path).expanduser().resolve() if getattr(args, "project_path", None) else None
    report = build_review_report(chapter_path, project_dir=project_dir)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_review_summary(report)

    return 0 if report["verdict"] == "pass" else 2 if report["blocking_issues"] else 1


def handle_next_chapter(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary, failures = evaluate_preflight(project_dir)
    chapter_num = determine_target_chapter_num(project_dir, summary, explicit=args.chapter_num)
    guidance = read_guidance(args)

    if args.json and failures:
        print(json.dumps({"project_dir": str(project_dir), "chapter": chapter_num, "failures": failures}, ensure_ascii=False, indent=2))
        return 2

    print_resume_summary(summary)
    if failures:
        print_gate_failures("前置校验失败: next-chapter 未通过", failures)
        return 2

    runtime_result = materialize_runtime_package(project_dir, summary, chapter_num, args.chapter_title, guidance)

    start_args = argparse.Namespace(
        project_path=str(project_dir),
        chapter_num=chapter_num,
        chapter_title=args.chapter_title,
        core_event=args.core_event,
        hook=args.hook,
        next_goal=args.next_goal,
        viewpoint=args.viewpoint,
        protagonist_location=args.protagonist_location,
        protagonist_state=args.protagonist_state,
        stage=args.stage or "正文创作中",
        target_total_words=args.target_total_words,
        target_volumes=args.target_volumes,
        current_volume=args.current_volume,
        current_phase=args.current_phase,
        phase_goal=args.phase_goal,
        pending_setting_sync=args.pending_setting_sync,
        plot_note=args.plot_note,
    )
    start_code = handle_start(start_args)
    if start_code != 0:
        return start_code

    finished = False
    review_report: dict[str, Any] | None = None
    if args.chapter_path or args.summary:
        if not args.chapter_path or not args.summary:
            print_gate_failures("next-chapter finish 参数不完整", ["执行 finish 时必须同时提供 --chapter-path 与 --summary"])
            return 2
        finish_args = argparse.Namespace(
            project_path=str(project_dir),
            chapter_num=chapter_num,
            chapter_title=args.chapter_title,
            core_event=args.core_event,
            hook=args.hook,
            next_goal=args.next_goal,
            viewpoint=args.viewpoint,
            protagonist_location=args.protagonist_location,
            protagonist_state=args.protagonist_state,
            stage=args.stage or "正文创作中",
            target_total_words=args.target_total_words,
            target_volumes=args.target_volumes,
            current_volume=args.current_volume,
            current_phase=args.current_phase,
            phase_goal=args.phase_goal,
            pending_setting_sync=args.pending_setting_sync,
            plot_note=args.plot_note,
            chapter_path=args.chapter_path,
            summary=args.summary,
            word_count=args.word_count,
            skip_checks=args.skip_checks,
        )
        finish_code = handle_finish(finish_args)
        if finish_code != 0:
            return finish_code
        finished = True
        review_report = build_review_report(Path(args.chapter_path).expanduser().resolve(), project_dir=project_dir)

    result = {
        "project_dir": str(project_dir),
        "chapter": chapter_num,
        "runtime": runtime_result,
        "started": True,
        "finished": finished,
        "review_verdict": review_report["verdict"] if review_report else None,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("\n" + "=" * 60)
    print("续写下一章工作流")
    print("=" * 60)
    print(f"- 章节: 第{chapter_num}章")
    print(f"- 已执行: preflight -> resume -> plan -> compose -> start")
    print(f"- 意图文件: {runtime_result['intent_path']}")
    print(f"- 场景卡文件: {runtime_result['scenes_path']}")
    if finished:
        print("- 已执行: finish")
        print(f"- Review Verdict: {review_report['verdict'] if review_report else 'unknown'}")
    else:
        print("- finish 未执行: 正文完成后，用同一命令补上 --chapter-path 和 --summary 即可闭环")
    return 0


def handle_marketing(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    extra_prompts = read_extra_texts(args.prompt, args.prompt_file)
    references = read_extra_texts(args.reference, args.reference_file)
    brief = build_marketing_brief(
        project_dir,
        summary,
        extra_prompts=extra_prompts,
        ai_words=args.ai_word or [],
        references=references,
        platform=args.platform,
        audience=args.audience,
        angle=args.angle,
    )

    if args.output_file:
        output_path = Path(args.output_file).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(brief["brief_markdown"], encoding="utf-8")

    if args.json:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
        return 0

    print(brief["brief_markdown"])
    if args.output_file:
        print(f"输出文件: {Path(args.output_file).expanduser().resolve()}")
    return 0


def handle_rules(args: argparse.Namespace) -> int:
    print_layer_catalog("Rule Layer", RULE_LAYER_CATALOG, json_mode=args.json)
    return 0


def handle_workflows(args: argparse.Namespace) -> int:
    print_layer_catalog("Workflow Layer", WORKFLOW_LAYER_CATALOG, json_mode=args.json)
    return 0


def handle_commands(args: argparse.Namespace) -> int:
    print_layer_catalog("Command Layer", COMMAND_LAYER_CATALOG, json_mode=args.json)
    return 0


def add_progress_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project_path", help="项目根目录")
    parser.add_argument("chapter_num", type=int, help="章节号")
    add_progress_option_arguments(parser)


def add_progress_option_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--chapter-title", help="章节标题")
    parser.add_argument("--core-event", help="本章核心事件")
    parser.add_argument("--hook", help="本章悬念钩子")
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


def handle_init(args: argparse.Namespace) -> int:
    create_novel_project(
        args.project_name,
        target_dir=args.target_dir,
        force=args.force,
        mode=args.mode,
        complex_relationships=args.complex_relationships,
        romance_focus=args.romance_focus,
    )
    return 0


def handle_resume(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    print_resume_summary(summarize_project(project_dir))
    return 0


def handle_plan(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    chapter_num = determine_target_chapter_num(project_dir, summary, explicit=args.chapter_num)
    guidance = read_guidance(args)
    result = materialize_plan(project_dir, summary, chapter_num, args.chapter_title, guidance)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_resume_summary(summary)
        print("\n" + "=" * 60)
        print("章节意图已生成")
        print("=" * 60)
        print(f"章节: 第{chapter_num}章")
        print(f"意图文件: {result['intent_path']}")
        print(f"目标: {result['goal']}")
    return 0


def handle_compose(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    chapter_num = determine_target_chapter_num(project_dir, summary, explicit=args.chapter_num)
    guidance = read_guidance(args)
    result = materialize_runtime_package(project_dir, summary, chapter_num, args.chapter_title, guidance)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_resume_summary(summary)
        print("\n" + "=" * 60)
        print("章节运行时产物已生成")
        print("=" * 60)
        print(f"章节: 第{chapter_num}章")
        print(f"意图文件: {result['intent_path']}")
        print(f"上下文文件: {result['context_path']}")
        print(f"场景卡文件: {result['scenes_path']}")
        print(f"规则栈文件: {result['rule_stack_path']}")
        print(f"轨迹文件: {result['trace_path']}")
    return 0


def handle_start(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    target_label = f"第{args.chapter_num}章"
    current_chapter_num = parse_chapter_number_from_text(summary["current_chapter"])
    effective_next_goal = args.next_goal or summary["next_goal"]
    effective_current_volume = args.current_volume or summary["current_volume"]
    effective_current_phase = args.current_phase or summary["current_phase"]

    failures: list[str] = []
    if summary["missing_files"]:
        failures.append("缺失项目记忆文件，先修记忆，再标记章节进行中")
    if requires_longform_governance(project_dir, summary) and summary["missing_longform_files"]:
        failures.append("缺失超长篇治理文件，先执行 bootstrap-longform")
    if effective_next_goal in {"未记录", "无", ""}:
        failures.append("未记录下一章目标，start 前必须先补 task_log.md 或传入 --next-goal")
    if current_chapter_num not in {None, args.chapter_num} and summary["current_chapter"] != "无":
        failures.append(f"当前已有进行中章节：{summary['current_chapter']}，不要并发开写多个章节")
    if requires_longform_governance(project_dir, summary) and effective_current_volume in {"未记录", "未开始", "无", ""}:
        failures.append("start 前必须先明确当前卷")
    if requires_longform_governance(project_dir, summary) and effective_current_phase in {"未记录", "未开始", "无", ""}:
        failures.append("start 前必须先明确当前阶段")

    if failures:
        print_resume_summary(summary)
        print_gate_failures("前置校验失败: start 未通过", failures)
        return 2

    update_progress(
        project_path=args.project_path,
        chapter_num=args.chapter_num,
        chapter_title=args.chapter_title,
        core_event=args.core_event,
        hook=args.hook,
        next_goal=args.next_goal,
        viewpoint=args.viewpoint,
        protagonist_location=args.protagonist_location,
        protagonist_state=args.protagonist_state,
        stage=args.stage or "正文创作中",
        target_total_words=args.target_total_words,
        target_volumes=args.target_volumes,
        current_volume=args.current_volume,
        current_phase=args.current_phase,
        phase_goal=args.phase_goal,
        pending_setting_sync=args.pending_setting_sync,
        status=STATUS_IN_PROGRESS,
    )
    return 0


def handle_check(args: argparse.Namespace) -> int:
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    print_check_summary(build_check_report(chapter_path, rule_project_dir=resolve_rule_project_dir(chapter_path=chapter_path)))
    return 0


def handle_finish(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    chapter_path = Path(args.chapter_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    target_label = f"第{args.chapter_num}章"
    current_chapter_num = parse_chapter_number_from_text(summary["current_chapter"])

    failures: list[str] = []
    if summary["missing_files"]:
        failures.append("缺失项目记忆文件，finish 前必须先恢复项目记忆")
    if requires_longform_governance(project_dir, summary) and summary["missing_longform_files"]:
        failures.append("缺失超长篇治理文件，finish 前必须先补齐")
    if current_chapter_num != args.chapter_num:
        failures.append(f"当前处理章节不是 {target_label}，请先执行 start 并保持章节状态一致")
    if not chapter_path.exists():
        failures.append(f"章节文件不存在：{chapter_path}")
    if not args.summary:
        failures.append("finish 必须提供 --summary，用于同步章节摘要和项目记忆")

    if failures:
        print_resume_summary(summary)
        print_gate_failures("前置校验失败: finish 未通过", failures)
        return 2

    report = None
    if not args.skip_checks:
        report = build_check_report(chapter_path)
        print_check_summary(report)

    word_count = args.word_count
    if word_count is None:
        result = report["wordcount"] if report else check_chapter(str(chapter_path))
        word_count = result.get("word_count")

    update_progress(
        project_path=args.project_path,
        chapter_num=args.chapter_num,
        word_count=word_count,
        chapter_title=args.chapter_title,
        summary=args.summary,
        core_event=args.core_event,
        hook=args.hook,
        next_goal=args.next_goal,
        viewpoint=args.viewpoint,
        protagonist_location=args.protagonist_location,
        protagonist_state=args.protagonist_state,
        stage=args.stage or "正文创作中",
        target_total_words=args.target_total_words,
        target_volumes=args.target_volumes,
        current_volume=args.current_volume,
        current_phase=args.current_phase,
        phase_goal=args.phase_goal,
        pending_setting_sync=args.pending_setting_sync,
        plot_note=args.plot_note,
        status=STATUS_DONE,
    )
    return 0


def handle_governance(args: argparse.Namespace) -> int:
    update_governance_state(
        args.project_path,
        target_total_words=args.target_total_words,
        target_volumes=args.target_volumes,
        current_volume=args.current_volume,
        current_phase=args.current_phase,
        phase_goal=args.phase_goal,
        pending_setting_sync=args.pending_setting_sync,
        clear_pending_setting_sync=args.clear_pending_setting_sync,
    )
    print_resume_summary(summarize_project(Path(args.project_path).expanduser().resolve()))
    return 0


def build_audit_payload(project_dir: Path, scope: str) -> tuple[dict, list[str], list[str], tuple[int, int]]:
    summary = summarize_project(project_dir)
    chapter_count, total_words = compute_manuscript_stats(project_dir)

    issues: list[str] = []
    warnings: list[str] = []

    if summary["missing_files"]:
        issues.append("项目记忆文件缺失")
    if summary["missing_longform_files"]:
        issues.append("超长篇治理文件缺失")
    if summary["pending_setting_sync"] not in {"无", "未记录", ""}:
        warnings.append(f"存在待同步的设定变更：{summary['pending_setting_sync']}")
    if summary["active_plot_count"] >= 12:
        warnings.append(f"活跃伏笔较多（{summary['active_plot_count']}），检查伏笔债务")
    if chapter_count > 0 and total_words > 0 and total_words / chapter_count < 2500:
        warnings.append("平均章字数偏低，检查是否切章过碎或阶段回报过短")

    if scope == "stage":
        if summary["current_phase"] in {"未记录", "未开始", "无", ""}:
            issues.append("未记录当前阶段")
        if summary["phase_goal"] in {"未记录", "无", ""}:
            issues.append("未记录当前阶段目标")
        phase_plan = read_text(project_dir / "docs" / "阶段规划.md")
        current_phase = summary["current_phase"]
        if current_phase not in {"未记录", "未开始", "无", ""} and current_phase not in phase_plan:
            warnings.append("当前阶段未在 docs/阶段规划.md 中显式出现")
    else:
        if summary["current_volume"] in {"未记录", "未开始", "无", ""}:
            issues.append("未记录当前卷")
        volume_plan = read_text(project_dir / "docs" / "卷纲.md")
        current_volume = summary["current_volume"]
        if current_volume not in {"未记录", "未开始", "无", ""} and current_volume not in volume_plan:
            warnings.append("当前卷未在 docs/卷纲.md 中显式出现")

    return summary, issues, warnings, (chapter_count, total_words)


def handle_bootstrap_longform(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    ensure_longform_governance_files(project_dir, force=args.force)
    summary = summarize_project(project_dir)
    print_resume_summary(summary)
    print("\n已补齐超长篇治理文件。")
    return 0


def handle_audit(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    scope = args.scope
    summary, issues, warnings, stats = build_audit_payload(project_dir, scope)
    chapter_count, total_words = stats
    print_resume_summary(summary)

    print("\n" + "=" * 60)
    print(f"{'阶段' if scope == 'stage' else '卷'}审计")
    print("=" * 60)
    print(f"累计章节: {chapter_count}")
    print(f"累计字数: {total_words}")

    if issues:
        print("\n阻塞问题:")
        for item in issues:
            print(f"- {item}")
    else:
        print("\n阻塞问题: 无")

    if warnings:
        print("\n风险提示:")
        for item in warnings:
            print(f"- {item}")
    else:
        print("\n风险提示: 无")

    status = "pass" if not issues else "fail"
    scope_name = "阶段" if scope == "stage" else "卷"
    summary_line = (
        f"{scope_name}审计 | 章节={chapter_count} | 字数={total_words} | "
        f"阻塞={len(issues)} | 风险={len(warnings)}"
    )
    update_task_log_audit(project_dir, scope, status, summary_line)

    if issues:
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="小说项目统一工作流入口")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rules_parser = subparsers.add_parser("rules", help="查看 Rule 层索引")
    rules_parser.add_argument("--json", action="store_true", help="输出 JSON")
    rules_parser.set_defaults(handler=handle_rules)

    workflows_parser = subparsers.add_parser("workflows", help="查看 Workflow 层索引")
    workflows_parser.add_argument("--json", action="store_true", help="输出 JSON")
    workflows_parser.set_defaults(handler=handle_workflows)

    commands_parser = subparsers.add_parser("commands", help="查看 Command 层索引")
    commands_parser.add_argument("--json", action="store_true", help="输出 JSON")
    commands_parser.set_defaults(handler=handle_commands)

    init_parser = subparsers.add_parser("init", help="初始化小说项目")
    init_parser.add_argument("project_name", help="项目名称")
    init_parser.add_argument("--target-dir", help="项目创建目录，默认当前目录")
    init_parser.add_argument("--mode", choices=("single", "dual", "ensemble"), default="single")
    init_parser.add_argument("--complex-relationships", action="store_true", help="创建关系图模板")
    init_parser.add_argument("--romance-focus", action="store_true", help="感情线重要时创建关系图模板")
    init_parser.add_argument("--force", action="store_true", help="覆盖已存在模板")
    init_parser.set_defaults(handler=handle_init)

    resume_parser = subparsers.add_parser("resume", help="恢复项目摘要")
    resume_parser.add_argument("project_path", help="项目根目录")
    resume_parser.set_defaults(handler=handle_resume)

    bootstrap_parser = subparsers.add_parser("bootstrap-longform", help="为已有项目补齐超长篇治理文件")
    bootstrap_parser.add_argument("project_path", help="项目根目录")
    bootstrap_parser.add_argument("--force", action="store_true", help="覆盖已存在的治理文件")
    bootstrap_parser.set_defaults(handler=handle_bootstrap_longform)

    plan_parser = subparsers.add_parser("plan", help="生成本章意图文件")
    plan_parser.add_argument("project_path", help="项目根目录")
    plan_parser.add_argument("--chapter-num", type=int, help="目标章节号；默认自动推断")
    plan_parser.add_argument("--chapter-title", help="目标章节标题")
    plan_parser.add_argument("--guidance", help="本章额外引导")
    plan_parser.add_argument("--guidance-file", help="从文件读取本章引导")
    plan_parser.add_argument("--json", action="store_true", help="输出 JSON")
    plan_parser.set_defaults(handler=handle_plan)

    compose_parser = subparsers.add_parser("compose", help="生成本章运行时上下文/规则栈/轨迹")
    compose_parser.add_argument("project_path", help="项目根目录")
    compose_parser.add_argument("--chapter-num", type=int, help="目标章节号；默认自动推断")
    compose_parser.add_argument("--chapter-title", help="目标章节标题")
    compose_parser.add_argument("--guidance", help="本章额外引导")
    compose_parser.add_argument("--guidance-file", help="从文件读取本章引导")
    compose_parser.add_argument("--json", action="store_true", help="输出 JSON")
    compose_parser.set_defaults(handler=handle_compose)

    governance_parser = subparsers.add_parser("governance", help="同步超长篇治理状态")
    governance_parser.add_argument("project_path", help="项目根目录")
    governance_parser.add_argument("--target-total-words", help="目标总字数，例如 3000000 或 300万")
    governance_parser.add_argument("--target-volumes", help="目标卷数")
    governance_parser.add_argument("--current-volume", help="当前卷，例如 第一卷")
    governance_parser.add_argument("--current-phase", help="当前阶段，例如 阶段1")
    governance_parser.add_argument("--phase-goal", help="当前阶段目标")
    governance_parser.add_argument("--pending-setting-sync", help="待同步的设定变更摘要")
    governance_parser.add_argument("--clear-pending-setting-sync", action="store_true", help="清空待同步设定变更")
    governance_parser.set_defaults(handler=handle_governance)

    preflight_parser = subparsers.add_parser("preflight", help="续写/开写前的硬门槛校验")
    preflight_parser.add_argument("project_path", help="项目根目录")
    preflight_parser.set_defaults(handler=handle_preflight)

    start_parser = subparsers.add_parser("start", help="将目标章节标记为进行中")
    add_progress_arguments(start_parser)
    start_parser.set_defaults(handler=handle_start)

    check_parser = subparsers.add_parser("check", help="汇总检查单章")
    check_parser.add_argument("chapter_path", help="章节文件路径")
    check_parser.set_defaults(handler=handle_check)

    lint_parser = subparsers.add_parser("lint", help="按规则检查单章")
    lint_parser.add_argument("chapter_path", help="章节文件路径")
    lint_parser.add_argument("--rule-set", default="novel-lint", help="规则集目录名，默认 novel-lint")
    lint_parser.add_argument("--json", action="store_true", help="输出 JSON")
    lint_parser.set_defaults(handler=handle_lint)

    dialogue_parser = subparsers.add_parser("dialogue-pass", help="对白专审")
    dialogue_parser.add_argument("chapter_path", help="章节文件路径")
    dialogue_parser.add_argument("--rule-set", default="novel-lint", help="规则集目录名，默认 novel-lint")
    dialogue_parser.add_argument("--json", action="store_true", help="输出 JSON")
    dialogue_parser.set_defaults(handler=handle_dialogue_pass)

    consistency_parser = subparsers.add_parser("consistency", help="连贯性结构化检查")
    consistency_parser.add_argument("chapter_path", help="章节文件路径")
    consistency_parser.add_argument("--project-path", help="项目根目录；不传则尝试自动定位")
    consistency_parser.add_argument("--json", action="store_true", help="输出 JSON")
    consistency_parser.set_defaults(handler=handle_consistency)

    review_parser = subparsers.add_parser("review", help="生成静态预审 + 审稿稿本，不再冒充已完成语义审稿")
    review_parser.add_argument("chapter_path", help="章节文件路径")
    review_parser.add_argument("--project-path", help="项目根目录；不传则尝试自动定位")
    review_parser.add_argument("--json", action="store_true", help="输出 JSON")
    review_parser.set_defaults(handler=handle_review)

    finish_parser = subparsers.add_parser("finish", help="检查并同步章节完成状态")
    add_progress_arguments(finish_parser)
    finish_parser.add_argument("chapter_path", help="章节文件路径")
    finish_parser.add_argument("--summary", help="本章摘要")
    finish_parser.add_argument("--word-count", type=int, help="手动指定章节字数")
    finish_parser.add_argument("--skip-checks", action="store_true", help="跳过写后检查")
    finish_parser.set_defaults(handler=handle_finish)

    audit_parser = subparsers.add_parser("audit", help="阶段/卷审计")
    audit_parser.add_argument("project_path", help="项目根目录")
    audit_parser.add_argument("--scope", choices=("stage", "volume"), default="stage", help="审计范围")
    audit_parser.set_defaults(handler=handle_audit)

    next_chapter_parser = subparsers.add_parser("next-chapter", help="把 preflight -> resume -> plan -> compose -> start -> finish 包成单入口")
    next_chapter_parser.add_argument("project_path", help="项目根目录")
    next_chapter_parser.add_argument("--chapter-num", type=int, help="目标章节号；默认自动推断")
    next_chapter_parser.add_argument("--guidance", help="本章额外引导")
    next_chapter_parser.add_argument("--guidance-file", help="从文件读取本章引导")
    next_chapter_parser.add_argument("--chapter-path", help="正文文件路径；提供时自动执行 finish")
    next_chapter_parser.add_argument("--summary", help="本章摘要；与 --chapter-path 一起触发 finish")
    next_chapter_parser.add_argument("--word-count", type=int, help="手动指定章节字数")
    next_chapter_parser.add_argument("--skip-checks", action="store_true", help="finish 时跳过写后检查")
    next_chapter_parser.add_argument("--json", action="store_true", help="输出 JSON")
    add_progress_option_arguments(next_chapter_parser)
    next_chapter_parser.set_defaults(handler=handle_next_chapter)

    marketing_parser = subparsers.add_parser("marketing", help="生成商业化包装 Brief / Prompt Pack")
    marketing_parser.add_argument("project_path", help="项目根目录")
    marketing_parser.add_argument("--platform", help="目标平台")
    marketing_parser.add_argument("--audience", help="目标读者")
    marketing_parser.add_argument("--angle", help="本次主打商业角度")
    marketing_parser.add_argument("--prompt", action="append", help="补充提示词，可重复传入")
    marketing_parser.add_argument("--prompt-file", action="append", help="从文件补充提示词，可重复传入")
    marketing_parser.add_argument("--ai-word", action="append", help="补充商业词/AI 味词汇，可重复传入")
    marketing_parser.add_argument("--reference", action="append", help="补充参考文本，可重复传入")
    marketing_parser.add_argument("--reference-file", action="append", help="从文件补充参考，可重复传入")
    marketing_parser.add_argument("--output-file", help="将营销 Brief 写入文件")
    marketing_parser.add_argument("--json", action="store_true", help="输出 JSON")
    marketing_parser.set_defaults(handler=handle_marketing)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
