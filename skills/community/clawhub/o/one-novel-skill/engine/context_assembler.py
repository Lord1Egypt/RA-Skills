#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
context_assembler.py — 上下文组装器

合并 ResearchEngine / ReferenceEngine / SoulSkill 的上下文注入逻辑。
统一管理生成前的上下文准备，避免 pipeline.py 中的散落调用。
"""

import logging
from typing import Dict, Any, Optional, List

_log = logging.getLogger("context_assembler")


class ContextAssembler:
    """统一的上下文组装器"""

    def __init__(self):
        self._research_engine = None
        self._reference_engine = None
        self._soul_skill = None

    def assemble(
        self,
        chapter: int,
        total: int,
        platform: str,
        genre: str,
        characters: Optional[List[Dict[str, str]]] = None,
        book_dir: str = "",
    ) -> str:
        """组装完整的生成上下文

        返回注入到 LLM prompt 的上下文字符串。
        """
        parts = []

        # 1. ResearchEngine — 本地参考搜索
        research_note = self._inject_research(chapter, platform, genre)
        if research_note:
            parts.append(research_note)

        # 2. ReferenceEngine — 结构化资料注入
        ref_note = self._inject_references(chapter, platform, genre)
        if ref_note:
            parts.append(ref_note)

        # 3. SoulSkill — 角色灵魂注入
        soul_note = self._inject_soul(characters)
        if soul_note:
            parts.append(soul_note)

        return "\n".join(parts)

    def _inject_research(self, chapter: int, platform: str, genre: str) -> str:
        try:
            from .research_engine import ResearchEngine
            if self._research_engine is None:
                self._research_engine = ResearchEngine()
            if chapter <= 3:
                ch_pos = "开头"
            elif chapter <= 20:
                ch_pos = "前期"
            elif chapter <= 100:
                ch_pos = "中期"
            else:
                ch_pos = "后期"
            results = self._research_engine.search_by_context(genre, platform, ch_pos, max_results=2)
            if results and results[0].get("snippet"):
                lines = ["[研究参考]"]
                for r in results[:2]:
                    if r.get("snippet"):
                        lines.append(f"- {r.get('topic', '')}: {r['snippet'][:200]}")
                return "\n".join(lines)
        except Exception as e:
            _log.debug(f"ContextAssembler: research failed: {e}")
        return ""

    def _inject_references(self, chapter: int, platform: str, genre: str) -> str:
        try:
            from .reference_engine import ReferenceEngine
            if self._reference_engine is None:
                self._reference_engine = ReferenceEngine()
            phase_docs = self._reference_engine.query_by_phase(chapter, platform, genre)
            if phase_docs:
                lines = ["[资料注入]"]
                lines.append(" | ".join(
                    f"{d['topic']}: {d['snippet'][:80]}"
                    for d in phase_docs[:3]
                ))
                # 前3章额外注入开篇模板
                if chapter <= 3:
                    template = self._reference_engine.get_genre_opening_template(genre)
                    if template:
                        lines.append(f"[开篇模板] {template[:400]}")
                return "\n".join(lines)
        except Exception as e:
            _log.debug(f"ContextAssembler: references failed: {e}")
        return ""

    def _inject_soul(self, characters: Optional[List[Dict[str, str]]]) -> str:
        if not characters:
            return ""
        try:
            from .soul_skill import SoulSkill
            if self._soul_skill is None:
                self._soul_skill = SoulSkill()
            soul_lines = ["[角色灵魂]"]
            for char in characters[:5]:
                profile = self._soul_skill.get_profile(char.get("archetype", ""))
                if profile:
                    soul_lines.append(
                        f"- {char['name']}({char.get('archetype', '')}): {profile.voice_dna[:60]}"
                    )
            if len(soul_lines) > 1:
                return "\n".join(soul_lines)
        except Exception as e:
            _log.debug(f"ContextAssembler: soul_skill failed: {e}")
        return ""
