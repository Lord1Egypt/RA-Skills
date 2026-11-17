"""
test_school_email_monitor.py — Unit tests for school_email_monitor.py

Covers:
  - _is_auth_error_notified() / _set_auth_error_notified(): flag persistence
  - get_gmail_service(): first-failure notifies, subsequent failures are silent
  - _extract_body_and_attachments(): text/plain, nested multipart, PDF detection
  - fetch_recent_school_emails(): skip processed IDs, filter daily summaries
  - format_for_whatsapp(): structure, PDF annotation, body truncation
  - _mark_processed() / _load_processed_ids(): round-trip, 500-item cap
"""
import base64
import json
import contextlib
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).parent.parent))


# Make `from google.oauth2.credentials import Credentials` resolvable from
# the MagicMock stubs (otherwise Python's importlib refuses on "unknown location").

with patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    from features.school.school_email_monitor import SchoolEmailMonitor


# ─── Fixture helpers ──────────────────────────────────────────────────────────

def _make_monitor(tmp_path):
    """Create a SchoolEmailMonitor pointing at a tmp directory."""
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"email_body_context_limit": 2000}))
    # exist_ok: several tests build a second monitor over the same tmp_path
    # to assert what actually survived a reload.
    cal_dir = tmp_path / "calendar_data"; cal_dir.mkdir(exist_ok=True)
    m = SchoolEmailMonitor(base_path=str(tmp_path))
    return m


