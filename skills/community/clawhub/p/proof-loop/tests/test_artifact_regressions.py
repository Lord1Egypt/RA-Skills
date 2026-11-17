import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/demo-repo/tasks/nav-labels-proof"

class ArtifactRegressionTests(unittest.TestCase):
    def run_case(self, change, command="check"):
        with tempfile.TemporaryDirectory() as tmp:
            task = Path(tmp) / SOURCE.name
            shutil.copytree(SOURCE, task)
            change(task)
            result = subprocess.run(["python3", str(ROOT / "bin/proof-loop"), command, str(task)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def mutate(self, task, fn, name="verdict.json"):
        path = task / name
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data))

    def test_incomplete_and_malformed_verdicts_fail(self):
        mutations = [
            lambda v: v.clear(),
            lambda v: v.update(criteria=[]),
            lambda v: v["criteria"].pop(),
            lambda v: v["criteria"].append(v["criteria"][0]),
            lambda v: v["criteria"][0].update(id="AC99"),
            lambda v: v["criteria"][0].update(status=[]),
            lambda v: v["criteria"][0].update(note=""),
            lambda v: v.update(task_id="other"),
            lambda v: v.update(phase="build"),
            lambda v: v.update(agent="unassigned"),
            lambda v: v.update(timestamp="yesterday"),
            lambda v: v.pop("agent"),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.run_case(lambda t: self.mutate(t, mutate))

    def test_missing_evidence_or_problem_file_fails(self):
        for name in ("evidence.md", "problems.md"):
            self.run_case(lambda t: (t / name).unlink())
        self.run_case(lambda t: (t / "spec.md").write_text("# No criteria"))
        self.run_case(lambda t: (t / "spec.md").write_text("AC1: one\nAC1: duplicate"))

    def test_nested_schema_constraints_are_enforced(self):
        for mutate in (
            lambda v: v.update(criteria="not an array"),
            lambda v: v.update(overall="MAYBE"),
            lambda v: v["criteria"][0].pop("status"),
            lambda v: v.update(timestamp=12),
        ):
            self.run_case(lambda t: self.mutate(t, mutate), "validate")
        self.run_case(lambda t: self.mutate(t, lambda e: e.update(checks=[{}]), "evidence.json"), "validate")

if __name__ == "__main__":
    unittest.main()
