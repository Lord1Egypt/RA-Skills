#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notion_db_weekly_report_generator import ValidationError, run, validate_payload


BASE_PAYLOAD = {
    "user_id": "u005",
    "week_label": "2026-W10",
    "records": [
        {"title": "落地页改版", "owner": "小王", "status": "进行中", "progress": 70},
        {"title": "投放素材更新", "owner": "小李", "status": "已完成", "progress": 100},
        {"title": "埋点修复", "owner": "小张", "status": "进行中", "progress": 35},
    ],
}


class NotionDbWeeklyReportGeneratorTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["week_label"], "2026-W10")

    def test_validate_payload_empty_records(self):
        payload = dict(BASE_PAYLOAD)
        payload["records"] = []
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_free_success(self):
        result = run(BASE_PAYLOAD)
        self.assertTrue(result["success"])
        self.assertIn("## 数据概览", result["report"]["markdown"])

    def test_run_premium_upgrade_required(self):
        payload = dict(BASE_PAYLOAD)
        payload["tier"] = "premium"
        result = run(payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "PREMIUM_UPGRADE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
