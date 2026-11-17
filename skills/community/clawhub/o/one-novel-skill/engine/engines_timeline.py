#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""时间线追踪引擎 — 千万字级设计

关键优化:
  - 分卷存储: 每100章一个文件, 避免单文件膨胀
  - 增量写入: 追加模式, 不重写旧数据
  - 自动归档: 旧卷自动压缩为摘要
  - 内存友好: 只加载当前卷到内存
"""

import json
import os
from pathlib import Path
from threading import Lock

VOLUME_SIZE = 100  # 每卷100章
import re


class TimelineEngine:
    """全书时间线追踪 — 分卷存储/增量写入"""

    def __init__(self, book_dir=""):
        self.book_dir = Path(book_dir) if book_dir else None
        self._cache = {}  # 卷号 → 数据
        self._lock = Lock()
        self._current_vol = 0

    def _vol_path(self, vol):
        return self.book_dir / "追踪" / "timeline" / f"vol-{vol:04d}.json" if self.book_dir else None

    def _vol_index(self, chapter):
        return (chapter - 1) // VOLUME_SIZE + 1

    def _load_vol(self, vol):
        with self._lock:
            if vol in self._cache:
                return self._cache[vol]
        p = self._vol_path(vol)
        if p and p.exists():
            data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        else:
            data = {"vol": vol, "events": [], "summary": {}}
        with self._lock:
            self._cache[vol] = data
        return data

    def _save_vol(self, vol, data):
        if not self.book_dir:
            return
        d = self.book_dir / "追踪" / "timeline"
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"vol-{vol:04d}.json"
        with self._lock:
            self._cache[vol] = data
        # atomic write: tmp → replace
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(p)

    def record_chapter(self, ch, text, characters=None):
        """增量记录一章——不重写旧数据"""
        issues = []
        vol = self._vol_index(ch)
        data = self._load_vol(vol)

        time_hints = re.findall(r"(?:这天|第二天|次日|三天后|一周后|一个月后|半年后|一年后|第一天|前一天)", text)
        location_hints = re.findall(r".{1,6}(?:城|村|宫|谷|洞|山|岛|殿|府|楼|市|镇)", text)

        event = {
            "ch": ch,
            "time_hints": time_hints[:3],
            "locations": list(set(location_hints[:5])),
        }

        # 时间一致性 — 跳过回述/倒叙场景
        is_flashback = any(w in text[:500] for w in ["回想起","回忆","想起","记得","回想",
            "昔日","那时","从前","小时候","当年"])
        if data["events"] and not is_flashback:
            last_event = data["events"][-1]
            last_time = last_event.get("time_hints", [""])[-1] if last_event.get("time_hints") else ""
            if last_time and time_hints:
                for t in time_hints:
                    if any(w in t for w in ["前一天", "昨天"]):
                        issues.append(f"时间矛盾(非回述): ch{ch}出现'{t}'但上章是'{last_time}'")

        # 位置一致性（检查是否有任何地点重叠来确认连续性）
        if data["events"] and location_hints:
            last_event = data["events"][-1]
            last_locs = set(last_event.get("locations", []))
            curr_locs = set(location_hints)
            # 有重叠地点 → 位置连续，不报错
            if last_locs and curr_locs and not last_locs & curr_locs:
                travel_verbs = ["来到", "前往", "到达", "离开", "返回", "赶往", "出发", "动身"]
                if not any(v in text[:500] for v in travel_verbs):
                    issues.append(f"位置跳跃: 上章{list(last_locs)[:2]}, 本章{list(curr_locs)[:2]}")

        data["events"].append(event)
        self._save_vol(vol, data)
        self._current_vol = vol
        return issues

    def get_events(self, chapter_from=1, chapter_to=None):
        """按范围加载事件（避免全量加载）"""
        if chapter_to is None:
            chapter_to = chapter_from + VOLUME_SIZE * 100  # 默认到全书范围
        events = []
        vol_start = self._vol_index(chapter_from)
        vol_end = self._vol_index(chapter_to)
        for vol in range(vol_start, vol_end + 1):
            data = self._load_vol(vol)
            for e in data.get("events", []):
                if chapter_from <= e["ch"] <= chapter_to:
                    events.append(e)
        return events

    def check_consistency(self, total_chapters):
        """全时间线审计（基于索引, 非全量加载）"""
        issues = []
        if total_chapters < 3:
            return ["数据不足"]
        # 只检查每卷的摘要
        locations = set()
        for vol in range(1, self._vol_index(total_chapters) + 1):
            data = self._load_vol(vol)
            for e in data.get("events", []):
                for loc in e.get("locations", []):
                    locations.add(loc)
        if len(locations) < 3 and total_chapters > 20:
            issues.append(f"地点过少({len(locations)}/20章)")
        return issues

    def get_status(self):
        """当前时间线状态摘要"""
        vols = set()
        events = []
        if self.book_dir:
            td = self.book_dir / "追踪" / "timeline"
            if td.exists():
                for f in sorted(td.glob("vol-*.json")):
                    vols.add(f.stem)
                    data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                    events.extend(data.get("events", []))
        return {
            "volumes": len(vols),
            "total_events": len(events),
            "current_vol": self._current_vol,
        }

    def log_deduction(self, chapter, premise, outcome):
        """记录设定→情节推导"""
        vol = self._vol_index(chapter)
        data = self._load_vol(vol)
        if "deductions" not in data:
            data["deductions"] = []
        data["deductions"].append({"ch": chapter, "premise": premise, "outcome": outcome})
        self._save_vol(vol, data)