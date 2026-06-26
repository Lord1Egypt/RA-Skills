"""Tests for identity-level self-model and belief drift detection."""

import sys
import json
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.self_model import Belief, BeliefDrift, SelfModel, SelfModelEngine


class TestBelief:
    def test_basic_creation(self):
        b = Belief(claim="Prefers local-first tools", confidence=0.8, category="preferences")
        assert b.claim == "Prefers local-first tools"
        assert b.confidence == 0.8
        assert b.status == "active"

    def test_net_confidence_no_evidence(self):
        b = Belief(claim="test", confidence=0.8, category="goals")
        assert b.net_confidence() == 0.8

    def test_net_confidence_balanced(self):
        b = Belief(
            claim="test", confidence=0.8, category="goals",
            evidence_for=["a", "b"], evidence_against=["c", "d"],
        )
        # 2/4 = 0.5 balance, 0.8 * 0.5 = 0.4
        assert b.net_confidence() == pytest.approx(0.4)

    def test_net_confidence_strong_for(self):
        b = Belief(
            claim="test", confidence=0.8, category="goals",
            evidence_for=["a", "b", "c"], evidence_against=["d"],
        )
        # 3/4 = 0.75 balance, 0.8 * 0.75 = 0.6
        assert b.net_confidence() == pytest.approx(0.6)

    def test_to_dict_roundtrip(self):
        b = Belief(
            claim="test claim",
            confidence=0.7,
            category="values",
            evidence_for=["ev1"],
            evidence_against=["ev2"],
            first_observed="2026-01-01",
            last_updated="2026-02-01",
            status="active",
        )
        d = b.to_dict()
        b2 = Belief.from_dict(d)
        assert b2.claim == b.claim
        assert b2.confidence == b.confidence
        assert b2.evidence_for == b.evidence_for

    def test_from_dict_extra_keys(self):
        """Unknown keys should be ignored."""
        d = {"claim": "test", "confidence": 0.5, "category": "goals", "unknown_key": 42}
        b = Belief.from_dict(d)
        assert b.claim == "test"


class TestBeliefDrift:
    def test_creation(self):
        d = BeliefDrift(
            belief_claim="Prefers startups",
            drift_type="strengthened",
            old_confidence=0.6,
            new_confidence=0.8,
            trigger_event="Turned down corporate offer",
            reasoning="Third time choosing startup",
            significance=0.5,
        )
        assert d.drift_type == "strengthened"
        assert d.significance == 0.5

    def test_to_dict(self):
        d = BeliefDrift(
            belief_claim="test",
            drift_type="new",
            old_confidence=0.0,
            new_confidence=0.7,
            trigger_event="event",
            reasoning="reason",
            significance=0.8,
        )
        result = d.to_dict()
        assert result["belief_claim"] == "test"
        assert result["significance"] == 0.8


