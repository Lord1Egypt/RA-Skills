#!/usr/bin/env python3
"""初始化小说参考资产提炼工程。"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATES_ROOT = SKILL_ROOT / "references" / "templates"


COMMON_ENCODINGS = (
    "utf-8",
    "utf-8-sig",
    "gb18030",
    "gbk",
    "big5",
)

HEADING_PATTERNS = (
    re.compile(r"^\s*第[0-9零〇一二两三四五六七八九十百千万]+[章回节卷部篇幕集].*$"),
    re.compile(r"^\s*(chapter|chap\.?)\s+\d+.*$", re.IGNORECASE),
    re.compile(r"^\s*(prologue|epilogue|番外|序章|楔子|尾声|后记).*$", re.IGNORECASE),
)

METHOD_CARD_NAMES = (
    "开篇规划方法卡",
    "大纲设计方法卡",
    "章节类型与写作模式方法卡",
    "冲突与角色设计方法卡",
    "读者情绪管理方法卡",
    "长篇创作与文风优化方法卡",
)

@dataclass
class LineInfo:
    text: str
    start: int
    end: int


@dataclass
class Section:
    title: str
    start: int
    end: int
    text: str
    headings: list[str]

    @property
    def char_count(self) -> int:
        return self.end - self.start


@dataclass
class Chunk:
    chunk_id: str
    title: str
    start: int
    end: int
    text: str
    headings: list[str]
    source_mode: str

    @property
    def char_count(self) -> int:
        return self.end - self.start


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化小说参考资产提炼工程")
    parser.add_argument("source_txt", help="原始小说 txt 的绝对路径")
    parser.add_argument("--story-root", default="story", help="输出根目录，默认 ./story")
    parser.add_argument("--book-name", help="小说名，默认从文件名推断")
    parser.add_argument("--encoding", default="auto", help="文本编码，默认 auto")
    parser.add_argument("--target-chars", type=int, default=12000, help="目标块大小，默认 12000")
    parser.add_argument("--hard-max-chars", type=int, default=18000, help="单块硬上限，默认 18000")
    parser.add_argument("--min-headings", type=int, default=3, help="启用章节模式所需最少标题数")
    parser.add_argument("--stage-size", type=int, default=8, help="每多少块做一次阶段收束，默认 8")
    parser.add_argument("--copy-source", action="store_true", help="复制原始 txt 到工程目录")
    parser.add_argument("--force", action="store_true", help="若工程已存在则覆盖同名引导文件；不会清理旧文件")
    return parser.parse_args()


def read_text(path: Path, encoding: str) -> tuple[str, str]:
    if encoding != "auto":
        return path.read_text(encoding=encoding), encoding

    last_error: Exception | None = None
    for candidate in COMMON_ENCODINGS:
        try:
            return path.read_text(encoding=candidate), candidate
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    raise RuntimeError("无法识别文本编码")


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", "  ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def safe_book_name(raw_name: str) -> str:
    name = raw_name.strip().replace("/", "-").replace("\\", "-")
    return name or "未命名小说"


def build_lines(text: str) -> list[LineInfo]:
    lines: list[LineInfo] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        start = offset
        end = offset + len(raw_line)
        lines.append(LineInfo(text=raw_line, start=start, end=end))
        offset = end
    if not lines:
        lines.append(LineInfo(text="", start=0, end=0))
    return lines


def is_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False
    return any(pattern.match(stripped) for pattern in HEADING_PATTERNS)


def detect_sections(lines: list[LineInfo], min_headings: int) -> tuple[list[Section], str]:
    heading_indexes = [index for index, line in enumerate(lines) if is_heading(line.text)]
    if len(heading_indexes) < min_headings:
        full_text = "".join(line.text for line in lines)
        return [Section(title="全文", start=0, end=len(full_text), text=full_text, headings=[])], "length"

    sections: list[Section] = []
    if heading_indexes[0] > 0:
        preface_text = "".join(line.text for line in lines[: heading_indexes[0]])
        if preface_text.strip():
            sections.append(
                Section(
                    title="开篇",
                    start=lines[0].start,
                    end=lines[heading_indexes[0]].start,
                    text=preface_text,
                    headings=["开篇"],
                )
            )

    for position, start_index in enumerate(heading_indexes):
        end_index = heading_indexes[position + 1] if position + 1 < len(heading_indexes) else len(lines)
        title = lines[start_index].text.strip()
        text = "".join(line.text for line in lines[start_index:end_index])
        sections.append(
            Section(
                title=title,
                start=lines[start_index].start,
                end=lines[end_index - 1].end if end_index > start_index else lines[start_index].end,
                text=text,
                headings=[title],
            )
        )
    return sections, "chapter"


def split_section_by_length(section: Section, target_chars: int, hard_max_chars: int) -> list[Section]:
    if section.char_count <= hard_max_chars:
        return [section]

    lines = build_lines(section.text)
    pieces: list[Section] = []
    start_idx = 0
    piece_index = 1

    while start_idx < len(lines):
        current_chars = 0
        cut_idx = start_idx
        last_blank_idx: int | None = None

        while cut_idx < len(lines):
            current_chars += len(lines[cut_idx].text)
            if not lines[cut_idx].text.strip():
                last_blank_idx = cut_idx + 1
            next_idx = cut_idx + 1
            if current_chars >= target_chars and last_blank_idx is not None and last_blank_idx > start_idx:
                cut_idx = last_blank_idx
                break
            if current_chars >= hard_max_chars:
                cut_idx = last_blank_idx if last_blank_idx is not None and last_blank_idx > start_idx else next_idx
                break
            cut_idx = next_idx

        if cut_idx <= start_idx:
            cut_idx = min(start_idx + 1, len(lines))

        part_lines = lines[start_idx:cut_idx]
        text = "".join(line.text for line in part_lines)
        start = section.start + part_lines[0].start
        end = section.start + part_lines[-1].end
        pieces.append(
            Section(
                title=f"{section.title} / part {piece_index}",
                start=start,
                end=end,
                text=text,
                headings=section.headings[:],
            )
        )
        piece_index += 1
        start_idx = cut_idx

    return pieces


def build_chunks(sections: list[Section], mode: str, target_chars: int, hard_max_chars: int) -> list[Chunk]:
    prepared_sections: list[Section] = []
    for section in sections:
        prepared_sections.extend(split_section_by_length(section, target_chars, hard_max_chars))

    chunks: list[Chunk] = []
    bucket: list[Section] = []
    bucket_chars = 0

    def flush_bucket() -> None:
        nonlocal bucket, bucket_chars
        if not bucket:
            return
        chunk_number = len(chunks) + 1
        start = bucket[0].start
        end = bucket[-1].end
        text = "".join(section.text for section in bucket)
        headings: list[str] = []
        for section in bucket:
            headings.extend(section.headings)
        title = " / ".join(headings[:3]) if headings else f"chunk-{chunk_number:04d}"
        if len(headings) > 3:
            title = f"{title} 等 {len(headings)} 段"
        chunks.append(
            Chunk(
                chunk_id=f"{chunk_number:04d}",
                title=title,
                start=start,
                end=end,
                text=text,
                headings=headings,
                source_mode=mode,
            )
        )
        bucket = []
        bucket_chars = 0

    for section in prepared_sections:
        if bucket and bucket_chars + section.char_count > target_chars:
            flush_bucket()
        bucket.append(section)
        bucket_chars += section.char_count
        if bucket_chars >= hard_max_chars:
            flush_bucket()

    flush_bucket()
    return chunks


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: object, force: bool) -> None:
    if path.exists() and not force:
        return
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_reference_template(*relative_parts: str) -> str:
    template_path = TEMPLATES_ROOT.joinpath(*relative_parts)
    return template_path.read_text(encoding="utf-8")


def ensure_project_can_initialize(project_dir: Path, force: bool) -> None:
    if not project_dir.exists():
        return
    if force:
        return
    if not project_dir.is_dir():
        raise FileExistsError(f"目标路径已存在且不是目录: {project_dir.resolve()}")
    if not any(project_dir.iterdir()):
        return

    raise FileExistsError(
        "工程已存在："
        f"{project_dir.resolve()}\n"
        "bootstrap 默认只用于初始化新工程，不会静默合并或刷新已有文件。\n"
        "如果你只是继续分析，请直接在现有工程里工作；"
        "如果你明确要覆盖同名引导文件，请重新运行并加上 --force；"
        "如果你要彻底重建工程，请先删除旧目录或换一个 --story-root。"
    )


def render_chunk_raw(source_txt: Path, chunk: Chunk) -> str:
    headings = "\n".join(f"- {item}" for item in chunk.headings) if chunk.headings else "- 无明确章节标题"
    return (
        f"# Chunk {chunk.chunk_id}\n\n"
        f"- 标题：{chunk.title}\n"
        f"- 来源文件：{source_txt}\n"
        f"- 起始字符：{chunk.start}\n"
        f"- 结束字符：{chunk.end}\n"
        f"- 字符数：{chunk.char_count}\n"
        f"- 分块模式：{chunk.source_mode}\n\n"
        "## 覆盖章节\n\n"
        f"{headings}\n\n"
        "## 原文\n\n"
        f"{chunk.text.strip()}\n"
    )


def render_extraction_card_template(chunk: Chunk) -> str:
    headings = "\n".join(f"- {item}" for item in chunk.headings) if chunk.headings else "- 无明确章节标题"
    return (
        f"# 资产提取卡 {chunk.chunk_id}\n\n"
        f"- 标题：{chunk.title}\n"
        f"- 字符数：{chunk.char_count}\n"
        f"- 对应原文：../chunks/raw/{chunk.chunk_id}.md\n\n"
        "## 覆盖章节\n\n"
        f"{headings}\n\n"
        "## 这一块的主要叙事功能\n\n"
        "- 先写主功能，再补次功能。可参考：开篇立人 / 开篇钩子 / 催化剂 / 首次升级 / 推进 / 过渡 / 章末钩子 / 情绪补偿 / 代价显化 / 卷末爆点 / 地图切换 / 规则更新 / 对手更换 / 目标调整 / 文风节奏片段 / 其他。\n\n"
        "## 关键内容\n\n"
        "- 只写 3-5 条关键动作或变化，不写长剧情。\n\n"
        "## 方法候选\n\n"
        "### 支撑哪张方法卡\n\n"
        "- 开篇规划 / 大纲设计 / 章节类型与写作模式 / 冲突与角色设计 / 读者情绪管理 / 长篇创作与文风优化\n\n"
        "### 可提炼的写法动作\n\n"
        "- 这段到底体现了什么可迁移的写法。\n\n"
        "### 为什么有效\n\n"
        "- 这段为什么对读者有效，或者为什么对结构有效。\n\n"
        "### 可量化参数\n\n"
        "- 尽量补时机、频率、间隔、占比、篇幅、章节位置等可量化信息。\n\n"
        "## 案例候选\n\n"
        "### 候选类型或标签\n\n"
        "- 可从推荐类型里选，也可自定义。优先写有明确写法价值的标签，例如：开篇立人 / 开篇钩子 / 催化剂 / 首次升级 / 重要选择 / 推进章 / 过渡章 / 章末钩子 / 情绪补偿 / 代价显化 / 关系冲突 / 卷末爆点 / 地图切换 / 规则更新 / 目标调整 / 文风节奏片段。\n\n"
        "### 典型程度\n\n"
        "- 强 / 中 / 弱\n\n"
        "### 是否需要跨 chunk 合并\n\n"
        "- 如果单块不完整，就写明还要合并哪些 chunk。\n\n"
        "### 值不值得正式建卡\n\n"
        "- 写“立即建卡 / 继续观察 / 只留候选”，不要强凑数量。\n\n"
        "## 书籍画像信号\n\n"
        "- 这块补充了哪些题材、风格、节奏、钩子、情绪或扩长信号。\n\n"
        "## 关键证据\n\n"
        "- 摘 1-3 个最关键的证据点，不要大段抄原文。\n\n"
        "## 可学 / 不可照搬\n\n"
        "- 哪些可以学成方法，哪些只是具体桥段、设定或题材红利。\n\n"
        "## 写回草稿\n\n"
        "### 书籍画像草稿\n\n"
        "- 要写回什么。\n\n"
        "### 方法候选笔记\n\n"
        "- 要写回什么。\n\n"
        "### 案例候选笔记\n\n"
        "- 要写回什么。\n"
    )


def render_chunk_index(chunks: Iterable[Chunk]) -> str:
    rows = [
        "| Chunk | 标题 | 字符数 | 起始字符 | 结束字符 | 模式 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for chunk in chunks:
        rows.append(
            f"| {chunk.chunk_id} | {chunk.title} | {chunk.char_count} | "
            f"{chunk.start} | {chunk.end} | {chunk.source_mode} |"
        )
    return "# Chunk Index\n\n" + "\n".join(rows) + "\n"


def render_stage_plan(chunks: list[Chunk], stage_size: int) -> str:
    lines = ["# 阶段计划", "", f"- 建议每 {stage_size} 个 chunk 做一次资产收束。", ""]
    for index in range(0, len(chunks), stage_size):
        batch = chunks[index : index + stage_size]
        batch_id = index // stage_size + 1
        lines.append(f"## 阶段 {batch_id}")
        lines.append("")
        lines.append(f"- Chunk 范围：{batch[0].chunk_id} - {batch[-1].chunk_id}")
        lines.append(f"- 处理顺序：{', '.join(chunk.chunk_id for chunk in batch)}")
        lines.append("- 阶段结束后，更新 3 份草稿：`drafts/书籍画像草稿.md`、`drafts/方法候选笔记.md`、`drafts/案例候选笔记.md`。")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_use_guide(book_name: str, chunk_count: int) -> str:
    return f"""# 使用说明

