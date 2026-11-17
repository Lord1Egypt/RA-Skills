#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应上下文 ContextBuilder

替换 NovelState.llm_context() 的全量上下文策略，改为自适应策略：
- 章节 < 50:   全量上下文（角色列表 + 伏笔列表 + 时间线）
- 50-200 章:   滑窗（最近 5 章摘要 + 相关角色 + 相关伏笔）
- 200+ 章:     分层（卷摘要 + 按需拉取）

三层记忆体系已拆分至独立模块：
  working_memory.py   -- 工作记忆（短期上下文窗口）
  episodic_memory.py  -- 情节记忆（章节历史记录 + 持久化）
  semantic_memory.py  -- 语义记忆（高层创作洞察）
"""

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, List

from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory

if TYPE_CHECKING:
    from novel_state import NovelState

_log = logging.getLogger("context_builder")

THRESHOLD_FULL = 50
THRESHOLD_SLIDING = 200
WINDOW_SIZE = 5
MAX_HOOKS = 5
MAX_TIMELINE = 10


class ContextBuilder:
    """自适应上下文构建器（整合三层记忆体系）

    兼容两种状态源：
    - NovelState 对象（旧接口，通过 property 代理）
    - None（优雅降级，从文件系统直接读取）
    """

    def __init__(self, novel_state, book_dir: str):
        self.ns = novel_state
        self.book_dir = Path(book_dir)
        self.vol_dir = self.book_dir / "追踪" / "volumes"
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory(book_dir)
        self.semantic = SemanticMemory()
        self.episodic.load()

    def _get_state_dict(self) -> dict:
        """获取状态字典，兼容 NovelState 和 None"""
        if self.ns is not None:
            try:
                # 尝试通过 to_dict() 获取（StateRoot 路径）
                if hasattr(self.ns, 'to_dict'):
                    return self.ns.to_dict()
                # 回退到 _state property
                return self.ns._state
            except Exception:
                pass
        # 从文件系统直接加载
        state_path = self.book_dir / "state.json"
        if state_path.exists():
            try:
                return json.loads(state_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    # -- 公开入口

    def build(self, chapter: int) -> str:
        s = self._get_state_dict()
        total = s.get("meta", {}).get("total_chapters", 0) if self.ns else 0
        if self.ns and hasattr(self.ns, 'meta'):
            total = self.ns.meta.get("total_chapters", 0)
        effective = max(total, chapter)
        self.working.update(chapter, f"\u5f53\u524d\u5904\u7406\u7b2c{chapter}\u7ae0")
        if effective < THRESHOLD_FULL or chapter < THRESHOLD_FULL:
            return self._full_context(chapter)
        elif effective < THRESHOLD_SLIDING:
            return self._sliding_window(chapter)
        else:
            return self._hierarchical(chapter)

    # -- 策略 1：全量上下文

    def _full_context(self, chapter: int) -> str:
        s = self._get_state_dict()
        lines = []
        meta = s.get("meta", {})
        prog = s.get("progress", {})
        lines.append(f"\u5e73\u53f0: {meta.get('platform','?')} \u7c7b\u578b: {meta.get('genre','?')}")
        lines.append(f"\u8fdb\u5ea6: {prog.get('written',0)}/{prog.get('total_planned',0)}")
        lines.append("")
        chars = s.get("characters", {})
        lines.append("\u3010\u89d2\u8272\u72b6\u6001\u3011")
        for name, data in chars.items():
            lines.append(f"  {name}: {data.get('state','?')} @ {data.get('location','?')}")
        lines.append("")
        settings = [st for st in s.get("settings", []) if st.get("status") == "active"]
        if settings:
            lines.append("\u3010\u8bbe\u5b9a\u3011")
            for st in settings[:3]:
                lines.append(f"  {st['name']}: {st.get('content','')[:50]}")
            lines.append("")
        hooks = self.ns.unresolved_hooks() if self.ns and hasattr(self.ns, "unresolved_hooks") else []
        if hooks:
            lines.append("\u3010\u672a\u56de\u6536\u4f0f\u7b14\u3011")
            for h in hooks[:MAX_HOOKS]:
                imp = "\u2605" * h.get("importance", 3)
                lines.append(f"  {imp} \u7b2c{h.get('chapter','?')}\u7ae0: {h.get('text','')[:40]}")
            lines.append("")
        tl = s.get("timeline", [])
        if tl:
            lines.append("\u3010\u65f6\u95f4\u7ebf\u3011")
            for e in tl[-MAX_TIMELINE:]:
                lines.append(f"  \u7b2c{e.get('chapter','?')}\u7ae0: {e.get('event','')[:60]}")
            lines.append("")
        return "\n".join(lines)

    # -- 策略 2：滑窗上下文

    def _sliding_window(self, chapter: int) -> str:
        lines = []
        spec_dir = self.book_dir / "\u89c4\u683c"
        lines.append("\u3010\u524d\u60c5\u63d0\u8981\u3011")
        start = max(1, chapter - WINDOW_SIZE)
        for ch in range(start, chapter):
            spec_file = spec_dir / f"\u7b2c{ch:03d}.json"
            if spec_file.exists():
                try:
                    spec = json.loads(spec_file.read_text(encoding="utf-8"))
                    summary = spec.get("summary", "") or spec.get("brief", "")
                    lines.append(f"  \u7b2c{ch}\u7ae0: {summary[:120]}")
                except Exception:
                    pass
        lines.append("")
        chars = self.ns.characters if self.ns and hasattr(self.ns, 'characters') else {}
        lines.append("\u3010\u76f8\u5173\u89d2\u8272\u3011")
        for name, data in chars.items():
            lines.append(f"  {name}: {data.get('state','?')}")
        lines.append("")
        hooks = self.ns.unresolved_hooks() if self.ns and hasattr(self.ns, "unresolved_hooks") else []
        if hooks:
            lines.append("\u3010\u6d3b\u8dc3\u4f0f\u7b14\u3011")
            for h in hooks[:MAX_HOOKS]:
                lines.append(f"  {h.get('text','')[:60]} [\u7b2c{h.get('chapter','?')}\u7ae0]")
            lines.append("")
        return "\n".join(lines)

    # -- 策略 3：分层上下文

    def _hierarchical(self, chapter: int) -> str:
        vol = max(1, (chapter - 1) // 100 + 1)
        self.vol_dir.mkdir(parents=True, exist_ok=True)
        lines = []
        summary_file = self.vol_dir / f"vol-{vol:04d}-summary.txt"
        if summary_file.exists():
            lines.append(f"\u3010\u7b2c{vol}\u5377\u6458\u8981\u3011")
            lines.append(summary_file.read_text(encoding="utf-8").strip())
            lines.append("")
        else:
            lines.append(f"\u3010\u7b2c{vol}\u5377\u3011\uff08\u6458\u8981\u672a\u751f\u6210\uff0c\u81ea\u52a8\u91c7\u96c6\u4e2d\uff09")
            lines.append("")
        lines.append("\u3010\u672c\u7ae0\u4fe1\u606f\u3011")
        spec_file = self.book_dir / "\u89c4\u683c" / f"\u7b2c{chapter:03d}.json"
        if spec_file.exists():
            try:
                spec = json.loads(spec_file.read_text(encoding="utf-8"))
                before = spec.get("before_state", {})
                chars = before.get("characters", [])
                if chars:
                    lines.append(f"  \u51fa\u573a\u89d2\u8272: {', '.join(str(c) for c in chars)}")
                summary = spec.get("summary", "") or spec.get("brief", "")
                if summary:
                    lines.append(f"  \u7ae0\u8282\u6982\u8981: {summary[:200]}")
            except Exception:
                lines.append("  (\u89c4\u683c\u6587\u4ef6\u8bfb\u53d6\u5931\u8d25)")
        else:
            lines.append("  (\u89c4\u683c\u6587\u4ef6\u672a\u751f\u6210)")
        hooks = self.ns.unresolved_hooks() if hasattr(self.ns, "unresolved_hooks") else []
        high_prio = [h for h in hooks if h.get("importance", 3) >= 4]
        if high_prio:
            lines.append("")
            lines.append("\u3010\u9ad8\u4f18\u5148\u7ea7\u4f0f\u7b14\u3011")
            for h in high_prio[:3]:
                lines.append(f"  {h.get('text','')[:80]} [\u7b2c{h.get('chapter','?')}\u7ae0]")
        return "\n".join(lines)

    # -- 三层记忆接口（委托给独立模块）

    def record_chapter(self, chapter: int, summary: str):
        self.episodic.record(chapter, summary)

    def get_relevant_memory(self, chapter: int, count: int = 5) -> str:
        return self.episodic.get_relevant(chapter, count)

    def build_with_memory(self, chapter: int) -> str:
        ctx = self.build(chapter)
        memory = self.get_relevant_memory(chapter)
        if memory:
            ctx += "\n\n\u3010\u5267\u96c6\u8bb0\u5fc6\u3011\n" + memory
        return ctx

    def add_insight(self, insight: str, source_chapter: int = 0):
        self.semantic.add(insight, source_chapter)

    def get_semantic_context(self) -> str:
        return self.semantic.get_all()


def build_context(novel_state, chapter: int, book_dir: str = None) -> str:
    if book_dir is None:
        book_dir = str(novel_state.book_dir)
    builder = ContextBuilder(novel_state, book_dir)
    return builder.build(chapter)
