from __future__ import annotations

import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import peco_loop


class TestUtilityFunctions(unittest.TestCase):
    def test_normalize_human_task_compacts_spaces_and_case(self) -> None:
        raw = "  Need   OTP   Code  "
        self.assertEqual(peco_loop.normalize_human_task(raw), "need otp code")

    def test_merge_override_text_with_feishu_section(self) -> None:
        merged = peco_loop.merge_override_text("run task A", "ticket-1 resolved")
        self.assertEqual(
            merged,
            "run task A\n\n[FEISHU_RESOLVED_TASKS]\nticket-1 resolved",
        )

    def test_extract_markdown_section_returns_desire_block(self) -> None:
        text = """# Worker Soul

## Infinite Oracle Desire
Deliver compounding leverage.
Prefer reusable automation over one-off output.

## Other Section
Ignore this.
"""
        self.assertEqual(
            peco_loop.extract_markdown_section(text, peco_loop.DESIRE_SECTION_TITLE),
            "Deliver compounding leverage.\nPrefer reusable automation over one-off output.",
        )

    def test_build_loop_prompt_includes_desire_anchor(self) -> None:
        state = peco_loop.LoopState(
            objective="Automate research",
            worker_desire="Turn every cycle into reusable capability.",
            session="peco-session",
            phase="PLAN",
        )

        prompt = peco_loop.build_loop_prompt(state, override_text="")

        self.assertIn(
            "worker_desire: Turn every cycle into reusable capability.", prompt
        )
        self.assertIn("[DESIRE ANCHOR]", prompt)
        self.assertIn("desire_alignment", prompt)

    def test_parse_structured_output_requires_plan_desire_alignment(self) -> None:
        raw = """[PHASE:PLAN]
```json
{
  "phase": "PLAN",
  "next_phase": "EXECUTE",
  "decision": "continue",
  "confidence": 0.8,
  "summary": "plan ready",
  "phase_payload": {
    "objective_slice": "ship desire-aware planning",
    "candidates": ["path-a"],
    "chosen_plan": "path-a",
    "acceptance_checks": ["check-a"],
    "blocked_by_human": false
  },
  "risks": []
}
```
"""

        with self.assertRaises(peco_loop.ParseError):
            peco_loop.parse_structured_output(raw, expected_phase="PLAN")


class TestFeishuSync(unittest.TestCase):
    def _make_sync(self) -> peco_loop.FeishuSync:
        logger = logging.getLogger("peco-loop-test")
        logger.handlers.clear()
        logger.addHandler(logging.NullHandler())
        return peco_loop.FeishuSync(
            app_id="app_id",
            app_secret="app_secret",
            app_token="app_token",
            progress_table_id="progress_table",
            human_table_id="human_table",
            base_url="https://open.feishu.cn",
            timeout=10,
            logger=logger,
        )

    def test_ensure_field_maps_supports_execution_time_column(self) -> None:
        sync = self._make_sync()
        with patch.object(
            sync,
            "_list_table_fields",
            side_effect=[
                ["会话ID", "轮次", "阶段", "摘要", "状态", "执行时间"],
                ["问题描述", "状态", "Agent已读取", "解决方案", "时间"],
            ],
        ):
            sync._ensure_field_maps()

        self.assertEqual(sync._progress_field_map["timestamp_text"], "执行时间")

    def test_append_progress_writes_timestamp_with_second_precision(self) -> None:
        sync = self._make_sync()
        sync._progress_field_map = {
            "session": "Session",
            "iteration": "Iteration",
            "phase": "Phase",
            "summary": "Summary",
            "status": "Status",
            "timestamp": "时间戳",
            "timestamp_text": "执行时间",
        }
        sync._create_record = Mock(return_value=True)
        sync._ensure_field_maps = Mock(return_value=None)

        with (
            patch("peco_loop.time.time", return_value=1700000000.123),
            patch("peco_loop.datetime") as datetime_mock,
        ):
            datetime_mock.now.return_value.strftime.return_value = "2026-03-02 12:34:56"
            ok = sync.append_progress(
                session="peco-session",
                iteration=3,
                phase="EXECUTE",
                summary="ran automation",
                status="continue",
            )

        self.assertTrue(ok)
        sync._create_record.assert_called_once()
        _, fields = sync._create_record.call_args.args
        self.assertEqual(fields["时间戳"], 1700000000123)
        self.assertEqual(fields["执行时间"], "2026-03-02 12:34:56")

    def test_append_human_task_writes_timestamp_with_second_precision(self) -> None:
        sync = self._make_sync()
        sync._human_field_map = {
            "desc": "问题描述",
            "status": "状态",
            "read": "Agent已读取",
            "resolution": "解决方案",
            "timestamp": "时间戳",
            "timestamp_text": "更新时间",
        }
        sync._create_record = Mock(return_value=True)
        sync.has_human_task = Mock(return_value=False)
        sync._ensure_field_maps = Mock(return_value=None)

        with (
            patch("peco_loop.time.time", return_value=1700000000.123),
            patch("peco_loop.datetime") as datetime_mock,
        ):
            datetime_mock.now.return_value.strftime.return_value = "2026-03-02 12:34:56"
            ok = sync.append_human_task("Need OTP code")

        self.assertTrue(ok)
        sync._create_record.assert_called_once()
        _, fields = sync._create_record.call_args.args
        self.assertEqual(fields["状态"], "待处理")
        self.assertEqual(fields["Agent已读取"], False)
        self.assertEqual(fields["时间戳"], 1700000000123)
        self.assertEqual(fields["更新时间"], "2026-03-02 12:34:56")

    def test_append_human_task_skips_duplicates(self) -> None:
        sync = self._make_sync()
        sync.has_human_task = Mock(return_value=True)
        sync._create_record = Mock(return_value=True)
        sync._human_field_map = {
            "desc": "问题描述",
            "status": "状态",
            "read": "Agent已读取",
        }

        ok = sync.append_human_task("Same blocker")

        self.assertFalse(ok)
        sync._create_record.assert_not_called()


class TestBacklogBehavior(unittest.TestCase):
    def test_append_human_task_backlog_dedupes_local_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            backlog_file = Path(tmp_dir) / "backlog.txt"
            backlog_file.write_text(
                "[2026-03-02T00:00:00+00:00] session=s1 iteration=1 phase=EXECUTE task=Need OTP\n",
                encoding="utf-8",
            )
            state = peco_loop.LoopState(objective="obj", session="s1", iteration=2)
            parsed = peco_loop.ParsedResponse(
                phase="EXECUTE",
                next_phase="CHECK",
                decision="continue",
                confidence=0.8,
                summary="ok",
                human_task="Need OTP",
                phase_payload={},
                risks=[],
                raw_json={},
            )

            logger = logging.getLogger("peco-loop-backlog-test")
            logger.handlers.clear()
            logger.addHandler(logging.NullHandler())

            notifier = Mock()
            feishu_sync = Mock()

            count = peco_loop.append_human_task_backlog(
                backlog_file=backlog_file,
                state=state,
                parsed=parsed,
                logger=logger,
                notifier=notifier,
                feishu_sync=feishu_sync,
            )

            self.assertEqual(count, 1)
            notifier.notify.assert_not_called()
            feishu_sync.append_human_task.assert_not_called()
            lines = backlog_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)


if __name__ == "__main__":
    unittest.main()
