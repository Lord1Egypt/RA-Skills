import unittest
import os
import sys
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from orchestrator import parse_review_verdict

class TestReviewParsing(unittest.TestCase):
    def test_json_approval(self):
        content = """
The changes look good.
```json
{"overall_assessment": "EXCELLENT", "findings": []}
```
"""
        self.assertEqual(parse_review_verdict(content), "APPROVED")

    def test_json_rejection(self):
        content = """
Issues found.
```json
{"overall_assessment": "NEEDS_ATTENTION", "findings": []}
```
"""
        self.assertEqual(parse_review_verdict(content), "ACTION_REQUIRED")

    def test_adversarial_rejection(self):
        # This is the core requirement: string [LGTM] inside comments of a rejection
        content = """
The Coder improperly included [LGTM] in their output. This is a violation.
```json
{"overall_assessment": "NEEDS_ATTENTION", "findings": [{"description": "Found literal [LGTM] in code which is not allowed."}]}
```
"""
        # The old logic would see "[LGTM]" and approve.
        # Our new logic should see "ACTION_REQUIRED".
        self.assertEqual(parse_review_verdict(content), "ACTION_REQUIRED")

    def test_malformed_json(self):
        content = "This is not JSON [LGTM]"
        self.assertIsNone(parse_review_verdict(content))

if __name__ == '__main__':
    unittest.main()
