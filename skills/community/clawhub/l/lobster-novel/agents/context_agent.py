from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.contract import RuntimeContract
from core.story_state import HookState, StoryState

# RAG import (optional — no crash if model file missing)
try:
    from rag.novel_rag import NovelRAGIndex, format_rag_prompt
    _HAS_RAG = True
except ImportError:
    _HAS_RAG = False

# 三定律（从 three_laws 导入，唯一权威版本）
try:
    from agents.three_laws import THREE_LAWS as _THREE_LAWS, PreWriteValidator, format_three_laws_block
    _HAS_LAWS = True
except ImportError:
    _HAS_LAWS = False
    _THREE_LAWS = [
        "大纲即法律：严格遵循大纲设定，不擅自添加未规划的情节、角色、地点或物品",
        "设定即物理：人物能力、世界观规则、时间线必须前后一致，不得矛盾",
        "发明需识别：任何新增的实体、地点、能力必须在章节记录中以【新增】标记明确标注",
    ]

_DEFAULT_STYLE = ["西幻·史诗感", "描写细腻", "对话节制"]

DEFAULT_STRANDS = {"quest": 0.6, "fire": 0.2, "constellation": 0.2}


class ContextAgent:
    """Builds writing context (RuntimeContract) before each chapter is written."""

    def __init__(self, project_dir: str | Path, use_rag: bool = True) -> None:
        self.project_dir = Path(project_dir)
        self._rag_index: Optional[NovelRAGIndex] = None
        self._use_rag = use_rag and _HAS_RAG

    def _init_rag(self) -> None:
        """Lazy-init RAG index."""
        if not self._use_rag or self._rag_index is not None:
            return
        idx = NovelRAGIndex.load(self.project_dir)
        if idx is None:
            idx = NovelRAGIndex(self.project_dir)
            idx.build()
            idx.save()
        self._rag_index = idx

    def build_runtime_contract(
        self, chapter_number: int, story_state: StoryState, chapter_title: str = "",
    ) -> RuntimeContract:
        outline = self._find_outline_section(chapter_number)
        active_chars = self._resolve_active_characters(chapter_number, story_state)
        active_hooks = self._resolve_active_hooks(chapter_number, story_state)
        strand_targets = self._resolve_strand_targets(story_state)
        style_constraints = self._load_style_template()

        # RAG semantic retrieval
        entity_constraints: list[str] = []
        self._init_rag()
        if self._rag_index is not None:
            query = outline or f"第{chapter_number}章"
            rag_results = self._rag_index.search(
                query, top_k=6, categories=None,
            )
            if rag_results:
                entity_constraints.append(
                    format_rag_prompt(rag_results, top_k=6)
                )
                print(f"[ContextAgent] RAG retrieved {len(rag_results)} relevant items")

        # 三定律写前校验
        if _HAS_LAWS and outline:
            try:
                pv = PreWriteValidator(self.project_dir)
                pre_report = pv.check_outline(chapter_number, outline, story_state)
                if pre_report.violations:
                    entity_constraints.append(pre_report.to_prompt_block())
                    print(f"[ContextAgent] Pre-write validation: {len(pre_report.violations)} warnings")
            except Exception as e:
                print(f"[ContextAgent] Pre-write validation error: {e}")

        contract = RuntimeContract(
            chapter_number=chapter_number,
            chapter_title=chapter_title or f"第{chapter_number}章",
            outline_section=outline,
            active_characters=active_chars,
            active_hooks=active_hooks,
            strand_targets=strand_targets,
            style_constraints=style_constraints,
            entity_constraints=entity_constraints,
            three_laws=list(_THREE_LAWS),
        )
        print(
            f"[ContextAgent] Chapter {chapter_number} contract ready — "
            f"{len(active_chars)} active characters, "
            f"{len(active_hooks)} active hooks, "
            f"strands={strand_targets}, "
            f"laws={len(_THREE_LAWS)}, "
            f"rag={self._rag_index is not None}"
        )
        return contract

    def format_writing_prompt(self, contract: RuntimeContract) -> str:
        lines = [f"第{contract.chapter_number}章：{contract.chapter_title}", ""]
        lines.append("【大纲】")
        lines.append(contract.outline_section or "（暂无大纲章节）")
        lines.append("")
        if contract.active_characters:
            lines.append("【活跃角色】")
            lines.append("、".join(contract.active_characters))
            lines.append("")
        if contract.active_hooks:
            lines.append("【活跃伏笔】")
            for h in contract.active_hooks:
                lines.append(f"- {h.get('description', h.get('id', str(h)))}({h.get('type', '悬念')})")
            lines.append("")
        t = contract.strand_targets
        lines.append("【节奏目标】")
        lines.append(f"- 主线剧情(Quest): {t.get('quest', 0) * 100:.0f}%")
        lines.append(f"- 感情线(Fire): {t.get('fire', 0) * 100:.0f}%")
        lines.append(f"- 世界观(Constellation): {t.get('constellation', 0) * 100:.0f}%")
        lines.append("")
        if contract.style_constraints:
            lines.append("【风格约束】")
            for sc in contract.style_constraints:
                lines.append(f"- {sc}")
            lines.append("")
        # RAG semantic context (from entity_constraints)
        for ec in contract.entity_constraints:
            if ec.startswith("【RAG"):
                lines.append(ec)
                lines.append("")
                break
        lines.append("【创作纪律 — 防幻觉三定律】")
        for i, law in enumerate(contract.three_laws, 1):
            lines.append(f"{i}. {law}")
        return "\n".join(lines)

    def _find_outline_section(self, chapter_number: int) -> str:
        volumes_dir = self.project_dir / "volumes"
        if not volumes_dir.is_dir():
            return ""
        patterns = [f"## Ch{chapter_number}", f"## {chapter_number}"]
        for md_file in sorted(volumes_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            for pat in patterns:
                if pat not in text:
                    continue
                return self._extract_section(text, pat)
        return ""

    @staticmethod
    def _extract_section(text: str, heading: str) -> str:
        lines = text.splitlines()
        start = None
        for i, line in enumerate(lines):
            if line.strip() == heading:
                start = i
                break
        if start is None:
            return ""
        result = []
        for line in lines[start + 1 :]:
            if re.match(r"^##\s", line):
                break
            result.append(line)
        return "\n".join(result).strip()

    def _resolve_active_characters(
        self, chapter_number: int, story_state: StoryState,
    ) -> list[str]:
        active = []
        for cid, ch in story_state.characters.items():
            if ch.status != "active":
                continue
            # Exclude characters who haven't appeared yet
            if ch.first_appearance > 0 and ch.first_appearance > chapter_number:
                continue
            # Exclude characters absent for more than 5 chapters
            if ch.last_appearance > 0 and ch.last_appearance < chapter_number - 5:
                continue
            active.append(ch.name or ch.id)
        return active

    def _resolve_active_hooks(
        self, chapter_number: int, story_state: StoryState,
    ) -> list[dict[str, Any]]:
        result = []
        for hook in story_state.get_active_hooks():
            if self._hook_payoff_matches(hook, chapter_number):
                result.append({
                    "id": hook.id,
                    "description": hook.description,
                    "type": hook.type,
                    "chapter_created": hook.chapter_created,
                    "expected_payoff": hook.expected_payoff,
                })
        return result

    @staticmethod
    def _hook_payoff_matches(hook: HookState, chapter: int) -> bool:
        raw = hook.expected_payoff.strip()
        if not raw:
            return True
        m = re.match(r"(\d+)\s*[-–]\s*(\d+)", raw)
        if m:
            return int(m.group(1)) <= chapter <= int(m.group(2))
        m = re.match(r"^(\d+)$", raw)
        if m:
            return chapter >= int(m.group(1))
        m = re.match(r"(\d+)\s*\+?", raw)
        if m:
            return chapter >= int(m.group(1))
        return True

    def _resolve_strand_targets(self, story_state: StoryState) -> dict[str, float]:
        targets = dict(DEFAULT_STRANDS)
        if story_state.strands.quest_streak > 3:
            targets["quest"] -= 0.1
            targets["fire"] += 0.1
        return targets

    def _load_style_template(self) -> list[str]:
        bible_path = self.project_dir / "bible.json"
        if not bible_path.is_file():
            return list(_DEFAULT_STYLE)
        try:
            data = json.loads(bible_path.read_text(encoding="utf-8"))
            template = data.get("style_template")
            if isinstance(template, list) and all(isinstance(s, str) for s in template):
                return template
        except (json.JSONDecodeError, OSError):
            pass
        return list(_DEFAULT_STYLE)
