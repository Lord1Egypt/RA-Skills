"""Tests for the decay scoring module."""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.decay import (
    calculate_decay, score_fact, apply_decay_to_graph,
    prune_decayed, reinforce_fact, DEFAULT_HALF_LIFE
)


@pytest.fixture
def graph_file(tmp_path):
    gf = tmp_path / "graph.jsonl"
    return gf


def make_fact(subject, predicate, obj, days_ago=0, confidence=0.8, reinforcements=0):
    """Create a test fact with timestamp."""
    ts = (datetime.now() - timedelta(days=days_ago)).isoformat()
    return {
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "provenance": {
            "timestamp": ts,
            "confidence": confidence,
        },
        "reinforcements": reinforcements,
    }


class TestCalculateDecay:
    def test_fresh_fact_has_high_decay(self):
        ts = datetime.now().isoformat()
        decay = calculate_decay(ts)
        assert decay > 0.95
    
    def test_old_fact_has_low_decay(self):
        ts = (datetime.now() - timedelta(days=60)).isoformat()
        decay = calculate_decay(ts, half_life_days=30)
        assert decay < 0.3  # After 2 half-lives
    
    def test_half_life_is_accurate(self):
        ts = (datetime.now() - timedelta(days=30)).isoformat()
        decay = calculate_decay(ts, half_life_days=30)
        assert 0.45 < decay < 0.55  # Should be ~0.5
    
    def test_reinforcements_slow_decay(self):
        ts = (datetime.now() - timedelta(days=30)).isoformat()
        no_reinforce = calculate_decay(ts, reinforcements=0)
        with_reinforce = calculate_decay(ts, reinforcements=2)
        assert with_reinforce > no_reinforce


class TestScoreFact:
    def test_score_combines_confidence_and_decay(self):
        fact = make_fact("A", "knows", "B", days_ago=0, confidence=0.8)
        score = score_fact(fact)
        assert 0.75 < score < 0.85  # Fresh fact, ~confidence
    
    def test_old_low_confidence_has_low_score(self):
        fact = make_fact("A", "knows", "B", days_ago=90, confidence=0.5)
        score = score_fact(fact, half_life_days=30)
        assert score < 0.2


class TestApplyDecayToGraph:
    def test_scores_all_facts(self, graph_file):
        facts = [
            make_fact("A", "knows", "B", days_ago=0),
            make_fact("C", "knows", "D", days_ago=60),
        ]
        graph_file.write_text("\n".join(json.dumps(f) for f in facts))
        
        scored = apply_decay_to_graph(graph_file)
        assert len(scored) == 2
        assert all("_decay_score" in f for f in scored)
    
    def test_sorted_by_score(self, graph_file):
        facts = [
            make_fact("Fresh", "is", "new", days_ago=0),
            make_fact("Old", "is", "ancient", days_ago=90),
        ]
        graph_file.write_text("\n".join(json.dumps(f) for f in facts))
        
        scored = apply_decay_to_graph(graph_file)
        # Lowest score first
        assert scored[0]["subject"] == "Old"


class TestPruneDecayed:
    def test_dry_run_doesnt_modify(self, graph_file):
        facts = [make_fact("A", "knows", "B", days_ago=0)]
        graph_file.write_text(json.dumps(facts[0]))
        
        kept, pruned = prune_decayed(graph_file, threshold=0.0, dry_run=True)
        assert kept == 1
        assert pruned == 0
    
    def test_prune_removes_old_facts(self, graph_file):
        facts = [
            make_fact("Fresh", "is", "new", days_ago=0),
            make_fact("Old", "is", "ancient", days_ago=365),
        ]
        graph_file.write_text("\n".join(json.dumps(f) for f in facts))
        
        kept, pruned = prune_decayed(graph_file, threshold=0.5, dry_run=False)
        assert kept == 1
        assert pruned == 1
        
        # Verify file was updated
        remaining = graph_file.read_text().strip().split('\n')
        assert len(remaining) == 1


class TestReinforceFact:
    def test_increments_reinforcement_count(self, graph_file):
        fact = make_fact("A", "knows", "B")
        graph_file.write_text(json.dumps(fact))
        
        result = reinforce_fact(graph_file, "A", "knows", "B")
        assert result is True
        
        updated = json.loads(graph_file.read_text().strip())
        assert updated["reinforcements"] == 1
    
    def test_returns_false_for_missing_fact(self, graph_file):
        fact = make_fact("A", "knows", "B")
        graph_file.write_text(json.dumps(fact))
        
        result = reinforce_fact(graph_file, "X", "knows", "Y")
        assert result is False
