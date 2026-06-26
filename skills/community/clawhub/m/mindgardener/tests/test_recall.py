"""Smoke tests for Engram — validates core functionality without LLM calls."""

import json
import os
import tempfile
from pathlib import Path

import pytest

# Set workspace before imports
_tmpdir = None


@pytest.fixture(autouse=True)
def workspace(tmp_path):
    """Create a temp workspace with test data."""
    global _tmpdir
    _tmpdir = tmp_path
    
    # Create directory structure
    (tmp_path / "memory" / "entities").mkdir(parents=True)
    
    # Create a daily log
    (tmp_path / "memory" / "2026-02-16.md").write_text("""# 2026-02-16

## OpenClaw Contribution
- Submitted PR #18444: fix infinite retry loop
- steipete merged it within 2 hours
- Greptile gave 5/5 review score

## Job Search
- Sent cold email to Adrian Krebs at Kadoa
- Adrian replied same day — interested in collaboration
""")
    
    # Create entity files
    (tmp_path / "memory" / "entities" / "Kadoa.md").write_text("""# Kadoa
**Type:** company

## Facts
- AI web scraping startup
- Adrian Krebs works here

## Timeline
### [[2026-02-16]]
- Received reply from [[Adrian Krebs]] after HN outreach
- [[Revenue Hunter]] sent cold email

## Relations
- [[Adrian Krebs]]
""")
    
    (tmp_path / "memory" / "entities" / "Adrian-Krebs.md").write_text("""# Adrian Krebs
**Type:** person

## Facts
- Works at [[Kadoa]]

## Timeline
### [[2026-02-16]]
- Replied to cold outreach
""")
    
    (tmp_path / "memory" / "entities" / "OpenClaw.md").write_text("""# OpenClaw
**Type:** project

## Timeline
### [[2026-02-16]]
- PR #18444 submitted and merged
""")
    
    # Create graph file
    triplets = [
        {"subject": "Adrian Krebs", "predicate": "works_at", "object": "Kadoa", "date": "2026-02-16", "detail": ""},
        {"subject": "steipete", "predicate": "merged", "object": "PR #18444", "date": "2026-02-16", "detail": ""},
        {"subject": "PR #18444", "predicate": "fixes", "object": "OpenClaw", "date": "2026-02-16", "detail": "infinite retry loop"},
    ]
    with open(tmp_path / "memory" / "graph.jsonl", "w") as f:
        for t in triplets:
            f.write(json.dumps(t) + "\n")
    
    # Create MEMORY.md
    (tmp_path / "MEMORY.md").write_text("# Long-term Memory\n\nMarcus is looking for AI engineering jobs.\n")
    
    # Create config
    (tmp_path / "engram.yaml").write_text(f"""
workspace: {tmp_path}
memory_dir: memory/
entities_dir: memory/entities/
graph_file: memory/graph.jsonl
long_term_memory: MEMORY.md
""")
    
    os.environ["ENGRAM_WORKSPACE"] = str(tmp_path)
    yield tmp_path
    del os.environ["ENGRAM_WORKSPACE"]


class TestConfig:
    def test_load_config(self, workspace):
        from engram.config import load_config
        cfg = load_config(workspace / "engram.yaml")
        assert cfg.workspace == workspace
        assert cfg.entities_dir.exists()
        assert cfg.graph_file.exists()

    def test_default_config(self):
        from engram.config import EngramConfig
        cfg = EngramConfig()
        assert cfg.extraction.model == "gemini-2.0-flash"
        assert cfg.consolidation.surprise_threshold == 0.5


class TestRecall:
    def test_exact_match(self, workspace):
        from engram.config import load_config
        from engram.recall import recall
        cfg = load_config(workspace / "engram.yaml")
        
        result = recall("Kadoa", cfg)
        assert "Kadoa" in result
        assert "company" in result
        assert "Adrian Krebs" in result

    def test_linked_entities(self, workspace):
        from engram.config import load_config
        from engram.recall import recall
        cfg = load_config(workspace / "engram.yaml")
        
        result = recall("Kadoa", cfg, hops=1)
        assert "Adrian Krebs" in result
        assert "Works at" in result or "works_at" in result

    def test_graph_connections(self, workspace):
        from engram.config import load_config
        from engram.recall import recall
        cfg = load_config(workspace / "engram.yaml")
        
        result = recall("Kadoa", cfg)
        assert "works_at" in result

    def test_no_match(self, workspace):
        from engram.config import load_config
        from engram.recall import recall
        cfg = load_config(workspace / "engram.yaml")
        
        result = recall("NonExistentEntity", cfg)
        assert "No entities found" in result

    def test_partial_match(self, workspace):
        from engram.config import load_config
        from engram.recall import recall
        cfg = load_config(workspace / "engram.yaml")
        
        result = recall("Adrian", cfg)
        assert "Adrian Krebs" in result


