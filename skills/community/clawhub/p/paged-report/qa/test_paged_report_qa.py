"""Focused self-checks for the paged-report QA evidence gate."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

try:
    from pypdf import PdfWriter
except ImportError:  # pragma: no cover - exercised by dependency diagnostics
    PdfWriter = None

if __package__:
    from .paged_report_qa import main, run_gate
else:  # direct discovery with qa on sys.path or direct script execution
    from paged_report_qa import main, run_gate


GOOD_HTML = """<!doctype html>
<html lang="en-AU">
<head><meta charset="utf-8"><style>.report-page { min-height: 10px; }</style></head>
<body><div class="report-page cover">Cover</div><div class="report-page">Content</div></body>
</html>
"""

BAD_HTML = """<html><head><link rel="stylesheet" href="https://example.test/report.css"></head>
<body><div class="report-page"></div></body></html>
"""


class HtmlGateTests(unittest.TestCase):
    def test_html_contract_and_logical_page_count_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "report.html"
            html_path.write_text(GOOD_HTML, encoding="utf-8")

            evidence = run_gate(html_path)

        self.assertEqual(evidence["html"]["status"], "PASS")
        self.assertEqual(evidence["logical_pages"]["status"], "PASS")
        self.assertEqual(evidence["logical_pages"]["count"], 2)
        self.assertEqual(evidence["overflow"]["status"], "WARN")
        self.assertEqual(evidence["page_policy"]["verdict"], "INDEPENDENT")
        self.assertEqual(evidence["pdf"]["status"], "SKIP")
        self.assertEqual(evidence["pdf"]["checks"]["provided"]["status"], "SKIP")
        self.assertEqual(evidence["status"], "WARN")

    def test_deterministic_html_failure_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "bad.html"
            html_path.write_text(BAD_HTML, encoding="utf-8")

            evidence = run_gate(html_path)

        self.assertEqual(evidence["status"], "FAIL")
        self.assertEqual(evidence["html"]["status"], "FAIL")
        self.assertEqual(evidence["html"]["checks"]["doctype"]["status"], "FAIL")
        self.assertEqual(evidence["html"]["checks"]["self_containment"]["status"], "FAIL")

    def test_expected_logical_page_mismatch_is_nonzero_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "report.html"
            html_path.write_text(GOOD_HTML, encoding="utf-8")

            evidence = run_gate(html_path, expected_logical_pages=3)

        self.assertEqual(evidence["logical_pages"]["status"], "FAIL")
        self.assertEqual(evidence["status"], "FAIL")

    def test_require_pdf_rejects_missing_pdf_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "report.html"
            html_path.write_text(GOOD_HTML, encoding="utf-8")

            evidence = run_gate(html_path, require_pdf=True)

        self.assertEqual(evidence["pdf"]["status"], "FAIL")
        self.assertEqual(evidence["pdf"]["checks"]["provided"]["status"], "FAIL")
        self.assertEqual(
            evidence["pdf"]["checks"]["provided"]["message"],
            "PDF is required but no PDF was supplied",
        )
        self.assertEqual(evidence["status"], "FAIL")

    @unittest.skipUnless(PdfWriter is not None, "pypdf unavailable; PDF checks report a dependency warning")
    def test_pdf_count_a4_and_blank_page_verdicts_are_separate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "report.html"
            html_path.write_text(GOOD_HTML, encoding="utf-8")
            pdf_path = Path(tmp) / "blank-a4.pdf"

            writer = PdfWriter()
            writer.add_blank_page(width=595.2756, height=841.8898)
            with pdf_path.open("wb") as handle:
                writer.write(handle)

            evidence = run_gate(html_path, pdf_path=pdf_path)

        self.assertEqual(evidence["pdf"]["physical_page_count"], 1)
        self.assertEqual(evidence["pdf"]["checks"]["a4_mediabox"]["status"], "PASS")
        self.assertEqual(evidence["pdf"]["checks"]["blank_pages"]["status"], "FAIL")
        self.assertEqual(evidence["pdf"]["checks"]["blank_pages"]["pages"], [1])
        self.assertEqual(evidence["status"], "FAIL")

    def test_cli_emits_json_and_nonzero_for_missing_html(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["/tmp/paged-report-qa-file-that-does-not-exist.html"])

        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["status"], "FAIL")
        self.assertIn("error", payload)


if __name__ == "__main__":
    unittest.main()
