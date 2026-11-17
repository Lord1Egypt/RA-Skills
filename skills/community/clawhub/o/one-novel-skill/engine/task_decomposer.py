#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task_decomposer.py — 任务分解系统

融合源: openclaw-novel-write 的 /novel tasks (按卷分拆任务，细化到每章节)
功能: 从大纲/规格分解为可执行任务清单
"""

import json, re
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime


@dataclass
class ChapterTask:
    """单章任务"""
    chapter: int
    volume: int = 1
    title: str = ""
    summary: str = ""
    word_target: int = 2500
    key_scenes: List[str] = field(default_factory=list)
    characters_involved: List[str] = field(default_factory=list)
    foreshadow_to_plant: List[str] = field(default_factory=list)
    foreshadow_to_reveal: List[str] = field(default_factory=list)
    plot_points: List[str] = field(default_factory=list)
    emotional_arc: str = ""
    status: str = "pending"  # pending / spec / written / reviewed

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}
    
    def to_md_row(self) -> str:
        status_icon = {"pending": "⏳", "spec": "📋", "written": "✍️", "reviewed": "✅"}
        icon = status_icon.get(self.status, "⏳")
        return f"| {icon} | 第{self.chapter}章 | {self.title or '-'} | {self.word_target} | {self.summary[:40] or '-'} |"


@dataclass 
class VolumePlan:
    """卷计划"""
    volume: int
    title: str = ""
    description: str = ""
    chapter_start: int = 1
    chapter_end: int = 0
    core_conflict: str = ""
    emotional_theme: str = ""
    climax_chapter: int = 0
    major_arc: str = ""
    tasks: List[ChapterTask] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "volume": self.volume, "title": self.title, "description": self.description,
            "chapter_start": self.chapter_start, "chapter_end": self.chapter_end,
            "core_conflict": self.core_conflict, "emotional_theme": self.emotional_theme,
            "climax_chapter": self.climax_chapter, "major_arc": self.major_arc,
            "tasks": [t.to_dict() for t in self.tasks],
        }


@dataclass
class MasterTaskList:
    """总任务清单"""
    title: str = ""
    volumes: List[VolumePlan] = field(default_factory=list)
    created_at: str = ""
    
    @property
    def total_chapters(self) -> int:
        return sum(v.chapter_end - v.chapter_start + 1 for v in self.volumes if v.chapter_end >= v.chapter_start)
    
    @property
    def completed(self) -> int:
        return sum(1 for v in self.volumes for t in v.tasks if t.status == "reviewed")
    
    @property
    def in_progress(self) -> int:
        return sum(1 for v in self.volumes for t in v.tasks if t.status in ("written", "spec"))

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "volumes": [v.to_dict() for v in self.volumes],
            "total_chapters": self.total_chapters,
            "completed": self.completed,
            "in_progress": self.in_progress,
            "created_at": self.created_at,
        }


class TaskDecomposer:
    """任务分解器"""

    def __init__(self, book_dir: Path = None):
        self.book_dir = Path(book_dir) if book_dir else None

    def decompose(self, total_chapters: int = 100, volume_defs: List[Dict] = None,
                  platform: str = "番茄") -> MasterTaskList:
        """从总章数和卷定义分解为任务清单"""
        master = MasterTaskList(created_at=datetime.now().isoformat())
        
        if volume_defs:
            for vd in volume_defs:
                vp = VolumePlan(
                    volume=vd.get("volume", 1),
                    title=vd.get("title", f"第{vd.get('volume',1)}卷"),
                    description=vd.get("description", ""),
                    chapter_start=vd.get("chapter_start", 1),
                    chapter_end=vd.get("chapter_end", total_chapters),
                    core_conflict=vd.get("core_conflict", ""),
                    emotional_theme=vd.get("emotional_theme", ""),
                    climax_chapter=vd.get("climax_chapter", 0),
                    major_arc=vd.get("major_arc", ""),
                )
                # 按卷分解章节
                for ch in range(vp.chapter_start, vp.chapter_end + 1):
                    vp.tasks.append(ChapterTask(
                        chapter=ch, volume=vp.volume,
                        word_target=2500,
                        summary=self._guess_chapter_role(ch, vp, total_chapters),
                    ))
                master.volumes.append(vp)
        else:
            # 自动分卷
            volumes = self._auto_volume_split(total_chapters, platform)
            for i, (start, end, desc) in enumerate(volumes):
                vp = VolumePlan(
                    volume=i + 1,
                    title=f"第{i+1}卷",
                    description=desc,
                    chapter_start=start, chapter_end=end,
                    climax_chapter=end - 2 if end > start else start,
                )
                for ch in range(start, end + 1):
                    vp.tasks.append(ChapterTask(
                        chapter=ch, volume=i + 1,
                        summary=self._guess_chapter_role(ch, vp, total_chapters),
                    ))
                master.volumes.append(vp)
        return master

    def _auto_volume_split(self, total: int, platform: str) -> List[tuple]:
        """自动分卷策略"""
        if total <= 30:
            return [(1, total, "全书")]
        vol_size = {  # 按平台推荐
            "番茄": 25, "七猫": 25, "飞卢": 30, "起点": 35,
        }.get(platform, 30)
        vcount = max(1, total // vol_size + (1 if total % vol_size > vol_size // 2 else 0))
        chunk = total // vcount
        volumes = []
        for i in range(vcount):
            s = i * chunk + 1
            e = (i + 1) * chunk if i < vcount - 1 else total
            descs = ["开局铺垫", "发展壮大", "矛盾升级", "高潮转折", "终局决战", "尾声结卷"]
            desc = descs[i] if i < len(descs) else f"第{i+1}阶段"
            volumes.append((s, e, desc))
        return volumes

    def _guess_chapter_role(self, ch: int, vol: VolumePlan, total: int) -> str:
        """根据位置猜测章节功能"""
        rel = ch - vol.chapter_start
        length = vol.chapter_end - vol.chapter_start
        if length == 0:
            return "单章完"
        ratio = rel / length
        if ratio < 0.1:
            return "开篇引入"
        elif ratio < 0.3:
            return "冲突建立"
        elif ratio < 0.6:
            return "矛盾推进"
        elif ratio < 0.8:
            return "高潮铺垫"
        elif ratio < 0.9:
            return "高潮爆发"
        else:
            return "收尾过渡"

    def save(self, master: MasterTaskList) -> bool:
        if not self.book_dir:
            return False
        md_path = self.book_dir / "大纲" / "tasks.md"
        json_path = self.book_dir / "大纲" / "tasks.json"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        lines = [f"# 任务总纲: {master.title}", 
                 f"总章节: {master.total_chapters} | 已完成: {master.completed} | 进行中: {master.in_progress}",
                 ""]
        for v in master.volumes:
            lines.extend([
                f"## 第{v.volume}卷: {v.title}",
                f"章节范围: 第{v.chapter_start}-{v.chapter_end}章 | 核心冲突: {v.core_conflict or '-'}",
                "",
                "| 状态 | 章节 | 标题 | 字数 | 摘要 |",
                "|------|------|------|------|------|",
            ])
            for t in v.tasks:
                lines.append(t.to_md_row())
            lines.append("")
        
        try:
            md_path.write_text("\n".join(lines), encoding="utf-8")
            json_path.write_text(json.dumps(master.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
            return True
        except OSError:
            return False

    def load(self) -> Optional[MasterTaskList]:
        if not self.book_dir:
            return None
        path = self.book_dir / "大纲" / "tasks.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            master = MasterTaskList(title=data.get("title", ""), created_at=data.get("created_at", ""))
            for vd in data.get("volumes", []):
                vp = VolumePlan(volume=vd["volume"], title=vd.get("title", ""),
                    description=vd.get("description", ""),
                    chapter_start=vd.get("chapter_start", 1), chapter_end=vd.get("chapter_end", 0),
                    core_conflict=vd.get("core_conflict", ""), emotional_theme=vd.get("emotional_theme", ""),
                    climax_chapter=vd.get("climax_chapter", 0), major_arc=vd.get("major_arc", ""))
                for td in vd.get("tasks", []):
                    vp.tasks.append(ChapterTask(**td))
                master.volumes.append(vp)
            return master
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            return None

    def update_status(self, chapter: int, status: str) -> bool:
        """更新单章任务状态"""
        for v in self.load().volumes if self.load() else []:
            for t in v.tasks:
                if t.chapter == chapter:
                    t.status = status
                    return True
        return False
