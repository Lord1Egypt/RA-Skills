"""
Smoke tests for agent-engram.

Tests core pipeline with mocked LLM calls.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# ---- Fixtures ----

@pytest.fixture
def workspace(tmp_path):
    """Minimal engram workspace."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    entities_dir = memory_dir / "entities"
    entities_dir.mkdir()
    
    daily = memory_dir / "2026-02-16.md"
    daily.write_text("""# 2026-02-16 Daily Notes
## Research
- Talked to Adrian Krebs at Kadoa about web scraping
- Adrian is the CTO of Kadoa
- Submitted PR #18444 to OpenClaw (infinite retry loop fix)
""")
    
    memory_file = tmp_path / "MEMORY.md"
    memory_file.write_text("# Long-term Memory\n- Working on OpenClaw contributions\n")
    
    return {
        "root": tmp_path,
        "memory_dir": memory_dir,
        "entities_dir": entities_dir,
        "memory_file": memory_file,
    }


# ---- PE Engine Tests (class-based, direct) ----

def make_mock_llm():
    """Mock LLM provider matching engram's LLMProvider interface."""
    from engram.providers import LLMProvider
    
    llm = MagicMock(spec=LLMProvider)
    
    predict_response = {
        "predictions": [
            {"event": "Continued OpenClaw work", "confidence": 0.8, "reasoning": "Active contributor"},
        ]
    }
    
    compare_response = {
        "errors": [
            {"event": "Talked to Adrian Krebs at Kadoa", "prediction_error": 0.7,
             "predicted": None, "reason": "New contact", "category": "new_relationship",
             "entities": ["Adrian Krebs", "Kadoa"]},
            {"event": "Submitted PR #18444", "prediction_error": 0.3,
             "predicted": "Continued OpenClaw work", "reason": "Expected",
             "category": "routine", "entities": ["OpenClaw"]},
        ],
        "model_updates": ["Add Kadoa as a new contact/company"]
    }
    
    def side_effect(prompt):
        if "predict" in prompt.lower() and "compare" not in prompt.lower() and "prediction error" not in prompt.lower():
            return predict_response
        return compare_response
    
    llm.generate_json_sync = MagicMock(side_effect=side_effect)
    llm.generate_json = AsyncMock(side_effect=side_effect)
    
    return llm


class TestPredictionErrorEvent:
    def test_should_consolidate(self):
        from engram.prediction_error import PredictionErrorEvent
        
        high = PredictionErrorEvent(event="test", prediction_error=0.8)
        low = PredictionErrorEvent(event="test", prediction_error=0.3)
        
        assert high.should_consolidate(threshold=0.5)
        assert not low.should_consolidate(threshold=0.5)
    
    def test_serialization_roundtrip(self):
        from engram.prediction_error import PredictionErrorEvent
        
        event = PredictionErrorEvent(
            event="test event",
            prediction_error=0.7,
            reason="unexpected",
            category="new_relationship",
            entities=["Alice", "Bob"]
        )
        d = event.to_dict()
        restored = PredictionErrorEvent.from_dict(d)
        
        assert restored.event == "test event"
        assert restored.prediction_error == 0.7
        assert restored.entities == ["Alice", "Bob"]
    
    def test_default_threshold(self):
        from engram.prediction_error import PredictionErrorEvent
        
        # Default threshold is 0.5
        at_threshold = PredictionErrorEvent(event="test", prediction_error=0.5)
        assert at_threshold.should_consolidate()  # >= 0.5


class TestPredictionErrorEngine:
    def test_compute_scores(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        result = engine.compute_sync("2026-02-16")
        
        assert len(result.errors) == 2
        assert result.errors[0].prediction_error == 0.7
        assert result.errors[1].prediction_error == 0.3
    
    def test_mean_surprise(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        result = engine.compute_sync("2026-02-16")
        
        assert abs(result.mean_surprise - 0.5) < 0.01  # (0.7 + 0.3) / 2
    
    def test_high_vs_medium_surprise(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        result = engine.compute_sync("2026-02-16")
        
        assert len(result.high_surprise) == 0   # Nothing > 0.7
        assert len(result.medium_surprise) == 1  # 0.7 is in [0.4, 0.7]
    
    def test_no_daily_log(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        result = engine.compute_sync("2099-01-01")
        
        assert len(result.errors) == 0
        assert result.mean_surprise == 0.0
    
    def test_scores_persisted(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        engine.compute_sync("2026-02-16")
        
        scores_file = workspace["memory_dir"] / "prediction-errors.jsonl"
        assert scores_file.exists()
        
        lines = [l for l in scores_file.read_text().strip().split('\n') if l]
        assert len(lines) == 2
        
        first = json.loads(lines[0])
        assert "prediction_error" in first
        assert "event" in first
    
    def test_model_updates(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        result = engine.compute_sync("2026-02-16")
        
        assert len(result.model_updates) == 1
        assert "Kadoa" in result.model_updates[0]
    
    def test_learning_rate_empty(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        
        # No scores yet
        assert engine.learning_rate() == 0.0
    
    def test_learning_rate_after_compute(self, workspace):
        from engram.prediction_error import PredictionErrorEngine
        
        llm = make_mock_llm()
        engine = PredictionErrorEngine(llm, workspace["memory_dir"], workspace["memory_file"])
        engine.compute_sync("2026-02-16")
        
        lr = engine.learning_rate()
        assert lr > 0
        assert abs(lr - 0.5) < 0.01


class TestPredictionResult:
    def test_empty_result(self):
        from engram.prediction_error import PredictionResult
        
        result = PredictionResult(date="2026-02-16", predictions=[], actual_events=[], errors=[])
        assert result.mean_surprise == 0.0
        assert result.high_surprise == []
        assert result.medium_surprise == []


class TestRecall:
    def test_recall_function(self, workspace):
        """Test the recall module's entity listing."""
        from engram.recall import list_entities
        from engram.config import EngramConfig
        
        # Create a test entity
        entity_file = workspace["entities_dir"] / "TestEntity.md"
        entity_file.write_text("# TestEntity\n**Type:** test\n\n## Facts\n- A test entity\n")
        
        config = EngramConfig.__new__(EngramConfig)
        config.workspace = workspace["root"]
        config.memory_dir = workspace["memory_dir"]
        config.entities_dir = workspace["entities_dir"]
        config.graph_file = workspace["memory_dir"] / "graph.jsonl"
        config.long_term_memory = workspace["memory_file"]
        config.surprise_file = workspace["memory_dir"] / "surprise-scores.jsonl"
        
        entities = list_entities(config)
        assert len(entities) >= 1
        names = [e["name"] for e in entities]
        assert "TestEntity" in names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
