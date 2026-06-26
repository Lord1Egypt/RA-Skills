import sqlite3
import os
from datetime import datetime
import numpy as np

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/memory.db')

class MemoryDB:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_tables()
    
    def _init_tables(self):
        cursor = self.conn.cursor()
        
        # 记忆主表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            type TEXT DEFAULT 'fact', -- fact/preference/project/todo/other
            source TEXT DEFAULT 'conversation', -- conversation/manual
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expire_at TIMESTAMP,
            is_deleted BOOLEAN DEFAULT 0
        )
        ''')
        
        # 向量表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER NOT NULL,
            vector BLOB NOT NULL,
            FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
        )
        ''')
        
        # 配置表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
    
    def add_memory(self, content, memory_type='fact', source='conversation', expire_days=90):
        cursor = self.conn.cursor()
        expire_at = None
        if expire_days:
            expire_at = datetime.fromtimestamp(datetime.now().timestamp() + expire_days * 86400).isoformat()
        
        cursor.execute('''
        INSERT INTO memories (content, type, source, expire_at)
        VALUES (?, ?, ?, ?)
        ''', (content, memory_type, source, expire_at))
        memory_id = cursor.lastrowid
        self.conn.commit()
        return memory_id
    
    def add_vector(self, memory_id, vector):
        cursor = self.conn.cursor()
        vector_blob = vector.tobytes()
        cursor.execute('''
        INSERT INTO memory_vectors (memory_id, vector)
        VALUES (?, ?)
        ''', (memory_id, vector_blob))
        self.conn.commit()
    
    def search_similar(self, query_vector, top_k=5):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT m.id, m.content, m.type, m.created_at, v.vector
        FROM memories m
        JOIN memory_vectors v ON m.id = v.memory_id
        WHERE m.is_deleted = 0 AND (m.expire_at IS NULL OR m.expire_at > ?)
        ''', (datetime.now().isoformat(),))
        
        results = []
        for row in cursor.fetchall():
            mem_id, content, mem_type, created_at, vec_blob = row
            vec = np.frombuffer(vec_blob, dtype=np.float32)
            # 计算余弦相似度
            similarity = np.dot(query_vector, vec) / (np.linalg.norm(query_vector) * np.linalg.norm(vec))
            results.append({
                'id': mem_id,
                'content': content,
                'type': mem_type,
                'created_at': created_at,
                'similarity': float(similarity)
            })
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def list_memories(self, limit=100):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, content, type, created_at, expire_at
        FROM memories
        WHERE is_deleted = 0
        ORDER BY created_at DESC
        LIMIT ?
        ''', (limit,))
        
        return [
            {
                'id': row[0],
                'content': row[1],
                'type': row[2],
                'created_at': row[3],
                'expire_at': row[4]
            }
            for row in cursor.fetchall()
        ]
    
    def delete_memory(self, memory_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE memories SET is_deleted = 1 WHERE id = ?
        ''', (memory_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_memory(self, memory_id, content):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE memories SET content = ?, updated_at = ? WHERE id = ?
        ''', (content, datetime.now().isoformat(), memory_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def close(self):
        self.conn.close()
