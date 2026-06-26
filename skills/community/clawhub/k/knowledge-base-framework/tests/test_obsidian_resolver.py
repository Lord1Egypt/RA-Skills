#!/usr/bin/env python3
"""
Tests for Obsidian Path Resolver Module

Tests wiki link resolution using shortest-match algorithm.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.resolver import (
    PathResolver,
    resolve_wikilink,
)


class TestPathResolver(unittest.TestCase):
    """Test PathResolver class."""
    
    def setUp(self):
        """Create temporary vault for testing."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.resolver = PathResolver(self.vault_path)
        
        # Create test structure:
        # vault/
        #   Simple.md
        #   Folder/
        #     Note.md
        #     SubFolder/
        #       Deep.md
        #   index.md
        #   ALLCAPS.md
        
        self.simple = self.vault_path / "Simple.md"
        self.simple.write_text("# Simple Note\n")
        
        self.folder_dir = self.vault_path / "Folder"
        self.folder_dir.mkdir()
        self.folder_note = self.folder_dir / "Note.md"
        self.folder_note.write_text("# Folder Note\n")
        
        self.subfolder_dir = self.folder_dir / "SubFolder"
        self.subfolder_dir.mkdir()
        self.deep_note = self.subfolder_dir / "Deep.md"
        self.deep_note.write_text("# Deep Note\n")
        
        self.index = self.vault_path / "index.md"
        self.index.write_text("# Index\n")
        
        self.allcaps = self.vault_path / "ALLCAPS.md"
        self.allcaps.write_text("# All Caps\n")
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.vault_dir)
    
    # =========================================================================
    # Basic Resolution Tests
    # =========================================================================
    
    def test_resolve_simple_note(self):
        """Test resolving [[Simple]] to Simple.md."""
        result = self.resolver.resolve_link("Simple")
        self.assertEqual(result, self.simple)
    
    def test_resolve_nonexistent_note(self):
        """Test resolving non-existent note returns None."""
        result = self.resolver.resolve_link("NonExistent")
        self.assertIsNone(result)
    
    def test_resolve_with_folder_path(self):
        """Test resolving [[Folder/Note]]."""
        result = self.resolver.resolve_link("Folder/Note")
        self.assertEqual(result, self.folder_note)
    
    def test_resolve_deep_nested(self):
        """Test resolving [[Folder/SubFolder/Deep]]."""
        result = self.resolver.resolve_link("Folder/SubFolder/Deep")
        self.assertEqual(result, self.deep_note)
    
    # =========================================================================
    # Case-Insensitive Tests
    # =========================================================================
    
    def test_resolve_case_insensitive(self):
        """Test case-insensitive matching."""
        result = self.resolver.resolve_link("simple")
        self.assertEqual(result, self.simple)
        
        result = self.resolver.resolve_link("SIMPLE")
        self.assertEqual(result, self.simple)
        
        result = self.resolver.resolve_link("SiMpLe")
        self.assertEqual(result, self.simple)
    
    def test_resolve_allcaps(self):
        """Test resolving ALLCAPS.md."""
        result = self.resolver.resolve_link("ALLCAPS")
        self.assertEqual(result, self.allcaps)
        
        result = self.resolver.resolve_link("allcaps")
        self.assertEqual(result, self.allcaps)
    
    # =========================================================================
    # Shortest Match Tests
    # =========================================================================
    
    def test_shortest_match_simple(self):
        """Test that simple notes resolve to direct .md files."""
        # Create duplicate in subfolder
        dup_dir = self.vault_path / "Dup"
        dup_dir.mkdir()
        dup_file = dup_dir / "Simple.md"
        dup_file.write_text("# Duplicate Simple\n")
        
        # Should return shortest (root Simple.md)
        result = self.resolver.resolve_link("Simple")
        self.assertEqual(result, self.simple)
        
        # Direct path should still work
        result = self.resolver.resolve_link("Dup/Simple")
        self.assertEqual(result, dup_file)
    
    # =========================================================================
    # Heading Resolution Tests
    # =========================================================================
    
    def test_resolve_heading_found(self):
        """Test finding heading in file."""
        # Write content with heading
        self.simple.write_text("# Main Heading\n\nSome content\n\n## Sub Heading\n")
        
        result = self.resolver.resolve_heading(self.simple, "Main Heading")
        self.assertIsNotNone(result)
        self.assertEqual(result, "main-heading")
    
    def test_resolve_heading_case_insensitive(self):
        """Test heading search is case-insensitive."""
        self.simple.write_text("# Main Heading\n")
        
        result = self.resolver.resolve_heading(self.simple, "main heading")
        self.assertIsNotNone(result)
    
    def test_resolve_heading_not_found(self):
        """Test heading not found returns None."""
        result = self.resolver.resolve_heading(self.simple, "NonExistent")
        self.assertIsNone(result)
    
    # =========================================================================
    # Embed Resolution Tests
    # =========================================================================
    
    def test_resolve_embed_simple(self):
        """Test resolving ![[embed]]."""
        # Create a non-markdown file
        img_path = self.vault_path / "image.png"
        img_path.write_text("fake image data")
        
        result = self.resolver.resolve_embed("image.png")
        self.assertEqual(result, img_path)
    
    def test_resolve_embed_in_folder(self):
        """Test resolving ![[folder/file]]."""
        sub_dir = self.vault_path / "assets"
        sub_dir.mkdir()
        img_path = sub_dir / "photo.jpg"
        img_path.write_text("fake jpg data")
        
        result = self.resolver.resolve_embed("assets/photo.jpg")
        self.assertEqual(result, img_path)
    
    # =========================================================================
    # Wiki Link with Alias/Heading Tests
    # =========================================================================
    
    def test_resolve_link_with_heading(self):
        """Test resolving [[Note#Heading]]."""
        result = self.resolver.resolve_link("Simple#Main")
        self.assertEqual(result, self.simple)
    
    def test_resolve_link_with_alias(self):
        """Test resolving [[Note|Alias]]."""
        result = self.resolver.resolve_link("Simple|Display Text")
        self.assertEqual(result, self.simple)
    
    def test_resolve_link_with_heading_and_alias(self):
        """Test resolving [[Note#Heading|Alias]]."""
        result = self.resolver.resolve_link("Folder/Note#Sub|Alias")
        self.assertEqual(result, self.folder_note)
    
    # =========================================================================
    # Full Link Resolution Tests
    # =========================================================================
    
    def test_resolve_full_link(self):
        """Test resolve_full_link returns (path, heading_fragment)."""
        # Create note with heading
        self.simple.write_text("# Main Heading\n")
        
        path, fragment = self.resolver.resolve_full_link("Simple#Main Heading")
        self.assertEqual(path, self.simple)
        self.assertIsNotNone(fragment)
    
    def test_resolve_full_link_no_heading(self):
        """Test resolve_full_link without heading."""
        path, fragment = self.resolver.resolve_full_link("Simple")
        self.assertEqual(path, self.simple)
        self.assertIsNone(fragment)
    
    # =========================================================================
    # Cache Tests
    # =========================================================================
    
    def test_invalidate_cache(self):
        """Test cache invalidation."""
        # First call builds index
        self.resolver.resolve_link("Simple")
        
        # Add new file
        new_file = self.vault_path / "New.md"
        new_file.write_text("# New\n")
        
        # Without invalidate, new file won't be found
        self.resolver.invalidate_cache()
        result = self.resolver.resolve_link("New")
        self.assertEqual(result, new_file)
    
    # =========================================================================
    # Slugify Tests
    # =========================================================================
    
    def test_slugify_basic(self):
        """Test basic slugification."""
        slug = self.resolver._slugify("Main Heading")
        self.assertEqual(slug, "main-heading")
    
    def test_slugify_special_chars(self):
        """Test slugify removes special characters."""
        slug = self.resolver._slugify("Hello! World?")
        self.assertEqual(slug, "hello-world")
    
    def test_slugify_multiple_dashes(self):
        """Test slugify collapses multiple dashes."""
        slug = self.resolver._slugify("One   Two")
        self.assertEqual(slug, "one-two")


