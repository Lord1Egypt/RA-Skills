#!/usr/bin/env python3
"""
Tests for Obsidian Writer Module

Tests create_note, update_frontmatter, wikilink operations, and move_note.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.writer import VaultWriter, create_note, update_frontmatter


class TestVaultWriterCreateNote(unittest.TestCase):
    """Test VaultWriter.create_note() method."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_create_note_basic(self):
        """Test creating a minimal note."""
        result = self.writer.create_note("Test.md", "Hello world")
        
        self.assertIsInstance(result, Path)
        self.assertTrue(result.exists())
        self.assertEqual(result.read_text(), "Hello world")
    
    def test_create_note_with_frontmatter(self):
        """Test creating a note with frontmatter."""
        frontmatter = {
            'title': 'Test Note',
            'tags': ['test', 'unit'],
            'created': '2024-01-01'
        }
        result = self.writer.create_note("Test.md", "Body content", frontmatter)
        
        content = result.read_text()
        self.assertIn('---', content)
        self.assertIn('title: Test Note', content)
        self.assertIn('tags:', content)
        self.assertIn('Body content', content)
    
    def test_create_note_duplicate_error(self):
        """Test that creating duplicate file raises FileExistsError."""
        self.writer.create_note("Test.md", "First")
        
        with self.assertRaises(FileExistsError):
            self.writer.create_note("Test.md", "Second")
    
    def test_create_note_with_subdirectory(self):
        """Test creating note in subdirectory."""
        result = self.writer.create_note("Notes/Test.md", "Content")
        
        self.assertTrue(result.exists())
        self.assertTrue(result.parent.name, "Notes")
    
    def test_create_note_empty_content(self):
        """Test creating note with empty content."""
        result = self.writer.create_note("Empty.md")
        
        self.assertTrue(result.exists())
        self.assertEqual(result.read_text(), "")
    
    def test_create_note_empty_frontmatter(self):
        """Test that empty dict frontmatter is handled."""
        result = self.writer.create_note("Test.md", "Content", {})
        
        content = result.read_text()
        # Empty dict should produce empty frontmatter
        self.assertIn("---", content)


class TestVaultWriterUpdateFrontmatter(unittest.TestCase):
    """Test VaultWriter.update_frontmatter() method."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_update_frontmatter_merge(self):
        """Test merging frontmatter with existing."""
        # Create note with frontmatter
        self.writer.create_note("Test.md", "Body", {
            'title': 'Original',
            'author': 'Test'
        })
        
        # Update with merge
        self.writer.update_frontmatter("Test.md", {'tags': ['new']}, merge=True)
        
        content = Path(self.vault_dir, "Test.md").read_text()
        self.assertIn('title: Original', content)
        self.assertIn('author: Test', content)
        self.assertIn('tags:', content)
    
    def test_update_frontmatter_replace(self):
        """Test replacing frontmatter entirely."""
        # Create note with frontmatter
        self.writer.create_note("Test.md", "Body", {
            'title': 'Original',
            'author': 'Test'
        })
        
        # Update with replace
        self.writer.update_frontmatter("Test.md", {'new_title': 'Replaced'}, merge=False)
        
        content = Path(self.vault_dir, "Test.md").read_text()
        self.assertNotIn('title: Original', content)
        self.assertIn('new_title: Replaced', content)
    
    def test_update_frontmatter_file_not_found(self):
        """Test updating non-existent file raises error."""
        with self.assertRaises(FileNotFoundError):
            self.writer.update_frontmatter("NotExist.md", {'key': 'value'})


class TestVaultWriterWikilinks(unittest.TestCase):
    """Test wikilink operations."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_add_wikilink(self):
        """Test adding a wikilink to a file."""
        self.writer.create_note("Source.md", "Some content")
        
        self.writer.add_wikilink("Source.md", "Target Note")
        
        content = Path(self.vault_dir, "Source.md").read_text()
        self.assertIn("[[Target Note]]", content)
    
    def test_add_wikilink_with_context(self):
        """Test adding wikilink with context text."""
        self.writer.create_note("Source.md", "Some content")
        
        self.writer.add_wikilink("Source.md", "Target", "See also")
        
        content = Path(self.vault_dir, "Source.md").read_text()
        self.assertIn("See also [[Target]]", content)
    
    def test_add_wikilink_no_duplicate(self):
        """Test that duplicate wikilinks are not added."""
        self.writer.create_note("Source.md", "Some content")
        
        self.writer.add_wikilink("Source.md", "Target")
        self.writer.add_wikilink("Source.md", "Target")  # Second should be ignored
        
        content = Path(self.vault_dir, "Source.md").read_text()
        # Should only appear once
        self.assertEqual(content.count("[[Target]]"), 1)
    
    def test_remove_wikilink(self):
        """Test removing a wikilink from a file."""
        content = "Some text before [[Target Note]] and after"
        self.writer.create_note("Source.md", content)
        
        self.writer.remove_wikilink("Source.md", "Target Note")
        
        result = Path(self.vault_dir, "Source.md").read_text()
        self.assertNotIn("[[Target Note]]", result)
    
    def test_remove_wikilink_with_alias(self):
        """Test removing wikilink with alias."""
        content = "Link to [[Target|Display Text]]"
        self.writer.create_note("Source.md", content)
        
        self.writer.remove_wikilink("Source.md", "Target")
        
        result = Path(self.vault_dir, "Source.md").read_text()
        self.assertNotIn("[[Target", result)
    
    def test_replace_wikilink_single_file(self):
        """Test replacing wikilink in a single file."""
        self.writer.create_note("Source.md", "See [[Old Target]] here")
        
        count = self.writer.replace_wikilink("Old Target", "New Target", scope=Path(self.vault_dir, "Source.md"))
        
        self.assertEqual(count, 1)
        content = Path(self.vault_dir, "Source.md").read_text()
        self.assertIn("[[New Target]]", content)
        self.assertNotIn("[[Old Target]]", content)
    
    def test_replace_wikilink_vault_wide(self):
        """Test replacing wikilink across entire vault."""
        # Create multiple files with the link
        self.writer.create_note("File1.md", "Link to [[Old]] here")
        self.writer.create_note("File2.md", "Another [[Old]] link")
        self.writer.create_note("File3.md", "No links here")
        
        count = self.writer.replace_wikilink("Old", "New")
        
        self.assertEqual(count, 2)
        
        # Verify replacements
        self.assertIn("[[New]]", Path(self.vault_dir, "File1.md").read_text())
        self.assertIn("[[New]]", Path(self.vault_dir, "File2.md").read_text())
        self.assertNotIn("[[Old]]", Path(self.vault_dir, "File1.md").read_text())
    
    def test_replace_wikilink_with_alias_preserved(self):
        """Test that alias is preserved when replacing link."""
        self.writer.create_note("Source.md", "Link [[Old|Display]] text")
        
        self.writer.replace_wikilink("Old", "New")
        
        content = Path(self.vault_dir, "Source.md").read_text()
        self.assertIn("[[New|Display]]", content)


