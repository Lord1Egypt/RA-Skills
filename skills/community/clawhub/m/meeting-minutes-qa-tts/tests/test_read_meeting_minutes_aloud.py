import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from read_meeting_minutes_aloud import read_meeting_minutes_aloud


class ReadMeetingMinutesAloudTests(unittest.TestCase):
    def test_missing_file_returns_error(self) -> None:
        result = read_meeting_minutes_aloud("D:\\skill\\meeting-minutes-retriever\\missing.txt")
        self.assertTrue(result.startswith("ERROR: Local file does not exist:"))

    def test_reads_local_file_then_reports_missing_api_key(self) -> None:
        sample_path = Path("D:/skill/meeting-minutes-retriever/sample_meeting.txt")
        self.assertTrue(sample_path.exists())

        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": ""}, clear=False):
            result = read_meeting_minutes_aloud(str(sample_path))

        self.assertEqual(
            result,
            "ERROR: Missing SenseAudio API key. Set SENSEAUDIO_API_KEY or provide --api-key.",
        )

    def test_env_api_key_is_used_when_no_user_key_is_provided(self) -> None:
        sample_path = Path("D:/skill/meeting-minutes-retriever/sample_meeting.txt")

        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": "env-key"}, clear=False):
            with patch("read_meeting_minutes_aloud.generate_meeting_audio") as mock_generate:
                mock_generate.return_value = '{"status": "ok"}'
                result = read_meeting_minutes_aloud(
                    str(sample_path),
                    output_path="D:/skill/custom-output.mp3",
                )

        self.assertEqual(result, '{"status": "ok"}')
        mock_generate.assert_called_once()
        _, kwargs = mock_generate.call_args
        self.assertIsNone(kwargs["api_key"])
        self.assertEqual(kwargs["output_path"], "D:/skill/custom-output.mp3")

    def test_user_provided_api_key_is_forwarded(self) -> None:
        sample_path = Path("D:/skill/meeting-minutes-retriever/sample_meeting.txt")

        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": ""}, clear=False):
            with patch("read_meeting_minutes_aloud.generate_meeting_audio") as mock_generate:
                mock_generate.return_value = '{"status": "ok"}'
                result = read_meeting_minutes_aloud(
                    str(sample_path),
                    output_path="D:/skill/custom-output.mp3",
                    api_key="user-key",
                )

        self.assertEqual(result, '{"status": "ok"}')
        mock_generate.assert_called_once()
        _, kwargs = mock_generate.call_args
        self.assertEqual(kwargs["api_key"], "user-key")
        self.assertEqual(kwargs["output_path"], "D:/skill/custom-output.mp3")


if __name__ == "__main__":
    unittest.main()
