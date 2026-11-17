#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_preferences.py — 用户偏好持久化系统

灵感来源: chinese-novelist-skill 的 user-preferences.json 模式
核心思想: 跨会话持久化用户偏好，渐进式学习用户习惯，影响每次交互。

用法:
  up = UserPreferences(book_dir)
  up.record("platform", "番茄")         # 记录偏好
  up.record("style", "快节奏")          # 自动增加计数
  up.get_preferred("platform")          # 获取最常用的选择
  up.get_summary()                      # 获取偏好摘要
"""

import json, logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import Counter

_log = logging.getLogger("user_preferences")


class UserPreferences:
    """用户偏好持久化系统"""

    def __init__(self, book_dir: str = ""):
        self._path = Path(book_dir) / "追踪" / "用户偏好.json" if book_dir else None
        self._data = self._load()

    def _load(self) -> dict:
        if self._path and self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "platform": {},       # 平台偏好 {"番茄": 5, "起点": 2}
            "genre": {},          # 题材偏好
            "style": {},          # 风格偏好
            "word_count": {},     # 字数偏好
            "names": [],          # 常用角色名
            "phrases": [],        # 常用短语/口头禅
            "custom_rules": [],   # 用户自定义规则
            "session_count": 0,
            "total_chapters": 0,
            "last_session": "",
        }

    def _save(self):
        if not self._path:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def record(self, category: str, value: str, weight: int = 1):
        """记录一次用户偏好

        Args:
            category: 分类 (platform/genre/style/word_count)
            value: 偏好值
            weight: 权重（默认为1）
        """
        if category not in self._data:
            self._data[category] = {}

        if isinstance(self._data[category], dict):
            self._data[category][value] = self._data[category].get(value, 0) + weight
        elif isinstance(self._data[category], list):
            if value not in self._data[category]:
                self._data[category].append(value)

        self._save()
        _log.debug(f"Preference: {category}={value} (+{weight})")

    def get_preferred(self, category: str) -> Optional[str]:
        """获取最常用的偏好值"""
        data = self._data.get(category, {})
        if isinstance(data, dict) and data:
            return max(data, key=data.get)
        if isinstance(data, list) and data:
            return data[-1]  # 返回最近添加的
        return None

    def get_top(self, category: str, n: int = 3) -> List[tuple]:
        """获取 Top N 偏好"""
        data = self._data.get(category, {})
        if isinstance(data, dict):
            return sorted(data.items(), key=lambda x: -x[1])[:n]
        return []

    def get_summary(self) -> Dict[str, Any]:
        """获取偏好摘要（用于注入生成 prompt）"""
        summary = {}
        for cat in ["platform", "genre", "style", "word_count"]:
            pref = self.get_preferred(cat)
            if pref:
                summary[cat] = pref
        return summary

    def add_character_name(self, name: str):
        """记录常用角色名"""
        if name not in self._data["names"]:
            self._data["names"].append(name)
            if len(self._data["names"]) > 50:
                self._data["names"] = self._data["names"][-50:]
            self._save()

    def add_phrase(self, phrase: str):
        """记录常用短语"""
        if phrase not in self._data["phrases"]:
            self._data["phrases"].append(phrase)
            if len(self._data["phrases"]) > 100:
                self._data["phrases"] = self._data["phrases"][-100:]
            self._save()

    def add_custom_rule(self, rule: str):
        """添加用户自定义规则"""
        self._data["custom_rules"].append({
            "rule": rule,
            "added": datetime.now().isoformat(),
        })
        self._save()

    def get_custom_rules(self) -> List[str]:
        """获取所有自定义规则"""
        return [r["rule"] for r in self._data["custom_rules"]]

    def start_session(self):
        """标记新会话开始"""
        self._data["session_count"] += 1
        self._data["last_session"] = datetime.now().isoformat()
        self._save()

    def add_chapter_count(self, count: int = 1):
        """增加写作章节计数"""
        self._data["total_chapters"] += count
        self._save()

    def get_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        return {
            "session_count": self._data["session_count"],
            "total_chapters": self._data["total_chapters"],
            "last_session": self._data["last_session"],
            "preferred_platform": self.get_preferred("platform"),
            "preferred_genre": self.get_preferred("genre"),
            "preferred_style": self.get_preferred("style"),
        }