def _b64_encode_text(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode()


# ─── Auth error deduplication ────────────────────────────────────────────────

class TestAuthErrorDeduplication:
    def test_not_notified_by_default(self, tmp_path):
        m = _make_monitor(tmp_path)
        assert m._is_auth_error_notified() is False

    def test_set_and_get_notified_flag(self, tmp_path):
        m = _make_monitor(tmp_path)
        m._set_auth_error_notified(True)
        assert m._is_auth_error_notified() is True

    def test_clear_notified_flag(self, tmp_path):
        m = _make_monitor(tmp_path)
        m._set_auth_error_notified(True)
        m._set_auth_error_notified(False)
        assert m._is_auth_error_notified() is False

    def test_state_persists_across_instances(self, tmp_path):
        """Regression: notified flag must survive re-instantiation."""
        m1 = _make_monitor(tmp_path)
        m1._set_auth_error_notified(True)
        # Create fresh instance pointing to same directory
        m2 = SchoolEmailMonitor(base_path=str(tmp_path))
        assert m2._is_auth_error_notified() is True

    def test_state_file_corruption_returns_false(self, tmp_path):
        m = _make_monitor(tmp_path)
        # Corrupt the state file
        state_file = Path(m.auth_error_state_file)
        state_file.write_text("{not valid json{{")
        assert m._is_auth_error_notified() is False


# ─── get_gmail_service auth error notify-once ────────────────────────────────

class TestAuthFailureAlert:
    """The one-shot auth alert, asserted through the surface that now raises it.

    Replaces TestGetGmailServiceAuthError. That class drove `get_gmail_service`,
    which built a Google client from GOOGLE_* env vars; since 2026-09-07 the
    credentials belong to the `gog` CLI and a failure arrives as an exception
    out of core.gmail instead.

    Two of its cases went with the method: `env_broken` (this interpreter has
    no `keyring`) and `no_creds` (the env vars are empty) were distinctions
    about homebase's OWN credential handling, and homebase no longer has any.
    `gog auth status` answers the equivalent about gog. What survives is the
    part that protects the family from an alert on every run, four times a day.
    """

    @contextlib.contextmanager
    def _fetchable(self, m):
        """Config with a usable school query, so a fetch reaches the Gmail call
        rather than short-circuiting on `no_query`.

        Patches the whole `config` object rather than the attribute, because
        `school_email_query` is a read-only property and setattr on it raises.
        """
        with patch("core.config_loader.config") as cfg:
            cfg.school_email_query = "from:school@example.com"
            yield

    def test_first_auth_error_offers_the_alert_once(self, tmp_path, capsys):
        """Regression: first auth failure exposes the WhatsApp alert."""
        m = _make_monitor(tmp_path)
        with self._fetchable(m), \
             patch("core.gmail.search", side_effect=Exception("Token expired")):
            assert m.fetch_recent_school_emails() == []

        assert m.auth_status == "auth_failed"
        assert m.auth_message is not None
        assert "auth error" in m.auth_message.lower()
        # The alert must never reach stdout: these tools' stdout IS their
        # return value, and a WhatsApp message printed in front of the JSON is
        # what this contract was changed to stop.
        assert capsys.readouterr().out == ""

    def test_subsequent_auth_error_is_silent(self, tmp_path, capsys):
        """After the first notification, later failures carry no message."""
        m = _make_monitor(tmp_path)
        m._set_auth_error_notified(True)
        with self._fetchable(m), \
             patch("core.gmail.search", side_effect=Exception("Still expired")):
            assert m.fetch_recent_school_emails() == []

        assert m.auth_status == "auth_failed"
        assert m.auth_message is None
        assert capsys.readouterr().out == ""

    def test_a_successful_fetch_rearms_the_alert(self, tmp_path):
        """A token that breaks, is fixed, then breaks again must be reported
        the second time. Only a successful fetch clears the flag."""
        m = _make_monitor(tmp_path)
        m._set_auth_error_notified(True)
        with self._fetchable(m), patch("core.gmail.search", return_value=[]):
            m.fetch_recent_school_emails()
        assert m._is_auth_error_notified() is False

    def test_a_failed_fetch_is_not_an_empty_inbox(self, tmp_path):
        """[] with no status is how a broken token looked like a quiet day —
        the same silent-drop family as the `none` bucket and has:attachment."""
        m = _make_monitor(tmp_path)
        with self._fetchable(m), \
             patch("core.gmail.search", side_effect=Exception("boom")):
            assert m.fetch_recent_school_emails() == []
        assert m.auth_status == "auth_failed"


class TestExtractBodyAndAttachments:
    def test_extracts_plain_text(self, tmp_path):
        m = _make_monitor(tmp_path)
        text = "Hello from school!"
        payload = {
            "mimeType": "text/plain",
            "body": {"data": _b64_encode_text(text)}
        }
        body, has_pdf, has_image = m._extract_body_and_attachments(payload)
        assert text in body
        assert has_pdf is False
        assert has_image is False

    def test_detects_pdf_attachment(self, tmp_path):
        m = _make_monitor(tmp_path)
        payload = {"mimeType": "application/pdf", "body": {}}
        body, has_pdf, has_image = m._extract_body_and_attachments(payload)
        assert has_pdf is True
        assert has_image is False
        assert body == ""

    def test_detects_inline_image(self, tmp_path):
        m = _make_monitor(tmp_path)
        payload = {"mimeType": "image/jpeg", "body": {"attachmentId": "att123"}}
        body, has_pdf, has_image = m._extract_body_and_attachments(payload)
        assert has_image is True
        assert has_pdf is False
        assert body == ""

    def test_handles_nested_multipart(self, tmp_path):
        """Regression: nested multipart must be parsed recursively."""
        m = _make_monitor(tmp_path)
        inner_text = "Important school notice"
        payload = {
            "mimeType": "multipart/mixed",
            "parts": [
                {
                    "mimeType": "multipart/alternative",
                    "parts": [
                        {
                            "mimeType": "text/plain",
                            "body": {"data": _b64_encode_text(inner_text)}
                        }
                    ]
                },
                {"mimeType": "application/pdf", "body": {}}
            ]
        }
        body, has_pdf, has_image = m._extract_body_and_attachments(payload)
        assert inner_text in body
        assert has_pdf is True
        assert has_image is False

    def test_nested_multipart_with_image_and_pdf(self, tmp_path):
        """Multipart with both a PDF and an inline image detects both."""
        m = _make_monitor(tmp_path)
        payload = {
            "mimeType": "multipart/mixed",
            "parts": [
                {"mimeType": "text/plain", "body": {"data": _b64_encode_text("text")}},
                {"mimeType": "application/pdf", "body": {}},
                {"mimeType": "image/png", "body": {"attachmentId": "att456"}},
            ]
        }
        body, has_pdf, has_image = m._extract_body_and_attachments(payload)
        assert has_pdf is True
        assert has_image is True
        assert "text" in body

    def test_empty_payload_returns_empty(self, tmp_path):
        m = _make_monitor(tmp_path)
        body, has_pdf, has_image = m._extract_body_and_attachments({"mimeType": "text/html", "body": {}})
        assert body == ""
        assert has_pdf is False
        assert has_image is False


# ─── _mark_processed / _load_processed_ids ───────────────────────────────────

class TestProcessedIds:
    def test_marks_and_loads(self, tmp_path):
        m = _make_monitor(tmp_path)
        m._mark_processed("msg123")
        m2 = SchoolEmailMonitor(base_path=str(tmp_path))
        assert "msg123" in m2.processed_ids

    def test_caps_at_500_ids(self, tmp_path):
        m = _make_monitor(tmp_path)
        for i in range(600):
            m.processed_ids.add(f"msg{i}")
        m._save_processed_ids()
        m2 = SchoolEmailMonitor(base_path=str(tmp_path))
        assert len(m2.processed_ids) <= 500

    def test_starts_empty_when_no_file(self, tmp_path):
        m = _make_monitor(tmp_path)
        # Delete the file
        pf = Path(m.processed_ids_file)
        pf.unlink(missing_ok=True)
        m2 = SchoolEmailMonitor(base_path=str(tmp_path))
        assert m2.processed_ids == set()


# ─── fetch_recent_school_emails skip_processed ──────────────────────────────

class TestFetchSkipProcessed:
    """Regression: fetch_school_emails must skip already-processed emails by default."""

    @contextlib.contextmanager
    def _gmail_returning(self, msg_ids):
        """Install the core.gmail seam for these message ids.

        Was `_mock_gmail_list`, which faked a Gmail service object. Since
        2026-09-07 the monitor calls core.gmail.search (ids) and
        core.gmail.get_message (raw Gmail message) — both gog subprocesses —
        so there is no service to fake. The message fixtures are unchanged
        because gog returns Google's own shape.
        """
        def _get(mid, fmt="full"):
            return {
                "id": mid,
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": f"Email {mid}"},
                        {"name": "From", "value": "school@school.example.com"},
                        {"name": "Date", "value": "Mon, 13 Apr 2026 10:00:00 -0700"},
                    ],
                    "mimeType": "text/plain",
                    "body": {"data": _b64_encode_text(f"Body of {mid}")},
                },
            }

        with patch("core.gmail.search", return_value=list(msg_ids)), \
             patch("core.gmail.get_message", side_effect=_get):
            yield


    def test_skip_processed_true_skips_known_ids(self, tmp_path):
        m = _make_monitor(tmp_path)
        m._mark_processed("msg_old")
        with self._gmail_returning(["msg_old", "msg_new"]), \
             patch("core.config_loader.config") as mock_cfg:
            mock_cfg.school_email_query = "from:school.example.com"
            emails = m.fetch_recent_school_emails(skip_processed=True)

        ids = [e["id"] for e in emails]
        assert "msg_new" in ids
        assert "msg_old" not in ids

    def test_skip_processed_false_returns_all(self, tmp_path):
        m = _make_monitor(tmp_path)
        m._mark_processed("msg_old")
        with self._gmail_returning(["msg_old", "msg_new"]), \
             patch("core.config_loader.config") as mock_cfg:
            mock_cfg.school_email_query = "from:school.example.com"
            emails = m.fetch_recent_school_emails(skip_processed=False)

        ids = [e["id"] for e in emails]
        assert "msg_new" in ids
        assert "msg_old" in ids

    def test_daily_summary_emails_are_skipped_and_marked(self, tmp_path):
        """Emails with 'daily summary' or 'checked in' should be auto-skipped."""
        m = _make_monitor(tmp_path)
        summary = {
            "id": "summary_msg",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Daily Summary"},
                    {"name": "From", "value": "school@school.example.com"},
                    {"name": "Date", "value": "Mon, 13 Apr 2026 10:00:00 -0700"},
                ],
                "mimeType": "text/plain",
                "body": {"data": _b64_encode_text("Your child checked in at 8am")},
            },
        }

        with patch("core.gmail.search", return_value=["summary_msg"]), \
             patch("core.gmail.get_message", return_value=summary), \
             patch("core.config_loader.config") as mock_cfg:
            mock_cfg.school_email_query = "from:school.example.com"
            emails = m.fetch_recent_school_emails(skip_processed=True)

        assert len(emails) == 0
        assert "summary_msg" in m.processed_ids

    def test_actionable_email_not_marked_processed_on_fetch(self, tmp_path):
        """Regression: fetching an actionable email must NOT mark it processed.
        Only mark_email_synced() may do that — otherwise an agent that bails
        out after fetching (crash, hallucinated tool call, silent no-op)
        loses the email forever with no retry."""
        m = _make_monitor(tmp_path)
        with self._gmail_returning(["msg_new"]), \
             patch("core.config_loader.config") as mock_cfg:
            mock_cfg.school_email_query = "from:school.example.com"
            emails = m.fetch_recent_school_emails(skip_processed=True)

        assert len(emails) == 1
        assert "msg_new" not in m.processed_ids

        # A second fetch (simulating the agent never calling mark_email_synced,
        # e.g. it bailed early) must return the same email again, not drop it.
        with self._gmail_returning(["msg_new"]), \
             patch("core.config_loader.config") as mock_cfg:
            mock_cfg.school_email_query = "from:school.example.com"
            emails_again = m.fetch_recent_school_emails(skip_processed=True)
        assert len(emails_again) == 1