## 目标

把《{book_name}》拆成一个创作参考包，而不是剧情总结。

固定产出只有：

- 1 份书籍画像
- 6 张方法卡
- 若干张案例卡

## 正常使用顺序

1. 先读 `workspace/chunk-index.md` 和 `workspace/stage-plan.md`
2. 逐块阅读 `chunks/raw/*.md`
3. 每块填写一张 `extraction-cards/*.md`
4. 每个阶段更新 3 份草稿：
   `drafts/书籍画像草稿.md`
   `drafts/方法候选笔记.md`
   `drafts/案例候选笔记.md`
5. 全书读完后，再整理 `outputs/` 里的 `1 + 6 + N`
6. 案例卡只要值得建就记录，不设上限；命名建议用 `NN-案例类型-核心动作.md`

## 处理总数

- 分块数量：{chunk_count}

## 硬约束

- 不把剧情复述当主产品
- 不把文学评论当主产品
- 每个 chunk 都要先判断它支撑哪张方法卡、能不能进某类案例卡
- 案例卡不需要凑数，只保留真的值得参考的片段
- 最终一切都服务创作参考，不服务赏析完整性
"""


def build_book_profile_draft(book_name: str) -> str:
    return f"""# 书籍画像草稿

## 基本定位
- 书名：{book_name}
- 题材：
- 子题材：
- 面向读者：
- 篇幅体量：

