#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System - Dual Brain Architecture
SQLite (Left Brain) + LanceDB (Right Brain)
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import numpy as np

# 尝试导入Ollama嵌入（可选）
try:
    from ollama_embedding import OllamaEmbedding, OllamaMemoryEmbedding
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class MemorySystem:
    """Complete memory management system with dual-brain architecture"""
    
    def __init__(self, db_path: str = None, config: Dict = None):
        """
        Initialize Memory System
        
        Args:
            db_path: Path to SQLite database
            config: Configuration dictionary
        """
        if db_path is None:
            db_path = "memory/database/xiaozhi_memory.db"
        
        self.db_path = db_path
        self.config = config or {}
        self.conn = None
        self.vector_db = None
        self.ollama = None
        
        # Default configuration
        self.min_confidence = self.config.get('min_confidence', 0.3)
        self.cleanup_days = self.config.get('cleanup_interval_days', 90)
        
        # Initialize Ollama if available and configured
        if OLLAMA_AVAILABLE and self.config.get('use_ollama', False):
            ollama_model = self.config.get('ollama_model', 'nomic-embed-text')
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            self.ollama = OllamaEmbedding(model=ollama_model, base_url=ollama_url)
            if not self.ollama.check_connection():
                print("Warning: Ollama service not available, falling back to text search")
                self.ollama = None
    
    def initialize(self) -> bool:
        """
        Initialize database and create tables
        
        Returns:
            True if successful
        """
        # Create directory if not exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connect to SQLite
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create tables
        self._create_tables()
        
        # Try to initialize LanceDB (optional)
        try:
            import lancedb
            vector_db_path = self.config.get('vector_db', 
                os.path.join(os.path.dirname(self.db_path), 'lancedb'))
            os.makedirs(vector_db_path, exist_ok=True)
            self.vector_db = lancedb.connect(vector_db_path)
        except ImportError:
            print("LanceDB not available, using SQLite only")
        
        return True
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Main memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                tags TEXT,
                importance INTEGER DEFAULT 5,
                confidence REAL DEFAULT 0.8,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)')
        
        # Memory links table (for associations)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id_1 INTEGER,
                memory_id_2 INTEGER,
                link_type TEXT,
                strength REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (memory_id_1) REFERENCES memories(id),
                FOREIGN KEY (memory_id_2) REFERENCES memories(id)
            )
        ''')
        
        self.conn.commit()
    
    def save(self, type: str, title: str, content: str = None,
             category: str = None, tags: List[str] = None,
             importance: int = 5, confidence: float = 0.8,
             source: str = None) -> int:
        """
        Save a new memory
        
        Args:
            type: Memory type (learning, event, preference, etc.)
            title: Memory title
            content: Memory content
            category: Memory category
            tags: List of tags
            importance: Importance score (1-10)
            confidence: Confidence score (0.0-1.0)
            source: Source of the memory
            
        Returns:
            Memory ID
        """
        cursor = self.conn.cursor()
        
        tags_json = json.dumps(tags) if tags else None
        
        cursor.execute('''
            INSERT INTO memories (type, title, content, category, tags, 
                                importance, confidence, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (type, title, content, category, tags_json, 
              importance, confidence, source))
        
        self.conn.commit()
        memory_id = cursor.lastrowid
        
        # Add to vector database if available
        if self.vector_db and content:
            self._add_to_vector_db(memory_id, content)
        
        return memory_id
    
    def query(self, type: str = None, category: str = None,
              min_importance: int = None, limit: int = 100) -> List[Dict]:
        """
        Query memories (left brain - structured)
        
        Args:
            type: Filter by type
            category: Filter by category
            min_importance: Minimum importance
            limit: Maximum results
            
        Returns:
            List of memories
        """
        cursor = self.conn.cursor()
        
        query = 'SELECT * FROM memories WHERE 1=1'
        params = []
        
        if type:
            query += ' AND type = ?'
            params.append(type)
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if min_importance:
            query += ' AND importance >= ?'
            params.append(min_importance)
        
        query += ' ORDER BY importance DESC, created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        memories = []
        for row in cursor.fetchall():
            memory = dict(row)
            if memory['tags']:
                memory['tags'] = json.loads(memory['tags'])
            memories.append(memory)
        
        return memories
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Semantic search (right brain - vectors)
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of similar memories
        """
        # Try Ollama semantic search first
        if self.ollama and self.ollama.check_connection():
            return self._ollama_search(query, limit)
        
        # Fall back to vector DB if available
        if self.vector_db:
            return self._vector_search(query, limit)
        
        # Fall back to text search
        return self._text_search(query, limit)
    
    def _ollama_search(self, query: str, limit: int) -> List[Dict]:
        """Ollama semantic search"""
        try:
            # Generate query embedding
            query_emb = self.ollama.embed(query)
            if not query_emb:
                return self._text_search(query, limit)
            
            # Get all memories
            memories = self.query(limit=1000)
            
            # Calculate similarities
            results = []
            for mem in memories:
                text = f"{mem.get('title', '')} {mem.get('content', '')}"
                mem_emb = self.ollama.embed(text)
                if mem_emb:
                    similarity = self.ollama.similarity(query_emb, mem_emb)
                    results.append((mem, similarity))
            
            # Sort by similarity
            results.sort(key=lambda x: x[1], reverse=True)
            
            # Return top results
            return [r[0] for r in results[:limit]]
            
        except Exception as e:
            print(f"Ollama search failed: {e}")
            return self._text_search(query, limit)
    
    def _vector_search(self, query: str, limit: int) -> List[Dict]:
        """Vector database search"""
        # Vector search implementation would go here
        # For now, use text search
        return self._text_search(query, limit)
    
    def _text_search(self, query: str, limit: int) -> List[Dict]:
        """Fallback text search"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
            ORDER BY importance DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
        
        memories = []
        for row in cursor.fetchall():
            memory = dict(row)
            if memory['tags']:
                memory['tags'] = json.loads(memory['tags'])
            memories.append(memory)
        
        return memories
    
    def get(self, memory_id: int) -> Optional[Dict]:
        """
        Get a specific memory
        
        Args:
            memory_id: Memory ID
            
        Returns:
            Memory dict or None
        """
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
        row = cursor.fetchone()
        
        if row:
            memory = dict(row)
            if memory['tags']:
                memory['tags'] = json.loads(memory['tags'])
            return memory
        
        return None
    
    def update(self, memory_id: int, **kwargs) -> bool:
        """
        Update a memory
        
        Args:
            memory_id: Memory ID
            **kwargs: Fields to update
            
        Returns:
            True if successful
        """
        allowed_fields = ['title', 'content', 'category', 'tags', 
                         'importance', 'confidence', 'source']
        
        updates = {}
        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'tags' and isinstance(value, list):
                    value = json.dumps(value)
                updates[key] = value
        
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
        values = list(updates.values()) + [memory_id]
        
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE memories SET {set_clause} WHERE id = ?', values)
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete(self, memory_id: int) -> bool:
        """
        Delete a memory
        
        Args:
            memory_id: Memory ID
            
        Returns:
            True if successful
        """
        cursor = self.conn.cursor()
        
        cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0
    
    def cleanup(self, min_confidence: float = None, 
                days_old: int = None) -> int:
        """
        Clean up old, low-confidence memories
        
        Args:
            min_confidence: Minimum confidence threshold
            days_old: Age threshold in days
            
        Returns:
            Number of deleted memories
        """
        min_confidence = min_confidence or self.min_confidence
        days_old = days_old or self.cleanup_days
        
        cursor = self.conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cursor.execute('''
            DELETE FROM memories
            WHERE confidence < ?
            AND importance < 5
            AND datetime(created_at) < datetime(?)
        ''', (min_confidence, cutoff_date.isoformat()))
        
        self.conn.commit()
        return cursor.rowcount
    
    def export(self, format: str = 'json') -> str:
        """
        Export all memories
        
        Args:
            format: Export format (json)
            
        Returns:
            Exported data string
        """
        memories = self.query(limit=1000000)
        
        if format == 'json':
            return json.dumps(memories, indent=2, ensure_ascii=False)
        
        raise ValueError(f"Unsupported format: {format}")
    
    def import_data(self, data: str, format: str = 'json') -> int:
        """
        Import memories
        
        Args:
            data: Data string
            format: Import format (json)
            
        Returns:
            Number of imported memories
        """
        if format == 'json':
            memories = json.loads(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        count = 0
        for memory in memories:
            self.save(
                type=memory.get('type'),
                title=memory.get('title'),
                content=memory.get('content'),
                category=memory.get('category'),
                tags=memory.get('tags'),
                importance=memory.get('importance', 5),
                confidence=memory.get('confidence', 0.8),
                source=memory.get('source')
            )
            count += 1
        
        return count
    
    def stats(self) -> Dict:
        """
        Get memory statistics
        
        Returns:
            Statistics dict
        """
        cursor = self.conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM memories')
        total = cursor.fetchone()[0]
        
        # By type
        cursor.execute('''
            SELECT type, COUNT(*) as count
            FROM memories
            GROUP BY type
        ''')
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By category
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM memories
            WHERE category IS NOT NULL
            GROUP BY category
        ''')
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Average importance
        cursor.execute('SELECT AVG(importance) FROM memories')
        avg_importance = cursor.fetchone()[0]
        
        return {
            'total': total,
            'by_type': by_type,
            'by_category': by_category,
            'avg_importance': avg_importance
        }
    
    def _add_to_vector_db(self, memory_id: int, content: str):
        """Add memory to vector database (placeholder)"""
        # This would use sentence-transformers to create embeddings
        # and store in LanceDB
        pass
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# CLI interface
if __name__ == "__main__":
    import sys
    
    memory = MemorySystem()
    memory.initialize()
    
    print("="*70)
    print("Memory System - Dual Brain Architecture")
    print("="*70)
    
    # Show stats
    stats = memory.stats()
    print(f"\nTotal memories: {stats['total']}")
    print(f"Average importance: {stats['avg_importance']:.2f}")
    
    print("\nBy type:")
    for type_name, count in stats['by_type'].items():
        print(f"  {type_name}: {count}")
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(f"\nSearching for: {query}")
        results = memory.search(query)
        print(f"Found: {len(results)} results")
        
        for i, mem in enumerate(results[:5], 1):
            print(f"\n{i}. {mem['title']} (importance: {mem['importance']})")
            if mem['content']:
                print(f"   {mem['content'][:100]}...")
    
    memory.close()