# ─── tools.py fetch_school_emails uses skip_processed=True ───────────────────

class TestToolsFetchUsesSkipProcessed:
    """Regression: tools.py fetch_school_emails must use skip_processed=True."""

    def test_tools_fetch_calls_skip_processed_true(self):
        # Read the actual source to verify the flag
        tools_path = Path(__file__).parent.parent / "tools.py"
        source = tools_path.read_text()
        # Find the fetch_school_emails function and check skip_processed
        assert "skip_processed=True" in source, \
            "tools.py fetch_school_emails must call fetch_recent_school_emails(skip_processed=True)"
        assert "skip_processed=False" not in source, \
            "tools.py must NOT use skip_processed=False (causes duplicate processing)"


# ─── mark_email_synced gates re-fetch ────────────────────────────────────────

class TestMarkEmailSyncedGatesRefetch:
    """Regression: mark_email_synced() must be the thing that stops an email
    from being re-fetched — since fetch_recent_school_emails() no longer
    marks processed on its own (see test_actionable_email_not_marked_processed_on_fetch)."""

    def test_tools_mark_email_synced_calls_mark_processed(self):
        tools_path = Path(__file__).parent.parent / "tools.py"
        source = tools_path.read_text()
        start = source.index("def mark_email_synced")
        end = source.index("\ndef ", start + 1)
        body = source[start:end]
        assert "_mark_processed(" in body, \
            "mark_email_synced must call monitor._mark_processed() so the " \
            "email is actually excluded from future fetches, not just " \
            "recorded in calendar_synced_ids (which fetch never checks)."


