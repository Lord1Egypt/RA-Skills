import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_meeting_audio import read_text_source


class ReadMeetingTextTests(unittest.TestCase):
    def test_reads_local_text_file(self) -> None:
        sample_path = Path("D:/skill/meeting-minutes-summary-tts/tests/fixtures/sample_meeting.txt")
        self.assertTrue(sample_path.exists())
        result = read_text_source(str(sample_path))
        self.assertIn("Decision: ship the retriever.", result)


if __name__ == "__main__":
    unittest.main()
