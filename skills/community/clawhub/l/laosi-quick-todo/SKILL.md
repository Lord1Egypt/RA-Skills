---
name: quick-todo
version: 1.0.0
description: 待办清单 - 最轻的任务管理，语音添加、划掉完成、进度统计、优先级排序，本地JSON存储
tags: [todo, tasks, productivity, gtd, daily-life, kanban]
author: laosi
source: original
---

# Quick Todo - 待办清单

> 激活词: 待办 / 任务 / todo / 加一个任务

## 功能

- 语音/文字快速添加任务
- 标记完成 / 删除任务
- 优先级排序（high / medium / low）
- 进度统计（完成/待办/总数）
- 本地 JSON 持久化

## Python 实现

```python
import os, json
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "quick_tasks.json")

class QuickTodo:
    def __init__(self):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        self.tasks = self._load()
    
    def _load(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add(self, task: str, priority: str = "medium", due: str = None) -> dict:
        """添加新任务"""
        item = {
            "id": len(self.tasks) + 1,
            "task": task,
            "priority": priority,
            "done": False,
            "created": datetime.now().isoformat(),
            "due": due,
            "completed_at": None
        }
        self.tasks.append(item)
        self._save()
        return item
    
    def done(self, task_id: int) -> bool:
        """标记完成"""
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = True
                t["completed_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False
    
    def delete(self, task_id: int) -> bool:
        """删除任务"""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < before:
            self._save()
            return True
        return False
    
    def list(self, filter_done: bool = None, priority: str = None) -> list:
        """查看任务，支持筛选"""
        results = self.tasks
        if filter_done is not None:
            results = [t for t in results if t["done"] == filter_done]
        if priority:
            results = [t for t in results if t["priority"] == priority]
        # 排序：待办优先、高优先级优先
        results.sort(key=lambda t: (
            t["done"],
            {"high": 0, "medium": 1, "low": 2}.get(t["priority"], 3),
            t["created"]
        ))
        return results
    
    def stats(self) -> dict:
        """进度统计"""
        total = len(self.tasks)
        done_count = sum(1 for t in self.tasks if t["done"])
        pending = total - done_count
        return {
            "total": total,
            "done": done_count,
            "pending": pending,
            "progress": f"{done_count}/{total}",
            "pct": round(done_count / total * 100, 1) if total > 0 else 0
        }

# 使用示例
todo = QuickTodo()
todo.add("学习Transformer架构", priority="high")
todo.add("写周报", priority="medium", due="2026-05-30")
todo.add("整理书签", priority="low")

# 查看待办
for t in todo.list(filter_done=False):
    pri = {"high": "🔴", "medium": "🟡", "low": "⚪"}[t["priority"]]
    print(f"[{t['id']}] {pri} {t['task']}")

# 标记完成
todo.done(1)

# 查看统计
s = todo.stats()
print(f"进度: {s['done']}/{s['total']} ({s['pct']}%)")
```

## 命令行用法

```bash
# 添加一个高优先级任务
python -c "from quick_todo import QuickTodo; QuickTodo().add('读FlashAttention论文', priority='high')"

# 标记完成
python -c "from quick_todo import QuickTodo; QuickTodo().done(1)"

# 查看统计
python -c "from quick_todo import QuickTodo; print(QuickTodo().stats())"
```

## 数据格式

```json
[
  {
    "id": 1,
    "task": "学习Transformer架构",
    "priority": "high",
    "done": true,
    "created": "2026-05-28T10:00:00",
    "due": null,
    "completed_at": "2026-05-28T11:30:00"
  }
]
```

## 使用场景

1. **日常任务**: 早上列今天要做的事，做完一条说一声
2. **购物清单**: 去超市前快速列清单
3. **项目追踪**: 拆分大任务为小步骤，逐项攻克
4. **GTD工作流**: 收集→整理→执行 的轻量实现

## 依赖

- Python 3.8+
- 无第三方依赖
