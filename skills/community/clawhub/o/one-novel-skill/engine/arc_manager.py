#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""弧管理器 — 卷弧滚动规划"""

import json
from pathlib import Path
from typing import Optional


class ArcManager:
    """管理小说卷弧的滚动规划"""
    
    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self._arc_file = self.book_dir / "追踪" / "arcs.json"
        self._arcs = self._load()
    
    def _load(self) -> dict:
        if self._arc_file.exists():
            return json.loads(self._arc_file.read_text(encoding="utf-8"))
        return {"arcs": [], "current_arc": 0, "expanded_until": 0}
    
    def _save(self):
        self._arc_file.parent.mkdir(parents=True, exist_ok=True)
        self._arc_file.write_text(
            json.dumps(self._arcs, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def init_plan(self, total_arcs: int, arc_names: list):
        """初始化时只存骨架，不展开细节"""
        self._arcs["arcs"] = [
            {"id": i, "name": arc_names[i] if i < len(arc_names) else f"第{i+1}卷",
             "chapters": 0, "status": "skeleton",
             "summary": "", "start_chapter": 0}
            for i in range(total_arcs)
        ]
        self._arcs["current_arc"] = 0
        self._arcs["expanded_until"] = 2  # 只展开前2卷
        self._save()
    
    def get_current_chapter_range(self) -> tuple:
        """返回当前可写章节范围 (start, end)"""
        if not self._arcs["arcs"]:
            return (1, 10)
        expanded = min(self._arcs["expanded_until"], len(self._arcs["arcs"]))
        total_ch = sum(
            a.get("chapters", 0) or 100
            for a in self._arcs["arcs"][:expanded]
        )
        return (1, max(10, total_ch))
    
    def advance_arc(self, current_chapter: int):
        """当写入接近当前弧尾时，展开下一弧"""
        end = self.get_current_chapter_range()[1]
        if current_chapter >= end - 10:
            if self._arcs["expanded_until"] < len(self._arcs["arcs"]):
                self._arcs["expanded_until"] += 1
                self._arcs["current_arc"] = self._arcs["expanded_until"] - 2
                self._save()
                return True
        return False
    
    def get_status(self) -> dict:
        return {
            "total_arcs": len(self._arcs["arcs"]),
            "expanded_until": self._arcs["expanded_until"],
            "current_arc": self._arcs["current_arc"],
        }

    def volume_reflection(self, volume, chapters):
        from datetime import datetime
        lines = ['# 第{}卷 反思报告'.format(volume), '']
        arcs = [a for a in self._arcs.get("arcs", []) if a.get("start_chapter", 0) <= chapters[-1]
                and (a.get("end_chapter", 0) == 0 or a.get("end_chapter", 0) >= chapters[0])]
        if not arcs:
            lines.append('该卷无活跃弧线')
            return chr(10).join(lines)
        resolved = sum(1 for a in arcs if a.get("status", "") == 'completed')
        lines.append('活跃弧线: {} 条, 已解决: {}'.format(len(arcs), resolved))
        lines.append('')
        if resolved == 0:
            lines.append('- 建议: 所有弧线仍在进行, 关注闭合节奏')
        elif resolved < len(arcs) * 0.3:
            lines.append('- 建议: 解决率偏低, 在下卷安排弧线回收')
        elif resolved > len(arcs) * 0.7:
            lines.append('- 建议: 解决率高, 下卷可开新弧线')
        lines.append('> 生成: {}'.format(datetime.now().isoformat()[:19]))
        return chr(10).join(lines)

    def save_volume_reflection(self, volume, chapters, book_dir):
        report = self.volume_reflection(volume, chapters)
        bd = Path(book_dir) / '评审'
        bd.mkdir(parents=True, exist_ok=True)
        (bd / '第{}卷反思.md'.format(volume)).write_text(report, encoding='utf-8')
        return True
