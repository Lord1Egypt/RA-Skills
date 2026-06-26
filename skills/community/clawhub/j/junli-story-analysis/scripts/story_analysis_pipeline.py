#!/usr/bin/env python3
"""统一的初始化、恢复、阶段推进、质检、收束与修复入口。"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    from bootstrap_story_analysis import (
        Chunk,
        METHOD_CARD_NAMES,
        build_book_profile_draft,
        build_book_profile_output,
        build_case_candidate_notes,
        build_case_card_template,
        build_case_type_reference,
        build_chapter_method_card,
        build_chunks,
        build_conflict_character_method_card,
        build_emotion_method_card,
        build_lines,
        build_longform_style_method_card,
        build_method_candidate_notes,
        build_opening_method_card,
        build_outline_method_card,
        detect_sections,
        ensure_dir,
        initialize_project,
        normalize_text,
        read_text as read_source_text,
        render_chunk_index,
        render_extraction_card_template,
        render_stage_plan,
        render_use_guide,
        safe_book_name,
        write_text,
        write_json,
    )
except ModuleNotFoundError:
    from scripts.bootstrap_story_analysis import (
        Chunk,
        METHOD_CARD_NAMES,
        build_book_profile_draft,
        build_book_profile_output,
        build_case_candidate_notes,
        build_case_card_template,
        build_case_type_reference,
        build_chapter_method_card,
        build_chunks,
        build_conflict_character_method_card,
        build_emotion_method_card,
        build_lines,
        build_longform_style_method_card,
        build_method_candidate_notes,
        build_opening_method_card,
        build_outline_method_card,
        detect_sections,
        ensure_dir,
        initialize_project,
        normalize_text,
        read_text as read_source_text,
        render_chunk_index,
        render_extraction_card_template,
        render_stage_plan,
        render_use_guide,
        safe_book_name,
        write_text,
        write_json,
    )


PROGRESS_FILE = Path("workspace/analysis-progress.json")
REQUIRED_SUPPORT_FILES = (
    "workspace/manifest.json",
    "workspace/chunk-index.md",
    "workspace/stage-plan.md",
    "workspace/use-guide.md",
    "drafts/书籍画像草稿.md",
    "drafts/方法候选笔记.md",
    "drafts/案例候选笔记.md",
    "outputs/书籍画像.md",
)


@dataclass(frozen=True)
class Stage:
    stage_id: int
    chunk_ids: list[str]

    @property
    def chunk_range(self) -> str:
        return f"{self.chunk_ids[0]} - {self.chunk_ids[-1]}"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def write_json_file(path: Path, data: dict) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_chunk_raw(path: Path) -> Chunk:
    text = path.read_text(encoding="utf-8")

    def match(pattern: str, label: str) -> str:
        found = re.search(pattern, text, re.MULTILINE)
        if not found:
            raise RuntimeError(f"无法从 {path} 解析 {label}")
        return found.group(1).strip()

    title = match(r"^- 标题：(.*)$", "标题")
    start = int(match(r"^- 起始字符：(.*)$", "起始字符"))
    end = int(match(r"^- 结束字符：(.*)$", "结束字符"))
    char_count = int(match(r"^- 字符数：(.*)$", "字符数"))
    source_mode = match(r"^- 分块模式：(.*)$", "分块模式")

    heading_match = re.search(r"(?ms)^## 覆盖章节\n\n(.*?)\n\n## 原文\n\n", text)
    if not heading_match:
        raise RuntimeError(f"无法从 {path} 解析覆盖章节")
    headings = []
    for line in heading_match.group(1).splitlines():
        if not line.startswith("- "):
            continue
        item = line[2:].strip()
        if item and item != "无明确章节标题":
            headings.append(item)

    raw_match = re.search(r"(?ms)^## 原文\n\n(.*)\Z", text)
    if not raw_match:
        raise RuntimeError(f"无法从 {path} 解析原文")
    raw_text = raw_match.group(1)

    parsed_end = start + char_count if end - start != char_count else end
    return Chunk(
        chunk_id=path.stem,
        title=title,
        start=start,
        end=parsed_end,
        text=raw_text,
        headings=headings,
        source_mode=source_mode,
    )


def load_chunks(project_dir: Path) -> list[Chunk]:
    chunk_dir = project_dir / "chunks" / "raw"
    if not chunk_dir.exists():
        return []
    return [parse_chunk_raw(path) for path in sorted(chunk_dir.glob("*.md"))]


def build_stages(chunks: list[Chunk], stage_size: int) -> list[Stage]:
    if not chunks:
        return []
    return [
        Stage(stage_id=index // stage_size + 1, chunk_ids=[chunk.chunk_id for chunk in chunks[index : index + stage_size]])
        for index in range(0, len(chunks), stage_size)
    ]


def load_source_path(project_dir: Path) -> Path | None:
    source_path_text = read_utf8(project_dir / "source" / "source-path.txt").strip()
    if not source_path_text:
        return None
    return Path(source_path_text).expanduser()


def load_stage_size(project_dir: Path, manifest: dict) -> int:
    stage_size = manifest.get("stage_size")
    if isinstance(stage_size, int) and stage_size > 0:
        return stage_size

    stage_plan = read_utf8(project_dir / "workspace" / "stage-plan.md")
    match = re.search(r"建议每\s+(\d+)\s+个 chunk", stage_plan)
    if match:
        return int(match.group(1))
    return 8


def build_project_manifest(
    project_dir: Path,
    book_name: str,
    source_txt: Path | None,
    detected_encoding: str,
    chunks: list[Chunk],
    chunk_mode: str,
    source_char_count: int,
    stage_size: int,
) -> dict:
    return {
        "book_name": book_name,
        "source_txt": str(source_txt) if source_txt else "",
        "project_dir": str(project_dir.resolve()),
        "encoding": detected_encoding,
        "chunk_mode": chunk_mode,
        "chunk_count": len(chunks),
        "source_char_count": source_char_count,
        "stage_size": stage_size,
        "outputs": {
            "book_profile": "outputs/书籍画像.md",
            "method_cards": [f"outputs/方法卡/{name}.md" for name in METHOD_CARD_NAMES],
            "case_cards_dir": "outputs/案例卡",
            "case_card_template": "workspace/案例卡模板.md",
            "case_type_reference": "workspace/推荐案例类型.md",
        },
    }


def build_progress_state(project_dir: Path, chunks: list[Chunk], stage_size: int, status: str) -> dict:
    return {
        "project_dir": str(project_dir.resolve()),
        "status": status,
        "current_stage": None,
        "stage_size": stage_size,
        "chunk_total": len(chunks),
        "processed_chunks": 0,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "finalized_at": None,
    }


def update_progress_state(project_dir: Path, patch: dict) -> dict:
    progress_path = project_dir / PROGRESS_FILE
    current = load_json_file(progress_path)
    current.update(patch)
    current["updated_at"] = now_iso()
    write_json_file(progress_path, current)
    return current


def get_method_card_defaults() -> dict[str, str]:
    return {
        "开篇规划方法卡": build_opening_method_card(),
        "大纲设计方法卡": build_outline_method_card(),
        "章节类型与写作模式方法卡": build_chapter_method_card(),
        "冲突与角色设计方法卡": build_conflict_character_method_card(),
        "读者情绪管理方法卡": build_emotion_method_card(),
        "长篇创作与文风优化方法卡": build_longform_style_method_card(),
    }


def is_modified(path: Path, default_content: str) -> bool:
    if not path.exists():
        return False
    return path.read_text(encoding="utf-8") != default_content


def collect_required_files() -> list[str]:
    files = list(REQUIRED_SUPPORT_FILES)
    files.extend(f"outputs/方法卡/{name}.md" for name in METHOD_CARD_NAMES)
    return files


def find_stage_for_chunk(stages: list[Stage], chunk_id: str) -> Stage | None:
    for stage in stages:
        if chunk_id in stage.chunk_ids:
            return stage
    return None


def ensure_project_exists(project_dir: Path) -> None:
    if not project_dir.exists():
        raise FileNotFoundError(f"找不到工程目录: {project_dir}")
    if not project_dir.is_dir():
        raise FileNotFoundError(f"工程路径不是目录: {project_dir}")


def summarize_project(project_dir: Path) -> dict:
    ensure_project_exists(project_dir)

    manifest = load_json_file(project_dir / "workspace" / "manifest.json")
    progress = load_json_file(project_dir / PROGRESS_FILE)
    chunks = load_chunks(project_dir)
    stage_size = load_stage_size(project_dir, manifest)
    stages = build_stages(chunks, stage_size)
    book_name = str(manifest.get("book_name") or project_dir.name)

    extraction_status: list[tuple[str, bool]] = []
    for chunk in chunks:
        card_path = project_dir / "extraction-cards" / f"{chunk.chunk_id}.md"
        extraction_status.append((chunk.chunk_id, is_modified(card_path, render_extraction_card_template(chunk))))

    processed_chunk_ids = [chunk_id for chunk_id, modified in extraction_status if modified]
    pending_chunk_ids = [chunk_id for chunk_id, modified in extraction_status if not modified]

    default_drafts = {
        "书籍画像草稿": build_book_profile_draft(book_name),
        "方法候选笔记": build_method_candidate_notes(),
        "案例候选笔记": build_case_candidate_notes(),
    }
    draft_status = {
        name: is_modified(project_dir / "drafts" / f"{name}.md", content)
        for name, content in default_drafts.items()
    }

    method_card_defaults = get_method_card_defaults()
    method_card_status = {
        name: is_modified(project_dir / "outputs" / "方法卡" / f"{name}.md", content)
        for name, content in method_card_defaults.items()
    }

    book_profile_touched = is_modified(project_dir / "outputs" / "书籍画像.md", build_book_profile_output())

    case_cards_dir = project_dir / "outputs" / "案例卡"
    ready_case_cards = 0
    template_only_case_cards = 0
    if case_cards_dir.exists():
        for path in sorted(case_cards_dir.glob("*.md")):
            if path.read_text(encoding="utf-8") == build_case_card_template():
                template_only_case_cards += 1
            else:
                ready_case_cards += 1

    missing_support_files = [relative for relative in collect_required_files() if not (project_dir / relative).exists()]

    current_stage = None
    if progress.get("current_stage"):
        current_stage = progress["current_stage"]
    elif pending_chunk_ids:
        stage = find_stage_for_chunk(stages, pending_chunk_ids[0])
        if stage:
            current_stage = {"stage_id": stage.stage_id, "chunk_ids": stage.chunk_ids, "chunk_range": stage.chunk_range}

    return {
        "project_dir": str(project_dir.resolve()),
        "book_name": book_name,
        "manifest": manifest,
        "progress": progress,
        "stage_size": stage_size,
        "stages": stages,
        "current_stage": current_stage,
        "chunks": chunks,
        "chunk_total": len(chunks),
        "processed_chunk_ids": processed_chunk_ids,
        "processed_chunk_count": len(processed_chunk_ids),
        "pending_chunk_ids": pending_chunk_ids,
        "pending_chunk_count": len(pending_chunk_ids),
        "draft_status": draft_status,
        "drafts_touched_count": sum(1 for touched in draft_status.values() if touched),
        "method_card_status": method_card_status,
        "method_cards_touched_count": sum(1 for touched in method_card_status.values() if touched),
        "book_profile_touched": book_profile_touched,
        "ready_case_cards": ready_case_cards,
        "template_only_case_cards": template_only_case_cards,
        "missing_support_files": missing_support_files,
    }


def recommend_next_step(summary: dict) -> str:
    project_dir = summary["project_dir"]
    if summary["missing_support_files"]:
        return f'先运行 `python3 scripts/story_analysis_pipeline.py repair "{project_dir}"`。'
    if summary["pending_chunk_count"] > 0:
        current_stage = summary.get("current_stage")
        if current_stage:
            return (
                "继续阶段提取："
                f'`python3 scripts/story_analysis_pipeline.py start-stage "{project_dir}" {current_stage["stage_id"]}`。'
            )
        return "继续按顺序处理 `extraction-cards/*.md`。"
    if summary["drafts_touched_count"] < 3:
        return "先收束并更新 3 份 drafts，再急着写最终卡片。"
    if not summary["book_profile_touched"] or summary["method_cards_touched_count"] < len(METHOD_CARD_NAMES):
        return "补齐 `outputs/书籍画像.md` 和 6 张方法卡。"
    if summary["ready_case_cards"] == 0:
        return "筛选并输出至少一张正式案例卡。"
    return f'可以运行 `python3 scripts/story_analysis_pipeline.py finalize "{project_dir}"`。'


def print_resume_summary(summary: dict) -> None:
    print("\n" + "=" * 60)
    print("拆书工程恢复摘要")
    print("=" * 60)
    print(f"工程目录: {summary['project_dir']}")
    print(f"书名: {summary['book_name']}")
    print(f"总 chunk: {summary['chunk_total']}")
    print(f"已处理提取卡: {summary['processed_chunk_count']}")
    print(f"待处理提取卡: {summary['pending_chunk_count']}")
    print(f"草稿更新: {summary['drafts_touched_count']}/3")
    print(f"方法卡更新: {summary['method_cards_touched_count']}/{len(METHOD_CARD_NAMES)}")
    print(f"书籍画像: {'已更新' if summary['book_profile_touched'] else '未更新'}")
    print(f"正式案例卡: {summary['ready_case_cards']}")

    current_stage = summary.get("current_stage")
    if current_stage:
        print(
            f"当前阶段: 阶段 {current_stage['stage_id']} "
            f"({current_stage['chunk_range']})"
        )

    if summary["missing_support_files"]:
        print("\n缺失支持文件:")
        for item in summary["missing_support_files"]:
            print(f"- {item}")

    if summary["pending_chunk_ids"]:
        preview = ", ".join(summary["pending_chunk_ids"][:8])
        print(f"\n待处理 chunk: {preview}")
        if summary["pending_chunk_count"] > 8:
            print(f"- 其余 {summary['pending_chunk_count'] - 8} 个待处理")

    untouched_methods = [name for name, touched in summary["method_card_status"].items() if not touched]
    if untouched_methods:
        print("\n仍是模板的输出:")
        if not summary["book_profile_touched"]:
            print("- outputs/书籍画像.md")
        for name in untouched_methods:
            print(f"- outputs/方法卡/{name}.md")

    if summary["template_only_case_cards"]:
        print(f"\n模板未实填案例卡: {summary['template_only_case_cards']}")

    print("\n下一步建议:")
    print(f"- {recommend_next_step(summary)}")


def build_check_report(project_dir: Path, finalize_mode: bool) -> dict:
    summary = summarize_project(project_dir)
    blocking_issues: list[str] = []
    warnings: list[str] = []

    if summary["chunk_total"] == 0:
        blocking_issues.append("缺少 `chunks/raw/*.md`，无法继续分析。")

    if summary["missing_support_files"]:
        blocking_issues.append("存在缺失的支持文件，先运行 `repair` 修复工程。")

    if summary["pending_chunk_count"] > 0:
        message = f"仍有 {summary['pending_chunk_count']} 个提取卡未完成。"
        if finalize_mode:
            blocking_issues.append(message)
        else:
            warnings.append(message)

    if summary["processed_chunk_count"] > 0 and summary["drafts_touched_count"] == 0:
        warnings.append("已有提取卡被填写，但 3 份 drafts 仍保持模板状态。")

    if not summary["book_profile_touched"]:
        message = "`outputs/书籍画像.md` 仍是模板状态。"
        if finalize_mode:
            blocking_issues.append(message)
        else:
            warnings.append(message)

    untouched_methods = [name for name, touched in summary["method_card_status"].items() if not touched]
    if untouched_methods:
        message = f"仍有 {len(untouched_methods)} 张方法卡保持模板状态。"
        if finalize_mode:
            blocking_issues.append(message)
        else:
            warnings.append(message)

    evidence_gaps = []
    for name in METHOD_CARD_NAMES:
        method_path = project_dir / "outputs" / "方法卡" / f"{name}.md"
        if re.search(r"(?m)^- 关键 chunk：\s*$", read_utf8(method_path)):
            evidence_gaps.append(name)
    if evidence_gaps:
        message = "以下方法卡还没有填入证据锚点：" + "、".join(evidence_gaps)
        if finalize_mode:
            blocking_issues.append(message)
        else:
            warnings.append(message)

    if summary["ready_case_cards"] == 0:
        message = "还没有正式案例卡。"
        if finalize_mode:
            blocking_issues.append(message)
        else:
            warnings.append(message)

    if summary["template_only_case_cards"] > 0:
        warnings.append(f"有 {summary['template_only_case_cards']} 张案例卡仍是原始模板。")

    return {
        "summary": summary,
        "blocking_issues": blocking_issues,
        "warnings": warnings,
    }


def print_check_summary(report: dict, finalize_mode: bool) -> None:
    summary = report["summary"]
    print("\n" + "=" * 60)
    print("拆书工程检查摘要")
    print("=" * 60)
    print(f"- 总 chunk: {summary['chunk_total']}")
    print(f"- 已处理提取卡: {summary['processed_chunk_count']}")
    print(f"- 待处理提取卡: {summary['pending_chunk_count']}")
    print(f"- 草稿更新: {summary['drafts_touched_count']}/3")
    print(f"- 方法卡更新: {summary['method_cards_touched_count']}/{len(METHOD_CARD_NAMES)}")
    print(f"- 书籍画像: {'已更新' if summary['book_profile_touched'] else '未更新'}")
    print(f"- 正式案例卡: {summary['ready_case_cards']}")

    if report["blocking_issues"]:
        title = "收束阻塞项" if finalize_mode else "阻塞项"
        print(f"\n{title}:")
        for item in report["blocking_issues"]:
            print(f"- {item}")

    if report["warnings"]:
        print("\n警告:")
        for item in report["warnings"]:
            print(f"- {item}")


def sync_support_files(project_dir: Path, force: bool) -> list[str]:
    ensure_project_exists(project_dir)
    chunks = load_chunks(project_dir)
    if not chunks:
        raise RuntimeError("缺少 `chunks/raw/*.md`，无法重建工程支撑文件。")

    manifest = load_json_file(project_dir / "workspace" / "manifest.json")
    book_name = str(manifest.get("book_name") or project_dir.name)
    source_txt = load_source_path(project_dir)
    detected_encoding = str(manifest.get("encoding") or "unknown")
    chunk_mode = str(manifest.get("chunk_mode") or chunks[0].source_mode)
    stage_size = load_stage_size(project_dir, manifest)
    source_char_count = int(manifest.get("source_char_count") or max(chunk.end for chunk in chunks))

    touched: list[str] = []

    def sync_file(relative_path: str, content: str) -> None:
        path = project_dir / relative_path
        existed = path.exists()
        write_text(path, content, force)
        if force or not existed:
            touched.append(relative_path)

    for relative in (
        "source",
        "workspace",
        "chunks/raw",
        "extraction-cards",
        "drafts",
        "outputs/方法卡",
        "outputs/案例卡",
    ):
        ensure_dir(project_dir / relative)

    new_manifest = build_project_manifest(
        project_dir=project_dir,
        book_name=book_name,
        source_txt=source_txt,
        detected_encoding=detected_encoding,
        chunks=chunks,
        chunk_mode=chunk_mode,
        source_char_count=source_char_count,
        stage_size=stage_size,
    )

    manifest_path = project_dir / "workspace" / "manifest.json"
    manifest_existed = manifest_path.exists()
    write_json(manifest_path, new_manifest, force)
    if force or not manifest_existed:
        touched.append("workspace/manifest.json")

    if source_txt:
        sync_file("source/source-path.txt", f"{source_txt}\n")

    sync_file("workspace/chunk-index.md", render_chunk_index(chunks))
    sync_file("workspace/stage-plan.md", render_stage_plan(chunks, stage_size))
    sync_file("workspace/use-guide.md", render_use_guide(book_name, len(chunks)))
    sync_file("workspace/案例卡模板.md", build_case_card_template())
    sync_file("workspace/推荐案例类型.md", build_case_type_reference())

    sync_file("drafts/书籍画像草稿.md", build_book_profile_draft(book_name))
    sync_file("drafts/方法候选笔记.md", build_method_candidate_notes())
    sync_file("drafts/案例候选笔记.md", build_case_candidate_notes())

    sync_file("outputs/书籍画像.md", build_book_profile_output())
    sync_file("outputs/方法卡/开篇规划方法卡.md", build_opening_method_card())
    sync_file("outputs/方法卡/大纲设计方法卡.md", build_outline_method_card())
    sync_file("outputs/方法卡/章节类型与写作模式方法卡.md", build_chapter_method_card())
    sync_file("outputs/方法卡/冲突与角色设计方法卡.md", build_conflict_character_method_card())
    sync_file("outputs/方法卡/读者情绪管理方法卡.md", build_emotion_method_card())
    sync_file("outputs/方法卡/长篇创作与文风优化方法卡.md", build_longform_style_method_card())

    for chunk in chunks:
        sync_file(f"extraction-cards/{chunk.chunk_id}.md", render_extraction_card_template(chunk))

    progress_path = project_dir / PROGRESS_FILE
    progress = load_json_file(progress_path)
    if not progress:
        progress = build_progress_state(project_dir, chunks, stage_size, "repaired")
        write_json_file(progress_path, progress)
        touched.append(str(PROGRESS_FILE))
    else:
        update_progress_state(
            project_dir,
            {
                "status": "repaired",
                "last_repaired_at": now_iso(),
                "stage_size": stage_size,
                "chunk_total": len(chunks),
            },
        )
        touched.append(str(PROGRESS_FILE))

    return touched


def handle_init(args: argparse.Namespace) -> int:
    source_txt = Path(args.source_txt).expanduser().resolve()
    if not source_txt.exists():
        raise FileNotFoundError(f"找不到原始文件: {source_txt}")
    if not source_txt.is_file():
        raise FileNotFoundError(f"输入路径不是文件: {source_txt}")
    if args.hard_max_chars < args.target_chars:
        raise ValueError("--hard-max-chars 必须大于或等于 --target-chars")
    if args.stage_size <= 0:
        raise ValueError("--stage-size 必须大于 0")

    text, detected_encoding = read_source_text(source_txt, args.encoding)
    text = normalize_text(text)
    lines = build_lines(text)
    sections, mode = detect_sections(lines, args.min_headings)
    chunks = build_chunks(sections, mode, args.target_chars, args.hard_max_chars)
    if not chunks:
        raise RuntimeError("分块结果为空，请检查输入文本")

    book_name = safe_book_name(args.book_name or source_txt.stem)
    story_root = Path(args.story_root).expanduser()
    project_dir = initialize_project(
        source_txt=source_txt,
        story_root=story_root,
        book_name=book_name,
        detected_encoding=detected_encoding,
        mode=mode,
        chunks=chunks,
        raw_text=text,
        stage_size=args.stage_size,
        copy_source=args.copy_source,
        force=args.force,
    )
    progress = build_progress_state(project_dir, chunks, args.stage_size, "initialized")
    write_json_file(project_dir / PROGRESS_FILE, progress)

    print("\n" + "=" * 60)
    print("拆书工程已初始化")
    print("=" * 60)
    print(f"工程目录: {project_dir.resolve()}")
    print(f"检测编码: {detected_encoding}")
    print(f"分块模式: {mode}")
    print(f"总 chunk: {len(chunks)}")
    print(f"阶段大小: {args.stage_size}")
    print("\n下一步建议:")
    print(f'- 先运行 `python3 scripts/story_analysis_pipeline.py resume "{project_dir.resolve()}"`')
    print(f'- 再按阶段执行 `start-stage` 并填写 `extraction-cards/*.md`')
    return 0


def handle_resume(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    print_resume_summary(summarize_project(project_dir))
    return 0


def handle_start_stage(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    summary = summarize_project(project_dir)
    stages = summary["stages"]
    if not stages:
        raise RuntimeError("工程里没有可用阶段，请先检查 `chunks/raw/`。")

    stage_map = {stage.stage_id: stage for stage in stages}
    if args.stage_num not in stage_map:
        raise ValueError(f"无效阶段号: {args.stage_num}")
    stage = stage_map[args.stage_num]

    update_progress_state(
        project_dir,
        {
            "status": "in_progress",
            "current_stage": {
                "stage_id": stage.stage_id,
                "chunk_ids": stage.chunk_ids,
                "chunk_range": stage.chunk_range,
                "started_at": now_iso(),
                "note": args.note or "",
            },
        },
    )

    print("\n" + "=" * 60)
    print("阶段已标记为进行中")
    print("=" * 60)
    print(f"工程目录: {project_dir}")
    print(f"阶段: {stage.stage_id}")
    print(f"Chunk 范围: {stage.chunk_range}")
    print(f"处理顺序: {', '.join(stage.chunk_ids)}")
    if args.note:
        print(f"备注: {args.note}")
    return 0


def handle_check(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    report = build_check_report(project_dir, finalize_mode=False)
    print_check_summary(report, finalize_mode=False)
    return 1 if report["blocking_issues"] else 0


def handle_finalize(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    report = build_check_report(project_dir, finalize_mode=True)
    print_check_summary(report, finalize_mode=True)

    if report["blocking_issues"] and not args.force:
        print("\n未完成收束。若你确认要忽略阻塞项，重新运行并加 `--force`。")
        return 1

    summary = report["summary"]
    update_progress_state(
        project_dir,
        {
            "status": "finalized",
            "current_stage": None,
            "finalized_at": now_iso(),
            "final_note": args.note or "",
            "processed_chunks": summary["processed_chunk_count"],
            "ready_case_cards": summary["ready_case_cards"],
        },
    )

    print("\n收束状态已写入 `workspace/analysis-progress.json`。")
    return 0


def handle_repair(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_path).expanduser().resolve()
    touched = sync_support_files(project_dir, force=args.force)
    print("\n" + "=" * 60)
    print("工程支撑文件已同步")
    print("=" * 60)
    if touched:
        for item in touched:
            print(f"- {item}")
    else:
        print("- 没有需要修复或覆盖的文件")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="君黎AI拆书统一入口")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="初始化新的拆书工程")
    init_parser.add_argument("source_txt", help="原始小说 txt 的绝对路径")
    init_parser.add_argument("--story-root", default="story", help="输出根目录，默认 ./story")
    init_parser.add_argument("--book-name", help="小说名，默认从文件名推断")
    init_parser.add_argument("--encoding", default="auto", help="文本编码，默认 auto")
    init_parser.add_argument("--target-chars", type=int, default=12000, help="目标块大小，默认 12000")
    init_parser.add_argument("--hard-max-chars", type=int, default=18000, help="单块硬上限，默认 18000")
    init_parser.add_argument("--min-headings", type=int, default=3, help="启用章节模式所需最少标题数")
    init_parser.add_argument("--stage-size", type=int, default=8, help="每多少块做一次阶段收束，默认 8")
    init_parser.add_argument("--copy-source", action="store_true", help="复制原始 txt 到工程目录")
    init_parser.add_argument("--force", action="store_true", help="若工程已存在则覆盖同名引导文件；不会清理旧文件")
    init_parser.set_defaults(func=handle_init)

    resume_parser = subparsers.add_parser("resume", help="恢复现有拆书工程摘要")
    resume_parser.add_argument("project_path", help="拆书工程根目录")
    resume_parser.set_defaults(func=handle_resume)

    start_parser = subparsers.add_parser("start-stage", help="标记某个阶段为进行中")
    start_parser.add_argument("project_path", help="拆书工程根目录")
    start_parser.add_argument("stage_num", type=int, help="阶段号")
    start_parser.add_argument("--note", help="阶段备注")
    start_parser.set_defaults(func=handle_start_stage)

    check_parser = subparsers.add_parser("check", help="检查拆书工程当前状态")
    check_parser.add_argument("project_path", help="拆书工程根目录")
    check_parser.set_defaults(func=handle_check)

    finalize_parser = subparsers.add_parser("finalize", help="写入收束状态并做最终检查")
    finalize_parser.add_argument("project_path", help="拆书工程根目录")
    finalize_parser.add_argument("--note", help="收束备注")
    finalize_parser.add_argument("--force", action="store_true", help="忽略阻塞项，强制写入 finalized 状态")
    finalize_parser.set_defaults(func=handle_finalize)

    repair_parser = subparsers.add_parser("repair", help="修复缺失的工程支撑文件")
    repair_parser.add_argument("project_path", help="拆书工程根目录")
    repair_parser.add_argument("--force", action="store_true", help="覆盖同名支撑文件")
    repair_parser.set_defaults(func=handle_repair)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))
