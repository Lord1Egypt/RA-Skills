"""Tests for the entity deduplication module."""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.dedup import find_duplicates, merge_entity_files, run_dedup, sanitize_filename


@pytest.fixture
def entity_dir(tmp_path):
    entities = tmp_path / "entities"
    entities.mkdir()
    return entities


@pytest.fixture
def graph_file(tmp_path):
    gf = tmp_path / "graph.jsonl"
    return gf


class TestFindDuplicates:
    def test_alias_detection(self, entity_dir):
        """Configured aliases should be detected."""
        (entity_dir / "steipete.md").write_text("# steipete\n**Type:** person\n")
        (entity_dir / "Peter-Steinberger.md").write_text("# Peter Steinberger\n**Type:** person\n")
        
        aliases = {"Peter Steinberger": "steipete"}
        dupes = find_duplicates(entity_dir, aliases=aliases)
        
        assert len(dupes) >= 1
        files = [d[0] + d[1] for d in dupes]
        assert any("steipete" in f and "Peter-Steinberger" in f for f in files)
    
    def test_mutual_reference_detection(self, entity_dir):
        """Entities that reference each other should be flagged."""
        (entity_dir / "steipete.md").write_text(
            "# steipete\n**Type:** person\n\n"
            "Peter Steinberger is the maintainer\n"
        )
        (entity_dir / "Peter-Steinberger.md").write_text(
            "# Peter Steinberger\n**Type:** person\n\n"
            "Also known as steipete on GitHub\n"
        )
        
        dupes = find_duplicates(entity_dir)
        assert len(dupes) >= 1
        assert any("mutual" in d[2] for d in dupes)
    
    def test_no_false_positives(self, entity_dir):
        """Unrelated entities should not be flagged."""
        (entity_dir / "Alice.md").write_text("# Alice\n**Type:** person\nWorks at Corp A\n")
        (entity_dir / "Bob.md").write_text("# Bob\n**Type:** person\nWorks at Corp B\n")
        
        dupes = find_duplicates(entity_dir)
        assert len(dupes) == 0
    
    def test_graph_overlap_detection(self, entity_dir, graph_file):
        """Entities sharing many graph neighbors should be flagged."""
        (entity_dir / "A.md").write_text("# A\n**Type:** person\n")
        (entity_dir / "B.md").write_text("# B\n**Type:** person\n")
        
        # Both A and B connected to same neighbors
        triplets = [
            {"subject": "a", "predicate": "knows", "object": "x"},
            {"subject": "a", "predicate": "knows", "object": "y"},
            {"subject": "b", "predicate": "knows", "object": "x"},
            {"subject": "b", "predicate": "knows", "object": "y"},
        ]
        graph_file.write_text('\n'.join(json.dumps(t) for t in triplets))
        
        dupes = find_duplicates(entity_dir, graph_file)
        assert len(dupes) >= 1
        assert any("graph overlap" in d[2] for d in dupes)


class TestMergeEntityFiles:
    def test_merge_facts(self, entity_dir):
        primary = entity_dir / "Peter-Steinberger.md"
        secondary = entity_dir / "steipete.md"
        
        primary.write_text(
            "# Peter Steinberger\n**Type:** person\n\n"
            "## Facts\n- Maintainer of OpenClaw\n\n"
            "## Timeline\n\n### [[2026-02-16]]\n- Merged PR #18444\n"
        )
        secondary.write_text(
            "# steipete\n**Type:** person\n\n"
            "## Facts\n- GitHub handle: @steipete\n\n"
            "## Timeline\n\n### [[2026-02-13]]\n- Merged PR #15739\n"
        )
        
        result = merge_entity_files(primary, secondary)
        merged = primary.read_text()
        
        assert "Maintainer of OpenClaw" in merged
        assert "GitHub handle: @steipete" in merged
        assert "2026-02-13" in merged
        assert "2026-02-16" in merged
        assert "steipete" in merged  # alias note
    
    def test_merge_preserves_existing(self, entity_dir):
        primary = entity_dir / "Primary.md"
        secondary = entity_dir / "Secondary.md"
        
        primary.write_text("# Primary\n**Type:** test\n\n## Facts\n- Fact A\n\n## Timeline\n")
        secondary.write_text("# Secondary\n**Type:** test\n\n## Facts\n- Fact A\n\n## Timeline\n")
        
        merge_entity_files(primary, secondary)
        merged = primary.read_text()
        
        # Fact A should appear only once
        assert merged.count("Fact A") == 1
    
    def test_merge_delete_secondary(self, entity_dir):
        primary = entity_dir / "Primary.md"
        secondary = entity_dir / "Secondary.md"
        
        primary.write_text("# Primary\n**Type:** test\n")
        secondary.write_text("# Secondary\n**Type:** test\n")
        
        merge_entity_files(primary, secondary, delete_secondary=True)
        
        assert primary.exists()
        assert not secondary.exists()


class TestRunDedup:
    def test_dry_run(self, entity_dir):
        (entity_dir / "steipete.md").write_text(
            "# steipete\n**Type:** person\nPeter Steinberger\n")
        (entity_dir / "Peter-Steinberger.md").write_text(
            "# Peter Steinberger\n**Type:** person\nsteipete\n")
        
        actions = run_dedup(entity_dir, auto_merge=False)
        assert any("Potential duplicate" in a or "duplicate" in a.lower() for a in actions)
    
    def test_auto_merge(self, entity_dir):
        (entity_dir / "steipete.md").write_text(
            "# steipete\n**Type:** person\nPeter Steinberger\n")
        (entity_dir / "Peter-Steinberger.md").write_text(
            "# Peter Steinberger\n**Type:** person\nsteipete\nMore content here\n")
        
        actions = run_dedup(entity_dir, auto_merge=True)
        assert any("Merged" in a for a in actions)
        
        # One file should be gone
        remaining = list(entity_dir.glob("*.md"))
        assert len(remaining) == 1
