import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from create_meeting_answer_audio import create_meeting_answer_audio
from create_meeting_summary_audio_session import create_meeting_summary_audio_session


class CreateMeetingAudioFlowsTests(unittest.TestCase):
    def test_create_summary_audio_session_returns_memory_and_output(self) -> None:
        with patch("create_meeting_summary_audio_session.read_text_source") as mock_read:
            with patch("create_meeting_summary_audio_session.save_meeting_memory") as mock_save:
                with patch("create_meeting_summary_audio_session.generate_summary_audio") as mock_audio:
                    mock_read.return_value = "会议原文"
                    mock_save.return_value = "D:/skill/memory/latest_meeting.json"
                    mock_audio.return_value = json.dumps(
                        {"status": "ok", "output_path": "D:/skill/summary.mp3"}
                    )
                    result = create_meeting_summary_audio_session(
                        location="D:/skill/meeting.txt",
                        summary_text="会议摘要",
                        output_path="D:/skill/summary.mp3",
                        api_key="tts-key",
                    )

        parsed = json.loads(result)
        self.assertEqual(parsed["output_path"], "D:/skill/summary.mp3")
        self.assertEqual(parsed["memory_path"], "D:/skill/memory/latest_meeting.json")
        self.assertEqual(parsed["summary_text"], "会议摘要")

    def test_create_answer_audio_returns_text_answer_and_output(self) -> None:
        with patch("create_meeting_answer_audio.load_meeting_memory") as mock_load:
            with patch("create_meeting_answer_audio.answer_meeting_question_audio") as mock_audio:
                mock_load.return_value = {"source_location": "D:/skill/meeting.txt"}
                mock_audio.return_value = json.dumps(
                    {"status": "ok", "output_path": "D:/skill/answer.mp3"}
                )
                result = create_meeting_answer_audio(
                    answer_text="这是会议问题的回答。",
                    output_path="D:/skill/answer.mp3",
                    api_key="tts-key",
                )

        parsed = json.loads(result)
        self.assertEqual(parsed["text_answer"], "这是会议问题的回答。")
        self.assertEqual(parsed["output_path"], "D:/skill/answer.mp3")
        self.assertEqual(parsed["memory_source_location"], "D:/skill/meeting.txt")
        self.assertTrue(parsed["memory_loaded"])

    def test_create_answer_audio_allows_missing_default_memory(self) -> None:
        with patch("create_meeting_answer_audio.load_meeting_memory") as mock_load:
            with patch("create_meeting_answer_audio.answer_meeting_question_audio") as mock_audio:
                mock_load.side_effect = FileNotFoundError("default memory missing")
                mock_audio.return_value = json.dumps(
                    {"status": "ok", "output_path": "D:/skill/answer.mp3"}
                )
                result = create_meeting_answer_audio(
                    answer_text="这是不依赖 memory 的回答。",
                    output_path="D:/skill/answer.mp3",
                    api_key="tts-key",
                )

        parsed = json.loads(result)
        self.assertEqual(parsed["text_answer"], "这是不依赖 memory 的回答。")
        self.assertEqual(parsed["output_path"], "D:/skill/answer.mp3")
        self.assertEqual(parsed["memory_source_location"], None)
        self.assertFalse(parsed["memory_loaded"])
        self.assertTrue(parsed["memory_path"].endswith("memory\\latest_meeting.json"))

    def test_create_answer_audio_still_requires_explicit_memory_path(self) -> None:
        with patch("create_meeting_answer_audio.load_meeting_memory") as mock_load:
            with patch("create_meeting_answer_audio.answer_meeting_question_audio") as mock_audio:
                mock_load.side_effect = FileNotFoundError("explicit memory missing")
                mock_audio.return_value = json.dumps(
                    {"status": "ok", "output_path": "D:/skill/answer.mp3"}
                )

                with self.assertRaises(FileNotFoundError):
                    create_meeting_answer_audio(
                        answer_text="回答",
                        output_path="D:/skill/answer.mp3",
                        api_key="tts-key",
                        memory_path="D:/skill/custom-memory.json",
                    )


if __name__ == "__main__":
    unittest.main()
