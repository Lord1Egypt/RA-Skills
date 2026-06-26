"""
SQLite FTS5 Keyword Search Provider
====================================

Wraps SQLite FTS5 full-text search to implement the
KeywordSearchProvider interface.

Falls back to LIKE-based search if FTS5 is not available.

Usage:
------
    from kb.framework.providers.fts5_provider import FTS5KeywordProvider

    provider = FTS5KeywordProvider(db_path=get_default_db_path())
    if provider.is_available():
        results = provider.search("methylierung genetik", limit=10)
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import List, Optional

from ..search_providers import ProviderResult
from ..text import parse_keywords
from ..paths import get_default_db_path
from ..exceptions import SearchError

logger = logging.getLogger(__name__)


class FTS5KeywordProvider:
    """SQLite FTS5-backed keyword search provider.

    Uses BM25 ranking via SQLite FTS5 virtual tables for
    keyword-based search. Falls back to LIKE queries if
    FTS5 tables are not available.

    Args:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = get_default_db_path()

        self.db_path = Path(db_path).expanduser()
        self._conn: Optional[sqlite3.Connection] = None
        self._fts5_available: Optional[bool] = None

    def _get_conn(self) -> sqlite3.Connection:
        """Get or create SQLite connection with graceful degradation."""
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(str(self.db_path))
                self._conn.row_factory = sqlite3.Row
            except sqlite3.OperationalError as e:
                logger.error(f"Cannot open database {self.db_path}: {e}. FTS5 search disabled.")
                self._conn = None
        return self._conn

    def is_available(self) -> bool:
        """Check if FTS5 is available and tables exist."""
        if self._fts5_available is not None:
            return self._fts5_available

        try:
            conn = self._get_conn()

            # Check if FTS5 extension is available
            cursor = conn.execute(
                "SELECT COUNT(*) FROM pragma_compile_options WHERE compile_options LIKE '%ENABLE_FTS5%'"
            )
            fts5_compiled = cursor.fetchone()[0] > 0

            if not fts5_compiled:
                # Try directly (some builds include FTS5 without pragma flag)
                try:
                    conn.execute("SELECT fts5()")
                    fts5_compiled = True
                except Exception as e:
                    logger.debug(f"FTS5 direct check failed: {e}")

            if not fts5_compiled:
                self._fts5_available = False
                return False

            # Check if FTS5 virtual table exists
            cursor = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE name='file_sections_fts' AND type='table'"
            )
            table_exists = cursor.fetchone()[0] > 0

            self._fts5_available = table_exists
            return table_exists

        except Exception as e:
            logger.debug(f"FTS5 availability check failed: {e}")
            self._fts5_available = False
            return False

    def search(self, query: str, limit: int = 20) -> List[ProviderResult]:
        """Search using FTS5 BM25 ranking.

        Args:
            query: Keyword query string.
            limit: Maximum number of results.

        Returns:
            List of ProviderResult sorted by keyword relevance.
        """
        if not query or not query.strip():
            return []

        try:
            if self.is_available():
                return self._search_fts5(query, limit)
            else:
                return self._search_like(query, limit)
        except sqlite3.OperationalError as e:
            logger.error(f"SQLite operational error during search: {e}")
            self._last_search_error = SearchError(f"FTS5 search failed: {e}")
            self._last_search_error.__cause__ = e
            return []

    def _search_fts5(self, query: str, limit: int) -> List[ProviderResult]:
        """BM25 search via FTS5 virtual table."""
        conn = self._get_conn()
        if conn is None:
            logger.error("No database connection available for FTS5 search")
            return []

        # Build FTS5 query from terms
        terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 1]
        if not terms:
            return []

        fts5_query = " AND ".join(terms)

        sql = """
            SELECT
                section_id,
                file_id,
                file_path,
                section_header,
                content_preview,
                content_full,
                importance_score,
                keywords,
                bm25(file_sections_fts) as bm25_rank
            FROM file_sections_fts
            WHERE file_sections_fts MATCH ?
            ORDER BY bm25_rank
            LIMIT ?
        """

        try:
            cursor = conn.execute(sql, (fts5_query, limit))
            rows = cursor.fetchall()
        except Exception as e:
            logger.warning(f"FTS5 query failed: {e}, falling back to LIKE")
            return self._search_like(query, limit)

        results = []
        total = len(rows)

        for idx, row in enumerate(rows):
            section_id = row["section_id"] if "section_id" in row.keys() else row[0]
            file_id = row["file_id"] if "file_id" in row.keys() else row[1]
            file_path = row["file_path"] if "file_path" in row.keys() else row[2]
            section_header = row["section_header"] if "section_header" in row.keys() else row[3]
            content_preview = row["content_preview"] if "content_preview" in row.keys() else row[4]
            content_full = row["content_full"] if "content_full" in row.keys() else row[5]
            importance_score = row["importance_score"] if "importance_score" in row.keys() else row[6]
            keywords_str = row["keywords"] if "keywords" in row.keys() else row[7]
            bm25_rank = row["bm25_rank"] if "bm25_rank" in row.keys() else row[8]

            # Convert BM25 rank to positive score
            # BM25 returns negative values (closer to 0 = better)
            position_score = (total - idx) / total if total > 0 else 0.5

            if bm25_rank is not None and bm25_rank < -0.001:
                bm25_boost = min(1.0, max(0.0, 0.5 + abs(bm25_rank) / 20.0))
                keyword_score = 0.7 * position_score + 0.3 * bm25_boost
            else:
                keyword_score = position_score

            keywords = parse_keywords(str(keywords_str) if keywords_str else "")

            results.append(ProviderResult(
                section_id=str(section_id),
                content=str(content_full or content_preview or ""),
                score=keyword_score,
                source="fts5",
                file_id=str(file_id) if file_id else "",
                file_path=str(file_path) if file_path else "",
                section_header=str(section_header) if section_header else "",
                importance_score=float(importance_score) if importance_score else 0.5,
                keywords=keywords,
                metadata={
                    "content_preview": str(content_preview or ""),
                    "bm25_rank": float(bm25_rank) if bm25_rank is not None else 0.0,
                },
            ))

        logger.info(f"FTS5 search for '{query}': {len(results)} results")
        return results

    def _search_like(self, query: str, limit: int) -> List[ProviderResult]:
        """Fallback LIKE-based search when FTS5 is unavailable."""
        conn = self._get_conn()
        if conn is None:
            logger.error("No database connection available for LIKE search")
            return []

        terms = [t.strip().lower() for t in query.split() if t.strip()]
        if not terms:
            return []

        # Build LIKE conditions for each term
        conditions = []
        params = []
        for term in terms:
            conditions.append(
                "(LOWER(section_header) LIKE ? OR LOWER(section_content) LIKE ?)"
            )
            params.extend([f"%{term}%", f"%{term}%"])

        where_clause = " AND ".join(conditions)

        sql = f"""
            SELECT
                fs.id as section_id,
                fs.file_id,
                f.file_path,
                fs.section_header,
                substr(fs.section_content, 1, 500) as content_preview,
                fs.section_content as content_full,
                0.5 as importance_score,
                '[]' as keywords
            FROM file_sections fs
            LEFT JOIN files f ON fs.file_id = f.id
            WHERE {where_clause}
            ORDER BY fs.section_header
            LIMIT ?
        """

        params.append(limit)

        try:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
        except Exception as e:
            logger.warning(f"LIKE search failed: {e}")
            return []

        results = []
        total = len(rows)

        for idx, row in enumerate(rows):
            score = (total - idx) / total if total > 0 else 0.5

            results.append(ProviderResult(
                section_id=str(row[0]),
                content=str(row[5] or row[4] or ""),
                score=score,
                source="like",
                file_id=str(row[1]) if row[1] else "",
                file_path=str(row[2]) if row[2] else "",
                section_header=str(row[3]) if row[3] else "",
                importance_score=float(row[6]) if row[6] else 0.5,
                keywords=[],
                metadata={"content_preview": str(row[4] or "")},
            ))

        logger.info(f"LIKE search for '{query}': {len(results)} results")
        return results

    def close(self):
        """Close the database connection."""
        conn = getattr(self, '_conn', None)
        if conn is not None:
            conn.close()
            self._conn = None

    def __del__(self):
        """Ensure connection is closed on garbage collection."""
        self.close()