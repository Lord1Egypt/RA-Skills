#!/usr/bin/env python3
"""
事实引擎 - 从 memory_engine.py 拆分的事实管理模块
负责: 事实录入/查询/相关性筛选/矛盾检测/归档
依赖: SQLite 数据库（需由 MemoryEngine 或自身初始化 schema）
"""

import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class FactEngine:
    """事实引擎 - 事实管理与相关性检索"""

    SCHEMA_VERSION = 2

    def __init__(self, db_path: str, project_path: str = None):
        self.db_path = Path(db_path)
        self.project_path = Path(project_path) if project_path else self.db_path.parent.parent
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_tables()

    def _ensure_tables(self):
        """确保事实相关表存在（支持独立使用）

        注意: 此方法与 MemoryEngine._init_schema 共享 DDL。
        Schema 变更须在两处同步维护，或通过先调用 MemoryEngine 初始化来避免分歧。
        """
        cur = self.conn.cursor()

        # 事实表（v2 含 importance/valid_from/valid_until）
        cur.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                entity TEXT NOT NULL,
                attribute TEXT NOT NULL,
                value TEXT NOT NULL,
                chapter INTEGER,
                created_at TEXT,
                superseded_by INTEGER DEFAULT NULL,
                importance TEXT DEFAULT 'chapter-scoped',
                valid_from INTEGER,
                valid_until INTEGER,
                FOREIGN KEY (superseded_by) REFERENCES facts(id)
            )
        """)
        # v2 迁移: 为旧库补充字段
        for col, default in [("importance", "'chapter-scoped'"),
                             ("valid_from", "NULL"), ("valid_until", "NULL")]:
            try:
                cur.execute(f"ALTER TABLE facts ADD COLUMN {col} {'TEXT' if col == 'importance' else 'INTEGER'} DEFAULT {default}")
            except sqlite3.OperationalError:
                pass
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_facts_entity_attr
            ON facts(entity, attribute)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_facts_active
            ON facts(entity, attribute) WHERE superseded_by IS NULL
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_facts_importance
            ON facts(importance) WHERE superseded_by IS NULL
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_facts_valid_range
            ON facts(valid_from, valid_until) WHERE superseded_by IS NULL
        """)

        # 弧线表（get_relevant_facts 需要查询）
        cur.execute("""
            CREATE TABLE IF NOT EXISTS arcs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                arc_type TEXT NOT NULL DEFAULT 'arc',
                start_chapter INTEGER NOT NULL,
                end_chapter INTEGER,
                phase_id TEXT,
                description TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)

        # 场景表（get_latest_chapter 需要查询）
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scenes_content (
                id INTEGER PRIMARY KEY,
                content TEXT,
                tags TEXT,
                chapter INTEGER,
                location TEXT,
                characters TEXT,
                mood TEXT,
                events TEXT
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_scenes_chapter
            ON scenes_content(chapter)
        """)

        # schema 版本表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        """)

        self.conn.commit()

    # ==================== 事实管理 ====================

    def set_fact(self, category: str, entity: str, attribute: str,
                 value: str, chapter: int,
                 importance: str = "chapter-scoped",
                 valid_from: int = None, valid_until: int = None) -> int:
        """
        设置事实（自动处理版本替代和相关性）

        Args:
            category: 类别（character / world / item / event）
            entity: 实体名
            attribute: 属性名
            value: 属性值
            chapter: 确立该事实的章节
            importance: 重要性层级（permanent / arc-scoped / chapter-scoped）
            valid_from: 生效起始章节（None=从chapter开始）
            valid_until: 失效章节（None=永久或直到被替代）

        Returns:
            事实ID
        """
        now = datetime.now().isoformat()

        if valid_from is None:
            valid_from = chapter

        try:
            cur = self.conn.cursor()
            cur.execute("BEGIN IMMEDIATE")

            # 将同实体的同属性的旧事实标记为已替代（临时标记-1）
            cur.execute("""
                UPDATE facts SET superseded_by = -1
                WHERE entity = ? AND attribute = ? AND superseded_by IS NULL
            """, (entity, attribute))

            cur.execute("""
                INSERT INTO facts (category, entity, attribute, value, chapter, importance,
                    valid_from, valid_until, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (category, entity, attribute, value, chapter, importance,
                  valid_from, valid_until, now))

            new_id = cur.lastrowid

            # 将临时标记替换为真正的新事实ID
            cur.execute("""
                UPDATE facts SET superseded_by = ?
                WHERE entity = ? AND attribute = ? AND superseded_by = -1
            """, (new_id, entity, attribute))

            self.conn.commit()
            return new_id
        except Exception:
            self.conn.rollback()
            # 修复残留的临时标记（-1），将其恢复为NULL
            try:
                self.conn.execute(
                    "UPDATE facts SET superseded_by = NULL WHERE superseded_by = -1"
                )
                self.conn.commit()
            except Exception:
                pass
            raise

    def get_fact(self, entity: str, attribute: str) -> Optional[str]:
        """获取当前有效的事实值"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT value FROM facts
            WHERE entity = ? AND attribute = ? AND superseded_by IS NULL
        """, (entity, attribute))
        row = cur.fetchone()
        return row["value"] if row else None

    def delete_fact(self, entity: str, attribute: str) -> int:
        """删除指定实体的指定属性事实（真删除，非supersede）"""
        cur = self.conn.cursor()
        cur.execute("""
            DELETE FROM facts WHERE entity = ? AND attribute = ?
        """, (entity, attribute))
        self.conn.commit()
        return cur.rowcount

    def delete_entity_facts(self, entity: str) -> int:
        """删除指定实体的全部事实"""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM facts WHERE entity = ?", (entity,))
        self.conn.commit()
        return cur.rowcount

    def get_all_facts(self, entity: str = None, category: str = None,
                      limit: int = None) -> List[Dict[str, Any]]:
        """获取所有当前有效的事实（可选限制数量）"""
        sql = "SELECT * FROM facts WHERE superseded_by IS NULL"
        params = []
        if entity:
            sql += " AND entity = ?"
            params.append(entity)
        if category:
            sql += " AND category = ?"
            params.append(category)
        sql += " ORDER BY chapter DESC"
        if limit:
            sql += " LIMIT ?"
            params.append(limit)
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def get_relevant_facts(self, current_chapter: int,
                           mentioned_entities: List[str] = None,
                           max_facts: int = 80) -> List[Dict[str, Any]]:
        """
        按相关性获取事实（2000章架构核心方法）

        优先级:
        1. permanent 事实（角色核心属性、世界观基石）
        2. 提及实体的所有活跃事实
        3. 当前弧线范围内的 arc-scoped 事实
        4. 近 10 章的 chapter-scoped 事实

        Args:
            current_chapter: 当前章节
            mentioned_entities: 章节大纲中提及的实体名列表
            max_facts: 最大返回数量
        """
        results = []
        seen_ids = set()
        cur = self.conn.cursor()

        def _add_rows(rows):
            for r in rows:
                d = dict(r)
                if d["id"] not in seen_ids:
                    seen_ids.add(d["id"])
                    results.append(d)

        # 通用条件：事实未被替代，或替代事实尚未生效（valid_from > current_chapter）
        active_condition = """
            (superseded_by IS NULL
             OR id IN (
                 SELECT f1.id FROM facts f1
                 JOIN facts f2 ON f1.superseded_by = f2.id
                 WHERE f2.valid_from IS NOT NULL AND f2.valid_from > ?
             ))
        """

        # 1. 全部 permanent 事实（已生效且未失效）
        cur.execute(f"""
            SELECT * FROM facts
            WHERE {active_condition} AND importance = 'permanent'
            AND (valid_from IS NULL OR valid_from <= ?)
            AND (valid_until IS NULL OR valid_until >= ?)
            ORDER BY chapter DESC
        """, (current_chapter, current_chapter, current_chapter))
        _add_rows(cur.fetchall())

        # 2. 提及实体的事实（已生效且未失效）
        if mentioned_entities:
            placeholders = ",".join("?" * len(mentioned_entities))
            cur.execute(f"""
                SELECT * FROM facts
                WHERE {active_condition} AND entity IN ({placeholders})
                AND (valid_from IS NULL OR valid_from <= ?)
                AND (valid_until IS NULL OR valid_until >= ?)
                ORDER BY chapter DESC
            """, [current_chapter] + mentioned_entities + [current_chapter, current_chapter])
            _add_rows(cur.fetchall())

        # 3. 当前弧线范围内的 arc-scoped 事实
        active_arc = self._get_active_arc(current_chapter)
        if active_arc:
            arc_start = active_arc["start_chapter"]
            arc_end = active_arc.get("end_chapter") or current_chapter + 100
            cur.execute(f"""
                SELECT * FROM facts
                WHERE {active_condition}
                AND importance = 'arc-scoped'
                AND (valid_from IS NULL OR valid_from <= ?)
                AND (valid_until IS NULL OR valid_until >= ?)
                ORDER BY chapter DESC
            """, (current_chapter, arc_end, arc_start))
            _add_rows(cur.fetchall())

        # 4. 近 10 章的 chapter-scoped 事实（已生效且未失效）
        recent_start = max(1, current_chapter - 10)
        cur.execute(f"""
            SELECT * FROM facts
            WHERE {active_condition}
            AND importance = 'chapter-scoped'
            AND chapter >= ? AND chapter <= ?
            AND (valid_from IS NULL OR valid_from <= ?)
            AND (valid_until IS NULL OR valid_until >= ?)
            ORDER BY chapter DESC
        """, (current_chapter, recent_start, current_chapter, current_chapter, current_chapter))
        _add_rows(cur.fetchall())

        return results[:max_facts]

    def detect_contradictions(self) -> List[Dict[str, Any]]:
        """检测事实矛盾"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT entity, attribute, COUNT(*) as cnt
            FROM facts
            WHERE superseded_by IS NULL
            GROUP BY entity, attribute
            HAVING cnt > 1
        """)
        return [dict(row) for row in cur.fetchall()]

    def get_fact_history(self, entity: str, attribute: str) -> List[Dict[str, Any]]:
        """获取事实的变更历史"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, value, chapter, importance, valid_from, valid_until, created_at, superseded_by
            FROM facts
            WHERE entity = ? AND attribute = ?
            ORDER BY id
        """, (entity, attribute))
        return [dict(row) for row in cur.fetchall()]

    def archive_old_facts(self, current_chapter: int, threshold: int = 200) -> int:
        """
        归档过旧的事实（将 chapter-scoped 事实设为已替代）

        Args:
            current_chapter: 当前章节
            threshold: 超过多少章前的事实被归档

        Returns:
            归档数量
        """
        cutoff = max(1, current_chapter - threshold)
        try:
            cur = self.conn.cursor()
            cur.execute("BEGIN IMMEDIATE")

            # 直接用 0（已归档）替代，避免两步临时标记
            cur.execute("""
                UPDATE facts SET superseded_by = 0
                WHERE superseded_by IS NULL
                AND importance = 'chapter-scoped'
                AND chapter < ?
                AND valid_until IS NULL
            """, (cutoff,))
            count = cur.rowcount
            self.conn.commit()
            return count
        except Exception:
            self.conn.rollback()
            raise

    def supersede_chapter_facts(self, chapter: int) -> int:
        """
        将指定章节确立的有效事实标记为系统废弃（superseded_by=-2）

        用于修订章节时清理旧事实。被废弃的事实不再出现在有效查询中，
        但仍保留在事实历史中可追溯。重新 set_fact 同 entity+attribute
        的事实会自动覆盖此标记。

        Args:
            chapter: 要清理的章节编号

        Returns:
            废弃的事实数量
        """
        try:
            cur = self.conn.cursor()
            cur.execute("BEGIN IMMEDIATE")

            cur.execute("""
                UPDATE facts SET superseded_by = -2
                WHERE superseded_by IS NULL
                AND chapter = ?
            """, (chapter,))
            count = cur.rowcount
            self.conn.commit()
            return count
        except Exception:
            self.conn.rollback()
            raise

    # ==================== 辅助方法 ====================

    def _get_active_arc(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取指定章节所属的活跃弧线（内部使用，仅查arcs表）"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE start_chapter <= ? AND (end_chapter IS NULL OR end_chapter >= ?)
            AND arc_type = 'arc'
            ORDER BY start_chapter DESC LIMIT 1
        """, (chapter, chapter))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_latest_chapter(self) -> int:
        """获取项目中已存储的最新章节号（从 scenes_content 查询）"""
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(chapter) FROM scenes_content")
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else 0

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "set-fact":
            entity = params.get("entity")
            attribute = params.get("attribute")
            value = params.get("value")
            category = params.get("category", "")
            chapter = params.get("chapter")
            if not entity or not attribute or not value or chapter is None:
                raise ValueError("set-fact需要entity/attribute/value/chapter")
            if not category:
                category = "默认"
            fid = self.set_fact(category, entity, attribute, value,
                                int(chapter),
                                params.get("importance", "chapter-scoped"),
                                params.get("valid_from"), params.get("valid_until"))
            return {"fact_id": fid}

        elif action == "get-fact":
            entity = params.get("entity")
            attribute = params.get("attribute")
            if not entity or not attribute:
                raise ValueError("get-fact需要entity和attribute")
            value = self.get_fact(entity, attribute)
            return {"entity": entity, "attribute": attribute, "value": value}

        elif action == "get-facts":
            return {"facts": self.get_all_facts(params.get("entity"),
                                                 params.get("category"),
                                                 params.get("limit"))}

        elif action == "relevant-facts":
            chapter = params.get("chapter")
            if chapter is None:
                chapter = self.get_latest_chapter()
                if chapter == 0:
                    return {"facts": [], "count": 0, "auto_chapter": 0}
            entities = []
            if params.get("entity"):
                entities = [e.strip() for e in str(params["entity"]).split(",") if e.strip()]
            facts = self.get_relevant_facts(int(chapter), entities,
                                             int(params.get("limit", 80)))
            return {"facts": facts, "count": len(facts), "current_chapter": int(chapter)}

        elif action == "detect-contradictions":
            return {"contradictions": self.detect_contradictions()}

        elif action == "fact-history":
            entity = params.get("entity")
            if not entity:
                raise ValueError("fact-history需要entity")
            attribute = params.get("attribute")
            if attribute:
                return {"history": self.get_fact_history(entity, attribute)}
            else:
                return {"entity": entity, "facts": self.get_all_facts(entity)}

        elif action == "archive-facts":
            chapter = params.get("chapter")
            if chapter is None:
                raise ValueError("archive-facts需要chapter")
            count = self.archive_old_facts(int(chapter), int(params.get("limit", 200)))
            return {"archived_count": count}

        elif action == "supersede-chapter-facts":
            chapter = params.get("chapter")
            if chapter is None:
                raise ValueError("supersede-chapter-facts需要chapter")
            count = self.supersede_chapter_facts(int(chapter))
            return {"superseded_count": count, "chapter": int(chapter)}

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭数据库连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='事实引擎')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['set-fact', 'get-fact', 'get-facts',
                                'relevant-facts', 'archive-facts',
                                'supersede-chapter-facts',
                                'detect-contradictions', 'fact-history'],
                       help='操作类型')
    parser.add_argument('--category', help='事实类别')
    parser.add_argument('--entity', help='实体名')
    parser.add_argument('--attribute', help='属性名')
    parser.add_argument('--value', help='属性值')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--importance', default='chapter-scoped',
                       choices=['permanent', 'arc-scoped', 'chapter-scoped'],
                       help='事实重要性层级')
    parser.add_argument('--valid-from', type=int, help='事实生效起始章节')
    parser.add_argument('--valid-until', type=int, help='事实失效章节')
    parser.add_argument('--limit', type=int, help='最大返回数量')
    parser.add_argument('--project-path', help='项目根路径')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    project_path = args.project_path or str(Path(args.db_path).parent.parent)
    engine = FactEngine(args.db_path, project_path)
    try:
        skip_keys = {"db_path", "project_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = engine.execute_action(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        engine.close()


if __name__ == '__main__':
    main()
