import os
import sys
import unittest
from unittest.mock import patch


SCRIPT_DIR = os.path.join("D:\\skill", "meeting-minutes-qa-tts", "scripts")
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from answer_meeting_question_audio import answer_meeting_question_audio


class AnswerMeetingQuestionAudioTests(unittest.TestCase):
    def test_answer_text_is_forwarded_to_tts(self) -> None:
        with patch("answer_meeting_question_audio.generate_summary_audio") as mock_generate:
            mock_generate.return_value = '{"status":"ok"}'
            result = answer_meeting_question_audio(
                answer_text="这次会议里决定先做检索器。",
                output_path="D:/skill/out.mp3",
                api_key="tts-key",
            )

        self.assertEqual(result, '{"status":"ok"}')
        mock_generate.assert_called_once_with(
            summary_text="这次会议里决定先做检索器。",
            output_path="D:/skill/out.mp3",
            voice_id=None,
            api_key="tts-key",
        )


if __name__ == "__main__":
    unittest.main()
