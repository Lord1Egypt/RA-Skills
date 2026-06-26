#!/usr/bin/env python3
"""v2 迁移脚本：添加 display_id + 自动进展记录"""

from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.db import Database

def migrate():
    db = Database()
    db.init_db()

    # 1. 添加 display_id 列
    try:
        db.execute("ALTER TABLE tasks ADD COLUMN display_id TEXT")
        print("✅ 添加 display_id 列")
    except Exception as e:
        if "duplicate column" in str(e).lower():
            print("⏭️  display_id 列已存在")
        else:
            raise

    # 2. 为已有任务生成 display_id（按 created_at 分配当天序号）
    tasks = db.fetch_all(
        "SELECT id, created_at FROM tasks WHERE display_id IS NULL ORDER BY created_at ASC",
        ()
    )
    day_counters = {}
    for t in tasks:
        day = t["created_at"][:10].replace("-", "")
        day_counters[day] = day_counters.get(day, 0) + 1
        display_id = f"{day}-{day_counters[day]:03d}"
        db.execute("UPDATE tasks SET display_id = ? WHERE id = ?", (display_id, t["id"]))

    print(f"✅ 为 {len(tasks)} 个已有任务生成 display_id")

    # 3. 创建唯一索引
    try:
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_display_id ON tasks(display_id)")
        print("✅ 创建 display_id 唯一索引")
    except Exception as e:
        print(f"⚠️  索引创建: {e}")

    print("\n🎉 v2 迁移完成")
    return tasks

if __name__ == "__main__":
    migrate()
