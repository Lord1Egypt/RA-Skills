#!/usr/bin/env python3
"""
DGRA Cache Layer
Phase 1 - v0.4 Architecture

SQLite-backed cache with TTL support for all API responses.
Schema designed for fast lookup by gene, variant, or tissue.
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class CacheEntry:
    """Represents a cached API response."""
    cache_key: str        # Composite key: "api_name:query_params"
    api_name: str         # ensembl, uniprot, gtex, gnomad, ncbi
    query_params: str     # JSON-encoded query parameters
    response_data: str    # JSON-encoded response
    created_at: float     # Unix timestamp
    expires_at: float     # Unix timestamp (TTL)
    http_status: int      # 200, 404, 500, etc.
    confidence: str       # high, medium, low


class DGRACache:
    """
    SQLite cache manager for DGRA API responses.
    
    Usage:
        cache = DGRACache(Path("~/.openclaw/skills/dgra-genomic-risk/cache/dgra_cache.db"))
        
        # Store
        cache.set("uniprot:MYH11", {"domains": [...]}, ttl_days=30)
        
        # Retrieve
        data = cache.get("uniprot:MYH11")
        if data:
            print(f"Cache hit: {data}")
        else:
            print("Cache miss - query API")
    """
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS api_cache (
        cache_key TEXT PRIMARY KEY,
        api_name TEXT NOT NULL,
        query_params TEXT,
        response_data TEXT NOT NULL,
        created_at REAL NOT NULL,
        expires_at REAL NOT NULL,
        http_status INTEGER,
        confidence TEXT DEFAULT 'medium',
        hit_count INTEGER DEFAULT 0
    );
    
    CREATE INDEX IF NOT EXISTS idx_api_name ON api_cache(api_name);
    CREATE INDEX IF NOT EXISTS idx_expires ON api_cache(expires_at);
    
    -- Metadata table for cache statistics
    CREATE TABLE IF NOT EXISTS cache_stats (
        api_name TEXT PRIMARY KEY,
        hits INTEGER DEFAULT 0,
        misses INTEGER DEFAULT 0,
        errors INTEGER DEFAULT 0,
        last_access REAL
    );
    """
    
    def __init__(self, db_path: Path, default_ttl_days: int = 30):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl_days * 86400  # seconds
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        with self._connection() as conn:
            conn.executescript(self.SCHEMA)
            conn.commit()
    
    @contextmanager
    def _connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _make_key(self, api_name: str, **params) -> str:
        """Generate a deterministic cache key from API name and parameters."""
        # Sort params for deterministic key generation
        sorted_params = json.dumps(params, sort_keys=True, separators=(',', ':'))
        return f"{api_name}:{sorted_params}"
    
    def get(self, api_name: str, **params) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if not expired.
        Returns None on cache miss or expired entry.
        """
        cache_key = self._make_key(api_name, **params)
        now = time.time()
        
        with self._connection() as conn:
            # Check if entry exists and is not expired
            cursor = conn.execute(
                """SELECT response_data, http_status, confidence, expires_at 
                   FROM api_cache 
                   WHERE cache_key = ? AND expires_at > ?""",
                (cache_key, now)
            )
            row = cursor.fetchone()
            
            if row:
                # Update hit count and stats
                conn.execute(
                    "UPDATE api_cache SET hit_count = hit_count + 1 WHERE cache_key = ?",
                    (cache_key,)
                )
                conn.execute(
                    """INSERT INTO cache_stats (api_name, hits, last_access)
                        VALUES (?, 1, ?)
                        ON CONFLICT(api_name) DO UPDATE SET
                        hits = hits + 1,
                        last_access = excluded.last_access""",
                    (api_name, now)
                )
                conn.commit()
                
                try:
                    return {
                        "data": json.loads(row["response_data"]),
                        "http_status": row["http_status"],
                        "confidence": row["confidence"],
                        "from_cache": True,
                        "expires_at": row["expires_at"],
                    }
                except json.JSONDecodeError:
                    # Corrupted cache entry — treat as miss and delete
                    conn.execute("DELETE FROM api_cache WHERE cache_key = ?", (cache_key,))
                    conn.commit()
                    return None
            else:
                # Record miss
                conn.execute(
                    """INSERT INTO cache_stats (api_name, misses, last_access)
                        VALUES (?, 1, ?)
                        ON CONFLICT(api_name) DO UPDATE SET
                        misses = misses + 1,
                        last_access = excluded.last_access""",
                    (api_name, now)
                )
                conn.commit()
                return None
    
    def set(self, api_name: str, response_data: Any, 
            http_status: int = 200, confidence: str = "medium",
            ttl_days: Optional[int] = None, **params) -> None:
        """
        Store API response in cache.
        
        Args:
            api_name: Which API produced this data (ensembl, uniprot, etc.)
            response_data: JSON-serializable response data
            http_status: HTTP status code from API
            confidence: Data quality confidence (high/medium/low)
            ttl_days: Override default TTL
            **params: Query parameters that produced this response
        """
        cache_key = self._make_key(api_name, **params)
        now = time.time()
        ttl = (ttl_days * 86400) if ttl_days else self.default_ttl
        expires = now + ttl
        
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO api_cache 
                    (cache_key, api_name, query_params, response_data, 
                     created_at, expires_at, http_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(cache_key) DO UPDATE SET
                    response_data = excluded.response_data,
                    created_at = excluded.created_at,
                    expires_at = excluded.expires_at,
                    http_status = excluded.http_status,
                    confidence = excluded.confidence,
                    hit_count = 0""",
                (cache_key, api_name, json.dumps(params), json.dumps(response_data),
                 now, expires, http_status, confidence)
            )
            conn.commit()
    
    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """Return cache statistics per API."""
        with self._connection() as conn:
            cursor = conn.execute(
                """SELECT api_name, hits, misses, errors, last_access
                   FROM cache_stats ORDER BY api_name"""
            )
            return {
                row["api_name"]: {
                    "hits": row["hits"],
                    "misses": row["misses"],
                    "errors": row["errors"],
                    "last_access": row["last_access"],
                    "hit_rate": row["hits"] / (row["hits"] + row["misses"]) 
                               if (row["hits"] + row["misses"]) > 0 else 0.0,
                }
                for row in cursor.fetchall()
            }
    
    def clear_expired(self) -> int:
        """Remove expired entries. Returns count of removed entries."""
        now = time.time()
        with self._connection() as conn:
            cursor = conn.execute(
                "DELETE FROM api_cache WHERE expires_at <= ?",
                (now,)
            )
            conn.commit()
            return cursor.rowcount
    
    def clear_all(self) -> None:
        """Clear entire cache."""
        with self._connection() as conn:
            conn.execute("DELETE FROM api_cache")
            conn.execute("DELETE FROM cache_stats")
            conn.commit()
    
    def warm_cache(self, api_name: str, entries: List[Dict[str, Any]], ttl_days: int = 30) -> int:
        """
        Bulk-load pre-computed entries into cache (for offline mode or seeding).
        
        Args:
            api_name: API these entries belong to
            entries: List of {params_dict, response_data} dicts
            ttl_days: TTL for all entries
        
        Returns:
            Number of entries loaded
        """
        count = 0
        for entry in entries:
            params = entry.get("params", {})
            data = entry.get("data", {})
            self.set(api_name, data, ttl_days=ttl_days, **params)
            count += 1
        return count
    
    def get_all_for_api(self, api_name: str) -> List[Dict[str, Any]]:
        """Retrieve all non-expired entries for a specific API (for export/backup)."""
        now = time.time()
        with self._connection() as conn:
            cursor = conn.execute(
                """SELECT cache_key, query_params, response_data, 
                          created_at, expires_at, http_status, confidence
                   FROM api_cache 
                   WHERE api_name = ? AND expires_at > ?
                   ORDER BY created_at DESC""",
                (api_name, now)
            )
            return [
                {
                    "cache_key": row["cache_key"],
                    "params": json.loads(row["query_params"]),
                    "data": json.loads(row["response_data"]),
                    "created_at": row["created_at"],
                    "expires_at": row["expires_at"],
                    "http_status": row["http_status"],
                    "confidence": row["confidence"],
                }
                for row in cursor.fetchall()
            ]
    
    def dump_to_json(self, output_path: Path) -> None:
        """Export entire cache to JSON for backup or transport."""
        apis = ["ensembl", "uniprot", "gtex", "gnomad", "ncbi_eutils", "clinvar_eutils"]
        dump = {}
        for api_name in apis:
            dump[api_name] = self.get_all_for_api(api_name)
        
        with open(output_path, 'w') as f:
            json.dump(dump, f, indent=2, default=str)
    
    def load_from_json(self, input_path: Path) -> int:
        """Import cache from JSON backup."""
        with open(input_path, 'r') as f:
            dump = json.load(f)
        
        total = 0
        for api_name, entries in dump.items():
            for entry in entries:
                params = entry.get("params", {})
                data = entry.get("data", {})
                ttl_days = int((entry.get("expires_at", 0) - time.time()) / 86400)
                if ttl_days > 0:
                    self.set(api_name, data, 
                            http_status=entry.get("http_status", 200),
                            confidence=entry.get("confidence", "medium"),
                            ttl_days=ttl_days,
                            **params)
                    total += 1
        return total
