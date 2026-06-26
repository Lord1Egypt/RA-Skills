#!/usr/bin/env python3
"""
Tests for Obsidian Backlink Indexer Module

Tests the inverted index for backlinks and unlinked mentions.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.indexer import BacklinkIndexer, index_vault, get_backlinks


class TestBacklinkIndexer(unittest.TestCase):
    """Test BacklinkIndexer class."""
    
    def setUp(self):
        """Create temporary vault for testing."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.indexer = BacklinkIndexer(self.vault_path)
        
        # Create test structure:
        # vault/
        #   Note A.md - links to Note B, Note C
        #   Note B.md - links to Note A
        #   Note C.md - no links
        #   Folder/
        #     Note D.md - links to Note A
        
        self.note_a = self.vault_path / "Note A.md"
        self.note_a.write_text("# Note A\nSee [[Note B]] and [[Note C]] for details.\n")
        
        self.note_b = self.vault_path / "Note B.md"
        self.note_b.write_text("# Note B\nRelated to [[Note A]].\n")
        
        self.note_c = self.vault_path / "Note C.md"
        self.note_c.write_text("# Note C\nNo links here.\n")
        
        self.folder_dir = self.vault_path / "Folder"
        self.folder_dir.mkdir()
        self.note_d = self.folder_dir / "Note D.md"
        self.note_d.write_text("# Note D\nBack to [[Note A]] again.\n")
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.vault_dir)
    
    # =========================================================================
    # Basic Indexing Tests
    # =========================================================================
    
    def test_index_vault_creates_backlinks(self):
        """Test that index_vault builds the backlink index correctly."""
        self.indexer.index_vault()
        
        # Note B should have a backlink from Note A
        backlinks_b = self.indexer.get_backlinks(self.note_b)
        self.assertEqual(len(backlinks_b), 1)
        self.assertEqual(backlinks_b[0]['source'], self.note_a)
    
    def test_index_vault_multiple_backlinks(self):
        """Test that Note A has multiple backlinks."""
        self.indexer.index_vault()
        
        # Note A should have backlinks from Note B and Note D
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        self.assertEqual(len(backlinks_a), 2)
        
        sources = {b['source'] for b in backlinks_a}
        self.assertIn(self.note_b, sources)
        self.assertIn(self.note_d, sources)
    
    def test_note_with_no_incoming_links(self):
        """Test file that has outgoing links but no incoming links."""
        # Note C has outgoing link to Note A, but we check Note D which has no incoming
        # First verify Note A has backlinks (from B and D)
        self.indexer.index_vault()
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        self.assertEqual(len(backlinks_a), 2)
        
        # Now check Note D has NO backlinks (nothing links TO Note D)
        backlinks_d = self.indexer.get_backlinks(self.note_d)
        self.assertEqual(len(backlinks_d), 0)
    
    # =========================================================================
    # Context Extraction Tests
    # =========================================================================
    
    def test_backlink_context(self):
        """Test that backlink context is extracted correctly."""
        self.indexer.index_vault()
        
        backlinks_b = self.indexer.get_backlinks(self.note_b)
        self.assertEqual(len(backlinks_b), 1)
        
        context = backlinks_b[0]['context']
        self.assertIn('Note B', context)
    
    def test_link_text_extraction(self):
        """Test that link text (alias) is extracted correctly."""
        # Create note with aliased link
        aliased = self.vault_path / "Aliased.md"
        aliased.write_text("# Aliased\nSee [[Note B|Another Name]] here.\n")
        
        self.indexer.index_vault()
        
        backlinks_b = self.indexer.get_backlinks(self.note_b)
        # Find the backlink from aliased note
        aliased_links = [b for b in backlinks_b if b['source'] == aliased]
        self.assertEqual(len(aliased_links), 1)
        self.assertEqual(aliased_links[0]['link_text'], 'Another Name')
    
    # =========================================================================
    # Index File (Incremental Update) Tests
    # =========================================================================
    
    def test_index_file_updates_backlinks(self):
        """Test that index_file updates the backlink index."""
        self.indexer.index_vault()
        
        # Verify initial state
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        initial_count = len(backlinks_a)
        
        # Create new note linking to Note A
        new_note = self.vault_path / "New Note.md"
        new_note.write_text("# New\nAlso links to [[Note A]].\n")
        
        # Index just the new file
        self.indexer.index_file(new_note)
        
        # Should now have more backlinks
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        self.assertGreater(len(backlinks_a), initial_count)
    
    def test_index_file_updates_existing(self):
        """Test that index_file updates backlinks when source file changes."""
        self.indexer.index_vault()
        
        # Note B currently links to Note A
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        initial_from_b = [b for b in backlinks_a if b['source'] == self.note_b]
        self.assertEqual(len(initial_from_b), 1)
        
        # Change Note B to link to Note C instead
        self.note_b.write_text("# Note B\nNow links to [[Note C]] instead.\n")
        
        # Re-index Note B - note we need to invalidate cache so resolver sees new content
        self.indexer.resolver.invalidate_cache()
        self.indexer.index_file(self.note_b)
        
        # Note A should no longer have backlink from Note B
        backlinks_a = self.indexer.get_backlinks(self.note_a)
        from_b = [b for b in backlinks_a if b['source'] == self.note_b]
        self.assertEqual(len(from_b), 0)
        
        # Note C should now have backlink from Note B
        backlinks_c = self.indexer.get_backlinks(self.note_c)
        from_b_c = [b for b in backlinks_c if b['source'] == self.note_b]
        self.assertEqual(len(from_b_c), 1)
    
    # =========================================================================
    # Unlinked Mentions Tests
    # =========================================================================
    
    def test_unlinked_mentions(self):
        """Test finding mentions without wikilinks."""
        # Add a mention without link
        self.note_b.write_text("# Note B\nMentions 'Python' without linking.\n")
        self.indexer.index_file(self.note_b)
        
        mentions = self.indexer.get_unlinked_mentions("Python")
        self.assertGreaterEqual(len(mentions), 1)
        
        # Should find in Note B
        note_b_mentions = [m for m in mentions if m['source'] == self.note_b]
        self.assertEqual(len(note_b_mentions), 1)
    
    def test_unlinked_mentions_excludes_links(self):
        """Test that unlinked mentions doesn't find wikilinks."""
        # Note A links to Note B
        mentions = self.indexer.get_unlinked_mentions("Note B")
        
        # Should NOT find the wikilink
        note_a_mentions = [m for m in mentions if m['source'] == self.note_a]
        self.assertEqual(len(note_a_mentions), 0)
    
    def test_unlinked_mentions_case_insensitive(self):
        """Test that unlinked mentions is case-insensitive."""
        self.note_c.write_text("# Note C\nMentions python and PYTHON.\n")
        self.indexer.index_file(self.note_c)
        
        mentions = self.indexer.get_unlinked_mentions("Python")
        self.assertGreaterEqual(len(mentions), 1)
    
    # =========================================================================
    # Stats Tests
    # =========================================================================
    
    def test_get_stats(self):
        """Test statistics generation."""
        self.indexer.index_vault()
        
        stats = self.indexer.get_stats()
        
        self.assertEqual(stats['total_files'], 4)  # A, B, C, D
        self.assertGreater(stats['total_links'], 0)
        self.assertGreater(stats['total_backlinks'], 0)
    
    # =========================================================================
    # WikiLink with Heading Tests
    # =========================================================================
    
    def test_backlinks_with_heading(self):
        """Test backlink index for links with heading anchors."""
        # Create isolated notes for this test
        source = self.vault_path / "Source.md"
        target = self.vault_path / "Target.md"
        target.write_text("# Target\n## Section\nContent\n")
        
        # Source links to Target#Section
        source.write_text("# Source\nSee [[Target#Section]] for details.\n")
        
        self.indexer.index_vault()
        
        backlinks_target = self.indexer.get_backlinks(target)
        self.assertEqual(len(backlinks_target), 1)
        self.assertEqual(backlinks_target[0]['heading'], 'Section')
    
    # =========================================================================
    # Edge Cases
    # =========================================================================
    
    def test_nonexistent_file(self):
        """Test getting backlinks for non-existent file."""
        self.indexer.index_vault()
        
        fake = self.vault_path / "Fake.md"
        backlinks = self.indexer.get_backlinks(fake)
        self.assertEqual(len(backlinks), 0)
    
    def test_empty_vault(self):
        """Test indexing empty vault."""
        empty_dir = tempfile.mkdtemp()
        try:
            empty_indexer = BacklinkIndexer(empty_dir)
            empty_indexer.index_vault()
            
            stats = empty_indexer.get_stats()
            self.assertEqual(stats['total_files'], 0)
        finally:
            shutil.rmtree(empty_dir)
    
    def test_case_insensitive_resolution(self):
        """Test backlinks work with case-insensitive file names."""
        # Note A links to note b (lowercase)
        self.note_a.write_text("# Note A\nLink to [[note b]].\n")
        
        self.indexer.index_vault()
        
        # Should still find backlink to Note B
        backlinks_b = self.indexer.get_backlinks(self.note_b)
        self.assertGreaterEqual(len(backlinks_b), 1)


