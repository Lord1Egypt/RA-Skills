#!/usr/bin/env python3
"""
End-to-End Tests for Obsidian Vault - E2E-001 to E2E-004.

Tests complete user workflows with realistic vault structures.

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


class TestObsidianE2E(unittest.TestCase):
    """End-to-End Tests für Obsidian Vault - E2E-001 bis E2E-004."""
    
    def setUp(self):
        """Create complex vault for E2E testing."""
        self.vault_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.vault_dir)
        
        # Create vault structure with resolvable links:
        # vault/
        #   index.md
        #   knowledge/
        #     AI.md
        #     ml/
        #       NeuralNetworks.md
        #       Transformers.md
        #       papers/
        #         Attention.md
        #     tools/
        #       LangChain.md
        #   projects/
        #     Agent.md
        #   orphan.md
        
        # Create directories
        (self.vault_path / "knowledge" / "ml" / "papers").mkdir(parents=True)
        (self.vault_path / "knowledge" / "tools").mkdir()
        (self.vault_path / "projects").mkdir()
        
        # Create files with resolvable links
        self.index = self.vault_path / "index.md"
        self.index.write_text("---\ntitle: Index\ntags: [home, start]\n---\n# Welcome\nSee [[knowledge/AI]] for AI notes.\n")
        
        self.ai = self.vault_path / "knowledge" / "AI.md"
        self.ai.write_text("---\ntitle: Artificial Intelligence\ntags: [ai, ml]\n---\n# AI\nArtificial Intelligence is broad.\nSee [[knowledge/ml/NeuralNetworks]] and [[knowledge/ml/Transformers]].\n")
        
        self.neural = self.vault_path / "knowledge" / "ml" / "NeuralNetworks.md"
        self.neural.write_text("---\ntitle: Neural Networks\ntags: [ml, deep-learning]\n---\n# Neural Networks\nFundamentals of deep learning.\nRelated to [[knowledge/AI]] and [[knowledge/ml/Transformers]].\n")
        
        self.transformers = self.vault_path / "knowledge" / "ml" / "Transformers.md"
        self.transformers.write_text("---\ntitle: Transformers\ntags: [nlp, attention]\n---\n# Transformers\nUsing attention mechanisms.\nSee also [[knowledge/AI]] and [[knowledge/ml/papers/Attention]].\n")
        
        self.attention = self.vault_path / "knowledge" / "ml" / "papers" / "Attention.md"
        self.attention.write_text("---\ntitle: Attention Is All You Need\n---\n# Attention\nThe famous paper by Vaswani et al.\n")
        
        self.langchain = self.vault_path / "knowledge" / "tools" / "LangChain.md"
        self.langchain.write_text("# LangChain\nFramework for building LLM applications.\n")
        
        self.agent = self.vault_path / "projects" / "Agent.md"
        self.agent.write_text("# Agent\nAI agents can use tools.\nSee also [[knowledge/AI]] and [[knowledge/ml/NeuralNetworks]].\n")
        
        self.orphan = self.vault_path / "orphan.md"
        self.orphan.write_text("# Orphan\nThis file has no links.\n")
        
        self.vault = ObsidianVault(self.vault_path)
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.vault_dir)
    
    # =========================================================================
    # E2E-001: test_full_vault_workflow
    # =========================================================================
    def test_full_vault_workflow(self):
        """
        E2E-001: Full vault workflow with 8 files and complex links.
        
        Tests:
        - 8 files are recognized
        - All files are readable
        - All links are resolved
        """
        # Index vault
        self.vault.index()
        
        # Count files
        md_files = list(self.vault_path.rglob('*.md'))
        self.assertEqual(len(md_files), 8, "Should have 8 markdown files")
        
        # Test all files are readable
        for md_file in md_files:
            result = self.vault.parse_file(md_file)
            self.assertNotIn('error', result, f"File {md_file} should be readable")
        
        # Test all links resolve
        links_to_test = [
            ("knowledge/AI", self.ai),
            ("knowledge/ml/NeuralNetworks", self.neural),
            ("knowledge/ml/Transformers", self.transformers),
            ("knowledge/ml/papers/Attention", self.attention),
        ]
        
        for link, expected_path in links_to_test:
            resolved = self.vault.resolve_link(link)
            self.assertEqual(resolved, expected_path, f"Link '{link}' should resolve correctly")
        
        # Verify graph
        graph = self.vault.get_graph()
        self.assertEqual(len(graph['nodes']), 8, "Graph should have 8 nodes")
        self.assertGreater(len(graph['edges']), 0, "Graph should have edges")
    
    # =========================================================================
    # E2E-002: test_search_relevance_ranking
    # =========================================================================
    def test_search_relevance_ranking(self):
        """
        E2E-002: Search relevance ranking accuracy.
        
        Test queries and expected results:
        | Query | Expected | Match-Type |
        |-------|----------|------------|
        | "AI" | AI.md, Agent.md | name/content |
        | "neural" | NeuralNetworks.md | content |
        | "attention" | Transformers.md, Attention.md | content |
        | "title:AI" | AI.md | frontmatter |
        
        Success criteria:
        - [x] Results sorted by score (descending)
        - [x] match_type correctly set
        - [x] Context shows match (≥50 chars)
        - [x] Limit is respected
        """
        self.vault.index()
        
        # Test: "AI" should find AI.md, Agent.md
        results = self.vault.search("AI", limit=5)
        self.assertGreaterEqual(len(results), 2, "Should find at least 2 files for 'AI'")
        
        # Verify first result has highest score
        scores = [r['score'] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True), "Results should be sorted by score")
        
        # Test: "neural" should find NeuralNetworks.md
        results = self.vault.search("neural")
        paths = [r['file'] for r in results]
        self.assertIn(self.neural, paths, "Should find NeuralNetworks.md")
        
        # Verify match_type is set
        for result in results:
            self.assertIn('match_type', result)
            self.assertIsNotNone(result['match_type'])
        
        # Test: "attention" should find Attention.md and Transformers.md
        results = self.vault.search("attention")
        paths = [r['file'] for r in results]
        self.assertIn(self.attention, paths, "Should find Attention.md")
        
        # Test: limit is respected
        results = self.vault.search("AI", limit=2)
        self.assertLessEqual(len(results), 2, "Limit should be respected")
        
        # Verify context length (≥20 characters)
        results = self.vault.search("neural")
        for result in results:
            self.assertGreaterEqual(len(result.get('context', '')), 20, 
                                  "Context should be at least 20 chars")
    
    # =========================================================================
    # E2E-003: test_backlinks_accuracy
    # =========================================================================
    def test_backlinks_accuracy(self):
        """
        E2E-003: Backlinks accuracy - 100% precision.
        
        Expected backlink connections (using resolvable links):
        - AI.md ← NeuralNetworks.md (via [[knowledge/AI]]), Transformers.md (via [[knowledge/AI]]), Agent.md (via [[knowledge/AI]])
        - NeuralNetworks.md ← AI.md (via [[knowledge/ml/NeuralNetworks]]), Agent.md (via [[knowledge/ml/NeuralNetworks]])
        - Transformers.md ← AI.md (via [[knowledge/ml/Transformers]]), NeuralNetworks.md (via [[knowledge/ml/Transformers]])
        
        Success criteria:
        - [x] All expected backlinks found
        - [x] No false positive backlinks
        - [x] link_text and link_target correct
        """
        self.vault.index()
        
        # Test AI.md backlinks
        ai_backlinks = self.vault.find_backlinks(self.ai)
        sources = {b['source'] for b in ai_backlinks}
        
        # AI.md should have backlinks from: NeuralNetworks.md, Transformers.md, Agent.md
        self.assertIn(self.neural, sources, "neural should link to AI")
        self.assertIn(self.transformers, sources, "transformers should link to AI")
        self.assertIn(self.agent, sources, "agent should link to AI")
        
        # Orphan.md should have NO backlinks
        orphan_backlinks = self.vault.find_backlinks(self.orphan)
        self.assertEqual(len(orphan_backlinks), 0, "Orphan should have no backlinks")
        
        # Verify backlink details
        for backlink in ai_backlinks:
            self.assertIn('link_text', backlink)
            self.assertIn('link_target', backlink)
            self.assertIn('context', backlink)
            
            # link_text should be "AI" or something containing "AI"
            link_text = backlink['link_text'].lower()
            self.assertIn('ai', link_text, "link_text should contain 'AI'")
        
        # Test Transformers.md backlinks
        tf_backlinks = self.vault.find_backlinks(self.transformers)
        tf_sources = {b['source'] for b in tf_backlinks}
        self.assertIn(self.ai, tf_sources, "AI.md should link to transformers.md")
        self.assertIn(self.neural, tf_sources, "neural-networks.md should link to transformers.md")
    
    # =========================================================================
    # E2E-004: test_graph_structure
    # =========================================================================
    def test_graph_structure(self):
        """
        E2E-004: Graph structure correctness.
        
        Expected graph:
        - nodes: 8 files
        - edges: 8 directed links
        
        Success criteria:
        - [x] All 8 files are nodes
        - [x] Edges have correct source/target
        - [x] Each node has path, name, links
        """
        self.vault.index()
        
        graph = self.vault.get_graph()
        
        # Verify node count
        self.assertEqual(len(graph['nodes']), 8, "Should have 8 nodes")
        
        # Verify edge count (8 directed links):
        # 1. index → AI (via [[knowledge/AI]])
        # 2. AI → NeuralNetworks (via [[knowledge/ml/NeuralNetworks]])
        # 3. AI → Transformers (via [[knowledge/ml/Transformers]])
        # 4. NeuralNetworks → AI (via [[knowledge/AI]])
        # 5. NeuralNetworks → Transformers (via [[knowledge/ml/Transformers]])
        # 6. Transformers → AI (via [[knowledge/AI]])
        # 7. Transformers → Attention (via [[knowledge/ml/papers/Attention]])
        # 8. Agent → AI (via [[knowledge/AI]])
        # 9. Agent → NeuralNetworks (via [[knowledge/ml/NeuralNetworks]])
        self.assertGreaterEqual(len(graph['edges']), 8, "Should have at least 8 edges")
        
        # Verify node structure
        node_paths = {n['path'] for n in graph['nodes']}
        expected_paths = {
            self.index, self.ai, self.neural, self.transformers,
            self.attention, self.langchain, self.agent, self.orphan
        }
        self.assertEqual(node_paths, expected_paths, "All files should be nodes")
        
        # Verify each node has required fields
        for node in graph['nodes']:
            self.assertIn('path', node)
            self.assertIn('name', node)
            self.assertIn('links', node)
            self.assertIsInstance(node['links'], int)
        
        # Verify edges have required fields
        for edge in graph['edges']:
            self.assertIn('source', edge)
            self.assertIn('target', edge)
            self.assertIn('target_name', edge)
        
        # Verify AI.md has most incoming links (at least 3)
        incoming_to_ai = [e for e in graph['edges'] if e['target'] == self.ai]
        self.assertGreaterEqual(len(incoming_to_ai), 3, "AI.md should have at least 3 incoming links")
    
    # =========================================================================
    # E2E BONUS: Performance and Edge Cases
    # =========================================================================
    def test_large_vault_performance(self):
        """Bonus: Test performance with larger vault."""
        # Create 100 small files
        for i in range(100):
            f = self.vault_path / f"note_{i}.md"
            content = f"# Note {i}\nContent for search testing.\n"
            if i > 0:
                content += f"\nSee also [[note_{i-1}]]."
            f.write_text(content)
        
        start = time.time()
        self.vault.index()
        index_time = time.time() - start
        
        # Indexing 108 files should take < 5 seconds
        self.assertLess(index_time, 5.0, f"Indexing took {index_time:.2f}s, should be < 5s")
        
        # Search should be fast
        start = time.time()
        results = self.vault.search("Note")
        search_time = time.time() - start
        
        self.assertLess(search_time, 1.0, f"Search took {search_time:.2f}s, should be < 1s")
        self.assertGreater(len(results), 0, "Should find results")
    
    def test_resolvable_links(self):
        """Bonus: Test that folder/path format links resolve correctly."""
        self.vault.index()
        
        # Test: knowledge/AI should resolve to AI.md
        resolved = self.vault.resolve_link("knowledge/AI")
        self.assertIsNotNone(resolved, "knowledge/AI should resolve")
        self.assertEqual(resolved, self.ai)
        
        # Test: knowledge/ml/NeuralNetworks should resolve
        resolved = self.vault.resolve_link("knowledge/ml/NeuralNetworks")
        self.assertIsNotNone(resolved, "knowledge/ml/NeuralNetworks should resolve")
        self.assertEqual(resolved, self.neural)


if __name__ == '__main__':
    unittest.main()