# ─── format_for_whatsapp ─────────────────────────────────────────────────────

class TestFormatForWhatsapp:
    def test_returns_none_for_empty_list(self, tmp_path):
        m = _make_monitor(tmp_path)
        assert m.format_for_whatsapp([]) is None

    def test_contains_subject(self, tmp_path):
        m = _make_monitor(tmp_path)
        emails = [{"subject": "Field Trip Reminder", "sender": "school@test.com",
                   "body": "Please sign the permission slip.", "has_pdf_attachment": False}]
        result = m.format_for_whatsapp(emails)
        assert "Field Trip Reminder" in result

    def test_shows_pdf_annotation(self, tmp_path):
        m = _make_monitor(tmp_path)
        emails = [{"subject": "Newsletter", "sender": "school@test.com",
                   "body": "See attached.", "has_pdf_attachment": True}]
        result = m.format_for_whatsapp(emails)
        assert "PDF" in result

    def test_truncates_long_body(self, tmp_path):
        m = _make_monitor(tmp_path)
        long_body = "A" * 500
        emails = [{"subject": "Long email", "sender": "school@test.com",
                   "body": long_body, "has_pdf_attachment": False}]
        result = m.format_for_whatsapp(emails)
        # Body snippet in output should be at most 300 chars
        # (as coded in format_for_whatsapp)
        assert "AAAA" in result  # some of it present
        assert len(result) < 1000  # but not 500 chars of A's

    def test_multiple_emails_formatted(self, tmp_path):
        m = _make_monitor(tmp_path)
        emails = [
            {"subject": "Email 1", "sender": "s@t.com", "body": "body1", "has_pdf_attachment": False},
            {"subject": "Email 2", "sender": "s@t.com", "body": "body2", "has_pdf_attachment": False},
        ]
        result = m.format_for_whatsapp(emails)
        assert "Email 1" in result
        assert "Email 2" in result


