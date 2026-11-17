#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线任务队列（M1）——对话间隙自动跑的地基

设计：
- 纯本地文件队列，零外部依赖；任务就是一个 JSON 文件
- 状态机：pending → running → done / failed（可重试，超过次数进死信）
- 对话间隙由 pipeline/runner.py 调用 run_idle() 排空队列，任务量可控（max_tasks）

目录：<data_dir>/pipeline/queue/
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/pipeline/queue.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class TaskQueue:
    """本地文件任务队列"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.queue_dir = self.data_dir / "pipeline" / "queue"
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    # ---------- 基础 IO ----------

    def _path(self, task_id: str) -> Path:
        return self.queue_dir / f"{task_id}.json"

    def _load(self, task_id: str) -> Optional[Dict[str, Any]]:
        data = read_json(self._path(task_id), None)
        return data if isinstance(data, dict) else None

    def _save(self, task: Dict[str, Any]) -> None:
        write_json(self._path(task["id"]), task)

    def all(self) -> List[Dict[str, Any]]:
        tasks = []
        for p in sorted(self.queue_dir.glob("*.json")):
            if p.name.startswith("."):
                continue  # 原子写的临时残件
            data = read_json(p, None)
            if isinstance(data, dict):
                tasks.append(data)
        return tasks

    # ---------- 生命周期 ----------

    def enqueue(self, kind: str, payload: Dict[str, Any], priority: int = 5,
                max_attempts: int = 3) -> str:
        """入队一个离线任务

        Args:
            kind: 任务类型，对应 runner 中注册的 handler
            payload: 任务数据（只放必要字段，绝不放大段原始上下文）
            priority: 数字越小越先执行
        """
        task_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        task = {
            "id": task_id,
            "kind": kind,
            "payload": payload,
            "priority": priority,
            "status": "pending",
            "attempts": 0,
            "max_attempts": max_attempts,
            "created_at": _now(),
            "updated_at": _now(),
            "last_error": "",
            "result": None,
        }
        self._save(task)
        return task_id

    def pending(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """待执行任务（优先级 → 创建时间）"""
        items = [t for t in self.all() if t.get("status") == "pending"]
        items.sort(key=lambda t: (t.get("priority", 5), t.get("created_at", "")))
        return items[:limit] if limit else items

    def claim(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = self._load(task_id)
        if not task or task["status"] != "pending":
            return None
        task["status"] = "running"
        task["attempts"] += 1
        task["updated_at"] = _now()
        self._save(task)
        return task

    def complete(self, task_id: str, result: Any = None) -> bool:
        task = self._load(task_id)
        if not task:
            return False
        task["status"] = "done"
        task["result"] = result
        task["updated_at"] = _now()
        self._save(task)
        return True

    def fail(self, task_id: str, error: str) -> bool:
        """失败一次；超过 max_attempts 转为 dead"""
        task = self._load(task_id)
        if not task:
            return False
        task["last_error"] = str(error)[:500]
        if task.get("attempts", 0) >= task.get("max_attempts", 3):
            task["status"] = "dead"
        else:
            task["status"] = "pending"  # 放回队列，等下一次间隙重试
        task["updated_at"] = _now()
        self._save(task)
        return True

    # ---------- 维护 ----------

    def purge(self, statuses=("done", "dead"), keep_recent: int = 50) -> int:
        """清理终态任务，保留最近 keep_recent 条，返回清理数量"""
        finished = [t for t in self.all() if t.get("status") in statuses]
        finished.sort(key=lambda t: t.get("updated_at", ""), reverse=True)
        removed = 0
        for task in finished[keep_recent:]:
            p = self._path(task["id"])
            if p.exists():
                p.unlink()
                removed += 1
        return removed

    def stats(self) -> Dict[str, int]:
        counter: Dict[str, int] = {}
        for t in self.all():
            counter[t.get("status", "?")] = counter.get(t.get("status", "?"), 0) + 1
        return counter


if __name__ == "__main__":
    import sys
    q = TaskQueue()
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(q.stats(), ensure_ascii=False))
    else:
        print(json.dumps({"pending": len(q.pending()), "stats": q.stats()}, ensure_ascii=False))
