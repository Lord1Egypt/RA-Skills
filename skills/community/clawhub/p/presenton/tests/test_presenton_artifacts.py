from __future__ import annotations

import argparse
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import presenton_artifacts  # noqa: E402


class PresentonResponseMessageTests(unittest.TestCase):
    def test_search_reads_wrapped_designs_and_shows_message(self) -> None:
        response = {
            "designs": [
                {
                    "id": 7,
                    "title": "Editorial Board Review",
                    "description": "Restrained navy and cream",
                }
            ],
            "message": "Search guidance for the user",
        }
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch.object(presenton_artifacts, "request_json", return_value=response),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = presenton_artifacts.command_search(argparse.Namespace(query="review"))

        self.assertEqual(result, 0)
        self.assertIn("Editorial Board Review (id=7)", stdout.getvalue())
        self.assertIn("API message: Search guidance for the user", stderr.getvalue())

    def test_export_shows_message_and_keeps_url_as_only_stdout_value(self) -> None:
        with tempfile.TemporaryDirectory(prefix="presenton-") as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            (temp_dir / presenton_artifacts.TEMP_MARKER_NAME).write_text(
                presenton_artifacts.TEMP_MARKER_CONTENT,
                encoding="utf-8",
            )
            html_path = temp_dir / "presentation.html"
            html_path.write_text("<html></html>", encoding="utf-8")
            response = {
                "id": 23,
                "url": "https://api.example.test/s/export",
                "message": "Export guidance for the user",
            }
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(presenton_artifacts, "validate_html", return_value=[]),
                patch.object(presenton_artifacts, "request_json", return_value=response),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
            ):
                result = presenton_artifacts.command_export(
                    argparse.Namespace(
                        html=html_path,
                        format="pptx",
                        title=None,
                        design_id=None,
                        json=False,
                    )
                )

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), "https://api.example.test/s/export\n")
        self.assertIn("API message: Export guidance for the user", stderr.getvalue())

    def test_export_json_includes_creation_id_and_url(self) -> None:
        with tempfile.TemporaryDirectory(prefix="presenton-") as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            (temp_dir / presenton_artifacts.TEMP_MARKER_NAME).write_text(
                presenton_artifacts.TEMP_MARKER_CONTENT,
                encoding="utf-8",
            )
            html_path = temp_dir / "presentation.html"
            html_path.write_text("<html></html>", encoding="utf-8")
            response = {"id": 31, "url": "https://api.example.test/s/export"}
            stdout = io.StringIO()

            with (
                patch.object(presenton_artifacts, "validate_html", return_value=[]),
                patch.object(
                    presenton_artifacts, "request_json", return_value=response
                ),
                redirect_stdout(stdout),
            ):
                result = presenton_artifacts.command_export(
                    argparse.Namespace(
                        html=html_path,
                        format="pdf",
                        title="Test",
                        design_id=None,
                        json=True,
                    )
                )

        self.assertEqual(result, 0)
        self.assertEqual(
            json.loads(stdout.getvalue()),
            {"id": 31, "url": "https://api.example.test/s/export"},
        )

    def test_create_preview_returns_url(self) -> None:
        response = {
            "url": (
                "https://presenton.example.test/presentation-preview?t=token"
            )
        }
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch.object(
                presenton_artifacts, "request_json", return_value=response
            ) as request,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = presenton_artifacts.command_create_preview(
                argparse.Namespace(id=31)
            )

        self.assertEqual(result, 0)
        request.assert_called_once_with(
            "/api/v3/export/html-to-any/create-preview",
            {"id": 31},
            timeout=presenton_artifacts.SEARCH_TIMEOUT_SECONDS,
        )
        self.assertEqual(stdout.getvalue(), f"{response['url']}\n")
        self.assertIn("preview URL is ready", stderr.getvalue())

    def test_create_preview_rejects_non_positive_creation_id(self) -> None:
        with self.assertRaisesRegex(
            presenton_artifacts.PresentonError, "positive integer"
        ):
            presenton_artifacts.command_create_preview(argparse.Namespace(id=0))

    def test_upload_image_returns_public_https_url(self) -> None:
        response = {
            "id": "18eb9e37-d1e1-42ba-8b1d-fb97c3948d4f",
            "url": "https://cdn.example.test/public/images/reference.png",
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        image_path = Path("/tmp/reference.png")

        with (
            patch.object(
                presenton_artifacts,
                "request_public_image_upload",
                return_value=response,
            ) as request,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = presenton_artifacts.command_upload_image(
                argparse.Namespace(file=image_path)
            )

        self.assertEqual(result, 0)
        request.assert_called_once_with(
            image_path,
            timeout=presenton_artifacts.SEARCH_TIMEOUT_SECONDS,
        )
        self.assertEqual(stdout.getvalue(), f"{response['url']}\n")
        self.assertIn("image URL is ready", stderr.getvalue())

    def test_public_image_upload_rejects_unsupported_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_name:
            image_path = Path(temp_dir_name) / "reference.gif"
            image_path.write_bytes(b"GIF89a")
            with self.assertRaisesRegex(
                presenton_artifacts.PresentonError,
                "PNG, JPEG, or WebP",
            ):
                presenton_artifacts.request_public_image_upload(image_path)

    def test_public_image_upload_sends_multipart_file(self) -> None:
        response = {"url": "https://cdn.example.test/public/image.png"}
        with tempfile.TemporaryDirectory() as temp_dir_name:
            image_path = Path(temp_dir_name) / "reference.png"
            image_path.write_bytes(b"png-image-bytes")
            with patch.object(
                presenton_artifacts,
                "send_json_request",
                return_value=response,
            ) as send:
                result = presenton_artifacts.request_public_image_upload(image_path)

        self.assertEqual(result, response)
        request, endpoint, timeout = send.call_args.args
        self.assertEqual(endpoint, "/api/v3/images/upload/public")
        self.assertEqual(timeout, 60.0)
        self.assertEqual(request.method, "POST")
        self.assertIn("multipart/form-data; boundary=", request.get_header("Content-type"))
        self.assertIn(b'name="file"; filename="reference.png"', request.data)
        self.assertIn(b"Content-Type: image/png", request.data)
        self.assertIn(b"png-image-bytes", request.data)

    def test_search_icons_returns_https_urls(self) -> None:
        response = [
            "https://cdn.example.test/icons/growth.svg",
            "https://cdn.example.test/icons/chart.svg",
        ]
        stdout = io.StringIO()

        with (
            patch.object(
                presenton_artifacts,
                "request_get_json",
                return_value=response,
            ) as request,
            redirect_stdout(stdout),
        ):
            result = presenton_artifacts.command_search_icons(
                argparse.Namespace(query=" growth ", limit=2, icon_type="thin")
            )

        self.assertEqual(result, 0)
        request.assert_called_once_with(
            "/api/v3/icons/search",
            {"query": "growth", "limit": 2, "icon_type": "thin"},
            timeout=presenton_artifacts.SEARCH_TIMEOUT_SECONDS,
        )
        self.assertEqual(stdout.getvalue().splitlines(), response)

    def test_get_json_encodes_icon_search_parameters(self) -> None:
        with patch.object(
            presenton_artifacts,
            "send_json_request",
            return_value=[],
        ) as send:
            result = presenton_artifacts.request_get_json(
                "/api/v3/icons/search",
                {"query": "revenue growth", "limit": 5, "icon_type": "thin"},
            )

        self.assertEqual(result, [])
        request, endpoint, timeout = send.call_args.args
        self.assertEqual(endpoint, "/api/v3/icons/search")
        self.assertEqual(timeout, 60.0)
        self.assertEqual(request.method, "GET")
        self.assertIn("query=revenue+growth", request.full_url)
        self.assertIn("limit=5", request.full_url)
        self.assertIn("icon_type=thin", request.full_url)

    def test_validator_rejects_data_image_urls(self) -> None:
        html = """<!doctype html>
<html><head><script src="https://cdn.tailwindcss.com"></script></head>
<body><main id="presentation-slides-wrapper" class="w-[1280px]">
<section class="h-[720px] w-[1280px]"><img src="data:image/png;base64,AAAA"></section>
</main></body></html>"""

        errors = presenton_artifacts.validate_html(html)

        self.assertTrue(any("data/base64 URLs" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