## 风格信号
- 节奏快慢：
- 钩子密度：
- 爽点强度：
- 压抑强度：
- 对话密度：
- 动作描写占比：
- 心理描写占比：

## 结构与扩长
- 开篇路数：
- 首次升级时机：
- 常见章节类型：
- 长篇扩展方式：

## 最值得参考的模块
- 开篇规划：
- 大纲设计：
- 章节写法：
- 冲突与角色：
- 情绪管理：
- 长篇与文风：

## 值得参考的方向
- 最值得参考什么：
- 最依赖题材的地方：
- 最不能乱学的地方：
"""


def build_method_candidate_notes() -> str:
    sections = []
    for name in METHOD_CARD_NAMES:
        sections.append(
            f"## {name}\n\n"
            "- chunk 证据：\n"
            "- 这本书怎么做：\n"
            "- 为什么有效：\n"
            "- 可复用写法：\n"
            "- 参数或频率：\n"
            "- 适用边界：\n"
            "- 不可照搬：\n"
        )
    return "# 方法候选笔记\n\n" + "\n".join(sections)


def build_case_candidate_notes() -> str:
    return (
        "# 案例候选笔记\n\n"
        "## 使用规则\n"
        "- 案例卡不设上限，只要“值得检索、值得复用、值得对照”就记录。\n"
        "- 一个案例可以同时打多个标签，但要有主标签。\n"
        "- 优先收录能稳定说明写法价值的案例，而不是只因为桥段精彩。\n"
        "- 命名建议：`NN-案例类型-核心动作.md`\n\n"
        f"{build_case_type_reference().strip()}\n\n"
        "## 候选模板\n\n"
        "### 案例候选 01\n"
        "- 候选 chunk：\n"
        "- 主标签：\n"
        "- 次标签：\n"
        "- 对应方法卡：\n"
        "- 典型程度：强 / 中 / 弱\n"
        "- 最适合参考什么场景：\n"
        "- 为什么值得建正式案例卡：\n"
        "- 是否需要跨 chunk 合并：\n"
        "- 关键证据：\n"
        "- 暂时不建卡的原因：\n"
    )


def build_book_profile_output() -> str:
    return load_reference_template("书籍画像模板.md")


def build_opening_method_card() -> str:
    return load_reference_template("方法卡", "开篇规划方法卡模板.md")


def build_outline_method_card() -> str:
    return load_reference_template("方法卡", "大纲设计方法卡模板.md")


def build_chapter_method_card() -> str:
    return load_reference_template("方法卡", "章节类型与写作模式方法卡模板.md")


def build_conflict_character_method_card() -> str:
    return load_reference_template("方法卡", "冲突与角色设计方法卡模板.md")


def build_emotion_method_card() -> str:
    return load_reference_template("方法卡", "读者情绪管理方法卡模板.md")


def build_longform_style_method_card() -> str:
    return load_reference_template("方法卡", "长篇创作与文风优化方法卡模板.md")


def build_case_card_template() -> str:
    return load_reference_template("案例卡", "案例卡模板.md")


def build_case_type_reference() -> str:
    return load_reference_template("案例卡", "推荐案例类型.md")


def initialize_project(
    source_txt: Path,
    story_root: Path,
    book_name: str,
    detected_encoding: str,
    mode: str,
    chunks: list[Chunk],
    raw_text: str,
    stage_size: int,
    copy_source: bool,
    force: bool,
) -> Path:
    project_dir = story_root / book_name
    ensure_project_can_initialize(project_dir, force)
    ensure_dir(project_dir)

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

    if copy_source:
        destination = project_dir / "source" / "original.txt"
        if force or not destination.exists():
            shutil.copyfile(source_txt, destination)

    manifest = {
        "book_name": book_name,
        "source_txt": str(source_txt),
        "project_dir": str(project_dir.resolve()),
        "encoding": detected_encoding,
        "chunk_mode": mode,
        "chunk_count": len(chunks),
        "source_char_count": len(raw_text),
        "stage_size": stage_size,
        "outputs": {
            "book_profile": "outputs/书籍画像.md",
            "method_cards": [f"outputs/方法卡/{name}.md" for name in METHOD_CARD_NAMES],
            "case_cards_dir": "outputs/案例卡",
            "case_card_template": "workspace/案例卡模板.md",
            "case_type_reference": "workspace/推荐案例类型.md",
        },
    }

    write_json(project_dir / "workspace" / "manifest.json", manifest, force)
    write_text(project_dir / "workspace" / "chunk-index.md", render_chunk_index(chunks), force)
    write_text(project_dir / "workspace" / "stage-plan.md", render_stage_plan(chunks, stage_size), force)
    write_text(project_dir / "workspace" / "use-guide.md", render_use_guide(book_name, len(chunks)), force)
    write_text(project_dir / "workspace" / "案例卡模板.md", build_case_card_template(), force)
    write_text(project_dir / "workspace" / "推荐案例类型.md", build_case_type_reference(), force)
    write_text(project_dir / "source" / "source-path.txt", f"{source_txt}\n", force)

    write_text(project_dir / "drafts" / "书籍画像草稿.md", build_book_profile_draft(book_name), force)
    write_text(project_dir / "drafts" / "方法候选笔记.md", build_method_candidate_notes(), force)
    write_text(project_dir / "drafts" / "案例候选笔记.md", build_case_candidate_notes(), force)

    write_text(project_dir / "outputs" / "书籍画像.md", build_book_profile_output(), force)
    write_text(project_dir / "outputs" / "方法卡" / "开篇规划方法卡.md", build_opening_method_card(), force)
    write_text(project_dir / "outputs" / "方法卡" / "大纲设计方法卡.md", build_outline_method_card(), force)
    write_text(project_dir / "outputs" / "方法卡" / "章节类型与写作模式方法卡.md", build_chapter_method_card(), force)
    write_text(project_dir / "outputs" / "方法卡" / "冲突与角色设计方法卡.md", build_conflict_character_method_card(), force)
    write_text(project_dir / "outputs" / "方法卡" / "读者情绪管理方法卡.md", build_emotion_method_card(), force)
    write_text(project_dir / "outputs" / "方法卡" / "长篇创作与文风优化方法卡.md", build_longform_style_method_card(), force)

    for chunk in chunks:
        write_text(project_dir / "chunks" / "raw" / f"{chunk.chunk_id}.md", render_chunk_raw(source_txt, chunk), force)
        write_text(project_dir / "extraction-cards" / f"{chunk.chunk_id}.md", render_extraction_card_template(chunk), force)

    return project_dir


def main() -> None:
    args = parse_args()
    source_txt = Path(args.source_txt).expanduser().resolve()
    if not source_txt.exists():
        raise FileNotFoundError(f"找不到原始文件: {source_txt}")
    if not source_txt.is_file():
        raise FileNotFoundError(f"输入路径不是文件: {source_txt}")
    if args.hard_max_chars < args.target_chars:
        raise ValueError("--hard-max-chars 必须大于或等于 --target-chars")
    if args.stage_size <= 0:
        raise ValueError("--stage-size 必须大于 0")

    text, detected_encoding = read_text(source_txt, args.encoding)
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

    print(f"工程已创建：{project_dir.resolve()}")
    print(f"检测编码：{detected_encoding}")
    print(f"分块模式：{mode}")
    print(f"分块数量：{len(chunks)}")
    print(f"阶段大小：{args.stage_size}")

if __name__ == "__main__":
    try:
        main()
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))
