import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from integrations.feishu.feishu_image_bot import (  # noqa: E402
    AnalysisSnapshot,
    ChatSettings,
    GoNextMoveFeishuBot,
    ProcessedMessageStore,
    format_analysis_text,
    format_elapsed,
    help_text,
    parse_settings_command,
    unsupported_text,
)


class FeishuBotTests(unittest.TestCase):
    def test_processed_message_store_persists_seen_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "processed.json"
            store = ProcessedMessageStore(path)

            self.assertTrue(store.add_if_new("om_1"))
            self.assertFalse(store.add_if_new("om_1"))

            reloaded = ProcessedMessageStore(path)
            self.assertFalse(reloaded.add_if_new("om_1"))
            self.assertTrue(reloaded.add_if_new("om_2"))

    def test_stale_message_detection_uses_start_time_margin(self):
        bot = object.__new__(GoNextMoveFeishuBot)
        bot.started_at_ms = 1_000_000

        stale = SimpleNamespace(create_time="930000")
        recent = SimpleNamespace(create_time="940000")
        invalid = SimpleNamespace(create_time="not-a-timestamp")

        self.assertTrue(bot._is_stale_message(stale))
        self.assertFalse(bot._is_stale_message(recent))
        self.assertFalse(bot._is_stale_message(invalid))

    def test_help_text_explains_explicit_commands(self):
        text = help_text(ChatSettings())

        self.assertIn("不会用 LLM", text)
        self.assertIn("获取帮助：帮助", text)
        self.assertIn("当前设置", text)

    def test_unsupported_text_points_to_help(self):
        text = unsupported_text()

        self.assertIn("不使用 LLM", text)
        self.assertIn("发送“帮助”", text)

    def test_format_analysis_text_includes_elapsed_time(self):
        result = {
            "visits_requested": 400,
            "recommendation": {
                "move": "D4",
                "visits": 123,
                "winrate": 0.55,
                "scoreLead": 1.25,
            }
        }

        text = format_analysis_text(result, ChatSettings(), elapsed_seconds=3.24)

        self.assertIn("推荐：黑棋走 D4", text)
        self.assertIn("耗时：3.2秒", text)
        self.assertIn("搜索预算：400", text)

    def test_format_elapsed_rounds_longer_durations(self):
        self.assertEqual(format_elapsed(1.24), "1.2秒")
        self.assertEqual(format_elapsed(12.4), "12秒")

    def test_help_alias_question_mark(self):
        self.assertEqual(parse_settings_command("帮助"), "help")
        self.assertEqual(parse_settings_command("/help"), "help")

    def test_parse_feedback_commands(self):
        self.assertEqual(parse_settings_command("上报"), "feedback")
        self.assertEqual(parse_settings_command("报错"), "feedback")
        self.assertEqual(parse_settings_command("识别错"), "feedback")
        self.assertEqual(parse_settings_command("反馈"), "feedback")

    def test_parse_settings_command_accepts_expert_level(self):
        command = parse_settings_command("设置 白 特级")

        self.assertEqual(command.side_to_move, "white")
        self.assertEqual(command.level, "expert")

    def test_chat_settings_visit_budget_uses_four_level_scale(self):
        self.assertEqual(ChatSettings(level="beginner").visit_budget(400), 100)
        self.assertEqual(ChatSettings(level="intermediate").visit_budget(400), 200)
        self.assertEqual(ChatSettings(level="advanced").visit_budget(400), 300)
        self.assertEqual(ChatSettings(level="expert").visit_budget(400), 400)

    def test_feedback_requires_configured_directory(self):
        bot = object.__new__(GoNextMoveFeishuBot)
        bot.config = SimpleNamespace(feedback_dir=None)

        text = bot._handle_feedback("chat_1", "report_1")

        self.assertIn("FEISHU_FEEDBACK_DIR", text)

    def test_feedback_requires_recent_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = object.__new__(GoNextMoveFeishuBot)
            bot.config = SimpleNamespace(feedback_dir=Path(tmp))
            bot._recent_analysis_lock = threading.Lock()
            bot._recent_analysis_by_chat = {}

            text = bot._handle_feedback("chat_1", "report_1")

            self.assertIn("还没有可上报", text)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_feedback_writes_input_output_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "input-source.jpg"
            output_path = tmp_path / "output-source.jpg"
            input_path.write_bytes(b"input")
            output_path.write_bytes(b"output")

            bot = object.__new__(GoNextMoveFeishuBot)
            bot.config = SimpleNamespace(feedback_dir=tmp_path / "feedback")
            bot.log = SimpleNamespace(info=lambda *args, **kwargs: None, exception=lambda *args, **kwargs: None)
            bot._recent_analysis_lock = threading.Lock()
            bot._recent_analysis_by_chat = {
                "chat_1": AnalysisSnapshot(
                    chat_id="chat_1",
                    message_id="om_1",
                    settings=ChatSettings(side_to_move="white", level="expert"),
                    input_image=input_path,
                    output_image=output_path,
                    result={
                        "recommendation": {"move": "D4"},
                        "timings": {"total_seconds": 1.25},
                    },
                    created_at=1_800_000_000.0,
                )
            }

            text = bot._handle_feedback("chat_1", "report_1")

            self.assertIn("已保存", text)
            sample_dirs = list((tmp_path / "feedback").iterdir())
            self.assertEqual(len(sample_dirs), 1)
            sample_dir = sample_dirs[0]
            self.assertEqual((sample_dir / "input.jpg").read_bytes(), b"input")
            self.assertEqual((sample_dir / "output.jpg").read_bytes(), b"output")
            metadata = json.loads((sample_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["analysis_message_id"], "om_1")
            self.assertEqual(metadata["report_message_id"], "report_1")
            self.assertEqual(metadata["settings"]["side_to_move"], "white")
            self.assertEqual(metadata["recommendation"]["move"], "D4")


if __name__ == "__main__":
    unittest.main()
