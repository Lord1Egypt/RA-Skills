#!/usr/bin/env python3
"""
MarkdownIndexer - Indexes Markdown files by header structure.
Core component of the knowledge base search engine.

Plugin System:
    The IndexingPlugin ABC allows flexible integration with external systems
    like ChromaDB for vector embeddings.
"""

import hashlib
import json
import logging
import re
import shutil
import sqlite3
import uuid
from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

# Maximum content preview length for database storage
MAX_CONTENT_PREVIEW = 200


class IndexingPlugin(ABC):
    """
    Abstract Base Class for indexing plugins.

    Plugins are called after successful file indexing and enable
    flexible post-processing actions (e.g., ChromaDB embedding).

    Example:
        class ChromaDBPlugin(IndexingPlugin):
            def on_file_indexed(self, file_path: Path, sections: int, file_id: str) -> None:
                # Queue for background embedding
                pass
    """

    @abstractmethod
    def on_file_indexed(self, file_path: Path, sections: int, file_id: str) -> None:
        """
        Callback after successful file indexing.

        Args:
            file_path: Path to the indexed file
            sections: Number of indexed sections
            file_id: UUID of the file in the database
        """
        pass

    @abstractmethod
    def on_file_removed(self, file_path: Path) -> None:
        """
        Callback after file removal from the index.

        Args:
            file_path: Path of the removed file
        """
        pass

    def on_indexing_complete(self, stats: dict) -> None:
        """
        Optional callback after full indexing (index_directory, check_and_update).

        Args:
            stats: Statistics dict with 'files' and 'sections' counters
        """
        pass


