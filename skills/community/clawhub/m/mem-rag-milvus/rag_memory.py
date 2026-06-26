#!/usr/bin/env python3
"""
RAG 记忆管理系统 - 通用版
支持多种后端：Milvus、ChromaDB、SQLite（默认）
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# 配置 - 从环境变量读取
BACKEND = os.getenv("RAG_MEMORY_BACKEND", "sqlite")  # sqlite | milvus | chromadb

# 容器环境检测 - 自动选择正确的宿主机地址
def _get_host_url(default_port: int) -> str:
    """自动检测宿主机 URL"""
    import socket
    try:
        # 尝试解析 host.docker.internal（Docker Desktop/WSL2）
        socket.gethostbyname("host.docker.internal")
        return f"http://host.docker.internal:{default_port}"
    except:
        pass
    try:
        # 尝试 Docker 网关
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.startswith("nameserver"):
                    gateway = line.split()[1].strip()
                    return f"http://{gateway}:{default_port}"
    except:
        pass
    # 默认回退到 localhost
    return f"http://localhost:{default_port}"

OLLAMA_URL = os.getenv("OLLAMA_URL", _get_host_url(11434))
MILVUS_URL = os.getenv("MILVUS_URL", _get_host_url(19530))
CHROMADB_URL = os.getenv("CHROMADB_URL", _get_host_url(8000))
COLLECTION_NAME = os.getenv("RAG_MEMORY_COLLECTION", "openclaw_memory")
BACKUP_DIR = os.getenv("RAG_MEMORY_BACKUP_DIR", "./memory_backup")
SQLITE_DB = os.getenv("RAG_MEMORY_SQLITE_DB", "./memory.db")

# 确保备份目录存在
os.makedirs(BACKUP_DIR, exist_ok=True)


class SQLiteMemory:
    """SQLite 后端 - 无需额外依赖，开箱即用"""
    
    def __init__(self, db_path: str):
        import sqlite3
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                embedding TEXT,
                timestamp TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def store(self, content: str, metadata: Dict = None, embedding: List[float] = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO memories (content, embedding, timestamp, metadata)
            VALUES (?, ?, ?, ?)
        ''', (
            content,
            json.dumps(embedding) if embedding else None,
            datetime.now().isoformat(),
            json.dumps(metadata or {})
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        # SQLite 不支持向量搜索，返回最近的记忆
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, content, timestamp, metadata
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
        ''', (top_k,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "content": row[1],
                "timestamp": row[2],
                "metadata": json.loads(row[3]) if row[3] else {},
                "distance": 0.0  # SQLite 不支持向量相似度
            })
        return results
    
    def delete(self, memory_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()


class MilvusMemory:
    """Milvus 后端 - 需要 Milvus 服务"""
    
    def __init__(self, url: str, collection: str):
        from pymilvus import MilvusClient
        self.client = MilvusClient(uri=url)
        self.collection = collection
        self._init_collection()
    
    def _init_collection(self):
        if not self.client.has_collection(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                dimension=1024,
                auto_id=True
            )
    
    def store(self, content: str, metadata: Dict = None, embedding: List[float] = None) -> int:
        result = self.client.insert(
            collection_name=self.collection,
            data=[{
                "vector": embedding or [],
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": json.dumps(metadata or {})
            }]
        )
        return result["ids"][0] if result["ids"] else None
    
    def search(self, query: str, top_k: int = 5, query_embedding: List[float] = None) -> List[Dict]:
        if not query_embedding:
            return []
        
        results = self.client.search(
            collection_name=self.collection,
            data=[query_embedding],
            limit=top_k,
            output_fields=["content", "timestamp", "metadata"]
        )
        
        formatted = []
        if results and len(results) > 0:
            for match in results[0]:
                formatted.append({
                    "id": match["id"],
                    "content": match["entity"]["content"],
                    "timestamp": match["entity"]["timestamp"],
                    "metadata": json.loads(match["entity"]["metadata"]) if match["entity"]["metadata"] else {},
                    "distance": match["distance"]
                })
        return formatted
    
    def delete(self, memory_id: int):
        self.client.delete(collection_name=self.collection, ids=[memory_id])


class RAGMemory:
    def __init__(self, backend: str = None):
        self.backend_name = backend or BACKEND
        self.ollama_url = OLLAMA_URL
        self._init_backend()
    
    def _init_backend(self):
        """初始化后端"""
        if self.backend_name == "milvus":
            self.backend = MilvusMemory(MILVUS_URL, COLLECTION_NAME)
        elif self.backend_name == "chromadb":
            # TODO: 实现 ChromaDB 后端
            print("⚠️ ChromaDB 后端暂未实现，使用 SQLite 代替")
            self.backend = SQLiteMemory(SQLITE_DB)
        else:
            self.backend = SQLiteMemory(SQLITE_DB)
            print(f"✅ 使用 SQLite 后端：{SQLITE_DB}")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取嵌入（需要 Ollama 服务）"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/embed",
                json={"model": "bge-m3", "input": text},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return data["embeddings"][0]
        except Exception as e:
            print(f"⚠️ 嵌入生成失败：{e}，将不使用向量搜索")
        return None
    
    def store_memory(self, content: str, metadata: Dict = None) -> int:
        """存储记忆"""
        embedding = self.get_embedding(content)
        
        memory_id = self.backend.store(content, metadata, embedding)
        self._backup_to_file(content, metadata, memory_id)
        
        print(f"✅ 记忆已存储：{content[:50]}...")
        return memory_id
    
    def search_memories(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索记忆"""
        embedding = self.get_embedding(query)
        
        if self.backend_name == "milvus" and embedding:
            return self.backend.search(query, top_k, embedding)
        else:
            # SQLite 返回最近记忆
            return self.backend.search(query, top_k)
    
    def _backup_to_file(self, content: str, metadata: Dict, memory_id: int):
        """备份到文件"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        backup_file = os.path.join(BACKUP_DIR, f"{date_str}.json")
        
        backups = []
        if os.path.exists(backup_file):
            with open(backup_file, "r", encoding="utf-8") as f:
                backups = json.load(f)
        
        backups.append({
            "id": memory_id,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backups, f, ensure_ascii=False, indent=2)
    
    def delete_memory(self, memory_id: int) -> bool:
        self.backend.delete(memory_id)
        print(f"✅ 记忆已删除：ID={memory_id}")
        return True
    
    def close(self):
        if hasattr(self.backend, 'close'):
            self.backend.close()


# 全局实例
_memory_instance: Optional[RAGMemory] = None

def get_memory() -> RAGMemory:
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = RAGMemory()
    return _memory_instance

def store(content: str, metadata: Dict = None) -> int:
    return get_memory().store_memory(content, metadata)

def search(query: str, top_k: int = 5) -> List[Dict]:
    return get_memory().search_memories(query, top_k)


if __name__ == "__main__":
    print(f"🚀 RAG 记忆系统 (后端：{BACKEND})")
    
    # 测试
    memory_id = store("测试记忆", {"type": "test"})
    print(f"存储 ID: {memory_id}")
    
    results = search("测试")
    print(f"搜索结果：{results}")