class TestSelfModel:
    def test_empty_model(self):
        m = SelfModel()
        assert len(m.beliefs) == 0
        assert m.version == 0

    def test_active_beliefs(self):
        m = SelfModel(beliefs=[
            Belief(claim="a", confidence=0.8, category="goals", status="active"),
            Belief(claim="b", confidence=0.5, category="goals", status="archived"),
            Belief(claim="c", confidence=0.3, category="goals", status="weakening"),
        ])
        assert len(m.active_beliefs()) == 1

    def test_by_category(self):
        m = SelfModel(beliefs=[
            Belief(claim="a", confidence=0.8, category="goals"),
            Belief(claim="b", confidence=0.5, category="values"),
            Belief(claim="c", confidence=0.3, category="goals"),
        ])
        assert len(m.by_category("goals")) == 2
        assert len(m.by_category("values")) == 1
        assert len(m.by_category("skills")) == 0

    def test_high_confidence(self):
        m = SelfModel(beliefs=[
            Belief(claim="a", confidence=0.9, category="goals"),
            Belief(claim="b", confidence=0.5, category="goals"),
            Belief(claim="c", confidence=0.8, category="goals"),
        ])
        high = m.high_confidence(0.7)
        assert len(high) == 2

    def test_weakening(self):
        m = SelfModel(beliefs=[
            Belief(claim="a", confidence=0.2, category="goals", status="weakening"),
            Belief(claim="b", confidence=0.8, category="goals", status="active"),
        ])
        assert len(m.weakening()) == 1
        assert m.weakening()[0].claim == "a"

    def test_find(self):
        m = SelfModel(beliefs=[
            Belief(claim="Prefers local-first tools", confidence=0.8, category="preferences"),
            Belief(claim="Targets AI startups", confidence=0.7, category="goals"),
        ])
        assert len(m.find("local")) == 1
        assert len(m.find("TARGETS")) == 1  # Case insensitive
        assert len(m.find("nonexistent")) == 0

    def test_yaml_roundtrip(self):
        m = SelfModel(
            beliefs=[
                Belief(
                    claim="Prefers local-first tools",
                    confidence=0.8,
                    category="preferences",
                    evidence_for=["Built MindGardener"],
                    first_observed="2026-01-01",
                    last_updated="2026-02-01",
                ),
                Belief(
                    claim="Targets AI startups",
                    confidence=0.7,
                    category="goals",
                    evidence_against=["Applied to H&M"],
                ),
            ],
            last_updated="2026-02-17",
            version=3,
        )
        yaml_str = m.to_yaml()
        m2 = SelfModel.from_yaml(yaml_str)

        assert len(m2.beliefs) == 2
        assert m2.beliefs[0].claim == "Prefers local-first tools"
        assert m2.beliefs[0].confidence == 0.8
        assert m2.beliefs[1].evidence_against == ["Applied to H&M"]
        assert m2.version == 3

    def test_yaml_empty(self):
        m = SelfModel.from_yaml("")
        assert len(m.beliefs) == 0

    def test_format_readable(self):
        m = SelfModel(
            beliefs=[
                Belief(claim="Prefers local-first", confidence=0.8, category="preferences"),
                Belief(claim="Weakening claim", confidence=0.2, category="goals", status="weakening"),
            ],
            version=1,
            last_updated="2026-02-17",
        )
        text = m.format_readable()
        assert "Prefers local-first" in text
        assert "Weakening" in text
        assert "80%" in text

    def test_format_readable_empty(self):
        m = SelfModel()
        text = m.format_readable()
        assert "No beliefs" in text