class TestVaultWriterMoveNote(unittest.TestCase):
    """Test move_note operation."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_move_note_basic(self):
        """Test basic file move."""
        # Create source file
        self.writer.create_note("Old.md", "Content here")
        
        # Move it
        self.writer.move_note("Old.md", "New.md")
        
        self.assertFalse(Path(self.vault_dir, "Old.md").exists())
        self.assertTrue(Path(self.vault_dir, "New.md").exists())
        self.assertEqual(Path(self.vault_dir, "New.md").read_text(), "Content here")
    
    def test_move_note_updates_backlinks(self):
        """Test that backlinks are updated after move."""
        # Create note and a file linking to it
        self.writer.create_note("Original.md", "Content")
        self.writer.create_note("Linker.md", "See [[Original]] for details")
        
        # Move the note
        self.writer.move_note("Original.md", "Renamed.md", update_links=True)
        
        # Check the link was updated
        linker_content = Path(self.vault_dir, "Linker.md").read_text()
        self.assertIn("[[Renamed]]", linker_content)
        self.assertNotIn("[[Original]]", linker_content)
    
    def test_move_note_file_not_found(self):
        """Test moving non-existent file raises error."""
        with self.assertRaises(FileNotFoundError):
            self.writer.move_note("NotExist.md", "New.md")
    
    def test_move_note_target_exists(self):
        """Test that move fails if target already exists."""
        self.writer.create_note("Old.md", "Old content")
        self.writer.create_note("New.md", "Existing content")
        
        with self.assertRaises(FileExistsError):
            self.writer.move_note("Old.md", "New.md")


class TestVaultWriterDeleteNote(unittest.TestCase):
    """Test delete_note operation."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_delete_note_with_backup(self):
        """Test that delete moves to .trash."""
        self.writer.create_note("Test.md", "Content")
        
        self.writer.delete_note("Test.md", backup=True)
        
        self.assertFalse(Path(self.vault_dir, "Test.md").exists())
        trash_dir = Path(self.vault_dir, ".trash")
        self.assertTrue(trash_dir.exists())
        # Should have one file in trash
        trash_files = list(trash_dir.glob("*"))
        self.assertEqual(len(trash_files), 1)
    
    def test_delete_note_without_backup(self):
        """Test that delete without backup actually removes file."""
        self.writer.create_note("Test.md", "Content")
        
        self.writer.delete_note("Test.md", backup=False)
        
        self.assertFalse(Path(self.vault_dir, "Test.md").exists())
        self.assertFalse(Path(self.vault_dir, ".trash").exists())


class TestVaultWriterBrokenLinks(unittest.TestCase):
    """Test get_broken_links operation."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
        self.writer = VaultWriter(self.vault_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_get_broken_links(self):
        """Test finding broken links."""
        # Create file with link to non-existent note
        self.writer.create_note("Source.md", "Link to [[NonExistent]] here")
        
        broken = self.writer.get_broken_links()
        
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0]['target'], 'NonExistent')
    
    def test_get_broken_links_none_exist(self):
        """Test that valid links are not reported as broken."""
        self.writer.create_note("Source.md", "Link to [[Existing]] here")
        self.writer.create_note("Existing.md", "I exist!")
        
        broken = self.writer.get_broken_links()
        
        self.assertEqual(len(broken), 0)


class TestStandaloneFunctions(unittest.TestCase):
    """Test standalone create_note and update_frontmatter functions."""
    
    def setUp(self):
        """Create temporary vault directory."""
        self.vault_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.vault_dir, ignore_errors=True)
    
    def test_create_note_function(self):
        """Test standalone create_note function."""
        result = create_note(self.vault_dir, "Test.md", "Content")
        
        self.assertTrue(result.exists())
        self.assertEqual(result.read_text(), "Content")
    
    def test_update_frontmatter_function(self):
        """Test standalone update_frontmatter function."""
        create_note(self.vault_dir, "Test.md", "Body", {'title': 'Original'})
        
        update_frontmatter(self.vault_dir, "Test.md", {'title': 'Updated'})
        
        content = Path(self.vault_dir, "Test.md").read_text()
        self.assertIn('title: Updated', content)


if __name__ == '__main__':
    unittest.main()