class TestStandaloneFunctions(unittest.TestCase):
    """Test standalone index_vault and get_backlinks functions."""
    
    def setUp(self):
        """Create temporary vault."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        
        # Create simple structure
        self.note_a = self.vault_path / "Note A.md"
        self.note_a.write_text("# Note A\n")
        
        self.note_b = self.vault_path / "Note B.md"
        self.note_b.write_text("# Note B\nSee [[Note A]].\n")
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_index_vault_function(self):
        """Test index_vault() standalone function."""
        indexer = index_vault(self.vault_path)
        
        backlinks = indexer.get_backlinks(self.note_a)
        self.assertEqual(len(backlinks), 1)
        self.assertEqual(backlinks[0]['source'], self.note_b)
    
    def test_get_backlinks_function(self):
        """Test get_backlinks() standalone function."""
        backlinks = get_backlinks(self.note_a, self.vault_path)
        
        self.assertEqual(len(backlinks), 1)


class TestCrossFolderLinks(unittest.TestCase):
    """Test links between folders."""
    
    def setUp(self):
        """Create vault with folder structure."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.indexer = BacklinkIndexer(self.vault_path)
        
        # Create:
        # vault/
        #   Root.md - links to Folder/Nested.md
        #   Folder/
        #     Nested.md - links to Root.md
        #     index.md - links to Root.md
        
        self.root = self.vault_path / "Root.md"
        self.root.write_text("# Root\nSee [[Folder/Nested]] and [[Folder/index]].\n")
        
        self.folder_dir = self.vault_path / "Folder"
        self.folder_dir.mkdir()
        
        self.nested = self.folder_dir / "Nested.md"
        self.nested.write_text("# Nested\nBack to [[Root]].\n")
        
        self.folder_index = self.folder_dir / "index.md"
        self.folder_index.write_text("# Folder Index\nAlso links to [[Root]].\n")
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_cross_folder_backlinks(self):
        """Test backlinks across folders."""
        self.indexer.index_vault()
        
        # Root should have backlinks from Nested and Folder/index
        backlinks_root = self.indexer.get_backlinks(self.root)
        self.assertEqual(len(backlinks_root), 2)
    
    def test_nested_note_backlinks(self):
        """Test backlinks to nested note."""
        self.indexer.index_vault()
        
        backlinks_nested = self.indexer.get_backlinks(self.nested)
        self.assertEqual(len(backlinks_nested), 1)
        self.assertEqual(backlinks_nested[0]['source'], self.root)


class TestDuplicateLinks(unittest.TestCase):
    """Test handling of duplicate links."""
    
    def setUp(self):
        """Create vault with duplicate links."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.indexer = BacklinkIndexer(self.vault_path)
        
        # Same link twice in one file
        self.source = self.vault_path / "Source.md"
        self.source.write_text("# Source\n[[Target]] and [[Target]] again.\n")
        
        self.target = self.vault_path / "Target.md"
        self.target.write_text("# Target\n")
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_duplicate_links_deduplicated(self):
        """Test that duplicate links from same file are deduplicated."""
        self.indexer.index_vault()
        
        backlinks = self.indexer.get_backlinks(self.target)
        
        # Should only have ONE entry from Source (not two)
        from_source = [b for b in backlinks if b['source'] == self.source]
        self.assertEqual(len(from_source), 1)


if __name__ == '__main__':
    unittest.main()
