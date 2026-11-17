"""
test_bills_watcher.py — Tests for the Bills watcher.

The watcher does NOT summarize or generate tips — the agent does that at
runtime with the fetched pdf_text. These tests cover:
  - Config: enabled flag, billers list, lookback_days, family_group
  - Dedup: msg_id set persistence, 500-item cap
  - Auth-error dedup: first failure sets flag, subsequent silent
  - build_query: OR across billers' full sender addresses and the lookback
    window, and specifically NOT has:attachment
  - body extraction: text/plain preferred, HTML stripped as a fallback, so a
    biller that attaches nothing still yields its amount and due date
  - fetch_emails: skips processed, hard cap of 1, extracts PDF text, flags
    has_pdf, and marks NOTHING — the ledger is two-phase (see mark_processed)
  - CLI entry point contract: parseable JSON status on every path
  - tools.py wrapper (fetch_bill_emails) returns the shape the agent expects,
    including the family-group `target`
  - tools.py mark_bill_processed: the second phase, and the reason a failed
    send no longer loses a bill
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ─── Make skill importable + stub google modules ─────────────────────────────

sys.path.insert(0, str(Path(__file__).parent.parent))


with patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    from features.bills.watcher import (
        BillsWatcher, _collapse_ws, _extract_body, _html_to_text,
    )


# ─── Test config helper ──────────────────────────────────────────────────────


def _write_config(tmp_path: Path, **overrides):
    cfg = {
        "app": {"owner_phone": "+10000000000"},
        "calendar": {"id": "testcal@group.calendar.google.com"},
        "whatsapp": {
            "groups": [{"id": "TEST_FAMILY@g.us", "name": "Family"}],
        },
        "bills": {
            "enabled": True,
            "lookback_days": 3,
            "billers": [
                {"name": "SCE", "sender": "billing@electricco.example.com"},
            ],
        },
    }
    cfg.update(overrides)
    (tmp_path / "config.json").write_text(json.dumps(cfg))
    (tmp_path / "household").mkdir(exist_ok=True)
    return cfg


def _make_watcher(tmp_path: Path, **overrides) -> BillsWatcher:
    _write_config(tmp_path, **overrides)
    return BillsWatcher(base_path=str(tmp_path))


# ─── Config ───────────────────────────────────────────────────────────────────


class TestConfig:
    def test_enabled_reads_from_config(self, tmp_path):
        w = _make_watcher(tmp_path)
        assert w.enabled is True

    def test_disabled_by_default_when_missing(self, tmp_path):
        (tmp_path / "config.json").write_text(json.dumps({}))
        (tmp_path / "household").mkdir()
        w = BillsWatcher(base_path=str(tmp_path))
        assert w.enabled is False

    def test_billers_list(self, tmp_path):
        w = _make_watcher(tmp_path)
        assert w.billers == [{"name": "SCE", "sender": "billing@electricco.example.com"}]

    def test_lookback_days_default(self, tmp_path):
        (tmp_path / "config.json").write_text(json.dumps({"bills": {"enabled": True}}))
        (tmp_path / "household").mkdir()
        w = BillsWatcher(base_path=str(tmp_path))
        assert w.lookback_days == 3

    def test_owner_phone(self, tmp_path):
        w = _make_watcher(tmp_path)
        assert w.owner_phone == "+10000000000"


class TestFamilyGroup:
    def test_reads_first_group(self, tmp_path):
        w = _make_watcher(tmp_path)
        assert w.family_group == {"jid": "TEST_FAMILY@g.us", "name": "Family"}

    def test_legacy_scalar_group_id(self, tmp_path):
        w = _make_watcher(tmp_path, whatsapp={"group_id": "LEGACY@g.us", "group_name": "L"})
        assert w.family_group == {"jid": "LEGACY@g.us", "name": "L"}

    def test_placeholder_jid_returns_none(self, tmp_path):
        w = _make_watcher(tmp_path, whatsapp={
            "groups": [{"id": "YOUR_GROUP_ID@g.us", "name": "Family"}],
        })
        assert w.family_group is None

    def test_no_groups_configured_returns_none(self, tmp_path):
        w = _make_watcher(tmp_path, whatsapp={})
        assert w.family_group is None


# ─── Query building ───────────────────────────────────────────────────────────


class TestBuildQuery:
    def test_single_biller(self, tmp_path):
        w = _make_watcher(tmp_path)
        query = w.build_query()
        assert "from:billing@electricco.example.com" in query
        assert "newer_than:3d" in query

    def test_query_has_no_attachment_filter(self, tmp_path):
        """Regression: `has:attachment` must never come back.

        It was in this query until 2026-08-22 and it silently reduced the
        watcher to whichever billers happen to attach a PDF. Of three
        configured billers only the water district did; the electricity and
        waste companies send a link-only "your bill is ready" notice, so their
        bills were never once matched and every run logged `no_new_emails`.
        Non-bill mail is now filtered downstream by the composing model
        (NOT_A_BILL), which can actually read it.
        """
        w = _make_watcher(tmp_path)
        assert "has:attachment" not in w.build_query()

    def test_multiple_billers_ored(self, tmp_path):
        w = _make_watcher(tmp_path, bills={
            "enabled": True,
            "lookback_days": 5,
            "billers": [
                {"name": "SCE", "sender": "billing@electricco.example.com"},
                {"name": "IRWD", "sender": "billpay@watertest.example.com"},
            ],
        })
        query = w.build_query()
        assert "from:billing@electricco.example.com" in query
        assert "from:billpay@watertest.example.com" in query
        assert " OR " in query
        assert "newer_than:5d" in query

    def test_full_address_avoids_shared_domain_overmatch(self, tmp_path):
        """A biller matched on bare domain could over-match unrelated senders
        on a shared third-party billing platform. Matching the full mailbox
        address avoids that."""
        w = _make_watcher(tmp_path, bills={
            "enabled": True,
            "billers": [{"name": "IRWD", "sender": "billpay@watertest.example.com"}],
        })
        query = w.build_query()
        assert "from:billpay@watertest.example.com" in query

    def test_no_billers_returns_empty_query(self, tmp_path):
        w = _make_watcher(tmp_path, bills={"enabled": True, "billers": []})
        assert w.build_query() == ""


# ─── Dedup ───────────────────────────────────────────────────────────────────


class TestDedup:
    def test_mark_and_load_roundtrip(self, tmp_path):
        w = _make_watcher(tmp_path)
        w.mark_processed("msg-1")
        w.mark_processed("msg-2")
        w2 = BillsWatcher(base_path=str(tmp_path))
        assert "msg-1" in w2.processed_ids
        assert "msg-2" in w2.processed_ids

    def test_500_item_cap_keeps_the_NEWEST_500(self, tmp_path):
        """CONTRACT CHANGE: this used to mutate `processed_ids` (a set) directly
        and assert only the *count* after reload. That passed against the old
        `list(self.processed_ids)[-500:]`, which slices an unordered collection
        — so which 500 survived was a hash-ordering accident, and recent IDs
        could be dropped. A dropped ID means the bill comes back and gets
        posted to the family group a second time. Now marks through the public
        API and asserts recency, which is what the cap is actually for."""
        w = _make_watcher(tmp_path)
        for i in range(600):
            w.mark_processed(f"msg-{i:04d}")

        w2 = BillsWatcher(base_path=str(tmp_path))
        assert len(w2.processed_ids) == 500
        # The 100 oldest are gone, the 500 newest are all present.
        assert "msg-0099" not in w2.processed_ids
        assert "msg-0100" in w2.processed_ids
        assert "msg-0599" in w2.processed_ids
        assert all(f"msg-{i:04d}" in w2.processed_ids for i in range(100, 600))

    def test_marking_the_same_id_twice_does_not_consume_cap(self, tmp_path):
        w = _make_watcher(tmp_path)
        for _ in range(5):
            w.mark_processed("msg-dup")
        assert BillsWatcher(base_path=str(tmp_path)).processed_ids == {"msg-dup"}


# ─── Auth-error dedup ────────────────────────────────────────────────────────


class TestAuthErrorDedup:
    def test_not_notified_by_default(self, tmp_path):
        w = _make_watcher(tmp_path)
        assert w._is_auth_error_notified() is False

    def test_set_and_persist(self, tmp_path):
        w = _make_watcher(tmp_path)
        w._set_auth_error_notified(True)
        w2 = BillsWatcher(base_path=str(tmp_path))
        assert w2._is_auth_error_notified() is True


# ─── Fetch ───────────────────────────────────────────────────────────────────


class TestFetchEmails:
    def test_fetch_returns_pdf_text(self, tmp_path):
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Your SCE bill is ready", sender="billing@electricco.example.com"),
        ])
        with patch(
            "features.bills.watcher.extract_pdf_attachments",
            return_value=["Total due: $142.17\nUsage: 512 kWh"],
        ):
            emails = w.fetch_emails()
        assert len(emails) == 1
        e = emails[0]
        assert e["id"] == "m1"
        assert e["biller_name"] == "SCE"
        assert "Total due: $142.17" in e["pdf_text"]

    def test_fetch_marks_nothing(self, tmp_path):
        """Fetching is not delivering.

        Until 2026-08-17 fetch marked as it took, so any later failure
        (compose, send, crash) destroyed the bill — the next poll skipped
        it and nobody ever saw it. The ledger now only advances via an
        explicit mark_processed() after a confirmed send.
        """
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill 1", sender="billing@electricco.example.com"),
            _fake_bill_msg("m2", "Bill 2", sender="billing@electricco.example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=["text"]):
            emails = w.fetch_emails(take=1)
        assert [e["id"] for e in emails] == ["m1"]
        assert w.processed_ids == set()

    def test_unmarked_bill_is_returned_again(self, tmp_path):
        """The retry property the two-phase ledger exists to provide."""
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill 1", sender="billing@electricco.example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=["text"]):
            first = w.fetch_emails(take=1)
            again = w.fetch_emails(take=1)
        assert [e["id"] for e in first] == [e["id"] for e in again] == ["m1"]

        w.mark_processed("m1")
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=["text"]):
            after = w.fetch_emails(take=1)
        assert after == []

    def test_fetch_skips_processed_ids(self, tmp_path):
        w = _make_watcher(tmp_path)
        w.mark_processed("m1")
        _install_gmail([
            _fake_bill_msg("m1", "Bill 1", sender="billing@electricco.example.com"),
            _fake_bill_msg("m2", "Bill 2", sender="billing@electricco.example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=["text"]):
            emails = w.fetch_emails(take=1)
        assert [e["id"] for e in emails] == ["m2"]

    def test_fetch_uses_biller_query(self, tmp_path):
        w = _make_watcher(tmp_path)
        with patch("core.gmail.search", return_value=[]) as search:
            w.fetch_emails()
        query = search.call_args.args[0]
        assert "from:billing@electricco.example.com" in query

    def test_fetch_empty_query_returns_empty(self, tmp_path):
        w = _make_watcher(tmp_path, bills={"enabled": True, "billers": []})
        service = MagicMock()
        emails = w.fetch_emails()
        assert emails == []
        service.users.return_value.messages.return_value.list.assert_not_called()

    def test_fetch_flags_has_pdf(self, tmp_path):
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill", sender="billing@electricco.example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments",
                   return_value=["Total due: $142.17"]):
            e = w.fetch_emails()[0]
        assert e["has_pdf"] is True
        assert "See attached bill." in e["body"]

    def test_notice_only_bill_survives_with_body(self, tmp_path):
        """Regression: a biller that attaches nothing is still a biller.

        SCE's "Bill is Ready" carries no PDF — the amount and due date are in
        the HTML body. Before 2026-08-22 the Gmail query excluded it outright;
        now it must come back with has_pdf False and a usable body, because
        that body is the only bill there is.
        """
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_notice_msg("m1", "Bill is Ready",
                             sender="billing@electricco.example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=[]):
            e = w.fetch_emails()[0]
        assert e["has_pdf"] is False
        assert e["pdf_text"] == ""
        assert "$204.55" in e["body"]
        assert "September 3, 2026" in e["body"]
        # Tags and inline CSS stripped, not handed to the model raw.
        assert "<" not in e["body"]
        assert "font-family" not in e["body"]


# ─── Body extraction ─────────────────────────────────────────────────────────


class TestBodyExtraction:
    def test_prefers_plain_text_over_html(self):
        payload = {
            "mimeType": "multipart/alternative",
            "parts": [
                {"mimeType": "text/plain", "body": {"data": _b64("Amount due $12.00")}},
                {"mimeType": "text/html",
                 "body": {"data": _b64("<p>Amount due <b>$12.00</b></p>")}},
            ],
        }
        assert _extract_body(payload) == "Amount due $12.00"

    def test_whitespace_padded_plain_loses_to_html(self):
        """Regression: pick the part with content, not the part with the
        preferred MIME type.

        SCE's real "Bill is Ready" carries a text/plain part that is 96 bytes
        of CRLF scaffolding around the customer's first name, while the amount
        and due date live only in the HTML. Preferring text/plain returned the
        scaffolding and the bill looked empty.
        """
        padding = "\r\n" * 200
        payload = {
            "mimeType": "multipart/alternative",
            "parts": [
                {"mimeType": "text/plain",
                 "body": {"data": _b64(padding + "Alexit" + padding)}},
                {"mimeType": "text/html", "body": {"data": _b64(
                    "<p>Amount Due</p><p>$64.73</p><p>Due Date</p><p>09/08/2026</p>"
                )}},
            ],
        }
        body = _extract_body(payload)
        assert "$64.73" in body
        assert "09/08/2026" in body

    def test_falls_back_to_html_when_that_is_all_there_is(self):
        payload = {
            "mimeType": "text/html",
            "body": {"data": _b64("<p>Amount due <b>$12.00</b> by Sep 3</p>")},
        }
        body = _extract_body(payload)
        assert "Amount due $12.00 by Sep 3" in body

    def test_walks_nested_multipart(self):
        payload = {
            "mimeType": "multipart/mixed",
            "parts": [{
                "mimeType": "multipart/alternative",
                "parts": [
                    {"mimeType": "text/plain", "body": {"data": _b64("nested total $9")}},
                ],
            }],
        }
        assert "nested total $9" in _extract_body(payload)

    def test_empty_payload_is_empty_string(self):
        assert _extract_body({"mimeType": "multipart/mixed"}) == ""

    def test_collapse_ws_reclaims_the_cap_from_crlf_padding(self):
        """`body` is truncated before the model sees it, so template padding
        is content that never arrives. 400 CRLFs must not cost 400 chars."""
        raw = "Amount Due" + ("\r\n" * 200) + "$64.73"
        out = _collapse_ws(raw)
        assert "Amount Due" in out and "$64.73" in out
        assert len(out) < 30

    def test_html_strips_script_and_style(self):
        markup = (
            "<style>.x{font-family:Arial;color:#fff}</style>"
            "<script>var a=1;</script>"
            "<p>Total: $85.21</p>"
        )
        text = _html_to_text(markup)
        assert "Total: $85.21" in text
        assert "font-family" not in text
        assert "var a" not in text

    def test_html_decodes_entities_and_strips_zero_width(self):
        # Real SCE markup carries &nbsp; and a BOM mid-line; both showed up in
        # the snippet as visible junk when passed through unprocessed.
        text = _html_to_text("<p>Account&nbsp;XXXX13578﻿ | Due&nbsp;Soon</p>")
        assert "﻿" not in text
        assert " " not in text
        assert "Account XXXX13578 | Due Soon" in text

    def test_fetch_gmail_list_error_returns_empty(self, tmp_path):
        w = _make_watcher(tmp_path)
        service = MagicMock()
        service.users.return_value.messages.return_value.list.return_value.execute.side_effect = \
            Exception("Gmail API down")
        emails = w.fetch_emails()
        assert emails == []

    def test_fetch_gmail_get_error_skips_that_message(self, tmp_path):
        """One bad message shouldn't kill the whole batch.

        A per-message failure is skipped and the rest are returned; only a
        failure of the SEARCH itself gives up on the run. The distinction
        matters because the caller cannot mark what it never received, so a
        skipped message simply comes back next run.
        """
        w = _make_watcher(tmp_path)

        def _get(mid, fmt="full"):
            if mid == "m1":
                raise Exception("boom")
            return _fake_bill_msg("m2", "Bill 2",
                                  sender="billing@electricco.example.com")

        with patch("core.gmail.search", return_value=["m1", "m2"]), \
             patch("core.gmail.get_message", side_effect=_get), \
             patch("features.bills.watcher.extract_pdf_attachments",
                   return_value=["text"]):
            emails = w.fetch_emails(take=None)
        assert [e["id"] for e in emails] == ["m2"]

    def test_pdf_text_truncated_at_20000_chars(self, tmp_path):
        """A real multi-page bill's actual billing-details table (tiered
        usage/rate breakdown) can land on page 2-3, after a page of pure
        legal boilerplate — an 8000-char cap cut off before that page ever
        arrived, leaving only page-1 promotional callouts visible."""
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill", sender="billing@electricco.example.com"),
        ])
        huge_text = "x" * 21000
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=[huge_text]):
            emails = w.fetch_emails()
        assert len(emails[0]["pdf_text"]) == 20000

    def test_unmatched_sender_labeled_unknown(self, tmp_path):
        """Defensive: query already filters by sender, but a biller could
        be removed from config between the query and this call."""
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill", sender="someoneelse@example.com"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=["text"]):
            emails = w.fetch_emails()
        assert emails[0]["biller_name"] == "Unknown"


# ─── CLI entry point ─────────────────────────────────────────────────────────


class TestCliEntryPoint:
    """The __main__ block is a debug helper. It must emit parseable JSON
    on every branch so scripting on top of it stays sane."""

    def test_disabled_prints_status_disabled(self, tmp_path, capsys):
        _write_config(tmp_path, bills={"enabled": False, "billers": []})
        from features.bills import watcher as bills_watcher
        with patch(
            "core.config_loader.SKILL_DIR", str(tmp_path)
        ), patch.object(sys, "argv", ["watcher"]):
            rc = bills_watcher._cli_main()
        out = capsys.readouterr().out
        parsed = json.loads(out.strip().splitlines()[-1])
        assert rc == 0
        assert parsed["status"] == "disabled"

    def test_crash_still_emits_parseable_json(self, tmp_path, capsys):
        """CLAUDE.md principle 4: cron entry always emits parseable status."""
        from features.bills import watcher as bills_watcher
        with patch(
            "core.config_loader.SKILL_DIR", str(tmp_path)
        ), patch.object(
            bills_watcher, "BillsWatcher", side_effect=RuntimeError("kaboom")
        ), patch.object(sys, "argv", ["watcher"]):
            rc = bills_watcher._cli_main()
        out = capsys.readouterr().out
        parsed = json.loads(out.strip().splitlines()[-1])
        assert rc == 1
        assert parsed["status"] == "crashed"
        assert "kaboom" in parsed["error"]


# ─── tools.py wrapper (agent-facing shape) ───────────────────────────────────


class TestToolsWrapper:
    def test_wrapper_shape_disabled(self, tmp_path, monkeypatch):
        _write_config(tmp_path, bills={"enabled": False, "billers": []})
        with patch("tools.SKILL_DIR", str(tmp_path)):
            import tools
            out = json.loads(tools.fetch_bill_emails())
        assert out["status"] == "disabled"
        assert out["emails"] == []
        assert out["target"] is None

    def test_wrapper_shape_emails_found(self, tmp_path, monkeypatch):
        _write_config(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Your SCE bill is ready", sender="billing@electricco.example.com"),
        ])

        from features.bills import watcher as bills_watcher
        monkeypatch.setattr(
            bills_watcher, "extract_pdf_attachments",
            lambda msg_id, payload: ["Total due: $100"],
        )

        with patch("tools.SKILL_DIR", str(tmp_path)):
            import tools
            out = json.loads(tools.fetch_bill_emails())
        assert out["status"] == "emails_found"
        assert out["count"] == 1
        assert out["emails"][0]["id"] == "m1"
        assert "Total due: $100" in out["emails"][0]["pdf_text"]
        assert out["target"] == {"jid": "TEST_FAMILY@g.us", "name": "Family"}

    def test_two_phase_ledger_end_to_end(self, tmp_path, monkeypatch):
        """Fetch, fetch again, mark, fetch again.

        This is the whole point of the 2026-08-17 change: the runner can
        fail between fetching and sending, and the bill survives it.
        """
        _write_config(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Your SCE bill is ready",
                           sender="billing@electricco.example.com"),
        ])

        from features.bills import watcher as bills_watcher
        monkeypatch.setattr(
            bills_watcher, "extract_pdf_attachments",
            lambda msg_id, payload: ["Total due: $100"],
        )

        with patch("tools.SKILL_DIR", str(tmp_path)):
            import tools

            # A run that fetched but never delivered leaves the bill available.
            assert json.loads(tools.fetch_bill_emails())["count"] == 1
            assert json.loads(tools.fetch_bill_emails())["count"] == 1

            assert "✅" in tools.mark_bill_processed("m1")

            after = json.loads(tools.fetch_bill_emails())
        assert after["status"] == "no_new_emails"
        assert after["count"] == 0

    def test_mark_bill_processed_is_reachable_through_execute_tool(self, tmp_path, monkeypatch):
        """The runner reaches this by name through bin/homebase, so a missing
        dispatcher entry would only surface in production."""
        _write_config(tmp_path)
        with patch("tools.SKILL_DIR", str(tmp_path)):
            import tools
            out = tools.execute_tool("mark_bill_processed", {"email_id": "m9"})
        assert "❌" not in out
        assert "m9" in out

    def test_wrapper_hard_caps_count_at_one(self, tmp_path, monkeypatch):
        _write_config(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Bill 1", sender="billing@electricco.example.com"),
            _fake_bill_msg("m2", "Bill 2", sender="billing@electricco.example.com"),
        ])
        from features.bills import watcher as bills_watcher
        monkeypatch.setattr(
            bills_watcher, "extract_pdf_attachments",
            lambda msg_id, payload: ["text"],
        )

        with patch("tools.SKILL_DIR", str(tmp_path)):
            import tools
            out = json.loads(tools.fetch_bill_emails(count=5))
        assert out["count"] == 1


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _b64(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode()


def _fake_bill_msg(
    msg_id: str,
    subject: str,
    sender: str = "billing@electricco.example.com",
    date_hdr: str = "Mon, 6 Jul 2026 12:00:00 -0700",
) -> dict:
    return {
        "id": msg_id,
        "internalDate": "1700000000000",
        "payload": {
            "mimeType": "multipart/mixed",
            "headers": [
                {"name": "Subject", "value": subject},
                {"name": "From", "value": sender},
                {"name": "Date", "value": date_hdr},
            ],
            "parts": [
                {"mimeType": "text/plain", "body": {"data": _b64("See attached bill.")}},
                {
                    "mimeType": "application/pdf",
                    "filename": "bill.pdf",
                    "body": {"attachmentId": "att-1"},
                },
            ],
        },
    }


def _fake_notice_msg(
    msg_id: str,
    subject: str,
    sender: str = "billing@electricco.example.com",
    date_hdr: str = "Tue, 18 Aug 2026 15:27:00 -0700",
) -> dict:
    """A link-only "your bill is ready" notice: HTML body, no attachment, no
    text/plain part. Shaped after a real SCE bill notice, which is the mail
    the old has:attachment filter threw away."""
    return {
        "id": msg_id,
        "internalDate": "1700000001000",
        "payload": {
            "mimeType": "text/html",
            "headers": [
                {"name": "Subject", "value": subject},
                {"name": "From", "value": sender},
                {"name": "Date", "value": date_hdr},
            ],
            "body": {"data": _b64(
                "<html><head><style>.b{font-family:Arial;font-size:12px}</style></head>"
                "<body><p>Your Bill is Due Soon</p>"
                "<p>Amount due: <b>$204.55</b></p>"
                "<p>Due date: September 3, 2026</p>"
                "<p>Your current bill is now available for viewing.</p>"
                "</body></html>"
            )},
        },
    }


def _install_gmail(messages: list) -> None:
    """Install the core.gmail seam for one test.

    Replaced _mock_service_returning on 2026-09-07. There is no Gmail service
    to fake any more — the watcher calls core.gmail.search (ids) and
    core.gmail.get_message (raw Gmail message), both of which shell out to the
    `gog` CLI. The fixtures are unchanged because gog returns Google's own
    message shape.

    Patches are started rather than scoped to a `with`, so the call sites keep
    their original one-line shape; `_stop_started_patches` below unwinds them.
    """
    by_id = {m["id"]: m for m in messages}
    patch("core.gmail.search",
          return_value=[m["id"] for m in messages]).start()
    patch("core.gmail.get_message",
          side_effect=lambda mid, fmt="full": by_id[mid]).start()


@pytest.fixture(autouse=True)
def _stop_started_patches():
    """Unwind anything _install_gmail started, even when a test fails."""
    yield
    patch.stopall()


class TestUnreadablePdf:
    """`has_pdf` means ATTACHED, not READABLE. Conflating the two made a
    scanned or malformed statement look like a notice-only bill, so the
    composer summarized a full statement as "your bill is ready"."""

    def test_an_attached_but_unreadable_pdf_is_flagged_not_downgraded(self, tmp_path):
        w = _make_watcher(tmp_path)
        _install_gmail([
            _fake_bill_msg("m1", "Your bill is ready"),
        ])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=[]):
            e = w.fetch_emails()[0]
        assert e["has_pdf"] is True, "a scanned statement read as notice-only"
        assert e["pdf_unreadable"] is True

    def test_a_readable_pdf_is_not_flagged_unreadable(self, tmp_path):
        w = _make_watcher(tmp_path)
        _install_gmail([_fake_bill_msg("m2", "Bill")])
        with patch("features.bills.watcher.extract_pdf_attachments",
                   return_value=["Total due: $10"]):
            e = w.fetch_emails()[0]
        assert e["has_pdf"] is True
        assert e["pdf_unreadable"] is False

    def test_a_notice_with_no_attachment_is_neither(self, tmp_path):
        w = _make_watcher(tmp_path)
        _install_gmail([_fake_notice_msg("m3", "Bill ready")])
        with patch("features.bills.watcher.extract_pdf_attachments", return_value=[]):
            e = w.fetch_emails()[0]
        assert e["has_pdf"] is False
        assert e["pdf_unreadable"] is False

    def test_has_pdf_part_finds_a_nested_attachment(self):
        from features.bills.watcher import _has_pdf_part
        nested = {"mimeType": "multipart/mixed", "parts": [
            {"mimeType": "multipart/related", "parts": [
                {"mimeType": "application/pdf"}]}]}
        assert _has_pdf_part(nested) is True
        assert _has_pdf_part({"mimeType": "text/html", "body": {}}) is False
