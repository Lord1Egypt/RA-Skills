import datetime as dt
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import recruiting_sync


class RecruitingSyncTests(unittest.TestCase):
    def test_format_due(self) -> None:
        self.assertEqual("2026-04-01 09:00:00", recruiting_sync.format_due("2026-04-01 09:00"))
        self.assertEqual("2026-04-01 09:00:30", recruiting_sync.format_due("2026-04-01 09:00:30"))

    def test_parse_bridge_row(self) -> None:
        result = recruiting_sync.parse_bridge_row("id123\tOpenClaw\t测试标题")
        self.assertEqual("id123", result["id"])
        self.assertEqual("OpenClaw", result["list"])
        self.assertEqual("测试标题", result["title"])

    def test_scan_emails_returns_json(self) -> None:
        """验证扫描模式返回正确格式的 JSON。"""
        args = type('Args', (), {
            'mail_account': '谷歌', 'mailbox': 'INBOX',
            'days': 2, 'max_results': 10, 'output': '/tmp/state.json', 'dry_run': False
        })()

        mock_messages = [
            recruiting_sync.MailMessage(
                message_id="msg-1", subject="测试邮件", sender="test@example.com",
                received_at=dt.datetime(2026, 4, 1, 10, 0), account="谷歌", mailbox="INBOX"
            )
        ]

        with patch.object(recruiting_sync, 'list_recent_mail_messages', return_value=mock_messages):
            with patch.object(recruiting_sync, 'fetch_mail_bodies_batch', return_value={"谷歌|INBOX|msg-1": "邮件正文"}):
                # 捕获 stdout
                import io
                import sys
                captured_output = io.StringIO()
                sys.stdout = captured_output
                try:
                    recruiting_sync.scan_emails(args)
                finally:
                    sys.stdout = sys.__stdout__

                output = captured_output.getvalue()
                import json
                result = json.loads(output)
                self.assertIn("emails", result)
                self.assertEqual(1, len(result["emails"]))
                self.assertEqual("msg-1", result["emails"][0]["message_id"])

    def test_apply_events_creates_reminders(self) -> None:
        """验证应用事件模式正确处理事件。"""
        import tempfile
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            events_file = Path(tmpdir) / "events.json"
            events_file.write_text(json.dumps({
                "events": [{
                    "id": "test-001", "company": "测试公司", "event_type": "interview",
                    "title": "测试公司面试", "timing": {"start": "2026-04-05 14:00"},
                    "role": "后端开发", "link": "https://example.com", "message_id": "msg-1"
                }]
            }))

            args = type('Args', (), {
                'apply_events': str(events_file), 'output': str(Path(tmpdir) / "state.json"),
                'dry_run': True
            })()

            with patch.object(recruiting_sync, 'sync_to_reminders') as mock_sync:
                mock_sync.return_value = {"created": 1, "updated": 0, "deleted": 0}
                recruiting_sync.apply_events(args)
                mock_sync.assert_called_once()
                events_arg = mock_sync.call_args[0][0]
                self.assertEqual(1, len(events_arg))
                self.assertEqual("测试公司", events_arg[0].company)


if __name__ == "__main__":
    unittest.main()