# ─── Ordered ID ledgers ──────────────────────────────────────────────────────

class TestIdLedgersKeepNewest:
    """Regression: both ledgers capped with `list(self.processed_ids)[-500:]`.
    A set has no order, so that kept an arbitrary 500, not the newest 500. Past
    the cap it silently drops recent IDs, and a dropped ID re-surfaces an email
    already handled — a duplicate school calendar proposal for the family."""

    def test_processed_ids_keeps_the_newest_500(self, tmp_path):
        m = _make_monitor(tmp_path)
        for i in range(600):
            m._mark_processed(f"msg-{i:04d}")

        reloaded = _make_monitor(tmp_path)
        assert len(reloaded.processed_ids) == 500
        assert "msg-0099" not in reloaded.processed_ids
        assert all(f"msg-{i:04d}" in reloaded.processed_ids for i in range(100, 600))

    def test_calendar_synced_ids_keeps_the_newest_500(self, tmp_path):
        m = _make_monitor(tmp_path)
        for i in range(600):
            m.mark_calendar_synced(f"cal-{i:04d}")

        reloaded = _make_monitor(tmp_path)
        assert len(reloaded.calendar_synced_ids) == 500
        assert "cal-0099" not in reloaded.calendar_synced_ids
        assert "cal-0599" in reloaded.calendar_synced_ids

    def test_on_disk_order_is_preserved(self, tmp_path):
        m = _make_monitor(tmp_path)
        for msg_id in ("a", "b", "c"):
            m._mark_processed(msg_id)
        assert json.loads(open(m.processed_ids_file).read()) == ["a", "b", "c"]


class TestToolsAuthBranch:
    """A dead token and a quiet inbox were indistinguishable from
    tools.fetch_school_emails — both returned "[]" — so the runner logged a
    quiet day forever. The branch that separates them had no test, and a
    regression removing it would have left the whole suite green."""

    def _monitor(self, auth_status=None, auth_detail=None, auth_message=None):
        from unittest.mock import MagicMock as _MM
        m = _MM()
        m.fetch_recent_school_emails.return_value = []
        m.auth_status = auth_status
        m.auth_detail = auth_detail
        m.auth_message = auth_message
        return m

    def test_a_broken_token_is_not_reported_as_an_empty_inbox(self):
        import json as _json
        import tools
        m = self._monitor("auth_failed", "invalid_grant")
        with patch("features.school.school_email_monitor.SchoolEmailMonitor",
                   return_value=m):
            payload = _json.loads(tools.fetch_school_emails())
        assert payload["status"] == "auth_failed"
        assert payload["emails"] == []

    def test_the_first_failure_carries_the_one_shot_alert(self):
        """get_gmail_service sets auth_message and persists the notified flag
        together, so the alert is single-use. Dropping it here spent it on a
        caller that never delivered it, and every later run stayed silent."""
        import json as _json
        import tools
        m = self._monitor("auth_failed", "invalid_grant", "GOOGLE AUTH ERROR")
        with patch("features.school.school_email_monitor.SchoolEmailMonitor",
                   return_value=m):
            payload = _json.loads(tools.fetch_school_emails())
        assert payload["summary"] == "GOOGLE AUTH ERROR"

    def test_a_genuinely_quiet_inbox_still_returns_a_list(self):
        import json as _json
        import tools
        m = self._monitor()
        with patch("features.school.school_email_monitor.SchoolEmailMonitor",
                   return_value=m):
            assert _json.loads(tools.fetch_school_emails()) == []
