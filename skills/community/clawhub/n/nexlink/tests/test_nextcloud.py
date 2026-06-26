#!/usr/bin/env python3
"""Unit tests for the Nextcloud module."""

import io
import os
import sys
import unittest
import zipfile
from io import StringIO
from unittest.mock import MagicMock, patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from modules.nextcloud.nextcloud import NextcloudClient, run_cli


class FakeResponse:
    """Simple fake HTTP response for tests."""

    def __init__(self, status_code=200, content=b"", text="", chunks=None):
        self.status_code = status_code
        self.content = content
        self.text = text
        self._chunks = chunks or []

    def iter_content(self, chunk_size=8192):
        """Yield configured chunks."""
        del chunk_size
        for chunk in self._chunks:
            yield chunk


class NextcloudTestCase(unittest.TestCase):
    """Base helpers for Nextcloud tests."""

    ENV = {
        "NEXTCLOUD_URL": "https://cloud.example.com",
        "NEXTCLOUD_USERNAME": "alex",
        "NEXTCLOUD_APP_PASSWORD": "app-pass",
    }

    def create_client(self):
        """Create a client with user ID resolution stubbed."""
        with patch.dict(os.environ, self.ENV, clear=False):
            with patch.object(
                NextcloudClient,
                "_resolve_user_id",
                lambda self: setattr(self, "user_id", "alex-id"),
            ):
                return NextcloudClient()


