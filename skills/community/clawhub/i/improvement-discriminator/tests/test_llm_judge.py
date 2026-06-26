#!/usr/bin/env python3
"""Tests for the LLM-as-Judge module and its integration with score.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repo root and scripts/ are importable
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPTS_DIR = str(Path(__file__).resolve().parents[1] / "scripts")
_INTERFACES_DIR = str(Path(__file__).resolve().parents[1] / "interfaces")
_GATE_SCRIPTS_DIR = str(_REPO_ROOT / "skills" / "improvement-gate" / "scripts")
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
if _INTERFACES_DIR not in sys.path:
    sys.path.insert(0, _INTERFACES_DIR)
if _GATE_SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _GATE_SCRIPTS_DIR)

import pytest

from llm_judge import JudgeConfig, JudgeVerdict, LLMJudge, JUDGE_PROMPT_TEMPLATE
from score import score_candidate


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_candidate(
    *,
    category: str = "docs",
    risk_level: str = "low",
    executor_support: bool = True,
    target_path: str = "/tmp/fake-skill/references/foo.md",
    source_refs: list | None = None,
    content_lines: list[str] | None = None,
) -> dict:
    """Build a minimal candidate dict suitable for scoring and LLM judging."""
    plan = {"action": "append_markdown_section"}
    if content_lines is not None:
        plan["content_lines"] = content_lines
    return {
        "id": "test-llm-001",
        "title": "Test candidate for LLM judge",
        "category": category,
        "risk_level": risk_level,
        "executor_support": executor_support,
        "target_path": target_path,
        "source_refs": source_refs or ["/some/ref.md"],
        "execution_plan": plan,
        "proposed_change_summary": "Add section X to references",
    }


# ---------------------------------------------------------------------------
# JudgeVerdict dataclass
# ---------------------------------------------------------------------------


class TestJudgeVerdict:
    """JudgeVerdict should hold structured verdict data."""

    def test_defaults(self):
        v = JudgeVerdict(score=0.7, decision="approve", reasoning="ok")
        assert v.score == 0.7
        assert v.decision == "approve"
        assert v.reasoning == "ok"
        assert v.confidence == 0.8
        assert v.dimensions == {}
        assert v.suggestions == []

    def test_with_dimensions(self):
        v = JudgeVerdict(
            score=0.5,
            decision="conditional",
            reasoning="needs work",
            dimensions={"clarity": 0.6, "safety": 0.4},
            confidence=0.3,
            suggestions=["be more specific"],
        )
        assert v.dimensions["clarity"] == 0.6
        assert len(v.suggestions) == 1


# ---------------------------------------------------------------------------
# JudgeConfig
# ---------------------------------------------------------------------------


class TestJudgeConfig:
    def test_defaults(self):
        cfg = JudgeConfig()
        assert cfg.backend == "mock"
        assert cfg.temperature == 0.0
        assert cfg.approve_threshold == 0.75
        assert cfg.reject_threshold == 0.40
        assert "clarity" in cfg.dimensions

    def test_custom_backend(self):
        cfg = JudgeConfig(backend="claude", model="claude-opus-4-20250514")
        assert cfg.backend == "claude"
        assert cfg.model == "claude-opus-4-20250514"


# ---------------------------------------------------------------------------
# LLMJudge._build_prompt
# ---------------------------------------------------------------------------


class TestBuildPrompt:
    def test_contains_candidate_info(self):
        judge = LLMJudge()
        candidate = _make_candidate(
            category="guardrail",
            risk_level="medium",
            content_lines=["## New guardrail", "Never do X"],
        )
        prompt = judge._build_prompt(candidate, target_content="# Existing Skill")
        assert "guardrail" in prompt
        assert "medium" in prompt
        assert "## New guardrail" in prompt
        assert "# Existing Skill" in prompt

    def test_no_content_lines(self):
        judge = LLMJudge()
        candidate = _make_candidate()
        prompt = judge._build_prompt(candidate, target_content="")
        assert "(no content specified)" in prompt

    def test_target_content_truncation(self):
        judge = LLMJudge()
        candidate = _make_candidate()
        long_content = "A" * 5000
        prompt = judge._build_prompt(candidate, target_content=long_content)
        # Should truncate to 2000 chars
        assert "A" * 2000 in prompt
        assert "A" * 2001 not in prompt


# ---------------------------------------------------------------------------
# LLMJudge._parse_response
# ---------------------------------------------------------------------------


class TestParseResponse:
    def test_valid_json(self):
        judge = LLMJudge()
        raw = json.dumps({
            "clarity": 0.9,
            "specificity": 0.85,
            "consistency": 0.8,
            "safety": 0.95,
            "overall": 0.88,
            "decision": "approve",
            "reasoning": "Good change.",
            "suggestions": [],
        })
        verdict = judge._parse_response(raw)
        assert verdict.score == 0.88
        assert verdict.decision == "approve"
        assert verdict.dimensions["clarity"] == 0.9
        assert verdict.confidence == 0.5  # mock backend

    def test_markdown_wrapped_json(self):
        judge = LLMJudge()
        raw = '```json\n{"clarity": 0.7, "specificity": 0.6, "consistency": 0.5, "safety": 0.8, "overall": 0.65, "decision": "conditional", "reasoning": "Needs work.", "suggestions": ["add examples"]}\n```'
        verdict = judge._parse_response(raw)
        assert verdict.score == 0.65
        assert verdict.decision == "conditional"
        assert "add examples" in verdict.suggestions

    def test_generic_code_block(self):
        judge = LLMJudge()
        raw = '```\n{"clarity": 0.8, "specificity": 0.7, "consistency": 0.6, "safety": 0.9, "overall": 0.75, "decision": "approve", "reasoning": "ok", "suggestions": []}\n```'
        verdict = judge._parse_response(raw)
        assert verdict.score == 0.75
        assert verdict.decision == "approve"

    def test_invalid_json_fallback(self):
        judge = LLMJudge()
        verdict = judge._parse_response("This is not JSON at all!")
        assert verdict.score == 0.5
        assert verdict.decision == "conditional"
        assert verdict.confidence == 0.2
        assert "Parse error" in verdict.reasoning
        assert len(verdict.suggestions) == 1

    def test_threshold_override_approve(self):
        """If overall >= approve_threshold, decision should be overridden to approve."""
        judge = LLMJudge(JudgeConfig(approve_threshold=0.6))
        raw = json.dumps({
            "clarity": 0.8,
            "specificity": 0.7,
            "consistency": 0.6,
            "safety": 0.9,
            "overall": 0.75,
            "decision": "conditional",  # LLM said conditional, but overall >= 0.6
            "reasoning": "ok",
            "suggestions": [],
        })
        verdict = judge._parse_response(raw)
        assert verdict.decision == "approve"

    def test_threshold_override_reject(self):
        """If overall < reject_threshold, decision should be overridden to reject."""
        judge = LLMJudge(JudgeConfig(reject_threshold=0.5))
        raw = json.dumps({
            "clarity": 0.3,
            "specificity": 0.2,
            "consistency": 0.4,
            "safety": 0.5,
            "overall": 0.35,
            "decision": "conditional",  # LLM said conditional, but overall < 0.5
            "reasoning": "bad",
            "suggestions": [],
        })
        verdict = judge._parse_response(raw)
        assert verdict.decision == "reject"


# ---------------------------------------------------------------------------
# LLMJudge mock backend scoring logic
# ---------------------------------------------------------------------------


class TestMockBackend:
    """The mock backend should produce deterministic scores based on prompt content."""

    def test_docs_low_risk_with_content_approve(self):
        """docs + low_risk + has content -> approve."""
        judge = LLMJudge()
        candidate = _make_candidate(
            category="docs",
            risk_level="low",
            content_lines=["## Added section", "Details here"],
        )
        verdict = judge.evaluate(candidate)
        assert verdict.decision == "approve"
        assert verdict.score >= 0.75

    def test_no_content_conditional(self):
        """No content lines -> conditional or reject."""
        judge = LLMJudge()
        candidate = _make_candidate(category="workflow", risk_level="medium")
        verdict = judge.evaluate(candidate)
        assert verdict.decision in ("conditional", "reject")
        assert verdict.score < 0.75

    def test_high_risk_no_content_reject(self):
        """High risk + no content -> reject."""
        judge = LLMJudge()
        candidate = _make_candidate(category="prompt", risk_level="high")
        # No content_lines, not docs, not low risk
        verdict = judge.evaluate(candidate)
        assert verdict.decision in ("conditional", "reject")
        assert verdict.score < 0.75

    def test_mock_confidence_is_low(self):
        """Mock backend should return confidence=0.5."""
        judge = LLMJudge()
        candidate = _make_candidate()
        verdict = judge.evaluate(candidate)
        assert verdict.confidence == 0.5


# ---------------------------------------------------------------------------
# LLMJudge.evaluate_batch
# ---------------------------------------------------------------------------


class TestEvaluateBatch:
    def test_batch_returns_list(self):
        judge = LLMJudge()
        candidates = [
            _make_candidate(category="docs", content_lines=["line1"]),
            _make_candidate(category="workflow"),
            _make_candidate(category="reference", content_lines=["ref content"]),
        ]
        verdicts = judge.evaluate_batch(candidates)
        assert len(verdicts) == 3
        assert all(isinstance(v, JudgeVerdict) for v in verdicts)

    def test_batch_different_scores(self):
        """Different candidates should get different scores (docs+content vs workflow+none)."""
        judge = LLMJudge()
        good = _make_candidate(category="docs", risk_level="low", content_lines=["content"])
        bad = _make_candidate(category="prompt", risk_level="high")
        verdicts = judge.evaluate_batch([good, bad])
        assert verdicts[0].score > verdicts[1].score


# ---------------------------------------------------------------------------
# Integration with score.py
# ---------------------------------------------------------------------------


class TestScoreIntegration:
    """Test LLM judge integration into score_candidate."""

    def test_score_with_llm_judge_enabled(self):
        judge = LLMJudge()
        candidate = _make_candidate(
            category="docs",
            risk_level="low",
            content_lines=["## New section", "Content here"],
        )
        result = score_candidate(candidate, llm_judge=judge)
        assert "llm_verdict" in result
        assert result["llm_verdict"]["decision"] in ("approve", "conditional", "reject")
        assert result["judge_adapter"]["llm_judge_enabled"] is True
        assert "score_components" in result
        assert "llm_weight" in result["score_components"]

    def test_score_without_llm_judge(self):
        candidate = _make_candidate()
        result = score_candidate(candidate)
        assert "llm_verdict" not in result
        assert result["judge_adapter"]["llm_judge_enabled"] is False

    def test_llm_reject_adds_blocker(self):
        """When LLM says reject, 'llm_judge_reject' should appear in blockers."""
        # Use a config with very high reject threshold to force reject
        judge = LLMJudge(JudgeConfig(approve_threshold=0.99, reject_threshold=0.99))
        candidate = _make_candidate(category="prompt", risk_level="high")
        result = score_candidate(candidate, llm_judge=judge)
        # The mock for high risk + no docs + no content should score low
        # and the reject threshold of 0.99 means everything gets rejected
        assert "llm_judge_reject" in result["blockers"]

    def test_blended_score_heuristic_plus_llm(self):
        """Score should be a blend of heuristic (0.6) and LLM (0.4)."""
        judge = LLMJudge()
        candidate = _make_candidate(
            category="docs",
            risk_level="low",
            content_lines=["content"],
        )
        result = score_candidate(candidate, llm_judge=judge)
        components = result["score_components"]
        assert components["heuristic_weight"] == 0.3
        assert components["llm_weight"] == 0.7

    def test_adapter_name_with_llm(self):
        judge = LLMJudge()
        candidate = _make_candidate()
        result = score_candidate(candidate, llm_judge=judge)
        assert result["judge_adapter"]["name"] == "heuristic+llm-judge"

    def test_adapter_name_with_llm_and_evaluator(self):
        judge = LLMJudge()
        candidate = _make_candidate()
        result = score_candidate(candidate, llm_judge=judge, use_evaluator_evidence=True)
        assert result["judge_adapter"]["name"] == "heuristic+evaluator+llm-judge"


# ---------------------------------------------------------------------------
# Gate ReviewGate integration
# ---------------------------------------------------------------------------


class TestReviewGateWithLLMVerdict:
    """Test that ReviewGate checks llm_verdict correctly."""

    def test_llm_reject_fails_gate(self):
        from gate import ReviewGate

        gate = ReviewGate()
        candidate = {
            "recommendation": "accept_for_execution",
            "llm_verdict": {"decision": "reject", "confidence": 0.9},
        }
        result = gate.validate(candidate)
        assert result["passed"] is False
        assert "LLM judge: reject" in result["details"]

    def test_llm_conditional_high_confidence_passes(self):
        from gate import ReviewGate

        gate = ReviewGate()
        candidate = {
            "recommendation": "accept_for_execution",
            "panel_result": {"cognitive_label": "CONSENSUS"},
            "llm_verdict": {"decision": "conditional", "confidence": 0.85},
        }
        result = gate.validate(candidate)
        assert result["passed"] is True
        assert "LLM conditional" in result["details"]

    def test_no_llm_verdict_passes_normally(self):
        from gate import ReviewGate

        gate = ReviewGate()
        candidate = {
            "recommendation": "accept_for_execution",
            "panel_result": {"cognitive_label": "CONSENSUS"},
        }
        result = gate.validate(candidate)
        assert result["passed"] is True

    def test_disputed_with_llm_reject(self):
        """DISPUTED + LLM reject should fail."""
        from gate import ReviewGate

        gate = ReviewGate()
        candidate = {
            "recommendation": "hold",
            "panel_result": {"cognitive_label": "DISPUTED"},
            "llm_verdict": {"decision": "reject", "confidence": 0.9},
        }
        result = gate.validate(candidate)
        assert result["passed"] is False
