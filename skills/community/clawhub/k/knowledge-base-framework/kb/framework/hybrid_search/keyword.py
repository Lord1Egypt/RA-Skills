"""
Keyword Search Implementations
===============================

FTS5 (BM25) and SQLite LIKE-based keyword search functions.
"""

import sqlite3
import logging
from typing import Optional

from ..fts5_setup import check_fts5_available
from ..text import parse_keywords

# Logging
logger = logging.getLogger(__name__)


def _keyword_search_fts(
    db_conn,
    query: str,
    limit: int = 100,
    keyword_exact_boost: float = 1.5,
    keyword_provider=None,
) -> list[dict]:
    """
    Keyword search — delegates to provider if available, else FTS5/LIKE.

    Uses BM25 (Best Match 25) algorithm for relevance ranking.
    Falls back to LIKE search if FTS5 is not available.

    Args:
        db_conn: SQLite database connection
        query: Query string
        limit: Max results
        keyword_exact_boost: Boost factor for exact keyword matches
        keyword_provider: Optional KeywordSearchProvider (Protocol)

    Returns:
        List of results with keyword match scores
    """
    # DG-2: Use injected provider if available
    if keyword_provider is not None:
        return _keyword_search_via_provider(keyword_provider, query, limit)

    # Legacy FTS5/LIKE path
    if db_conn is None:
        logger.error("No database connection available for keyword search")
        return []

    if not _check_fts5_available(db_conn):
        return _keyword_search(db_conn, query, limit, keyword_exact_boost)

    terms = _build_query_terms(query)
    if not terms:
        return []

    fts5_query = _build_fts_query(terms)
    results = _execute_fts_query(db_conn, fts5_query, limit)
    return _map_fts_results(results, len(terms), keyword_exact_boost)


def _keyword_search_via_provider(keyword_provider, query: str, limit: int) -> list[dict]:
    """Execute keyword search via injected provider."""
    try:
        provider_results = keyword_provider.search(query, limit)
        return [
            {
                "section_id": r.section_id,
                "keyword_score": r.score,
                "file_id": r.file_id,
                "file_path": r.file_path,
                "section_header": r.section_header,
                "content_preview": r.metadata.get("content_preview", ""),
                "content_full": r.content,
                "section_level": 0,
                "importance_score": r.importance_score,
                "keywords": r.keywords,
            }
            for r in provider_results
        ]
    except (KeyError, ValueError, AttributeError) as e:
        logger.warning(f"Keyword provider search failed: {e}")
        return []


def _check_fts5_available(db_conn) -> bool:
    """Check if FTS5 table exists."""
    try:
        cursor = db_conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name='file_sections_fts' AND type='table'"
        )
        if not cursor.fetchone()[0]:
            logger.warning("FTS5 table not found, falling back to LIKE")
            return False
    except sqlite3.OperationalError as e:
        logger.warning(f"FTS5 table check failed: {e}, falling back to LIKE")
        return False
    return True


def _build_query_terms(query: str) -> list[str]:
    """Parse query into searchable terms."""
    return [t.strip().lower() for t in query.split() if len(t.strip()) > 1]


def _build_fts_query(terms: list[str]) -> str:
    """Convert terms to FTS5 query syntax."""
    fts5_query_parts = []
    for term in terms:
        if ' ' in term:
            fts5_query_parts.append(f'"{term}"')
        else:
            fts5_query_parts.append(term)
    return ' AND '.join(fts5_query_parts)


def _execute_fts_query(db_conn, fts5_query: str, limit: int) -> list:
    """Execute FTS5 BM25 query and return raw results."""
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
    cursor = db_conn.execute(sql, (fts5_query, limit))
    return cursor.fetchall()


def _map_fts_results(rows, total_terms: int, keyword_exact_boost: float) -> list[dict]:
    """Map FTS5 BM25 rows to result dicts with computed scores."""
    results = []
    total_rows = len(rows)

    for row_num, row in enumerate(rows, 1):
        section_id, file_id, file_path, section_header, \
        content_preview, content_full, importance_score, \
        keywords_str, bm25_rank = row

        position_score = (total_rows - row_num) / total_rows if total_rows > 0 else 0.5

        if bm25_rank is not None and bm25_rank < -0.001:
            bm25_boost = min(1.0, max(0.0, 0.5 + abs(bm25_rank) / 20.0))
            bm25_score = 0.7 * position_score + 0.3 * bm25_boost
        else:
            bm25_score = position_score

        results.append({
            "section_id": str(section_id),
            "keyword_score": bm25_score,
            "file_id": str(file_id) if file_id else "",
            "file_path": file_path or "",
            "section_header": section_header or "",
            "content_preview": content_preview or "",
            "content_full": content_full or "",
            "section_level": 0,
            "importance_score": importance_score or 0.5,
            "keywords": parse_keywords(keywords_str)
        })

    logger.info(f"FTS5 BM25 search: {len(results)} results")
    return results


def _keyword_search(
    db_conn,
    query: str,
    limit: int = 100,
    keyword_exact_boost: float = 1.5,
) -> list[dict]:
    """
    Keyword search via SQLite LIKE.

    Args:
        db_conn: SQLite database connection
        query: Query string
        limit: Max results
        keyword_exact_boost: Boost factor for exact keyword matches

    Returns:
        List of results with keyword match scores
    """
    if db_conn is None:
        logger.error("No database connection available for LIKE search")
        return []

    # Build query terms (simple tokenization)
    terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 1]

    if not terms:
        return []

    # Build LIKE clauses
    like_clauses = []
    params = []

    for term in terms:
        like_clauses.append("(section_content LIKE ? OR section_header LIKE ?)")
        params.extend([f"%{term}%", f"%{term}%"])

    sql = f"""
        SELECT 
            fs.id, fs.file_id, fs.section_header, fs.section_content, fs.section_level,
            f.file_path
        FROM file_sections fs
        LEFT JOIN files f ON fs.file_id = f.id
        WHERE {' AND '.join(like_clauses)}
        ORDER BY COALESCE(fs.section_level, 0) DESC, fs.id
        LIMIT ?
    """
    params.append(limit)

    cursor = db_conn.execute(sql, params)

    results = []
    for row in cursor.fetchall():
        section_id, file_id, section_header, section_content, section_level, file_path = row
        file_path = file_path or ""

        # Calculate keyword score
        all_text = f"{section_header} {section_content}".lower()
        matches = sum(1 for term in terms if term in all_text)
        keyword_score = matches / len(terms)  # 0.0 to 1.0

        # Exact match bonus
        exact_matches = sum(1 for term in terms if term in all_text.split())
        if exact_matches == len(terms):
            keyword_score *= keyword_exact_boost

        results.append({
            "section_id": str(section_id),
            "keyword_score": min(keyword_score, 1.0),
            "file_id": str(file_id) if file_id else "",
            "file_path": file_path or "",
            "section_header": section_header or "",
            "content_preview": section_content[:500] if section_content else "",
            "content_full": section_content or "",
            "section_level": section_level or 0,
            "importance_score": 0.5,  # Default for file_sections without importance_score
            "keywords": []
        })

    return results
