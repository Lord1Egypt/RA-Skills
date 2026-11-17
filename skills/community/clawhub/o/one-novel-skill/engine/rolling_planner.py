#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rolling_planner.py — 指南针+视野滚动规划引擎

灵感来源: ainovel-cli 的卷弧双层滚动规划
核心思想: 长篇不一次规划全部章节，近处精细、远处模糊，模拟网文作者真实创作方式。

规划层次:
  指南针层: 全书3-5个大弧（每弧一个大目标/大冲突/大转折）
  视野层:   只展开当前弧的详细章节，下一弧只有骨架
  滚动:     写完当前弧的80%时自动展开下一弧

用法:
  planner = RollingPlanner(book_dir)
  planner.init_arcs(total_arcs=5, titles=[...])
  planner.get_next_chapter_plan()  # 返回下一章的规划上下文
  planner.mark_chapter_done(ch)    # 标记完成，触发滚动展开
"""

import json, logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

_log = logging.getLogger("rolling_planner")


class RollingPlanner:
    """指南针+视野滚动规划引擎"""

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self._plan_path = self.book_dir / "大纲" / "滚动规划.json"
        self._state = self._load()

    def _load(self) -> dict:
        if self._plan_path.exists():
            try:
                return json.loads(self._plan_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "compass": [],       # 指南针层: 全书弧
            "current_arc": 0,    # 当前弧索引
            "expanded_arcs": [], # 已展开详细章节的弧索引
            "chapters_written": 0,
            "last_updated": "",
        }

    def _save(self):
        self._state["last_updated"] = datetime.now().isoformat()
        self._plan_path.parent.mkdir(parents=True, exist_ok=True)
        self._plan_path.write_text(
            json.dumps(self._state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def init_arcs(self, total_arcs: int = 5, titles: Optional[List[str]] = None):
        """初始化全书指南针——只设弧级目标，不展开章节"""
        if not titles:
            titles = [f"第{i+1}卷" for i in range(total_arcs)]

        self._state["compass"] = [
            {
                "arc_id": i + 1,
                "title": titles[i] if i < len(titles) else f"第{i+1}卷",
                "goal": "",           # 本弧核心目标
                "conflict": "",       # 核心冲突
                "turning_point": "",  # 转折点
                "status": "locked",   # locked | expanded | writing | completed
                "total_chapters": 0,  # 展开后填充
                "chapters": [],       # 展开后填充详细章纲
            }
            for i in range(total_arcs)
        ]

        # 展开第一个弧
        self._expand_arc(0)
        self._state["current_arc"] = 0
        self._save()

    def _expand_arc(self, arc_idx: int, chapters: int = 10):
        """展开一个弧的详细章节骨架

        每个章节只包含: 目标/核心事件/结尾钩子类型，不包含详细情节。
        详细情节在每章写前由 pipeline Phase A 生成。
        """
        if arc_idx >= len(self._state["compass"]):
            return

        arc = self._state["compass"][arc_idx]
        if arc["status"] in ("expanded", "writing", "completed"):
            return

        arc["status"] = "expanded"
        arc["total_chapters"] = chapters
        arc["chapters"] = [
            {
                "ch": i + 1,
                "goal": "",        # 本章目标
                "core_event": "",  # 核心事件
                "hook_type": "",   # 钩子类型: 信息差/突发事件/关系转折/身份揭露
                "status": "planned",
            }
            for i in range(chapters)
        ]

        if arc_idx not in self._state["expanded_arcs"]:
            self._state["expanded_arcs"].append(arc_idx)

        _log.info(f"RollingPlanner: 展开弧{arc['arc_id']} — {chapters}章骨架")

    def get_current_arc(self) -> Optional[dict]:
        """获取当前弧"""
        idx = self._state["current_arc"]
        if idx < len(self._state["compass"]):
            return self._state["compass"][idx]
        return None

    def get_next_chapter_plan(self) -> Optional[dict]:
        """获取下一章规划上下文

        返回:
          {
            "chapter": 全局章节号,
            "arc_chapter": 弧内章节号,
            "arc": 弧信息,
            "arc_progress": "2/10",
            "goal": 本章目标,
            "core_event": 核心事件,
            "hook_type": 钩子类型,
            "nearby_chapters": 前后3章的骨架,
          }
        """
        arc = self.get_current_arc()
        if not arc or not arc["chapters"]:
            return None

        # 找到下一个未完成的章节
        chs = arc["chapters"]
        next_ch = None
        for ch in chs:
            if ch["status"] == "planned":
                next_ch = ch
                break

        if not next_ch:
            # 当前弧全部完成
            return None

        # 计算全局章节号
        global_ch = sum(
            a.get("total_chapters", 0) or 0
            for a in self._state["compass"][:self._state["current_arc"]]
        ) + next_ch["ch"]

        # 附近章节骨架（前后各3章）
        arc_ch_idx = next_ch["ch"] - 1  # 转为0基索引
        nearby = []
        for i in range(max(0, arc_ch_idx - 3), min(len(chs), arc_ch_idx + 4)):
            if i != arc_ch_idx:
                nearby.append({
                    "ch": chs[i]["ch"],
                    "goal": chs[i].get("goal", ""),
                    "status": chs[i]["status"],
                })

        return {
            "chapter": global_ch,
            "arc_chapter": next_ch["ch"],
            "arc": {
                "id": arc["arc_id"],
                "title": arc["title"],
                "goal": arc.get("goal", ""),
                "conflict": arc.get("conflict", ""),
            },
            "arc_progress": f"{next_ch['ch']}/{arc['total_chapters']}",
            "goal": next_ch.get("goal", ""),
            "core_event": next_ch.get("core_event", ""),
            "hook_type": next_ch.get("hook_type", ""),
            "nearby_chapters": nearby,
        }

    def mark_chapter_done(self, global_ch: int):
        """标记章节完成，自动触发滚动展开"""
        arc = self.get_current_arc()
        if not arc or not arc["chapters"]:
            return

        arc["status"] = "writing"

        # 在弧内找到对应章节
        arc_offset = sum(
            a.get("total_chapters", 0) or 0
            for a in self._state["compass"][:self._state["current_arc"]]
        )
        arc_ch = global_ch - arc_offset

        for ch in arc["chapters"]:
            if ch["ch"] == arc_ch:
                ch["status"] = "done"
                break

        self._state["chapters_written"] += 1

        # 检查当前弧是否完成
        done_in_arc = sum(1 for ch in arc["chapters"] if ch["status"] == "done")
        if done_in_arc >= arc["total_chapters"]:
            arc["status"] = "completed"
            _log.info(f"RollingPlanner: 弧{arc['arc_id']}完成 ({done_in_arc}章)")

            # 进入下一弧
            next_idx = self._state["current_arc"] + 1
            if next_idx < len(self._state["compass"]):
                self._state["current_arc"] = next_idx
                self._expand_arc(next_idx)
                _log.info(f"RollingPlanner: 进入弧{next_idx + 1}")

        # 滚动展开：当前弧完成80%时展开下一弧
        elif done_in_arc >= int(arc["total_chapters"] * 0.8):
            next_idx = self._state["current_arc"] + 1
            if next_idx < len(self._state["compass"]):
                next_arc = self._state["compass"][next_idx]
                if next_arc["status"] == "locked":
                    self._expand_arc(next_idx)
                    _log.info(
                        f"RollingPlanner: 滚动展开弧{next_idx + 1} "
                        f"(当前弧进度 {done_in_arc}/{arc['total_chapters']})"
                    )

        self._save()

    def get_summary(self) -> dict:
        """获取规划摘要"""
        arcs_summary = []
        for a in self._state["compass"]:
            done = sum(1 for ch in a.get("chapters", []) if ch.get("status") == "done")
            total = a.get("total_chapters", 0)
            arcs_summary.append({
                "id": a["arc_id"],
                "title": a["title"],
                "status": a["status"],
                "progress": f"{done}/{total}" if total else "未展开",
                "goal": a.get("goal", "")[:50],
            })

        return {
            "total_arcs": len(self._state["compass"]),
            "current_arc": self._state["current_arc"] + 1,
            "total_written": self._state["chapters_written"],
            "arcs": arcs_summary,
        }

    def update_chapter_plan(self, global_ch: int, **fields):
        """更新某章的规划字段（goal/core_event/hook_type）"""
        arc = self.get_current_arc()
        if not arc or not arc["chapters"]:
            return

        arc_offset = sum(
            a.get("total_chapters", 0) or 0
            for a in self._state["compass"][:self._state["current_arc"]]
        )
        arc_ch = global_ch - arc_offset

        for ch in arc["chapters"]:
            if ch["ch"] == arc_ch:
                for key, value in fields.items():
                    if key in ch:
                        ch[key] = value
                break

        self._save()
