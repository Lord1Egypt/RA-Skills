#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from meeting_minutes_task_extractor import ValidationError, run, validate_payload


BASE_PAYLOAD = {
    "user_id": "u002",
    "meeting_title": "增长周会",
    "meeting_notes": "1) 由小王负责落地页改版，截止2026-03-08\n2) TODO: 市场组完成渠道复盘\n3) 需要本周完成投放预算重排",
}


class MeetingMinutesTaskExtractorTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["meeting_title"], "增长周会")

    def test_validate_payload_invalid_notes(self):
        payload = dict(BASE_PAYLOAD)
        payload["meeting_notes"] = "太短"
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_free_success(self):
        result = run(BASE_PAYLOAD)
        self.assertTrue(result["success"])
        self.assertGreaterEqual(result["summary"]["task_count"], 1)
        self.assertTrue(result["upgrade"]["premium_available"])

    def test_run_premium_upgrade_required(self):
        payload = dict(BASE_PAYLOAD)
        payload["tier"] = "premium"
        result = run(payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "PREMIUM_UPGRADE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
