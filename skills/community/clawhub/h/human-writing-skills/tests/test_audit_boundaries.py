import hashlib
import json
import multiprocessing
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.audit_queue import claim_audit_task, submit_audit_report
from humanwriting.longform import verify_long_form_package
from test_mcp_server import complete_report


def race_claim(package, start, results, agent):
    start.wait(10)
    try:
        claim_audit_task(package, "review", agent)
        results.put("claimed")
    except ValueError:
        results.put("rejected")


class AuditBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "audit"
        self.package.mkdir()
        self.task = {"task_id": "review", "prompt": "prompt.md", "report": "report.md"}
        self.plan = {"tasks": [self.task]}
        self.save_plan()
        (self.package / "prompt.md").write_text("Read every assigned paragraph.", encoding="utf-8")

    def save_plan(self):
        (self.package / "agent-plan.json").write_text(json.dumps(self.plan), encoding="utf-8")

    def test_coverage_cannot_read_external_report(self):
        self.task["report"] = "../outside.md"
        self.save_plan()
        (self.root / "outside.md").write_text(complete_report("review"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "within the audit package"):
            verify_long_form_package(str(self.package))

    def test_malformed_or_vacuous_plans_fail_closed(self):
        for plan in ([], {"tasks": [None]}, {"tasks": []},
                     {"tasks": [{"task_id": "final", "required_before_reconciliation": False}]},
                     {"tasks": [self.task, self.task]}):
            with self.subTest(plan=plan):
                self.plan = plan
                self.save_plan()
                with self.assertRaises(ValueError):
                    verify_long_form_package(str(self.package))

    def test_claim_returns_assignment_and_digest_matches_saved_bytes(self):
        claim = claim_audit_task(self.package, "review", "worker")
        self.assertEqual(claim["content"], "Read every assigned paragraph.")
        report = complete_report("review") + "\n\n  "
        result = submit_audit_report(self.package, "review", report, "worker")
        self.assertEqual(result["report_sha256"], hashlib.sha256((self.package / "report.md").read_bytes()).hexdigest())
        with self.assertRaisesRegex(ValueError, "cannot submit"):
            submit_audit_report(self.package, "review", report, "other-worker")

    def test_parallel_processes_cannot_claim_same_task(self):
        ctx = multiprocessing.get_context("spawn")
        start, results = ctx.Event(), ctx.Queue()
        workers = [ctx.Process(target=race_claim, args=(str(self.package), start, results, f"worker-{i}")) for i in range(3)]
        try:
            for worker in workers:
                worker.start()
            start.set()
            received = [results.get(timeout=20) for _ in workers]
            self.assertEqual(received.count("claimed"), 1)
            self.assertEqual(received.count("rejected"), 2)
        finally:
            for worker in workers:
                worker.join(timeout=5)
                if worker.is_alive():
                    worker.terminate()
                    worker.join()
            results.close()

    def test_parallel_threads_cannot_claim_same_task(self):
        def claim(index):
            try:
                claim_audit_task(self.package, "review", f"thread-{index}")
                return True
            except ValueError:
                return False
        with ThreadPoolExecutor(max_workers=4) as pool:
            self.assertEqual(sum(pool.map(claim, range(4))), 1)

    def test_external_symlink_state_and_plan_are_rejected(self):
        outside = self.root / "outside.json"
        outside.write_text('{"tasks": {}}', encoding="utf-8")
        state = self.package / "agent-state.json"
        try:
            state.symlink_to(outside)
        except OSError:
            self.skipTest("Symlink creation is unavailable")
        with self.assertRaisesRegex(ValueError, "within the audit package"):
            claim_audit_task(self.package, "review")
        self.assertEqual(outside.read_text(encoding="utf-8"), '{"tasks": {}}')
        plan = self.package / "agent-plan.json"
        plan.unlink()
        plan.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "within the audit package"):
            verify_long_form_package(str(self.package))
