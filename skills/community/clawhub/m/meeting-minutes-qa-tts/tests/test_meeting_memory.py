import json
import shutil
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from meeting_memory import load_meeting_memory, save_meeting_memory


class MeetingMemoryTests(unittest.TestCase):
    def test_save_and_load_meeting_memory(self) -> None:
        temp_dir = Path("D:/skill/meeting-minutes-qa-tts/tests/tmp_memory")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        try:
            memory_path = temp_dir / "meeting.json"
            saved = save_meeting_memory(
                source_location="D:/skill/sample.txt",
                meeting_text="会议原文",
                summary_text="会议总结",
                memory_path=str(memory_path),
            )
            self.assertEqual(saved, str(memory_path.resolve()))
            loaded = load_meeting_memory(str(memory_path))
            self.assertEqual(loaded["meeting_text"], "会议原文")
            self.assertEqual(loaded["summary_text"], "会议总结")
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
