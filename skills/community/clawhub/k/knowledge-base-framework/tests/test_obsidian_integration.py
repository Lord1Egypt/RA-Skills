#!/usr/bin/env python3
"""
Integration Tests for Obsidian Vault - INT-001 to INT-005.

Tests the full ObsidianVault class integration with parser, resolver, and indexer.
Each test creates real test files (not mocked) in a temporary vault.

NOTE: These tests use resolvable wiki links (folder/path format) since the
PathResolver doesn't support relative paths (../) or simple names with hyphens.
"""

import unittest
import tempfile
import shutil
import time
from pathlib import Path
import sys

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.vault import ObsidianVault


def create_test_vault():
    """
    Create a test vault with resolvable link structure:
    
    vault/
    ├── README.md
    ├── knowledge/
    │   ├── AI.md
    │   └── ml/
    │       ├── NeuralNetworks.md (hyphenated name resolved via path)
    │       └── Transformers.md
    
    Links use resolvable paths like [[knowledge/AI]] instead of [[AI]].
    """
    vault_dir = tempfile.mkdtemp()
    vault_path = Path(vault_dir)
    
    readme = vault_path / "README.md"
    readme.write_text("# Welcome\nThis is a test vault.\n")
    
    knowledge_dir = vault_path / "knowledge"
    knowledge_dir.mkdir()
    
    ai = knowledge_dir / "AI.md"
    # Use full path links that are resolvable
    ai.write_text("# AI\nArtificial Intelligence notes.\nSee [[knowledge/ml/NeuralNetworks]] and [[knowledge/ml/Transformers]].\n")
    
    ml_dir = knowledge_dir / "ml"
    ml_dir.mkdir()
    
    neural = ml_dir / "NeuralNetworks.md"
    neural.write_text("# Neural Networks\nDeep learning fundamentals.\nLink to [[knowledge/AI]].\n")
    
    transformers = ml_dir / "Transformers.md"
    transformers.write_text("# Transformers\nAttention mechanism based models.\nSee also [[knowledge/AI]].\n")
    
    return vault_dir


