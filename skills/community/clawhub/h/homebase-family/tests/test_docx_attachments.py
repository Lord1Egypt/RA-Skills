"""
test_docx_attachments.py — Unit tests for core/docx_attachments.py

Covers the 2026-09-23 silent drop: a school newsletter arrived as a .docx,
matched neither the PDF nor the image collector, and was dropped with no log
line — the runner announced the 454-character cover note and reported success
while Parent-Teacher Conferences sat unread inside the attachment.

  - _xml_to_text(): paragraphs, explicit breaks, table rows/cells, entities
  - extract_docx_text_from_bytes(): real zip round-trip, corrupt bytes
  - _collect_docx_parts(): MIME match, filename fallback, nesting, .doc skip
  - extract_docx_attachments(): download path, empty payload, error isolation
  - tools.py wiring: docx text must reach the `pdf_text` field
"""
import io
import re
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.docx_attachments import (  # noqa: E402
    DOC_MIME,
    DOCX_MIME,
    _collect_docx_parts,
    _xml_to_text,
    extract_docx_attachments,
    extract_docx_text_from_bytes,
)


def _docx(document_xml: str) -> bytes:
    """Build a minimal but genuine .docx (a zip holding word/document.xml)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", document_xml)
    return buf.getvalue()


def _para(text: str) -> str:
    return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"


# ─── _xml_to_text ────────────────────────────────────────────────────────────

def test_paragraphs_become_separate_lines():
    """Without this the whole newsletter collapses onto one line and the
    dates stop being separable."""
    out = _xml_to_text(_para("October 23 (Friday)") + _para("Parent-Teacher Conferences"))
    assert out.splitlines() == ["October 23 (Friday)", "Parent-Teacher Conferences"]


def test_table_rows_and_cells_keep_their_shape():
    xml = (
        "<w:tbl><w:tr>"
        "<w:tc>" + _para("Oct 23") + "</w:tc>"
        "<w:tc>" + _para("Conferences") + "</w:tc>"
        "</w:tr><w:tr>"
        "<w:tc>" + _para("Oct 30") + "</w:tc>"
        "<w:tc>" + _para("Harvest party") + "</w:tc>"
        "</w:tr></w:tbl>"
    )
    out = _xml_to_text(xml)
    assert "Oct 23" in out and "Conferences" in out
    assert "Oct 30" in out and "Harvest party" in out
    # The two rows must not merge into one.
    assert re.search(r"Conferences\s*\n", out)


def test_explicit_breaks_and_tabs():
    xml = "<w:p><w:r><w:t>a</w:t><w:br/><w:t>b</w:t><w:tab/><w:t>c</w:t></w:r></w:p>"
    out = _xml_to_text(xml)
    assert out.splitlines()[0] == "a"
    assert "b" in out and "c" in out


def test_entities_are_unescaped():
    out = _xml_to_text(_para("Trunk &amp; Treat &#8212; 5pm"))
    assert "Trunk & Treat" in out
    assert "&amp;" not in out


def test_runs_inside_one_paragraph_stay_on_one_line():
    """Word splits a sentence across runs on any formatting change; a split
    that became a newline would break date-plus-weekday parsing."""
    xml = "<w:p><w:r><w:t>October 23 </w:t></w:r><w:r><w:t>(Friday)</w:t></w:r></w:p>"
    assert _xml_to_text(xml).splitlines() == ["October 23 (Friday)"]


def test_blank_paragraphs_do_not_pile_up():
    out = _xml_to_text(_para("a") + "<w:p/>" * 5 + _para("b"))
    assert "\n\n\n" not in out


# ─── extract_docx_text_from_bytes ────────────────────────────────────────────

def test_real_zip_round_trip():
    out = extract_docx_text_from_bytes(_docx(_para("Harvest party Oct 30")))
    assert "Harvest party Oct 30" in out


def test_corrupt_bytes_return_empty_not_raise():
    assert extract_docx_text_from_bytes(b"not a zip at all") == ""


def test_zip_without_document_xml_returns_empty():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/other.xml", "<x/>")
    assert extract_docx_text_from_bytes(buf.getvalue()) == ""


def test_document_xml_that_inflates_past_the_cap_is_skipped():
    """A few KB of compressed zeros must not inflate into memory."""
    import core.docx_attachments as mod
    bomb = _docx(_para("x") + " " * 4096)
    with patch.object(mod, "MAX_DOCUMENT_XML_BYTES", 1024):
        assert extract_docx_text_from_bytes(bomb) == ""


# ─── _collect_docx_parts ─────────────────────────────────────────────────────

def test_collects_by_mime_type():
    out = []
    _collect_docx_parts({"mimeType": DOCX_MIME, "filename": "n.docx"}, out)
    assert len(out) == 1


def test_collects_by_filename_when_mime_is_generic():
    """Phones and scanners label a .docx application/octet-stream; a
    MIME-only match would drop those exactly as silently as before."""
    out = []
    _collect_docx_parts(
        {"mimeType": "application/octet-stream", "filename": "October Newsletter.DOCX"}, out
    )
    assert len(out) == 1


def test_finds_nested_attachment():
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [
            {"mimeType": "multipart/alternative", "parts": [{"mimeType": "text/plain"}]},
            {"mimeType": DOCX_MIME, "filename": "n.docx"},
        ],
    }
    out = []
    _collect_docx_parts(payload, out)
    assert len(out) == 1


def test_legacy_doc_is_not_collected():
    """A .doc is not a zip. It must not be handed to the zip reader, and the
    point of the fix is that it is logged rather than dropped in silence."""
    out = []
    _collect_docx_parts({"mimeType": DOC_MIME, "filename": "old.doc"}, out)
    assert out == []


def test_pdf_and_images_are_ignored_here():
    out = []
    _collect_docx_parts({"mimeType": "application/pdf", "filename": "a.pdf"}, out)
    _collect_docx_parts({"mimeType": "image/jpeg", "filename": "a.jpg"}, out)
    assert out == []


# ─── extract_docx_attachments ────────────────────────────────────────────────

def test_downloads_and_extracts():
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [{
            "mimeType": DOCX_MIME,
            "filename": "October Newsletter 26.docx",
            "body": {"attachmentId": "att-1"},
        }],
    }
    blob = _docx(_para("October 23 (Friday)- Parent-Teacher Conferences"))
    with patch("core.gmail.get_attachment", return_value=blob) as g:
        texts = extract_docx_attachments("msg-1", payload)
    g.assert_called_once_with("msg-1", "att-1")
    assert len(texts) == 1
    assert "Parent-Teacher Conferences" in texts[0]


def test_no_attachment_means_no_download():
    with patch("core.gmail.get_attachment") as g:
        assert extract_docx_attachments("msg-1", {"mimeType": "text/plain"}) == []
    g.assert_not_called()


def test_one_bad_attachment_does_not_lose_the_others():
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [
            {"mimeType": DOCX_MIME, "filename": "bad.docx", "body": {"attachmentId": "a"}},
            {"mimeType": DOCX_MIME, "filename": "good.docx", "body": {"attachmentId": "b"}},
        ],
    }
    good = _docx(_para("Pumpkin decorating Oct 26"))

    def fake(_msg, aid):
        if aid == "a":
            raise RuntimeError("download blew up")
        return good

    with patch("core.gmail.get_attachment", side_effect=fake):
        texts = extract_docx_attachments("msg-1", payload)
    assert len(texts) == 1
    assert "Pumpkin decorating Oct 26" in texts[0]


# ─── tools.py wiring ─────────────────────────────────────────────────────────

def test_tools_folds_docx_text_into_pdf_text():
    """Regression for the incident itself. extract.md tells the model to read
    `body`, `pdf_text` and `image_paths` — a new key would be ignored, so the
    Word text has to arrive in pdf_text or nothing downstream sees it."""
    src = (Path(__file__).parent.parent / "tools.py").read_text()
    assert "extract_docx_attachments" in src, \
        "tools.py must call extract_docx_attachments"
    assert "pdf_texts + doc_texts" in src, \
        "docx text must be folded into the pdf_text field the prompt reads"


def test_tools_does_not_gate_docx_on_a_has_flag():
    """The has_* flags are computed by a separate parser; gating on one is how
    the original drop stayed invisible."""
    src = (Path(__file__).parent.parent / "tools.py").read_text()
    call = src.split("doc_texts = ")[1].split("\n")[0]
    assert "has_" not in call
