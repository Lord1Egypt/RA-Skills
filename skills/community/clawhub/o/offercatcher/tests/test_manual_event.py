import argparse
import tempfile
import unittest
from pathlib import Path

from scripts import manual_event


class ManualEventTests(unittest.TestCase):
    def test_format_due(self) -> None:
        self.assertEqual("2026-04-01 09:00", manual_event.format_due("2026-04-01 09:00"))
        self.assertEqual("2026-04-01 09:00:30", manual_event.format_due("2026-04-01 09:00:30"))

    def test_build_manual_entry(self) -> None:
        args = argparse.Namespace(
            title="重要事件",
            due="2026-04-01 10:00",
            notes="入口：https://example.com",
            priority="high",
            list="OpenClaw",
            account="iCloud",
        )
        event_id, entry = manual_event.build_manual_entry(args, {"id": "r1"})
        self.assertTrue(event_id)
        self.assertEqual("manual_note", entry["eventType"])
        self.assertEqual("r1", entry["reminder"]["id"])

    def test_write_and_load_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            state = manual_event.load_state(path)
            state["processed"]["x"] = {"title": "t"}
            manual_event.write_state(path, state)
            loaded = manual_event.load_state(path)
            self.assertIn("x", loaded["processed"])

    def test_manual_source_becomes_multi_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            manual_event.write_state(
                path,
                {
                    "schemaVersion": 2,
                    "list": "OpenClaw",
                    "account": "iCloud",
                    "source": "apple_mail",
                    "processed": {},
                    "review": [],
                },
            )
            state = manual_event.load_state(path)
            args = argparse.Namespace(
                title="重要事件",
                due="2026-04-01 10:00",
                notes="n",
                priority="high",
                list="OpenClaw",
                account="iCloud",
            )
            event_id, entry = manual_event.build_manual_entry(args, {"id": "r1"})
            state["processed"][event_id] = entry
            if state.get("source") and state.get("source") != "manual_event":
                state["source"] = "multi_source"
            else:
                state["source"] = "manual_event"
            self.assertEqual("multi_source", state["source"])


if __name__ == "__main__":
    unittest.main()
