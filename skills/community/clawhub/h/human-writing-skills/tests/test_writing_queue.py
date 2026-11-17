import hashlib
import json
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.writing_queue import (
    assemble_writing_project,
    claim_writing_task,
    count_length,
    list_writing_tasks,
    plan_long_form_writing,
    submit_writing_result,
    verify_writing_project,
    _publish_new_text,
)


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class WritingQueueTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.outline = self.root / "outline.md"
        self.outline.write_text("A visitor returns the borrowed key.\n\nThe owner locks the door and leaves.", encoding="utf-8")
        self.package = self.root / "writing"

    def plan(self, **kwargs):
        return plan_long_form_writing(self.outline, self.package, style=kwargs.pop("style", "fiction"),
            target_length=kwargs.pop("target_length", 400), chunk_size=200, **kwargs)

    def submit(self, task, result, agent=None):
        agent = agent or task + "-agent"
        claim_writing_task(self.package, task, agent)
        return self.finish(task, result, agent)

    def finish(self, task, result, agent):
        state = json.loads((self.package / "writing-state.json").read_text(encoding="utf-8"))
        return submit_writing_result(self.package, task,
            {"claim_token": state["entries"][task]["claim_token"], **result}, agent)

    def outline_check(self):
        return {"decision": "pass", "coverage": [
            {"id": "O0001", "quote": "visitor returns", "note": "Key ownership and return are specified."},
            {"id": "O0002", "quote": "owner locks", "note": "Leaving follows receiving the key."}], "issues": []}

    def chunk_plan(self, independent=False):
        return {"style_contract": "Plain English, restrained viewpoint, actions before reflection.", "chunks": [
            {"id": f"chunk-{i:04d}", "title": f"Part {i}", "brief": "Cover the assigned action without a reflective tail.",
             "outline_ids": [f"O{i:04d}"], "entry_state": "The key has not yet moved.",
             "exit_state": "The key's owner and location are explicit.", "source_ids": [], "reference_ids": [],
             "depends_on": [], "independent": independent} for i in (1, 2)]}

    def prepare(self, **kwargs):
        self.plan(**kwargs)
        self.submit("outline-check", self.outline_check())
        self.submit("chunk-plan", self.chunk_plan(kwargs.get("execution_mode") == "contract"))

    def draft(self, index, state=None):
        lead = "She accepted the key and closed her hand around it. " if index == 1 else "The owner locked the door and stepped onto the pavement. "
        return {"text": lead + "The rain had stopped. " * 9,
            "covered_outline_ids": [f"O{index:04d}"], "state": state or {"key.owner": "owner"},
            "state_changes": [], "pending_threads": [], "handoff": "Carry the key ownership into the next block."}

    def review(self, draft, style="fiction", revise=False):
        checks = {key: {"status": "pass", "note": "Checked against the assigned outline and actual prose."}
            for key in ("outline", "continuity", "voice", "naturalness")}
        if style == "formal-document":
            checks["sources"] = {"status": "pass", "note": "No unsupported statistics or citations were added."}
        return {"decision": "revise" if revise else "pass", "text_sha256": digest(draft["text"]),
            "coverage": [{"id": "P0001", "quote": draft["text"][:40], "note": "The action is legible; the ending needs no added reflection."}],
            "checks": checks, "issues": [{"paragraph_id": "P0001", "quote": "The rain had stopped.",
                "reason": "This sentence repeats without advancing the scene.", "suggestion": "Keep one occurrence."}] if revise else []}

    def final_review(self, drafts):
        return {"decision": "pass", "chunks": [{"id": f"chunk-{i:04d}", "text_sha256": digest(d["text"]),
                "note": "The block follows its outline and shared voice."} for i, d in enumerate(drafts, 1)],
            "boundaries": [{"left": "chunk-0001", "right": "chunk-0002",
                "left_quote": drafts[0]["text"][-40:], "right_quote": drafts[1]["text"][:40],
                "note": "Ownership carries through, and leaving follows locking."}], "revision_chunks": [], "issues": []}

    def write_and_review(self, index, draft=None, style="fiction"):
        draft = draft or self.draft(index)
        self.submit(f"write-{index:04d}", draft)
        self.submit(f"review-{index:04d}", self.review(draft, style))
        return draft

    def test_sixty_thousand_characters_allocate_twelve_writer_jobs(self):
        other = self.root / "default-size"
        created = plan_long_form_writing(self.outline, other, style="fiction", target_length=60000)
        self.assertEqual(created["chunk_count"], 12)
        rows = list_writing_tasks(other)["tasks"]
        self.assertEqual(len([t for t in rows if t["task_id"].startswith("write-")]), 12)
        self.assertEqual([t["task_id"] for t in rows if t["ready"]], ["outline-check"])

    def test_oversized_assignments_are_paginated_without_losing_current_schema(self):
        from unittest.mock import patch
        self.plan()
        material = "Complete assignment material. " * 2500
        with patch("humanwriting.writing_queue._prompt", return_value=material):
            claim = claim_writing_task(self.package, "outline-check", "checker")
        path = self.package / f"results/outline-check-{claim['claim_token']}-assignment.md"
        self.assertEqual(path.read_text(encoding="utf-8"), material)
        self.assertIn("offset/next_offset", claim["content"])
        self.assertLess(len(claim["content"]), 60000)
        self.assertEqual(claim["result_schema"]["claim_token"], claim["claim_token"])
        self.assertEqual(claim["lease_seconds"], 3600)

    def test_genre_schema_matches_mandatory_review_checks(self):
        for style in ("formal-document", "academic-paper", "news-report", "fiction"):
            from humanwriting.writing_queue import _schema
            checks = _schema("review-0001", style)["checks"]
            self.assertEqual("sources" in checks, style != "fiction")

    def test_expired_claim_is_visible_as_reclaimable_not_active(self):
        from unittest.mock import patch
        self.plan()
        claim_writing_task(self.package, "outline-check", "checker")
        with patch("humanwriting.writing_queue.LEASE_SECONDS", 0):
            row = list_writing_tasks(self.package)["tasks"][0]
        self.assertEqual(row["status"], "expired")
        self.assertTrue(row["ready"])

    def test_outline_and_planner_require_complete_evidence_and_coverage(self):
        self.plan()
        with self.assertRaisesRegex(ValueError, "Waiting for outline-check"):
            claim_writing_task(self.package, "chunk-plan", "planner")
        claim_writing_task(self.package, "outline-check", "checker")
        missing = self.outline_check()
        missing["coverage"].pop()
        with self.assertRaisesRegex(ValueError, "every assigned unit"):
            self.finish("outline-check", missing, "checker")
        self.finish("outline-check", self.outline_check(), "checker")
        planning = self.chunk_plan()
        planning["chunks"][1]["outline_ids"] = ["O0001"]
        claim_writing_task(self.package, "chunk-plan", "planner")
        with self.assertRaisesRegex(ValueError, "every outline unit"):
            self.finish("chunk-plan", planning, "planner")

    def test_default_serial_requires_approved_predecessor_and_distinct_editor(self):
        self.prepare()
        self.submit("write-0001", self.draft(1), "writer")
        with self.assertRaisesRegex(ValueError, "Waiting for review-0001"):
            claim_writing_task(self.package, "write-0002", "writer-two")
        with self.assertRaisesRegex(ValueError, "other than its writer"):
            claim_writing_task(self.package, "review-0001", "writer")
        self.submit("review-0001", self.review(self.draft(1)), "editor")
        claim = claim_writing_task(self.package, "write-0002", "writer-two")
        self.assertIn("key.owner", claim["content"])
        self.assertIn(self.draft(1)["text"][-50:], claim["content"])

    def test_contract_parallel_claims_are_bounded_and_owned(self):
        self.prepare(execution_mode="contract", max_parallel=1)
        claim_writing_task(self.package, "write-0001", "a")
        with self.assertRaisesRegex(ValueError, "Maximum parallel"):
            claim_writing_task(self.package, "write-0002", "b")
        with self.assertRaisesRegex(ValueError, "another agent"):
            claim_writing_task(self.package, "write-0001", "b")
        with self.assertRaisesRegex(ValueError, "same agent"):
            self.finish("write-0001", self.draft(1), "b")
        self.finish("write-0001", self.draft(1), "a")
        self.assertEqual(claim_writing_task(self.package, "write-0002", "b")["task_id"], "write-0002")

    def test_parallel_requires_explicit_independence_and_acyclic_contracts(self):
        self.plan(execution_mode="contract")
        self.submit("outline-check", self.outline_check())
        claim_writing_task(self.package, "chunk-plan", "planner")
        planning = self.chunk_plan()
        with self.assertRaisesRegex(ValueError, "explicit independence"):
            self.finish("chunk-plan", planning, "planner")
        planning["chunks"][1]["depends_on"] = ["chunk-0002"]
        with self.assertRaisesRegex(ValueError, "cycles"):
            self.finish("chunk-plan", planning, "planner")

    def test_state_cannot_disappear_or_change_without_literal_transition(self):
        self.prepare()
        self.write_and_review(1)
        claim_writing_task(self.package, "write-0002", "writer")
        draft = self.draft(2, {"door": "locked"})
        with self.assertRaisesRegex(ValueError, "disappeared"):
            self.finish("write-0002", draft, "writer")
        draft["state"]["key.owner"] = "visitor"
        with self.assertRaisesRegex(ValueError, "evidenced transition"):
            self.finish("write-0002", draft, "writer")
        draft["state_changes"] = [{"key": "key.owner", "before": "owner", "after": "visitor", "evidence": "invented quote"}]
        with self.assertRaisesRegex(ValueError, "literally"):
            self.finish("write-0002", draft, "writer")

    def test_short_output_and_stale_review_digests_are_rejected(self):
        self.prepare()
        claim_writing_task(self.package, "write-0001", "writer")
        short = self.draft(1)
        short["text"] = "Only a synopsis."
        with self.assertRaisesRegex(ValueError, "Draft length"):
            self.finish("write-0001", short, "writer")
        self.finish("write-0001", self.draft(1), "writer")
        claim_writing_task(self.package, "review-0001", "editor")
        report = self.review(self.draft(1))
        report["text_sha256"] = "stale"
        with self.assertRaisesRegex(ValueError, "current draft"):
            self.finish("review-0001", report, "editor")

    def test_revise_returns_writer_to_queue_and_stops_after_budget(self):
        self.prepare()
        for attempt in range(3):
            self.submit("write-0001", self.draft(1))
            result = self.submit("review-0001", self.review(self.draft(1), revise=True))
            self.assertEqual(result["status"], "revision_requested")
            if attempt < 2:
                claimed = claim_writing_task(self.package, "write-0001", "write-0001-agent")
                self.assertIn("Editor feedback", claimed["content"])
        with self.assertRaisesRegex(ValueError, "Revision budget exhausted"):
            claim_writing_task(self.package, "write-0001", "writer")
        self.assertFalse(verify_writing_project(self.package)["ready_for_assembly"])

    def test_full_pipeline_requires_all_boundaries_and_assembles_in_order(self):
        self.prepare()
        with self.assertRaisesRegex(ValueError, "before assembly"):
            assemble_writing_project(self.package, self.root / "book.md")
        drafts = [self.write_and_review(i) for i in (1, 2)]
        with self.assertRaisesRegex(ValueError, "independent"):
            claim_writing_task(self.package, "continuity", "write-0001-agent")
        claim = claim_writing_task(self.package, "continuity", "main-editor")
        self.assertIn("continuity-index.json", claim["content"])
        report = self.final_review(drafts)
        report["boundaries"] = []
        with self.assertRaisesRegex(ValueError, "every adjacent boundary"):
            self.finish("continuity", report, "main-editor")
        self.finish("continuity", self.final_review(drafts), "main-editor")
        self.assertTrue(verify_writing_project(self.package)["ready_for_assembly"])
        output = self.root / "book.md"
        assembled = assemble_writing_project(self.package, output)
        self.assertEqual(assembled["chunk_count"], 2)
        self.assertEqual(output.read_text(encoding="utf-8"), "\n\n".join(d["text"].strip() for d in drafts) + "\n")
        self.assertNotIn("Part 1", output.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "never overwritten"):
            assemble_writing_project(self.package, self.outline)

    def test_final_revision_invalidates_downstream_drafts_and_old_approvals(self):
        self.prepare()
        drafts = [self.write_and_review(i) for i in (1, 2)]
        report = self.final_review(drafts)
        report.update(decision="revise", revision_chunks=["chunk-0001"], issues=["Key state needs an evidenced transition."])
        self.submit("continuity", report, "main-editor")
        rows = {r["task_id"]: r for r in list_writing_tasks(self.package)["tasks"]}
        self.assertTrue(rows["write-0001"]["ready"])
        self.assertFalse(rows["write-0002"]["ready"])
        self.assertEqual(rows["write-0002"]["status"], "stale")
        self.assertFalse(verify_writing_project(self.package)["ready_for_assembly"])

    def test_serious_review_requires_sources_check_without_narrative_instructions(self):
        self.prepare(style="formal-document")
        draft = self.draft(1)
        self.submit("write-0001", draft)
        claim = claim_writing_task(self.package, "review-0001", "editor")
        self.assertIn("numbers, attribution and uncertainty", claim["content"])
        self.assertNotIn("directed dialogue/actions", claim["content"])
        with self.assertRaisesRegex(ValueError, "genre-specific"):
            self.finish("review-0001", self.review(draft), "editor")

    def test_tampered_snapshots_and_results_cannot_reuse_approvals(self):
        self.prepare()
        self.submit("write-0001", self.draft(1))
        result = self.package / "results/write-0001-v1.json"
        result.write_text(result.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "approval is invalid"):
            verify_writing_project(self.package)
        (self.package / "inputs/O0001.md").write_text("changed outline", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "snapshot changed"):
            list_writing_tasks(self.package)

    def test_counts_are_explicit_and_inputs_are_not_silently_truncated(self):
        self.assertEqual(count_length("今天 下雨。", "characters"), 5)
        self.assertEqual(count_length("It isn't raining today.", "words"), 4)
        context = self.root / "ledger.md"
        context.write_text("x" * 12001, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "compact approved ledger"):
            self.plan(context_paths=[str(context)])
        self.assertFalse(self.package.exists())

    def test_expired_and_reissued_claims_reject_late_results(self):
        self.prepare()
        old_claim = claim_writing_task(self.package, "write-0001", "writer")
        resumed = claim_writing_task(self.package, "write-0001", "writer")
        self.assertEqual(old_claim["claim_token"], resumed["claim_token"])
        state_path = self.package / "writing-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["entries"]["write-0001"]["claimed_at"] = 0
        state_path.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "same agent"):
            self.finish("write-0001", self.draft(1), "writer")
        fresh = claim_writing_task(self.package, "write-0001", "writer")
        self.assertNotEqual(old_claim["claim_token"], fresh["claim_token"])
        with self.assertRaisesRegex(ValueError, "stale results"):
            self.finish("write-0001", {**self.draft(1), "claim_token": old_claim["claim_token"]}, "writer")

    def test_pending_exchange_needs_literal_resolution_before_it_disappears(self):
        self.prepare()
        first = self.draft(1)
        first["pending_threads"] = ["The visitor is waiting for the owner's answer."]
        self.write_and_review(1, first)
        second = self.draft(2)
        claim_writing_task(self.package, "write-0002", "writer")
        with self.assertRaisesRegex(ValueError, "pending threads cannot disappear"):
            self.finish("write-0002", second, "writer")
        second["resolved_threads"] = [{"thread": first["pending_threads"][0], "evidence": "The owner locked the door"}]
        self.finish("write-0002", second, "writer")
        editorial = claim_writing_task(self.package, "review-0002", "editor")
        self.assertIn(first["pending_threads"][0], editorial["content"])

    def test_parallel_join_requires_evidence_for_conflicting_facts(self):
        self.plan(target_length=600, execution_mode="contract")
        self.submit("outline-check", self.outline_check())
        planning = self.chunk_plan(True)
        third = {**planning["chunks"][1], "id": "chunk-0003", "independent": False,
            "depends_on": ["chunk-0001", "chunk-0002"]}
        planning["chunks"].append(third)
        self.submit("chunk-plan", planning)
        self.write_and_review(1, self.draft(1, {"key.owner": "visitor"}))
        self.write_and_review(2, self.draft(2, {"key.owner": "owner"}))
        third_draft = self.draft(2)
        claim_writing_task(self.package, "write-0003", "writer")
        with self.assertRaisesRegex(ValueError, "evidenced transition"):
            self.finish("write-0003", third_draft, "writer")
        third_draft["state_changes"] = [{"key": "key.owner", "before": ["visitor", "owner"],
            "after": "owner", "evidence": "The owner locked the door"}]
        self.finish("write-0003", third_draft, "writer")

    def test_resolved_threads_are_not_resurrected_by_ancestor_dependencies(self):
        self.plan(target_length=600)
        self.submit("outline-check", self.outline_check())
        planning = self.chunk_plan()
        planning["chunks"].append({**planning["chunks"][1], "id": "chunk-0003", "depends_on": ["chunk-0001"]})
        self.submit("chunk-plan", planning)
        first = self.draft(1)
        first["pending_threads"] = ["The visitor is waiting for an answer."]
        self.write_and_review(1, first)
        second = self.draft(2)
        second["resolved_threads"] = [{"thread": first["pending_threads"][0], "evidence": second["text"][:40]}]
        self.write_and_review(2, second)
        third = self.draft(2)
        self.submit("write-0003", third)

    def test_rejected_outline_returns_an_explicit_terminal_block(self):
        self.plan()
        report = self.outline_check()
        report.update(decision="revise", issues=["Return order conflicts with the canonical ledger."])
        result = self.submit("outline-check", report)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("corrected immutable inputs", result["blocked_tasks"]["outline-check"])
        self.assertFalse(any(row["ready"] for row in list_writing_tasks(self.package)["tasks"]))

    def test_concurrent_output_publication_never_clobbers_another_file(self):
        output = self.root / "same-output.md"
        def publish(text):
            try:
                _publish_new_text(output, text)
                return True
            except ValueError:
                return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(publish, ["first manuscript", "second manuscript"]))
        self.assertEqual(sum(outcomes), 1)
        self.assertIn(output.read_text(encoding="utf-8"), ["first manuscript", "second manuscript"])

    def test_twelve_block_final_revision_keeps_feedback_out_of_writer_context(self):
        plan_long_form_writing(self.outline, self.package, style="fiction", target_length=60000)
        self.submit("outline-check", self.outline_check())
        planning = self.chunk_plan()
        planning["chunks"] = [{**planning["chunks"][0], "id": f"chunk-{i:04d}",
            "outline_ids": ["O0001" if i < 12 else "O0002"]} for i in range(1, 13)]
        self.submit("chunk-plan", planning)
        drafts = []
        for i in range(1, 13):
            draft = {**self.draft(1), "text": f"Block {i}. " + "The owner closes the door. " * 220,
                "covered_outline_ids": planning["chunks"][i - 1]["outline_ids"]}
            self.write_and_review(i, draft)
            drafts.append(draft)
        report = {"decision": "revise", "issues": ["Clarify the first block's state transition."],
            "revision_chunks": ["chunk-0001"], "chunks": [{"id": f"chunk-{i:04d}",
                "text_sha256": digest(d["text"]), "note": "A" * 2000} for i, d in enumerate(drafts, 1)],
            "boundaries": [{"left": f"chunk-{i:04d}", "right": f"chunk-{i + 1:04d}",
                "left_quote": drafts[i - 1]["text"][-500:], "right_quote": drafts[i]["text"][:500],
                "note": "B" * 2000} for i in range(1, 12)]}
        self.submit("continuity", report, "main-editor")
        revised = claim_writing_task(self.package, "write-0001", "write-0001-agent")
        self.assertLess(len(revised["content"]), 60000)
        self.assertIn("continuity-v1.json", revised["content"])
        self.assertNotIn("A" * 2000, revised["content"])

    def test_large_accepted_word_block_uses_paged_complete_review(self):
        plan_long_form_writing(self.outline, self.package, style="fiction",
            target_length=12000, chunk_size=12000, length_unit="words")
        self.submit("outline-check", self.outline_check())
        planning = self.chunk_plan()
        planning["chunks"] = [{**planning["chunks"][0], "outline_ids": ["O0001", "O0002"]}]
        self.submit("chunk-plan", planning)
        draft = {**self.draft(1), "text": ("trees " * 9600).strip(),
            "covered_outline_ids": ["O0001", "O0002"]}
        self.submit("write-0001", draft)
        claim = claim_writing_task(self.package, "review-0001", "editor")
        self.assertLessEqual(len(claim["content"]), 60000)
        self.assertIn("Paged review assignment", claim["content"])
        stored = self.package / f"review-input-0001-{claim['claim_token']}.md"
        material = stored.read_text(encoding="utf-8")
        self.assertGreater(len(material), 60000)
        self.assertIn(digest(draft["text"]), material)
        self.assertIn(draft["text"], material)
        self.submit("review-0001", self.review(draft), "editor")


if __name__ == "__main__":
    unittest.main()
