#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from github_issue_reply_assistant import ValidationError, run, validate_payload


BASE_PAYLOAD = {
    "user_id": "u003",
    "repo": "openclaw/openclaw",
    "issue_title": "Bug: login flow crashes",
    "issue_body": "When I click login, app crashes on callback page with 500 error.",
}


class GithubIssueReplyAssistantTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["repo"], "openclaw/openclaw")

    def test_validate_payload_invalid_repo(self):
        payload = dict(BASE_PAYLOAD)
        payload["repo"] = "bad_repo"
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_free_success(self):
        result = run(BASE_PAYLOAD)
        self.assertTrue(result["success"])
        self.assertIn("suggestion", result)
        self.assertTrue(result["upgrade"]["premium_available"])

    def test_run_premium_upgrade_required(self):
        payload = dict(BASE_PAYLOAD)
        payload["tier"] = "premium"
        result = run(payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "PREMIUM_UPGRADE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
