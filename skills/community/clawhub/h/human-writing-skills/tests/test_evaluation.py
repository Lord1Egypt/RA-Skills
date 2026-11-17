import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.cli import main
from humanwriting.evaluation import evaluate_cases


CASES = Path(__file__).parent / "fixtures" / "quality" / "multilingual-benchmark.json"


class EvaluationTests(unittest.TestCase):
    def test_seed_benchmark_is_explicitly_not_native_validation(self):
        result = evaluate_cases(str(CASES))
        self.assertEqual(result["groups"]["seed"]["total"], 21)
        self.assertEqual(result["groups"]["native-reviewed"]["total"], 0)
        self.assertEqual(result["groups"]["seed"]["serious_detection"]["fp"], 0)
        self.assertEqual(result["groups"]["seed"]["serious_detection"]["fn"], 0)
        self.assertEqual(result["groups"]["seed"]["passed"], 21)
        self.assertIn("fr / academic / seed", result["strata"])

    def test_cli_evaluate_json(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["evaluate", "--cases", str(CASES), "--format", "json"])
        self.assertEqual(status, 0)
        self.assertIn("strata", json.loads(output.getvalue()))

    def test_native_review_label_requires_provenance(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cases.json"
            path.write_text(json.dumps([{
                "id": "unattributed", "kind": "serious-detection", "language": "fr", "genre": "news",
                "review_status": "native-reviewed", "text": "Selon le journal, le porte-parole a déclaré.",
                "expected": True,
            }]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "require reviewer"):
                evaluate_cases(str(path))


if __name__ == "__main__":
    unittest.main()
