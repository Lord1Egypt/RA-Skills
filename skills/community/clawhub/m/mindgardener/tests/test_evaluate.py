"""Tests for the Context Evaluator — fact-checking + write-back."""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.config import EngramConfig
from engram.evaluate import (
    evaluate_output,
    write_back,
    _extract_claims,
    _check_claim_against_entity,
    FactCheck,
    EvaluationResult,
)


@pytest.fixture
def workspace(tmp_path):
    entities = tmp_path / "memory" / "entities"
    entities.mkdir(parents=True)
    memory = tmp_path / "memory"
    
    (entities / "Marcus.md").write_text(
        "# Marcus\n**Type:** person\n\n"
        "## Facts\n- Founder of the swarm project\n- Lives in Stockholm\n"
        "- Applied for CTO role at Sana Labs\n\n"
        "## Timeline\n\n### [[2026-02-16]]\n- Discussed MindGardener v2\n"
        "- Submitted PR to OpenClaw\n"
    )
    (entities / "Sana-Labs.md").write_text(
        "# Sana Labs\n**Type:** company\n\n"
        "## Facts\n- AI education company in Stockholm\n- Series B funded\n\n"
        "## Timeline\n\n### [[2026-02-15]]\n- Marcus applied for CTO position\n"
    )
    (entities / "MindGardener.md").write_text(
        "# MindGardener\n**Type:** project\n\n"
        "## Facts\n- File-based memory for AI agents\n- Uses surprise scoring\n"
        "- 12 CLI commands\n- 127 tests passing\n\n"
        "## Timeline\n\n### [[2026-02-17]]\n- Published to GitHub\n"
    )
    (entities / "OpenClaw.md").write_text(
        "# OpenClaw\n**Type:** project\n\n"
        "## Facts\n- Largest open-source AI agent framework\n- 200k stars on GitHub\n\n"
        "## Timeline\n"
    )
    
    return tmp_path


@pytest.fixture
def config(workspace):
    cfg = EngramConfig(workspace=workspace)
    return cfg.resolve()


class TestExtractClaims:
    def test_extracts_sentences_with_entities(self):
        text = "Marcus applied to Sana Labs. The weather is nice. OpenClaw has 200k stars."
        claims = _extract_claims(text)
        assert len(claims) >= 2
        assert any("Marcus" in c for c in claims)
        assert any("OpenClaw" in c for c in claims)
    
    def test_skips_short_text(self):
        claims = _extract_claims("Hi. Ok. Yes.")
        assert len(claims) == 0
    
    def test_skips_meta_commentary(self):
        claims = _extract_claims("Let me check that for you. I'll look into it.")
        assert len(claims) == 0
    
    def test_caps_at_20(self):
        text = "\n".join([f"Person{i} did something important number {i}" for i in range(30)])
        claims = _extract_claims(text)
        assert len(claims) <= 20


class TestCheckClaim:
    def test_confirmed_by_facts(self, workspace):
        entity_content = (workspace / "memory" / "entities" / "Marcus.md").read_text()
        fc = _check_claim_against_entity(
            "Marcus is the founder of the swarm project and lives in Stockholm",
            "Marcus", entity_content
        )
        assert fc.verdict == "confirmed"
        assert fc.confidence >= 0.5
    
    def test_confirmed_by_timeline(self, workspace):
        entity_content = (workspace / "memory" / "entities" / "Marcus.md").read_text()
        fc = _check_claim_against_entity(
            "Marcus submitted a PR to OpenClaw",
            "Marcus", entity_content
        )
        assert fc.verdict == "confirmed"
    
    def test_new_info(self, workspace):
        entity_content = (workspace / "memory" / "entities" / "Marcus.md").read_text()
        fc = _check_claim_against_entity(
            "Marcus recently started learning Rust programming",
            "Marcus", entity_content
        )
        assert fc.verdict == "new"
    
    def test_type_contradiction(self, workspace):
        entity_content = (workspace / "memory" / "entities" / "OpenClaw.md").read_text()
        fc = _check_claim_against_entity(
            "OpenClaw is a person who works at GitHub",
            "OpenClaw", entity_content
        )
        assert fc.verdict == "contradicted"
        assert "type" in fc.evidence.lower()


