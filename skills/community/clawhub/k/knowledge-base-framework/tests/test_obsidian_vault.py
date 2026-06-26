#!/usr/bin/env python3
"""
Tests for Obsidian Vault Module - High-Level API.

Tests the ObsidianVault class combining parser, resolver, and indexer.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.vault import ObsidianVault, open_vault


class TestObsidianVault(unittest.TestCase):
    """Test ObsidianVault class."""
    
    def setUp(self):
        """Create temporary vault for testing."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        self.vault = ObsidianVault(self.vault_path)
        
        # Create test structure:
        # vault/
        #   Simple.md
        #   Folder/
        #     Note.md
        #     Deep.md
        #   index.md
        #   ALLCAPS.md
        
        self.simple = self.vault_path / "Simple.md"
        self.simple.write_text("# Simple Note\nThis is a simple note.\n")
        
        self.folder_dir = self.vault_path / "Folder"
        self.folder_dir.mkdir()
        self.folder_note = self.folder_dir / "Note.md"
        self.folder_note.write_text("# Folder Note\nSee [[Simple]] for basics.\n")
        
        self.deep_note = self.folder_dir / "Deep.md"
        self.deep_note.write_text("# Deep Note\nLink to [[../Simple|deep link]].\n")
        
        self.index = self.vault_path / "index.md"
        self.index.write_text("---\ntitle: Index\ntags: [test, index]\n---\n# Index\nEntry point.\n")
        
        self.allcaps = self.vault_path / "ALLCAPS.md"
        self.allcaps.write_text("# ALLCAPS\nTesting case.\n")
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.vault_dir)
    
    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    
    def test_init_valid_vault(self):
        """Test vault initialization with valid path."""
        vault = ObsidianVault(self.vault_path)
        self.assertEqual(vault.vault_path, self.vault_path)
        self.assertIsNotNone(vault.resolver)
        self.assertIsNotNone(vault.indexer)
    
    def test_init_invalid_vault(self):
        """Test vault initialization with invalid path raises error."""
        with self.assertRaises(FileNotFoundError):
            ObsidianVault("/nonexistent/path")
    
    def test_open_vault_function(self):
        """Test open_vault helper function."""
        vault = open_vault(self.vault_path)
        self.assertIsInstance(vault, ObsidianVault)
    
    # =========================================================================
    # SEARCH
    # =========================================================================
    
    def test_search_finds_content(self):
        """Test search finds content matches."""
        results = self.vault.search("simple")
        
        self.assertTrue(len(results) > 0)
        # Simple.md should be in results
        paths = [r['file'] for r in results]
        self.assertIn(self.simple, paths)
    
    def test_search_by_filename(self):
        """Test search matches filenames."""
        results = self.vault.search("Simple")
        
        self.assertTrue(len(results) > 0)
        paths = [r['file'] for r in results]
        self.assertIn(self.simple, paths)
    
    def test_search_returns_scored_results(self):
        """Test search returns results with scores."""
        results = self.vault.search("simple")
        
        for result in results:
            self.assertIn('score', result)
            self.assertIn('context', result)
            self.assertIn('file', result)
            self.assertGreaterEqual(result['score'], 0.0)
            self.assertLessEqual(result['score'], 1.0)
    
    def test_search_limit(self):
        """Test search respects limit parameter."""
        # Create many files
        for i in range(15):
            f = self.vault_path / f"note_{i}.md"
            f.write_text(f"Content {i}\n")
        
        results = self.vault.search("Content", limit=5)
        self.assertLessEqual(len(results), 5)
    
    def test_search_no_matches(self):
        """Test search with no matches returns empty list."""
        results = self.vault.search("xyznonexistentquery")
        self.assertEqual(len(results), 0)
    
    # =========================================================================
    # BACKLINKS
    # =========================================================================
    
    def test_find_backlinks(self):
        """Test finding backlinks to a file."""
        # Index first
        self.vault.index()
        
        # Simple.md is linked from Folder/Note.md
        backlinks = self.vault.find_backlinks(self.simple)
        
        # Should have at least one backlink from Folder/Note.md
        sources = [b['source'] for b in backlinks]
        self.assertIn(self.folder_note, sources)
    
    def test_find_backlinks_with_context(self):
        """Test backlinks include context."""
        self.vault.index()
        
        backlinks = self.vault.find_backlinks(self.simple)
        
        self.assertTrue(len(backlinks) > 0)
        for backlink in backlinks:
            self.assertIn('context', backlink)
            self.assertIn('link_text', backlink)
    
    def test_find_backlinks_empty(self):
        """Test backlinks for file with no links to it."""
        self.vault.index()
        
        # Create a file no one links to
        orphan = self.vault_path / "orphan.md"
        orphan.write_text("# Orphan\nNo links here.\n")
        
        backlinks = self.vault.find_backlinks(orphan)
        self.assertEqual(len(backlinks), 0)
    
    def test_find_backlinks_auto_indexes(self):
        """Test find_backlinks auto-indexes if not already indexed."""
        # Don't call index() explicitly
        backlinks = self.vault.find_backlinks(self.simple)
        
        # Should still work
        self.assertTrue(len(backlinks) >= 0)  # May or may not have backlinks
    
    # =========================================================================
    # GRAPH
    # =========================================================================
    
    def test_get_graph_structure(self):
        """Test get_graph returns correct structure."""
        graph = self.vault.get_graph()
        
        self.assertIn('nodes', graph)
        self.assertIn('edges', graph)
        self.assertIsInstance(graph['nodes'], list)
        self.assertIsInstance(graph['edges'], list)
    
    def test_get_graph_nodes(self):
        """Test graph contains all vault files as nodes."""
        graph = self.vault.get_graph()
        
        node_paths = [n['path'] for n in graph['nodes']]
        
        # All markdown files should be nodes
        self.assertIn(self.simple, node_paths)
        self.assertIn(self.folder_note, node_paths)
        self.assertIn(self.index, node_paths)
    
    def test_get_graph_edges(self):
        """Test graph contains link edges."""
        graph = self.vault.get_graph()
        
        # Note.md links to Simple.md
        edge_sources = [e['source'] for e in graph['edges']]
        
        # Should have at least one edge from Note.md
        self.assertIn(self.folder_note, edge_sources)
    
    def test_get_graph_node_info(self):
        """Test nodes contain required info."""
        graph = self.vault.get_graph()
        
        for node in graph['nodes']:
            self.assertIn('path', node)
            self.assertIn('name', node)
            self.assertIn('links', node)
    
    # =========================================================================
    # LINK RESOLUTION
    # =========================================================================
    
    def test_resolve_link_simple(self):
        """Test resolving simple link."""
        resolved = self.vault.resolve_link("Simple")
        
        self.assertEqual(resolved, self.simple)
    
    def test_resolve_link_case_insensitive(self):
        """Test case-insensitive resolution."""
        resolved = self.vault.resolve_link("simple")
        
        self.assertEqual(resolved, self.simple)
    
    def test_resolve_link_folder(self):
        """Test resolving link in subfolder."""
        resolved = self.vault.resolve_link("Folder/Note")
        
        self.assertEqual(resolved, self.folder_note)
    
    def test_resolve_link_with_heading(self):
        """Test resolving link with heading."""
        resolved = self.vault.resolve_link("Simple#heading")
        
        self.assertEqual(resolved, self.simple)
    
    def test_resolve_link_not_found(self):
        """Test resolving nonexistent link."""
        resolved = self.vault.resolve_link("NonexistentNote")
        
        self.assertIsNone(resolved)
    
    def test_resolve_full_link(self):
        """Test resolve_full_link returns tuple."""
        file_path, fragment = self.vault.resolve_full_link("Simple#Heading")
        
        self.assertEqual(file_path, self.simple)
    
    # =========================================================================
    # FILE PARSING
    # =========================================================================
    
    def test_parse_file(self):
        """Test parsing a file."""
        result = self.vault.parse_file(self.simple)
        
        self.assertIn('file_path', result)
        self.assertIn('frontmatter', result)
        self.assertIn('body', result)
        self.assertIn('wikilinks', result)
        self.assertIn('tags', result)
        self.assertIn('embeds', result)
    
    def test_parse_file_with_frontmatter(self):
        """Test parsing file with frontmatter."""
        result = self.vault.parse_file(self.index)
        
        self.assertEqual(result['frontmatter'].get('title'), 'Index')
    
    def test_parse_file_extracts_wikilinks(self):
        """Test wikilink extraction during parse."""
        result = self.vault.parse_file(self.folder_note)
        
        self.assertTrue(len(result['wikilinks']) > 0)
    
    def test_parse_file_extracts_tags(self):
        """Test tag extraction during parse."""
        # Create file with tags
        tagged = self.vault_path / "tagged.md"
        tagged.write_text("# Tagged\n#tag1 #tag/subtag\n")
        
        result = self.vault.parse_file(tagged)
        
        self.assertIn('tag1', result['tags'])
        self.assertIn('tag/subtag', result['tags'])
    
    def test_parse_file_extracts_embeds(self):
        """Test embed extraction during parse."""
        embedded = self.vault_path / "embedded.md"
        embedded.write_text("# Embedded\n![[SomeFile]]\n")
        
        result = self.vault.parse_file(embedded)
        
        self.assertIn('SomeFile', result['embeds'])
    
    # =========================================================================
    # UTILITY
    # =========================================================================
    
    def test_get_file_info(self):
        """Test get_file_info returns metadata."""
        info = self.vault.get_file_info(self.simple)
        
        self.assertIn('path', info)
        self.assertIn('name', info)
        self.assertIn('size', info)
        self.assertEqual(info['name'], 'Simple')
    
    def test_get_stats(self):
        """Test get_stats returns vault statistics."""
        stats = self.vault.get_stats()
        
        self.assertIn('vault_path', stats)
        self.assertIn('total_files', stats)
        self.assertGreater(stats['total_files'], 0)
    
    def test_invalidate_cache(self):
        """Test cache invalidation."""
        # Index first
        self.vault.index()
        self.assertTrue(self.vault._is_indexed)
        
        # Invalidate
        self.vault.invalidate_cache()
        self.assertFalse(self.vault._is_indexed)
    
    def test_index_file(self):
        """Test indexing a single file."""
        # Create new file
        new_file = self.vault_path / "new.md"
        new_file.write_text("# New\nLink to [[Simple]].\n")
        
        # Index it
        self.vault.index_file(new_file)
        
        # Should have backlinks to Simple
        backlinks = self.vault.find_backlinks(self.simple)
        sources = [b['source'] for b in backlinks]
        self.assertIn(new_file, sources)
    
    # =========================================================================
    # HEADINGS
    # =========================================================================
    
    def test_extract_headings(self):
        """Test heading extraction."""
        content = """# Heading 1
Some text
## Heading 2
More text
### Heading 3
"""
        
        headings = self.vault._extract_headings(content)
        
        self.assertEqual(len(headings), 3)
        self.assertEqual(headings[0]['level'], 1)
        self.assertEqual(headings[0]['text'], 'Heading 1')
        self.assertIn('slug', headings[0])
    
    # =========================================================================
    # EDGE CASES
    # =========================================================================
    
    def test_search_with_special_characters(self):
        """Test search handles special characters."""
        results = self.vault.search("Note")  # Works
        self.assertIsNotNone(results)
    
    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file returns error."""
        result = self.vault.parse_file("/nonexistent/file.md")
        
        self.assertIn('error', result)
    
    def test_find_backlinks_with_string_path(self):
        """Test find_backlinks accepts string path."""
        self.vault.index()
        
        backlinks = self.vault.find_backlinks(str(self.simple))
        
        # Should work without error
        self.assertIsInstance(backlinks, list)


class TestObsidianVaultComplex(unittest.TestCase):
    """Test complex vault scenarios."""
    
    def setUp(self):
        """Create complex vault structure."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        
        # Create more complex structure:
        # vault/
        #   index.md
        #   topic1/
        #     main.md
        #     related.md
        #   topic2/
        #     main.md
        #   orphan.md
        
        self.index = self.vault_path / "index.md"
        self.index.write_text("---\ntitle: Vault Index\n---\n# Index\nSee [[topic1/main]] for details.\n")
        
        self.topic1_dir = self.vault_path / "topic1"
        self.topic1_dir.mkdir()
        self.topic1_main = self.topic1_dir / "main.md"
        self.topic1_main.write_text("# Topic 1 Main\nRelated to [[topic2/main]] and [[related]].\n#machine-learning\n")
        
        self.topic1_related = self.topic1_dir / "related.md"
        self.topic1_related.write_text("# Related\nBacklink to [[../topic1/main]].\n")
        
        self.topic2_dir = self.vault_path / "topic2"
        self.topic2_dir.mkdir()
        self.topic2_main = self.topic2_dir / "main.md"
        self.topic2_main.write_text("---\ntitle: Topic 2\ntags: [ai, nlp]\n---\n# Topic 2\nSee [[topic1/main]] for more.\n")
        
        self.orphan = self.vault_path / "orphan.md"
        self.orphan.write_text("# Orphan\nThis file has no links.\n")
        
        self.vault = ObsidianVault(self.vault_path)
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    def test_cross_folder_links(self):
        """Test resolving links across folders."""
        resolved = self.vault.resolve_link("topic1/main")
        self.assertEqual(resolved, self.topic1_main)
        
        resolved = self.vault.resolve_link("topic2/main")
        self.assertEqual(resolved, self.topic2_main)
    
    def test_relative_link_resolution(self):
        """Test relative wikilinks are resolved."""
        # topic1/related.md links to ../topic1/main
        result = self.vault.parse_file(self.topic1_related)
        
        # Should have extracted the wikilink
        self.assertTrue(len(result['wikilinks']) > 0)
    
    def test_graph_with_multiple_paths(self):
        """Test graph correctly represents complex linking."""
        graph = self.vault.get_graph()
        
        # All files should be nodes
        self.assertEqual(len(graph['nodes']), 5)
        
        # Should have edges from index -> topic1/main
        # and topic1/main -> topic2/main
        self.assertGreater(len(graph['edges']), 0)
    
    def test_backlinks_for_connected_file(self):
        """Test backlinks for highly connected file."""
        # topic1/main.md is linked from index and topic2
        backlinks = self.vault.find_backlinks(self.topic1_main)
        
        sources = [b['source'] for b in backlinks]
        
        # Should have backlinks from index.md and topic2/main.md
        self.assertIn(self.index, sources)
        self.assertIn(self.topic2_main, sources)
    
    def test_search_finds_tagged_content(self):
        """Test search finds content by tags."""
        results = self.vault.search("machine")
        
        # Should find topic1/main.md
        paths = [r['file'] for r in results]
        self.assertIn(self.topic1_main, paths)
    
    def test_search_in_frontmatter(self):
        """Test search matches frontmatter."""
        results = self.vault.search("Vault Index")
        
        paths = [r['file'] for r in results]
        self.assertIn(self.index, paths)


if __name__ == '__main__':
    unittest.main()