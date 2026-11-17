#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
session_state.py — WAL协议 + 三文件进度系统

灵感来源: planning-with-files + proactive-agent 的 WAL 协议
核心思想: 写作前先写状态，防止上下文丢失后遗忘当前进度。

三文件系统:
  SESSION-STATE.md — 当前会话状态（Hot RAM）
  PROGRESS.md       — 进度日志
  LEARNINGS.md      — 写作经验积累

用法:
  ss = SessionState(book_dir)
  ss.write_checkpoint(chapter, state, notes)  # WAL: 写前记录
  ss.log_progress(action, result)             # 进度日志
  ss.record_learning(insight, category)       # 经验积累
"""

import json, logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

_log = logging.getLogger("session_state")


class SessionState:
    """WAL协议 + 三文件进度系统"""

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self._track_dir = self.book_dir / "追踪"
        self._track_dir.mkdir(parents=True, exist_ok=True)

    # ── WAL 协议: 写前记录 ──

    def write_checkpoint(self, chapter: int, state: dict, notes: str = ""):
        """WAL协议核心: 在写章节之前先保存当前状态

        Args:
            chapter: 当前章节号
            state: 当前状态快照 (角色位置/情绪/伏笔进度)
            notes: 备注
        """
        content = f"""# 写作检查点 — 第{chapter}章

> 自动保存时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 当前状态

```json
{json.dumps(state, ensure_ascii=False, indent=2)}
```

## 备注

{notes if notes else "（无）"}

## 5-Question Reboot Test

如果中断后恢复，回答以下问题即可继续：
1. **位置**: 正在写第{chapter}章
2. **目标**: 本章核心目标是什么？
3. **状态**: 角色当前在哪？什么状态？
4. **伏笔**: 哪些伏笔需要在本章推进？
5. **钩子**: 上章结尾的钩子是什么？
"""
        path = self._track_dir / "SESSION-STATE.md"
        path.write_text(content, encoding="utf-8")
        _log.debug(f"WAL: checkpoint ch{chapter} written")

    def read_checkpoint(self) -> Optional[Dict[str, Any]]:
        """读取最近检查点，用于中断恢复"""
        path = self._track_dir / "SESSION-STATE.md"
        if not path.exists():
            return None

        text = path.read_text(encoding="utf-8")
        # 简单解析
        result = {"raw": text}

        # 提取章节号
        import re
        m = re.search(r"第(\d+)章", text)
        if m:
            result["chapter"] = int(m.group(1))

        # 提取 JSON 状态
        m = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
        if m:
            try:
                result["state"] = json.loads(m.group(1))
            except Exception:
                pass

        return result

    # ── 进度日志 ──

    def log_progress(self, action: str, result: str, chapter: int = 0):
        """记录操作到进度日志

        Args:
            action: 操作类型 (generate/detect/revise/review)
            result: 结果摘要
            chapter: 章节号
        """
        path = self._track_dir / "PROGRESS.md"
        timestamp = datetime.now().strftime("%m-%d %H:%M")

        entry = f"| {timestamp} | {action:8s} | 第{chapter:03d}章 | {result} |\n"

        if not path.exists():
            header = "| 时间 | 操作 | 章节 | 结果 |\n|------|------|------|------|\n"
            path.write_text(header + entry, encoding="utf-8")
        else:
            with open(path, "a", encoding="utf-8") as f:
                f.write(entry)

    def get_progress_summary(self) -> dict:
        """获取进度摘要"""
        path = self._track_dir / "PROGRESS.md"
        if not path.exists():
            return {"total_actions": 0, "chapters": []}

        lines = path.read_text(encoding="utf-8").split("\n")
        actions = [l for l in lines if l.startswith("| ") and "第" in l]
        chapters_seen = set()
        for line in actions:
            import re
            m = re.search(r"第(\d+)章", line)
            if m:
                chapters_seen.add(int(m.group(1)))

        return {
            "total_actions": len(actions),
            "chapters": sorted(chapters_seen),
            "last_action": actions[-1].strip("| ") if actions else "",
        }

    # ── 经验积累 ──

    def record_learning(self, insight: str, category: str = "general"):
        """记录写作经验（灵感来源: self-improving-agent）

        Args:
            insight: 经验/教训/发现
            category: 分类 (character/plot/dialogue/pacing/ai_removal/other)
        """
        path = self._track_dir / "LEARNINGS.md"
        timestamp = datetime.now().strftime("%Y-%m-%d")

        entry_id = f"LRN-{timestamp.replace('-', '')}-{hash(insight) % 10000:04d}"

        entry = f"""
### [{entry_id}] {category}

{insight}

*记录时间: {timestamp}*
---
"""

        if not path.exists():
            path.write_text(f"# 写作经验积累\n\n> 灵感来源: self-improving-agent 的 .learnings/ 模式\n\n{entry}", encoding="utf-8")
        else:
            with open(path, "a", encoding="utf-8") as f:
                f.write(entry)

        _log.info(f"Learning recorded: [{entry_id}] {category}")

    def get_recent_learnings(self, limit: int = 5) -> List[str]:
        """获取最近的经验"""
        path = self._track_dir / "LEARNINGS.md"
        if not path.exists():
            return []

        text = path.read_text(encoding="utf-8")
        # 按 LRN 条目分割
        entries = text.split("### [LRN-")
        results = []
        for entry in entries[1:]:  # 跳过头部
            lines = entry.strip().split("\n")
            # 提取分类后的第一段非空文字
            content = []
            started = False
            for line in lines:
                if not started and line and not line.startswith("*"):
                    started = True
                if started:
                    if line.startswith("*记录时间"):
                        break
                    if line.strip():
                        content.append(line.strip())
            if content:
                results.append(" ".join(content))
        return results[-limit:]
