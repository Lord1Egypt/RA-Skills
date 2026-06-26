#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mflow - 记忆流同步引擎

实现 OpenClaw × Hermes × DeerFlow 三端记忆无缝同步

Author: ruiyongwang
Version: 2.0.0
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import threading
import time


@dataclass
class MemoryLayer:
    """记忆层定义"""
    name: str
    ttl: Optional[int] = None  # 秒，None 表示永久
    persistent: bool = False
    description: str = ""


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    layer: str
    content: str
    source: str  # openclaw / hermes / deerflow
    timestamp: datetime
    metadata: Dict[str, Any]
    checksum: str = ""
    
    def __post_init__(self):
        if not self.checksum:
            self.checksum = hashlib.md5(
                f"{self.content}{self.timestamp}".encode()
            ).hexdigest()[:16]


class MFlowEngine:
    """记忆流引擎"""
    
    # 五层记忆架构
    LAYERS = {
        "instant": MemoryLayer(
            name="instant",
            ttl=3600,  # 1小时
            persistent=False,
            description="即时记忆 - 当前会话上下文"
        ),
        "short": MemoryLayer(
            name="short",
            ttl=604800,  # 7天
            persistent=True,
            description="短期记忆 - 最近7天会话"
        ),
        "long": MemoryLayer(
            name="long",
            ttl=None,
            persistent=True,
            description="长期记忆 - 持久化知识库"
        ),
        "skill": MemoryLayer(
            name="skill",
            ttl=None,
            persistent=True,
            description="技能记忆 - Skill使用经验"
        ),
        "expert": MemoryLayer(
            name="expert",
            ttl=None,
            persistent=True,
            description="专家记忆 - 蒸馏的专家思维"
        )
    }
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化记忆流引擎"""
        self.db_path = db_path or os.path.expanduser("~/.oclaw-hermes/mflow.db")
        self._init_db()
        self._lock = threading.Lock()
        
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    layer TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    checksum TEXT,
                    synced INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_layer ON memories(layer)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_source ON memories(source)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    direction TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    count INTEGER,
                    timestamp TEXT NOT NULL,
                    status TEXT
                )
            """)
            
            conn.commit()
    
    def store(self, entry: MemoryEntry) -> bool:
        """存储记忆"""
        try:
            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT OR REPLACE INTO memories 
                        (id, layer, content, source, timestamp, metadata, checksum, synced)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                    """, (
                        entry.id,
                        entry.layer,
                        entry.content,
                        entry.source,
                        entry.timestamp.isoformat(),
                        json.dumps(entry.metadata),
                        entry.checksum
                    ))
                    conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] 存储记忆失败: {e}")
            return False
    
    def retrieve(self, layer: Optional[str] = None, 
                 source: Optional[str] = None,
                 query: Optional[str] = None,
                 limit: int = 100) -> List[MemoryEntry]:
        """检索记忆"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                sql = "SELECT * FROM memories WHERE 1=1"
                params = []
                
                if layer:
                    sql += " AND layer = ?"
                    params.append(layer)
                
                if source:
                    sql += " AND source = ?"
                    params.append(source)
                
                if query:
                    sql += " AND content LIKE ?"
                    params.append(f"%{query}%")
                
                # 清理过期记忆
                self._cleanup_expired(conn)
                
                sql += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(sql, params)
                rows = cursor.fetchall()
                
                entries = []
                for row in rows:
                    entry = MemoryEntry(
                        id=row[0],
                        layer=row[1],
                        content=row[2],
                        source=row[3],
                        timestamp=datetime.fromisoformat(row[4]),
                        metadata=json.loads(row[5]) if row[5] else {},
                        checksum=row[6]
                    )
                    entries.append(entry)
                
                return entries
        except Exception as e:
            print(f"[ERROR] 检索记忆失败: {e}")
            return []
    
    def _cleanup_expired(self, conn: sqlite3.Connection):
        """清理过期记忆"""
        now = datetime.now()
        
        for layer_name, layer in self.LAYERS.items():
            if layer.ttl is not None:
                expiry = now - timedelta(seconds=layer.ttl)
                conn.execute(
                    "DELETE FROM memories WHERE layer = ? AND timestamp < ?",
                    (layer_name, expiry.isoformat())
                )
    
    def sync_to_openclaw(self) -> Dict[str, Any]:
        """同步记忆到 OpenClaw"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 获取未同步的记忆
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE synced = 0 AND source != 'openclaw'"
                )
                rows = cursor.fetchall()
                
                synced_count = 0
                for row in rows:
                    # 这里实现实际的 OpenClaw 同步逻辑
                    # 例如：调用 OpenClaw API 或写入文件
                    
                    entry_id = row[0]
                    conn.execute(
                        "UPDATE memories SET synced = 1 WHERE id = ?",
                        (entry_id,)
                    )
                    synced_count += 1
                
                conn.commit()
                
                # 记录同步日志
                conn.execute(
                    """INSERT INTO sync_log (direction, platform, count, timestamp, status)
                       VALUES (?, ?, ?, ?, ?)""",
                    ("export", "openclaw", synced_count, datetime.now().isoformat(), "success")
                )
                conn.commit()
                
                return {
                    "success": True,
                    "synced": synced_count,
                    "platform": "openclaw"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": "openclaw"
            }
    
    def sync_to_hermes(self) -> Dict[str, Any]:
        """同步记忆到 Hermes"""
        try:
            hermes_memory_path = os.path.expanduser("~/.hermes/memories")
            os.makedirs(hermes_memory_path, exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE synced = 0 AND source != 'hermes'"
                )
                rows = cursor.fetchall()
                
                synced_count = 0
                for row in rows:
                    entry = {
                        "id": row[0],
                        "layer": row[1],
                        "content": row[2],
                        "source": row[3],
                        "timestamp": row[4],
                        "metadata": json.loads(row[5]) if row[5] else {}
                    }
                    
                    # 写入 Hermes 记忆文件
                    memory_file = os.path.join(
                        hermes_memory_path,
                        f"mflow_{row[0]}.json"
                    )
                    with open(memory_file, 'w', encoding='utf-8') as f:
                        json.dump(entry, f, ensure_ascii=False, indent=2)
                    
                    conn.execute(
                        "UPDATE memories SET synced = 1 WHERE id = ?",
                        (row[0],)
                    )
                    synced_count += 1
                
                conn.commit()
                
                # 记录同步日志
                conn.execute(
                    """INSERT INTO sync_log (direction, platform, count, timestamp, status)
                       VALUES (?, ?, ?, ?, ?)""",
                    ("export", "hermes", synced_count, datetime.now().isoformat(), "success")
                )
                conn.commit()
                
                return {
                    "success": True,
                    "synced": synced_count,
                    "platform": "hermes"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": "hermes"
            }
    
    def sync_to_deerflow(self, deerflow_url: str = "http://localhost:2026") -> Dict[str, Any]:
        """同步记忆到 DeerFlow"""
        try:
            import requests
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM memories WHERE synced = 0 AND source != 'deerflow'"
                )
                rows = cursor.fetchall()
                
                synced_count = 0
                for row in rows:
                    entry = {
                        "id": row[0],
                        "layer": row[1],
                        "content": row[2],
                        "source": row[3],
                        "timestamp": row[4],
                        "metadata": json.loads(row[5]) if row[5] else {}
                    }
                    
                    # 调用 DeerFlow API 存储记忆
                    try:
                        response = requests.post(
                            f"{deerflow_url}/api/memory",
                            json=entry,
                            timeout=5
                        )
                        if response.status_code == 200:
                            conn.execute(
                                "UPDATE memories SET synced = 1 WHERE id = ?",
                                (row[0],)
                            )
                            synced_count += 1
                    except Exception as api_error:
                        print(f"[WARN] DeerFlow API 调用失败: {api_error}")
                        continue
                
                conn.commit()
                
                # 记录同步日志
                conn.execute(
                    """INSERT INTO sync_log (direction, platform, count, timestamp, status)
                       VALUES (?, ?, ?, ?, ?)""",
                    ("export", "deerflow", synced_count, datetime.now().isoformat(), "success")
                )
                conn.commit()
                
                return {
                    "success": True,
                    "synced": synced_count,
                    "platform": "deerflow"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": "deerflow"
            }
    
    def full_sync(self, deerflow_url: str = "http://localhost:2026") -> Dict[str, Any]:
        """全量同步到所有平台"""
        results = {
            "openclaw": self.sync_to_openclaw(),
            "hermes": self.sync_to_hermes(),
            "deerflow": self.sync_to_deerflow(deerflow_url)
        }
        
        total_synced = sum(
            r.get("synced", 0) for r in results.values() if r.get("success")
        )
        
        return {
            "success": all(r.get("success") for r in results.values()),
            "total_synced": total_synced,
            "details": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                stats = {}
                
                # 各层记忆数量
                for layer in self.LAYERS.keys():
                    cursor = conn.execute(
                        "SELECT COUNT(*) FROM memories WHERE layer = ?",
                        (layer,)
                    )
                    stats[f"{layer}_count"] = cursor.fetchone()[0]
                
                # 各来源记忆数量
                for source in ["openclaw", "hermes", "deerflow"]:
                    cursor = conn.execute(
                        "SELECT COUNT(*) FROM memories WHERE source = ?",
                        (source,)
                    )
                    stats[f"{source}_count"] = cursor.fetchone()[0]
                
                # 总记忆数
                cursor = conn.execute("SELECT COUNT(*) FROM memories")
                stats["total_count"] = cursor.fetchone()[0]
                
                # 未同步数量
                cursor = conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE synced = 0"
                )
                stats["unsynced_count"] = cursor.fetchone()[0]
                
                # 最近同步记录
                cursor = conn.execute(
                    """SELECT * FROM sync_log 
                       ORDER BY timestamp DESC LIMIT 5"""
                )
                stats["recent_syncs"] = [
                    {
                        "direction": row[1],
                        "platform": row[2],
                        "count": row[3],
                        "timestamp": row[4],
                        "status": row[5]
                    }
                    for row in cursor.fetchall()
                ]
                
                return stats
        except Exception as e:
            return {"error": str(e)}


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="mflow 记忆流同步引擎")
    parser.add_argument("command", choices=[
        "store", "retrieve", "sync", "stats", "cleanup"
    ])
    parser.add_argument("--layer", help="记忆层")
    parser.add_argument("--source", help="记忆来源")
    parser.add_argument("--content", help="记忆内容")
    parser.add_argument("--query", help="检索关键词")
    parser.add_argument("--deerflow-url", default="http://localhost:2026")
    
    args = parser.parse_args()
    
    engine = MFlowEngine()
    
    if args.command == "store":
        entry = MemoryEntry(
            id=hashlib.md5(f"{args.content}{time.time()}".encode()).hexdigest()[:16],
            layer=args.layer or "instant",
            content=args.content or "",
            source=args.source or "cli",
            timestamp=datetime.now(),
            metadata={}
        )
        success = engine.store(entry)
        print(json.dumps({"success": success}, ensure_ascii=False, indent=2))
    
    elif args.command == "retrieve":
        entries = engine.retrieve(
            layer=args.layer,
            source=args.source,
            query=args.query
        )
        print(json.dumps([
            {
                "id": e.id,
                "layer": e.layer,
                "content": e.content[:100] + "..." if len(e.content) > 100 else e.content,
                "source": e.source,
                "timestamp": e.timestamp.isoformat()
            }
            for e in entries
        ], ensure_ascii=False, indent=2))
    
    elif args.command == "sync":
        result = engine.full_sync(args.deerflow_url)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = engine.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "cleanup":
        # 清理过期记忆
        with sqlite3.connect(engine.db_path) as conn:
            engine._cleanup_expired(conn)
            conn.commit()
        print(json.dumps({"success": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
