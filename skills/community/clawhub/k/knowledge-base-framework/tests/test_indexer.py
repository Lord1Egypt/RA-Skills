#!/usr/bin/env python3
"""
Tests for BiblioIndexer

Coverage target: 70-85% for BiblioIndexer class
"""

import pytest
import tempfile
import shutil
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add kb to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kb"))
sys.path.insert(0, str(Path(__file__).parent.parent / "kb" / "framework"))

from kb.indexer import BiblioIndexer, MarkdownIndexer, IndexingPlugin


def create_full_test_db(tmpdir):
    """Create a test database with complete schema matching production."""
    db_path = Path(tmpdir) / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            file_path TEXT,
            file_name TEXT,
            file_category TEXT,
            file_type TEXT,
            file_size INTEGER,
            line_count INTEGER,
            file_hash TEXT,
            last_modified TIMESTAMP,
            index_status TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_sections (
            id TEXT PRIMARY KEY,
            file_id TEXT,
            section_level INTEGER,
            section_header TEXT,
            parent_section_id TEXT,
            content_preview TEXT,
            content_full TEXT,
            line_start INTEGER,
            line_end INTEGER,
            keywords TEXT,
            word_count INTEGER,
            file_hash TEXT,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id TEXT PRIMARY KEY,
            keyword TEXT,
            normalized TEXT,
            usage_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS section_keywords (
            section_id TEXT,
            keyword_id TEXT,
            weight REAL DEFAULT 1.0,
            PRIMARY KEY (section_id, keyword_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            section_id TEXT UNIQUE NOT NULL,
            file_id TEXT,
            model TEXT DEFAULT 'all-MiniLM-L6-v2',
            dimension INTEGER DEFAULT 384,
            embedding_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()
    return db_path


class TestBiblioIndexerInit:
    """Tests for BiblioIndexer initialization."""
    
    def test_init_creates_database_connection(self):
        """Test that __init__ creates a database connection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            assert indexer.conn is not None
            assert indexer.db_path == str(db_path)
            
            indexer.close()
    
    def test_init_creates_embeddings_table(self):
        """Test that __init__ creates the embeddings tracking table."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            # Check embeddings table exists
            cursor = indexer.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'"
            )
            assert cursor.fetchone() is not None
            
            indexer.close()
    
    def test_context_manager(self):
        """Test BiblioIndexer works as a context manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            
            with BiblioIndexer(str(db_path)) as indexer:
                assert indexer.conn is not None
                indexer.conn.execute("SELECT 1")  # Innerhalb des with-Blocks
            
            # Connection should be closed after context
            try:
                indexer.conn.execute("SELECT 1")
                assert False, "Should have raised error"
            except (sqlite3.ProgrammingError, AttributeError):
                pass  # Expected - conn is None or closed
    
    def test_init_with_plugins(self):
        """Test initialization with plugin list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            
            mock_plugin = Mock(spec=IndexingPlugin)
            indexer = BiblioIndexer(str(db_path), plugins=[mock_plugin])
            
            assert mock_plugin in indexer.plugins
            
            indexer.close()


class TestBiblioIndexerIndexFile:
    """Tests for index_file method."""
    
    def test_index_file_returns_zero_for_nonexistent(self):
        """Test that index_file returns 0 for non-existent files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            result = indexer.index_file(Path("/nonexistent/file.md"))
            
            assert result == 0
            indexer.close()
    
    def test_index_file_returns_zero_for_non_md(self):
        """Test that index_file returns 0 for non-markdown files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("some content")
            
            result = indexer.index_file(test_file)
            
            assert result == 0
            indexer.close()
    
    def test_index_file_indexes_markdown_file(self):
        """Test that index_file correctly indexes a markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_md = Path(tmpdir) / "test.md"
            test_md.write_text("# Header 1\nSome content here.\n\n## Header 2\nMore content.\n")
            
            result = indexer.index_file(test_md)
            
            assert result > 0
            
            cursor = indexer.conn.execute(
                "SELECT * FROM files WHERE file_path = ?",
                (str(test_md),)
            )
            assert cursor.fetchone() is not None
            
            indexer.close()
    
    def test_index_file_updates_existing_file(self):
        """Test that index_file updates an already indexed file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_md = Path(tmpdir) / "test.md"
            test_md.write_text("# Header\nOriginal content.")
            
            indexer.index_file(test_md)
            
            cursor = indexer.conn.execute(
                "SELECT file_hash FROM files WHERE file_path = ?",
                (str(test_md),)
            )
            original_hash = cursor.fetchone()[0]
            
            test_md.write_text("# Header\nModified content.")
            indexer.index_file(test_md)
            
            cursor = indexer.conn.execute(
                "SELECT file_hash FROM files WHERE file_path = ?",
                (str(test_md),)
            )
            new_hash = cursor.fetchone()[0]
            
            assert new_hash != original_hash
            indexer.close()
    
    def test_index_file_skips_unchanged_file(self):
        """Test that index_file skips files with same hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_md = Path(tmpdir) / "test.md"
            test_md.write_text("# Header\nSome content.")
            
            indexer.index_file(test_md)
            
            cursor = indexer.conn.execute("SELECT COUNT(*) FROM file_sections")
            original_count = cursor.fetchone()[0]
            
            result = indexer.index_file(test_md)
            
            assert result == 0  # Should skip
            
            indexer.close()


class TestBiblioIndexerRemoveFile:
    """Tests for remove_file method."""
    
    def test_remove_file_deletes_file(self):
        """Test that remove_file deletes the file from database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_md = Path(tmpdir) / "test.md"
            test_md.write_text("# Header\nContent.")
            
            indexer.index_file(test_md)
            result = indexer.remove_file(str(test_md))
            
            assert result == True
            
            cursor = indexer.conn.execute(
                "SELECT * FROM files WHERE file_path = ?",
                (str(test_md),)
            )
            assert cursor.fetchone() is None
            
            indexer.close()
    
    def test_remove_file_returns_false_for_nonexistent(self):
        """Test that remove_file returns False for non-existent files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            result = indexer.remove_file("/nonexistent/file.md")
            
            assert result == False
            indexer.close()


class TestBiblioIndexerIndexDirectory:
    """Tests for index_directory method."""
    
    def test_index_directory_indexes_all_md_files(self):
        """Test that index_directory indexes all .md files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_dir = Path(tmpdir) / "docs"
            test_dir.mkdir()
            
            (test_dir / "doc1.md").write_text("# Doc 1\nContent.")
            (test_dir / "doc2.md").write_text("# Doc 2\nContent.")
            (test_dir / "doc3.txt").write_text("Not a md file.")
            
            stats = indexer.index_directory(str(test_dir), recursive=False)
            
            assert stats['files'] == 2
            
            indexer.close()
    
    def test_index_directory_recursive(self):
        """Test recursive directory indexing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            test_dir = Path(tmpdir) / "docs"
            sub_dir = test_dir / "sub"
            sub_dir.mkdir(parents=True)
            
            (test_dir / "doc1.md").write_text("# Doc 1\nContent.")
            (sub_dir / "doc2.md").write_text("# Doc 2\nContent.")
            
            stats = indexer.index_directory(str(test_dir), recursive=True)
            assert stats['files'] == 2
            
            indexer.close()


class TestMarkdownIndexer:
    """Tests for MarkdownIndexer class."""
    
    def test_parse_file_splits_by_headers(self):
        """Test that parse_file correctly splits by headers."""
        indexer = MarkdownIndexer("dummy.db")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_md = Path(tmpdir) / "test.md"
            test_md.write_text("# Main Header\nContent under main header.\n\n## Sub Header\nContent under sub header.\n")
            
            sections = indexer.parse_file(test_md)
            
            assert len(sections) >= 2
            
            first_section = sections[0]
            assert first_section['section_header'] == 'Main Header'
            assert first_section['section_level'] == 1
    
    def test_extract_keywords_filters_stopwords(self):
        """Test that keyword extraction filters stopwords."""
        indexer = MarkdownIndexer("dummy.db")
        
        text = "Der hund und die katze sind sehr nette tiere"
        keywords = indexer._extract_keywords(text)
        
        assert 'der' not in keywords
        assert 'und' not in keywords
        assert 'hund' in keywords or 'katze' in keywords or 'tiere' in keywords
    
    def test_normalize_keyword_converts_umlauts(self):
        """Test that keyword normalization converts umlauts."""
        indexer = MarkdownIndexer("dummy.db")
        
        result = indexer._normalize_keyword("Ärger")
        assert 'ae' in result
        assert result == "aerger"
        
        assert indexer._normalize_keyword("Übung") == "uebung"
        assert indexer._normalize_keyword("Öl") == "oel"
        assert indexer._normalize_keyword("Straße").lower() == "strasse"


class TestIndexingPlugin:
    """Tests for IndexingPlugin abstract base class."""
    
    def test_plugin_can_be_subclassed(self):
        """Test that IndexingPlugin can be subclassed."""
        class TestPlugin(IndexingPlugin):
            def on_file_indexed(self, file_path, sections, file_id):
                pass
            
            def on_file_removed(self, file_path):
                pass
        
        plugin = TestPlugin()
        assert isinstance(plugin, IndexingPlugin)
    
    def test_plugin_on_indexing_complete_optional(self):
        """Test that on_indexing_complete is optional."""
        class MinimalPlugin(IndexingPlugin):
            def on_file_indexed(self, file_path, sections, file_id):
                pass
            
            def on_file_removed(self, file_path):
                pass
        
        plugin = MinimalPlugin()
        plugin.on_indexing_complete({'files': 0, 'sections': 0})


class TestBiblioIndexerStats:
    """Tests for stats methods."""
    
    def test_index_unindexed_handles_missing_dir(self):
        """Test index_unindexed handles missing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_full_test_db(tmpdir)
            indexer = BiblioIndexer(str(db_path))
            
            stats = indexer.index_unindexed("/nonexistent/dir")
            
            assert stats['files'] == 0
            assert stats['sections'] == 0
            
            indexer.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
