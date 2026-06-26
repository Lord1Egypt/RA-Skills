import os
import sys
import unittest
from unittest.mock import patch


SCRIPT_DIR = os.path.join("D:\\skill", "meeting-minutes-qa-tts", "scripts")
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from generate_summary_audio import generate_summary_audio


class GenerateSummaryAudioTests(unittest.TestCase):
    def test_summary_text_is_forwarded_directly_to_tts(self) -> None:
        with patch("generate_summary_audio.generate_meeting_audio") as mock_generate:
            mock_generate.return_value = '{"status":"ok"}'
            result = generate_summary_audio(
                summary_text="这是简短总结。",
                output_path="D:/skill/out.mp3",
                api_key="tts-key",
            )

        self.assertEqual(result, '{"status":"ok"}')
        mock_generate.assert_called_once_with(
            input_text="这是简短总结。",
            output_path="D:/skill/out.mp3",
            mode="full_text",
            voice_id=None,
            api_key="tts-key",
        )


if __name__ == "__main__":
    unittest.main()
