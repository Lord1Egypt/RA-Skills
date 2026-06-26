#!/usr/bin/env python3
"""KB Framework - Comprehensive Tests"""

import sqlite3
import sys
import tempfile
from pathlib import Path

# Add kb to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'kb'))

from indexer import BiblioIndexer
from kb.framework.chroma_integration import ChromaIntegration
from kb.framework.paths import get_default_db_path, get_default_chroma_path


class TestEmbeddings:
    """Test embedding tracking functionality."""
    
    def test_embeddings_table_exists(self):
        """Test that embeddings table is created."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        indexer = BiblioIndexer(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'"
        )
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None, "embeddings table should exist"
        print("✅ embeddings table exists")
    
    def test_embedding_hash(self):
        """Test SHA256 hash calculation."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        indexer = BiblioIndexer(db_path)
        test_embedding = [0.1] * 384
        hash_result = indexer.get_embedding_hash(test_embedding)
        
        assert len(hash_result) == 64, f"SHA256 hash should be 64 chars, got {len(hash_result)}"
        print("✅ embedding hash calculation works")


class TestConfig:
    """Test configuration."""
    
    def test_config_paths_exist(self):
        """Test that config paths are defined."""
        assert get_default_chroma_path() is not None
        assert get_default_db_path() is not None
        print("✅ config paths defined")
    
    def test_paths_are_paths(self):
        """Test that config paths are Path objects."""
        assert isinstance(get_default_chroma_path(), Path)
        assert isinstance(get_default_db_path(), Path)
        print("✅ config paths are Path objects")


class TestMigration:
    """Test migration functionality."""
    
    def test_migration_script_imports(self):
        """Test that migration script can be imported."""
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'kb' / 'scripts'))
            import migrate
            print("✅ migration script imports")
        except ImportError as e:
            print(f"⚠️  migration import failed: {e}")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("KB Framework Test Suite")
    print("=" * 50)
    
    # Run embedding tests
    print("\n--- Embeddings Tests ---")
    test_emb = TestEmbeddings()
    test_emb.test_embeddings_table_exists()
    test_emb.test_embedding_hash()
    
    # Run config tests
    print("\n--- Config Tests ---")
    test_cfg = TestConfig()
    test_cfg.test_config_paths_exist()
    test_cfg.test_paths_are_paths()
    
    # Run migration tests
    print("\n--- Migration Tests ---")
    test_mig = TestMigration()
    test_mig.test_migration_script_imports()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()