class MarkdownIndexer:
    """Indexes Markdown files by header structure."""

    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')

    # Stopwords for keyword extraction
    # These words are ignored during keyword extraction.
    # Typical German filler words (articles, conjunctions, prepositions)
    # that have no semantic meaning for search.
    STOPWORDS = {
        'der', 'die', 'das', 'und', 'oder', 'mit', 'fuer', 'von', 'auf', 'in', 'zu',
        'ist', 'sind', 'war', 'wurden', 'wird', 'werden', 'kann', 'koennen',
        'eine', 'einer', 'einem', 'einen', 'als', 'an', 'auch', 'bei', 'bis',
        'durch', 'hat', 'nach', 'nicht', 'nur', 'ob', 'oder', 'sich',
        'sie', 'sind', 'so', 'sowie', 'um', 'unter', 'von', 'vor', 'wenn',
        'wie', 'wird', 'noch', 'schon', 'sehr', 'wurde', 'wurden', 'sein'
    }

    # Umlaut mapping for keyword normalization
    UMLAUT_MAP = {'ae': 'ae', 'oe': 'oe', 'ue': 'ue', 'ss': 'ss', 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}

    def __init__(self, db_path: str):
        self.db_path = db_path

    def parse_file(self, file_path: Path) -> List[dict]:
        """
        Parse a MD file into sections.

        Headers (# ## ###) define section boundaries.
        """
        sections = []
        header_stack: List[tuple] = []  # (level, header_text)
        current_section = {
            'header': None,
            'level': 0,
            'content': [],
            'line_start': 1,
            'parent_header': None,
            'parent_level': 0
        }

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            match = self.HEADER_PATTERN.match(line)

            if match:
                # Save previous section
                if current_section['header']:
                    sections.append(self._build_section(
                        current_section, file_path, i - 1
                    ))

                level = len(match.group(1))
                header_text = match.group(2).strip()

                # Update hierarchy (pop to parent level)
                header_stack = header_stack[:level - 1]
                parent_header = header_stack[-1][1] if header_stack else None
                parent_level = header_stack[-1][0] if header_stack else 0
                header_stack.append((level, header_text))

                # Start new section
                current_section = {
                    'header': header_text,
                    'level': level,
                    'content': [],
                    'line_start': i,
                    'parent_header': parent_header,
                    'parent_level': parent_level
                }
            else:
                current_section['content'].append(line)

        # Save last section
        if current_section['header']:
            sections.append(self._build_section(
                current_section, file_path, len(lines)
            ))

        return sections

    def _build_section(self, section_data: dict, file_path: Path, line_end: int) -> dict:
        """
        Build a section data record.

        Creates a ready-to-insert dict for database insertion.
        """
        content = ''.join(section_data['content'])
        keywords = self._extract_keywords(content)

        return {
            'file_path': str(file_path),
            'section_header': section_data['header'],
            'section_level': section_data['level'],
            'parent_header': section_data['parent_header'],
            'content_full': content,
            'content_preview': content[:MAX_CONTENT_PREVIEW] + '...' if len(content) > MAX_CONTENT_PREVIEW else content,
            'line_start': section_data['line_start'],
            'line_end': line_end,
            'word_count': len(content.split()),
            'keywords': keywords,
            'file_hash': self._hash_file(file_path)
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text.

        Strategy:
        - Words with 4+ letters
        - Remove stopwords
        - Top 10 by frequency
        """
        # Words with 4+ letters
        words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', text.lower())
        # Remove stopwords
        keywords = [w for w in words if w not in self.STOPWORDS]
        # Top 10 by frequency
        return [k for k, _ in Counter(keywords).most_common(10)]

    def _hash_file(self, file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        return hashlib.md5(file_path.read_bytes()).hexdigest()

    def _categorize_file(self, path: Path) -> str:
        """
        Categorize file based on path/name.

        Categories: learnings, adr, briefing, projektplanung, dokumentation
        """
        name = path.name.lower()
        parent = path.parent.name
        path_str = str(path)

        if 'learnings' in parent or 'learning' in name:
            return 'learnings'
        elif 'adr' in name or 'architecture' in parent:
            return 'adr'
        elif 'briefing' in name:
            return 'briefing'
        elif 'projektplanung' in path_str:
            return 'projektplanung'
        return 'dokumentation'

    def _normalize_keyword(self, keyword: str) -> str:
        """
        Normalize keyword (lowercase, replace umlauts).

        Example: 'Aerger' -> 'aeger'
        """
        normalized = keyword.lower()
        for k, v in self.UMLAUT_MAP.items():
            normalized = normalized.replace(k, v)
        return normalized


class BiblioIndexer:
    """
    Full indexer with database connection and plugin system.

    Supports Context Manager protocol for automatic cleanup.

    Plugin system enables flexible post-processing like ChromaDB embedding.

    Example:
        with BiblioIndexer("knowledge.db", plugins=[ChromaDBPlugin()]) as indexer:
            indexer.index_file("test.md")
        # -> SQLite + ChromaDB (automatic via plugin)
    """

    def __init__(self, db_path: str, plugins: List[IndexingPlugin] = None):
        """
        Initialize BiblioIndexer with database connection.

        Args:
            db_path: Path to SQLite database
            plugins: Optional list of IndexingPlugin instances

        Raises:
            FileNotFoundError: If database directory does not exist
            sqlite3.Error: On database connection errors
        """
        self.db_path = db_path
        self.plugins = plugins or []

        # Validate: database directory must exist
        db_dir = Path(db_path).parent
        if db_dir and not db_dir.exists():
            raise FileNotFoundError(
                f"Database directory not found: {db_dir}\n"
                f"Please create the directory or check the path."
            )

        self.indexer = MarkdownIndexer(db_path)
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA foreign_key_check")
        self.conn.row_factory = sqlite3.Row

        # Create embeddings tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY,
                section_id TEXT UNIQUE NOT NULL,
                file_id TEXT,
                model TEXT DEFAULT 'all-MiniLM-L6-v2',
                dimension INTEGER DEFAULT 384,
                embedding_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (section_id) REFERENCES file_sections(id) ON DELETE CASCADE,
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_section_id ON embeddings(section_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_file_id ON embeddings(file_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_hash ON embeddings(embedding_hash)")
        self.conn.commit()

    def __enter__(self):
        """Context Manager Entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manager Exit - closes DB connection."""
        self.close()
        return False

    def remove_file(self, file_path: str) -> bool:
        """
        Remove a file from the index.

        Deletes all related sections (CASCADE) and file entry.
        """
        try:
            # Get file_id
            file_id = self.conn.execute(
                "SELECT id FROM files WHERE file_path = ?",
                (file_path,)
            ).fetchone()

            if not file_id:
                logger.warning(f"File not found: {file_path}")
                return False

            file_id = file_id[0]

            # Delete sections (first section_keywords, then file_sections)
            self.conn.execute(
                "DELETE FROM section_keywords WHERE section_id IN (SELECT id FROM file_sections WHERE file_id = ?)",
                (file_id,)
            )
            self.conn.execute(
                "DELETE FROM file_sections WHERE file_id = ?",
                (file_id,)
            )
            self.conn.execute(
                "DELETE FROM files WHERE file_path = ?",
                (file_path,)
            )
            self.conn.commit()
            logger.info(f"Removed: {file_path}")

            # Plugin callbacks
            for plugin in self.plugins:
                try:
                    plugin.on_file_removed(Path(file_path))
                except Exception as e:
                    logger.warning(f"Plugin {plugin.__class__.__name__} on_file_removed failed: {e}")

            return True
        except Exception as e:
            logger.error(f"Error removing file: {e}")
            return False

    def get_embedding_hash(self, embedding) -> str:
        """Calculate SHA256 hash of an embedding vector."""
        import hashlib
        import json
        vec_str = json.dumps(embedding.tolist() if hasattr(embedding, 'tolist') else embedding)
        return hashlib.sha256(vec_str.encode()).hexdigest()

    def close(self):
        """Close database connection."""
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
            finally:
                self.conn = None

    def _get_or_create_keyword(self, keyword: str) -> Optional[str]:
        """Get or create keyword entry."""
        normalized = self.indexer._normalize_keyword(keyword)

        existing = self.conn.execute(
            "SELECT id FROM keywords WHERE normalized = ?",
            (normalized,)
        ).fetchone()

        if existing:
            self.conn.execute(
                "UPDATE keywords SET usage_count = usage_count + 1 WHERE id = ?",
                (existing['id'],)
            )
            return existing['id']

        keyword_id = str(uuid.uuid4())
        self.conn.execute("""
            INSERT INTO keywords (id, keyword, normalized, usage_count)
            VALUES (?, ?, ?, 1)
        """, (keyword_id, keyword, normalized))
        return keyword_id

    def index_file(self, file_path: Path) -> int:
        """
        Index a single file.

        Args:
            file_path: Path to .md file

        Returns:
            Number of indexed sections (0 if unchanged)
        """
        if not file_path.exists() or not file_path.name.endswith('.md'):
            return 0

        current_hash = self.indexer._hash_file(file_path)

        # Check if anything changed
        existing = self.conn.execute(
            "SELECT id, file_hash FROM files WHERE file_path = ?",
            (str(file_path),)
        ).fetchone()

        if existing and existing['file_hash'] == current_hash:
            logger.debug(f"Unchanged: {file_path.name}")
            return 0

        # Delete old entries (CASCADE handles section_keywords)
        file_id = existing['id'] if existing else None
        if file_id:
            self.conn.execute(
                "DELETE FROM file_sections WHERE file_id = ?",
                (file_id,)
            )
        self.conn.execute(
            "DELETE FROM files WHERE file_path = ?",
            (str(file_path),)
        )

        # File metadata
        file_id = str(uuid.uuid4())
        category = self.indexer._categorize_file(file_path)
        content = file_path.read_text(encoding='utf-8')
        line_count = len(content.splitlines())

        self.conn.execute("""
            INSERT INTO files
            (id, file_path, file_name, file_category, file_type,
             file_size, line_count, file_hash, last_modified, index_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'indexed')
        """, (
            file_id,
            str(file_path),
            file_path.name,
            category,
            file_path.suffix[1:],
            file_path.stat().st_size,
            line_count,
            current_hash,
            datetime.fromtimestamp(file_path.stat().st_mtime)
        ))

        # Index sections
        sections = self.indexer.parse_file(file_path)
        section_id_map: dict = {}  # header -> id for FK

        for section in sections:
            section_id = str(uuid.uuid4())
            section_id_map[section['section_header']] = section_id

            # Resolve parent ID
            parent_section_id = None
            if section.get('parent_header') and section['parent_header'] in section_id_map:
                parent_section_id = section_id_map[section['parent_header']]

            self.conn.execute("""
                INSERT INTO file_sections
                (id, file_id, section_level, section_header, parent_section_id,
                 content_preview, content_full, line_start, line_end,
                 keywords, word_count, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                section_id,
                file_id,
                section['section_level'],
                section['section_header'],
                parent_section_id,
                section['content_preview'],
                section['content_full'],
                section['line_start'],
                section['line_end'],
                json.dumps(section['keywords']),
                section['word_count'],
                current_hash
            ))

            # Register keywords in section_keywords
            for keyword in section['keywords']:
                keyword_id = self._get_or_create_keyword(keyword)
                if keyword_id:
                    self.conn.execute("""
                        INSERT OR IGNORE INTO section_keywords
                        (section_id, keyword_id, weight)
                        VALUES (?, ?, 1.0)
                    """, (section_id, keyword_id))

        self.conn.commit()
        logger.info(f"Indexed: {file_path.name}: {len(sections)} sections")

        # Plugin callbacks after successful indexing
        for plugin in self.plugins:
            try:
                plugin.on_file_indexed(Path(file_path), len(sections), file_id)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} on_file_indexed failed: {e}")

        return len(sections)

    def index_directory(self, dir_path: str, recursive: bool = True) -> dict:
        """
        Index all .md files in a directory.

        Args:
            dir_path: Directory path
            recursive: Also search subdirectories

        Returns:
            Dict with 'files' and 'sections' counters
        """
        path = Path(dir_path)
        if not path.exists():
            logger.warning(f"Directory not found: {dir_path}")
            return {'files': 0, 'sections': 0}

        pattern = "**/*.md" if recursive else "*.md"
        md_files = list(path.glob(pattern))

        stats = {'files': 0, 'sections': 0}

        for md_file in sorted(md_files):
            sections = self.index_file(md_file)
            if sections > 0:
                stats['files'] += 1
                stats['sections'] += sections

        # Plugin callbacks after completed indexing
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'on_indexing_complete'):
                    plugin.on_indexing_complete(stats)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} on_indexing_complete failed: {e}")

        return stats

    def full_reindex(self, root_paths: List[str]) -> dict:
        """
        Full reindexing of all files.

        Args:
            root_paths: List of directories to index

        Returns:
            Aggregated statistics
        """
        total_stats = {'files': 0, 'sections': 0}

        for root in root_paths:
            logger.info(f"Indexing: {root}")
            stats = self.index_directory(root)
            total_stats['files'] += stats['files']
            total_stats['sections'] += stats['sections']

        return total_stats

    def check_and_update(self, watch_paths: List[str]) -> dict:
        """
        Check for changes and update only when needed.

        True delta indexing logic:
        - Compares file_hash with stored hash
        - Indexes only changed files
        - Deletes removed files from index

        Args:
            watch_paths: List of directories to watch

        Returns:
            Dict with statistics (files_updated, files_removed, sections)
        """
        stats = {'files_updated': 0, 'files_removed': 0, 'sections': 0}

        for watch_path in watch_paths:
            path = Path(watch_path)
            if not path.exists():
                logger.warning(f"Watch path not found: {watch_path}")
                continue

            # Collect current .md files
            md_files = {str(f): f for f in path.glob("**/*.md")}

            # Get already indexed files
            indexed_files = {}
            cursor = self.conn.execute(
                "SELECT file_path, file_hash FROM files"
            )
            while True:
                rows = cursor.fetchmany(1000)  # Batch von 1000
                if not rows:
                    break
                for row in rows:
                    indexed_files[row['file_path']] = row['file_hash']

            # Check for updates (changed or new files)
            for file_path, abs_path in md_files.items():
                if not abs_path.exists():
                    continue

                current_hash = self.indexer._hash_file(abs_path)

                if file_path not in indexed_files:
                    # New file - index
                    logger.info(f"New: {abs_path.name}")
                    sections = self.index_file(abs_path)
                    if sections > 0:
                        stats['files_updated'] += 1
                        stats['sections'] += sections

                elif indexed_files[file_path] != current_hash:
                    # Changed file - reindex
                    logger.info(f"Changed: {abs_path.name}")
                    sections = self.index_file(abs_path)
                    if sections > 0:
                        stats['files_updated'] += 1
                        stats['sections'] += sections

            # Find and delete removed files
            for indexed_path in indexed_files:
                if indexed_path not in md_files:
                    logger.info(f"Removed: {Path(indexed_path).name}")
                    self.remove_file(indexed_path)
                    stats['files_removed'] += 1

        logger.info(f"Delta index: {stats['files_updated']} updated, "
                   f"{stats['files_removed']} removed, {stats['sections']} sections")

        # Plugin callbacks after completed delta indexing
        for plugin in self.plugins:
            try:
                if hasattr(plugin, 'on_indexing_complete'):
                    plugin.on_indexing_complete(stats)
            except Exception as e:
                logger.warning(f"Plugin {plugin.__class__.__name__} on_indexing_complete failed: {e}")

        return stats

    def index_unindexed(self, unindexed_dir: str = "unindexed") -> dict:
        """
        Index files from the unindexed/ folder.

        This method finds all files in the unindexed/ directory
        and automatically indexes them into the database.

        Args:
            unindexed_dir: Path to unindexed directory (relative or absolute)

        Returns:
            Dict with 'files' and 'sections' counters
        """
        unindexed_path = Path(unindexed_dir)

        if not unindexed_path.exists():
            logger.info(f"Unindexed directory not found: {unindexed_dir}")
            return {'files': 0, 'sections': 0}

        # Find all .md files
        md_files = list(unindexed_path.glob("*.md"))

        if not md_files:
            logger.info(f"No .md files in {unindexed_dir}")
            return {'files': 0, 'sections': 0}

        logger.info(f"Found {len(md_files)} files to index")

        stats = {'files': 0, 'sections': 0}

        for md_file in sorted(md_files):
            # Move to corresponding target directory
            target_path = Path("projektplanung") / md_file.name

            # Index the file
            sections = self.index_file(md_file)

            if sections > 0:
                stats['files'] += 1
                stats['sections'] += sections

                # Optionally move indexed file
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(md_file), str(target_path))
                    logger.info(f"Moved: {md_file.name} -> {target_path}")
                except Exception as e:
                    logger.warning(f"Move failed: {e}")

        return stats


def main():
    """CLI for Indexer."""
    import sys

    # Default paths from config
    db_path = sys.argv[1] if len(sys.argv) > 1 else "knowledge.db"
    root_paths = KBConfig.get_instance().index_roots
    
    if len(sys.argv) > 2:
        root_paths = sys.argv[2:]

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )

    indexer = BiblioIndexer(db_path)

    logger.info(f"Starting indexing to {db_path}")
    logger.info(f"   Directories: {', '.join(root_paths)}\n")

    stats = indexer.full_reindex(root_paths)

    logger.info(f"\nResult: {stats['files']} files, {stats['sections']} sections indexed")

    indexer.close()


if __name__ == "__main__":
    main()
