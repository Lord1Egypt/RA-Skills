"""
Hybrid Search Engine
=====================

Main HybridSearch class combining semantic and keyword search.
"""

import sqlite3
import json
import logging
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Union

from ..chroma_integration import ChromaIntegration, get_chroma
from ..fts5_setup import check_fts5_available
from ..synonyms import SynonymExpander, get_expander
from ..reranker import Reranker, get_reranker
from ..search_providers import ProviderResult, SemanticSearchProvider, KeywordSearchProvider
from ..paths import get_default_db_path, get_default_chroma_path
from ..exceptions import ChromaConnectionError

from .models import SearchResult, SearchConfig
from .keyword import _keyword_search_fts, _keyword_search
from .semantic import _semantic_search
from .filters import search_with_filters

# Logging
logger = logging.getLogger(__name__)


class HybridSearch:
    """
    Hybrid Search Interface: SQLite + ChromaDB.
    
    Combines:
    - Semantic search via ChromaDB (embeddings)
    - Keyword search via SQLite (full-text LIKE)
    - Ranking via combined weighted scores
    
    Phase 3.1: Wing/Room/Hall Filter implemented
    Phase 3.2: Query Caching
    """
    
    def __init__(
        self,
        db_path: str = None,
        chroma_path: str = None,
        config: Optional[SearchConfig] = None,
        semantic_provider = None,
        keyword_provider = None
    ):
        """
        Initialize Hybrid Search.
        
        Args:
            db_path: Path to knowledge.db
            chroma_path: Path for ChromaDB
            config: SearchConfig (or default)
            semantic_provider: Optional SemanticSearchProvider (Protocol)
            keyword_provider: Optional KeywordSearchProvider (Protocol)
        
        If providers are not given, defaults are created:
        - semantic: ChromaSemanticProvider (wraps ChromaIntegration)
        - keyword: FTS5KeywordProvider (wraps SQLite FTS5)
        
        Pass semantic_provider=None to disable semantic search (cluster mode).
        """
        if db_path is None:
            db_path = str(get_default_db_path())
        self.db_path = Path(db_path).expanduser()
        self._chroma_disabled = chroma_path is False
        if chroma_path is None:
            self.chroma_path = get_default_chroma_path()
        elif chroma_path is False:
            self.chroma_path = None  # Cluster mode: no ChromaDB
        else:
            self.chroma_path = Path(chroma_path)
        self.config = config or SearchConfig()
        
        # Provider injection (DG-2: Interface-Extraktion)
        self._semantic_provider = semantic_provider  # Can be None for cluster mode
        self._keyword_provider = keyword_provider
        
        # Legacy ChromaDB connection (used when no provider is injected)
        if self._semantic_provider is None and not self._chroma_disabled:
            # Only init ChromaDB if no provider given and chroma_path not explicitly disabled
            try:
                self.chroma = get_chroma(chroma_path=str(self.chroma_path))
            except Exception as e:
                logger.warning(f"ChromaDB initialization failed: {e}")
                self.chroma = None
                self._chroma_error = ChromaConnectionError(f"ChromaDB init failed: {e}")
                self._chroma_error.__cause__ = e
        else:
            self.chroma = None
        
        self._db_conn: Optional[sqlite3.Connection] = None
        self._fts5_available: bool = False

        # Phase 3.2: Query Cache (LRU)
        self._query_cache: dict = {}
        self._cache_max_size: int = 100

        # Graceful degradation: if DB connection fails, disable keyword provider
        try:
            _test_conn = sqlite3.connect(str(self.db_path))
            _test_conn.close()
        except sqlite3.OperationalError as e:
            logger.error(f"Cannot open database {self.db_path}: {e}. Keyword provider disabled.")
            self._keyword_provider = None
        
        # Phase 2: Synonym Expander
        self._expander: Optional[SynonymExpander] = None
        self._synonym_expansion_enabled: bool = True
        
        # Phase 6: Re-Ranker
        self._reranker: Optional[Reranker] = None
        self._reranking_enabled: bool = False  # Off by default (adds latency)
        
        logger.info(f"HybridSearch init: db={self.db_path}, semantic_provider={type(self._semantic_provider).__name__ if self._semantic_provider else 'ChromaDB'}, keyword_provider={type(self._keyword_provider).__name__ if self._keyword_provider else 'FTS5'}")
    
    # -------------------------------------------------------------------------
    # Database Connection
    # -------------------------------------------------------------------------
    
    @property
    def db_conn(self) -> sqlite3.Connection:
        """Lazy SQLite connection with graceful degradation."""
        if self._db_conn is None:
            try:
                self._db_conn = sqlite3.connect(str(self.db_path))
                self._db_conn.row_factory = sqlite3.Row
            except sqlite3.OperationalError as e:
                logger.error(f"Cannot open database {self.db_path}: {e}. Keyword search disabled.")
                self._db_conn = None  # Graceful degradation
        return self._db_conn
    
    def close(self):
        """Close database connection."""
        if self._db_conn:
            self._db_conn.close()
            self._db_conn = None
    
    # -------------------------------------------------------------------------
    # Phase 2: Synonym Expansion
    # -------------------------------------------------------------------------
    
    @property
    def expander(self) -> SynonymExpander:
        """Lazy-load SynonymExpander."""
        if self._expander is None:
            self._expander = get_expander()
        return self._expander
    
    def enable_synonym_expansion(self, enabled: bool) -> None:
        """Enable or disable synonym expansion."""
        self._synonym_expansion_enabled = enabled
    
    def expand_query(self, query: str) -> str:
        """
        Expand query with synonyms for better recall.
        
        Phase 2: Synonym expansion before search.
        
        Args:
            query: Original query string
            
        Returns:
            Expanded query string with synonyms
        """
        if not self._synonym_expansion_enabled:
            return query
        return self.expander.expand_query(query)

    # -------------------------------------------------------------------------
    # Phase 6: Re-Ranking
    # -------------------------------------------------------------------------
    
    @property
    def reranker(self) -> Reranker:
        """Lazy-load Reranker."""
        if self._reranker is None:
            self._reranker = get_reranker()
        return self._reranker
    
    def enable_reranking(self, enabled: bool) -> None:
        """Enable or disable re-ranking (adds latency but improves quality)."""
        self._reranking_enabled = enabled
        logger.info(f"Re-ranking {'enabled' if enabled else 'disabled'}")
    
    def rerank_results(self, query: str, results: list) -> list:
        """
        Re-rank results using Cross-Encoder.
        
        Phase 6: Cross-Encoder re-ranking after hybrid search.
        
        Args:
            query: Original search query
            results: Initial search results
            
        Returns:
            Re-ranked results (adds rerank_score to each result)
        """
        if not self._reranking_enabled or not results:
            return results
        
        # Convert SearchResult to dict for reranker
        result_dicts = []
        for r in results:
            result_dicts.append({
                'section_id': r.section_id,
                'file_id': r.file_id,
                'file_path': r.file_path,
                'section_header': r.section_header,
                'content_preview': r.content_preview,
                'content_full': r.content_full,
                'section_level': r.section_level,
                'importance_score': r.importance_score,
                'keywords': r.keywords,
                'semantic_score': r.semantic_score,
                'keyword_score': r.keyword_score,
                'combined_score': r.combined_score,
                'source': r.source,
            })
        
        # Re-rank
        reranked_dicts = self.reranker.rerank(query, result_dicts)
        
        # Convert back to SearchResult
        reranked_results = []
        for rd in reranked_dicts:
            reranked_results.append(SearchResult(**rd))
        
        return reranked_results

    # -------------------------------------------------------------------------
    # Semantic Search (delegates to semantic module)
    # -------------------------------------------------------------------------

    def _semantic_search(self, query: str, limit: Optional[int] = None) -> list[dict]:
        """Semantic search — delegates to module function."""
        limit = limit or self.config.semantic_limit
        return _semantic_search(
            query=query,
            limit=limit,
            semantic_provider=self._semantic_provider,
            chroma=self.chroma,
        )

    # -------------------------------------------------------------------------
    # Keyword Search (delegates to keyword module)
    # -------------------------------------------------------------------------

    def _keyword_search_fts(self, query: str, limit: Optional[int] = None) -> list[dict]:
        """Keyword search — delegates to module function."""
        limit = limit or self.config.keyword_limit
        return _keyword_search_fts(
            db_conn=self.db_conn,
            query=query,
            limit=limit,
            keyword_exact_boost=self.config.keyword_exact_boost,
            keyword_provider=self._keyword_provider,
        )

    def _keyword_search(self, query: str, limit: Optional[int] = None) -> list[dict]:
        """Keyword LIKE search — delegates to module function."""
        limit = limit or self.config.keyword_limit
        return _keyword_search(
            db_conn=self.db_conn,
            query=query,
            limit=limit,
            keyword_exact_boost=self.config.keyword_exact_boost,
        )

    # -------------------------------------------------------------------------
    # Result Merging & Ranking
    # -------------------------------------------------------------------------
    
    def _merge_and_rank(
        self,
        semantic_results: list[dict],
        keyword_results: list[dict]
    ) -> list[SearchResult]:
        """
        Merges results from both searches and ranks.
        
        Scoring:
        - Semantic: from ChromaDB similarity
        - Keyword: from SQLite LIKE match
        - Combined: weighted average + boosts
        """
        
        # Build unified result set (deduplicate by section_id)
        result_map: dict[str, dict] = {}
        
        for r in semantic_results:
            result_map[r['section_id']] = {
                'section_id': r['section_id'],
                'file_id': r.get('file_id', ''),
                'file_path': r.get('file_path', ''),
                'section_header': r.get('section_header', ''),
                'content_preview': '',
                'content_full': '',
                'section_level': 0,
                'importance_score': r.get('importance_score', 0.5),
                'keywords': r.get('keywords', []),
                'semantic_score': r.get('semantic_score', 0.0),
                'keyword_score': 0.0,
                'source': 'chroma'
            }
        
        for r in keyword_results:
            sid = r['section_id']
            if sid in result_map:
                result_map[sid]['keyword_score'] = r.get('keyword_score', 0.0)
                result_map[sid]['content_preview'] = r.get('content_preview', '')
                result_map[sid]['content_full'] = r.get('content_full', '')
                result_map[sid]['section_level'] = r.get('section_level', 0)
                result_map[sid]['source'] = 'hybrid'
            else:
                r['semantic_score'] = 0.0
                r['source'] = 'sqlite'
                result_map[sid] = r
        
        # Calculate combined scores with optional normalization
        results = []
        max_semantic = max((r['semantic_score'] for r in result_map.values()), default=1.0)
        max_keyword = max((r['keyword_score'] for r in result_map.values()), default=1.0)
        
        for sid, data in result_map.items():
            semantic = data['semantic_score']
            keyword = data['keyword_score']
            
            # Normalize scores if enabled
            if self.config.normalize_scores:
                semantic = semantic / max_semantic if max_semantic > 0 else 0
                keyword = keyword / max_keyword if max_keyword > 0 else 0
            
            # Weighted combination
            combined = (
                semantic * self.config.semantic_weight +
                keyword * self.config.keyword_weight
            )
            
            # Apply importance boost
            if self.config.importance_boost:
                combined *= (0.5 + data['importance_score'])
            
            # Apply recency boost (future enhancement)
            # ...
            
            data['combined_score'] = combined
            results.append(SearchResult(**data))
        
        # Sort by combined score
        results.sort(key=lambda x: x.combined_score, reverse=True)
        
        # Limit final results
        return results[:self.config.final_limit]
    
    # -------------------------------------------------------------------------
    # Main Search Interface (with Cache - Phase 3.2)
    # -------------------------------------------------------------------------
    
    def _get_cached(self, cache_key: str):
        """Retrieve result from cache."""
        return self._query_cache.get(cache_key)
    
    def _set_cached(self, cache_key: str, result: list) -> None:
        """Store result in cache (LRU)."""
        if len(self._query_cache) >= self._cache_max_size:
            # Remove oldest entry
            oldest = next(iter(self._query_cache))
            del self._query_cache[oldest]
        self._query_cache[cache_key] = result
    
    def search(
        self,
        query: str,
        limit: Optional[int] = None,
        semantic_only: bool = False,
        keyword_only: bool = False
    ) -> list[SearchResult]:
        """
        Main search interface.
        
        Args:
            query: Natural language or keyword query
            limit: Override default result limit (default: 20)
            semantic_only: Only semantic search (skip SQLite)
            keyword_only: Only keyword search (skip ChromaDB)
            
        Returns:
            List of SearchResult ranked by combined score
        """
        if not query or not query.strip():
            return []
        
        query = query.strip()
        limit = limit or self.config.final_limit
        
        # Phase 2: Synonym expansion for better recall
        expanded_query = self.expand_query(query)
        
        # Phase 3.2: Cache check
        cache_key = f"{expanded_query}:{limit}:{semantic_only}:{keyword_only}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            logger.info(f"Cache HIT for query: '{query}'")
            return cached
        
        logger.info(f"HybridSearch query: '{query}' → expanded:'{expanded_query}' (semantic_only={semantic_only}, keyword_only={keyword_only})")
        
        # Execute searches
        semantic_results = []
        keyword_results = []
        
        if not keyword_only:
            semantic_results = self._semantic_search(query)
        
        if not semantic_only:
            # Use FTS5 BM25 search if available, fallback to LIKE
            keyword_results = self._keyword_search_fts(query)
        
        # Merge and rank
        results = self._merge_and_rank(semantic_results, keyword_results)
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        # Filter by minimum score
        results = [
            r for r in results 
            if r.combined_score >= self.config.min_combined_score
        ]
        
        logger.info(f"  -> {len(results)} results")
        
        # Phase 6: Re-ranking (optional, adds latency)
        results = self.rerank_results(query, results)
        
        # Cache result
        self._set_cached(cache_key, results)
        
        return results

    # -------------------------------------------------------------------------
    # Filtered Search (delegates to filters module)
    # -------------------------------------------------------------------------

    def search_with_filters(
        self,
        query: str,
        limit: Optional[int] = None,
        wing: Optional[str] = None,
        room: Optional[str] = None,
        hall: Optional[str] = None,
        file_types: Optional[list[str]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> list[SearchResult]:
        """Hybrid Search with Wing/Room/Hall metadata filter — delegates to filters module."""
        return search_with_filters(
            searcher=self,
            query=query,
            limit=limit,
            wing=wing,
            room=room,
            hall=hall,
            file_types=file_types,
            date_from=date_from,
            date_to=date_to,
        )
    
    def search_semantic(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> list[SearchResult]:
        """
        Semantic-only search using ChromaDB embeddings.
        
        Best for: Natural language queries, conceptual matches.
        
        Args:
            query: Natural language query
            limit: Max results (default: 20)
            
        Returns:
            List of SearchResult with semantic_score populated
        """
        return self.search(query, limit=limit, semantic_only=True)
    
    def search_keyword(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> list[SearchResult]:
        """
        Keyword-only search using SQLite LIKE.
        
        Best for: Exact term matches, known identifiers.
        
        Args:
            query: Keyword query string
            limit: Max results (default: 20)
            
        Returns:
            List of SearchResult with keyword_score populated
        """
        return self.search(query, limit=limit, keyword_only=True)
    
    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------
    
    def get_stats(self) -> dict:
        """Collect and return search system statistics from ChromaDB and SQLite.

        Queries both backends to provide an overview of indexed content:
        - ChromaDB: section count in the kb_sections collection
        - SQLite: total file_sections count and total files count
        - Config: current semantic/keyword weight settings

        Returns:
            Dict with keys:
            - chroma_sections (int): Number of sections in ChromaDB
            - sqlite_sections (int): Number of sections in SQLite
            - sqlite_files (int): Number of files in SQLite
            - config (dict): Search weights (semantic_weight, keyword_weight)

        Raises:
            sqlite3.OperationalError: If SQLite tables are missing or corrupted
        """
        chroma = self.chroma
        
        # ChromaDB stats
        try:
            chroma_stats = chroma.get_collection_stats("kb_sections")
        except Exception as e:
            logger.debug(f"ChromaDB stats unavailable: {e}")
            chroma_stats = {"count": 0, "name": "kb_sections"}
        
        # SQLite stats
        db_conn = self.db_conn
        if db_conn is None:
            logger.error("No database connection available for stats")
            return {
                "chroma_sections": chroma_stats.get("count", 0),
                "sqlite_sections": 0,
                "sqlite_files": 0,
                "config": {
                    "semantic_weight": self.config.semantic_weight,
                    "keyword_weight": self.config.keyword_weight
                }
            }

        cursor = db_conn.execute("SELECT COUNT(*) FROM file_sections")
        total_sections = cursor.fetchone()[0]
        
        cursor = db_conn.execute("SELECT COUNT(*) FROM files")
        total_files = cursor.fetchone()[0]
        
        return {
            "chroma_sections": chroma_stats.get("count", 0),
            "sqlite_sections": total_sections,
            "sqlite_files": total_files,
            "config": {
                "semantic_weight": self.config.semantic_weight,
                "keyword_weight": self.config.keyword_weight
            }
        }
    
    def suggest_refinements(self, query: str) -> list[str]:
        """
        Suggests query refinements based on keyword analysis.
        
        Future enhancement for query expansion.
        """
        # Simple implementation: extract keywords from top SQLite results
        keyword_results = self._keyword_search(query, limit=5)
        
        suggestions = []
        for r in keyword_results[:3]:
            suggestions.extend(r.get('keywords', [])[:3])
        
        # Deduplicate and return top suggestions
        seen = set()
        unique = []
        for s in suggestions:
            if s not in seen and s not in query.lower():
                seen.add(s)
                unique.append(s)
        
        return unique[:5]


# =============================================================================
# Convenience Functions
# =============================================================================

# Lazy global instance (thread-safe)
_global_search: Optional[HybridSearch] = None
_search_lock = threading.RLock()

def get_search(**kwargs) -> HybridSearch:
    """Get or create global HybridSearch instance (thread-safe)."""
    global _global_search
    if _global_search is None:
        with _search_lock:
            if _global_search is None:
                _global_search = HybridSearch(**kwargs)
    return _global_search

def search(query: str, **kwargs) -> list[SearchResult]:
    """Quick search convenience function."""
    return get_search().search(query, **kwargs)


# =============================================================================
# Main: Quick Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Hybrid Search - Quick Test")
    print("=" * 60)
    
    searcher = HybridSearch()
    
    print("\n[1] System Stats:")
    stats = searcher.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n[2] Testing Keyword Search:")
    keyword_results = searcher.search_keyword("MTHFR Genmutation", limit=5)
    print(f"   Found {len(keyword_results)} results")
    for r in keyword_results[:3]:
        print(f"   - [{r.section_id[:8]}...] score={r.keyword_score:.2f} header={r.section_header[:50]}")
    
    print("\n[3] Testing Semantic Search:")
    semantic_results = searcher.search_semantic("genetische Methylierung Behandlung", limit=5)
    print(f"   Found {len(semantic_results)} results")
    for r in semantic_results[:3]:
        print(f"   - [{r.section_id[:8]}...] score={r.semantic_score:.2f} header={r.section_header[:50]}")
    
    print("\n[4] Testing Hybrid Search:")
    hybrid_results = searcher.search("MTHFR Genmutation Methylierung", limit=10)
    print(f"   Found {len(hybrid_results)} results")
    print(f"   {'Source':<10} {'Semantic':<10} {'Keyword':<10} {'Combined':<10} Header")
    print(f"   {'-'*60}")
    for r in hybrid_results[:5]:
        print(f"   {r.source:<10} {r.semantic_score:<10.3f} {r.keyword_score:<10.3f} {r.combined_score:<10.3f} {r.section_header[:40]}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    # Don't forget to close DB connection
    searcher.close()