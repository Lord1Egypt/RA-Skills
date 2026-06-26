"""
SQLite Storage Backend
"""
import json
import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from memory_system.storage.base import StorageBackend, MemoryEntry


class SQLiteStorage(StorageBackend):
    """SQLite-based storage for better performance"""
    
    def __init__(self, base_path: str = "./memory.db"):
        """
        Initialize SQLite storage
        
        Args:
            base_path: Path to SQLite database file
        """
        self.db_path = Path(base_path)
        self._conn: Optional[sqlite3.Connection] = None
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection"""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._init_db()
        return self._conn
    
    def _init_db(self):
        """Initialize database schema"""
        conn = self._conn
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT,
                embedding TEXT,
                metadata TEXT,
                is_shared INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)
        ''')
        
        conn.commit()
    
    def init(self):
        """Initialize the storage"""
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._get_connection()
    
    def save(self, entry: MemoryEntry) -> bool:
        """Save a memory entry"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO memories 
                (id, content, timestamp, tags, embedding, metadata, is_shared)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry.id,
                entry.content,
                entry.timestamp,
                json.dumps(entry.tags, ensure_ascii=False) if entry.tags else '[]',
                json.dumps(entry.embedding, ensure_ascii=False) if entry.embedding else None,
                json.dumps(entry.metadata or {}, ensure_ascii=False),
                1 if getattr(entry, 'is_shared', False) else 0
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving entry {entry.id}: {e}")
            return False
    
    def load(self, entry_id: str) -> Optional[MemoryEntry]:
        """Load a memory entry by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memories WHERE id = ?', (entry_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_entry(row)
    
    def delete(self, entry_id: str) -> bool:
        """Delete a memory entry"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM memories WHERE id = ?', (entry_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    def list_all(self) -> List[MemoryEntry]:
        """List all memory entries"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memories ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        return [self._row_to_entry(row) for row in rows]
    
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """Search entries by tags"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build query for multiple tags
        placeholders = ','.join(['?' for _ in tags])
        cursor.execute(f'''
            SELECT * FROM memories 
            WHERE tags LIKE '%' || ? || '%'
            ORDER BY timestamp DESC
        ''', (tags[0],))
        
        rows = cursor.fetchall()
        
        # Filter for all tags
        results = []
        for row in rows:
            entry = self._row_to_entry(row)
            if entry.tags:
                entry_tags = set(t.lower() for t in entry.tags)
                if all(t.lower() in entry_tags for t in tags):
                    results.append(entry)
        
        return results
    
    def _row_to_entry(self, row: sqlite3.Row) -> MemoryEntry:
        """Convert a database row to MemoryEntry"""
        tags = json.loads(row['tags']) if row['tags'] else []
        embedding = json.loads(row['embedding']) if row['embedding'] else None
        metadata = json.loads(row['metadata']) if row['metadata'] else {}
        
        return MemoryEntry(
            id=row['id'],
            content=row['content'],
            timestamp=row['timestamp'],
            tags=tags,
            embedding=embedding,
            metadata=metadata,
            is_shared=bool(row['is_shared'])
        )
    
    def count(self) -> int:
        """Count total memories"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM memories')
        return cursor.fetchone()[0]
    
    def vacuum(self):
        """Optimize database"""
        conn = self._get_connection()
        conn.execute('VACUUM')
    
    def close(self):
        """Close database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
