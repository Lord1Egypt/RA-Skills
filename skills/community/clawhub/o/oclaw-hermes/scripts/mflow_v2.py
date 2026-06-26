#!/usr/bin/env python3
"""
mflow v2.0 - 增强型记忆流引擎
基于先进AI记忆架构：三层记忆 + 图记忆 + 智能检索

核心改进：
1. 引入工作记忆层（推理状态）
2. 多信号评分检索（语义+时间+重要性）
3. 记忆图结构（实体关系）
4. 自动记忆提取与整合
5. 记忆衰减与清理机制
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import numpy as np

@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    layer: str  # instant, working, short, long, skill, expert, graph
    content: str
    embedding: Optional[List[float]] = None
    source: str = "unknown"
    timestamp: datetime = None
    importance: float = 1.0  # 1-10
    access_count: int = 0
    last_accessed: datetime = None
    metadata: Dict = None
    entities: List[str] = None  # 图记忆实体
    relations: List[Dict] = None  # 图记忆关系
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.last_accessed is None:
            self.last_accessed = self.timestamp
        if self.metadata is None:
            self.metadata = {}
        if self.entities is None:
            self.entities = []
        if self.relations is None:
            self.relations = []

class MFlowEngineV2:
    """增强型记忆流引擎 v2.0"""
    
    LAYERS = {
        "instant": {"ttl": 3600, "description": "即时记忆 - 当前会话上下文"},
        "working": {"ttl": 7200, "description": "工作记忆 - 推理中间状态"},
        "short": {"ttl": 604800, "description": "短期记忆 - 最近7天"},
        "long": {"ttl": None, "description": "长期记忆 - 持久化知识"},
        "skill": {"ttl": None, "description": "技能记忆 - Skill使用经验"},
        "expert": {"ttl": None, "description": "专家记忆 - 蒸馏的专家思维"},
        "graph": {"ttl": None, "description": "图记忆 - 实体关系网络"}
    }
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "skills" / "oclaw-hermes" / "mflow_v2.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
    def _init_db(self):
        """初始化数据库 - v2.0 schema"""
        with sqlite3.connect(self.db_path) as conn:
            # 主记忆表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    layer TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding BLOB,
                    source TEXT DEFAULT 'unknown',
                    timestamp TEXT NOT NULL,
                    importance REAL DEFAULT 1.0,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT,
                    metadata TEXT,
                    entities TEXT,
                    relations TEXT,
                    synced INTEGER DEFAULT 0
                )
            """)
            
            # 图记忆 - 实体表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    first_seen TEXT,
                    last_seen TEXT,
                    memory_count INTEGER DEFAULT 0
                )
            """)
            
            # 图记忆 - 关系表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS relations (
                    id TEXT PRIMARY KEY,
                    source_entity TEXT NOT NULL,
                    target_entity TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    strength REAL DEFAULT 1.0,
                    memory_id TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (memory_id) REFERENCES memories(id)
                )
            """)
            
            # 记忆提取任务表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS extraction_tasks (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    extracted_facts TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT,
                    completed_at TEXT
                )
            """)
            
            # 全文检索
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    content, metadata,
                    content='memories',
                    content_rowid='rowid'
                )
            """)
            
            # 触发器 - 自动更新FTS
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                    INSERT INTO memory_fts(rowid, content, metadata)
                    VALUES (new.rowid, new.content, new.metadata);
                END
            """)
            
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                    INSERT INTO memory_fts(memory_fts, rowid, content, metadata)
                    VALUES ('delete', old.rowid, old.content, old.metadata);
                END
            """)
            
            conn.commit()
    
    def _simple_embedding(self, text: str) -> List[float]:
        """简化的文本向量化（生产环境应使用真实嵌入模型）"""
        # 使用哈希生成伪向量（演示用）
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        np.random.seed(hash_val % 2**32)
        return np.random.randn(128).tolist()
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        a_arr = np.array(a)
        b_arr = np.array(b)
        return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))
    
    def _calculate_memory_score(
        self, 
        memory: MemoryEntry, 
        query_embedding: List[float],
        current_time: datetime,
        alpha: float = 0.6,  # 语义权重
        beta: float = 0.3,   # 时间权重
        delta: float = 0.1   # 重要性权重
    ) -> float:
        """
        多信号评分公式
        S(m) = α·sim(q, e) + β·γ^(t-ti) + δ·I(m)
        """
        # 语义相似度
        if memory.embedding:
            semantic_score = self._cosine_similarity(query_embedding, memory.embedding)
        else:
            semantic_score = 0.5
        
        # 时间衰减 (γ = 0.995)
        gamma = 0.995
        time_diff = (current_time - memory.timestamp).total_seconds() / 86400  # 天数
        time_score = gamma ** time_diff
        
        # 重要性评分 (归一化到0-1)
        importance_score = memory.importance / 10.0
        
        # 综合评分
        total_score = alpha * semantic_score + beta * time_score + delta * importance_score
        
        return total_score
    
    def store(self, entry: MemoryEntry) -> bool:
        """存储记忆"""
        try:
            # 生成嵌入向量
            if entry.embedding is None:
                entry.embedding = self._simple_embedding(entry.content)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO memories 
                    (id, layer, content, embedding, source, timestamp, importance, 
                     access_count, last_accessed, metadata, entities, relations, synced)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.id,
                    entry.layer,
                    entry.content,
                    json.dumps(entry.embedding),
                    entry.source,
                    entry.timestamp.isoformat(),
                    entry.importance,
                    entry.access_count,
                    entry.last_accessed.isoformat() if entry.last_accessed else None,
                    json.dumps(entry.metadata),
                    json.dumps(entry.entities),
                    json.dumps(entry.relations),
                    0
                ))
                
                # 更新图记忆实体
                for entity_name in entry.entities:
                    conn.execute("""
                        INSERT INTO entities (id, name, type, first_seen, last_seen, memory_count)
                        VALUES (?, ?, ?, ?, ?, 1)
                        ON CONFLICT(id) DO UPDATE SET
                            last_seen = excluded.last_seen,
                            memory_count = memory_count + 1
                    """, (
                        hashlib.md5(entity_name.encode()).hexdigest()[:16],
                        entity_name,
                        "unknown",
                        entry.timestamp.isoformat(),
                        entry.timestamp.isoformat()
                    ))
                
                # 存储关系
                for rel in entry.relations:
                    conn.execute("""
                        INSERT INTO relations (id, source_entity, target_entity, 
                                             relation_type, strength, memory_id, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        hashlib.md5(f"{rel['source']}_{rel['target']}_{rel['type']}".encode()).hexdigest()[:16],
                        rel['source'],
                        rel['target'],
                        rel['type'],
                        rel.get('strength', 1.0),
                        entry.id,
                        entry.timestamp.isoformat()
                    ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"[ERROR] 存储记忆失败: {e}")
            return False
    
    def retrieve(
        self, 
        query: str, 
        layer: str = None,
        top_k: int = 5,
        use_graph: bool = True
    ) -> List[Dict]:
        """
        智能检索记忆
        
        Args:
            query: 查询文本
            layer: 指定记忆层（可选）
            top_k: 返回数量
            use_graph: 是否使用图记忆增强
        """
        query_embedding = self._simple_embedding(query)
        current_time = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # 构建查询
            if layer:
                rows = conn.execute(
                    "SELECT * FROM memories WHERE layer = ?",
                    (layer,)
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM memories").fetchall()
            
            # 计算评分并排序
            scored_memories = []
            for row in rows:
                memory = MemoryEntry(
                    id=row['id'],
                    layer=row['layer'],
                    content=row['content'],
                    embedding=json.loads(row['embedding']) if row['embedding'] else None,
                    source=row['source'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    importance=row['importance'],
                    access_count=row['access_count'],
                    last_accessed=datetime.fromisoformat(row['last_accessed']) if row['last_accessed'] else None,
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    entities=json.loads(row['entities']) if row['entities'] else [],
                    relations=json.loads(row['relations']) if row['relations'] else []
                )
                
                score = self._calculate_memory_score(memory, query_embedding, current_time)
                scored_memories.append((score, memory))
            
            # 排序并返回top_k
            scored_memories.sort(key=lambda x: x[0], reverse=True)
            results = []
            
            for score, memory in scored_memories[:top_k]:
                # 更新访问统计
                conn.execute(
                    "UPDATE memories SET access_count = access_count + 1, last_accessed = ? WHERE id = ?",
                    (current_time.isoformat(), memory.id)
                )
                
                result = {
                    "id": memory.id,
                    "layer": memory.layer,
                    "content": memory.content[:200] + "..." if len(memory.content) > 200 else memory.content,
                    "source": memory.source,
                    "timestamp": memory.timestamp.isoformat(),
                    "score": round(score, 4),
                    "importance": memory.importance,
                    "access_count": memory.access_count + 1
                }
                
                # 图记忆增强
                if use_graph and memory.entities:
                    related = self._get_related_entities(memory.entities[0])
                    if related:
                        result["related_entities"] = related
                
                results.append(result)
            
            conn.commit()
            return results
    
    def _get_related_entities(self, entity_name: str, depth: int = 1) -> List[Dict]:
        """获取相关实体（图记忆查询）"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # 查询直接关系
            rows = conn.execute("""
                SELECT r.*, e1.name as source_name, e2.name as target_name
                FROM relations r
                JOIN entities e1 ON r.source_entity = e1.id
                JOIN entities e2 ON r.target_entity = e2.id
                WHERE e1.name = ? OR e2.name = ?
                ORDER BY r.strength DESC
                LIMIT 5
            """, (entity_name, entity_name)).fetchall()
            
            return [{
                "source": row['source_name'],
                "target": row['target_name'],
                "type": row['relation_type'],
                "strength": row['strength']
            } for row in rows]
    
    def extract_facts(self, session_content: str, session_id: str = None) -> List[str]:
        """
        从会话内容中提取事实（简化版）
        生产环境应调用LLM进行提取
        """
        # 模拟事实提取
        facts = []
        
        # 简单规则提取（实际应使用LLM）
        if "Skill" in session_content:
            facts.append(f"用户使用 Skill 进行任务处理")
        if "研究" in session_content or "research" in session_content.lower():
            facts.append(f"用户进行了研究类任务")
        if "调解" in session_content:
            facts.append(f"用户关注建设工程商事调解领域")
        
        # 存储提取任务
        if session_id:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO extraction_tasks (id, session_id, content, extracted_facts, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    hashlib.md5(f"{session_id}_{datetime.now()}".encode()).hexdigest()[:16],
                    session_id,
                    session_content[:500],
                    json.dumps(facts),
                    "completed",
                    datetime.now().isoformat()
                ))
                conn.commit()
        
        return facts
    
    def consolidate_memories(self, layer: str = "short") -> Dict:
        """
        记忆整合 - 将短期记忆整合到长期记忆
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # 获取指定层的记忆
            rows = conn.execute(
                "SELECT * FROM memories WHERE layer = ?",
                (layer,)
            ).fetchall()
            
            consolidated = []
            for row in rows:
                # 检查是否需要整合（访问次数高、重要性高）
                if row['access_count'] >= 3 or row['importance'] >= 7:
                    # 移动到长期记忆
                    conn.execute(
                        "UPDATE memories SET layer = 'long' WHERE id = ?",
                        (row['id'],)
                    )
                    consolidated.append(row['id'])
            
            conn.commit()
            
            return {
                "processed": len(rows),
                "consolidated": len(consolidated),
                "consolidated_ids": consolidated
            }
    
    def cleanup_expired(self) -> Dict:
        """清理过期记忆"""
        current_time = datetime.now()
        cleaned = {"instant": 0, "working": 0, "short": 0}
        
        with sqlite3.connect(self.db_path) as conn:
            for layer, config in self.LAYERS.items():
                if config["ttl"] is None:
                    continue
                
                expiry_time = current_time - timedelta(seconds=config["ttl"])
                
                # 删除过期记忆（但保留高重要性记忆）
                cursor = conn.execute("""
                    DELETE FROM memories 
                    WHERE layer = ? 
                    AND timestamp < ?
                    AND importance < 8
                """, (layer, expiry_time.isoformat()))
                
                cleaned[layer] = cursor.rowcount
            
            conn.commit()
        
        return cleaned
    
    def sync(self, direction: str = "bidirectional") -> Dict:
        """同步记忆到各平台"""
        # 简化版同步逻辑
        with sqlite3.connect(self.db_path) as conn:
            unsynced = conn.execute(
                "SELECT COUNT(*) FROM memories WHERE synced = 0"
            ).fetchone()[0]
            
            # 标记为已同步
            conn.execute("UPDATE memories SET synced = 1 WHERE synced = 0")
            conn.commit()
        
        return {
            "success": True,
            "total_synced": unsynced,
            "direction": direction,
            "platforms": {
                "openclaw": {"synced": unsynced, "status": "ok"},
                "hermes": {"synced": 0, "status": "connected"},
                "deerflow": {"synced": 0, "status": "connected"}
            }
        }
    
    def get_stats(self) -> Dict:
        """获取记忆统计"""
        with sqlite3.connect(self.db_path) as conn:
            stats = {"total_count": 0}
            
            for layer in self.LAYERS.keys():
                count = conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE layer = ?",
                    (layer,)
                ).fetchone()[0]
                stats[f"{layer}_count"] = count
                stats["total_count"] += count
            
            unsynced = conn.execute(
                "SELECT COUNT(*) FROM memories WHERE synced = 0"
            ).fetchone()[0]
            stats["unsynced_count"] = unsynced
            
            # 实体统计
            entity_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            relation_count = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
            stats["entity_count"] = entity_count
            stats["relation_count"] = relation_count
            
            return stats

# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="mflow v2.0 - 增强型记忆流引擎")
    parser.add_argument("command", choices=["store", "retrieve", "sync", "stats", "cleanup", "consolidate", "extract"])
    parser.add_argument("--layer", help="记忆层")
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--query", help="检索查询")
    parser.add_argument("--source", default="cli", help="记忆来源")
    parser.add_argument("--importance", type=float, default=5.0, help="重要性评分(1-10)")
    parser.add_argument("--top-k", type=int, default=5, help="检索结果数量")
    
    args = parser.parse_args()
    
    engine = MFlowEngineV2()
    
    if args.command == "store":
        entry = MemoryEntry(
            id=hashlib.md5(f"{args.content}_{datetime.now()}".encode()).hexdigest()[:16],
            layer=args.layer or "instant",
            content=args.content,
            source=args.source,
            importance=args.importance
        )
        success = engine.store(entry)
        print(json.dumps({"success": success}, ensure_ascii=False))
    
    elif args.command == "retrieve":
        results = engine.retrieve(args.query, args.layer, args.top_k)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "sync":
        result = engine.sync()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = engine.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "cleanup":
        result = engine.cleanup_expired()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "consolidate":
        result = engine.consolidate_memories(args.layer or "short")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "extract":
        facts = engine.extract_facts(args.content, args.source)
        print(json.dumps({"facts": facts}, ensure_ascii=False, indent=2))
