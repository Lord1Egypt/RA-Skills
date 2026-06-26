import unittest
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from notification_formatter import format_notification

class TestSyncNotifications(unittest.TestCase):
    def test_github_sync_start(self):
        msg = format_notification("github_sync_start", {"pr_id": "PR_001"})
        self.assertEqual(msg, "Synchronizing code to GitHub...")

    def test_github_sync_complete(self):
        msg = format_notification("github_sync_complete", {"pr_id": "PR_001"})
        self.assertEqual(msg, "GitHub sync complete.")

if __name__ == "__main__":
    unittest.main()
