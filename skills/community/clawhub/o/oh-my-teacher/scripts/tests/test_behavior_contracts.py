"""Behavior-contract regression tests for the Oh My Teacher skill.

Unlike test_validate_skill.py (structure: files exist, commands registered),
these assert *behavioral* properties of the skill's instructions and worked
examples — the contracts a model is supposed to honor at runtime. They are
static assertions over Markdown, so they cannot run a live model, but they
catch the most common silent regression: editing a reference or example until
it no longer matches the behavior the skill promises.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
REFS = ROOT / "references"
EXAMPLES = ROOT / "examples"

sys.path.insert(0, str(SCRIPTS))
from srs import markdown_table  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# The 8 sections a /grade, /quiz, or /mock grading response must return.
GRADE_SECTIONS = [
    "## Score",
    "## Checks Performed",
    "## What Is Correct",
    "## Lost Points",
    "## Exact Mistake",
    "## Correct Version",
    "## Repair Drill",
    "## SRS Update",
]


class GradeOutputContract(unittest.TestCase):
    def test_question_types_defines_all_grade_sections(self):
        text = read(REFS / "question-types.md")
        for section in GRADE_SECTIONS:
            self.assertIn(section, text, f"question-types.md missing grade section {section!r}")

    def test_sample_session_grade_block_follows_contract(self):
        text = read(EXAMPLES / "sample-session.md")
        # The worked /quiz grading example must use the same section structure.
        for section in GRADE_SECTIONS:
            self.assertIn(section, text, f"sample-session.md grade example missing {section!r}")


class StrictGradingContract(unittest.TestCase):
    def test_strict_calibration_present(self):
        text = read(REFS / "question-types.md")
        self.assertIn("false positive", text)
        self.assertIn("Do not award full marks", text)

    def test_double_pass_protocol_present(self):
        text = read(REFS / "question-types.md")
        self.assertIn("Double-Pass", text)
        self.assertIn("self-correction", text.lower())


class DiagnoseContract(unittest.TestCase):
    def test_diagnose_uses_fixed_difficulty(self):
        text = read(REFS / "question-types.md")
        # /diagnose must NOT adapt difficulty mid-run, unlike /quiz.
        self.assertIn("Fixed", text)
        self.assertIn("do NOT step up/down mid-diagnostic", text)


class SRSSchemaContract(unittest.TestCase):
    CANONICAL = "| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |"

    def test_script_writes_canonical_8_column_header(self):
        header = markdown_table([]).splitlines()[0]
        self.assertEqual(header, self.CANONICAL)

    def test_spaced_repetition_doc_documents_8_columns(self):
        text = read(REFS / "spaced-repetition.md")
        self.assertIn("Ease", text)
        self.assertIn("Lapses", text)
        self.assertIn(self.CANONICAL, text)

    def test_no_stored_srs_table_uses_legacy_5_columns(self):
        # The documented SRS *state* table (the one the script reads/writes)
        # must be 8 columns everywhere it appears as a stored table.
        legacy = re.compile(r"\|\s*Topic\s*\|\s*Last Review\s*\|\s*Score\s*\|\s*Streak\s*\|\s*Next Review\s*\|\s*\n")
        for path in [REFS / "spaced-repetition.md", REFS / "ima-adaptation.md",
                     EXAMPLES / "sample-ima-course-home.md"]:
            text = read(path)
            self.assertIsNone(legacy.search(text),
                              f"{path.name} still contains a legacy 5-column SRS state table")


class CalibrationContract(unittest.TestCase):
    def test_calibration_strategy_documented(self):
        strat = read(REFS / "learning-strategies.md")
        self.assertIn("Confidence Calibration", strat)
        qt = read(REFS / "question-types.md")
        self.assertIn("Calibration", qt)


class ErrorAnalyticsContract(unittest.TestCase):
    def test_error_taxonomy_and_analytics_present(self):
        wrong = read(REFS / "wrong-note.md")
        self.assertIn("Error Taxonomy", wrong)
        self.assertIn("错误类型分布", wrong)

    def test_dashboard_template_includes_error_distribution(self):
        plans = read(REFS / "review-plans.md")
        self.assertIn("错误类型分布", plans)


class PacingContract(unittest.TestCase):
    def test_mock_documents_pacing(self):
        text = read(REFS / "practice-workflows.md")
        self.assertIn("Pacing", text)
        self.assertIn("节奏复盘", text)


class CramAnxietyContract(unittest.TestCase):
    def test_cram_handles_anxiety(self):
        text = read(REFS / "review-plans.md")
        self.assertIn("Managing Exam Anxiety", text)
        self.assertIn("quick win", text.lower())


class IntegrityContract(unittest.TestCase):
    def test_skill_states_academic_integrity(self):
        text = read(ROOT / "SKILL.md")
        self.assertIn("Academic Integrity", text)
        self.assertIn("proxy", text.lower())

    def test_readme_states_academic_integrity(self):
        text = read(ROOT / "README.md")
        self.assertIn("integrity", text.lower())


class CapabilityProbeContract(unittest.TestCase):
    def test_detection_order_documented(self):
        text = read(REFS / "environment-adaptation.md")
        self.assertIn("Detection Order", text)


class RoutingMapContract(unittest.TestCase):
    """The SKILL.md quick routing map must not drift from INDEX.md commands."""

    INDEX_ROW_RE = re.compile(r"^\|\s*`(?P<command>/[a-z][a-z0-9-]*)(?:\s+[^`]*)?`\s*\|")

    def _index_commands(self) -> set[str]:
        commands = set()
        for line in read(REFS / "INDEX.md").splitlines():
            m = self.INDEX_ROW_RE.match(line)
            if m:
                commands.add(m.group("command"))
        return commands

    def _quick_map_commands(self) -> set[str]:
        text = read(ROOT / "SKILL.md")
        start = text.index("Quick routing map")
        end = text.index("Then, before executing", start)
        block = text[start:end]
        return set(re.findall(r"`(/[a-z][a-z0-9-]*)`", block))

    def test_quick_map_commands_are_all_registered(self):
        index = self._index_commands()
        quick = self._quick_map_commands()
        self.assertTrue(quick, "quick routing map parsed to empty set")
        unregistered = sorted(quick - index)
        self.assertEqual(unregistered, [],
                         f"SKILL.md quick map references commands missing from INDEX.md: {unregistered}")


class StagedReviewWorkflowContract(unittest.TestCase):
    def test_stage_one_priority_table_is_documented(self):
        staged = read(REFS / "staged-review-workflow.md")
        self.assertIn("Most Worth Studying Chapters", staged)
        self.assertIn("Exam-scope weight", staged)
        self.assertIn("Past-paper frequency", staged)
        self.assertIn("Teacher-emphasis strength", staged)
        self.assertIn("| Priority | Chapter/topic | Exam-scope weight | Past-paper frequency | Teacher emphasis |", staged)
        self.assertIn("P0", staged)
        self.assertIn("P1", staged)
        self.assertIn("P2", staged)

    def test_materials_and_plan_reuse_stage_one_priority_contract(self):
        materials = read(REFS / "materials-ingestion.md")
        plans = read(REFS / "review-plans.md")
        for text in [materials, plans]:
            self.assertIn("exam-scope weight", text.lower())
            self.assertIn("past-paper frequency", text.lower())
            self.assertIn("teacher-emphasis strength", text.lower())
            self.assertIn("P0", text)


class FocusFeedbackIterationContract(unittest.TestCase):
    def test_focus_feedback_iteration_contract_exists(self):
        text = read(REFS / "focus-feedback-iteration.md")
        for phrase in [
            "Focus",
            "Feedback",
            "Iteration",
            "本轮闭环",
            "repair, repeat, interleave, escalate, de-prioritize, or schedule",
        ]:
            self.assertIn(phrase, text)

    def test_core_workflows_reference_focus_feedback_iteration(self):
        for path in [
            ROOT / "SKILL.md",
            REFS / "materials-ingestion.md",
            REFS / "practice-workflows.md",
            REFS / "learning-strategies.md",
            REFS / "review-plans.md",
            REFS / "staged-review-workflow.md",
        ]:
            text = read(path)
            self.assertIn("focus-feedback-iteration.md", text, f"{path.name} does not reference the loop contract")

    def test_materials_output_includes_loop_footer(self):
        text = read(REFS / "materials-ingestion.md")
        self.assertIn("## 本轮闭环", text)
        self.assertIn("重点:", text)
        self.assertIn("反馈:", text)
        self.assertIn("下一轮:", text)


class OptInReminderContract(unittest.TestCase):
    def test_reminders_are_explicit_opt_in_only(self):
        text = read(REFS / "opt-in-reminders.md")
        lower = text.lower()
        for phrase in [
            "opt-in only",
            "never enable proactive messages by default",
            "never send or schedule background messages unless the user has explicitly",
            "if the user asks for a one-time digest, generate only that digest",
        ]:
            self.assertIn(phrase, lower)

    def test_daily_and_weekly_digest_contracts_cover_weak_points_and_memory(self):
        text = read(REFS / "opt-in-reminders.md")
        for phrase in [
            "Daily Knowledge Digest",
            "Weekly Knowledge Digest",
            "每日知识归纳卷",
            "每周知识归纳卷",
            "P0/P1",
            "必背清单",
            "薄弱板块",
            "今日到期复习",
            "反复薄弱板块",
            "章节优先级更新",
            "本轮闭环",
        ]:
            self.assertIn(phrase, text)

    def test_shared_agent_contract_exposes_reminder_capabilities(self):
        contract = read(REFS / "agent-adapter-contract.md")
        optimization = read(REFS / "agent-optimization.md")
        for phrase in ["proactive-message", "scheduler"]:
            self.assertIn(phrase, contract)
            self.assertIn(phrase, optimization)
        self.assertIn("reminder-agent", optimization)
        self.assertIn("explicit user opt-in", optimization)

    def test_openclaw_and_hermes_use_opt_in_reminder_path_only_conditionally(self):
        for name in ["openclaw.yaml", "hermes.yaml"]:
            text = read(ROOT / "agents" / name)
            self.assertIn("Opt-in reminders", text)
            self.assertIn("references/opt-in-reminders.md", text)
            self.assertIn("if and only if", text)
            self.assertIn("explicitly asks", text)
            self.assertIn("never send or schedule background", text)


if __name__ == "__main__":
    unittest.main()