class TestNextcloudClient(NextcloudTestCase):
    """Tests for Nextcloud client behavior."""

    def _build_docx_bytes(self, text):
        """Create a minimal DOCX payload for parser tests."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr(
                "word/document.xml",
                (
                    "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
                    "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"
                    f"<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>"
                ),
            )
        return buffer.getvalue()

    def test_get_full_url_uses_user_id_and_normalized_path(self):
        client = self.create_client()

        result = client._get_full_url("Documents//Offers/")

        self.assertEqual(
            result,
            "https://cloud.example.com/remote.php/dav/files/alex-id/Documents/Offers",
        )

    def test_list_recursive_collects_nested_entries(self):
        client = self.create_client()

        with patch.object(client, "_list_directory") as mock_list_directory:
            mock_list_directory.side_effect = [
                [
                    {"name": "Docs", "type": "folder", "path": "/Docs", "size": 0, "modified": "-", "mime_type": ""},
                    {"name": "root.txt", "type": "file", "path": "/root.txt", "size": 10, "modified": "-", "mime_type": "text/plain"},
                ],
                [
                    {"name": "Nested", "type": "folder", "path": "/Docs/Nested", "size": 0, "modified": "-", "mime_type": ""},
                    {"name": "offer.pdf", "type": "file", "path": "/Docs/offer.pdf", "size": 20, "modified": "-", "mime_type": "application/pdf"},
                ],
                [
                    {"name": "notes.md", "type": "file", "path": "/Docs/Nested/notes.md", "size": 30, "modified": "-", "mime_type": "text/markdown"},
                ],
            ]

            results = client.list("/", recursive=True)

        self.assertEqual([item["path"] for item in results], [
            "/Docs",
            "/root.txt",
            "/Docs/Nested",
            "/Docs/offer.pdf",
            "/Docs/Nested/notes.md",
        ])

    def test_search_filters_case_insensitive_results(self):
        client = self.create_client()

        with patch.object(client, "list", return_value=[
            {"name": "Contract.pdf", "type": "file", "path": "/Clients/Contract.pdf", "size": 10, "modified": "-", "mime_type": "application/pdf"},
            {"name": "notes.txt", "type": "file", "path": "/Clients/notes.txt", "size": 5, "modified": "-", "mime_type": "text/plain"},
        ]):
            results = client.search("contract")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["path"], "/Clients/Contract.pdf")

    def test_create_share_link_returns_share_metadata(self):
        client = self.create_client()
        xml_response = b"""
        <ocs>
          <meta><status>ok</status><statuscode>100</statuscode><message>OK</message></meta>
          <data>
            <id>44</id>
            <url>https://cloud.example.com/s/abc123</url>
            <token>abc123</token>
            <path>/Clients/offer.pdf</path>
            <permissions>1</permissions>
          </data>
        </ocs>
        """

        with patch("modules.nextcloud.nextcloud.requests.request", return_value=FakeResponse(status_code=200, content=xml_response)):
            result = client.create_share_link("/Clients/offer.pdf", password="secret", expire_date="2026-04-30")

        self.assertEqual(result["id"], "44")
        self.assertEqual(result["url"], "https://cloud.example.com/s/abc123")
        self.assertEqual(result["path"], "/Clients/offer.pdf")
        self.assertTrue(result["password_protected"])

    def test_list_share_links_returns_only_public_links(self):
        client = self.create_client()
        xml_response = b"""
        <ocs>
          <meta><status>ok</status><statuscode>100</statuscode><message>OK</message></meta>
          <data>
            <element>
              <id>10</id>
              <share_type>3</share_type>
              <path>/Public/report.pdf</path>
              <url>https://cloud.example.com/s/report</url>
              <permissions>1</permissions>
            </element>
            <element>
              <id>11</id>
              <share_type>0</share_type>
              <path>/Private/internal.txt</path>
              <permissions>1</permissions>
            </element>
          </data>
        </ocs>
        """

        with patch("modules.nextcloud.nextcloud.requests.request", return_value=FakeResponse(status_code=200, content=xml_response)):
            results = client.list_share_links()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "10")
        self.assertEqual(results[0]["path"], "/Public/report.pdf")

    def test_revoke_share_link_returns_true_on_success(self):
        client = self.create_client()
        xml_response = b"""
        <ocs>
          <meta><status>ok</status><statuscode>100</statuscode><message>OK</message></meta>
          <data/>
        </ocs>
        """

        with patch("modules.nextcloud.nextcloud.requests.request", return_value=FakeResponse(status_code=200, content=xml_response)):
            result = client.revoke_share_link("55")

        self.assertTrue(result)

    def test_extract_text_returns_plain_text_payload(self):
        client = self.create_client()
        response = FakeResponse(content=b"Contract renewal is due on 15 May 2026. Contact Ana for approval.")

        with patch.object(client, "_request", return_value=response):
            result = client.extract_text("/Clients/contract.txt")

        self.assertEqual(result["path"], "/Clients/contract.txt")
        self.assertIn("15 May 2026", result["text"])
        self.assertEqual(result["extension"], ".txt")

    def test_extract_text_reads_docx_payload(self):
        client = self.create_client()
        response = FakeResponse(content=self._build_docx_bytes("Important clause for renewal"))

        with patch.object(client, "_request", return_value=response):
            result = client.extract_text("/Clients/contract.docx")

        self.assertIn("Important clause for renewal", result["text"])
        self.assertEqual(result["extension"], ".docx")

    def test_summarize_returns_grounded_summary(self):
        client = self.create_client()
        extracted = {
            "path": "/Clients/contract.txt",
            "extension": ".txt",
            "text": (
                "Contract renewal is due on 15 May 2026. "
                "The client expects confirmation this week. "
                "Finance should approve the updated price list. "
                "Ana owns the follow-up."
            ),
            "char_count": 137,
            "truncated": False,
        }

        with patch.object(client, "extract_text", return_value=extracted):
            result = client.summarize("/Clients/contract.txt")

        self.assertEqual(result["path"], "/Clients/contract.txt")
        self.assertIn("15 May 2026", result["summary"])
        self.assertTrue(result["highlights"])

    def test_ask_file_returns_best_matching_excerpt(self):
        client = self.create_client()
        extracted = {
            "path": "/Clients/contract.txt",
            "extension": ".txt",
            "text": (
                "Contract renewal is due on 15 May 2026. "
                "The client expects confirmation this week. "
                "Finance should approve the updated price list. "
                "Ana owns the follow-up."
            ),
            "char_count": 137,
            "truncated": False,
        }

        with patch.object(client, "extract_text", return_value=extracted):
            result = client.ask_file("/Clients/contract.txt", "When is the renewal due?")

        self.assertIn("15 May 2026", result["answer"])
        self.assertTrue(result["supporting_excerpts"])


    def test_extract_text_prefers_pdfplumber_over_pypdf(self):
        """Verify _extract_pdf_text tries pdfplumber before pypdf."""
        import inspect
        client = self.create_client()
        source = inspect.getsource(client._extract_pdf_text)
        pdfplumber_pos = source.find("pdfplumber")
        pypdf_pos = source.find("pypdf")
        self.assertLess(pdfplumber_pos, pypdf_pos, "pdfplumber should be tried before pypdf")
        self.assertIn("pdfplumber", source)
        self.assertIn("pypdf", source)

    def test_extract_text_pdf_returns_none_without_parsers(self):
        """When no PDF parser extracts text, extract_text returns None."""
        client = self.create_client()
        with patch.object(client, "_extract_pdf_text", return_value=""):
            with patch.object(client, "_request", return_value=FakeResponse(content=b"%PDF-1.4 fake")):
                result = client.extract_text("/Docs/report.pdf")
        self.assertIsNone(result)

    def test_extract_actions_returns_grounded_action_items(self):
        client = self.create_client()
        response = FakeResponse(
            content=(
                b"Please send the updated quote by 15 May 2026. "
                b"Ana should confirm the pricing with finance this week. "
                b"Create a follow-up for the renewal call."
            )
        )

        with patch.object(client, "_request", return_value=response):
            result = client.extract_actions("/Clients/contract.txt")

        self.assertEqual(result["path"], "/Clients/contract.txt")
        self.assertEqual(result["document_type"], "contract")
        self.assertTrue(result["summary"])
        self.assertGreaterEqual(result["count"], 2)
        self.assertTrue(any(item["due_hint"] == "2026-05-15" for item in result["actions"]))
        self.assertTrue(any(item["owner_hint"] == "Ana" for item in result["actions"]))
        self.assertTrue(all(item["confidence"] in {"low", "medium", "high"} for item in result["actions"]))
        self.assertTrue(all("due_date" in item and "owner" in item and "priority" in item for item in result["actions"]))

    def test_create_tasks_from_file_defaults_to_preview_mode(self):
        client = self.create_client()
        extracted = {
            "path": "/Clients/contract.txt",
            "document_type": "contract",
            "summary": "Renewal terms and follow-up obligations.",
            "highlights": ["renewal", "follow-up"],
            "count": 2,
            "actions": [
                {
                    "index": 1,
                    "title": "Send the updated quote",
                    "reason": "Explicit action phrase found in source sentence.",
                    "details": "Please send the updated quote by 15 May 2026.",
                    "due_hint": "2026-05-15",
                    "owner_hint": "Ana",
                    "source_excerpt": "Please send the updated quote by 15 May 2026.",
                    "evidence": ["Please send the updated quote by 15 May 2026."],
                    "due_date": {"value": "2026-05-15", "source": "inferred"},
                    "owner": {"value": "Ana", "source": "inferred"},
                    "priority": {"value": "medium", "source": "inferred"},
                    "confidence": "high",
                },
                {
                    "index": 2,
                    "title": "Create a follow-up for the renewal call",
                    "reason": "Explicit action phrase found in source sentence.",
                    "details": "Create a follow-up for the renewal call.",
                    "due_hint": None,
                    "owner_hint": None,
                    "source_excerpt": "Create a follow-up for the renewal call.",
                    "evidence": ["Create a follow-up for the renewal call."],
                    "due_date": {"value": None, "source": "missing"},
                    "owner": {"value": None, "source": "missing"},
                    "priority": {"value": "normal", "source": "inferred"},
                    "confidence": "medium",
                },
            ],
        }

        with patch.object(client, "extract_actions", return_value=extracted):
            result = client.create_tasks_from_file("/Clients/contract.txt")

        self.assertEqual(result["mode"], "preview")
        self.assertTrue(result["dry_run"])
        self.assertFalse(result["execute"])
        self.assertEqual(result["proposal_count"], 2)
        self.assertEqual(result["selected_indexes"], [1, 2])
        self.assertEqual(result["tasks"][0]["subject"], "Send the updated quote")

    def test_create_tasks_from_file_execute_respects_selected_indexes(self):
        client = self.create_client()
        created = []

        class FakeTask:
            def __init__(self, account=None, folder=None, subject=None, body=None):
                self.account = account
                self.folder = folder
                self.subject = subject
                self.body = body
                self.importance = None
                self.due_date = None
                self.id = f"task-{len(created) + 1}"

            def save(self):
                created.append(self)

        fake_account = type("Account", (), {"tasks": object(), "primary_smtp_address": "owner@example.com"})()
        extracted = {
            "path": "/Clients/contract.txt",
            "document_type": "contract",
            "summary": "Renewal terms and follow-up obligations.",
            "highlights": ["renewal", "follow-up"],
            "count": 2,
            "actions": [
                {
                    "index": 1,
                    "title": "Send the updated quote",
                    "reason": "Explicit action phrase found in source sentence.",
                    "details": "Please send the updated quote by 15 May 2026.",
                    "due_hint": "2026-05-15",
                    "owner_hint": "Ana",
                    "source_excerpt": "Please send the updated quote by 15 May 2026.",
                    "evidence": ["Please send the updated quote by 15 May 2026."],
                    "due_date": {"value": "2026-05-15", "source": "inferred"},
                    "owner": {"value": "Ana", "source": "inferred"},
                    "priority": {"value": "medium", "source": "inferred"},
                    "confidence": "high",
                },
                {
                    "index": 2,
                    "title": "Create a follow-up for the renewal call",
                    "reason": "Explicit action phrase found in source sentence.",
                    "details": "Create a follow-up for the renewal call.",
                    "due_hint": None,
                    "owner_hint": None,
                    "source_excerpt": "Create a follow-up for the renewal call.",
                    "evidence": ["Create a follow-up for the renewal call."],
                    "due_date": {"value": None, "source": "missing"},
                    "owner": {"value": None, "source": "missing"},
                    "priority": {"value": "normal", "source": "inferred"},
                    "confidence": "medium",
                },
            ],
        }

        with patch.object(client, "extract_actions", return_value=extracted):
            with patch("modules.nextcloud.nextcloud.get_exchange_account", return_value=fake_account):
                with patch("modules.nextcloud.nextcloud.build_exchange_task", side_effect=lambda account, subject, body: FakeTask(account=account, folder=account.tasks, subject=subject, body=body)):
                    with patch("modules.nextcloud.nextcloud.build_ews_date", return_value="ews-date"):
                        result = client.create_tasks_from_file(
                            "/Clients/contract.txt",
                            execute=True,
                            selected_indexes=[1],
                        )

        self.assertEqual(result["mode"], "execute")
        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["selected_indexes"], [1])
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].subject, "Send the updated quote")
        self.assertEqual(created[0].due_date, "ews-date")


class TestNextcloudCli(NextcloudTestCase):
    """Tests for Nextcloud CLI behavior."""

    def test_run_cli_requires_search_query(self):
        with patch.dict(os.environ, self.ENV, clear=False):
            with patch("sys.stdout", new_callable=StringIO) as stdout:
                exit_code = run_cli(["search"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Usage: nextcloud.py search <query> [remote_path]", stdout.getvalue())

    def test_run_cli_list_recursive_prints_results(self):
        fake_result = [
            {"name": "Docs", "type": "folder", "path": "/Docs", "size": 0, "modified": "Wed, 10 Apr 2026 12:00:00 GMT", "mime_type": ""}
        ]

        with patch.dict(os.environ, self.ENV, clear=False):
            with patch.object(
                NextcloudClient,
                "_resolve_user_id",
                lambda self: setattr(self, "user_id", "alex-id"),
            ):
                with patch.object(NextcloudClient, "list", return_value=fake_result):
                    with patch("sys.stdout", new_callable=StringIO) as stdout:
                        exit_code = run_cli(["list", "/", "--recursive"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Docs", stdout.getvalue())

    def test_run_cli_requires_question_for_ask_file(self):
        with patch.dict(os.environ, self.ENV, clear=False):
            with patch("sys.stdout", new_callable=StringIO) as stdout:
                exit_code = run_cli(["ask-file", "/Clients/contract.txt"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Usage: nextcloud.py ask-file <remote_path> <question>", stdout.getvalue())

    def test_run_cli_requires_path_for_create_tasks_from_file(self):
        with patch.dict(os.environ, self.ENV, clear=False):
            with patch("sys.stdout", new_callable=StringIO) as stdout:
                exit_code = run_cli(["create-tasks-from-file"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Usage: nextcloud.py create-tasks-from-file <remote_path>", stdout.getvalue())

    def test_run_cli_parses_execute_and_select_for_create_tasks_from_file(self):
        fake_result = {"mode": "execute", "created_count": 1, "tasks": [{"subject": "Send the updated quote"}]}

        with patch.dict(os.environ, self.ENV, clear=False):
            with patch.object(
                NextcloudClient,
                "_resolve_user_id",
                lambda self: setattr(self, "user_id", "alex-id"),
            ):
                with patch.object(NextcloudClient, "create_tasks_from_file", return_value=fake_result) as mocked:
                    with patch("sys.stdout", new_callable=StringIO) as stdout:
                        exit_code = run_cli([
                            "create-tasks-from-file",
                            "/Clients/contract.txt",
                            "--select",
                            "1,2",
                            "--execute",
                        ])

        self.assertEqual(exit_code, 0)
        mocked.assert_called_once_with(
            "/Clients/contract.txt",
            mailbox=None,
            priority="normal",
            execute=True,
            selected_indexes=[1, 2],
        )
        self.assertIn("created_count", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
