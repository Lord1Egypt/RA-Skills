import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.cli import main
from humanwriting.fixer import build_fix_report, format_fix_report


class FixerTests(unittest.TestCase):
    def test_preview_removes_only_mechanical_artifacts(self):
        text = "值得注意的是，数据仍不完整。希望这对你有所帮助。"
        report = build_fix_report(text)
        self.assertEqual(len(report.edits), 2)
        self.assertEqual(report.candidate, "数据仍不完整。")

    def test_preview_removes_pseudo_objective_fillers(self):
        text = "不可否认的是，方案仍需完善。It is undeniable that results improved."
        report = build_fix_report(text)
        self.assertEqual(len(report.edits), 2)
        self.assertEqual(report.candidate, "方案仍需完善。results improved.")

    def test_preview_does_not_rewrite_comparisons_or_claims(self):
        text = "走廊比昨夜更窄，比记忆里更长。约有一半人不确定。"
        report = build_fix_report(text)
        self.assertEqual(report.edits, ())
        self.assertEqual(report.candidate, text)

    def test_json_output_contains_candidate_and_spans(self):
        payload = json.loads(format_fix_report(build_fix_report("In order to test, wait."), "json"))
        self.assertEqual(payload["candidate"], "to test, wait.")
        self.assertIn("start", payload["edits"][0])

    def test_cli_fix_previews_by_default_and_writes_only_with_output(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            output = Path(directory) / "cleaned.md"
            draft.write_text("值得注意的是，结论有限。", encoding="utf-8")
            stdout = StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(main(["fix", "--draft", str(draft)]), 0)
            self.assertEqual(draft.read_text(encoding="utf-8"), "值得注意的是，结论有限。")
            self.assertIn("结论有限。", stdout.getvalue())
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    main(["fix", "--draft", str(draft), "--output", str(output)]), 0
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "结论有限。")


if __name__ == "__main__":
    unittest.main()
