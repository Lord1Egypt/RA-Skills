#!/usr/bin/env python3
"""
Simple SQLite cache for task classifications and model availability.
"""

import sqlite3
import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Any


class RouterCache:
    """
    SQLite-based cache for smart router.
    
    Caches:
    - Task classifications (task_hash -> classification)
    - Model availability (endpoint -> available models)
    - Health check results (endpoint -> health status)
    """
    
    def __init__(self, db_path: str = "cache/router.db", ttl_seconds: int = 86400):
        """
        Initialize cache.
        
        Args:
            db_path: Path to SQLite database
            ttl_seconds: Time-to-live for cached entries (default 24 hours)
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS classifications (
                    task_hash TEXT PRIMARY KEY,
                    score INTEGER,
                    reason TEXT,
                    created_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS model_availability (
                    endpoint TEXT PRIMARY KEY,
                    models TEXT,  -- JSON list
                    created_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_status (
                    endpoint TEXT PRIMARY KEY,
                    status TEXT,  -- JSON dict
                    created_at REAL
                )
            """)
            conn.commit()
    
    def _hash_task(self, task: str) -> str:
        """Create hash for task text."""
        return hashlib.sha256(task.lower().strip().encode()).hexdigest()[:16]
    
    def get_classification(self, task: str) -> Optional[tuple[int, str]]:
        """
        Get cached classification for task.
        
        Returns: (score, reason) or None if not cached/expired
        """
        task_hash = self._hash_task(task)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT score, reason, created_at FROM classifications WHERE task_hash = ?",
                (task_hash,)
            )
            row = cursor.fetchone()
            
            if row:
                score, reason, created_at = row
                # Check TTL
                if time.time() - created_at < self.ttl_seconds:
                    return score, reason
                else:
                    # Expired - delete
                    conn.execute("DELETE FROM classifications WHERE task_hash = ?", (task_hash,))
                    conn.commit()
        
        return None
    
    def set_classification(self, task: str, score: int, reason: str):
        """Cache classification for task."""
        task_hash = self._hash_task(task)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO classifications (task_hash, score, reason, created_at)
                   VALUES (?, ?, ?, ?)""",
                (task_hash, score, reason, time.time())
            )
            conn.commit()
    
    def get_available_models(self, endpoint: str) -> Optional[list[str]]:
        """
        Get cached available models for endpoint.
        
        Returns: List of model names or None if not cached/expired
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT models, created_at FROM model_availability WHERE endpoint = ?",
                (endpoint,)
            )
            row = cursor.fetchone()
            
            if row:
                models_json, created_at = row
                # Check TTL (shorter for model availability - 5 minutes)
                if time.time() - created_at < 300:  # 5 minutes
                    return json.loads(models_json)
                else:
                    conn.execute("DELETE FROM model_availability WHERE endpoint = ?", (endpoint,))
                    conn.commit()
        
        return None
    
    def set_available_models(self, endpoint: str, models: list[str]):
        """Cache available models for endpoint."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO model_availability (endpoint, models, created_at)
                   VALUES (?, ?, ?)""",
                (endpoint, json.dumps(models), time.time())
            )
            conn.commit()
    
    def get_health_status(self, endpoint: str) -> Optional[dict]:
        """
        Get cached health status for endpoint.
        
        Returns: Health dict or None if not cached/expired
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT status, created_at FROM health_status WHERE endpoint = ?",
                (endpoint,)
            )
            row = cursor.fetchone()
            
            if row:
                status_json, created_at = row
                # Check TTL (very short for health - 30 seconds)
                if time.time() - created_at < 30:
                    return json.loads(status_json)
                else:
                    conn.execute("DELETE FROM health_status WHERE endpoint = ?", (endpoint,))
                    conn.commit()
        
        return None
    
    def set_health_status(self, endpoint: str, status: dict):
        """Cache health status for endpoint."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO health_status (endpoint, status, created_at)
                   VALUES (?, ?, ?)""",
                (endpoint, json.dumps(status), time.time())
            )
            conn.commit()
    
    def clear(self):
        """Clear all cached entries."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM classifications")
            conn.execute("DELETE FROM model_availability")
            conn.execute("DELETE FROM health_status")
            conn.commit()
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        with sqlite3.connect(self.db_path) as conn:
            classifications = conn.execute("SELECT COUNT(*) FROM classifications").fetchone()[0]
            models = conn.execute("SELECT COUNT(*) FROM model_availability").fetchone()[0]
            health = conn.execute("SELECT COUNT(*) FROM health_status").fetchone()[0]
        
        return {
            "classifications": classifications,
            "model_availability": models,
            "health_status": health
        }


# Global cache instance
_cache_instance: Optional[RouterCache] = None


def get_cache(db_path: str = "cache/router.db", ttl_seconds: int = 86400) -> RouterCache:
    """Get or create global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RouterCache(db_path, ttl_seconds)
    return _cache_instance


if __name__ == "__main__":
    # Test cache
    cache = RouterCache("test_cache.db")
    
    # Test classification cache
    cache.set_classification("What is 2+2?", 1, "simple-qa")
    result = cache.get_classification("What is 2+2?")
    print(f"Cached classification: {result}")
    
    # Test model availability cache
    cache.set_available_models("http://localhost:11434", ["llama3.2", "qwen2.5:14b"])
    models = cache.get_available_models("http://localhost:11434")
    print(f"Cached models: {models}")
    
    # Stats
    print(f"Cache stats: {cache.get_stats()}")
    
    # Cleanup
    import os
    os.remove("test_cache.db")
    print("Cache test passed!")
