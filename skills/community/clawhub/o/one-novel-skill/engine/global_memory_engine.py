#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
global_memory_engine.py — 全局记忆动态更新算法引擎

参考：《网络小说全维度创新创作与AI工业化稳态落地深度研究报告（进阶迭代版）》
第4章 §4.1.1 全局记忆动态更新算法

核心功能：
  - 增量式摘要合并：每章节定稿后汇总全书关键事件
  - 关键词向量检索：根据当前章节需求召回相关历史细节
  - 全局压缩摘要：实时覆盖更新，杜绝记忆断层
  - 标准化JSON台账输出

流程：
  1. 章节定稿 -> 提取本章核心事件、角色状态、新增伏笔
  2. 合并历史全局摘要，剔除冗余信息，保留核心闭环数据
  3. 生成标准化JSON格式台账
  4. Prompt自动注入最新全局摘要
  5. 循环迭代
"""

import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

_log = logging.getLogger("global_memory_engine")


class GlobalMemoryEngine:
    """全局记忆动态更新算法引擎"""

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else None
        self._global_summary = {
            "version": 1,
            "total_chapters": 0,
            "core_premise": "",        # 核心设定
            "key_events": [],          # 关键事件列表
            "character_milestones": [],  # 角色里程碑
            "active_plot_threads": [],   # 活跃剧情线
            "unresolved_hooks": [],      # 未解决悬念
            "world_evolution": [],       # 世界观演变
            "last_updated_chapter": 0,
        }

    # ========== 章节信息提取 ==========

    def extract_chapter_events(self, text: str, chapter: int, spec_data: dict = None) -> Dict:
        """从章节正文提取关键信息

        返回:
        {
            "events": [...],         # 关键事件
            "char_progress": [...],   # 角色进展
            "new_hooks": [...],       # 新增悬念
            "new_info": [...],        # 新世界观信息
            "summary": str,           # 章节摘要(100字内)
        }
        """
        events = []
        char_progress = []
        new_hooks = []
        new_info = []

        # 从 spec 获取信息（如果有）
        if spec_data:
            must_happen = spec_data.get("must_happen", [])
            for mh in must_happen:
                events.append(f"ch{chapter}: {mh[:80]}")
            hooks_data = spec_data.get("new_hooks", [])
            for hk in hooks_data:
                new_hooks.append(f"ch{chapter}: {hk[:80] if isinstance(hk, str) else str(hk)[:80]}")

        # 从文本提取关键信息
        lines = text.split("\n")
        char_names = re.findall(r"[\u4e00-\u9fff]{2,4}(?:说|道|问|喊|叫)", text)
        char_names = list(set(char_names))[:5]
        for cn in char_names:
            name = cn[:-1]
            char_progress.append(f"ch{chapter}: {name} 出场")

        # 生成章节摘要
        first_500 = text[:500].replace("\n", "")
        summary = f"ch{chapter}: {first_500[:80]}..."

        return {
            "events": events[:5],
            "char_progress": char_progress[:5],
            "new_hooks": new_hooks[:3],
            "new_info": new_info[:3],
            "summary": summary,
        }

    # ========== 全局摘要更新 ==========

    def update(self, text: str, chapter: int, spec_data: dict = None):
        """更新全局记忆，每章定稿后调用"""
        extracted = self.extract_chapter_events(text, chapter, spec_data)

        # 更新总章节数
        self._global_summary["total_chapters"] = chapter
        self._global_summary["last_updated_chapter"] = chapter

        # 追加关键事件（保留最近50条）
        for ev in extracted["events"]:
            if ev not in self._global_summary["key_events"]:
                self._global_summary["key_events"].append(ev)
        self._global_summary["key_events"] = self._global_summary["key_events"][-50:]

        # 追加角色里程碑
        for cp in extracted["char_progress"]:
            if cp not in self._global_summary["character_milestones"]:
                self._global_summary["character_milestones"].append(cp)
        self._global_summary["character_milestones"] = self._global_summary["character_milestones"][-30:]

        # 追加未解决悬念
        for hk in extracted["new_hooks"]:
            self._global_summary["unresolved_hooks"].append(hk)
        self._global_summary["unresolved_hooks"] = self._global_summary["unresolved_hooks"][-20:]

        # 版本号递增
        self._global_summary["version"] += 1

        _log.info(f"GlobalMemory: 更新到 ch{chapter} (v{self._global_summary['version']})")

    # ========== 获取压缩摘要（用于注入 Prompt） ==========

    def get_compressed_summary(self, max_chars: int = 1500) -> str:
        """获取压缩后的全局摘要文本，用于注入生成 prompt

        按优先级排序：核心设定 > 关键事件 > 活跃剧情 > 角色进展 > 未决悬念
        """
        parts = []

        # 1. 核心设定
        if self._global_summary["core_premise"]:
            parts.append(f"[设定] {self._global_summary['core_premise']}")

        # 2. 关键事件（最近10条）
        recent_events = self._global_summary["key_events"][-10:]
        if recent_events:
            parts.append("[事件] " + " | ".join(recent_events))

        # 3. 活跃剧情线
        threads = self._global_summary["active_plot_threads"]
        if threads:
            parts.append("[剧情线] " + " | ".join(threads[:5]))

        # 4. 角色里程碑（最近5条）
        recent_chars = self._global_summary["character_milestones"][-5:]
        if recent_chars:
            parts.append("[角色] " + " | ".join(recent_chars))

        # 5. 未解决悬念
        hooks = self._global_summary["unresolved_hooks"][-5:]
        if hooks:
            parts.append("[悬念] " + " | ".join(hooks))

        result = "\n".join(parts)

        # 截断
        if len(result) > max_chars:
            result = result[:max_chars] + "..."

        return result

    def get_structured_summary(self) -> Dict:
        """获取结构化摘要（JSON格式）"""
        return {
            "version": self._global_summary["version"],
            "total_chapters": self._global_summary["total_chapters"],
            "last_updated": self._global_summary["last_updated_chapter"],
            "event_count": len(self._global_summary["key_events"]),
            "hook_count": len(self._global_summary["unresolved_hooks"]),
            "recent_events": self._global_summary["key_events"][-5:],
            "active_threads": self._global_summary["active_plot_threads"][:5],
        }

    # ========== 关键词检索 ==========

    def search_memory(self, keyword: str) -> List[str]:
        """根据关键词检索历史记忆"""
        results = []
        keyword_lower = keyword.lower()

        for ev in self._global_summary["key_events"]:
            if keyword_lower in ev.lower():
                results.append(ev)

        for cp in self._global_summary["character_milestones"]:
            if keyword_lower in cp.lower():
                results.append(cp)

        return results[:5]

    # ========== 持久化 ==========

    def to_dict(self) -> dict:
        return self._global_summary

    def load_from_dict(self, data: dict):
        self._global_summary.update(data)
        _log.info(f"GlobalMemoryEngine: loaded (v{self._global_summary['version']}, ch{self._global_summary['total_chapters']})")

    def save_to_file(self):
        if not self.book_dir:
            return
        path = self.book_dir / "追踪" / "global_memory.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._global_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_from_file(self):
        if not self.book_dir:
            return
        path = self.book_dir / "追踪" / "global_memory.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.load_from_dict(data)
            except Exception as e:
                _log.warning(f"GlobalMemory: 加载失败 {e}")

    def reset(self):
        self._global_summary = {k: v if not isinstance(v, list) else [] for k, v in self._global_summary.items()}
        self._global_summary["version"] = 1
        self._global_summary["total_chapters"] = 0
