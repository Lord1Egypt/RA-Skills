#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timeline_builder.py — 时间线生成与校验

融合源: openclaw-novel-write 的 /novel timeline (时间线文档 + 与计划互相校验)
功能: 
  1. 从大纲提取事件并按时间线排列
  2. 与创作计划互相校验（关键情节点必须在时间线中）
  3. 校验失败输出冲突报告
"""

import json
import re
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from datetime import datetime


@dataclass
class TimelineEvent:
    """时间线事件"""
    seq: int
    time_label: str           # 时间点描述："第1年3月" / "三个月后"
    event: str                # 事件描述
    chapter: Optional[int] = None  # 对应章节
    importance: int = 2       # 1-3: low/mid/high
    status: str = "计划"      # 计划 / 已写 / 待校验
    category: str = "主线"    # 主线 / 支线 / 感情线 / 伏笔

    def to_markdown_row(self) -> str:
        stars = "⭐" * self.importance
        ch = f"第{self.chapter}章" if self.chapter else "-"
        return f"| {self.seq:03d} | {self.time_label} | {self.event} | {ch} | {stars} |"


@dataclass
class Timeline:
    """完整时间线"""
    title: str = ""
    events: List[TimelineEvent] = field(default_factory=list)
    created_at: str = ""

    def add_event(self, time_label: str, event: str, chapter: Optional[int] = None,
                  importance: int = 2, category: str = "主线") -> int:
        seq = len(self.events) + 1
        te = TimelineEvent(seq=seq, time_label=time_label, event=event,
                           chapter=chapter, importance=importance, category=category)
        self.events.append(te)
        return seq

    def sort_by_time(self):
        """按时间标签排序（简单按数字优先）"""
        def _time_key(e: TimelineEvent) -> tuple:
            nums = re.findall(r'\d+', e.time_label)
            return (int(nums[0]) if nums else 9999, e.time_label)
        self.events.sort(key=_time_key)
        for i, e in enumerate(self.events):
            e.seq = i + 1

    def to_markdown(self) -> str:
        lines = [
            f"# 时间线: {self.title}",
            "",
            "| 序号 | 时间点 | 事件 | 章节对应 | 重要程度 |",
            "|------|--------|------|---------|---------|",
        ]
        for e in self.events:
            lines.append(e.to_markdown_row())
        lines.append("")
        lines.append(f"> 共 {len(self.events)} 个事件 | 生成时间: {self.created_at}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "events": [asdict(e) for e in self.events],
            "created_at": self.created_at,
        }


@dataclass
class ValidationConflict:
    """校验冲突"""
    conflict_type: str   # "时间线缺失" / "计划缺失" / "章节偏移"
    event_description: str
    source: str          # "计划" / "时间线"
    severity: str        # "error" / "warning"

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.conflict_type}: {self.event_description} (来源: {self.source})"


class TimelineBuilder:
    """时间线构建器"""

    def __init__(self, book_dir: Path):
        self.book_dir = Path(book_dir)

    def _load_outline(self) -> Optional[dict]:
        """从大纲目录加载故事大纲"""
        path = self.book_dir / "大纲" / "故事大纲.md"
        alt_path = self.book_dir / "大纲" / "故事大纲.json"
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            return {"text": text, "format": "md"}
        if alt_path.exists():
            try:
                return json.loads(alt_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return None
        return None

    def _load_chapter_specs(self) -> List[dict]:
        """从规格目录加载所有章节spec"""
        spec_dir = self.book_dir / "规格"
        specs = []
        if spec_dir.exists():
            for f in sorted(spec_dir.glob("*.json")):
                try:
                    specs.append(json.loads(f.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    continue
        return specs

    def build_from_outline(self, title: str) -> Timeline:
        """从大纲构建时间线"""
        tl = Timeline(title=title, created_at=datetime.now().isoformat())
        outline = self._load_outline()
        if not outline:
            return tl

        text = outline if isinstance(outline, str) else outline.get("text", "")
        specs = self._load_chapter_specs()

        # 从spec提取事件
        for spec in specs:
            ch = spec.get("chapter", 0)
            must_happen = spec.get("must_happen", [])
            if isinstance(must_happen, list):
                for event in must_happen:
                    tl.add_event(
                        time_label=f"第{ch}章",
                        event=event,
                        chapter=ch,
                        importance=2,
                        category="主线",
                    )
            after_state = spec.get("after_state", {})
            new_chars = after_state.get("new_characters", []) if isinstance(after_state, dict) else []
            if isinstance(new_chars, list):
                for char in new_chars:
                    if isinstance(char, dict):
                        name = char.get("name", str(char))
                        tl.add_event(
                            time_label=f"第{ch}章",
                            event=f"{name} 出场",
                            chapter=ch,
                            importance=2,
                            category="角色",
                        )
        return tl

    def validate_with_plan(self, tl: Timeline, plan_text: str) -> List[ValidationConflict]:
        """校验时间线与计划的一致性"""
        conflicts = []

        # 提取计划中的关键事件
        plan_events = re.findall(r'[-*]\s*(?:第\d+章[：:]\s*)?([^\n]{5,60})', plan_text)

        # 检查计划中的事件是否在时间线中
        timeline_events_text = [e.event for e in tl.events]
        for pe in plan_events:
            pe_clean = pe.strip()[:20]
            found = any(pe_clean in te for te in timeline_events_text)
            if not found:
                # 检查是否在spec中
                in_spec = False
                specs = self._load_chapter_specs()
                for spec in specs:
                    mh = spec.get("must_happen", [])
                    if isinstance(mh, list) and any(pe_clean in str(m) for m in mh):
                        in_spec = True
                        break
                if not in_spec:
                    conflicts.append(ValidationConflict(
                        conflict_type="时间线缺失",
                        event_description=f"计划中的事件未在时间线中出现: {pe[:40]}",
                        source="计划",
                        severity="warning",
                    ))

        return conflicts

    def save(self, tl: Timeline) -> bool:
        """保存时间线"""
        md_path = self.book_dir / "大纲" / "时间线.md"
        json_path = self.book_dir / "大纲" / "时间线.json"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            md_path.write_text(tl.to_markdown(), encoding="utf-8")
            json_path.write_text(json.dumps(tl.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
            return True
        except OSError:
            return False

    def load(self) -> Optional[Timeline]:
        json_path = self.book_dir / "大纲" / "时间线.json"
        if not json_path.exists():
            return None
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            tl = Timeline(title=data.get("title", ""), created_at=data.get("created_at", ""))
            for ed in data.get("events", []):
                tl.events.append(TimelineEvent(**ed))
            return tl
        except (json.JSONDecodeError, TypeError, KeyError):
            return None
