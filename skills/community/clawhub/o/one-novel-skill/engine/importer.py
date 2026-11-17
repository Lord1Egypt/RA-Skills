#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Importer — 增强版（融合 story-import 的完整导入管线）

融合源:
  - oh-story/story-import (章节切分自动识别、残章检测、按篇幅分流、拆文库→对标引用)
  - chinese-novelist-skill (中断续写检测)
功能: 世界观→项目 / 已有作品→项目 / 纯文本导入（自动切分+残章+篇幅判定）
"""

import json, os, logging, re
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

_log = logging.getLogger("importer")


# 章节分隔符模式
CHAPTER_SPLIT_PATTERNS = [
    re.compile(r'第[零一二三四五六七八九十百千万\d]+[章节回]'),
    re.compile(r'Chapter\s+\d+', re.IGNORECASE),
    re.compile(r'^\d+\.\s+', re.MULTILINE),
]

# 短篇判定阈值
SHORT_NOVEL_MAX_CHAPTERS = 20
SHORT_NOVEL_MAX_WORDS = 60000


class ImportResult:
    """导入结果"""
    def __init__(self):
        self.success = False
        self.chapters_imported = 0
        self.title = ""
        self.book_dir = ""
        self.length_type = ""          # "long" / "short"
        self.last_chapter_status = ""  # "complete" / "residual"
        self.warnings = []
        self.errors = []

    def to_dict(self) -> dict:
        return {
            "success": self.success, "chapters_imported": self.chapters_imported,
            "title": self.title, "book_dir": self.book_dir, "length_type": self.length_type,
            "last_chapter_status": self.last_chapter_status,
            "warnings": self.warnings, "errors": self.errors,
        }


class ProjectImporter:
    """项目导入器（增强版）"""

    def __init__(self, book_dir: str, generator=None):
        self.book_dir = Path(book_dir)
        self.gen = generator

    def from_worldbuilding(self, world_text: str, title: str = "",
                           platform: str = "番茄", genre: str = "修仙",
                           total_chapters: int = 0) -> Dict[str, Any]:
        """从世界观文档初始化完整项目"""
        _log.info(f"ProjectImporter: 世界观→项目 {title}@{platform}")
        self._ensure_dirs()
        (self.book_dir / "设定/世界观原始.md").write_text(world_text, encoding="utf-8")

        from engine.novel_state import NovelState
        from engine.state_accessor import StateAccessor
        ns = NovelState(str(self.book_dir))
        sa = StateAccessor(ns)
        sa.set_meta("platform", platform)
        sa.set_meta("genre", genre)
        sa.set_meta("total_chapters", total_chapters or 200)
        sa.set_meta("title", title[:50] or "未命名")
        sa.save()
        return {"success": True, "title": title, "book_dir": str(self.book_dir), "novel_state": ns}

    def from_text(self, text: str, title: str = "", platform: str = "番茄",
                  genre: str = "") -> ImportResult:
        """从纯文本导入（自动切分+篇幅判定+残章检测）"""
        result = ImportResult()
        result.title = title or "导入作品"
        self._ensure_dirs()

        total_words = len(text)
        detected_ch = self._count_chapters(text)
        result.length_type = self._detect_length_type(total_words, detected_ch)
        result.warnings.append(f"检测到约{detected_ch}章，{total_words}字 → {result.length_type}篇")

        # 智能切分
        chapters = self._smart_split(text)
        if not chapters:
            result.errors.append("未识别到章节分隔")
            return result

        # 残章检测
        last_text, last_title = chapters[-1]
        if len(last_text.strip()) < 1000:
            result.last_chapter_status = "residual"
            result.warnings.append(f"最后一章({last_title})字数<1000，判定为残章")

        # 写入项目
        from engine.novel_state import NovelState
        from engine.state_accessor import StateAccessor
        ns = NovelState(str(self.book_dir))
        sa = StateAccessor(ns)
        sa.set_meta("platform", platform)
        sa.set_meta("genre", genre or "都市")
        sa.set_meta("total_chapters", len(chapters) + 200)
        sa.set_meta("title", title[:50] or "未命名")

        for i, (ch_text, ch_title) in enumerate(chapters):
            ch = i + 1
            (self.book_dir / "正文" / f"第{ch:03d}章.txt").write_text(ch_text, encoding="utf-8")
            spec = {"chapter": ch, "title": ch_title or f"第{ch}章",
                    "word_count": len(ch_text), "is_imported": True}
            (self.book_dir / "规格" / f"第{ch:03d}.json").write_text(
                json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            ns.mark_chapter_done(ch)

        ns.save()
        result.success = True
        result.chapters_imported = len(chapters)
        result.book_dir = str(self.book_dir)
        return result

    def from_existing(self, chapters_dir: str, outline_dir: str = "",
                      platform: str = "番茄", genre: str = "修仙") -> ImportResult:
        """从已有章节目录导入（增强：残章检测+篇幅判定+反向解析）"""
        result = ImportResult()
        self._ensure_dirs()
        src_dir = Path(chapters_dir)

        chapter_files = sorted(src_dir.glob("第*.txt")) + sorted(src_dir.glob("第*.md"))
        chapter_files += sorted(src_dir.glob("*.txt")) + sorted(src_dir.glob("*.md"))

        if not chapter_files:
            result.errors.append(f"未找到章节文件: {chapters_dir}")
            return result

        total_words = sum(f.stat().st_size for f in chapter_files)
        result.length_type = self._detect_length_type(total_words, len(chapter_files))

        from engine.novel_state import NovelState
        from engine.state_accessor import StateAccessor
        ns = NovelState(str(self.book_dir))
        sa = StateAccessor(ns)
        sa.set_meta("platform", platform)
        sa.set_meta("genre", genre)
        sa.set_meta("total_chapters", len(chapter_files) + 200)
        sa.set_meta("title", src_dir.name[:50])

        for i, cf in enumerate(chapter_files):
            ch = i + 1
            text = cf.read_text(encoding="utf-8", errors="replace")
            (self.book_dir / "正文" / f"第{ch:03d}章.txt").write_text(text, encoding="utf-8")
            spec = {"chapter": ch, "title": cf.stem, "word_count": len(text), "is_imported": True}
            (self.book_dir / "规格" / f"第{ch:03d}.json").write_text(
                json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            ns.mark_chapter_done(ch)
            if i == len(chapter_files) - 1 and len(text) < 1000:
                result.last_chapter_status = "residual"

        if outline_dir and Path(outline_dir).exists():
            for f in Path(outline_dir).glob("*"):
                if f.is_file():
                    (self.book_dir / "大纲" / f.name).write_text(f.read_text(), encoding="utf-8")

        ns.save()
        result.success = True
        result.chapters_imported = len(chapter_files)
        result.book_dir = str(self.book_dir)
        result.title = src_dir.name
        return result

    # ── 章节切分 ───────────────────────────

    def _smart_split(self, text: str) -> List[Tuple[str, str]]:
        """智能章节切分"""
        pattern = re.compile(r'(第[零一二三四五六七八九十百千万\d]+[章节回][\s:：]*[^\n]*)')
        parts = pattern.split(text)
        chapters = []
        current_title = ""
        for i, part in enumerate(parts):
            if i == 0 and not pattern.match(part):
                if part.strip():
                    chapters.append((part.strip(), "序章"))
                continue
            if pattern.match(part):
                current_title = part.strip()
            elif current_title and part.strip():
                chapters.append((part.strip(), current_title))
                current_title = ""
        return chapters if chapters else [(text.strip(), "第1章")]

    def _count_chapters(self, text: str) -> int:
        return max(len(CHAPTER_SPLIT_PATTERNS[0].findall(text)), 1)

    def _detect_length_type(self, total_words: int, ch_count: int) -> str:
        if ch_count <= SHORT_NOVEL_MAX_CHAPTERS and total_words <= SHORT_NOVEL_MAX_WORDS:
            return "short"
        return "long"

    def _ensure_dirs(self):
        for d in ["设定", "大纲", "规格", "正文", "追踪/timeline", "追踪/volumes"]:
            (self.book_dir / d).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def discover(base_dir: str) -> Optional[Dict[str, Any]]:
        d = Path(base_dir)
        if not d.exists():
            return None
        has = (d / "正文").exists() and len(list((d / "正文").iterdir())) > 0
        return {"has_chapters": has, "count": len(list((d / "正文").iterdir())) if has else 0}
