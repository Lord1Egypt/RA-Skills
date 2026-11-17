import json
import unittest
from pathlib import Path

from humanwriting.linter import lint_text


ROOT = Path(__file__).resolve().parent.parent


class QualityFixtureTests(unittest.TestCase):
    def test_template_shaped_fixture_scores_above_concrete_reference(self):
        reference = (ROOT / "examples" / "reference-style-source.zh-CN.md").read_text(
            encoding="utf-8"
        )
        draft = (ROOT / "examples" / "reference-style-draft.zh-CN.md").read_text(
            encoding="utf-8"
        )
        reference_report = lint_text(reference, style="fiction")
        draft_report = lint_text(draft, style="fiction")

        self.assertGreater(draft_report.score, reference_report.score)
        self.assertTrue({"LEX002", "EMO001"} <= {item.rule_id for item in draft_report.findings})

    def test_cross_genre_calibration_cases_rank_template_text_higher(self):
        cases = json.loads(
            (ROOT / "tests" / "fixtures" / "quality" / "calibration-cases.json").read_text(
                encoding="utf-8"
            )
        )
        for case in cases:
            with self.subTest(case=case["name"]):
                natural = lint_text(case["natural"], style=case["style"])
                template = lint_text(case["template"], style=case["style"])
                self.assertGreater(template.score, natural.score)
                self.assertTrue(
                    set(case["expected"]) <= {finding.rule_id for finding in template.findings}
                )


if __name__ == "__main__":
    unittest.main()