class TestEvaluateOutput:
    def test_basic_evaluation(self, config):
        output = "Marcus lives in Stockholm and founded the swarm project."
        result = evaluate_output(output, config)
        assert isinstance(result, EvaluationResult)
        assert result.overall_confidence > 0
        assert result.evaluated_at != ""
    
    def test_confirmed_claims_boost_confidence(self, config):
        output = "Marcus lives in Stockholm. He founded the swarm project. He applied for CTO at Sana Labs."
        result = evaluate_output(output, config)
        assert result.overall_confidence >= 0.5
        assert len(result.confirmed) > 0
    
    def test_contradicted_claims_lower_confidence(self, config):
        output = "OpenClaw is a person who lives in Berlin."
        result = evaluate_output(output, config)
        # Should have lower confidence due to type contradiction
        if result.contradicted:
            assert result.overall_confidence < 0.8
    
    def test_new_entity_detection(self, config):
        output = "Koylanai wrote a tweet about agent memory. Adrian Krebs replied."
        result = evaluate_output(output, config)
        detected_names = [ne["name"] for ne in result.new_entities]
        assert "Koylanai" in detected_names or "Adrian Krebs" in detected_names
    
    def test_empty_output(self, config):
        result = evaluate_output("", config)
        assert result.overall_confidence == 0.5
        assert len(result.fact_checks) == 0
    
    def test_summary_output(self, config):
        output = "Marcus founded the swarm project."
        result = evaluate_output(output, config)
        summary = result.summary()
        assert "Evaluation Summary" in summary
    
    def test_json_output(self, config):
        output = "Marcus lives in Stockholm."
        result = evaluate_output(output, config)
        j = result.to_json()
        assert "overall_confidence" in j
        assert isinstance(j["fact_checks"], list)


class TestWriteBack:
    def test_writes_new_facts(self, config):
        result = EvaluationResult(
            evaluated_at="2026-02-17",
            new_facts=[
                type('NewFact', (), {
                    'entity_name': 'Marcus',
                    'fact': 'Recently started learning Rust',
                    'confidence': 0.8,
                    'source_context': 'test',
                })()
            ],
        )
        # Use the actual NewFact
        from engram.evaluate import NewFact
        result.new_facts = [NewFact(
            entity_name="Marcus",
            fact="Recently started learning Rust",
            confidence=0.8,
        )]
        
        actions = write_back(result, config)
        assert any("ADDED" in a for a in actions)
        
        content = (config.entities_dir / "Marcus.md").read_text()
        assert "Rust" in content
        assert "auto-evaluated" in content
    
    def test_dry_run(self, config):
        from engram.evaluate import NewFact
        result = EvaluationResult(
            evaluated_at="2026-02-17",
            new_facts=[NewFact(
                entity_name="Marcus",
                fact="New fact for dry run",
                confidence=0.8,
            )],
        )
        
        actions = write_back(result, config, dry_run=True)
        assert any("WOULD ADD" in a for a in actions)
        
        content = (config.entities_dir / "Marcus.md").read_text()
        assert "dry run" not in content  # Not actually written
    
    def test_skips_low_confidence(self, config):
        from engram.evaluate import NewFact
        result = EvaluationResult(
            evaluated_at="2026-02-17",
            new_facts=[NewFact(
                entity_name="Marcus",
                fact="Unreliable claim",
                confidence=0.3,
            )],
        )
        
        actions = write_back(result, config, min_confidence=0.6)
        assert not any("ADDED" in a for a in actions)
    
    def test_skips_duplicate_facts(self, config):
        from engram.evaluate import NewFact
        result = EvaluationResult(
            evaluated_at="2026-02-17",
            new_facts=[NewFact(
                entity_name="Marcus",
                fact="Lives in Stockholm",  # Already exists
                confidence=0.9,
            )],
        )
        
        actions = write_back(result, config)
        assert any("already exists" in a for a in actions)
    
    def test_logs_evaluation(self, config):
        from engram.evaluate import NewFact
        result = EvaluationResult(
            evaluated_at="2026-02-17",
            overall_confidence=0.8,
            new_facts=[],
        )
        
        write_back(result, config)
        
        log_file = config.memory_dir / "evaluations.jsonl"
        assert log_file.exists()
        log = json.loads(log_file.read_text().strip())
        assert log["overall_confidence"] == 0.8
