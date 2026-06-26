#!/usr/bin/env python3
"""
记忆引擎 - OnKos 的核心存储与检索系统
SQLite FTS5 全文索引 + ONNX 语义检索（可选增强）+ 6级分层摘要
支持 2000 章规模: 事实相关性引擎 + 章节范围预过滤 + numpy 向量化搜索

职责分区:
  - 场景存储与检索（FTS5 + ONNX 语义）
  - 摘要管理（6级分层）
  - 弧线管理（创建/查询/列表）
  - 统计信息

事实管理已拆分至 fact_engine.py
"""

import os
import json
import sqlite3
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


# 检测 ONNX Runtime 是否可用
try:
    import onnxruntime as ort
    import numpy as np
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False

# 语义模型管理器（延迟导入）
_semantic_model = None


class MemoryEngine:
    """记忆引擎 - 全书级别的存储与语义检索（2000章架构）"""

    SCHEMA_VERSION = 2

    @staticmethod
    def _segment_for_fts(text: str) -> str:
        """将文本用 jieba 分词后以空格连接，使 FTS5 unicode61 能正确索引中文"""
        if not text:
            return text
        try:
            import jieba
            return " ".join(jieba.cut(text))
        except ImportError:
            # jieba不可用时直接返回原文，FTS5仍可按单字符索引
            return text

    @staticmethod
    def _read_project_config(project_path: str) -> Dict[str, Any]:
        """读取项目配置（含默认值回退）"""
        config_path = Path(project_path) / "data" / "project_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"settings": {"chapters_per_volume": 20}}

    def __init__(self, db_path: str, model_dir: str = None, project_path: str = None):
        """
        初始化记忆引擎

        Args:
            db_path: SQLite 数据库文件路径
            model_dir: ONNX 语义模型目录（可选，默认自动检测）
            project_path: 项目根路径（用于读取配置）
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.project_path = Path(project_path) if project_path else self.db_path.parent.parent
        self.model_dir = model_dir
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self):
        """初始化数据库结构（含自动升级）"""
        cur = self.conn.cursor()

        # 版本表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        """)

        # 读取当前版本
        cur.execute("SELECT MAX(version) FROM schema_version")
        row = cur.fetchone()
        current_version = row[0] if row and row[0] else 0

        # === 版本 1: 基础表 ===
        if current_version < 1:
            cur.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS scenes USING fts5(
                    content, tags, chapter, location, characters, mood, events,
                    content='scenes_content', tokenize='unicode61'
                )
            """)
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
                CREATE TABLE IF NOT EXISTS embeddings (
                    scene_id INTEGER PRIMARY KEY,
                    embedding BLOB,
                    model_name TEXT,
                    FOREIGN KEY (scene_id) REFERENCES scenes_content(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY,
                    level TEXT NOT NULL,
                    range_desc TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT,
                    updated_at TEXT,
                    UNIQUE(level, range_desc)
                )
            """)
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
                    FOREIGN KEY (superseded_by) REFERENCES facts(id)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_facts_entity_attr
                ON facts(entity, attribute)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_facts_active
                ON facts(entity, attribute) WHERE superseded_by IS NULL
            """)

        # === 版本 2: 2000章架构扩展 ===
        if current_version < 2:
            # 事实表扩展: 相关性引擎
            try:
                cur.execute("ALTER TABLE facts ADD COLUMN importance TEXT DEFAULT 'chapter-scoped'")
            except sqlite3.OperationalError:
                pass
            try:
                cur.execute("ALTER TABLE facts ADD COLUMN valid_from INTEGER")
            except sqlite3.OperationalError:
                pass
            try:
                cur.execute("ALTER TABLE facts ADD COLUMN valid_until INTEGER")
            except sqlite3.OperationalError:
                pass
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_facts_importance
                ON facts(importance) WHERE superseded_by IS NULL
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_facts_valid_range
                ON facts(valid_from, valid_until) WHERE superseded_by IS NULL
            """)

            # 场景表索引: 章节范围查询
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_scenes_chapter
                ON scenes_content(chapter)
            """)

            # 知识图谱表
            cur.execute("""
                CREATE TABLE IF NOT EXISTS kg_nodes (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    tags TEXT,
                    properties TEXT,
                    created_at TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS kg_edges (
                    id INTEGER PRIMARY KEY,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    properties TEXT,
                    created_at TEXT,
                    FOREIGN KEY (source) REFERENCES kg_nodes(id),
                    FOREIGN KEY (target) REFERENCES kg_nodes(id)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_kg_nodes_type ON kg_nodes(type)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_kg_nodes_name ON kg_nodes(name)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_kg_edges_source ON kg_edges(source)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_kg_edges_target ON kg_edges(target)
            """)

            # 伏笔表
            cur.execute("""
                CREATE TABLE IF NOT EXISTS hooks (
                    id TEXT PRIMARY KEY,
                    desc TEXT NOT NULL,
                    planted_chapter INTEGER,
                    expected_resolve INTEGER,
                    resolved_chapter INTEGER,
                    resolution TEXT,
                    status TEXT DEFAULT 'open',
                    priority TEXT DEFAULT 'normal',
                    tags TEXT,
                    related_characters TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_hooks_status ON hooks(status)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_hooks_planted ON hooks(planted_chapter)
            """)

            # 弧线表
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
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_arcs_type ON arcs(arc_type)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_arcs_range ON arcs(start_chapter, end_chapter)
            """)

        # 记录版本
        if current_version < self.SCHEMA_VERSION:
            cur.execute("DELETE FROM schema_version")
            cur.execute("INSERT INTO schema_version VALUES (?)", (self.SCHEMA_VERSION,))

        self.conn.commit()


    # ==================== 场景存储 ====================

    def _insert_scene_raw(self, cur, content: str, chapter: int, tags: str = "",
                          location: str = "", characters: str = "",
                          mood: str = "", events: str = "") -> int:
        """
        内部方法：插入单条场景记录（不含commit，供事务内调用）

        将 scenes_content / scenes(FTS5) / embeddings 三表写入统一在调用方事务中commit，
        避免部分提交导致数据不一致。
        """
        cur.execute("""
            INSERT INTO scenes_content (content, tags, chapter, location, characters, mood, events)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (content, tags, chapter, location, characters, mood, events))

        scene_id = cur.lastrowid

        fts_content = self._segment_for_fts(content)
        fts_tags = self._segment_for_fts(tags)
        fts_characters = self._segment_for_fts(characters)
        fts_location = self._segment_for_fts(location)
        fts_events = self._segment_for_fts(events)
        cur.execute("""
            INSERT INTO scenes (rowid, content, tags, chapter, location, characters, mood, events)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (scene_id, fts_content, fts_tags, str(chapter), fts_location, fts_characters, mood, fts_events))

        if ONNX_AVAILABLE:
            embedding = self._encode(content)
            if embedding is not None:
                cur.execute("""
                    INSERT INTO embeddings (scene_id, embedding, model_name)
                    VALUES (?, ?, ?)
                """, (scene_id, embedding.tobytes(), "miniLM-L12-v2"))

        return scene_id

    def store_scene(self, content: str, chapter: int, tags: str = "",
                    location: str = "", characters: str = "",
                    mood: str = "", events: str = "",
                    replace: bool = False) -> int:
        """
        存储场景到记忆引擎

        Args:
            content: 场景原文
            chapter: 章节编号
            tags: 关键词标签（逗号分隔）
            location: 场景地点
            characters: 出场角色（逗号分隔）
            mood: 情感基调
            events: 关键事件（逗号分隔）
            replace: 是否替换该章节已有场景（True时先删除旧场景再录入）

        Returns:
            场景ID
        """
        if replace:
            # 事务保证 delete + insert 原子性
            try:
                cur = self.conn.cursor()
                cur.execute("BEGIN")
                self.delete_chapter_scenes(chapter, commit=False)
                scene_id = self._insert_scene_raw(cur, content, chapter, tags,
                                                  location, characters, mood, events)
                self.conn.commit()
            except Exception:
                self.conn.rollback()
                raise
        else:
            cur = self.conn.cursor()
            scene_id = self._insert_scene_raw(cur, content, chapter, tags,
                                              location, characters, mood, events)
            self.conn.commit()
        return scene_id

    def delete_chapter_scenes(self, chapter_num: int, commit: bool = True) -> int:
        """
        删除指定章节的所有场景（含FTS索引和embedding），返回删除数量

        用于修订章节时清理旧数据，防止场景数据膨胀。

        Args:
            chapter_num: 章节编号
            commit: 是否立即提交（事务内调用时传False，由调用方统一commit）
        """
        cur = self.conn.cursor()

        # 1. 获取该章节所有场景ID
        cur.execute("SELECT id FROM scenes_content WHERE chapter = ?", (chapter_num,))
        scene_ids = [row[0] for row in cur.fetchall()]

        if not scene_ids:
            return 0

        # 2. 删除 embedding
        placeholders = ",".join("?" * len(scene_ids))
        cur.execute(f"DELETE FROM embeddings WHERE scene_id IN ({placeholders})", scene_ids)

        # 3. 删除 FTS 索引（rowid 与 scenes_content.id 一致）
        cur.execute(f"DELETE FROM scenes WHERE rowid IN ({placeholders})", scene_ids)

        # 4. 删除场景内容
        cur.execute("DELETE FROM scenes_content WHERE chapter = ?", (chapter_num,))

        if commit:
            self.conn.commit()
        return len(scene_ids)

    def store_chapter(self, chapter_num: int, content: str, tags: str = "",
                      characters: str = "", events: str = "",
                      replace: bool = False) -> List[int]:
        """
        存储完整章节（按段落拆分为场景），事务保证原子性

        replace=True 时，delete + store 在同一事务中完成，
        避免旧数据已删但新数据未写入的数据丢失风险。

        Args:
            chapter_num: 章节编号
            content: 章节全文
            tags: 关键词标签
            characters: 出场角色
            events: 关键事件
            replace: 是否替换已有场景（True时先删除该章节的旧场景再录入）

        Returns:
            场景ID列表
        """
        # 混合段落拆分策略
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        if len(paragraphs) <= 1:
            # 中文小说常用单换行分段
            paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
        if not paragraphs:
            paragraphs = [content]

        # 对过长段落（>500字）按句号二次拆分
        final_paragraphs = []
        for para in paragraphs:
            if len(para) > 500:
                sub_parts = []
                current = ""
                for sentence in para.replace("。", "。\n").replace("！", "！\n").replace("？", "？\n").split("\n"):
                    s = sentence.strip()
                    if not s:
                        continue
                    if len(current) + len(s) > 500 and current:
                        sub_parts.append(current)
                        current = s
                    else:
                        current += s
                if current:
                    sub_parts.append(current)
                final_paragraphs.extend(sub_parts if sub_parts else [para])
            else:
                final_paragraphs.append(para)

        if not final_paragraphs:
            final_paragraphs = [content]

        # 事务包裹：delete(如有) + 全部 store 统一 commit
        scene_ids = []
        try:
            cur = self.conn.cursor()
            cur.execute("BEGIN")

            if replace:
                self.delete_chapter_scenes(chapter_num, commit=False)

            for i, para in enumerate(final_paragraphs):
                sid = self._insert_scene_raw(
                    cur, para, chapter_num, tags,
                    characters=characters,
                    events=events if i == 0 else ""
                )
                scene_ids.append(sid)

            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        return scene_ids

    # ==================== 检索 ====================

    def search(self, query: str, top_k: int = 5,
               chapter_filter: int = None,
               chapter_range: Tuple[int, int] = None,
               character_filter: str = None) -> List[Dict[str, Any]]:
        """
        搜索相关场景

        Args:
            query: 搜索查询
            top_k: 返回结果数量
            chapter_filter: 精确章节过滤
            chapter_range: 章节范围过滤 (start, end)，优先于 chapter_filter
            character_filter: 角色过滤

        Returns:
            搜索结果列表
        """
        if ONNX_AVAILABLE:
            results = self._semantic_search(query, top_k, chapter_filter, chapter_range, character_filter)
            if results:
                return results
        return self._keyword_search(query, top_k, chapter_filter, chapter_range, character_filter)

    def _keyword_search(self, query: str, top_k: int = 5,
                        chapter_filter: int = None,
                        chapter_range: Tuple[int, int] = None,
                        character_filter: str = None) -> List[Dict[str, Any]]:
        """FTS5 关键词搜索"""
        if " OR " in query:
            parts = query.split(" OR ")
            segmented_parts = []
            for part in parts:
                seg = self._segment_for_fts(part.strip())
                if seg.strip():
                    segmented_parts.append(seg.strip())
            fts_query = " OR ".join(segmented_parts)
        else:
            segmented = self._segment_for_fts(query)
            tokens = [t.strip() for t in segmented.split() if t.strip()]
            fts_query = " OR ".join(tokens)

        if not fts_query.strip():
            return []

        sql = """
            SELECT sc.id, sc.content, sc.tags, sc.chapter,
                   sc.location, sc.characters, sc.mood, sc.events,
                   bm25(scenes) as rank
            FROM scenes
            JOIN scenes_content sc ON scenes.rowid = sc.id
            WHERE scenes MATCH ?
        """
        params = [fts_query]

        if chapter_range:
            sql += " AND sc.chapter >= ? AND sc.chapter <= ?"
            params.extend([chapter_range[0], chapter_range[1]])
        elif chapter_filter is not None:
            sql += " AND sc.chapter = ?"
            params.append(str(chapter_filter))

        if character_filter:
            sql += " AND sc.characters LIKE ?"
            params.append(f"%{character_filter}%")

        sql += " ORDER BY rank LIMIT ?"
        params.append(top_k)

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def _semantic_search(self, query: str, top_k: int = 5,
                         chapter_filter: int = None,
                         chapter_range: Tuple[int, int] = None,
                         character_filter: str = None) -> List[Dict[str, Any]]:
        """ONNX 语义搜索（含章节范围预过滤 + numpy 向量化）"""
        query_emb = self._encode(query)
        if query_emb is None:
            return []

        cur = self.conn.cursor()
        sql = """SELECT e.scene_id, e.embedding, sc.content, sc.tags, sc.chapter,
                        sc.location, sc.characters, sc.mood, sc.events
                 FROM embeddings e JOIN scenes_content sc ON e.scene_id = sc.id WHERE 1=1"""
        params = []

        # 章节范围预过滤: 优先使用 chapter_range
        if chapter_range:
            sql += " AND sc.chapter >= ? AND sc.chapter <= ?"
            params.extend([chapter_range[0], chapter_range[1]])
        elif chapter_filter is not None:
            sql += " AND sc.chapter = ?"
            params.append(chapter_filter)

        if character_filter:
            sql += " AND sc.characters LIKE ?"
            params.append(f"%{character_filter}%")

        cur.execute(sql, params)
        rows = cur.fetchall()

        if not rows:
            # 如果预过滤后无结果，回退到全量搜索
            if chapter_range or chapter_filter is not None:
                return []
            return []

        # numpy 向量化相似度计算
        emb_list = []
        row_data = []
        for row in rows:
            emb = np.frombuffer(row["embedding"], dtype=np.float32)
            emb_list.append(emb)
            row_data.append(dict(row))

        if not emb_list:
            return []

        emb_matrix = np.stack(emb_list)  # (N, 768)
        scores = emb_matrix @ query_emb  # (N,)
        norms = np.linalg.norm(emb_matrix, axis=1) * np.linalg.norm(query_emb) + 1e-8
        scores = scores / norms

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [{**row_data[i], "similarity": float(scores[i])} for i in top_indices]

    def _encode(self, text: str) -> Optional[Any]:
        """使用 ONNX 语义模型编码文本"""
        global _semantic_model

        if not ONNX_AVAILABLE:
            return None

        try:
            if _semantic_model is None:
                from semantic_model import SemanticModel
                if self.model_dir:
                    _semantic_model = SemanticModel(self.model_dir)
                else:
                    project_model_dir = self.db_path.parent / "semantic_model"
                    if project_model_dir.exists():
                        _semantic_model = SemanticModel(str(project_model_dir))
                    else:
                        _semantic_model = SemanticModel()

            if not _semantic_model.is_ready:
                return None

            embedding = _semantic_model.encode(text)
            if embedding is not None:
                return embedding.astype(np.float32)
            return None
        except Exception:
            return None

    # ==================== 摘要管理 ====================

    def store_summary(self, level: str, range_desc: str, content: str) -> int:
        """
        存储摘要（支持 6 级: book / phase / arc / volume / chapter / scene）

        Args:
            level: 摘要层级
            range_desc: 范围描述
            content: 摘要内容

        Returns:
            摘要ID
        """
        now = datetime.now().isoformat()
        cur = self.conn.cursor()

        cur.execute("""
            INSERT OR REPLACE INTO summaries (level, range_desc, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (level, range_desc, content, now, now))

        self.conn.commit()
        return cur.lastrowid

    def get_summary(self, level: str, range_desc: str) -> Optional[str]:
        """获取摘要"""
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM summaries WHERE level=? AND range_desc=?", (level, range_desc))
        row = cur.fetchone()
        return row["content"] if row else None

    def get_chapter_summary(self, chapter: int) -> Optional[str]:
        """获取章节摘要"""
        return self.get_summary("chapter", str(chapter))

    def get_volume_summary(self, volume: int) -> Optional[str]:
        """获取卷摘要"""
        return self.get_summary("volume", str(volume))

    def get_arc_summary(self, arc_id: str) -> Optional[str]:
        """获取弧线摘要"""
        return self.get_summary("arc", arc_id)

    def get_phase_summary(self, phase_id: str) -> Optional[str]:
        """获取阶段摘要"""
        return self.get_summary("phase", phase_id)

    def get_book_summary(self) -> Optional[str]:
        """获取全书摘要"""
        return self.get_summary("book", "全书")

    def get_current_state_summary(self) -> Optional[str]:
        """获取当前状态摘要（滚动更新的最新进展概览）"""
        return self.get_summary("book", "current_state")

    # ==================== 弧线管理 ====================

    def create_arc(self, arc_id: str, title: str, arc_type: str = "arc",
                   start_chapter: int = 1, end_chapter: int = None,
                   phase_id: str = None, description: str = "") -> str:
        """创建弧线或阶段"""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO arcs (id, title, arc_type, start_chapter, end_chapter,
                phase_id, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (arc_id, title, arc_type, start_chapter, end_chapter, phase_id, description, now, now))
        self.conn.commit()
        return arc_id

    def get_arc(self, arc_id: str) -> Optional[Dict[str, Any]]:
        """获取弧线信息"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM arcs WHERE id = ?", (arc_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_active_arc(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取指定章节所属的活跃弧线"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE start_chapter <= ? AND (end_chapter IS NULL OR end_chapter >= ?)
            AND arc_type = 'arc'
            ORDER BY start_chapter DESC LIMIT 1
        """, (chapter, chapter))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_active_phase(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取指定章节所属的阶段"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM arcs
            WHERE start_chapter <= ? AND (end_chapter IS NULL OR end_chapter >= ?)
            AND arc_type = 'phase'
            ORDER BY start_chapter DESC LIMIT 1
        """, (chapter, chapter))
        row = cur.fetchone()
        return dict(row) if row else None

    def list_arcs(self, arc_type: str = None) -> List[Dict[str, Any]]:
        """列出所有弧线/阶段"""
        cur = self.conn.cursor()
        if arc_type:
            cur.execute("SELECT * FROM arcs WHERE arc_type = ? ORDER BY start_chapter", (arc_type,))
        else:
            cur.execute("SELECT * FROM arcs ORDER BY start_chapter")
        return [dict(row) for row in cur.fetchall()]

    def update_arc(self, arc_id: str, **kwargs) -> bool:
        """更新弧线属性"""
        arc = self.get_arc(arc_id)
        if not arc:
            return False
        sets = []
        vals = []
        for k, v in kwargs.items():
            if k in ("title", "end_chapter", "phase_id", "description"):
                sets.append(f"{k} = ?")
                vals.append(v)
        if not sets:
            return False
        sets.append("updated_at = ?")
        vals.append(datetime.now().isoformat())
        vals.append(arc_id)
        cur = self.conn.cursor()
        cur.execute(f"UPDATE arcs SET {', '.join(sets)} WHERE id = ?", vals)
        self.conn.commit()
        return True

    def get_volume_for_chapter(self, chapter: int) -> int:
        """根据项目配置计算章节所属的卷号"""
        config = self._read_project_config(str(self.project_path))
        cpv = config.get("settings", {}).get("chapters_per_volume", 20)
        return (chapter - 1) // cpv + 1

    # ==================== 统计 ====================

    def get_stats(self) -> Dict[str, Any]:
        """获取记忆引擎统计信息"""
        cur = self.conn.cursor()
        stats = {}
        cur.execute("SELECT COUNT(*) FROM scenes_content")
        stats["total_scenes"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM summaries")
        stats["total_summaries"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM facts WHERE superseded_by IS NULL")
        stats["active_facts"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM embeddings")
        stats["total_embeddings"] = cur.fetchone()[0]
        cur.execute("SELECT DISTINCT chapter FROM scenes_content ORDER BY chapter")
        stats["chapters"] = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM kg_nodes")
        stats["kg_nodes"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM kg_edges")
        stats["kg_edges"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM hooks WHERE status = 'open'")
        stats["open_hooks"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM arcs")
        stats["total_arcs"] = cur.fetchone()[0]
        stats["onnx_available"] = ONNX_AVAILABLE
        return stats

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口：command_executor直接调用此方法"""
        # 参数便捷转换：chapter可作为range_desc的简写
        if "chapter" in params and "range_desc" not in params:
            params = dict(params)
            params["range_desc"] = str(params["chapter"])

        # 支持从文件读取内容（支持相对路径，基于项目目录解析）
        content = params.get("content", "")
        content_file = params.get("content_file", "")
        if content_file:
            # 如果是相对路径，基于数据库所在目录解析
            content_path = Path(content_file)
            if not content_path.is_absolute():
                content_path = Path(self.db_path).parent / content_path
            try:
                with open(content_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                return {"error": f"读取内容文件失败: {str(e)}"}

        if action == "store-chapter":
            chapter = params.get("chapter")
            if not content or not content.strip() or chapter is None:
                raise ValueError("store-chapter需要chapter和content")
            ids = self.store_chapter(int(chapter), content,
                                     params.get("tags", ""),
                                     params.get("characters", ""),
                                     params.get("events", ""),
                                     replace=params.get("replace", False))
            return {"scene_ids": ids, "scene_count": len(ids)}

        elif action == "store-scene":
            chapter = params.get("chapter")
            if not content or not content.strip() or chapter is None:
                raise ValueError("store-scene需要chapter和content")
            sid = self.store_scene(content, int(chapter),
                                   params.get("tags", ""),
                                   location=params.get("location", ""),
                                   characters=params.get("characters", ""),
                                   mood=params.get("mood", ""),
                                   events=params.get("events", ""),
                                   replace=params.get("replace", False))
            return {"scene_id": sid}

        elif action == "search":
            query = params.get("query")
            if not query:
                raise ValueError("search需要query")
            chapter_range = None
            cr = params.get("chapter_range")
            if cr:
                parts = str(cr).split(",")
                if len(parts) == 2:
                    chapter_range = (int(parts[0]), int(parts[1]))
            chapter = params.get("chapter")
            results = self.search(query, int(params.get("top_k", 5)),
                                  int(chapter) if chapter else None, chapter_range)
            return {"results": results}

        elif action == "store-summary":
            level = params.get("level")
            summary_content = params.get("content", content)  # 优先取params中的content，否则用顶层content(可能来自文件)
            # 自动推断range_desc：优先使用显式range_desc，否则从chapter/volume/arc_id/phase_id推断
            range_desc = params.get("range_desc")
            if not range_desc:
                if params.get("chapter") is not None:
                    range_desc = str(params["chapter"])
                elif params.get("volume") is not None:
                    range_desc = str(params["volume"])
                elif params.get("arc_id"):
                    range_desc = params["arc_id"]
                elif params.get("phase_id"):
                    range_desc = str(params["phase_id"])
                elif level == "book":
                    range_desc = "book"
                else:
                    range_desc = ""
            if not level or not range_desc or not summary_content:
                raise ValueError("store-summary需要level/range_desc(或chapter/volume等)和content")
            sid = self.store_summary(level, range_desc, summary_content)
            return {"summary_id": sid}

        elif action == "stats":
            return self.get_stats()

        elif action == "delete-chapter-scenes":
            chapter = params.get("chapter")
            if chapter is None:
                raise ValueError("delete-chapter-scenes需要chapter")
            count = self.delete_chapter_scenes(int(chapter))
            return {"deleted_count": count, "chapter": int(chapter)}

        elif action == "create-arc":
            arc_id = params.get("arc_id")
            title = params.get("title")
            start_chapter = params.get("start_chapter")
            if not arc_id or not title or start_chapter is None:
                raise ValueError("create-arc需要arc_id/title/start_chapter")
            aid = self.create_arc(arc_id, title,
                                   params.get("arc_type", "arc"),
                                   int(start_chapter),
                                   int(params["end_chapter"]) if params.get("end_chapter") else None,
                                   params.get("phase_id"),
                                   params.get("description", ""))
            return {"arc_id": aid}

        elif action == "list-arcs":
            return {"arcs": self.list_arcs(params.get("arc_type"))}

        elif action == "chapter-complete":
            # chapter-complete = store-chapter with replace=True
            chapter = params.get("chapter")
            if not content or not content.strip() or chapter is None:
                raise ValueError("chapter-complete需要chapter和content")
            ids = self.store_chapter(int(chapter), content,
                                     params.get("tags", ""),
                                     params.get("characters", ""),
                                     params.get("events", ""),
                                     replace=True)
            return {"scene_ids": ids, "scene_count": len(ids)}

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭数据库连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='记忆引擎')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['store-chapter', 'store-scene', 'search',
                               'store-summary', 'stats',
                               'create-arc', 'get-arc', 'list-arcs', 'update-arc',
                               'delete-chapter-scenes', 'chapter-complete'],
                       help='操作类型')
    parser.add_argument('--content', help='内容')
    parser.add_argument('--content-file', help='内容文件路径')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--query', help='搜索查询')
    parser.add_argument('--tags', help='标签')
    parser.add_argument('--characters', help='出场角色')
    parser.add_argument('--location', help='场景地点')
    parser.add_argument('--mood', help='情感基调')
    parser.add_argument('--events', help='关键事件')
    parser.add_argument('--level', help='摘要层级')
    parser.add_argument('--range-desc', help='摘要范围')
    parser.add_argument('--top-k', type=int, default=5, help='返回数量')
    parser.add_argument('--chapter-range', help='章节范围(start,end)')
    parser.add_argument('--output', choices=['text', 'json'], default='json')
    parser.add_argument('--model-dir', help='ONNX 语义模型目录')
    parser.add_argument('--project-path', help='项目根路径（用于配置读取）')
    parser.add_argument('--arc-id', help='弧线ID')
    parser.add_argument('--arc-title', help='弧线标题')
    parser.add_argument('--arc-type', choices=['phase', 'arc'], default='arc', help='弧线类型')
    parser.add_argument('--start-chapter', type=int, help='弧线起始章节')
    parser.add_argument('--end-chapter', type=int, help='弧线结束章节')
    parser.add_argument('--phase-id', help='所属阶段ID')
    parser.add_argument('--description', help='描述')
    parser.add_argument('--replace', action='store_true', help='替换模式：先删除该章节旧数据再录入')

    args = parser.parse_args()
    project_path = args.project_path or str(Path(args.db_path).parent.parent)
    engine = MemoryEngine(args.db_path, args.model_dir, project_path)
    try:
        # 将argparse命名空间转为dict，通过execute_action统一调度
        skip_keys = {"db_path", "project_path", "action", "output", "model_dir"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        # argparse的store_true特殊处理
        if args.replace:
            params["replace"] = True

        result = engine.execute_action(args.action, params)

        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        engine.close()

if __name__ == '__main__':
    main()
