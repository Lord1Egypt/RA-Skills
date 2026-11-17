import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from jev_control import (  # noqa: E402
    ControlInputError,
    assess_tool_call,
    judge_typed_answers,
    route_choice,
)


class JevControlTests(unittest.TestCase):
    def test_route_uses_distribution_and_margin_not_reported_confidence(self):
        result = route_choice(
            {
                "answers": {
                    "complexity": {
                        "type": "choice",
                        "choice": "fast",
                        "confidence": 0.99,
                        "probabilities": {"fast": 0.76, "strong": 0.24},
                    }
                }
            },
            {"fast": "cheap-model", "strong": "strong-model"},
            question_id="complexity",
            min_confidence=0.75,
            min_margin=0.10,
        )
        self.assertEqual(result["status"], "route")
        self.assertEqual(result["route"], "cheap-model")
        self.assertAlmostEqual(result["confidence"], 0.76)

    def test_route_abstains_on_close_runner_up(self):
        result = route_choice(
            {
                "type": "choice",
                "choice": "fast",
                "probabilities": {"fast": 0.81, "strong": 0.19},
            },
            {"fast": "cheap-model", "strong": "strong-model"},
            min_confidence=0.80,
            min_margin=0.70,
        )
        self.assertEqual(result["status"], "review")
        self.assertEqual(result["route"], "review")
        self.assertTrue(any("margin" in reason for reason in result["reasons"]))

    def test_route_rejects_distribution_that_does_not_sum_to_one(self):
        with self.assertRaises(ControlInputError):
            route_choice(
                {
                    "type": "choice",
                    "choice": "fast",
                    "probabilities": {"fast": 0.8, "strong": 0.8},
                },
                {"fast": "cheap-model", "strong": "strong-model"},
            )

    def test_protected_tool_requires_deterministic_authorization(self):
        result = assess_tool_call(
            "delete_database",
            {"type": "noul", "noul": 0.10},
            protected_tools={"delete_database"},
            authorized=False,
        )
        self.assertEqual(result["decision"], "review")

    def test_high_risk_tool_is_blocked_even_when_authorized(self):
        result = assess_tool_call(
            "delete_database",
            {"type": "noul", "noul": 0.90},
            protected_tools={"delete_database"},
            authorized=True,
        )
        self.assertEqual(result["decision"], "block")

    def test_tool_classifier_failure_is_fail_closed(self):
        result = assess_tool_call(
            "bash",
            None,
            protected_tools={"bash"},
            authorized=True,
            classifier_error="timeout",
        )
        self.assertEqual(result["decision"], "block")

    def test_unlisted_tool_defaults_to_review(self):
        result = assess_tool_call(
            "read_file",
            {"type": "noul", "noul": 0.01},
            protected_tools={"bash"},
            authorized=True,
        )
        self.assertEqual(result["decision"], "review")

    def test_rubric_judge_accepts_weighted_typed_criteria(self):
        result = judge_typed_answers(
            {
                "answers": {
                    "correct": {"type": "noul", "noul": 0.95},
                    "grounded": {"type": "noul", "noul": 0.85},
                    "citation": {"type": "choice", "choice": "present", "probabilities": {"present": 0.9, "missing": 0.1}},
                }
            },
            {
                "correct": {"type": "noul", "threshold": 0.8, "weight": 2},
                "grounded": {"type": "noul", "threshold": 0.8},
                "citation": {"type": "choice", "expected": "present", "threshold": 0.8},
            },
        )
        self.assertEqual(result["decision"], "accept")
        self.assertEqual(result["passed"], 3)
        self.assertEqual(result["total"], 3)

    def test_rubric_judge_reviews_partial_result(self):
        result = judge_typed_answers(
            {
                "good": {"type": "noul", "noul": 0.9},
                "grounded": {"type": "noul", "noul": 0.2},
            },
            {
                "good": {"type": "noul", "threshold": 0.8},
                "grounded": {"type": "noul", "threshold": 0.8},
            },
            accept_threshold=0.8,
            review_threshold=0.4,
        )
        self.assertEqual(result["decision"], "review")
        self.assertAlmostEqual(result["score"], 0.55)


if __name__ == "__main__":
    unittest.main()
