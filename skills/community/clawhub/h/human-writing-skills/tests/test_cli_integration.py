import hashlib
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import humanwriting

from humanwriting.cli import build_parser, main


class CliIntegrationTests(unittest.TestCase):
    def test_real_writing_cli_plans_claims_submits_verifies_and_assembles(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            outline = root / "outline.md"
            outline.write_text("Mara carries the key to the station.", encoding="utf-8")
            package = root / "writing"
            final = root / "final.md"
            text = ('Mara walked to the station with the key in her coat pocket. She stopped beneath the clock. '
                    'A woman in the ticket office looked up from her book. "You are early," the woman said. '
                    'Mara put the key on the counter and waited. Behind the closed door, a chair scraped across the floor.')
            target = len("".join(text.split()))
            def invoke(command, *args):
                code, output = self.run_cli(["--no-project-config", command, *map(str, args)])
                return code, json.loads(output)
            code, plan = invoke("plan-writing", "--outline", outline, "--output-dir", package,
                                "--target-length", target, "--chunk-size", 500, "--execution-mode", "contract")
            self.assertEqual(code, 0)
            self.assertEqual(plan["chunk_count"], 1)
            code, listed = invoke("writing-tasks", "--package-dir", package)
            self.assertEqual(code, 0)
            self.assertEqual([task["task_id"] for task in listed["tasks"] if task["ready"]], ["outline-check"])
            self.assertEqual(invoke("verify-writing", "--package-dir", package)[0], 1)
            self.assertEqual(invoke("assemble-writing", "--package-dir", package, "--output", final)[0], 1)
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            results = [
                ("outline-check", "planner", {"decision": "pass", "coverage": [{"id": "O0001", "quote": "Mara carries",
                    "note": "A clear action connects the key and station."}], "issues": []}),
                ("chunk-plan", "planner", {"style_contract": "Plain third-person fiction.", "chunks": [{"id": "chunk-0001",
                    "title": "Arrival", "brief": "Mara brings the key to the ticket office.", "outline_ids": ["O0001"],
                    "entry_state": "Mara carries the key.", "exit_state": "The key is on the counter.",
                    "source_ids": [], "reference_ids": [], "depends_on": [], "independent": True}]}),
                ("write-0001", "writer", {"text": text, "covered_outline_ids": ["O0001"], "state": {"key.location": "counter"},
                    "state_changes": [], "pending_threads": [], "handoff": "Mara waits at the counter."}),
                ("review-0001", "editor", {"decision": "pass", "text_sha256": digest,
                    "coverage": [{"id": "P0001", "quote": "Mara walked to the station", "note": "The planned arrival occurs."}],
                    "checks": {key: {"status": "pass", "note": "The assigned scene meets its contract."}
                               for key in ("outline", "continuity", "voice", "naturalness")}, "issues": []}),
                ("continuity", "final-editor", {"decision": "pass", "chunks": [{"id": "chunk-0001", "text_sha256": digest,
                    "note": "Arrival and key placement agree with the outline."}], "boundaries": [], "revision_chunks": [], "issues": []}),
            ]
            result_path = root / "result.json"
            for task_id, agent_id, result in results:
                code, claim = invoke("claim-writing", "--package-dir", package, "--task-id", task_id, "--agent-id", agent_id)
                self.assertEqual(code, 0, claim)
                self.assertIn("result_schema", claim)
                result["claim_token"] = claim["claim_token"]
                result_path.write_text(json.dumps(result), encoding="utf-8")
                code, submitted = invoke("submit-writing", "--package-dir", package, "--task-id", task_id,
                                         "--agent-id", agent_id, "--result", result_path)
                self.assertEqual(code, 0, submitted)
            code, verified = invoke("verify-writing", "--package-dir", package)
            self.assertEqual(code, 0)
            self.assertTrue(verified["ready_for_assembly"])
            code, assembled = invoke("assemble-writing", "--package-dir", package, "--output", final)
            self.assertEqual(code, 0, assembled)
            self.assertEqual(final.read_text(encoding="utf-8"), text + "\n")

    def test_writing_parser_defaults_and_repeated_material_paths(self):
        args = build_parser().parse_args([
            "plan-writing", "--outline", "outline.md", "--output-dir", "writing", "--target-length", "10000",
            "--context", "ledger.md", "--context", "prior.md", "--source", "facts.md", "--reference", "voice.md",
        ])
        self.assertEqual(args.style, "fiction")
        self.assertEqual(args.chunk_size, 5000)
        self.assertEqual(args.length_unit, "characters")
        self.assertEqual(args.execution_mode, "sequential")
        self.assertEqual(args.max_parallel, 4)
        self.assertEqual(args.context, ["ledger.md", "prior.md"])
        self.assertEqual(args.source, ["facts.md"])
        self.assertEqual(args.reference, ["voice.md"])

    def test_writing_cli_dispatch_preserves_structured_json_and_materials(self):
        queue = Mock()
        queue.plan_long_form_writing.return_value = {"package_dir": "writing", "title": 'A "quoted" title\nNext line'}
        with patch.object(humanwriting, "writing_queue", queue, create=True):
            code, output = self.run_cli([
                "--no-project-config", "plan-writing", "--outline", "outline.md", "--output-dir", "writing",
                "--target-length", "10000", "--style", "fiction", "--execution-mode", "contract",
                "--context", "ledger.md", "--context", "prior.md", "--source", "facts.md", "--reference", "voice.md",
            ])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["title"], 'A "quoted" title\nNext line')
        queue.plan_long_form_writing.assert_called_once_with(
            "outline.md", "writing", style="fiction", target_length=10000, chunk_size=5000,
            length_unit="characters", execution_mode="contract", max_parallel=4,
            context_paths=["ledger.md", "prior.md"], source_paths=["facts.md"], reference_paths=["voice.md"],
        )

    def test_submit_writing_reads_json_file_and_rejects_invalid_json(self):
        queue = Mock()
        queue.submit_writing_result.return_value = {"accepted": True}
        with TemporaryDirectory() as directory, patch.object(humanwriting, "writing_queue", queue, create=True):
            path = Path(directory) / "result.json"
            args = ["--no-project-config", "submit-writing", "--package-dir", "writing", "--task-id", "writer-001",
                    "--agent-id", "worker", "--result", str(path)]
            result = {"claim_token": "opaque-cli-claim", "text": 'A "quoted" line.\nA backslash: \\.', "notes": []}
            path.write_text(json.dumps(result), encoding="utf-8")
            code, output = self.run_cli(args)
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(output)["accepted"])
            queue.submit_writing_result.assert_called_once_with("writing", "writer-001", result, "worker")
            for invalid in ("[]", "{not-json", "null"):
                path.write_text(invalid, encoding="utf-8")
                code, output = self.run_cli(args)
                self.assertNotEqual(code, 0)
                self.assertIn("error", json.loads(output))
            self.assertEqual(queue.submit_writing_result.call_count, 1)

    def test_writing_coordination_cli_dispatch_and_failure_status(self):
        queue = Mock()
        cases = [
            (["writing-tasks"], "list_writing_tasks", ("writing",)),
            (["claim-writing", "--task-id", "outline-check", "--agent-id", "worker"],
             "claim_writing_task", ("writing", "outline-check", "worker")),
            (["assemble-writing", "--output", "final.md"], "assemble_writing_project", ("writing", "final.md")),
        ]
        with patch.object(humanwriting, "writing_queue", queue, create=True):
            for args, method, expected in cases:
                getattr(queue, method).return_value = {"ok": True}
                code, output = self.run_cli(["--no-project-config", *args, "--package-dir", "writing"])
                self.assertEqual(code, 0)
                self.assertTrue(json.loads(output)["ok"])
                getattr(queue, method).assert_called_once_with(*expected)
            for ready in (False, True):
                queue.verify_writing_project.return_value = {"ready_for_assembly": ready}
                code, output = self.run_cli(["--no-project-config", "verify-writing", "--package-dir", "writing"])
                self.assertEqual(code, 0 if ready else 1)
                self.assertEqual(json.loads(output)["ready_for_assembly"], ready)
            queue.assemble_writing_project.side_effect = ValueError("Required tasks are incomplete.")
            code, output = self.run_cli(["--no-project-config", "assemble-writing", "--package-dir", "writing", "--output", "final.md"])
            self.assertNotEqual(code, 0)
            self.assertIn("incomplete", json.loads(output)["error"])

    def run_cli(self, arguments, stdin_text=""):
        output = io.StringIO()
        previous_stdin = sys.stdin
        sys.stdin = io.StringIO(stdin_text)
        try:
            with redirect_stdout(output):
                code = main(arguments)
        finally:
            sys.stdin = previous_stdin
        return code, output.getvalue()

    def test_lint_reads_stdin_and_emits_github_annotations(self):
        code, output = self.run_cli(
            ["lint", "--draft", "-", "--style", "fiction", "--format", "github"],
            "未来可期。",
        )
        self.assertEqual(code, 0)
        self.assertIn("::warning file=stdin.md", output)
        self.assertIn("CLOSE001", output)

    def test_rule_catalog_has_machine_readable_ids(self):
        code, output = self.run_cli(["list", "--kind", "rule", "--format", "json"])
        catalog = json.loads(output)
        self.assertEqual(code, 0)
        self.assertIn("END002", {item["id"] for item in catalog})
        self.assertIn("ARG001", {item["id"] for item in catalog})

    def test_extract_ledger_accepts_stdin(self):
        code, output = self.run_cli(
            ["extract-ledger", "--draft", "-"],
            "Mara keeps the key and promises to return before dawn.",
        )
        self.assertEqual(code, 0)
        self.assertIn("Continuity Ledger Extraction", output)
        self.assertIn("evidence", output)


if __name__ == "__main__":
    unittest.main()
