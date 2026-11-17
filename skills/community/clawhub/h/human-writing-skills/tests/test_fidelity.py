import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.cli import main
from humanwriting.fidelity import compare_fidelity
from humanwriting.protection import extract_protected_items


class FidelityTests(unittest.TestCase):
    def test_exact_text_is_only_automatic_semantic_pass(self):
        source = "The intervention may improve adherence by 20% [1]."
        self.assertEqual(compare_fidelity(source, source).status, "pass-exact")
        self.assertEqual(
            compare_fidelity(source, "The intervention improves adherence by 20% [1].").status,
            "needs-review",
        )

    def test_uncertainty_and_attribution_cues_have_source_locations(self):
        source = "According to the study, treatment may reduce risk by 20% [1]."
        candidate = "Treatment reduces risk by 20% [1]."
        report = compare_fidelity(source, candidate)
        cues = [item for item in report.findings if item.kind == "anchored-signal-change"]
        self.assertTrue(cues)
        self.assertIn("uncertainty", cues[0].detail)
        self.assertIn("attribution", cues[0].detail)
        self.assertEqual(cues[0].source_line, 1)

    def test_chinese_adjacent_number_and_actor_swap(self):
        source = "A组的改善率为20%。B组无显著改善。"
        candidate = "B组的改善率为20%。A组无显著改善。"
        self.assertIn("20%", {item.value for item in extract_protected_items(source)})
        report = compare_fidelity(source, candidate)
        self.assertEqual(report.status, "needs-review")
        self.assertTrue(any("actor" in item.detail for item in report.findings))

    def test_scope_change_with_same_anchor_is_reviewed(self):
        report = compare_fidelity("Only some patients improved by 20% [1].", "All patients improved by 20% [1].")
        self.assertEqual(report.status, "needs-review")
        self.assertTrue(any("scope" in item.detail for item in report.findings))

    def test_literal_change_fails_and_cli_review_exit_is_distinct(self):
        source = "The rate may be 20% [1]."
        with TemporaryDirectory() as directory:
            original = Path(directory) / "original.md"
            revised = Path(directory) / "revised.md"
            original.write_text(source, encoding="utf-8")
            revised.write_text("The rate is 20% [1].", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                status = main([
                    "verify-fidelity", "--source", str(original), "--candidate", str(revised), "--format", "json"
                ])
            self.assertEqual(status, 2)
            self.assertEqual(json.loads(output.getvalue())["status"], "needs-review")
            revised.write_text("The rate is 25% [1].", encoding="utf-8")
            with redirect_stdout(StringIO()):
                status = main(["verify-fidelity", "--source", str(original), "--candidate", str(revised)])
            self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main()