class TestSelfModelEngine:
    @pytest.fixture
    def engine_setup(self, tmp_path):
        """Set up engine with mock LLM."""
        model_path = tmp_path / "memory" / "self-model.yaml"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        return tmp_path, model_path

    def test_load_empty(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)
        model = engine.load()
        assert len(model.beliefs) == 0

    def test_save_and_load(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[
            Belief(claim="Test belief", confidence=0.9, category="goals"),
        ])
        engine.save(model)

        loaded = engine.load()
        assert len(loaded.beliefs) == 1
        assert loaded.beliefs[0].claim == "Test belief"
        assert loaded.version == 1

    def test_save_increments_version(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[])
        engine.save(model)
        assert model.version == 1
        engine.save(model)
        assert model.version == 2

    def test_apply_drifts_new(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        # Create initial model
        model = SelfModel(beliefs=[
            Belief(claim="Targets AI startups", confidence=0.7, category="goals"),
        ])
        engine.save(model)

        # Apply new belief drift
        drifts = [BeliefDrift(
            belief_claim="Values remote work",
            drift_type="new",
            old_confidence=0.0,
            new_confidence=0.8,
            trigger_event="Turned down office-only role",
            reasoning="Pattern of remote preference",
            significance=0.6,
        )]
        result = engine.apply_drifts(drifts)
        assert len(result.beliefs) == 2
        new_belief = [b for b in result.beliefs if b.claim == "Values remote work"]
        assert len(new_belief) == 1
        assert new_belief[0].confidence == 0.8

    def test_apply_drifts_strengthen(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[
            Belief(claim="Targets AI startups", confidence=0.6, category="goals"),
        ])
        engine.save(model)

        drifts = [BeliefDrift(
            belief_claim="Targets AI startups",
            drift_type="strengthened",
            old_confidence=0.6,
            new_confidence=0.85,
            trigger_event="Applied to third AI startup",
            reasoning="Consistent pattern",
            significance=0.4,
        )]
        result = engine.apply_drifts(drifts)
        assert result.beliefs[0].confidence == 0.85
        assert "Applied to third AI startup" in result.beliefs[0].evidence_for

    def test_apply_drifts_weaken(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[
            Belief(claim="Targets AI startups", confidence=0.8, category="goals"),
        ])
        engine.save(model)

        drifts = [BeliefDrift(
            belief_claim="Targets AI startups",
            drift_type="weakened",
            old_confidence=0.8,
            new_confidence=0.4,
            trigger_event="Applied to H&M (non-AI)",
            reasoning="Breaking the AI-only pattern",
            significance=0.5,
        )]
        result = engine.apply_drifts(drifts)
        assert result.beliefs[0].confidence == 0.4
        assert "Applied to H&M (non-AI)" in result.beliefs[0].evidence_against

    def test_apply_drifts_contradict(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[
            Belief(claim="Dislikes networking", confidence=0.7, category="habits"),
        ])
        engine.save(model)

        drifts = [BeliefDrift(
            belief_claim="Dislikes networking",
            drift_type="contradicted",
            old_confidence=0.7,
            new_confidence=0.2,
            trigger_event="Initiated 5 networking DMs in one day",
            reasoning="Direct contradiction of assumed behavior",
            significance=0.8,
        )]
        result = engine.apply_drifts(drifts)
        assert result.beliefs[0].confidence == 0.2
        assert result.beliefs[0].status == "weakening"

    def test_apply_drifts_below_threshold(self, engine_setup):
        tmp_path, model_path = engine_setup
        engine = SelfModelEngine(llm=None, model_path=model_path)

        model = SelfModel(beliefs=[
            Belief(claim="Test", confidence=0.5, category="goals"),
        ])
        engine.save(model)

        drifts = [BeliefDrift(
            belief_claim="Test",
            drift_type="strengthened",
            old_confidence=0.5,
            new_confidence=0.55,
            trigger_event="Minor event",
            reasoning="Tiny confirmation",
            significance=0.1,  # Below default 0.3 threshold
        )]
        result = engine.apply_drifts(drifts, significance_threshold=0.3)
        # Should not have changed
        assert result.beliefs[0].confidence == 0.5

    def test_drift_log(self, engine_setup):
        tmp_path, model_path = engine_setup
        drift_log = tmp_path / "memory" / "belief-drifts.jsonl"
        engine = SelfModelEngine(llm=None, model_path=model_path, drift_log_path=drift_log)

        drifts = [BeliefDrift(
            belief_claim="Test",
            drift_type="new",
            old_confidence=0.0,
            new_confidence=0.7,
            trigger_event="event",
            reasoning="reason",
            significance=0.5,
        )]
        engine._log_drifts(drifts)

        assert drift_log.exists()
        lines = drift_log.read_text().strip().split("\n")
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["belief_claim"] == "Test"
        assert "timestamp" in entry

    def test_format_drifts_empty(self):
        engine = SelfModelEngine(llm=None, model_path=Path("/tmp/unused"))
        text = engine.format_drifts([])
        assert "No identity-level changes" in text

    def test_format_drifts(self):
        engine = SelfModelEngine(llm=None, model_path=Path("/tmp/unused"))
        drifts = [BeliefDrift(
            belief_claim="Targets AI startups",
            drift_type="strengthened",
            old_confidence=0.6,
            new_confidence=0.85,
            trigger_event="Applied to Kadoa",
            reasoning="Pattern confirmed",
            significance=0.5,
        )]
        text = engine.format_drifts(drifts)
        assert "STRENGTHENED" in text
        assert "Targets AI startups" in text
        assert "Applied to Kadoa" in text
