"""
Search with Filters
=====================

Hybrid search with Wing/Room/Hall metadata filters.
"""

import logging
from pathlib import Path
from typing import Optional

from .models import SearchResult

# Logging
logger = logging.getLogger(__name__)


def search_with_filters(
    searcher,  # HybridSearch instance
    query: str,
    limit: Optional[int] = None,
    wing: Optional[str] = None,
    room: Optional[str] = None,
    hall: Optional[str] = None,
    file_types: Optional[list[str]] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> list[SearchResult]:
    """
    Hybrid Search with Wing/Room/Hall metadata filter.

    Phase 3.1: Full implementation

    Wing/Room/Hall are virtual categories:
    - wing: Main area (e.g., 'health', 'agent', 'project')
    - room: Sub-area (e.g., 'documentation', 'workflow')
    - hall: Specific topic (e.g., 'kb-optimization', 'treechat')

    Filters are interpreted as keywords or content markers.

    Args:
        searcher: HybridSearch instance (for .search() and .db_conn)
        query: Natural language or keyword query
        limit: Override default result limit
        wing: Filter by wing (category area)
        room: Filter by room (subcategory)
        hall: Filter by hall (specific topic)
        file_types: Filter by file extensions (e.g., ['md', 'pdf'])
        date_from: Filter by last_modified >= date (ISO format)
        date_to: Filter by last_modified <= date (ISO format)

    Returns:
        List of SearchResult ranked by combined score
    """
    if not query or not query.strip():
        return []

    query = query.strip()
    limit = limit or searcher.config.final_limit

    # Build filter keywords from wing/room/hall
    filter_keywords = []
    if wing:
        filter_keywords.append(f"wing:{wing}")
    if room:
        filter_keywords.append(f"room:{room}")
    if hall:
        filter_keywords.append(f"hall:{hall}")

    # Enhance query with filter keywords
    enhanced_query = query
    if filter_keywords:
        enhanced_query = f"{query} {' '.join(filter_keywords)}"

    # Get more results initially to account for filtering
    results = searcher.search(enhanced_query, limit=limit * 3)

    # Apply post-filters
    filtered = []
    for r in results:
        # File type filter
        if file_types:
            file_ext = Path(r.file_path).suffix.lstrip('.').lower()
            if not any(ft.lower() == file_ext for ft in file_types):
                continue

        # Date filter
        if date_from or date_to:
            # Get file last_modified from DB
            try:
                cursor = searcher.db_conn.execute(
                    "SELECT last_modified FROM files WHERE id = ?",
                    (r.file_id,)
                )
                row = cursor.fetchone()
                if row and row[0]:
                    file_date_str = row[0]
                    # Parse date (handle various formats)
                    from datetime import datetime
                    try:
                        # Try ISO format first
                        file_date = datetime.fromisoformat(file_date_str.replace('Z', '+00:00'))
                    except ValueError:
                        try:
                            # Try simple date format
                            file_date = datetime.strptime(file_date_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            continue  # Skip if can't parse date

                    if date_from:
                        from_dt = datetime.fromisoformat(date_from)
                        if file_date < from_dt:
                            continue
                    if date_to:
                        to_dt = datetime.fromisoformat(date_to)
                        if file_date > to_dt:
                            continue

            except (ValueError, TypeError) as e:
                logger.debug(f"Date filter error, skipping filter: {e}")

        filtered.append(r)
        if len(filtered) >= limit:
            break

    logger.info(f"search_with_filters: {len(results)} -> {len(filtered)} after filtering")
    return filtered