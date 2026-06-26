"""Tests for the chunker module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from engram.chunker import pre_filter, chunk_text, merge_extractions, ChunkConfig


class TestPreFilter:
    def test_strips_heartbeats(self):
        text = """## Morning
- Did important work
- HEARTBEAT_OK
- More important work
- No alert needed
"""
        result = pre_filter(text)
        assert "important work" in result
        assert "HEARTBEAT_OK" not in result
        assert "No alert needed" not in result
    
    def test_strips_long_code_blocks(self):
        text = "## Code\n```python\n" + "\n".join(f"line {i}" for i in range(20)) + "\n```\n## After"
        result = pre_filter(text)
        assert "omitted" in result
        assert "## After" in result
    
    def test_keeps_short_code_blocks(self):
        text = "## Code\n```\nshort block\n```\n## After"
        result = pre_filter(text)
        assert "short block" in result
    
    def test_dedup_repeated_lines(self):
        text = """Status update from server: OK
Status update from server: OK
Status update from server: OK
Something unique happened"""
        result = pre_filter(text)
        assert result.count("Status update") == 1
        assert "Something unique" in result


class TestChunkText:
    def test_small_text_single_chunk(self):
        text = "Small text"
        chunks = chunk_text(text)
        assert len(chunks) == 1
        assert chunks[0] == "Small text"
    
    def test_large_text_multiple_chunks(self):
        text = "\n".join(f"Line {i}: " + "x" * 80 for i in range(100))
        config = ChunkConfig(max_chunk_size=1000, pre_filter=False)
        chunks = chunk_text(text, config)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= 1200  # Some tolerance for line boundaries
    
    def test_splits_at_headers(self):
        text = "## Section 1\n" + "a " * 500 + "\n## Section 2\n" + "b " * 500
        config = ChunkConfig(max_chunk_size=600, pre_filter=False)
        chunks = chunk_text(text, config)
        assert len(chunks) >= 2
    
    def test_with_prefilter(self):
        text = "## Real content\n- Important\n- HEARTBEAT_OK\n- Also important\n" + "x " * 3000
        config = ChunkConfig(max_chunk_size=500, pre_filter=True)
        chunks = chunk_text(text, config)
        full = '\n'.join(chunks)
        assert "HEARTBEAT_OK" not in full


class TestMergeExtractions:
    def test_merges_entities(self):
        r1 = {"entities": [{"name": "Alice", "type": "person", "facts": ["likes cats"]}],
               "triplets": [], "events": []}
        r2 = {"entities": [{"name": "Alice", "type": "person", "facts": ["works at Corp"]}],
               "triplets": [], "events": []}
        
        merged = merge_extractions([r1, r2])
        assert len(merged["entities"]) == 1
        assert "likes cats" in merged["entities"][0]["facts"]
        assert "works at Corp" in merged["entities"][0]["facts"]
    
    def test_dedup_triplets(self):
        t = {"subject": "A", "predicate": "knows", "object": "B"}
        r1 = {"entities": [], "triplets": [t], "events": []}
        r2 = {"entities": [], "triplets": [t], "events": []}
        
        merged = merge_extractions([r1, r2])
        assert len(merged["triplets"]) == 1
    
    def test_dedup_events(self):
        e = {"description": "Something important happened today that matters", "entities": []}
        r1 = {"entities": [], "triplets": [], "events": [e]}
        r2 = {"entities": [], "triplets": [], "events": [e]}
        
        merged = merge_extractions([r1, r2])
        assert len(merged["events"]) == 1
    
    def test_different_entities_preserved(self):
        r1 = {"entities": [{"name": "Alice", "type": "person"}],
               "triplets": [], "events": []}
        r2 = {"entities": [{"name": "Bob", "type": "person"}],
               "triplets": [], "events": []}
        
        merged = merge_extractions([r1, r2])
        assert len(merged["entities"]) == 2