class TestEntities:
    def test_list_entities(self, workspace):
        from engram.config import load_config
        from engram.recall import list_entities
        cfg = load_config(workspace / "engram.yaml")
        
        entities = list_entities(cfg)
        assert len(entities) == 3
        
        names = {e["name"] for e in entities}
        assert "Kadoa" in names
        assert "Adrian Krebs" in names
        assert "OpenClaw" in names

    def test_entity_types(self, workspace):
        from engram.config import load_config
        from engram.recall import list_entities
        cfg = load_config(workspace / "engram.yaml")
        
        entities = list_entities(cfg)
        types = {e["name"]: e["type"] for e in entities}
        assert types["Kadoa"] == "company"
        assert types["Adrian Krebs"] == "person"
        assert types["OpenClaw"] == "project"


class TestGraphSearch:
    def test_search_subject(self, workspace):
        from engram.config import load_config
        from engram.recall import search_graph
        cfg = load_config(workspace / "engram.yaml")
        
        results = search_graph("Adrian", cfg)
        assert any("works_at" in r for r in results)

    def test_search_object(self, workspace):
        from engram.config import load_config
        from engram.recall import search_graph
        cfg = load_config(workspace / "engram.yaml")
        
        results = search_graph("Kadoa", cfg)
        assert len(results) >= 1


class TestWikilinks:
    def test_extract_wikilinks(self):
        from engram.recall import extract_wikilinks
        
        text = "Talked to [[Adrian Krebs]] about [[Kadoa]] on [[2026-02-16]]"
        links = extract_wikilinks(text)
        
        assert "Adrian Krebs" in links
        assert "Kadoa" in links
        # Date links should be excluded
        assert "2026-02-16" not in links

    def test_dedup_wikilinks(self):
        from engram.recall import extract_wikilinks
        
        text = "[[Kadoa]] mentioned [[Kadoa]] again, also [[Adrian]]"
        links = extract_wikilinks(text)
        assert links.count("Kadoa") == 1


class TestProviders:
    def test_get_provider_google(self):
        from engram.providers import get_provider
        p = get_provider("google", api_key="test")
        assert p is not None

    def test_get_provider_openai(self):
        from engram.providers import get_provider
        p = get_provider("openai", api_key="test")
        assert p is not None

    def test_get_provider_anthropic(self):
        from engram.providers import get_provider
        p = get_provider("anthropic", api_key="test")
        assert p is not None

    def test_unknown_provider(self):
        from engram.providers import get_provider
        with pytest.raises(ValueError):
            get_provider("unknown")

    def test_json_parsing(self):
        from engram.providers import _parse_json
        
        assert _parse_json('{"a": 1}') == {"a": 1}
        assert _parse_json('```json\n{"a": 1}\n```') == {"a": 1}
        assert _parse_json('some text {"a": 1} more text') == {"a": 1}
        assert _parse_json('not json at all') is None


class TestPredictionError:
    def test_dataclass(self):
        from engram.prediction_error import PredictionErrorEvent
        
        pe = PredictionErrorEvent(
            event="Surprise event",
            prediction_error=0.8,
            reason="Unexpected",
        )
        assert pe.should_consolidate(0.5)
        assert not pe.should_consolidate(0.9)

    def test_prediction_result(self):
        from engram.prediction_error import PredictionErrorEvent, PredictionResult
        
        result = PredictionResult(
            date="2026-02-16",
            predictions=["Expected A"],
            actual_events=["A happened", "B happened"],
            errors=[
                PredictionErrorEvent(event="A", prediction_error=0.2, reason="expected"),
                PredictionErrorEvent(event="B", prediction_error=0.8, reason="novel"),
            ],
        )
        assert len(result.high_surprise) == 1
        assert result.high_surprise[0].event == "B"
        assert result.mean_surprise == pytest.approx(0.5)


class TestCLI:
    def test_help(self, workspace):
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "engram.cli", "--help"],
            capture_output=True, text=True,
            cwd=str(workspace),
            env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        )
        assert result.returncode == 0
        assert "hippocampus" in result.stdout.lower() or "engram" in result.stdout.lower()

    def test_version(self, workspace):
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "engram.cli", "--version"],
            capture_output=True, text=True,
            cwd=str(workspace),
            env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        )
        assert "1.0.0" in result.stdout

    def test_stats(self, workspace):
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "engram.cli", "stats"],
            capture_output=True, text=True,
            cwd=str(workspace),
            env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent / "src")},
        )
        assert result.returncode == 0
        assert "Entities:" in result.stdout
