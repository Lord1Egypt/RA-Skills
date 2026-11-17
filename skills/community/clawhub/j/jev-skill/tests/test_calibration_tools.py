import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compare_reports import comparable_identity  # noqa: E402
from fit_calibration import build_profile  # noqa: E402


class CalibrationToolTests(unittest.TestCase):
    def test_fit_profile_is_bound_to_provider_model_and_questions(self):
        report = {
            "config": {
                "provider": "von",
                "model": "von-latest",
                "question_sha256": "questions-hash",
                "case_sha256": "cases-hash",
            },
            "records": [
                {
                    "ok": True,
                    "tags": ["calibration"],
                    "answers": {
                        "urgent": {"type": "noul", "noul": 0.9},
                        "team": {"type": "choice", "choice": "billing", "probabilities": {"billing": 0.8, "other": 0.2}},
                        "severity": {"type": "score", "score": 1.6, "probabilities": {"0": 0.1, "1": 0.2, "2": 0.7}},
                    },
                    "evaluations": [
                        {"id": "urgent", "type": "noul", "expected": True},
                        {"id": "team", "type": "choice", "expected": "billing"},
                        {"id": "severity", "type": "score", "expected_level": 2.0},
                    ],
                }
            ],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(report, handle)
            report_path = Path(handle.name)
        try:
            profile = build_profile(report, report_path, fit_tag="calibration", minimum_samples=1, by_question=True)
        finally:
            report_path.unlink()
        self.assertEqual(profile["schema_version"], "jev-calibration-v1")
        self.assertEqual(profile["source"]["provider"], "von")
        self.assertIn("noul", profile["temperatures"])
        self.assertIn("severity", profile["by_question"])

    def test_comparison_identity_includes_case_manifest_and_tag_filter(self):
        first = {"config": {"question_sha256": "q", "case_sha256": "c", "tag_filter": ["golden"]}}
        second = {"config": {"question_sha256": "q", "case_sha256": "c", "tag_filter": ["golden"]}}
        different = {"config": {"question_sha256": "q", "case_sha256": "other", "tag_filter": ["golden"]}}
        self.assertEqual(comparable_identity(first), comparable_identity(second))
        self.assertNotEqual(comparable_identity(first), comparable_identity(different))


if __name__ == "__main__":
    unittest.main()
