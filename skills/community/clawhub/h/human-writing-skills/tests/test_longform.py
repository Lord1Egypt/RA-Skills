import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.cli import main
from humanwriting.longform import (
    split_long_text,
    verify_long_form_package,
    write_long_form_audit,
)


class LongFormAuditTests(unittest.TestCase):
    def test_split_bodies_reconstruct_source_without_overlap_or_loss(self):
        text = "\n\n".join(
            f"第{index}段。" + "这是一段用于检查自然边界的正文。" * 80
            for index in range(1, 6)
        )
        chunks = split_long_text(text, chunk_size=2000, overlap=300)

        self.assertGreater(len(chunks), 1)
        self.assertEqual("".join(chunk.body for chunk in chunks), text)
        for previous, current in zip(chunks, chunks[1:]):
            self.assertEqual(previous.end, current.start)
            self.assertEqual(current.lead_in, text[current.lead_start : current.start])
            self.assertLessEqual(len(current.lead_in), 300)

    def test_fiction_package_uses_outline_and_dialogue_only_where_supported(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "novel.md"
            outline = root / "outline.md"
            output = root / "audit"
            draft.write_text(
                ("第一章\n\n“你还记得那封信吗？”她问。\n\n" + "雨落在窗外。" * 260)
                + ("\n\n第二章\n\n他沿着河岸继续走。" + "天色渐暗。" * 260),
                encoding="utf-8",
            )
            draft_length = len(draft.read_text(encoding="utf-8"))
            outline.write_text(
                "林澈隐瞒信件来源，不会主动向周岚承认。周岚已经知道信件存在。",
                encoding="utf-8",
            )

            written, chunks = write_long_form_audit(
                str(draft),
                str(output),
                style="fiction",
                context_path=str(outline),
                chunk_size=2000,
                overlap=250,
            )

            manifest = json.loads((written / "manifest.json").read_text(encoding="utf-8"))
            prompts = [
                (written / f"{chunk.index:04d}-chunk-audit.md").read_text(encoding="utf-8")
                for chunk in chunks
            ]

        self.assertEqual(sum(item["body_characters"] for item in manifest["chunks"]), draft_length)
        self.assertTrue(all("Audit Module: long-form-style-consistency" in prompt for prompt in prompts))
        self.assertTrue(all("Audit Module: character-consistency-audit" in prompt for prompt in prompts))
        self.assertIn("Audit Module: dialogue-voice-audit", prompts[0])
        self.assertTrue(any("Audit Module: dialogue-voice-audit" not in prompt for prompt in prompts[1:]))
        self.assertIn("Outline / Continuity Authority", prompts[0])
        self.assertIn("read-only continuity context", prompts[0])

    def test_serious_package_protects_content_without_fiction_modules(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "report.md"
            context = root / "plan.md"
            reference = root / "approved.md"
            output = root / "audit"
            draft.write_text(
                "## 项目进展\n\n本季度完成第一阶段测试，样本为120项。" * 160,
                encoding="utf-8",
            )
            context.write_text("术语使用“第一阶段测试”；结论不得扩大到第二阶段。", encoding="utf-8")
            reference.write_text("本报告按事实、依据、限制和下一步安排展开。" * 80, encoding="utf-8")

            written, chunks = write_long_form_audit(
                str(draft),
                str(output),
                style="formal-document",
                context_path=str(context),
                reference_paths=[str(reference)],
                chunk_size=2000,
                overlap=200,
            )
            prompt = (written / "0001-chunk-audit.md").read_text(encoding="utf-8")
            manifest = json.loads((written / "manifest.json").read_text(encoding="utf-8"))

        self.assertGreater(len(chunks), 1)
        self.assertIn("Audit Module: protected-content", prompt)
        self.assertNotIn("Audit Module: character-consistency-audit", prompt)
        self.assertNotIn("Audit Module: dialogue-voice-audit", prompt)
        self.assertIn("explicit reference files: approved.md", manifest["baseline_source"])

    def test_cli_writes_discoverable_long_form_package(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            output = root / "audit"
            draft.write_text("一段正文。" * 500, encoding="utf-8")
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "chunk-audit",
                        "--draft",
                        str(draft),
                        "--style",
                        "fiction",
                        "--chunk-size",
                        "2000",
                        "--output-dir",
                        str(output),
                    ]
                )

            self.assertEqual(code, 0)
            self.assertTrue((output / "00-baseline-prompt.md").is_file())
            self.assertTrue((output / "00-style-drift.json").is_file())
            self.assertTrue((output / "9999-reconcile-prompt.md").is_file())
            self.assertTrue((output / "agent-plan.json").is_file())
            self.assertTrue((output / "reports").is_dir())
            self.assertIn("bounded long-form audit chunks", stdout.getvalue())

    def test_deep_package_creates_gated_agent_tasks_and_blocks_reconciliation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "novel.md"
            outline = root / "outline.md"
            output = root / "audit"
            draft.write_text(
                ("“你还要走吗？”她问。\n\n他没有回答。\n\n" + "雨落在窗外。" * 280)
                + ("\n\n" + "他沿着河岸继续走。" + "天色渐暗。" * 280),
                encoding="utf-8",
            )
            outline.write_text("两人仍因信件争执。", encoding="utf-8")
            written, chunks = write_long_form_audit(
                str(draft),
                str(output),
                style="fiction",
                context_path=str(outline),
                chunk_size=2000,
                overlap=200,
                agent_mode="deep",
            )
            plan = json.loads((written / "agent-plan.json").read_text(encoding="utf-8"))
            kinds = {task["kind"] for task in plan["tasks"]}
            verification = verify_long_form_package(str(written))
            prose_prompt = (written / "0001-prose-audit.md").read_text(encoding="utf-8")
            baseline_prompt = (written / "00-baseline-prompt.md").read_text(encoding="utf-8")

        self.assertGreater(len(chunks), 1)
        self.assertIn("deep-prose-audit", kinds)
        self.assertIn("deep-dialogue-audit", kinds)
        self.assertIn("Coverage Receipt", prose_prompt)
        self.assertIn("Coverage Receipt", baseline_prompt)
        self.assertFalse(verification["ready_for_reconciliation"])
        self.assertEqual(
            verification["planned"],
            sum(task["required_before_reconciliation"] for task in plan["tasks"]),
        )

    def test_whole_book_stage_is_explicit_and_depends_on_all_chunk_reports(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "novel.md"
            draft.write_text(
                "\n\n".join(f"第{index}章\n\n" + "人物作出选择，代价随之改变。" * 130 for index in range(1, 4)),
                encoding="utf-8",
            )
            output = root / "audit"
            written, _ = write_long_form_audit(
                str(draft), str(output), style="fiction", chunk_size=2000, book_level=True
            )
            plan = json.loads((written / "agent-plan.json").read_text(encoding="utf-8"))
            book = next(task for task in plan["tasks"] if task["kind"] == "whole-book-architecture-audit")
            chapter_map = json.loads((written / "00-chapter-map.json").read_text(encoding="utf-8"))
            self.assertTrue(book["required_before_reconciliation"])
            self.assertEqual(len(chapter_map), 3)
            self.assertTrue(all(item["chunks"] for item in chapter_map))
            self.assertTrue(all(task["task_id"] in book["depends_on"] for task in plan["tasks"][:-2]))
            self.assertIn("Audit Module: story-architecture-audit", (written / book["prompt"]).read_text(encoding="utf-8"))
            self.assertFalse(verify_long_form_package(str(written))["ready_for_reconciliation"])

    def test_whole_book_stage_rejects_other_genres_and_too_few_chapters(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("第一章\n\n正文。" * 900, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "limited to fiction"):
                write_long_form_audit(str(draft), str(Path(directory) / "formal"), style="formal-document", book_level=True)
            draft.write_text("第一章\n\n正文。" * 900 + "\n第二章\n正文。", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "at least three"):
                write_long_form_audit(str(draft), str(Path(directory) / "short"), style="fiction", book_level=True)

    def test_coverage_verification_accepts_completed_receipts(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            output = root / "audit"
            draft.write_text("正文。" * 1500, encoding="utf-8")
            written, _ = write_long_form_audit(
                str(draft), str(output), style="fiction", chunk_size=2000
            )
            plan = json.loads((written / "agent-plan.json").read_text(encoding="utf-8"))
            for task in plan["tasks"]:
                if not task["required_before_reconciliation"]:
                    continue
                receipt = (
                    "# Coverage Receipt\n\n"
                    f"- Task ID: `{task['task_id']}`\n"
                    "- Coverage: complete\n"
                    "- Units checked: all assigned units\n"
                    "- Confirmed findings: none\n"
                    "- Unchecked or blocked material: none\n"
                )
                report_path = written / task["report"]
                report_path.write_text(receipt + "x" * 80, encoding="utf-8")
            verification = verify_long_form_package(str(written))

        self.assertTrue(verification["ready_for_reconciliation"])
        self.assertFalse(verification["missing"])
        self.assertFalse(verification["invalid"])
        self.assertEqual(verification["deferred"], ["reconcile"])

    def test_coverage_verification_rejects_blocked_or_undeclared_receipts(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            output = root / "audit"
            draft.write_text("正文。" * 1500, encoding="utf-8")
            written, _ = write_long_form_audit(
                str(draft), str(output), style="fiction", chunk_size=2000
            )
            plan = json.loads((written / "agent-plan.json").read_text(encoding="utf-8"))
            task = next(task for task in plan["tasks"] if task["required_before_reconciliation"])
            (written / task["report"]).write_text(
                "# Coverage Receipt\n\n"
                f"- Task ID: `{task['task_id']}`\n"
                "- Coverage: blocked\n"
                "- Units checked: opening only\n"
                "- Confirmed findings: none\n"
                "- Unchecked or blocked material: remaining paragraphs\n"
                + "x" * 80,
                encoding="utf-8",
            )
            verification = verify_long_form_package(str(written))

        self.assertFalse(verification["ready_for_reconciliation"])
        self.assertTrue(any("coverage is blocked" in entry for entry in verification["invalid"]))

    def test_deep_serious_package_gates_source_tasks_and_translationese(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "report.md"
            source = root / "source.md"
            output = root / "audit"
            draft.write_text("该项目在6月完成，样本为120人。" * 400, encoding="utf-8")
            source.write_text("项目于6月完成，样本为120人。" * 100, encoding="utf-8")
            written, _ = write_long_form_audit(
                str(draft),
                str(output),
                style="news-report",
                source_paths=[str(source)],
                source_budget=1000,
                chunk_size=2000,
                agent_mode="deep",
                translationese=True,
            )
            plan = json.loads((written / "agent-plan.json").read_text(encoding="utf-8"))
            core_prompt = (written / "0001-chunk-audit.md").read_text(encoding="utf-8")

        self.assertIn("deep-evidence-audit", {task["kind"] for task in plan["tasks"]})
        self.assertIn("Audit Module: translationese-audit", core_prompt)

    def test_invalid_overlap_and_baseline_chunk_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "smaller than half"):
            split_long_text("正文" * 1200, chunk_size=2000, overlap=1000)

        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("正文。" * 1000, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Baseline chunk"):
                write_long_form_audit(
                    str(draft),
                    str(Path(directory) / "audit"),
                    style="fiction",
                    chunk_size=2000,
                    baseline_chunk=99,
                )

    def test_nonempty_output_directory_is_rejected_to_prevent_stale_prompts(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            output = root / "audit"
            draft.write_text("正文。" * 1000, encoding="utf-8")
            output.mkdir()
            (output / "old-chunk.md").write_text("stale", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "must be empty"):
                write_long_form_audit(
                    str(draft),
                    str(output),
                    style="fiction",
                    chunk_size=2000,
                )


if __name__ == "__main__":
    unittest.main()