class TestStandaloneResolve(unittest.TestCase):
    """Test standalone resolve_wikilink function."""
    
    def setUp(self):
        """Create temporary vault."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        
        # Create test file
        note = self.vault_path / "Test.md"
        note.write_text("# Test\n")
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_resolve_wikilink_standalone(self):
        """Test standalone function."""
        result = resolve_wikilink("Test", self.vault_path)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test.md")


class TestIndexMDResolution(unittest.TestCase):
    """Test special index.md resolution."""
    
    def setUp(self):
        """Create temporary vault with index.md."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.resolver = PathResolver(self.vault_path)
        
        # Create index.md directly in vault
        self.index = self.vault_path / "index.md"
        self.index.write_text("# Index Note\n")
        
        # Create folder/index.md
        self.folder_dir = self.vault_path / "MyFolder"
        self.folder_dir.mkdir()
        self.folder_index = self.folder_dir / "index.md"
        self.folder_index.write_text("# My Folder Index\n")
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_resolve_folder_to_index(self):
        """Test that [[folder]] resolves to folder/index.md."""
        result = self.resolver.resolve_link("MyFolder")
        # Should match MyFolder/index.md
        self.assertIsNotNone(result)
    
    def test_resolve_root_index(self):
        """Test resolving root index."""
        result = self.resolver.resolve_link("index")
        self.assertEqual(result, self.index)


if __name__ == '__main__':
    unittest.main()