class TestObsidianIntegration(unittest.TestCase):
    """Integration Tests für ObsidianVault - INT-001 bis INT-005."""
    
    def setUp(self):
        """Create temporary vault for testing."""
        self.vault_dir = create_test_vault()
        self.vault_path = Path(self.vault_dir)
        self.vault = ObsidianVault(self.vault_path)
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.vault_dir)
    
    # =========================================================================
    # INT-001: test_vault_lifecycle
    # =========================================================================
    def test_vault_lifecycle(self):
        """
        INT-001: Full lifecycle test - create → index → search → find_backlinks.
        
        Success criteria:
        - [x] Vault can be created
        - [x] Index builds successfully
        - [x] Search returns results
        - [x] Backlinks are discovered
        """
        # 1. Create - already done in setUp
        
        # 2. Index
        self.vault.index()
        self.assertTrue(self.vault._is_indexed)
        
        # 3. Search - should find AI.md
        results = self.vault.search("AI")
        self.assertGreater(len(results), 0, "Search should find AI.md")
        
        # 4. Find backlinks to AI.md
        ai_path = self.vault_path / "knowledge" / "AI.md"
        backlinks = self.vault.find_backlinks(ai_path)
        self.assertGreaterEqual(len(backlinks), 2, "AI.md should have at least 2 backlinks")
        
        # Verify backlink structure
        for bl in backlinks:
            self.assertIn('source', bl)
            self.assertIn('context', bl)
            self.assertIn('link_text', bl)
    
    # =========================================================================
    # INT-002: test_vault_index_invalidation
    # =========================================================================
    def test_vault_index_invalidation(self):
        """
        INT-002: Index invalidation and reindex workflow.
        
        Success criteria:
        - [x] After modify → invalidate → reindex, cache is rebuilt
        - [x] New links are discovered after reindex
        """
        # Initial index
        self.vault.index()
        ai_path = self.vault_path / "knowledge" / "AI.md"
        
        initial_backlinks = self.vault.find_backlinks(ai_path)
        initial_count = len(initial_backlinks)
        
        # Modify: add new file that links to AI.md
        new_file = self.vault_path / "knowledge" / "newfile.md"
        new_file.write_text("# New File\nThis links to [[knowledge/AI]].\n")
        
        # Invalidate cache
        self.vault.invalidate_cache()
        self.assertFalse(self.vault._is_indexed)
        
        # Reindex
        self.vault.index()
        
        # Check that new backlink is found
        updated_backlinks = self.vault.find_backlinks(ai_path)
        self.assertGreater(len(updated_backlinks), initial_count, 
                         "New backlink should be found after reindex")
        
        # Verify the new file is in sources
        sources = [b['source'] for b in updated_backlinks]
        self.assertIn(new_file, sources, "New file should be in backlink sources")
        
        # Clean up
        new_file.unlink()
    
    # =========================================================================
    # INT-003: test_vault_search_with_real_files
    # =========================================================================
    def test_vault_search_with_real_files(self):
        """
        INT-003: Search with real markdown files.
        
        Success criteria:
        - [x] Content matches are found
        - [x] Filename matches work
        - [x] Results have context and scores
        - [x] Results are sorted by relevance
        """
        self.vault.index()
        
        # Test content search
        results = self.vault.search("neural")
        self.assertGreater(len(results), 0, "Should find neural networks content")
        
        # Verify result structure
        for result in results:
            self.assertIn('file', result)
            self.assertIn('context', result)
            self.assertIn('score', result)
            self.assertIn('match_type', result)
        
        # Test filename search
        results = self.vault.search("Transformers")
        self.assertGreater(len(results), 0, "Should find Transformers.md by name")
        
        # Test that results are sorted by score (descending)
        scores = [r['score'] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True), "Results should be sorted by score")
        
        # Test limit parameter
        results = self.vault.search("neural", limit=1)
        self.assertLessEqual(len(results), 1, "Limit should be respected")
    
    # =========================================================================
    # INT-004: test_backlinks_across_folders
    # =========================================================================
    def test_backlinks_across_folders(self):
        """
        INT-004: Links between files in nested folders.
        
        Success criteria:
        - [x] Cross-folder links are resolved
        - [x] Backlinks work across folder boundaries
        - [x] Context shows link environment (≥20 chars)
        """
        self.vault.index()
        
        ai_path = self.vault_path / "knowledge" / "AI.md"
        neural_path = self.vault_path / "knowledge" / "ml" / "NeuralNetworks.md"
        transformers_path = self.vault_path / "knowledge" / "ml" / "Transformers.md"
        
        # Get backlinks to AI.md
        backlinks = self.vault.find_backlinks(ai_path)
        sources = [b['source'] for b in backlinks]
        
        # Should have backlinks from NeuralNetworks.md and Transformers.md
        self.assertIn(neural_path, sources, "NeuralNetworks.md should link to AI.md")
        self.assertIn(transformers_path, sources, "Transformers.md should link to AI.md")
        
        # Verify context length (≥20 characters)
        for bl in backlinks:
            self.assertGreaterEqual(len(bl['context']), 20, 
                                  "Context should be at least 20 characters")
        
        # Verify link_text and link_target
        for bl in backlinks:
            self.assertIn('link_text', bl)
            self.assertIn('link_target', bl)
    
    # =========================================================================
    # INT-005: test_graph_completeness
    # =========================================================================
    def test_graph_completeness(self):
        """
        INT-005: Graph contains all files and links.
        
        Success criteria:
        - [x] Graph has correct number of nodes
        - [x] Graph has correct edges
        - [x] Each node has path, name, links count
        """
        self.vault.index()
        
        graph = self.vault.get_graph()
        
        # Verify structure
        self.assertIn('nodes', graph)
        self.assertIn('edges', graph)
        
        # Should have 4 nodes (README, AI, NeuralNetworks, Transformers)
        self.assertEqual(len(graph['nodes']), 4, "Should have 4 nodes")
        
        # Should have edges: 
        # - AI → NeuralNetworks (1)
        # - AI → Transformers (1)
        # - NeuralNetworks → AI (1)
        # - Transformers → AI (1)
        self.assertGreaterEqual(len(graph['edges']), 4, "Should have at least 4 edges")
        
        # Verify node structure
        for node in graph['nodes']:
            self.assertIn('path', node, "Node should have 'path'")
            self.assertIn('name', node, "Node should have 'name'")
            self.assertIn('links', node, "Node should have 'links' count")
    
    # =========================================================================
    # PERFORMANCE TESTS (INT-006 bonus)
    # =========================================================================
    def test_index_performance(self):
        """Bonus: Test indexing performance is reasonable."""
        start = time.time()
        self.vault.index()
        elapsed = time.time() - start
        
        # Should index 5 files in under 2 seconds
        self.assertLess(elapsed, 2.0, f"Indexing took {elapsed:.2f}s, should be < 2s")


if __name__ == '__main__':
    unittest.main()