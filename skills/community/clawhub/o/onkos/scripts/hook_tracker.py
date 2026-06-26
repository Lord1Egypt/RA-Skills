#!/usr/bin/env python3
"""
伏笔追踪器 - 基于 SQLite 的伏笔/悬念管理
数据存储在 novel_memory.db 的 hooks 表中
支持: 种埋、收线、遗忘预警、超期统计、强度/紧迫度/部分回收
"""

import os
import json
import sqlite3
import argparse
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class HookTracker:
    """伏笔追踪器 - SQLite 存储"""

    def __init__(self, db_path: str):
        """
        初始化伏笔追踪器

        Args:
            db_path: SQLite 数据库路径（与 MemoryEngine 共享 novel_memory.db）
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_tables()

    def _ensure_tables(self):
        """确保所需表存在（支持独立使用，无需依赖 MemoryEngine 先建表）"""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hooks (
                id TEXT PRIMARY KEY,
                desc TEXT NOT NULL,
                planted_chapter INTEGER NOT NULL,
                expected_resolve INTEGER,
                resolved_chapter INTEGER,
                resolution TEXT,
                status TEXT DEFAULT 'open',
                priority TEXT DEFAULT 'normal',
                tags TEXT DEFAULT '[]',
                related_characters TEXT DEFAULT '[]',
                strength REAL DEFAULT 0.5,
                urgency REAL DEFAULT 1.0,
                partial_count INTEGER DEFAULT 0,
                last_hint_chapter INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        # 为已有表添加新列（兼容旧库）
        new_cols = [
            ("strength", "REAL DEFAULT 0.5"),
            ("urgency", "REAL DEFAULT 1.0"),
            ("partial_count", "INTEGER DEFAULT 0"),
            ("last_hint_chapter", "INTEGER"),
        ]
        for col_name, col_type in new_cols:
            try:
                cur.execute(f"ALTER TABLE hooks ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass  # 列已存在

        cur.execute("CREATE INDEX IF NOT EXISTS idx_hooks_status ON hooks(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_hooks_priority ON hooks(priority)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_hooks_planted ON hooks(planted_chapter)")
        self.conn.commit()

    def plant(self, desc: str, planted_chapter: int,
              expected_resolve: int = None, priority: str = "normal",
              tags: List[str] = None, related_characters: List[str] = None,
              hook_id: str = None, strength: float = 0.5) -> str:
        """
        种埋伏笔（自动检测重复：同描述的open伏笔已存在时返回已有ID）

        Args:
            desc: 伏笔描述
            planted_chapter: 种埋章节
            expected_resolve: 预期收线章节
            priority: 优先级（critical / normal / minor）
            tags: 标签列表
            related_characters: 关联角色列表
            hook_id: 自定义ID
            strength: 伏笔强度(0-1)，由智能体评估，默认0.5

        Returns:
            伏笔ID
        """
        # 重复检测：同描述的open伏笔已存在时直接返回
        existing = self.conn.execute(
            "SELECT id FROM hooks WHERE desc = ? AND status = 'open'", (desc,)
        ).fetchone()
        if existing:
            return existing["id"]

        if not hook_id:
            hook_id = f"hook_{uuid.uuid4().hex[:8]}"

        now = datetime.now().isoformat()
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        chars_json = json.dumps(related_characters or [], ensure_ascii=False)
        strength = max(0.0, min(1.0, strength))

        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO hooks (id, desc, planted_chapter, expected_resolve,
                resolved_chapter, resolution, status, priority, tags,
                related_characters, strength, urgency, partial_count,
                last_hint_chapter, created_at, updated_at)
            VALUES (?, ?, ?, ?, NULL, NULL, 'open', ?, ?, ?, ?, 1.0, 0, NULL, ?, ?)
        """, (hook_id, desc, planted_chapter, expected_resolve, priority,
              tags_json, chars_json, strength, now, now))
        self.conn.commit()
        return hook_id

    def resolve(self, hook_id: str, resolved_chapter: int, resolution: str = "") -> bool:
        """
        收线伏笔

        Args:
            hook_id: 伏笔ID
            resolved_chapter: 收线章节
            resolution: 收线描述
        """
        # 不允许重复resolve已resolved的伏笔
        cur = self.conn.cursor()
        cur.execute("SELECT status FROM hooks WHERE id=?", (hook_id,))
        row = cur.fetchone()
        if not row:
            return False
        if row['status'] == 'resolved':
            return False  # 已回收，不覆盖

        now = datetime.now().isoformat()
        cur.execute("""
            UPDATE hooks
            SET resolved_chapter = ?, resolution = ?, status = 'resolved',
                updated_at = ?
            WHERE id = ? AND status != 'resolved'
        """, (resolved_chapter, resolution, now, hook_id))
        self.conn.commit()
        return cur.rowcount > 0

    def partial_resolve(self, hook_id: str, hint_chapter: int) -> bool:
        """
        部分回收伏笔（increment partial_count, update last_hint_chapter）

        Args:
            hook_id: 伏笔ID
            hint_chapter: 暗示/部分回收所在章节

        Returns:
            是否成功
        """
        cur = self.conn.cursor()
        cur.execute("SELECT status FROM hooks WHERE id=?", (hook_id,))
        row = cur.fetchone()
        if not row or row['status'] != 'open':
            return False

        now = datetime.now().isoformat()
        cur.execute("""
            UPDATE hooks
            SET partial_count = partial_count + 1,
                last_hint_chapter = ?,
                updated_at = ?
            WHERE id = ? AND status = 'open'
        """, (hint_chapter, now, hook_id))
        self.conn.commit()
        return cur.rowcount > 0

    def hint(self, hook_id: str, hint_chapter: int) -> bool:
        """
        暗示提及伏笔（仅更新last_hint_chapter，不增加partial_count）

        Args:
            hook_id: 伏笔ID
            hint_chapter: 暗示提及的章节

        Returns:
            是否成功
        """
        cur = self.conn.cursor()
        cur.execute("SELECT status FROM hooks WHERE id=?", (hook_id,))
        row = cur.fetchone()
        if not row or row['status'] != 'open':
            return False

        now = datetime.now().isoformat()
        cur.execute("""
            UPDATE hooks
            SET last_hint_chapter = ?,
                updated_at = ?
            WHERE id = ? AND status = 'open'
        """, (hint_chapter, now, hook_id))
        self.conn.commit()
        return cur.rowcount > 0

    def update_strength(self, hook_id: str, strength: float) -> bool:
        """
        更新伏笔强度

        Args:
            hook_id: 伏笔ID
            strength: 新强度值(0-1)
        """
        strength = max(0.0, min(1.0, strength))
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE hooks SET strength = ?, updated_at = ? WHERE id = ?
        """, (strength, now, hook_id))
        self.conn.commit()
        return cur.rowcount > 0

    def compute_urgency(self, current_chapter: int) -> List[Dict[str, Any]]:
        """
        批量计算所有open伏笔的衰减urgency并更新

        Urgency公式:
        - base = strength * (1 + 0.2 * partial_count)
        - elapsed = current_chapter - planted_chapter
        - 若超期: urgency = base * (1 + 0.5 * (elapsed - expected_window) / 10)
        - 若未超期: urgency = base * max(0.3, 1.0 - elapsed * 0.02)
        - Clamp to [0, 5.0]

        Args:
            current_chapter: 当前章节

        Returns:
            更新后的伏笔列表（含计算后的urgency）
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, strength, partial_count, planted_chapter, expected_resolve
            FROM hooks WHERE status = 'open'
        """)
        updated = []
        now = datetime.now().isoformat()
        for row in cur.fetchall():
            strength = row["strength"] or 0.5
            partial_count = row["partial_count"] or 0
            planted = row["planted_chapter"]
            expected = row["expected_resolve"]

            base = strength * (1.0 + 0.2 * partial_count)
            elapsed = max(0, current_chapter - planted)

            if expected is not None and expected > planted:
                expected_window = expected - planted
                if elapsed > expected_window:
                    overdue_ratio = (elapsed - expected_window) / max(expected_window, 1)
                    urgency = base * (1.0 + 0.5 * overdue_ratio)
                else:
                    urgency = base * max(0.3, 1.0 - elapsed * 0.02)
            else:
                urgency = base * max(0.3, 1.0 - elapsed * 0.02)

            urgency = max(0.0, min(5.0, round(urgency, 3)))
            self.conn.execute(
                "UPDATE hooks SET urgency = ?, updated_at = ? WHERE id = ?",
                (urgency, now, row["id"])
            )
            updated.append({"id": row["id"], "urgency": urgency})

        self.conn.commit()
        return updated

    def abandon(self, hook_id: str, reason: str = "") -> bool:
        """放弃伏笔"""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE hooks
            SET status = 'abandoned', resolution = ?, updated_at = ?
            WHERE id = ?
        """, (reason, now, hook_id))
        self.conn.commit()
        return cur.rowcount > 0

    def abandon_chapter_hooks(self, chapter: int, reason: str = "章节修订") -> int:
        """
        放弃指定章节种埋的open伏笔（用于修订章节时清理旧伏笔）

        Args:
            chapter: 种埋章节
            reason: 放弃原因

        Returns:
            放弃的伏笔数量
        """
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE hooks
            SET status = 'abandoned', resolution = ?, updated_at = ?
            WHERE planted_chapter = ? AND status = 'open'
        """, (reason, now, chapter))
        count = cur.rowcount
        self.conn.commit()
        return count

    def get_open_hooks(self, current_chapter: int = None,
                       priority: str = None) -> List[Dict[str, Any]]:
        """获取未收线的伏笔"""
        cur = self.conn.cursor()
        sql = "SELECT * FROM hooks WHERE status = 'open'"
        params = []

        if priority:
            sql += " AND priority = ?"
            params.append(priority)

        if current_chapter is not None:
            # 优先显示即将到期和已超期的
            sql += " ORDER BY CASE WHEN expected_resolve IS NOT NULL AND expected_resolve < ? THEN 0 ELSE 1 END, priority, planted_chapter"
            params.append(current_chapter)
        else:
            sql += " ORDER BY priority, planted_chapter"

        cur.execute(sql, params)
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["related_characters"] = json.loads(r.get("related_characters", "[]"))
            results.append(r)
        return results

    def get_overdue_hooks(self, current_chapter: int) -> List[Dict[str, Any]]:
        """获取超期未收的伏笔（含urgency信息）"""
        # 先计算urgency
        self.compute_urgency(current_chapter)

        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM hooks
            WHERE status = 'open'
            AND expected_resolve IS NOT NULL
            AND expected_resolve < ?
            ORDER BY urgency DESC, expected_resolve
        """, (current_chapter,))
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["related_characters"] = json.loads(r.get("related_characters", "[]"))
            results.append(r)
        return results

    def get_forgotten_hooks(self, current_chapter: int, threshold: int = 100) -> List[Dict[str, Any]]:
        """获取可能被遗忘的伏笔（种埋很久但未收线且近期未提及）"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM hooks
            WHERE status = 'open'
            AND planted_chapter < ?
            ORDER BY planted_chapter
        """, (max(1, current_chapter - threshold),))
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["related_characters"] = json.loads(r.get("related_characters", "[]"))
            # 追加遗忘风险评估
            last_hint = r.get("last_hint_chapter")
            if last_hint is None:
                r["forget_risk"] = "high"
            elif current_chapter - last_hint > 20:
                r["forget_risk"] = "high"
            elif current_chapter - last_hint > 10:
                r["forget_risk"] = "medium"
            else:
                r["forget_risk"] = "low"
            results.append(r)
        return results

    def get_hook(self, hook_id: str) -> Optional[Dict[str, Any]]:
        """获取单个伏笔"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM hooks WHERE id = ?", (hook_id,))
        row = cur.fetchone()
        if not row:
            return None
        r = dict(row)
        r["tags"] = json.loads(r.get("tags", "[]"))
        r["related_characters"] = json.loads(r.get("related_characters", "[]"))
        return r

    def list_all(self, status: str = None) -> List[Dict[str, Any]]:
        """列出所有伏笔"""
        cur = self.conn.cursor()
        if status:
            cur.execute("SELECT * FROM hooks WHERE status = ? ORDER BY planted_chapter", (status,))
        else:
            cur.execute("SELECT * FROM hooks ORDER BY planted_chapter")
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["related_characters"] = json.loads(r.get("related_characters", "[]"))
            results.append(r)
        return results

    def find_by_description(self, desc: str, status: str = "open") -> List[Dict[str, Any]]:
        """按描述查找伏笔（模糊匹配）"""
        cur = self.conn.cursor()
        if status:
            cur.execute("""
                SELECT * FROM hooks WHERE desc LIKE ? AND status = ?
                ORDER BY planted_chapter
            """, (f"%{desc}%", status))
        else:
            cur.execute("""
                SELECT * FROM hooks WHERE desc LIKE ?
                ORDER BY planted_chapter
            """, (f"%{desc}%",))
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["related_characters"] = json.loads(r.get("related_characters", "[]"))
            results.append(r)
        return results

    def get_stats(self) -> Dict[str, Any]:
        """获取伏笔统计"""
        cur = self.conn.cursor()
        cur.execute("SELECT status, COUNT(*) FROM hooks GROUP BY status")
        status_counts = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("SELECT priority, COUNT(*) FROM hooks WHERE status = 'open' GROUP BY priority")
        priority_counts = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("""
            SELECT AVG(urgency), MAX(urgency), AVG(strength)
            FROM hooks WHERE status = 'open'
        """)
        row = cur.fetchone()
        urgency_avg = round(row[0], 3) if row[0] else 0
        urgency_max = round(row[1], 3) if row[1] else 0
        strength_avg = round(row[2], 3) if row[2] else 0
        return {
            "status_counts": status_counts,
            "open_priority_counts": priority_counts,
            "open_urgency_avg": urgency_avg,
            "open_urgency_max": urgency_max,
            "open_strength_avg": strength_avg,
            "total": sum(status_counts.values())
        }

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "plant":
            desc = params.get("description") or params.get("desc")
            planted_chapter = params.get("planted_chapter") or params.get("chapter")
            if not desc or planted_chapter is None:
                raise ValueError("plant需要description/desc和planted_chapter")
            tags = params.get("tags", "").split(",") if params.get("tags") else []
            chars = params.get("characters", "").split(",") if params.get("characters") else []
            strength = float(params.get("strength", 0.5))
            hid = self.plant(desc, int(planted_chapter),
                             params.get("expected_resolve"),
                             params.get("priority"), tags, chars,
                             params.get("hook_id"), strength)
            return {"hook_id": hid}

        elif action == "resolve":
            hook_id = params.get("hook_id")
            resolved_chapter = params.get("resolved_chapter")
            if not hook_id or resolved_chapter is None:
                raise ValueError("resolve需要hook_id和resolved_chapter")
            resolution = params.get("how") or params.get("resolution", "")
            success = self.resolve(hook_id, int(resolved_chapter), resolution)
            return {"success": success}

        elif action == "partial-resolve":
            hook_id = params.get("hook_id")
            hint_chapter = params.get("hint_chapter") or params.get("chapter")
            if not hook_id or hint_chapter is None:
                raise ValueError("partial-resolve需要hook_id和hint_chapter")
            success = self.partial_resolve(hook_id, int(hint_chapter))
            return {"success": success}

        elif action == "hint":
            hook_id = params.get("hook_id")
            hint_chapter = params.get("hint_chapter") or params.get("chapter")
            if not hook_id or hint_chapter is None:
                raise ValueError("hint需要hook_id和hint_chapter")
            success = self.hint(hook_id, int(hint_chapter))
            return {"success": success}

        elif action == "update-strength":
            hook_id = params.get("hook_id")
            strength = params.get("strength")
            if not hook_id or strength is None:
                raise ValueError("update-strength需要hook_id和strength")
            success = self.update_strength(hook_id, float(strength))
            return {"success": success}

        elif action == "compute-urgency":
            current_chapter = params.get("current_chapter")
            if current_chapter is None:
                raise ValueError("compute-urgency需要current_chapter")
            result = self.compute_urgency(int(current_chapter))
            return {"updated": result}

        elif action == "abandon":
            hook_id = params.get("hook_id")
            if not hook_id:
                raise ValueError("abandon需要hook_id")
            success = self.abandon(hook_id, params.get("reason", ""))
            return {"success": success}

        elif action == "abandon-chapter":
            chapter = params.get("planted_chapter") or params.get("chapter")
            if chapter is None:
                raise ValueError("abandon-chapter需要chapter")
            count = self.abandon_chapter_hooks(int(chapter), params.get("reason", "章节修订"))
            return {"abandoned_count": count, "chapter": int(chapter)}

        elif action == "list-open":
            return {"hooks": self.get_open_hooks(params.get("current_chapter"),
                                                   params.get("priority"))}

        elif action == "overdue":
            current_chapter = params.get("current_chapter")
            if current_chapter is None:
                raise ValueError("overdue需要current_chapter")
            return {"hooks": self.get_overdue_hooks(int(current_chapter))}

        elif action == "forgotten":
            current_chapter = params.get("current_chapter")
            if current_chapter is None:
                raise ValueError("forgotten需要current_chapter")
            return {"hooks": self.get_forgotten_hooks(int(current_chapter))}

        elif action == "stats":
            return self.get_stats()

        elif action == "get":
            hook_id = params.get("hook_id")
            if not hook_id:
                raise ValueError("get需要hook_id")
            hook = self.get_hook(hook_id)
            return {"hook": hook} if hook else {"hook": None}

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='伏笔追踪器')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['plant', 'resolve', 'partial-resolve', 'hint',
                               'update-strength', 'compute-urgency',
                               'abandon', 'abandon-chapter',
                               'get', 'list-open', 'list-all', 'overdue',
                               'forgotten', 'stats'],
                       help='操作类型')
    parser.add_argument('--hook-id', help='伏笔ID')
    parser.add_argument('--desc', help='伏笔描述')
    parser.add_argument('--planted-chapter', type=int, help='种埋章节')
    parser.add_argument('--expected-resolve', type=int, help='预期收线章节')
    parser.add_argument('--resolved-chapter', type=int, help='收线章节')
    parser.add_argument('--resolution', help='收线描述')
    parser.add_argument('--reason', help='放弃原因')
    parser.add_argument('--priority', choices=['critical', 'normal', 'minor'],
                       default=None, help='优先级(默认不限)')
    parser.add_argument('--tags', help='标签(逗号分隔)')
    parser.add_argument('--characters', help='关联角色(逗号分隔)')
    parser.add_argument('--current-chapter', type=int, help='当前章节')
    parser.add_argument('--strength', type=float, default=None, help='伏笔强度(0-1)')
    parser.add_argument('--hint-chapter', type=int, help='暗示/部分回收章节')
    parser.add_argument('--status', choices=['open', 'resolved', 'abandoned'],
                       help='状态过滤')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    tracker = HookTracker(args.db_path)
    try:
        skip_keys = {"db_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = tracker.execute_action(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        tracker.close()


if __name__ == '__main__':
    main()
