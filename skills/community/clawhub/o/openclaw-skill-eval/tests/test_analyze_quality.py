"""
Unit tests for analyze_quality.py
"""
import json
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from analyze_quality import (
    score_against_assertions,
    estimate_quality_score,
    analyze_quality,
)


class TestScoreAgainstAssertions:
    """Tests for assertion matching logic."""

    def test_all_assertions_pass(self):
        """Should detect all matching assertions."""
        transcript = "The weather in Singapore is sunny with temperature 32C."
        assertions = ["weather", "Singapore", "temperature"]

        result = score_against_assertions(transcript, assertions)

        assert result["passed"] == 3
        assert result["total"] == 3
        assert result["pass_rate"] == 1.0

    def test_partial_assertions_pass(self):
        """Should correctly count partial matches."""
        transcript = "The weather is sunny."
        assertions = ["weather", "Singapore", "rain"]

        result = score_against_assertions(transcript, assertions)

        assert result["passed"] == 1  # only "weather" matches
        assert result["total"] == 3
        assert result["pass_rate"] == 0.33

    def test_no_assertions(self):
        """Should handle empty assertion list."""
        result = score_against_assertions("some text", [])

        assert result["passed"] == 0
        assert result["total"] == 0

    def test_case_insensitive(self):
        """Should match case-insensitively."""
        transcript = "WEATHER forecast for SINGAPORE"
        assertions = ["weather", "singapore"]

        result = score_against_assertions(transcript, assertions)

        assert result["passed"] == 2

    def test_filters_short_words(self):
        """Should ignore short words (<=3 chars) in assertions."""
        transcript = "Get the forecast"
        assertions = ["get the forecast"]  # "get" and "the" should be filtered

        result = score_against_assertions(transcript, assertions)

        # "forecast" (7 chars) should match, "get" (3) and "the" (3) filtered
        assert result["passed"] == 1


class TestEstimateQualityScore:
    """Tests for heuristic quality scoring."""

    def test_baseline_score(self):
        """Basic non-empty transcript should get baseline score."""
        transcript = "A" * 100
        assertions_result = {"pass_rate": 0}

        score = estimate_quality_score(transcript, assertions_result)

        assert 4.0 <= score <= 6.0  # Baseline + small length bonus

    def test_empty_transcript_zero(self):
        """Empty transcript should score 0."""
        score = estimate_quality_score("", {"pass_rate": 0})
        assert score == 0.0

    def test_high_assertion_pass_rate_bonus(self):
        """High assertion pass rate should increase score."""
        transcript = "A" * 200
        low_pass = estimate_quality_score(transcript, {"pass_rate": 0})
        high_pass = estimate_quality_score(transcript, {"pass_rate": 1.0})

        assert high_pass > low_pass
        assert high_pass - low_pass >= 2.5  # Should get significant bonus

    def test_length_bonus(self):
        """Longer transcripts should get bonus."""
        short = estimate_quality_score("A" * 100, {"pass_rate": 0.5})
        medium = estimate_quality_score("A" * 600, {"pass_rate": 0.5})
        long = estimate_quality_score("A" * 1200, {"pass_rate": 0.5})

        assert medium > short
        assert long > medium

    def test_error_penalty(self):
        """Error keywords should reduce score."""
        clean = estimate_quality_score("A" * 200, {"pass_rate": 0.5})
        error = estimate_quality_score("Error occurred " + "A" * 185, {"pass_rate": 0.5})

        assert error < clean

    def test_score_capped_at_10(self):
        """Score should never exceed 10."""
        transcript = "A" * 2000  # Very long
        score = estimate_quality_score(transcript, {"pass_rate": 1.0})

        assert score <= 10.0

    def test_score_minimum_zero(self):
        """Score should never go below 0."""
        transcript = "error failed cannot unable to"  # All penalty words
        score = estimate_quality_score(transcript, {"pass_rate": 0})

        assert score >= 0.0


class TestAnalyzeQuality:
    """Integration tests for full quality analysis."""

    def test_full_analysis(self, tmp_path):
        """Test complete quality analysis workflow."""
        # Create evals file
        evals_data = {
            "skill_name": "test-skill",
            "evals": [
                {
                    "id": 1,
                    "name": "basic-test",
                    "assertions": ["weather", "temperature"]
                },
            ]
        }
        evals_file = tmp_path / "evals.json"
        evals_file.write_text(json.dumps(evals_data))

        # Create transcripts directory
        transcripts_dir = tmp_path / "transcripts"
        transcripts_dir.mkdir()

        # With skill: good response
        with_transcript = "The weather in Singapore is 32C temperature with sunny skies."
        (transcripts_dir / "eval-1-with.txt").write_text(with_transcript)

        # Without skill: poor response
        without_transcript = "I don't know."
        (transcripts_dir / "eval-1-without.txt").write_text(without_transcript)

        output_file = tmp_path / "results.json"

        # Run analysis
        result = analyze_quality(
            evals_file=str(evals_file),
            transcripts_dir=str(transcripts_dir),
            output_file=str(output_file),
        )

        # Check results
        assert result["skill_name"] == "test-skill"
        assert len(result["results"]) == 1

        eval_result = result["results"][0]
        assert eval_result["with_skill"]["quality_score"] > eval_result["without_skill"]["quality_score"]
        assert eval_result["delta"] > 0
        assert eval_result["skill_helps"] is True

        # Check output file
        assert output_file.exists()

    def test_missing_transcripts(self, tmp_path):
        """Should handle missing transcript files gracefully."""
        evals_data = {
            "skill_name": "test-skill",
            "evals": [
                {"id": 1, "name": "test1", "assertions": []},
                {"id": 999, "name": "missing", "assertions": []},  # No transcript
            ]
        }
        evals_file = tmp_path / "evals.json"
        evals_file.write_text(json.dumps(evals_data))

        transcripts_dir = tmp_path / "transcripts"
        transcripts_dir.mkdir()

        # Only create transcripts for eval-1
        (transcripts_dir / "eval-1-with.txt").write_text("some response")
        (transcripts_dir / "eval-1-without.txt").write_text("another response")

        output_file = tmp_path / "results.json"

        result = analyze_quality(
            evals_file=str(evals_file),
            transcripts_dir=str(transcripts_dir),
            output_file=str(output_file),
        )

        # Should only have 1 result (eval-999 skipped)
        assert len(result["results"]) == 1

    def test_skill_hurts_detection(self, tmp_path):
        """Should detect when skill makes things worse."""
        evals_data = {
            "skill_name": "bad-skill",
            "evals": [{"id": 1, "name": "test", "assertions": ["answer"]}]
        }
        evals_file = tmp_path / "evals.json"
        evals_file.write_text(json.dumps(evals_data))

        transcripts_dir = tmp_path / "transcripts"
        transcripts_dir.mkdir()

        # With skill: bad response with errors
        (transcripts_dir / "eval-1-with.txt").write_text("Error: cannot process")

        # Without skill: good response
        (transcripts_dir / "eval-1-without.txt").write_text(
            "Here is the answer you requested with detailed explanation."
        )

        output_file = tmp_path / "results.json"

        result = analyze_quality(
            evals_file=str(evals_file),
            transcripts_dir=str(transcripts_dir),
            output_file=str(output_file),
        )

        eval_result = result["results"][0]
        assert eval_result["delta"] < 0
        assert eval_result["skill_helps"] is False
