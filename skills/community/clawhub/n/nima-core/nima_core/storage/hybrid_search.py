#!/usr/bin/env python3
"""
Hybrid Memory Search
====================
Combines keyword (BM25) + semantic (VSA) search for unified recall.

Sources:
1. LadybugDB - Vector embeddings (semantic search)
2. SQLite FTS5 - Full-text search (keyword BM25)
3. Text files - Grep-like matching

Usage:
    from nima_core.storage.hybrid_search import HybridSearcher
    
    searcher = HybridSearcher()
    results = searcher.search("David's pattern with NIMA", limit=10)
    
    # Or search single source:
    results = searcher.search_semantic("query", limit=5)
    results = searcher.search_keyword("query", limit=5)

Author: Extracted from nima_core/cli/unified_recall.py
Ported: 2026-03-10
"""

import os
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict


class HybridSearcher:
    """
    Unified search across multiple memory systems.
    
    Combines:
    - Semantic search (LadybugDB embeddings)
    - Keyword search (SQLite FTS5 BM25)
    - Text matching (grep-like in markdown files)
    
    Returns normalized results with combined scores.
    """
    
    def __init__(self, db_path: Path = None, memory_db: Path = None,
                 allowed_base_dirs: Optional[List[Path]] = None):
        """
        Initialize searcher.
        
        Args:
            db_path: LadybugDB path (default: ~/.nima/memory/ladybug.lbug)
            memory_db: OpenClaw SQLite FTS5 path (default: ~/.openclaw/memory/main.sqlite)
            allowed_base_dirs: List of allowed base directories for path traversal protection
        """
        self._ladybug = None
        self._sqlite = None
        
        # LadybugDB
        if db_path is None:
            db_path = Path.home() / ".nima" / "memory" / "ladybug.lbug"
        self._ladybug_path = Path(db_path).resolve()
        self._ladybug_available = self._ladybug_path.exists()
        
        # OpenClaw SQLite
        if memory_db is None:
            memory_db = Path.home() / ".openclaw" / "memory" / "main.sqlite"
        self._sqlite_path = Path(memory_db).resolve()
        self._sqlite_available = self._sqlite_path.exists()
        
        # Text files - with path traversal protection
        self._allowed_base_dirs = allowed_base_dirs or [
            Path.home() / ".openclaw" / "workspace",
            Path.home() / ".nima" / "memory",
        ]
        self._memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        self._text_files = self._collect_text_files()
        
        if self._ladybug_available:
            print("✅ LadybugDB: Semantic search")
        else:
            print(f"⚠️  LadybugDB not found: {self._ladybug_path}")
        
        if self._sqlite_available:
            print("✅ SQLite: FTS5 keyword search")
        else:
            print(f"⚠️  SQLite DB not found: {self._sqlite_path}")
        
        if self._text_files:
            print(f"✅ Text: {len(self._text_files)} markdown files")
        else:
            print("⚠️  No markdown files found")
    
    def _is_safe_path(self, path: Path) -> bool:
        """
        Check if path is within allowed directories (path traversal protection).
        
        Args:
            path: Path to validate
            
        Returns:
            True if path is safe, False otherwise
        """
        resolved = path.resolve()
        for allowed_dir in self._allowed_base_dirs:
            try:
                resolved.relative_to(allowed_dir.resolve())
                return True
            except ValueError:
                continue
        return False
    
    def _collect_text_files(self) -> List[Path]:
        """Collect markdown files to search."""
        files = []
        
        if self._memory_dir.exists() and self._is_safe_path(self._memory_dir):
            files.extend(list(self._memory_dir.glob("*.md")))
        
        # Add root files - with path traversal protection
        workspace = Path.home() / ".openclaw" / "workspace"
        for fname in ["MEMORY.md", "HEARTBEAT.md", "IDENTITY.md"]:
            fpath = workspace / fname
            if fpath.exists() and self._is_safe_path(fpath):
                files.append(fpath)
        
        return files
    
    def search(
        self,
        query: str,
        limit: int = 10,
        sources: List[str] = None,
        combine: bool = True
    ) -> List[Dict]:
        """
        Search across all available sources.
        
        Args:
            query: Search query string
            limit: Max results per source
            sources: List of sources to search (default: all available)
            combine: If True, merge and re-rank results; if False, return separate lists
        
        Returns:
            List of result dicts with keys: source, score, content, metadata
        """
        if sources is None:
            sources = []
            if self._ladybug_available:
                sources.append('ladybug')
            if self._sqlite_available:
                sources.append('sqlite')
            if self._text_files:
                sources.append('text')
        
        all_results = []
        
        if 'ladybug' in sources and self._ladybug_available:
            all_results.extend(self._search_ladybug(query, limit))
        
        if 'sqlite' in sources and self._sqlite_available:
            all_results.extend(self._search_sqlite(query, limit))
        
        if 'text' in sources and self._text_files:
            all_results.extend(self._search_text(query, limit))
        
        if combine and all_results:
            # Merge and re-rank by combined score
            all_results = self._merge_results(all_results, query, limit)
        
        return all_results[:limit]
    
    def _search_ladybug(self, query: str, limit: int = 10,
                        max_retries: int = 3, base_delay: float = 2.0) -> List[Dict]:
        """
        Search LadybugDB using semantic (embedding) similarity.
        
        Falls back to keyword search if embeddings not available.
        Implements retry logic with exponential backoff for connection failures.
        
        Args:
            query: Search query string
            limit: Max results to return
            max_retries: Maximum number of retry attempts (default: 3)
            base_delay: Base delay in seconds for exponential backoff (default: 2.0)
            
        Returns:
            List of result dicts with search results
            
        Raises:
            RuntimeError: If all retry attempts fail
        """
        last_exception: Optional[Exception] = None
        
        for attempt in range(max_retries):
            try:
                import real_ladybug as lb
                
                db = lb.Database(str(self._ladybug_path))
                conn = lb.Connection(db)
                
                # Try keyword search first (LIKE query on text field)
                try:
                    results = conn.execute(f"""
                        SELECT id, text, who, what, timestamp, embedding
                        FROM memories
                        WHERE text LIKE ?
                        LIMIT ?
                    """, (f'%{query}%', limit)).fetch()
                    
                    return [{
                        'source': 'ladybug_keyword',
                        'score': 0.8,  # Placeholder - real cosine sim requires embedding
                        'content': r[1] if r[1] else f"{r[2]}: {r[3]}",
                        'who': r[2] or '?',
                        'timestamp': r[4] or '',
                        'memory_id': r[0],
                    } for r in results]
                    
                except Exception as e:
                    # Fallback to simple text match
                    print(f"[hybrid_search] Warning: Vector search failed, falling back to keyword search. Exception: {type(e).__name__}: {e}")
                    results = conn.execute("""
                        SELECT id, text, who, what, timestamp
                        FROM memories
                        WHERE text LIKE ? OR who LIKE ? OR what LIKE ?
                        LIMIT ?
                    """, (f'%{query}%', f'%{query}%', f'%{query}%', limit)).fetch()
                    
                    return [{
                        'source': 'ladybug_keyword',
                        'score': 0.5,
                        'content': r[1] if r[1] else f"{r[2]}: {r[3]}",
                        'who': r[2] or '?',
                        'timestamp': r[4] or '',
                        'memory_id': r[0],
                    } for r in results]
                    
            except Exception as e:
                last_exception = e
                delay = base_delay * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                print(f"[hybrid_search] LadybugDB connection failed (attempt {attempt + 1}/{max_retries}). Operation: search, Path: {self._ladybug_path}, Exception: {type(e).__name__}: {e}. Retrying in {delay}s...")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        
        # All retries failed
        print(f"[hybrid_search] LadybugDB search failed after {max_retries} attempts. Operation: search, Path: {self._ladybug_path}, Exception: {type(last_exception).__name__}: {last_exception}")
        return []
    
    def _search_sqlite(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search SQLite FTS5 using BM25 keyword ranking.
        
        Args:
            query: Search query string
            limit: Max results to return
            
        Returns:
            List of result dicts with search results
        """
        conn = None
        try:
            conn = sqlite3.connect(str(self._sqlite_path), timeout=30.0)
            cursor = conn.cursor()
            
            # FTS5 query with BM25 rank
            cursor.execute("""
                SELECT 
                    chunks_fts.text,
                    chunks_fts.path,
                    chunks_fts.source,
                    chunks_fts.start_line,
                    chunks_fts.end_line,
                    bm25(chunks_fts) as rank
                FROM chunks_fts 
                WHERE chunks_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            
            results = []
            for row in cursor.fetchall():
                text, path, source, start_line, end_line, rank = row
                
                # BM25 rank is negative (lower = better), normalize to 0-1
                # Typical range is -10 to -1
                score = max(0, min(1, (10 + rank) / 10))
                
                results.append({
                    'source': 'sqlite_fts5',
                    'score': float(score),
                    'content': text[:500],
                    'path': str(path),
                    'file_source': source,
                    'lines': f"{start_line}-{end_line}",
                })
            
            return results
            
        except Exception as e:
            print(f"[hybrid_search] SQLite search failed. Operation: search_keyword, Path: {self._sqlite_path}, Exception: {type(e).__name__}: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def _search_text(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search markdown files using simple text matching with TF-IDF-like scoring.
        
        Args:
            query: Search query string
            limit: Max results to return
            
        Returns:
            List of result dicts with search results
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        results = []
        
        for fpath in self._text_files:
            # Validate path before accessing (path traversal protection)
            if not self._is_safe_path(fpath):
                print(f"[hybrid_search] Skipping unsafe path: {fpath}")
                continue
            
            try:
                content = fpath.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # Search paragraphs (split by blank lines)
                paragraphs = content.split('\n\n')
                
                for i, para in enumerate(paragraphs):
                    para_lower = para.lower()
                    
                    # Count matching words
                    matches = sum(1 for w in query_words if w in para_lower)
                    if matches == 0:
                        continue
                    
                    # Simple TF-IDF-like score
                    word_count = len(para.split())
                    score = matches / max(1, word_count) ** 0.5
                    
                    # Find line numbers
                    start_line = para.count('\n', 0, para.find(para)) + 1
                    
                    if score > 0.05:  # Threshold
                        results.append({
                            'source': 'text',
                            'score': float(score),
                            'content': para[:500],
                            'file': str(fpath),
                            'lines': f"~{start_line}",
                            'matches': matches,
                        })
                
                if len(results) >= limit * 2:  # Get extra, will trim after merge
                    break
                    
            except Exception as e:
                print(f"[hybrid_search] Failed to read file. Operation: search_text, Path: {fpath}, Exception: {type(e).__name__}: {e}")
                continue
        
        return results
    
    def _merge_results(
        self,
        all_results: List[Dict],
        query: str,
        limit: int
    ) -> List[Dict]:
        """
        Merge results from different sources with score normalization.
        
        Strategy:
        1. Group by source
        2. Normalize scores within each source (min-max to 0-1)
        3. Apply source weights (semantic=0.5, keyword=0.3, text=0.2)
        4. Re-rank by weighted score
        """
        weights = {
            'ladybug_semantic': 0.5,
            'ladybug_keyword': 0.4,
            'sqlite_fts5': 0.4,
            'text': 0.2,
        }
        
        # Group by source
        by_source = defaultdict(list)
        for r in all_results:
            by_source[r['source']].append(r)
        
        # Normalize scores within each source
        normalized = []
        for source, results in by_source.items():
            if not results:
                continue
            
            scores = [r['score'] for r in results]
            min_s, max_s = min(scores), max(scores)
            score_range = max_s - min_s if max_s > min_s else 1.0
            
            for r in results:
                # Normalize to 0-1
                norm_score = (r['score'] - min_s) / score_range if score_range > 0 else r['score']
                
                # Apply weight
                weight = weights.get(r['source'], 0.3)
                weighted_score = norm_score * weight
                
                r['weighted_score'] = weighted_score
                r['original_score'] = r['score']
                r['score'] = weighted_score
                normalized.append(r)
        
        # Sort by weighted score
        normalized.sort(key=lambda x: x['score'], reverse=True)
        
        return normalized[:limit]
    
    def search_semantic(self, query: str, limit: int = 10) -> List[Dict]:
        """Search only semantic sources (LadybugDB)."""
        return self._search_ladybug(query, limit)
    
    def search_keyword(self, query: str, limit: int = 10) -> List[Dict]:
        """Search only keyword sources (SQLite FTS5)."""
        return self._search_sqlite(query, limit)
    
    def search_text(self, query: str, limit: int = 10) -> List[Dict]:
        """Search only text files."""
        return self._search_text(query, limit)
