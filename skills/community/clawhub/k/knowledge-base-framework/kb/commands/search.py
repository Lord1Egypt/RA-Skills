#!/usr/bin/env python3
"""
SearchCommand - Hybrid Search CLI

Integration: HybridSearch aus kb.library.knowledge_base.hybrid_search

Features:
- Hybrid Search: Semantic (ChromaDB) + Keyword (SQLite) combined
- Fallback: If ChromaDB unavailable, keyword-only search
- Line numbers from file_sections if available
- Section headers as fallback when line numbers missing
- Filters: file-type, date-from, date-to
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from kb.base.command import BaseCommand
from kb.commands import register_command
from kb.framework.hybrid_search import HybridSearch, SearchResult


@register_command
class SearchCommand(BaseCommand):
    """KB Hybrid Search – Semantische + Keyword Suche."""

    name = "search"
    help = "Search knowledge base (hybrid: semantic + keyword)"

    DEFAULT_LIMIT = 20
    DEFAULT_FORMAT = "short"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            'query',
            nargs='+',
            help='Search query (multi-word allowed)'
        )
        parser.add_argument(
            '--limit', '-n', '-l',
            type=int,
            default=self.DEFAULT_LIMIT,
            help=f'Max results (default: {self.DEFAULT_LIMIT})'
        )
        parser.add_argument(
            '--semantic-only', '-s',
            action='store_true',
            help='Only semantic search (ChromaDB vector)'
        )
        parser.add_argument(
            '--keyword-only', '-k',
            action='store_true',
            help='Only keyword search (SQLite LIKE)'
        )
        parser.add_argument(
            '--format', '-f',
            choices=['short', 'full'],
            default=self.DEFAULT_FORMAT,
            help='Output format (default: short)'
        )
        parser.add_argument(
            '--file-type', '--ft',
            dest='file_types',
            action='append',
            help='Filter by file type (e.g., md, pdf)'
        )
        parser.add_argument(
            '--date-from',
            help='Filter by date from (ISO format: YYYY-MM-DD)'
        )
        parser.add_argument(
            '--date-to',
            help='Filter by date to (ISO format: YYYY-MM-DD)'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Show debug info (scores, sources)'
        )

    def _execute(self) -> int:
        log = self.get_logger()
        config = self.get_config()

        # Build query string from args
        query = ' '.join(self._args.query)
        if not query.strip():
            log.error("Empty query not allowed")
            return self.EXIT_VALIDATION_ERROR

        # Detect mode
        semantic_only = self._args.semantic_only
        keyword_only = self._args.keyword_only
        
        # Handle conflicting flags
        if semantic_only and keyword_only:
            log.warning("Cannot use both --semantic-only and --keyword-only, using hybrid")
            semantic_only = False
            keyword_only = False

        # Initialize HybridSearch
        try:
            searcher = HybridSearch(
                db_path=str(config.db_path),
                chroma_path=str(config.chroma_path)
            )
        except Exception as e:
            log.error(f"Failed to initialize search: {e}")
            return self.EXIT_EXECUTION_ERROR

        try:
            # Check if ChromaDB is available for semantic search
            chroma_available = self._check_chroma_available(searcher)
            
            if semantic_only and not chroma_available:
                log.warning("ChromaDB not available, using keyword-only search instead")
                keyword_only = True
                semantic_only = False

            # Execute search based on mode
            if self._has_filters():
                # Use search_with_filters for file-type/date filters
                results = searcher.search_with_filters(
                    query=query,
                    limit=self._args.limit,
                    file_types=self._args.file_types,
                    date_from=self._args.date_from,
                    date_to=self._args.date_to
                )
            elif semantic_only:
                results = searcher.search_semantic(query, limit=self._args.limit)
            elif keyword_only:
                results = searcher.search_keyword(query, limit=self._args.limit)
            else:
                results = searcher.search(query, limit=self._args.limit)

        except Exception as e:
            log.error(f"Search failed: {e}")
            if self._args.debug:
                import traceback
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR
        finally:
            try:
                searcher.close()
            except Exception:
                pass  # Don't mask original error

        # Output results
        if not results:
            mode = self._get_search_mode(semantic_only, keyword_only, chroma_available)
            log.info(f"No results found for '{query}' ({mode})")
            return self.EXIT_SUCCESS

        # Log summary
        mode = self._get_search_mode(semantic_only, keyword_only, chroma_available)
        log.info(f"Found {len(results)} results for '{query}' ({mode}):\n")

        # Print results
        for r in results:
            self._print_result(r)

        return self.EXIT_SUCCESS

    def _check_chroma_available(self, searcher: HybridSearch) -> bool:
        """Check if ChromaDB is available for semantic search."""
        try:
            stats = searcher.get_stats()
            return stats.get('chroma_sections', 0) > 0
        except Exception:
            return False

    def _has_filters(self) -> bool:
        """Check if any filters are specified."""
        return bool(
            self._args.file_types or
            self._args.date_from or
            self._args.date_to
        )

    def _get_search_mode(self, semantic_only: bool, keyword_only: bool, chroma_available: bool) -> str:
        """Get human-readable search mode description."""
        if semantic_only:
            return "semantic only"
        elif keyword_only:
            return "keyword only"
        elif not chroma_available:
            return "hybrid (keyword fallback)"
        else:
            return "hybrid"

    def _print_result(self, r: SearchResult) -> None:
        """Print a single search result."""
        log = self.get_logger()
        path = Path(r.file_path)

        if self._args.format == 'full':
            self._print_result_full(r)
        else:
            self._print_result_short(r, path)

    def _print_result_short(self, r: SearchResult, path: Path) -> None:
        """Print result in short format: 📄 filename:line [score] header"""
        log = self.get_logger()
        
        # Build location string: file:line or file (if no line)
        filename = path.name
        location = self._get_location_string(r, filename)
        
        # Score
        score_str = f"[{r.combined_score:.2f}]"
        
        # Build header text - show section_header or content preview
        header_text = r.section_header if r.section_header else self._truncate_content(r.content_preview)
        
        # Debug info
        debug_info = ""
        if self._args.debug:
            src = r.source or "unknown"
            sem = f"sem={r.semantic_score:.2f}" if r.semantic_score > 0 else ""
            kw = f"kw={r.keyword_score:.2f}" if r.keyword_score > 0 else ""
            parts = [p for p in [src, sem, kw] if p]
            debug_info = f" ({', '.join(parts)})"
        
        log.info(f"📄 {location} {score_str} {header_text}{debug_info}")

    def _print_result_full(self, r: SearchResult) -> None:
        """Print result in full format with all details."""
        log = self.get_logger()
        
        log.info(f"📄 {r.file_path}")
        log.info(f"   Header: {r.section_header or '(none)'}")
        log.info(f"   Score: combined={r.combined_score:.3f} (sem={r.semantic_score:.3f}, kw={r.keyword_score:.2f})")
        log.info(f"   Source: {r.source or 'unknown'}")
        
        if r.content_preview:
            preview = self._truncate_content(r.content_preview, max_len=200)
            log.info(f"   Preview: {preview}")
        
        log.info("")

    def _get_location_string(self, r: SearchResult, filename: str) -> str:
        """
        Build location string for short format.
        
        Priority:
        1. file:line_start (if line_start available)
        2. file (section_header only if line_start missing)
        """
        # Check if line_start is available and meaningful
        line_start = getattr(r, 'line_start', None)
        
        if line_start and line_start > 0:
            return f"{filename}:{line_start}"
        else:
            # No line number available - just show filename
            # If section_header is long, show truncated
            return filename

    def _truncate_content(self, content: str, max_len: int = 80) -> str:
        """Truncate content for display."""
        if not content:
            return ""
        content = content.replace('\n', ' ').strip()
        if len(content) > max_len:
            return content[:max_len-3] + "..."
        return content


# --- Import for type hints ---
from pathlib import Path