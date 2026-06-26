"""Tests for escalation.py — Confidence detection and retry logic."""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from escalation import EscalationEngine, EscalationLevel, check_escalation


class TestEscalationLowConfidence(unittest.TestCase):
    """Tests for low-confidence response detection."""

    def test_i_dont_know_triggers_escalation(self):
        result = check_escalation("I don't know the answer to that question")
        self.assertTrue(result.should_escalate)
        self.assertLess(result.confidence, 0.7)

    def test_not_sure_triggers_escalation(self):
        result = check_escalation("I am not sure about this")
        self.assertTrue(result.should_escalate)

    def test_cannot_determine_triggers_escalation(self):
        result = check_escalation("I cannot determine the cause of this issue")
        self.assertTrue(result.should_escalate)

    def test_insufficient_information_triggers_escalation(self):
        result = check_escalation("There is insufficient information to answer this")
        self.assertTrue(result.should_escalate)

    def test_unclear_triggers_escalation(self):
        result = check_escalation("The answer is unclear based on available data")
        self.assertTrue(result.should_escalate)

    def test_cannot_provide_triggers_escalation(self):
        result = check_escalation("I cannot provide a definitive answer")
        self.assertTrue(result.should_escalate)


class TestEscalationHighConfidence(unittest.TestCase):
    """Tests for high-confidence responses (no escalation needed)."""

    def test_confident_response_no_escalation(self):
        result = check_escalation(
            "The function sorts the list in O(n log n) time using merge sort. "
            "Here's the implementation..."
        )
        self.assertFalse(result.should_escalate)
        self.assertGreaterEqual(result.confidence, 0.7)

    def test_factual_response_no_escalation(self):
        result = check_escalation(
            "Python 3.12 was released in October 2023 with improved error messages."
        )
        self.assertFalse(result.should_escalate)

    def test_clear_explanation_no_escalation(self):
        result = check_escalation(
            "To fix this, you need to update the dependency version in package.json "
            "and then run npm install again."
        )
        self.assertFalse(result.should_escalate)


class TestEscalationChain(unittest.TestCase):
    """Tests for escalation chain progression."""

    def test_level_0_escalates_to_level_1(self):
        result = check_escalation(
            "I don't know the answer",
            current_model_key="qwen3-14b",
            current_level=0,
        )
        self.assertTrue(result.should_escalate)
        self.assertEqual(result.escalation_level, EscalationLevel.LEVEL_0)
        # Should escalate to deepseek-r1 (level 1)
        self.assertEqual(result.next_model_key, "deepseek-r1")

    def test_level_1_escalates_to_level_2(self):
        result = check_escalation(
            "I am not sure about this either",
            current_model_key="deepseek-r1",
            current_level=1,
        )
        self.assertTrue(result.should_escalate)
        # Should escalate to glm-5-1-cloud (level 2)
        self.assertEqual(result.next_model_key, "glm-5-1-cloud")

    def test_level_2_no_further_escalation(self):
        result = check_escalation(
            "I still don't know",
            current_model_key="glm-5-1-cloud",
            current_level=2,
        )
        # Max retries reached (2), no further escalation
        self.assertFalse(result.should_escalate)

    def test_level_1_with_confident_response_no_escalation(self):
        result = check_escalation(
            "Here's the solution: update the config file and restart the service.",
            current_model_key="deepseek-r1",
            current_level=1,
        )
        self.assertFalse(result.should_escalate)


class TestEscalationConfidenceScoring(unittest.TestCase):
    """Tests for confidence scoring in escalation."""

    def test_zero_patterns_high_confidence(self):
        result = check_escalation("This is a clear and definitive answer.")
        self.assertEqual(result.confidence, 1.0)

    def test_one_pattern_medium_confidence(self):
        result = check_escalation("I don't know the answer")
        self.assertEqual(result.confidence, 0.5)

    def test_two_patterns_lower_confidence(self):
        result = check_escalation("I don't know, and I am not sure about this")
        self.assertEqual(result.confidence, 0.3)

    def test_three_plus_patterns_very_low_confidence(self):
        result = check_escalation(
            "I don't know, I am not sure, and I cannot determine the answer"
        )
        self.assertLessEqual(result.confidence, 0.1)


class TestEscalationResultFormat(unittest.TestCase):
    """Tests for EscalationResult formatting."""

    def test_escalate_result_string(self):
        result = check_escalation("I don't know")
        if result.should_escalate:
            self.assertIn("ESCALATE", str(result))
            self.assertIn("level=", str(result))

    def test_ok_result_string(self):
        result = check_escalation("Here's a clear answer to your question.")
        if not result.should_escalate:
            self.assertIn("OK", str(result))
            self.assertIn("confidence=", str(result))


class TestEscalationEdgeCases(unittest.TestCase):
    """Tests for edge cases in escalation."""

    def test_empty_response(self):
        result = check_escalation("")
        # Empty response — no patterns, high confidence
        self.assertFalse(result.should_escalate)

    def test_none_like_response(self):
        result = check_escalation("None of the above options work")
        # "None" shouldn't match "I don't know" patterns
        # This should be a normal response
        self.assertGreaterEqual(result.confidence, 0.7)

    def test_mixed_response(self):
        """Response with both confident and uncertain language."""
        result = check_escalation(
            "The primary cause is X. However, I am not sure about the secondary factor."
        )
        # Should detect the uncertainty and escalate
        self.assertTrue(result.should_escalate or result.confidence < 1.0)


if __name__ == "__main__":
    unittest.main()