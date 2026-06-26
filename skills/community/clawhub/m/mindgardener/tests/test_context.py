"""Tests for token-budget-aware context assembly."""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.config import EngramConfig
from engram.context import (
    assemble_context,
    estimate_tokens,
    _score_entity,
    _score_daily,
    CHARS_PER_TOKEN,
)


@pytest.fixture
def workspace(tmp_path):
    """Create a test workspace with entities, logs, and memory."""
    entities = tmp_path / "memory" / "entities"
    entities.mkdir(parents=True)
    memory = tmp_path / "memory"
    
    # Create entities
    (entities / "Marcus.md").write_text(
        "# Marcus\n**Type:** person\n\n## Timeline\n### [[2026-02-17]]\n"
        "- Applied to Sana Labs\n- Working on MindGardener\n"
        "- Lives in [[Stockholm]]\n- Uses [[OpenClaw]]\n"
    )
    (entities / "OpenClaw.md").write_text(
        "# OpenClaw\n**Type:** project\n\n## Facts\n- 200k stars\n\n"
        "## Timeline\n### [[2026-02-17]]\n- PR merged\n"
    )
    (entities / "Stockholm.md").write_text(
        "# Stockholm\n**Type:** location\n\n## Timeline\n"
    )
    (entities / "Sana-Labs.md").write_text(
        "# Sana Labs\n**Type:** company\n\n## Facts\n- AI startup\n"
    )
    
    # Create daily log
    today = datetime.now().strftime("%Y-%m-%d")
    (memory / f"{today}.md").write_text(
        f"# {today}\n## Jobs\n- Applied to Sana Labs\n- MindGardener v2 shipped\n"
    )
    
    # Create MEMORY.md
    (tmp_path / "MEMORY.md").write_text(
        "# Long Term Memory\n## Job Search\n- Applied to H&M, Sana, SÄPO\n"
        "## Projects\n- MindGardener: memory for AI agents\n"
    )
    
    # Create graph
    (memory / "graph.jsonl").write_text(
        json.dumps({"subject": "Marcus", "predicate": "applied_to", "object": "Sana Labs", "date": "2026-02-17"}) + "\n"
        + json.dumps({"subject": "Marcus", "predicate": "uses", "object": "OpenClaw", "date": "2026-02-17"}) + "\n"
    )
    
    # Create garden.yaml
    (tmp_path / "garden.yaml").write_text(
        f"workspace: {tmp_path}\n"
        f"memory_dir: memory/\n"
        f"entities_dir: memory/entities/\n"
        f"graph_file: memory/graph.jsonl\n"
        f"long_term_memory: MEMORY.md\n"
    )
    
    return EngramConfig(
        workspace=tmp_path,
        memory_dir=memory,
        entities_dir=entities,
        graph_file=memory / "graph.jsonl",
        long_term_memory=tmp_path / "MEMORY.md",
    )


class TestEstimateTokens:
    def test_basic(self):
        assert estimate_tokens("hello world") > 0
    
    def test_empty(self):
        assert estimate_tokens("") >= 1  # minimum 1
    
    def test_proportional(self):
        short = estimate_tokens("hello")
        long = estimate_tokens("hello " * 100)
        assert long > short
    
    def test_chars_per_token(self):
        text = "a" * 400
        assert estimate_tokens(text) == 400 // CHARS_PER_TOKEN


class TestScoreEntity:
    def test_exact_name_match(self):
        score = _score_entity("Marcus", "Marcus", "some content", {"marcus"})
        assert score >= 0.9
    
    def test_partial_name_match(self):
        score = _score_entity("Sana", "Sana Labs", "some content", {"sana"})
        assert score > 0.5
    
    def test_content_match(self):
        score = _score_entity("Stockholm", "Marcus", "Lives in Stockholm", {"stockholm"})
        assert score > 0
    
    def test_no_match(self):
        score = _score_entity("quantum physics", "Marcus", "AI developer", {"quantum", "physics"})
        assert score == 0.0 or score < 0.3


class TestScoreDaily:
    def test_exact_query_in_content(self):
        score = _score_daily("MindGardener", "Worked on MindGardener v2", {"mindgardener"}, 0)
        assert score >= 0.3
    
    def test_word_match(self):
        score = _score_daily("something", "something happened", {"something"}, 0)
        assert score > 0
    
    def test_recency_decay(self):
        score_today = _score_daily("something", "something happened", {"something"}, 0)
        score_old = _score_daily("something", "something happened", {"something"}, 5)
        assert score_today >= score_old


class TestAssembleContext:
    def test_basic_query(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000)
        assert "Marcus" in result["context"]
        assert result["manifest"]["tokens_used"] > 0
    
    def test_respects_budget(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=100)
        assert result["manifest"]["tokens_used"] <= 150  # Allow some overhead
    
    def test_large_budget(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=10000)
        assert result["manifest"]["loaded_count"] > 0
    
    def test_includes_linked_entities(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000, max_hops=1)
        # Should include Stockholm or OpenClaw (linked from Marcus)
        assert "Stockholm" in result["context"] or "OpenClaw" in result["context"]
    
    def test_includes_graph(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000, include_graph=True)
        assert "applied_to" in result["context"] or "Graph" in result["context"]
    
    def test_excludes_graph_when_disabled(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000, include_graph=False)
        graph_loaded = [i for i in result["manifest"]["loaded"] if i["type"] == "graph"]
        assert len(graph_loaded) == 0
    
    def test_includes_memory(self, workspace):
        result = assemble_context("job search", workspace, token_budget=4000, include_memory=True)
        assert "Job Search" in result["context"] or "Long-Term" in result["context"]
    
    def test_manifest_structure(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000)
        manifest = result["manifest"]
        assert "query" in manifest
        assert "token_budget" in manifest
        assert "tokens_used" in manifest
        assert "loaded" in manifest
        assert "skipped" in manifest
        assert "timestamp" in manifest
    
    def test_manifest_json_serializable(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000)
        # Should be JSON serializable
        json_str = json.dumps(result["manifest"])
        parsed = json.loads(json_str)
        assert parsed["query"] == "Marcus"
    
    def test_empty_query(self, workspace):
        result = assemble_context("", workspace, token_budget=4000)
        # Should not crash
        assert isinstance(result["context"], str)
    
    def test_no_matches(self, tmp_path):
        empty_entities = tmp_path / "entities"
        empty_entities.mkdir()
        cfg = EngramConfig(
            workspace=tmp_path,
            memory_dir=tmp_path,
            entities_dir=empty_entities,
            graph_file=tmp_path / "graph.jsonl",
            long_term_memory=tmp_path / "MEMORY.md",
        )
        result = assemble_context("nonexistent", cfg, token_budget=4000)
        assert result["manifest"]["loaded_count"] == 0
    
    def test_budget_tokens_alias(self, workspace):
        """budget_tokens parameter alias works."""
        result = assemble_context("Marcus", workspace, budget_tokens=4000)
        assert result["manifest"]["tokens_used"] > 0
    
    def test_utilization(self, workspace):
        result = assemble_context("Marcus", workspace, token_budget=4000)
        manifest = result["manifest"]
        assert 0 <= manifest["utilization"] <= 1.0
